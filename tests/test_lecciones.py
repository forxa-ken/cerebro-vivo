# -*- coding: utf-8 -*-
"""Spec 026: lecciones.py escribe lecciones en .brain/lecciones/ sin duplicar."""
import datetime
import importlib.util
import os
import shutil
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_espec = importlib.util.spec_from_file_location("lecciones", os.path.join(RAIZ, ".brain", "guardianes", "lecciones.py"))
lecciones = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(lecciones)


class TestLecciones(unittest.TestCase):
    def setUp(self):
        self.raiz = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.raiz, True)

    def leer(self, rel):
        with open(os.path.join(self.raiz, rel), encoding="utf-8") as f:
            return f.read()

    def test_escribe_la_leccion_y_el_indice(self):
        r = lecciones.agregar(self.raiz, "Video", "falla el lanzador", "ruta mal", "usar ruta absoluta", hoy=datetime.date(2026, 11, 7))
        self.assertEqual(r, "nueva")
        txt = self.leer(".brain/lecciones/video.md")
        self.assertIn("- **falla el lanzador** → ruta mal → **usar ruta absoluta** (2026-11-07)", txt)
        self.assertIn("[video](video.md) | 1", self.leer(".brain/lecciones/indice.md"))

    def test_no_repite_la_misma_leccion(self):
        lecciones.agregar(self.raiz, "video", "Falla X", "a", "Hacer Y")
        self.assertEqual(lecciones.agregar(self.raiz, "video", "falla x", "otra causa", "hacer y"), "repetida")
        self.assertEqual(lecciones.contar(os.path.join(self.raiz, ".brain", "lecciones", "video.md")), 1)

    def test_tema_se_limpia(self):
        self.assertEqual(lecciones.limpiar_tema(" Vídeo Raro/../x "), "v-deo-raro-x")
        self.assertEqual(lecciones.limpiar_tema(""), "general")

    def test_falta_problema_o_regla(self):
        with self.assertRaises(ValueError):
            lecciones.agregar(self.raiz, "video", "", "c", "r")
        with self.assertRaises(ValueError):
            lecciones.agregar(self.raiz, "video", "p", "c", " ")

    def test_resumen_de_temas(self):
        self.assertEqual(lecciones.resumen_temas(self.raiz), "")
        lecciones.agregar(self.raiz, "video", "p1", "", "r1")
        lecciones.agregar(self.raiz, "video", "p2", "", "r2")
        lecciones.agregar(self.raiz, "metodo", "p3", "", "r3")
        self.assertEqual(lecciones.resumen_temas(self.raiz), "metodo (1), video (2)")


if __name__ == "__main__":
    unittest.main()
