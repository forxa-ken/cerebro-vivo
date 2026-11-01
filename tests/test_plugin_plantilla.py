"""Estructura del plugin /plantilla (spec 009): está completo, el catálogo apunta a él y no se reparte a los proyectos."""
import json
import os
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ruta(*partes):
    return os.path.join(RAIZ, *partes)


class TestPluginPlantilla(unittest.TestCase):
    def test_archivos_del_plugin(self):
        for p in ("hooks/register.tsx", "hooks/logica.ts", "hooks/logica.test.ts", "hooks/hooks.json",
                  ".claude-plugin/plugin.json", "README.md"):
            self.assertTrue(os.path.isfile(ruta("plantilla-prompt", *p.split("/"))), p)

    def test_catalogo_apunta_al_plugin(self):
        with open(ruta(".claude-plugin", "marketplace.json"), encoding="utf-8") as f:
            cat = json.load(f)
        for pl in cat["plugins"]:
            self.assertTrue(os.path.isdir(ruta(*pl["source"].split("/"))), pl["name"])

    def test_botones_de_estado_lanzan_las_skills(self):
        with open(ruta("plantilla-prompt", "hooks", "logica.ts"), encoding="utf-8") as f:
            texto = f.read()
        self.assertIn("prompt: '/pendiente'", texto)
        self.assertIn("prompt: '/resumen'", texto)
        self.assertNotIn("Retomar:", texto)

    def test_no_se_reparte_a_los_proyectos(self):
        with open(ruta("manifiesto.json"), encoding="utf-8") as f:
            self.assertNotIn("plantilla-prompt", f.read())


if __name__ == "__main__":
    unittest.main()
