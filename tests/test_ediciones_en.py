# -*- coding: utf-8 -*-
"""Spec 024 fase 3: las ediciones inglesas (`X.en.md`) llegan solo a los proyectos con idioma «en», en el sitio de `X.md`."""
import importlib.util
import json
import os
import shutil
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_espec = importlib.util.spec_from_file_location("actualizar_arnes", os.path.join(RAIZ, ".brain", "guardianes", "actualizar_arnes.py"))
act = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(act)

ARCHIVOS = {".claude/skills/hola/SKILL.md": "es hola\n", ".claude/skills/hola/SKILL.en.md": "en hello\n",
            ".brain/biblioteca/MANUAL.md": "es manual\n", ".brain/biblioteca/MANUAL.en.md": "en manual\n",
            ".brain/biblioteca/suelto.en.md": "sin hermano\n", ".brain/guardianes/x.py": "x = 1\n"}


def escribir(base, rel, texto):
    ruta = os.path.join(base, *rel.split("/"))
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)


class TestEdicionesEn(unittest.TestCase):
    def setUp(self):
        self.repo, self.proy = tempfile.mkdtemp(), tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.repo, True)
        self.addCleanup(shutil.rmtree, self.proy, True)
        manifiesto = {"version": "9.9.9", "pruebas": [], "retirados": [], "archivos": {}}
        for rel, texto in ARCHIVOS.items():
            escribir(self.repo, rel, texto)
            manifiesto["archivos"][rel] = act.huella(act._normalizar(texto.encode("utf-8"), rel))
        with open(os.path.join(self.repo, "manifiesto.json"), "w", encoding="utf-8") as f:
            json.dump(manifiesto, f)
        self.manifiesto = manifiesto

    def proyecto(self, idioma=None, agents=False):
        cfg = {} if idioma is None else {"idioma": idioma}
        escribir(self.proy, ".brain/guardianes/guardianes.json", json.dumps(cfg))
        if agents:
            escribir(self.proy, "AGENTS.md", "x")

    def leer(self, rel):
        with open(os.path.join(self.proy, *rel.split("/")), encoding="utf-8") as f:
            return f.read()

    def test_base_de_edicion(self):
        a = self.manifiesto["archivos"]
        self.assertEqual(act.base_de_edicion(".brain/biblioteca/MANUAL.en.md", a), ".brain/biblioteca/MANUAL.md")
        self.assertIsNone(act.base_de_edicion(".brain/biblioteca/suelto.en.md", a))
        self.assertIsNone(act.base_de_edicion(".brain/guardianes/x.py", a))

    def test_espanol_no_recibe_las_ediciones_inglesas(self):
        self.proyecto("es")
        act.sincronizar(self.repo, self.proy)
        self.assertEqual(self.leer(".claude/skills/hola/SKILL.md"), "es hola\n")
        self.assertFalse(os.path.exists(os.path.join(self.proy, ".claude", "skills", "hola", "SKILL.en.md")))
        self.assertEqual(self.leer(".brain/biblioteca/MANUAL.md"), "es manual\n")

    def test_sin_ajuste_de_idioma_es_espanol(self):
        self.proyecto(None)
        act.sincronizar(self.repo, self.proy)
        self.assertEqual(self.leer(".claude/skills/hola/SKILL.md"), "es hola\n")

    def test_ingles_recibe_la_edicion_en_el_sitio_del_original(self):
        self.proyecto("en")
        act.sincronizar(self.repo, self.proy)
        self.assertEqual(self.leer(".claude/skills/hola/SKILL.md"), "en hello\n")
        self.assertEqual(self.leer(".brain/biblioteca/MANUAL.md"), "en manual\n")
        self.assertFalse(os.path.exists(os.path.join(self.proy, ".claude", "skills", "hola", "SKILL.en.md")))
        self.assertEqual(self.leer(".brain/biblioteca/suelto.en.md"), "sin hermano\n")  # sin original: va tal cual

    def test_codex_recibe_la_skill_en_ingles(self):
        self.proyecto("en", agents=True)
        act.sincronizar(self.repo, self.proy)
        self.assertEqual(self.leer(".agents/skills/hola/SKILL.md"), "en hello\n")

    def test_cambiar_a_ingles_actualiza_sin_marcar_a_mano(self):
        self.proyecto("es")
        act.sincronizar(self.repo, self.proy)
        self.proyecto("en")
        res = act.sincronizar(self.repo, self.proy)
        self.assertEqual(res["a_mano"], [])
        self.assertEqual(self.leer(".claude/skills/hola/SKILL.md"), "en hello\n")

    def test_simulacion_anuncia_lo_mismo(self):
        self.proyecto("en")
        res = act.sincronizar(self.repo, self.proy, simular=True)
        self.assertIn(".claude/skills/hola/SKILL.md", res["nuevos"])
        self.assertNotIn(".claude/skills/hola/SKILL.en.md", res["nuevos"])


if __name__ == "__main__":
    unittest.main()
