# -*- coding: utf-8 -*-
"""Medidor de ahorro y efectividad (spec 001): detección de correcciones."""
import importlib.util
import json
import os
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_e = importlib.util.spec_from_file_location("medir", os.path.join(RAIZ, ".brain", "guardianes", "medir.py"))
medir = importlib.util.module_from_spec(_e)
_e.loader.exec_module(medir)


def chat(textos):
    lineas = []
    for i, t in enumerate(textos):
        lineas.append({"type": "user", "timestamp": "2026-11-01T10:00:00Z", "message": {"content": t}})
        lineas.append({"type": "user", "message": {"content": [{"type": "tool_result", "content": "x"}]}})
        lineas.append({"type": "user", "isMeta": True, "message": {"content": "meta"}})
        lineas.append({"type": "assistant", "uuid": "u%d" % i, "message": {"id": "m%d" % i, "usage": {
            "input_tokens": 10, "cache_creation_input_tokens": 100, "cache_read_input_tokens": 1000, "output_tokens": 50}}})
    return "\n".join(json.dumps(x) for x in lineas)


class TestMedir(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def escribir(self, nombre, textos):
        ruta = os.path.join(self.dir, nombre)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(chat(textos))
        return ruta

    def test_cuenta_turnos_y_correcciones(self):
        r = self.escribir("a.jsonl", ["Haz X", "No, así no", "otra vez, mal", "Perfecto, gracias"])
        d = medir.medir_chat(r)
        self.assertEqual(d["turnos"], 4)
        self.assertEqual(d["correcciones"], 2)

    def test_el_encargo_inicial_no_es_correccion(self):
        d = medir.medir_chat(self.escribir("b.jsonl", ["No toques nada fuera de X"]))
        self.assertEqual(d["correcciones"], 0)

    def test_tokens_nuevos_del_chat(self):
        r = self.escribir("c.jsonl", ["a", "b"])
        self.assertEqual(medir.medir_chat(r)["nuevos"], 220)

    def test_ignora_avisos_automaticos_y_filtra_por_tarea(self):
        self.escribir("e.jsonl", ["<system-reminder>aviso</system-reminder>\n[T3] Haz Y"])
        chats = medir.chats_de(self.dir)
        self.assertEqual(chats[0]["turnos"], 1)
        self.assertEqual(len(medir.chats_de(self.dir, tarea="[T3]")), 1)
        self.assertEqual(len(medir.chats_de(self.dir, tarea="[T1]")), 0)

    def test_coste_ponderado_y_cache_fria(self):
        r = self.escribir("f.jsonl", ["a", "b"])  # cada mensaje: 10 entrada, 100 escritura, 1000 lectura, 50 salida
        d = medir.medir_chat(r)
        por_mensaje = 10 + 100 * 1.25 + 1000 * 0.1 + 50 * 5
        self.assertAlmostEqual(d["coste"], 2 * por_mensaje)
        self.assertTrue(d["frio"])  # 1000 leídos < 50000

    def test_comparar_solo_con_la_misma_cache(self):
        import io
        import contextlib
        self.escribir("g.jsonl", ["a"])
        frio = medir.chats_de(self.dir)
        caliente = [dict(frio[0], frio=False)]
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            medir.comparar(frio, caliente)
        self.assertIn("no se compara", buf.getvalue())

    def test_comparar_calcula_diferencia(self):
        self.escribir("d.jsonl", ["a"])
        con = medir.chats_de(self.dir)
        sin = [dict(con[0], nuevos=con[0]["nuevos"] * 2)]
        self.assertEqual(medir.media(sin, "nuevos"), 220)
        self.assertEqual(medir.media(con, "nuevos"), 110)


class TestSkills(unittest.TestCase):
    """Informe 028 (3.2): uso real de las skills leído de los registros de los chats."""
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.proyecto = tempfile.mkdtemp()
        for n in ("traspaso-in", "pendiente", "nunca-usada"):
            os.makedirs(os.path.join(self.proyecto, ".claude", "skills", n))

    def chat(self, nombre, eventos):
        with open(os.path.join(self.dir, nombre), "w", encoding="utf-8") as f:
            f.write("\n".join(json.dumps(e) for e in eventos))

    def llamada(self, skill):
        return {"type": "assistant", "timestamp": "2026-11-08T10:00:00Z",
                "message": {"id": skill, "content": [{"type": "tool_use", "name": "Skill", "input": {"skill": skill}}]}}

    def comando(self, skill):
        return {"type": "user", "timestamp": "2026-11-07T10:00:00Z",
                "message": {"content": [{"type": "text", "text": "<command-name>/%s</command-name>" % skill}]}}

    def test_cuenta_llamadas_y_comandos_sin_sumar_el_mismo_uso(self):
        self.chat("a.jsonl", [self.comando("traspaso-in"), self.llamada("traspaso-in"), self.llamada("traspaso-in"), self.comando("pendiente")])
        self.assertEqual(medir.skills_usadas(os.path.join(self.dir, "a.jsonl")), {"traspaso-in": 2, "pendiente": 1})

    def test_tabla_incluye_las_no_usadas_con_cero_y_ordena(self):
        self.chat("a.jsonl", [self.llamada("traspaso-in"), self.llamada("plugin:traspaso-in")])
        self.chat("b.jsonl", [self.llamada("traspaso-in"), self.llamada("de-otro-proyecto")])
        tabla = medir.uso_de_skills(self.dir, self.proyecto)
        self.assertEqual([f[0] for f in tabla], ["traspaso-in", "nunca-usada", "pendiente"])
        self.assertEqual(tabla[0][1:3], (3, 2))
        self.assertEqual(tabla[1][1:3], (0, 0))

    def test_sin_registros_ni_skills_no_falla(self):
        self.assertEqual(medir.uso_de_skills(self.dir, tempfile.mkdtemp()), [])


class TestRitual(unittest.TestCase):
    """Informe 032: coste de rituales frente a trabajo y avisos del guardián."""
    def llamada(self, i, herramienta, entrada, salida=100):
        return {"type": "assistant", "message": {"id": "m%d" % i, "usage": {"input_tokens": 10, "output_tokens": salida},
                "content": [{"type": "tool_use", "name": herramienta, "input": entrada}]}}

    def test_clasifica_trabajo_memoria_chat_nuevo_y_aviso(self):
        d = tempfile.mkdtemp()
        proyecto = tempfile.mkdtemp()
        os.makedirs(os.path.join(proyecto, ".claude", "skills", "traspaso-in"))
        filas = [self.llamada(1, "Edit", {"file_path": "app.py"}),
                 self.llamada(2, "Bash", {"command": "python .brain/guardianes/cerrar.py x"}),
                 self.llamada(3, "mcp__ccd_session__start_session", {}),
                 {"type": "user", "message": {"content": "Stop hook feedback: Hito sin lección apuntada"}},
                 self.llamada(4, "Edit", {"file_path": "app.py"})]
        with open(os.path.join(d, "a.jsonl"), "w", encoding="utf-8") as f:
            f.write("\n".join(json.dumps(x) for x in filas))
        total, avisos, chats, llamadas = medir.ritual_de_proyecto(d, proyecto)
        self.assertEqual((chats, llamadas), (1, 4))
        for c in ("trabajo", "memoria", "chat_nuevo", "aviso"):
            self.assertGreater(total[c], 0, c)
        self.assertEqual(avisos, {"hito": 1})

    def test_descarta_chats_de_menos_de_3_llamadas_y_no_falla_sin_registros(self):
        d = tempfile.mkdtemp()
        with open(os.path.join(d, "a.jsonl"), "w", encoding="utf-8") as f:
            f.write(json.dumps(self.llamada(1, "Edit", {})))
        self.assertEqual(medir.ritual_de_proyecto(d, tempfile.mkdtemp())[2], 0)
        medir.imprimir_ritual({c: 0.0 for c in medir.CATEGORIAS}, {}, 0, 0)


if __name__ == "__main__":
    unittest.main()
