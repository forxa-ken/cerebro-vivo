# -*- coding: utf-8 -*-
"""Spec 026: el guardián de hitos exige apuntar la lección en el momento."""
import importlib.util
import json
import os
import shutil
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_espec = importlib.util.spec_from_file_location("hitos", os.path.join(RAIZ, ".brain", "guardianes", "hitos.py"))
hitos = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(hitos)

CFG = {"lecciones_activas": True, "lecciones_vigiladas": {"video": ["lanzador*.py"]}, "hitos_max_archivos": 3, "hitos_errores_min": 1,
       "ignorar_cambios": [".brain/*", ".claude/*"], "traspaso_corto_max": 2500}
_n = [0]


def uso(nombre, entrada):
    _n[0] += 1
    i = "t%d" % _n[0]
    return i, {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": i, "name": nombre, "input": entrada}]}}


def resultado(i, texto, error=False):
    return {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": i, "content": texto, "is_error": error}]}}


class TestHitos(unittest.TestCase):
    def setUp(self):
        self.raiz = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.raiz, True)
        self.registro = os.path.join(self.raiz, "chat.jsonl")

    def avisos(self, eventos, cfg=None):
        with open(self.registro, "w", encoding="utf-8") as f:
            for e in eventos:
                f.write(json.dumps(e) + "\n")
        return hitos.avisos(self.registro, cfg or CFG, self.raiz)

    def ruta(self, rel):
        return os.path.join(self.raiz, rel)

    def test_sin_senales_no_avisa(self):
        i, u = uso("Bash", {"command": "ls"})
        self.assertEqual(self.avisos([u, resultado(i, "ok")]), [])

    def test_error_resuelto_avisa(self):
        i1, u1 = uso("Bash", {"command": "python x.py"})
        i2, u2 = uso("Edit", {"file_path": self.ruta("x.py")})
        i3, u3 = uso("Bash", {"command": "python x.py"})
        ev = [u1, resultado(i1, "Traceback (most recent call last)", True), u2, resultado(i2, "ok"), u3, resultado(i3, "bien")]
        self.assertEqual(len(self.avisos(ev)), 1)

    def test_otro_comando_que_funciona_no_resuelve_el_error(self):
        i1, u1 = uso("Bash", {"command": "ls carpeta_que_no_existe"})
        i2, u2 = uso("Edit", {"file_path": self.ruta("x.py")})
        i3, u3 = uso("Bash", {"command": "git status"})
        ev = [u1, resultado(i1, "No such file", True), u2, resultado(i2, "ok"), u3, resultado(i3, "limpio")]
        self.assertEqual(self.avisos(ev), [])

    def test_mismo_script_con_otros_argumentos_si_resuelve_el_error(self):
        i1, u1 = uso("Bash", {"command": 'cd "x" && python .brain/g.py --a'})
        i2, u2 = uso("Edit", {"file_path": self.ruta("g.py")})
        i3, u3 = uso("Bash", {"command": "python .brain/g.py --b | tail -3"})
        ev = [u1, resultado(i1, "Traceback", True), u2, resultado(i2, "ok"), u3, resultado(i3, "bien")]
        self.assertEqual(len(self.avisos(ev)), 1)

    def test_leer_codigo_con_la_palabra_error_no_es_un_fallo(self):
        i1, u1 = uso("Read", {"file_path": self.ruta("x.py")})
        i2, u2 = uso("Edit", {"file_path": self.ruta("x.py")})
        i3, u3 = uso("Read", {"file_path": self.ruta("x.py")})
        ev = [u1, resultado(i1, "def hito_error(): raise ValueError  # Error aqui"), u2, resultado(i2, "ok"), u3, resultado(i3, "bien")]
        self.assertEqual(self.avisos(ev), [])

    def test_consola_que_imprime_la_palabra_error_sin_fallar_no_cuenta(self):
        i1, u1 = uso("Bash", {"command": "grep -n error x.py"})
        i2, u2 = uso("Edit", {"file_path": self.ruta("x.py")})
        i3, u3 = uso("Bash", {"command": "grep -n error x.py"})
        ev = [u1, resultado(i1, "3: manejo de error"), u2, resultado(i2, "ok"), u3, resultado(i3, "3: manejo de error")]
        self.assertEqual(self.avisos(ev), [])

    def test_fallo_real_de_consola_sigue_contando(self):
        i1, u1 = uso("Bash", {"command": "python x.py"})
        i2, u2 = uso("Edit", {"file_path": self.ruta("x.py")})
        i3, u3 = uso("Bash", {"command": "python x.py"})
        ev = [u1, resultado(i1, "Traceback (most recent call last):\n  ...\nValueError: mal"), u2, resultado(i2, "ok"), u3, resultado(i3, "bien")]
        self.assertEqual(len(self.avisos(ev)), 1)

    def test_error_sin_resolver_no_avisa(self):
        i1, u1 = uso("Bash", {"command": "python x.py"})
        self.assertEqual(self.avisos([u1, resultado(i1, "Traceback", True)]), [])

    def test_archivo_vigilado_avisa(self):
        i, u = uso("Edit", {"file_path": self.ruta("lanzador_video.py")})
        self.assertEqual(len(self.avisos([u, resultado(i, "ok")])), 1)

    def test_modificacion_grande_avisa_y_brain_no_cuenta(self):
        ev = []
        for n in ("a.py", "b.py", ".brain/c.md"):
            i, u = uso("Write", {"file_path": self.ruta(n)})
            ev += [u, resultado(i, "ok")]
        self.assertEqual(self.avisos(ev), [])
        i, u = uso("Write", {"file_path": self.ruta("d.py")})
        ev += [u, resultado(i, "ok")]
        i, u = uso("Write", {"file_path": self.ruta("e.py")})
        ev += [u, resultado(i, "ok")]
        self.assertEqual(len(self.avisos(ev)), 1)

    def test_apuntar_leccion_o_ninguna_cierra_el_hito(self):
        i, u = uso("Edit", {"file_path": self.ruta("lanzador_video.py")})
        j, m = uso("Bash", {"command": 'python .brain/guardianes/lecciones.py ninguna "cosmetico"'})
        self.assertEqual(self.avisos([u, resultado(i, "ok"), m, resultado(j, "ok")]), [])

    def test_leccion_lanzada_con_powershell_tambien_cierra_el_hito(self):
        i, u = uso("Edit", {"file_path": self.ruta("lanzador_video.py")})
        j, m = uso("PowerShell", {"command": 'python .brain/guardianes/lecciones.py ninguna "cosmetico"'})
        self.assertEqual(self.avisos([u, resultado(i, "ok"), m, resultado(j, "ok")]), [])

    def test_senal_nueva_tras_la_leccion_vuelve_a_avisar(self):
        i, u = uso("Edit", {"file_path": self.ruta("lanzador_video.py")})
        j, m = uso("Bash", {"command": "python .brain/guardianes/lecciones.py --tema video 'a | b | c'"})
        k, u2 = uso("Edit", {"file_path": self.ruta("lanzador_otro.py")})
        self.assertEqual(len(self.avisos([u, resultado(i, "ok"), m, resultado(j, "ok"), u2, resultado(k, "ok")])), 1)

    def test_desactivado_no_avisa(self):
        i, u = uso("Edit", {"file_path": self.ruta("lanzador_video.py")})
        cfg = dict(CFG, lecciones_activas=False)
        self.assertEqual(self.avisos([u, resultado(i, "ok")], cfg), [])

    def test_traspaso_corto_demasiado_largo_avisa(self):
        i, u = uso("Write", {"file_path": self.ruta(".brain/traspaso.md"), "content": "x" * 3000})
        self.assertEqual(len(self.avisos([u, resultado(i, "ok")])), 1)
        i, u = uso("Write", {"file_path": self.ruta(".brain/traspaso.md"), "content": "x" * 1000})
        self.assertEqual(self.avisos([u, resultado(i, "ok")]), [])

    def test_registro_inexistente_calla(self):
        self.assertEqual(hitos.avisos(os.path.join(self.raiz, "no.jsonl"), CFG, self.raiz), [])


if __name__ == "__main__":
    unittest.main()
