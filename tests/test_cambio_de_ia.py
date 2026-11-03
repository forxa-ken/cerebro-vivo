# -*- coding: utf-8 -*-
"""Spec 010: skill `cambio-de-ia` y su regla en los archivos de entrada."""
import json
import os
import tempfile
import unittest
import importlib.util

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_espec = importlib.util.spec_from_file_location("instalar", os.path.join(RAIZ, ".brain", "biblioteca", "kit-arranque", "instalar.py"))
instalar = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(instalar)


def leer(*partes):
    with open(os.path.join(*partes), encoding="utf-8") as f:
        return f.read()


class TestCambioDeIA(unittest.TestCase):
    def test_skill_existe_y_esta_en_el_manifiesto(self):
        ruta = os.path.join(RAIZ, ".claude", "skills", "cambio-de-ia", "SKILL.md")
        self.assertTrue(os.path.isfile(ruta))
        self.assertIn("name: cambio-de-ia", leer(ruta))
        with open(os.path.join(RAIZ, "manifiesto.json"), encoding="utf-8") as f:
            self.assertIn(".claude/skills/cambio-de-ia/SKILL.md", json.load(f)["archivos"])

    def test_plantilla_de_traspaso_lleva_los_campos_nuevos(self):
        t = leer(RAIZ, ".brain", "biblioteca", "PLANTILLA_TRASPASO.md")
        for campo in ("IA que lo escribe", "IA que sigue", "Hora"):
            self.assertIn(campo, t)

    def test_regla_en_los_tres_archivos_de_entrada_en_nivel_medio_y_completo(self):
        for nivel in ("medio", "completo"):
            with tempfile.TemporaryDirectory() as d:
                instalar.instalar(d, "Prueba", "Darwin", "español", "python -m unittest discover tests", ["claude", "gemini", "codex"], nivel)
                for archivo in ("CLAUDE.md", "GEMINI.md", "AGENTS.md"):
                    self.assertIn("cambio-de-ia", leer(d, archivo), "%s en nivel %s" % (archivo, nivel))

    def test_nivel_ligero_no_lleva_la_regla(self):
        with tempfile.TemporaryDirectory() as d:
            instalar.instalar(d, "Prueba", "Darwin", "español", "python -m unittest discover tests", ["claude"], "ligero")
            self.assertNotIn("cambio-de-ia", leer(d, "CLAUDE.md"))


if __name__ == "__main__":
    unittest.main()
