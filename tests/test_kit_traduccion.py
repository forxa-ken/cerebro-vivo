# -*- coding: utf-8 -*-
"""Kit de traducción (spec 057): se instala como opción, la paridad detecta lo que falta y el motor sigue alineado con el de LoboHook."""
import copy
import importlib.util
import os
import re
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
KIT = os.path.join(RAIZ, ".brain", "biblioteca", "kit-traduccion")


def _cargar(nombre, ruta):
    espec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(espec)
    espec.loader.exec_module(mod)
    return mod


instalador = _cargar("instalar_kit", os.path.join(RAIZ, ".brain", "biblioteca", "kit-arranque", "instalar.py"))
paridad = _cargar("paridad_idiomas", os.path.join(KIT, "paridad_idiomas.py"))


def _instalar(traduccion, nivel="ligero", nombre="Mi App Nueva"):
    destino = tempfile.mkdtemp()
    hechos = instalador.instalar(destino, nombre, "Ana", "español", "pytest", ["claude"], nivel, hoy="2026-01-01", traduccion=traduccion)
    return destino, hechos


class TestKitTraduccion(unittest.TestCase):
    def test_es_opcional(self):
        destino, _ = _instalar(False)
        self.assertFalse(os.path.exists(os.path.join(destino, "static", "i18n")))
        self.assertFalse(os.path.exists(os.path.join(destino, "tests", "test_paridad_idiomas.py")))

    def test_instala_los_archivos_y_personaliza_la_clave(self):
        destino, _ = _instalar(True)
        for rel in ("static/i18n/i18n_motor.js", "static/i18n/idiomas.js", "static/i18n/ejemplo.html",
                    "static/i18n/LEEME.md", "tests/test_paridad_idiomas.py"):
            self.assertTrue(os.path.exists(os.path.join(destino, rel)), rel)
        with open(os.path.join(destino, "static", "i18n", "idiomas.js"), encoding="utf-8") as f:
            texto = f.read()
        self.assertIn('"claveGuardado": "mi_app_nueva_lang"', texto)
        self.assertNotIn("mi_proyecto_lang", texto)

    def test_no_pisa_lo_que_ya_existe(self):
        destino, _ = _instalar(True)
        ruta = os.path.join(destino, "static", "i18n", "idiomas.js")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("// mío")
        instalador.instalar(destino, "Mi App Nueva", "Ana", "español", "pytest", ["claude"], "ligero", traduccion=True)
        with open(ruta, encoding="utf-8") as f:
            self.assertEqual(f.read(), "// mío")

    def test_el_proyecto_instalado_pasa_su_comprobacion(self):
        destino, _ = _instalar(True)
        res = [r for r in instalador.comprobar(destino) if r[0].startswith("Idiomas")]
        self.assertEqual(len(res), 1)
        self.assertTrue(res[0][1], res[0][2])

    def test_los_textos_de_ejemplo_estan_completos(self):
        self.assertEqual(paridad.problemas(paridad.cargar(os.path.join(KIT, "idiomas.js"))), [])

    def test_la_paridad_detecta_clave_que_falta_texto_vacio_y_sin_traducir(self):
        base = paridad.cargar(os.path.join(KIT, "idiomas.js"))
        falta = copy.deepcopy(base)
        del falta["textos"]["en"]["app.bienvenida"]
        self.assertTrue(any("app.bienvenida" in p for p in paridad.problemas(falta)))
        vacio = copy.deepcopy(base)
        vacio["textos"]["pt"]["form.enviar"] = "  "
        self.assertTrue(any("vacío" in p for p in paridad.problemas(vacio)))
        igual = copy.deepcopy(base)
        igual["textos"]["en"]["app.descripcion"] = igual["textos"]["es"]["app.descripcion"]
        self.assertTrue(any("falta traducirlo" in p for p in paridad.problemas(igual)))

    def test_se_puede_anadir_un_idioma(self):
        nuevo = copy.deepcopy(paridad.cargar(os.path.join(KIT, "idiomas.js")))
        nuevo["idiomas"]["fr"] = "Français"
        self.assertTrue(any("no coinciden" in p for p in paridad.problemas(nuevo)), "un idioma sin bloque de textos debe avisar")
        nuevo["textos"]["fr"] = {k: "FR " + v for k, v in nuevo["textos"]["es"].items()}
        self.assertEqual(paridad.problemas(nuevo), [])

    def test_un_idiomas_js_roto_da_un_aviso_claro_con_la_linea(self):
        with open(os.path.join(KIT, "idiomas.js"), encoding="utf-8") as f:
            texto = f.read()
        roto = texto.replace('"form.buscar": "Search…",', '"form.buscar": "Search…"', 1)
        self.assertNotEqual(roto, texto)
        with tempfile.TemporaryDirectory() as d:
            ruta = os.path.join(d, "idiomas.js")
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(roto)
            with self.assertRaises(ValueError) as ctx:
                paridad.cargar(ruta)
        self.assertIn("mal escrito cerca de la línea", str(ctx.exception))
        self.assertIn("coma", str(ctx.exception))

    @unittest.skipUnless(os.path.exists(os.path.join(RAIZ, "static", "js", "i18n.js")), "el proyecto no tiene su propio motor de idiomas")
    def test_el_motor_del_kit_sigue_alineado_con_el_del_proyecto(self):
        with open(os.path.join(KIT, "i18n_motor.js"), encoding="utf-8") as f:
            kit_js = f.read()
        with open(os.path.join(RAIZ, "static", "js", "i18n.js"), encoding="utf-8") as f:
            lobo_js = f.read()
        for attr in ("data-i18n", "data-i18n-html", "data-i18n-placeholder", "data-i18n-title", "data-i18n-aria"):
            self.assertIn('"%s"' % attr, kit_js, attr)
            self.assertIn('"%s"' % attr, lobo_js, attr)
        self.assertIsNotNone(re.search(r"localStorage\.setItem", kit_js))
        self.assertIsNotNone(re.search(r"localStorage\.setItem", lobo_js))


if __name__ == "__main__":
    unittest.main()
