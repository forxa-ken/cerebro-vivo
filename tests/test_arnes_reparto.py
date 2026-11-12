# -*- coding: utf-8 -*-
"""Pruebas del reparto del arnés que solo valen en el repo del arnés (no se reparten a los proyectos).

Comprueban que las ediciones en inglés y `generar_manifiesto.py` existen y listan lo nuevo.
Antes vivían en `test_auditor.py` y `test_colabora.py`, que sí se reparten, y fallaban en los proyectos."""
import os
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


class RepartoAuditor(unittest.TestCase):
    def test_plantilla_e_informe_existen_en_los_dos_idiomas(self):
        for n in ("PLANTILLA_INFORME_REVISION.md", "PLANTILLA_INFORME_REVISION.en.md"):
            self.assertTrue(os.path.isfile(os.path.join(RAIZ, ".brain", "biblioteca", n)), n)

    def test_plantilla_va_en_el_manifiesto(self):
        with open(os.path.join(RAIZ, "generar_manifiesto.py"), encoding="utf-8") as f:
            self.assertIn("PLANTILLA_INFORME_REVISION.en.md", f.read())

    def test_la_skill_esta_en_los_dos_idiomas(self):
        for n in ("SKILL.md", "SKILL.en.md"):
            self.assertTrue(os.path.isfile(os.path.join(RAIZ, ".claude", "skills", "auditor", n)), n)


class RepartoColabora(unittest.TestCase):
    def test_plantilla_y_skill_existen_en_los_dos_idiomas(self):
        for rel in (".brain/biblioteca/IAS_COLABORATIVAS.md", ".brain/biblioteca/IAS_COLABORATIVAS.en.md",
                    ".claude/skills/colabora/SKILL.md", ".claude/skills/colabora/SKILL.en.md"):
            self.assertTrue(os.path.isfile(os.path.join(RAIZ, *rel.split("/"))), rel)


class LoQueNoSeReparte(unittest.TestCase):
    def test_este_archivo_no_va_en_el_manifiesto(self):
        import json
        with open(os.path.join(RAIZ, "manifiesto.json"), encoding="utf-8") as f:
            archivos = json.load(f)["archivos"]
        self.assertNotIn("tests/test_arnes_reparto.py", archivos)
        self.assertIn("tests/test_auditor.py", archivos)


if __name__ == "__main__":
    unittest.main()
