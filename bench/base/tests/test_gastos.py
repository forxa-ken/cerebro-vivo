# -*- coding: utf-8 -*-
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import gastos


class TestGastos(unittest.TestCase):
    def test_total_por_categoria(self):
        g = [{"fecha": "x", "categoria": "Ocio", "importe": 5.0}, {"fecha": "x", "categoria": "Ocio", "importe": 2.5}]
        self.assertEqual(gastos.por_categoria(g), {"Ocio": 7.5})

    def test_resumen_incluye_total(self):
        g = [{"fecha": "x", "categoria": "Ocio", "importe": 5.0}]
        self.assertIn("TOTAL", gastos.resumen(g))


if __name__ == "__main__":
    unittest.main()
