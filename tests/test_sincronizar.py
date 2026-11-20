# -*- coding: utf-8 -*-
"""Spec 093: sincronizar.py baja de GitHub sin mezclar, pisar ni subir nada."""
import os
import subprocess
import sys
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(RAIZ, ".brain", "guardianes"))
import sincronizar  # noqa: E402
import textos  # noqa: E402


def g(carpeta, *args):
    r = subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false"] + list(args),
                       cwd=carpeta, capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, r.stderr
    return r.stdout


def escribir(carpeta, nombre, texto):
    with open(os.path.join(carpeta, nombre), "w", encoding="utf-8") as f:
        f.write(texto)


class TestSincronizar(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = self.tmp.name
        self.origen = os.path.join(base, "origen.git")
        self.a = os.path.join(base, "a")
        self.b = os.path.join(base, "b")
        os.makedirs(self.a)
        g(base, "init", "--bare", "-b", "main", self.origen)
        g(self.a, "init", "-b", "main")
        g(self.a, "remote", "add", "origin", self.origen)
        escribir(self.a, "x.txt", "1\n")
        g(self.a, "add", ".")
        g(self.a, "commit", "-m", "uno")
        g(self.a, "push", "-u", "origin", "main")
        g(base, "clone", self.origen, self.b)

    def tearDown(self):
        self.tmp.cleanup()

    def subir_desde_a(self, nombre="y.txt"):
        escribir(self.a, nombre, "2\n")
        g(self.a, "add", ".")
        g(self.a, "commit", "-m", "dos")
        g(self.a, "push")

    def test_al_dia(self):
        lineas, ok = sincronizar.sincronizar(self.b, lengua="es")
        self.assertTrue(ok)
        self.assertIn("al día", lineas[0])

    def test_baja_lo_nuevo(self):
        self.subir_desde_a()
        lineas, ok = sincronizar.sincronizar(self.b, lengua="es")
        self.assertTrue(ok)
        self.assertIn("Bajados 1", lineas[0])
        self.assertTrue(os.path.isfile(os.path.join(self.b, "y.txt")))

    def test_simular_no_toca(self):
        self.subir_desde_a()
        lineas, ok = sincronizar.sincronizar(self.b, simular=True, lengua="es")
        self.assertTrue(ok)
        self.assertIn("Bajaría 1", lineas[0])
        self.assertFalse(os.path.isfile(os.path.join(self.b, "y.txt")))

    def test_rama_separada_no_toca(self):
        self.subir_desde_a()
        escribir(self.b, "z.txt", "3\n")
        g(self.b, "add", ".")
        g(self.b, "commit", "-m", "local")
        lineas, ok = sincronizar.sincronizar(self.b, lengua="es")
        self.assertFalse(ok)
        self.assertIn("se separó", lineas[0])
        self.assertFalse(os.path.isfile(os.path.join(self.b, "y.txt")))

    def test_choque_con_cambios_locales(self):
        self.subir_desde_a("x.txt")
        escribir(self.b, "x.txt", "cambio local\n")
        lineas, ok = sincronizar.sincronizar(self.b, lengua="es")
        self.assertFalse(ok)
        self.assertIn("No pude bajar", lineas[0])
        with open(os.path.join(self.b, "x.txt"), encoding="utf-8") as f:
            self.assertEqual(f.read(), "cambio local\n")

    def test_commits_sin_subir_se_avisan_y_no_se_suben(self):
        escribir(self.b, "z.txt", "3\n")
        g(self.b, "add", ".")
        g(self.b, "commit", "-m", "local")
        lineas, ok = sincronizar.sincronizar(self.b, lengua="es")
        self.assertTrue(ok)
        self.assertTrue(any("sin subir" in x for x in lineas))
        self.assertEqual(g(self.origen, "rev-list", "--count", "main").strip(), "1")

    def test_sin_remoto_y_fuera_de_git(self):
        sin = os.path.join(self.tmp.name, "sin")
        os.makedirs(sin)
        self.assertFalse(sincronizar.sincronizar(sin, lengua="es")[1])
        g(sin, "init", "-b", "main")
        lineas, ok = sincronizar.sincronizar(sin, lengua="es")
        self.assertFalse(ok)
        self.assertIn("remoto", lineas[0])

    def test_textos_es_en_paridad(self):
        claves = [k for k in textos.TEXTOS["es"] if k.startswith("sync_")]
        self.assertTrue(claves)
        for k in claves:
            self.assertIn(k, textos.TEXTOS["en"], k)
        self.assertEqual(set(claves), {k for k in textos.TEXTOS["en"] if k.startswith("sync_")})


if __name__ == "__main__":
    unittest.main()
