# -*- coding: utf-8 -*-
"""Banco de la prueba del índice (spec 004): los tres lados se montan bien, el lado c trae 5 filas falsas y las respuestas se juzgan."""
import os
import subprocess
import sys
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(RAIZ, "bench", "indice"))
import montar  # noqa: E402
from preguntas import juzgar  # noqa: E402

INDICE = """# Índice
| ID | Decisión | Área | Estado |
| :--- | :--- | :--- | :--- |
| [D-053](D-053-a.md) | desc 53 | Negocio | vigente |
| [D-054](D-054-b.md) | desc 54 | Negocio | vigente |
| [D-055](D-055-c.md) | desc 55 | Proceso | vigente |
| [D-056](D-056-d.md) | desc 56 | Proceso | vigente |
| [D-062](D-062-e.md) | desc 62 | Negocio | vigente |
| [D-065](D-065-f.md) | desc 65 | Negocio | vigente |
"""


def origen_falso():
    o = os.path.join(tempfile.mkdtemp(), ".brain")
    os.makedirs(os.path.join(o, "decisions"))
    os.makedirs(os.path.join(o, "archive"))
    for ruta, txt in ((("decisions", "indice.md"), INDICE), (("decisions", "D-062-e.md"), "ficha"),
                      (("archive", "hechos.md"), "## 1\nx"), (("archive", "hechos-indice.md"), "| 1 | x |")):
        with open(os.path.join(o, *ruta), "w", encoding="utf-8") as f:
            f.write(txt)
    return o


def correr(*args):
    return subprocess.run([sys.executable, os.path.join(RAIZ, "bench", "indice", "montar.py")] + list(args), capture_output=True, text=True)


class TestBenchIndice(unittest.TestCase):
    def test_lados_a_b_c(self):
        o, d = origen_falso(), tempfile.mkdtemp()
        for lado in "abc":
            self.assertEqual(correr(lado, "1", "--origen", o, "--destino", d).returncode, 0)
        ind = lambda l: os.path.join(d, "lado_" + l, ".brain", "decisions", "indice.md")  # noqa: E731
        self.assertTrue(os.path.isfile(ind("a")))
        self.assertFalse(os.path.exists(ind("b")))
        self.assertFalse(os.path.exists(os.path.join(d, "lado_b", ".brain", "archive", "hechos-indice.md")))
        with open(os.path.join(d, "lado_a", "CLAUDE.md"), encoding="utf-8") as f:
            self.assertIn("indice.md", f.read())
        with open(os.path.join(d, "lado_b", "CLAUDE.md"), encoding="utf-8") as f:
            self.assertNotIn("indice.md", f.read())

    def test_lado_c_estropea_cinco_filas_y_el_origen_no_cambia(self):
        o, d = origen_falso(), tempfile.mkdtemp()
        antes = open(os.path.join(o, "decisions", "indice.md"), encoding="utf-8").read()
        correr("c", "2", "--origen", o, "--destino", d)
        c = open(os.path.join(d, "lado_c", ".brain", "decisions", "indice.md"), encoding="utf-8").read()
        self.assertIn("[D-054](D-062-e.md)", c)
        self.assertNotEqual(c, antes)
        self.assertEqual(montar.estropear(antes)[1], 5)
        self.assertEqual(open(os.path.join(o, "decisions", "indice.md"), encoding="utf-8").read(), antes)

    def test_remontar_mueve_a_historial(self):
        o, d = origen_falso(), tempfile.mkdtemp()
        correr("a", "1", "--origen", o, "--destino", d)
        correr("a", "1", "--origen", o, "--destino", d)
        self.assertTrue(os.listdir(os.path.join(d, "_historial")))

    def test_nombres_planos(self):
        o, d = origen_falso(), tempfile.mkdtemp()
        self.assertEqual(correr("c", "1", "--origen", o, "--destino", d, "--nombres-planos").returncode, 0)
        dec = os.path.join(d, "lado_c", ".brain", "decisions")
        self.assertTrue(os.path.isfile(os.path.join(dec, "D-062.md")))
        self.assertFalse(os.path.exists(os.path.join(dec, "D-062-e.md")))
        with open(os.path.join(dec, "indice.md"), encoding="utf-8") as f:
            t = f.read()
        self.assertNotRegex(t, r"D-\d+-[a-z]\.md")
        self.assertIn("(D-062.md)", t)  # c cruza D-054 con D-062: aun asi los enlaces son planos
        self.assertTrue(os.path.isfile(os.path.join(o, "decisions", "D-062-e.md")))  # el origen no cambia

    def test_origen_inexistente_falla(self):
        self.assertNotEqual(correr("a", "1", "--origen", os.path.join(tempfile.mkdtemp(), "no"), "--destino", tempfile.mkdtemp()).returncode, 0)

    def test_juzgar(self):
        self.assertEqual(juzgar(1, "10.000 créditos por $9.99"), "acierta")
        self.assertEqual(juzgar(1, "5.000 créditos por 4,99"), "falla")
        self.assertEqual(juzgar(2, "15 flujos y 8 acciones"), "acierta")
        self.assertEqual(juzgar(3, "Del 000000000000000001 al …006; un ID real nunca empieza por 15 ceros"), "acierta")
        self.assertEqual(juzgar(4, "30 días"), "acierta")
        self.assertEqual(juzgar(5, "No consta en la memoria."), "acierta")
        self.assertEqual(juzgar(5, "Se decidió aceptar Bizum desde noviembre."), "inventa")

    @unittest.skipUnless(os.path.isdir(montar.ORIGEN), "LoboHook no está en esta máquina")
    def test_respuestas_estan_en_las_fichas_reales(self):
        """Solo lectura sobre LoboHook: los datos de las preguntas existen y Bizum no."""
        def leer(sub):
            t = ""
            for r, _, fs in os.walk(os.path.join(montar.ORIGEN, sub)):
                for n in fs:
                    if n.endswith(".md"):
                        with open(os.path.join(r, n), encoding="utf-8", errors="replace") as f:
                            t += f.read()
            return t
        todo = leer("decisions") + leer("archive")
        for dato in ("10.000 ($9.99", "15 y 8", "15 ceros", "30 días de aviso"):
            self.assertIn(dato, todo, dato)
        self.assertNotIn("bizum", todo.lower())


if __name__ == "__main__":
    unittest.main()
