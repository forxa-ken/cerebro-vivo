# -*- coding: utf-8 -*-
"""El repo del arnés por sí solo (spec 087): manifiesto al día, configuración neutra, sin rastros de ningún proyecto, plugin coherente."""
import importlib.util
import json
import os
import re
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_espec = importlib.util.spec_from_file_location("generar_manifiesto", os.path.join(RAIZ, "generar_manifiesto.py"))
gen = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(gen)

RASTROS = re.compile(r"lobohook|users\.db|gumroad|ko-fi", re.I)
# La carta, el manual y las pruebas citan el proyecto de origen como caso real; las pruebas lo nombran para vigilarlo.
PERMITIDOS = (".brain/biblioteca/CARTA_META_ARNES.md", ".brain/biblioteca/CEREBRO_VIVO.md", "generar_manifiesto.py", "CAMBIOS.md", "CLAUDE.md")


def leer(rel):
    with open(os.path.join(RAIZ, *rel.split("/")), encoding="utf-8") as f:
        return f.read()


class TestRepoArnes(unittest.TestCase):
    def test_manifiesto_al_dia(self):
        self.assertEqual(json.loads(leer("manifiesto.json")), gen.construir(),
                         "Cambió un archivo del arnés: sube VERSION, anota CAMBIOS.md y lanza `python generar_manifiesto.py`")

    def test_version_anotada_en_cambios(self):
        version = leer("VERSION").strip()
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")
        self.assertIn("## " + version, leer("CAMBIOS.md"))

    def test_el_manifiesto_no_reparte_datos_ni_configuracion_de_proyecto(self):
        for rel in json.loads(leer("manifiesto.json"))["archivos"]:
            self.assertFalse(rel.startswith((".brain/specs/0", ".brain/decisions", ".brain/archive", ".brain/notas-chats")), rel)
            self.assertNotIn(rel, (".brain/pendientes.md", ".brain/guardianes/guardianes.json", ".brain/modo_auto.json"))
            self.assertFalse(rel.endswith((".db", ".log")), rel)

    def test_configuracion_neutra(self):
        cfg = json.loads(leer(".brain/guardianes/guardianes.json"))
        self.assertEqual(cfg["secretos"]["permitidos"], [])
        self.assertEqual(cfg["analisis"]["sql_excepciones"], [])
        self.assertFalse(cfg["base_datos_activo"] or cfg["analisis_activo"])
        self.assertEqual(cfg["arnes_repo"], "")

    def test_sin_rastros_de_otros_proyectos(self):
        lista = list(json.loads(leer("manifiesto.json"))["archivos"]) + ["README.md", ".claude-plugin/marketplace.json"]
        for base, dirs, nombres in os.walk(os.path.join(RAIZ, "plantilla-prompt")):
            dirs[:] = [d for d in dirs if d != "node_modules"]
            lista += [os.path.relpath(os.path.join(base, n), RAIZ).replace("\\", "/") for n in nombres]
        for rel in lista:
            if rel in PERMITIDOS or rel.startswith("tests/") or not rel.lower().endswith((".py", ".md", ".json", ".js", ".ts", ".tsx", ".html", ".bat")):
                continue
            m = RASTROS.search(leer(rel))
            self.assertIsNone(m, "Rastro de un proyecto concreto en %s: %s" % (rel, m and m.group(0)))

    def test_plugin_y_marketplace_coherentes(self):
        mercado = json.loads(leer(".claude-plugin/marketplace.json"))
        self.assertEqual(mercado["name"], "cerebro-vivo")
        plugin = json.loads(leer("plantilla-prompt/.claude-plugin/plugin.json"))
        self.assertEqual(plugin["name"], "plantilla-prompt")
        self.assertEqual([p["name"] for p in mercado["plugins"]], ["plantilla-prompt"])
        self.assertTrue(os.path.isdir(os.path.join(RAIZ, mercado["plugins"][0]["source"])))
        cfg = json.loads(leer(".brain/guardianes/guardianes.json"))
        self.assertEqual(cfg["plugins_requeridos"], ["plantilla-prompt@cerebro-vivo"])
        neutros = json.loads(leer(".brain/biblioteca/kit-arranque/ajustes_neutros.json"))
        self.assertEqual(neutros["plugins_requeridos"], ["plantilla-prompt@cerebro-vivo"])

    def test_el_actualizador_del_proyecto_esta_en_el_manifiesto_y_en_el_kit(self):
        self.assertIn(".brain/guardianes/actualizar_arnes.py", json.loads(leer("manifiesto.json"))["archivos"])
        self.assertIn("actualizar_arnes", leer(".brain/biblioteca/kit-arranque/instalar.py").split("GUARDIANES = ")[1].split("\n")[0])

    def test_manual_documenta_los_comandos_del_actualizador(self):
        manual = leer(".brain/biblioteca/CEREBRO_VIVO.md")
        for comando in ("actualizar_arnes.py --simular", "actualizar.py", "generar_manifiesto.py"):
            self.assertIn(comando, manual)


if __name__ == "__main__":
    unittest.main()
