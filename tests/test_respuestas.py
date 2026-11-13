# -*- coding: utf-8 -*-
"""Spec 045 (pendiente 45): respuestas.py archiva respuestas útiles en .brain/respuestas/ con su fuente."""
import datetime
import importlib.util
import os
import shutil
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_espec = importlib.util.spec_from_file_location("respuestas", os.path.join(RAIZ, ".brain", "guardianes", "respuestas.py"))
respuestas = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(respuestas)
HOY = datetime.date(2026, 11, 13)


class TestRespuestas(unittest.TestCase):
    def setUp(self):
        self.raiz = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.raiz, True)

    def leer(self, rel):
        with open(os.path.join(self.raiz, rel), encoding="utf-8") as f:
            return f.read()

    def test_guarda_la_respuesta_con_fuente_y_el_indice(self):
        estado, nombre = respuestas.guardar(self.raiz, "Por qué sí el tipo fijo", "chat cerebro-vivo #19", "Porque se filtra con grep.", HOY)
        self.assertEqual((estado, nombre), ("nueva", "2026-11-13-por-que-si-el-tipo-fijo.md"))
        txt = self.leer(".brain/respuestas/" + nombre)
        self.assertIn("# Por qué sí el tipo fijo", txt)
        self.assertIn("- **Fuente:** chat cerebro-vivo #19", txt)
        self.assertIn("Porque se filtra con grep.", txt)
        indice = self.leer(".brain/respuestas/indice.md")
        self.assertIn("[Por qué sí el tipo fijo](" + nombre + ") | chat cerebro-vivo #19", indice)

    def test_no_pisa_una_respuesta_ya_guardada(self):
        respuestas.guardar(self.raiz, "Tema", "chat", "primera", HOY)
        estado, nombre = respuestas.guardar(self.raiz, "Tema", "chat", "segunda", HOY)
        self.assertEqual(estado, "repetida")
        self.assertIn("primera", self.leer(".brain/respuestas/" + nombre))

    def test_exige_titulo_fuente_y_texto(self):
        for args, motivo in ((("", "f", "x"), "titulo"), (("t", "", "x"), "fuente"), (("t", "f", "  "), "texto")):
            with self.assertRaises(ValueError) as c:
                respuestas.guardar(self.raiz, *args, hoy=HOY)
            self.assertEqual(str(c.exception), motivo)

    def test_tope_de_tamano(self):
        with self.assertRaises(ValueError) as c:
            respuestas.guardar(self.raiz, "Larga", "chat", "x" * 9000, HOY)
        self.assertEqual(str(c.exception), "tope")

    def test_indice_con_varias_la_mas_nueva_primero(self):
        respuestas.guardar(self.raiz, "Vieja", "chat", "a", datetime.date(2026, 11, 1))
        respuestas.guardar(self.raiz, "Nueva", "chat", "b", HOY)
        indice = self.leer(".brain/respuestas/indice.md")
        self.assertLess(indice.index("Nueva"), indice.index("Vieja"))

    def test_titulo_con_tildes_y_simbolos_da_nombre_limpio(self):
        self.assertEqual(respuestas.limpiar_titulo("¿Qué es «hermanos»?"), "que-es-hermanos")


if __name__ == "__main__":
    unittest.main()
