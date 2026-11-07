# -*- coding: utf-8 -*-
"""Comprueba que la página tiene lo mismo en español y en inglés (spec 024 de cerebro-vivo).

Uso: python comprobar_idiomas.py   (sale con 0 si todo está bien; si no, dice qué falta en lenguaje llano)
- idiomas.js: las mismas claves en cada idioma, sin textos vacíos, y cada clave usada en index.html existe.
- datos.js: las mismas listas con el mismo número de elementos; los campos que no se traducen (nombres de
  archivo, comandos de tipo y filtros) son iguales en los dos idiomas."""
import json, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
FIJOS = {"FILES": ("d", "g"), "G": ("f", "k", "ek")}


def leer(nombre, var):
    t = open(os.path.join(AQUI, nombre), encoding="utf-8").read()
    t = t[t.index(var):]
    return json.loads(t[t.index("=") + 1:].strip().rstrip(";"))


def problemas():
    res = []
    cfg = leer("idiomas.js", "window.KIT_I18N")
    tx = cfg["textos"]; base = tx[cfg["porDefecto"]]
    for lang, dic in tx.items():
        for k in sorted(set(base) - set(dic)): res.append("A «%s» le falta el texto «%s»." % (lang, k))
        for k in sorted(set(dic) - set(base)): res.append("«%s» tiene el texto «%s», que no está en «%s»." % (lang, k, cfg["porDefecto"]))
        res += ["El texto «%s» de «%s» está vacío." % (k, lang) for k, v in dic.items() if not str(v).strip()]
    html = open(os.path.join(AQUI, "index.html"), encoding="utf-8").read()
    usadas = set(re.findall(r'data-i18n(?:-html|-placeholder|-title|-aria)?="([^"]+)"', html))
    usadas |= {k for k in re.findall(r'tr\("([^"]+)"', html) if not k.endswith(".")}
    usadas |= {"side." + s for s in re.findall(r'<section class="ch" id="(c\d+)"', html)}
    res += ["index.html usa el texto «%s», que no existe." % k for k in sorted(usadas - set(base))]
    datos = leer("datos.js", "window.DATOS")
    es = datos["es"]
    for lang, d in datos.items():
        for lista, filas in es.items():
            otra = d.get(lista)
            if otra is None: res.append("En datos.js, a «%s» le falta la lista %s." % (lang, lista)); continue
            if len(otra) != len(filas): res.append("En datos.js, la lista %s tiene %d elementos en «%s» y %d en «es»." % (lista, len(otra), lang, len(filas))); continue
            for i, (a, b) in enumerate(zip(filas, otra)):
                if isinstance(a, dict):
                    if set(a) != set(b): res.append("En datos.js, %s[%d] no tiene los mismos campos en «%s»." % (lista, i, lang))
                    res += ["En datos.js, %s[%d].%s cambia en «%s» y no debe traducirse." % (lista, i, c, lang) for c in FIJOS.get(lista, ()) if a.get(c) != b.get(c)]
                    res += ["En datos.js, %s[%d].%s está vacío en «%s»." % (lista, i, c, lang) for c, v in b.items() if v in ("", [])]
                elif lista == "SK" and a[1] != b[1]:
                    res.append("En datos.js, los nombres de skills del grupo %d no coinciden en «%s»." % (i + 1, lang))
    return res


if __name__ == "__main__":
    try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception: pass
    p = problemas()
    print("\n".join(p) if p else "Todo bien: español e inglés tienen lo mismo.")
    sys.exit(1 if p else 0)
