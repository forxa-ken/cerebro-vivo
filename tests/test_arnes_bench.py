# -*- coding: utf-8 -*-
"""Banco de la prueba de ahorro (spec 001, parte A): las carpetas gemelas se montan y el punto de partida NO cuenta como logrado."""
import os
import subprocess
import sys
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def correr(*args):
    return subprocess.run([sys.executable] + list(args), cwd=RAIZ, capture_output=True, text=True)


class TestBench(unittest.TestCase):
    def test_sin_arnes_monta_y_parte_sin_lograr(self):
        d = tempfile.mkdtemp()
        for tarea in ("t1", "t2", "t3"):
            self.assertEqual(correr("bench/montar.py", "sin", tarea, "--destino", d).returncode, 0)
            self.assertFalse(os.path.isdir(os.path.join(d, "sin_arnes", ".brain")))
            self.assertNotEqual(correr("bench/verificar.py", "sin", tarea, "--destino", d).returncode, 0, tarea)

    def test_con_arnes_trae_el_metodo_y_t3_trae_traspaso(self):
        d = tempfile.mkdtemp()
        self.assertEqual(correr("bench/montar.py", "con", "t3", "--destino", d).returncode, 0)
        self.assertTrue(os.path.isfile(os.path.join(d, "con_arnes", ".brain", "traspaso.md")))
        self.assertTrue(os.path.isfile(os.path.join(d, "con_arnes", ".brain", "guardianes", "medir.py")))

    def test_remontar_mueve_a_historial_sin_borrar(self):
        d = tempfile.mkdtemp()
        correr("bench/montar.py", "sin", "t1", "--destino", d)
        open(os.path.join(d, "sin_arnes", "huella.txt"), "w").close()
        correr("bench/montar.py", "sin", "t2", "--destino", d)
        hist = os.path.join(d, "_historial")
        self.assertTrue(any(os.path.exists(os.path.join(hist, n, "huella.txt")) for n in os.listdir(hist)))


if __name__ == "__main__":
    unittest.main()
