#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera `manifiesto.json`: la lista de archivos del arnés que se reparten a los proyectos, con la huella de cada uno.

Uso:  python generar_manifiesto.py           (reescribe el manifiesto)
      python generar_manifiesto.py --ver     (dice si está al día, sin escribir)
Hay que lanzarlo después de cambiar cualquier archivo del arnés y subir `VERSION`; una prueba avisa si se olvida."""

import fnmatch
import importlib.util
import json
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
_espec = importlib.util.spec_from_file_location("actualizar_arnes", os.path.join(RAIZ, ".brain", "guardianes", "actualizar_arnes.py"))
actualizador = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(actualizador)

# Lo que se reparte a los proyectos. Cada entrada es un archivo, o una carpeta entera.
INCLUIR = [
    ".brain/guardianes/*.py",
    ".brain/biblioteca/CARTA_META_ARNES.md", ".brain/biblioteca/CEREBRO_VIVO.md",
    ".brain/biblioteca/PLANTILLA_NOTA_CHAT.md", ".brain/biblioteca/PLANTILLA_TRASPASO.md",
    ".brain/biblioteca/kit-arranque/", ".brain/biblioteca/kit-traduccion/",
    ".brain/specs/_template.md", ".brain/pruebas/_plantilla.md",
    ".claude/skills/",
    "instalar_kit.bat",
    "tests/test_*.py",
]
EXCLUIR = ["*/__pycache__/*", "*.pyc", ".brain/biblioteca/kit-arranque/preferencias.json",
           "tests/test_arnes_*.py"]  # las pruebas del propio repo del arnés no se reparten
PRUEBAS = ["tests.test_arranque", "tests.test_cerebro_indices", "tests.test_kit_arranque", "tests.test_kit_traduccion",
           "tests.test_modo_auto", "tests.test_longitud", "tests.test_librerias", "tests.test_secretos", "tests.test_poda",
           "tests.test_pruebas", "tests.test_experiencia", "tests.test_instalar_gui", "tests.test_analisis", "tests.test_medir", "tests.test_modo_ligero"]


def listar():
    res = []
    for patron in INCLUIR:
        if patron.endswith("/"):
            for base, dirs, nombres in os.walk(os.path.join(RAIZ, patron.rstrip("/"))):
                dirs[:] = [d for d in dirs if d != "__pycache__"]
                res += [os.path.relpath(os.path.join(base, n), RAIZ).replace("\\", "/") for n in nombres]
        elif any(c in patron for c in "*?"):
            carpeta, _, filtro = patron.rpartition("/")
            res += [carpeta + "/" + n for n in sorted(os.listdir(os.path.join(RAIZ, carpeta))) if fnmatch.fnmatch(n, filtro)]
        else:
            res.append(patron)
    return sorted({r for r in res if not any(fnmatch.fnmatch(r, x) for x in EXCLUIR)})


def construir():
    with open(os.path.join(RAIZ, "VERSION"), encoding="utf-8") as f:
        version = f.read().strip()
    archivos = {}
    for rel in listar():
        archivos[rel] = actualizador.huella(actualizador._normalizar(actualizador.leer_bytes(os.path.join(RAIZ, rel)), rel))
    return {"version": version, "archivos": archivos, "pruebas": [p for p in PRUEBAS if os.path.exists(os.path.join(RAIZ, *p.split(".")) + ".py")]}


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    nuevo = construir()
    ruta = os.path.join(RAIZ, "manifiesto.json")
    try:
        with open(ruta, encoding="utf-8") as f:
            actual = json.load(f)
    except Exception:
        actual = None
    if "--ver" in sys.argv:
        print("al día" if actual == nuevo else "DESACTUALIZADO: lanza `python generar_manifiesto.py`")
        return 0 if actual == nuevo else 1
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        json.dump(nuevo, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    print("Manifiesto %s: %d archivos." % (nuevo["version"], len(nuevo["archivos"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
