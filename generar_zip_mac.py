#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera el ZIP de prueba para Mac (cerebro-vivo-mac-VERSION.zip) con los archivos del manifiesto.

Uso:  python generar_zip_mac.py [CARPETA_DESTINO]
Por defecto escribe en ../cerebro-vivo-para-mac (junto a este repo). El ZIP anterior se mueve a `anteriores/`, no se borra.
Se lanza después de `generar_manifiesto.py` cada vez que cambia el arnés (ver CLAUDE.md)."""
import json
import os
import shutil
import sys
import zipfile

RAIZ = os.path.dirname(os.path.abspath(__file__))
EXTRA = [".brain/guardianes/guardianes.json", "manifiesto.json", "VERSION", "CAMBIOS.md", ".gitattributes", "instalar_kit.bat", "instalar_kit.command"]


def archivos():
    with open(os.path.join(RAIZ, "manifiesto.json"), encoding="utf-8") as f:
        man = json.load(f)
    lista = set(man.get("archivos", man))
    lista |= {e for e in EXTRA if os.path.exists(os.path.join(RAIZ, e))}
    for rel in ("tests/test_cerebro_indices.py", "tests/test_instalar_gui.py", "tests/test_kit_arranque.py", "tests/test_soporte_mac.py"):
        lista.add(rel)
    return sorted(x for x in lista if os.path.isfile(os.path.join(RAIZ, x)))


def generar(destino):
    with open(os.path.join(RAIZ, "VERSION"), encoding="utf-8") as f:
        version = f.read().strip()
    os.makedirs(destino, exist_ok=True)
    nombre = "cerebro-vivo-mac-%s.zip" % version
    ruta = os.path.join(destino, nombre)
    anteriores = os.path.join(destino, "anteriores")
    for viejo in os.listdir(destino):
        if viejo.startswith("cerebro-vivo-mac-") and viejo.endswith(".zip") and viejo != nombre:
            os.makedirs(anteriores, exist_ok=True)
            shutil.move(os.path.join(destino, viejo), os.path.join(anteriores, viejo))
    leeme = os.path.join(destino, "LEEME_PRIMERO.md")
    with zipfile.ZipFile(ruta, "w", zipfile.ZIP_DEFLATED) as z:
        if os.path.exists(leeme):
            z.write(leeme, "LEEME_PRIMERO.md")
        for rel in archivos():
            z.write(os.path.join(RAIZ, rel), rel)
    return ruta


if __name__ == "__main__":
    print(generar(sys.argv[1] if len(sys.argv) > 1 else os.path.join(RAIZ, "..", "cerebro-vivo-para-mac")))
