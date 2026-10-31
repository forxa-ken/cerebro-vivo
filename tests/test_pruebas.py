# -*- coding: utf-8 -*-
"""Guardián 11 (spec 053): memoria de pruebas indexada; la línea de arranque solo sale con hallazgos abiertos."""
import importlib.util
import os
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_espec = importlib.util.spec_from_file_location("pruebas", os.path.join(RAIZ, ".brain", "guardianes", "pruebas.py"))
pr = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(pr)
CFG = {"pruebas_activo": True, "pruebas": {"carpeta": "pruebas"}}


def montar(detalle, indexar=True, archivos_extra=()):
    raiz = tempfile.mkdtemp()
    car = os.path.join(raiz, "pruebas")
    os.makedirs(car)
    fila = "| P-001 | 2026-01-01 | Web | Darwin | [P-001-x.md](P-001-x.md) |\n" if indexar else ""
    with open(os.path.join(car, "indice.md"), "w", encoding="utf-8") as f:
        f.write("| ID | Fecha | Área | Quién | Archivo |\n| :--- | :--- | :--- | :--- | :--- |\n" + fila)
    if detalle is not None:
        with open(os.path.join(car, "P-001-x.md"), "w", encoding="utf-8") as f:
            f.write(detalle)
    for n in archivos_extra:
        open(os.path.join(car, n), "w", encoding="utf-8").close()
    return raiz


class TestPruebas(unittest.TestCase):
    def test_cuenta_solo_abiertos(self):
        raiz = montar("## Hallazgos\n- [ ] falla A\n- [x] ya cerrado\n- [ ] falla B\n")
        abiertos, problemas = pr.analizar(raiz, pr.ajustes(CFG))
        self.assertEqual([t for _, t in abiertos], ["falla A", "falla B"])
        self.assertEqual(problemas, [])
        self.assertIn("2 hallazgo(s)", pr.resumen(raiz, CFG)[0])

    def test_todo_cerrado_no_imprime_nada(self):
        raiz = montar("- [x] cerrado\n")
        self.assertEqual(pr.resumen(raiz, CFG), [])

    def test_incoherencias(self):
        self.assertIn("falta el archivo", pr.analizar(montar(None), pr.ajustes(CFG))[1][0])
        raiz = montar("- [x] ok\n", indexar=False)
        self.assertIn("no está en el índice", pr.analizar(raiz, pr.ajustes(CFG))[1][0])
        self.assertTrue(pr.resumen(raiz, CFG))

    def test_apagado_y_fallo_callan(self):
        raiz = montar("- [ ] abierto\n")
        self.assertEqual(pr.resumen(raiz, {"pruebas_activo": False, "pruebas": CFG["pruebas"]}), [])
        self.assertEqual(pr.resumen(tempfile.mkdtemp(), CFG), [])

    def test_repositorio_real_coherente(self):
        _, problemas = pr.analizar(RAIZ, pr.ajustes(pr.cargar_config()))
        self.assertEqual(problemas, [])


if __name__ == "__main__":
    unittest.main()
