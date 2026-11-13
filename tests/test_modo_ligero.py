# -*- coding: utf-8 -*-
"""Modo ligero (spec 002): el guardián de cierre escribe él mismo la línea en tareas pequeñas, no sensibles y en verde."""
import importlib.util
import json
import os
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
G = os.path.join(RAIZ, ".brain", "guardianes")
_e = importlib.util.spec_from_file_location("cierre", os.path.join(G, "cierre.py"))
cierre = importlib.util.module_from_spec(_e)
_e.loader.exec_module(cierre)
with open(os.path.join(G, "guardianes.json"), encoding="utf-8") as f:
    CFG = json.load(f)


def registro(*bloques):
    return "\n".join(json.dumps(b) for b in bloques)


def usuario(texto):
    return {"type": "user", "message": {"content": texto}}


def edita(ruta, id_="e1"):
    return {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": id_, "name": "Edit", "input": {"file_path": ruta}}]}}


def corre_pruebas(id_, resultado):
    return [{"type": "assistant", "message": {"content": [{"type": "tool_use", "id": id_, "name": "Bash", "input": {"command": "python -m unittest discover tests"}}]}},
            {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": id_, "content": resultado}]}}]


class TestModoLigero(unittest.TestCase):
    def test_tarea_pequena_en_verde_cierra_sola(self):
        self.assertIn("gastos.py", cierre.cierre_ligero(CFG, ["gastos.py", "tests/test_gastos.py"], True))

    def test_sin_pruebas_o_en_rojo_no(self):
        self.assertIsNone(cierre.cierre_ligero(CFG, ["gastos.py"], None))
        self.assertIsNone(cierre.cierre_ligero(CFG, ["gastos.py"], False))

    def test_tres_archivos_no(self):
        self.assertIsNone(cierre.cierre_ligero(CFG, ["a.py", "b.py", "c.py"], True))

    def test_archivo_sensible_no(self):
        self.assertIsNone(cierre.cierre_ligero(CFG, ["pagos.py"], True))
        self.assertIsNone(cierre.cierre_ligero(CFG, ["app/login.py"], True))

    def test_si_toca_el_cerebro_no(self):
        self.assertIsNone(cierre.cierre_ligero(CFG, ["gastos.py", ".brain/pendientes.md"], True))

    def test_apagado(self):
        self.assertIsNone(cierre.cierre_ligero(dict(CFG, modo_ligero_activo=False), ["gastos.py"], True))

    def test_detalle_lee_archivos_y_verde(self):
        d = tempfile.mkdtemp()
        ruta = os.path.join(d, "t.jsonl")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(registro(usuario("haz X"), edita(os.path.join(d, "gastos.py")), *corre_pruebas("b1", "Ran 3 tests\n\nOK")))
        self.assertEqual(cierre.detalle_respuesta(ruta, d), (["gastos.py"], True))

    def test_detalle_en_rojo_y_mensaje_nuevo_reinicia(self):
        d = tempfile.mkdtemp()
        ruta = os.path.join(d, "t.jsonl")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(registro(usuario("uno"), edita(os.path.join(d, "a.py")), *corre_pruebas("b1", "FAILED (failures=1)"),
                             usuario("dos"), edita(os.path.join(d, "b.py")), *corre_pruebas("b2", "Ran 1 test\n\nOK")))
        self.assertEqual(cierre.detalle_respuesta(ruta, d), (["b.py"], True))
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(registro(usuario("uno"), edita(os.path.join(d, "a.py")), *corre_pruebas("b1", "FAILED (failures=1)")))
        self.assertEqual(cierre.detalle_respuesta(ruta, d), (["a.py"], False))

    def test_linea_automatica_marcada(self):
        d = tempfile.mkdtemp()
        os.makedirs(os.path.join(d, ".brain"))
        cierre.escribir_linea_auto(d, CFG, "(auto) tocó a.py; pruebas en verde")
        with open(os.path.join(d, CFG["registro"]), encoding="utf-8") as f:
            linea = f.read()
        self.assertIn("Claude (auto)", linea)
        self.assertIn(" | auto | Claude (auto) | ", linea)  # spec 048: tipo fijo
        self.assertTrue(linea.endswith("| Cambio pequeño\n"))

    def test_carril_nuevo_y_alias_antiguo(self):
        import cerrar
        for c in ("Cambio pequeño", "Small change", "Fast-Track", "SDD"):
            self.assertTrue(cerrar.linea_registro("2026-11-10", "Claude", "x #1", "hecho", c, CFG).endswith("| " + c))

    def test_no_repite_la_misma_linea(self):
        d = tempfile.mkdtemp()
        os.makedirs(os.path.join(d, ".brain"))
        for _ in range(2):
            cierre.escribir_linea_auto(d, CFG, "(auto) tocó a.py; pruebas en verde")
        with open(os.path.join(d, CFG["registro"]), encoding="utf-8") as f:
            self.assertEqual(len(f.read().splitlines()), 1)


if __name__ == "__main__":
    unittest.main()
