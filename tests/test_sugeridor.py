# -*- coding: utf-8 -*-
"""Spec 095: el sugeridor avisa de correcciones, decisiones y órdenes repetidas sin apuntar, y solo sugiere."""
import importlib.util
import json
import os
import shutil
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_espec = importlib.util.spec_from_file_location("sugeridor", os.path.join(RAIZ, ".brain", "guardianes", "sugeridor.py"))
sugeridor = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(sugeridor)

CFG = {"sugeridor_activo": True, "sugeridor_max": 3, "sugeridor_repeticiones": 3, "sugeridor_dedup_puntos": 40, "idioma": "es"}


def dicho(texto):
    return {"type": "user", "message": {"content": texto}}


def uso(nombre, entrada):
    return {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "x", "name": nombre, "input": entrada}]}}


class TestSugeridor(unittest.TestCase):
    def setUp(self):
        self.raiz = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.raiz, True)
        self.registro = os.path.join(self.raiz, "chat.jsonl")

    def avisos(self, eventos, cfg=None):
        with open(self.registro, "w", encoding="utf-8") as f:
            for e in eventos:
                f.write(json.dumps(e) + "\n")
        return sugeridor.avisos(self.registro, cfg or CFG, self.raiz)

    def lecciones(self, texto):
        os.makedirs(os.path.join(self.raiz, ".brain", "lecciones"))
        with open(os.path.join(self.raiz, ".brain", "lecciones", "tema.md"), "w", encoding="utf-8") as f:
            f.write(texto)

    def test_sin_senales_calla(self):
        self.assertEqual(self.avisos([dicho("hazme una tabla de los pendientes"), uso("Bash", {"command": "ls"})]), [])

    def test_correccion_avisa(self):
        r = self.avisos([dicho("no, así no: usa Edit y no un heredoc")])
        self.assertEqual(len(r), 1)
        self.assertIn("Darwin corrigió", r[0])
        self.assertIn("ninguna", r[0])

    def test_decision_avisa(self):
        r = self.avisos([dicho("vamos con la opción dos, descartado lo demás")])
        self.assertEqual(len(r), 1)
        self.assertIn("decisión", r[0])

    def test_orden_repetida_avisa_a_las_tres(self):
        orden = uso("Bash", {"command": "python tools/regenerar_informe.py --todo"})
        self.assertEqual(self.avisos([orden, orden]), [])
        r = self.avisos([orden, orden, orden])
        self.assertEqual(len(r), 1)
        self.assertIn("3 veces", r[0])

    def test_ordenes_de_oficio_no_cuentan(self):
        pruebas = uso("Bash", {"command": "python -m unittest discover tests"})
        lectura = uso("Bash", {"command": "grep -rn tope .brain/guardianes"})
        git = uso("PowerShell", {"command": "git status --short"})
        self.assertEqual(self.avisos([pruebas] * 4 + [lectura] * 4 + [git] * 4), [])

    def test_mensajes_de_hooks_y_recordatorios_no_son_de_darwin(self):
        r = self.avisos([dicho("<system-reminder>no, así no, otra vez</system-reminder>"),
                         dicho("Stop hook feedback: te dije que no"),
                         {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "x", "content": "no, así no"}]}}])
        self.assertEqual(r, [])

    def test_una_leccion_apuntada_reinicia_la_cuenta(self):
        r = self.avisos([dicho("te dije que no"), uso("Bash", {"command": "python .brain/guardianes/lecciones.py ninguna \"nada\""})])
        self.assertEqual(r, [])
        r = self.avisos([dicho("te dije que no"), uso("Write", {"file_path": self.raiz + "/.brain/lecciones/tema.md", "content": "x"}),
                         dicho("otra vez lo mismo")])
        self.assertEqual(len(r), 1)  # solo cuenta lo posterior a la marca

    def test_propuesta_en_propuestas_md_tambien_reinicia(self):
        r = self.avisos([dicho("mal, te dije que no"), uso("Edit", {"file_path": self.raiz + "/.brain/propuestas.md", "new_string": "x"})])
        self.assertEqual(r, [])

    def test_no_repite_lo_que_la_memoria_ya_recoge(self):
        frase = "no, así no: usa Edit y no un heredoc con comillas rotas"
        self.lecciones("# Heredocs\n\n- **heredoc con comillas rotas** → usa Edit y no un heredoc así no → **escribe con Edit**\n")
        self.assertEqual(self.avisos([dicho(frase)]), [])

    def test_maximo_de_senales_por_aviso(self):
        eventos = [dicho("no, tema %d distinto" % i) for i in range(6)]
        r = self.avisos(eventos)
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0].count("Darwin corrigió"), 3)

    def test_apagado_calla(self):
        self.assertEqual(self.avisos([dicho("no, así no")], dict(CFG, sugeridor_activo=False)), [])

    def test_auto_solo_en_el_repo_del_arnes(self):
        cfg = dict(CFG, sugeridor_activo="auto")
        self.assertEqual(self.avisos([dicho("no, así no")], cfg), [])  # sin manifiesto.json: es un proyecto
        with open(os.path.join(self.raiz, "manifiesto.json"), "w") as f:
            f.write("{}")
        self.assertEqual(len(self.avisos([dicho("no, así no")], cfg)), 1)

    def test_aviso_en_ingles(self):
        r = self.avisos([dicho("no, así no")], dict(CFG, idioma="en"))
        self.assertIn("Darwin corrected", r[0])

    def test_registro_roto_o_inexistente_no_falla(self):
        self.assertEqual(sugeridor.avisos(os.path.join(self.raiz, "no-existe.jsonl"), CFG, self.raiz), [])
        with open(self.registro, "w", encoding="utf-8") as f:
            f.write("esto no es json\n{")
        self.assertEqual(sugeridor.avisos(self.registro, CFG, self.raiz), [])


if __name__ == "__main__":
    unittest.main()
