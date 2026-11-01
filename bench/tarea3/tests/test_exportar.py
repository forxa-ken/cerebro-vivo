# -*- coding: utf-8 -*-
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import gastos


class TestExportar(unittest.TestCase):
    def test_escribe_json_valido(self):
        ruta = os.path.join(tempfile.mkdtemp(), "s.json")
        gastos.exportar_json([{"fecha": "x", "categoria": "Ocio", "importe": 5.0}], ruta)
        with open(ruta, encoding="utf-8") as f:
            json.load(f)


if __name__ == "__main__":
    unittest.main()
