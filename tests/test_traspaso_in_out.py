# -*- coding: utf-8 -*-
"""Specs 010 y 011: skills `traspaso-in` y `traspaso-out` y su regla en los archivos de entrada."""
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


class TestTraspasoInOut(unittest.TestCase):
    def test_skills_nuevas_existen_y_las_viejas_no(self):
        for nombre in ("traspaso-in", "traspaso-out"):
            ruta = os.path.join(RAIZ, ".claude", "skills", nombre, "SKILL.md")
            self.assertTrue(os.path.isfile(ruta), nombre)
            self.assertIn("name: " + nombre, leer(ruta))
            if os.path.isfile(os.path.join(RAIZ, "manifiesto.json")):  # solo existe en el repo del arnés, no en los proyectos
                with open(os.path.join(RAIZ, "manifiesto.json"), encoding="utf-8") as f:
                    self.assertIn(".claude/skills/%s/SKILL.md" % nombre, json.load(f)["archivos"])
        for viejo in ("cambio-de-ia", "traspaso-entre-chats"):
            self.assertFalse(os.path.isdir(os.path.join(RAIZ, ".claude", "skills", viejo)), viejo)

    def test_traspaso_in_salgo_abre_el_chat_nuevo_y_lo_separa(self):
        t = leer(RAIZ, ".claude", "skills", "traspaso-in", "SKILL.md")
        for palabra in ("start_session", "detach_session", "traspaso-in entro"):
            self.assertIn(palabra, t)

    def test_plantilla_de_traspaso_lleva_los_campos_nuevos(self):
        t = leer(RAIZ, ".brain", "biblioteca", "PLANTILLA_TRASPASO.md")
        for campo in ("IA que lo escribe", "IA que sigue", "Hora"):
            self.assertIn(campo, t)

    def test_regla_en_los_tres_archivos_de_entrada_en_nivel_medio_y_completo(self):
        for nivel in ("medio", "completo"):
            with tempfile.TemporaryDirectory() as d:
                instalar.instalar(d, "Prueba", "Darwin", "español", "python -m unittest discover tests", ["claude", "gemini", "codex"], nivel)
                for archivo in ("CLAUDE.md", "GEMINI.md", "AGENTS.md"):
                    texto = leer(d, archivo)
                    self.assertIn("traspaso-in", texto, "%s en nivel %s" % (archivo, nivel))
                    self.assertIn("traspaso-out", texto, "%s en nivel %s" % (archivo, nivel))

    def test_nivel_ligero_no_lleva_la_regla(self):
        with tempfile.TemporaryDirectory() as d:
            instalar.instalar(d, "Prueba", "Darwin", "español", "python -m unittest discover tests", ["claude"], "ligero")
            self.assertNotIn("traspaso-out", leer(d, "CLAUDE.md"))


if __name__ == "__main__":
    unittest.main()
