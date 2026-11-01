# -*- coding: utf-8 -*-
"""Medidor de ahorro y efectividad (spec 001): totales iguales a uso_tokens y detección de correcciones."""
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

    def test_tokens_iguales_a_uso_tokens(self):
        r = self.escribir("c.jsonl", ["a", "b"])
        self.assertEqual(medir.medir_chat(r)["nuevos"], medir.uso.leer_chat(r)["nuevos"])
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


if __name__ == "__main__":
    unittest.main()
