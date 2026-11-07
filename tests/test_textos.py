# -*- coding: utf-8 -*-
"""Spec 024 fase 2: los textos de los guardianes están en español e inglés, sin claves que falten,
y el idioma sale de `"idioma"` en guardianes.json (por defecto español)."""

import importlib.util
import os
import re
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
G = os.path.join(RAIZ, ".brain", "guardianes")


def cargar(nombre):
    espec = importlib.util.spec_from_file_location(nombre + "_textos", os.path.join(G, nombre + ".py"))
    mod = importlib.util.module_from_spec(espec)
    espec.loader.exec_module(mod)
    return mod


textos = cargar("textos")


class TestParidad(unittest.TestCase):
    def test_mismas_claves_en_cada_idioma(self):
        base = set(textos.TEXTOS["es"])
        for idioma in textos.IDIOMAS:
            with self.subTest(idioma=idioma):
                self.assertEqual(set(textos.TEXTOS[idioma]) ^ base, set(), "Claves que faltan o sobran en %s" % idioma)

    def test_mismos_huecos_en_cada_idioma(self):
        for clave, es in textos.TEXTOS["es"].items():
            for idioma in textos.IDIOMAS:
                with self.subTest(clave=clave, idioma=idioma):
                    self.assertEqual(re.findall(r"%[sd]", textos.TEXTOS[idioma][clave]), re.findall(r"%[sd]", es))

    def test_sin_claves_repetidas(self):
        """Una clave escrita dos veces en el mismo idioma se pisaría sin avisar."""
        import ast
        with open(os.path.join(G, "textos.py"), encoding="utf-8") as f:
            arbol = ast.parse(f.read())
        dicts = [n for n in ast.walk(arbol) if isinstance(n, ast.Dict) and n.keys
                 and all(isinstance(k, ast.Constant) for k in n.keys) and len(n.keys) > 10]
        self.assertEqual(len(dicts), len(textos.IDIOMAS))
        for d in dicts:
            claves = [k.value for k in d.keys]
            self.assertEqual(sorted({c for c in claves if claves.count(c) > 1}), [])

    def test_nada_vacio(self):
        for idioma in textos.IDIOMAS:
            for clave, valor in textos.TEXTOS[idioma].items():
                self.assertTrue(valor.strip(), "%s/%s vacío" % (idioma, clave))

    def test_claves_usadas_existen(self):
        """Cada t(…, "clave") de los guardianes y el instalador apunta a una clave que existe."""
        rutas = [os.path.join(G, n) for n in os.listdir(G) if n.endswith(".py")]
        rutas.append(os.path.join(RAIZ, ".brain", "biblioteca", "kit-arranque", "instalar.py"))
        for ruta in rutas:
            with open(ruta, encoding="utf-8") as f:
                texto = f.read()
                usadas = re.findall(r"\bt\([^,()]+(?:\([^()]*\))?,\s*\"(\w+)\"", texto) + re.findall(r"\btp\(\"(\w+)\"", texto)
                for clave in usadas:
                    with self.subTest(archivo=os.path.basename(ruta), clave=clave):
                        self.assertIn(clave, textos.TEXTOS["es"])


class TestIdioma(unittest.TestCase):
    def test_por_defecto_espanol(self):
        self.assertEqual(textos.idioma({}), "es")
        self.assertEqual(textos.idioma(None), "es")
        self.assertEqual(textos.idioma({"idioma": "fr"}), "es")
        self.assertEqual(textos.idioma("español"), "es")

    def test_ingles(self):
        for valor in ("en", "EN", "English", "inglés", "en-GB", {"idioma": "en"}):
            self.assertEqual(textos.idioma(valor), "en", valor)

    def test_todos_los_guardianes_usan_textos(self):
        """Cada guardián (salvo textos.py) toma sus mensajes de textos.py."""
        for nombre in sorted(os.listdir(G)):
            if nombre.endswith(".py") and nombre != "textos.py":
                with open(os.path.join(G, nombre), encoding="utf-8") as f:
                    self.assertIn("from textos import", f.read(), nombre)

    def test_sin_args_devuelve_la_plantilla(self):
        self.assertEqual(textos.t("en", "cerrar_carril"), "The lane must be one of: %s")

    def test_formato(self):
        self.assertEqual(textos.t({"idioma": "en"}, "cerrar_registrado", "x"), "Logged: x\n")
        self.assertEqual(textos.t({}, "cerrar_registrado", "x"), "Registrado: x\n")


class TestGuardianesEnIngles(unittest.TestCase):
    EN = {"idioma": "en", "registro": ".brain/decisions.log", "pendientes": ".brain/pendientes.md", "tope_pendientes_bytes": 10,
          "ignorar_cambios": [".brain/*"]}

    def test_cierre(self):
        cierre = cargar("cierre")
        avisos = cierre.evaluar(["app.py"], 20, self.EN)
        self.assertIn("There are changes in the project (app.py)", avisos[0])
        self.assertIn("weighs 20 bytes and the cap is 10", avisos[1])
        self.assertIn("Hay cambios en el proyecto", cierre.evaluar(["app.py"], 0, dict(self.EN, idioma="es"))[0])

    def test_longitud(self):
        longitud = cargar("longitud")
        self.assertIn("This chat already weighs ~250k tokens", longitud.texto_aviso(250000, "en"))
        self.assertIn("Este chat ya pesa ~250k tokens", longitud.texto_aviso(250000))

    def test_cerrar(self):
        cerrar = cargar("cerrar")
        with self.assertRaisesRegex(ValueError, "lane must be"):
            cerrar.linea_registro("2026-11-07", "Claude", "x", "algo", "Otro", "en")

    def test_arranque(self):
        arranque = cargar("arranque")
        self.assertEqual(arranque.texto_sin_commitear(["a", "b"], "en"), "- Not committed: 2 files (a, b).")
        self.assertEqual(arranque.texto_sin_commitear(["a"]), "- Sin commitear: 1 archivo (a).")


if __name__ == "__main__":
    unittest.main()
