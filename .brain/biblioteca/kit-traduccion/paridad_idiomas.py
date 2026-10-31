# -*- coding: utf-8 -*-
"""Paridad de idiomas (kit de traducción, spec 057): cada idioma debe tener las mismas claves que el idioma por defecto,
sin textos vacíos. Lee `idiomas.js` (JSON estricto tras `window.KIT_I18N =`). Solo librería estándar.

Se ejecuta con `python -m unittest tests.test_paridad_idiomas` (en un proyecto con el kit) o directamente con `python paridad_idiomas.py`.
Clave opcional en idiomas.js: "iguales_permitidos": [claves cuyo texto puede ser igual en todos los idiomas, p. ej. marcas]."""
import json
import os
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
CANDIDATOS = [os.path.join(AQUI, "..", "static", "i18n", "idiomas.js"), os.path.join(AQUI, "idiomas.js")]


def cargar(ruta=None):
    ruta = ruta or next((c for c in CANDIDATOS if os.path.exists(c)), None)
    if not ruta:
        raise FileNotFoundError("No encuentro idiomas.js")
    with open(ruta, encoding="utf-8") as f:
        texto = f.read()
    inicio = texto.index("window.KIT_I18N")
    cuerpo = texto[inicio:]
    cuerpo = cuerpo[cuerpo.index("=") + 1:].strip().rstrip(";").strip()
    try:
        return json.loads(cuerpo)
    except json.JSONDecodeError as e:
        # el cuerpo empieza en la línea donde está «window.KIT_I18N»
        linea = e.lineno + texto.count("\n", 0, inicio)
        raise ValueError(
            "El archivo idiomas.js está mal escrito cerca de la línea %d (%s). Mira esa línea y la de justo encima: "
            "lo más habitual es una coma que falta al final de un texto, una coma de más en el último, o unas comillas sin cerrar. "
            "Recuerda: comillas dobles y sin coma tras el último texto de cada bloque." % (linea, e.msg)) from None


def problemas(config):
    """Lista de frases en lenguaje llano con lo que falla; vacía si todo está bien."""
    res = []
    idiomas, textos, base = config.get("idiomas", {}), config.get("textos", {}), config.get("porDefecto")
    if set(idiomas) != set(textos):
        res.append("La lista de idiomas (%s) y los bloques de textos (%s) no coinciden." % (sorted(idiomas), sorted(textos)))
    if base not in textos:
        res.append("El idioma por defecto «%s» no tiene textos." % base)
        return res
    claves, permitidas = set(textos[base]), set(config.get("iguales_permitidos", []))
    for lang, dic in textos.items():
        for k in sorted(claves - set(dic)):
            res.append("Al idioma «%s» le falta la clave «%s»." % (lang, k))
        for k in sorted(set(dic) - claves):
            res.append("El idioma «%s» tiene la clave «%s» que no existe en «%s»." % (lang, k, base))
        for k, v in dic.items():
            if not str(v).strip():
                res.append("El texto «%s» de «%s» está vacío." % (k, lang))
            elif lang != base and k in textos[base] and v == textos[base][k] and k not in permitidas and len(v) > 3:
                res.append("El texto «%s» de «%s» es igual al de «%s»: ¿falta traducirlo?" % (k, lang, base))
    return res


class ParidadIdiomas(unittest.TestCase):
    def test_todos_los_idiomas_tienen_las_mismas_claves(self):
        try:
            p = problemas(cargar())
        except ValueError as e:
            self.fail(str(e))
        self.assertEqual(p, [], "\n".join(p))


if __name__ == "__main__":
    try:
        fallos = problemas(cargar())
    except ValueError as e:
        print("❌ " + str(e))
        raise SystemExit(1)
    print("\n".join(fallos) if fallos else "✅ Todos los idiomas están completos.")
    raise SystemExit(1 if fallos else 0)
