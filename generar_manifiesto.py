#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera `manifiesto.json`: la lista de archivos del arnés que se reparten a los proyectos, con la huella de cada uno.

Uso:  python generar_manifiesto.py           (reescribe el manifiesto)
      python generar_manifiesto.py --ver     (dice si está al día, sin escribir)
Hay que lanzarlo después de cambiar cualquier archivo del arnés y subir `VERSION`; una prueba avisa si se olvida.
Spec 021: lo que estaba en el manifiesto anterior y ya no se reparte entra solo en `retirados`, y el actualizador lo quita de los proyectos."""

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
    ".brain/biblioteca/CARTA_META_ARNES.md", ".brain/biblioteca/CEREBRO_VIVO.md", ".brain/biblioteca/CEREBRO_VIVO.en.md",
    ".brain/biblioteca/PLANTILLA_NOTA_CHAT.md", ".brain/biblioteca/PLANTILLA_TRASPASO.md",
    ".brain/biblioteca/PLANTILLA_NOTA_CHAT.en.md", ".brain/biblioteca/PLANTILLA_TRASPASO.en.md",
    ".brain/biblioteca/PLANTILLAS_FABRICA.md", ".brain/biblioteca/PLANTILLAS_FABRICA.en.md",
    ".brain/biblioteca/CARTA_EJECUTORA.md", ".brain/biblioteca/CARTA_EJECUTORA.en.md",
    ".brain/biblioteca/IAS_COLABORATIVAS.md", ".brain/biblioteca/IAS_COLABORATIVAS.en.md",
    ".brain/biblioteca/PLANTILLA_PORTAR.md", ".brain/biblioteca/PLANTILLA_PORTAR.en.md", ".brain/biblioteca/PLANTILLA_HALLAZGOS.md", ".brain/biblioteca/PLANTILLA_HALLAZGOS.en.md", ".brain/biblioteca/PLANTILLA_INFORME_REVISION.md", ".brain/biblioteca/PLANTILLA_INFORME_REVISION.en.md",
    ".brain/biblioteca/kit-arranque/", ".brain/biblioteca/kit-traduccion/",
    ".brain/specs/_template.md", ".brain/specs/_template.en.md", ".brain/pruebas/_plantilla.md", ".brain/pruebas/_plantilla.en.md",
    ".claude/skills/",
    "instalar_kit.bat", "instalar_kit.command",
    "tests/test_*.py",
]
EXCLUIR = ["*/__pycache__/*", "*.pyc", ".brain/biblioteca/kit-arranque/preferencias.json",
           "tests/test_arnes_*.py", "tests/test_plugin_*.py"]  # las pruebas del propio repo del arnés no se reparten
PRUEBAS = ["tests.test_arranque", "tests.test_cerebro_indices", "tests.test_kit_arranque", "tests.test_kit_traduccion",
           "tests.test_longitud", "tests.test_guardar_traspaso", "tests.test_librerias", "tests.test_secretos", "tests.test_poda",
           "tests.test_pruebas", "tests.test_experiencia", "tests.test_instalar_gui", "tests.test_analisis", "tests.test_medir", "tests.test_modo_ligero", "tests.test_textos", "tests.test_lecciones", "tests.test_hitos", "tests.test_ediciones_en", "tests.test_eventos_chat", "tests.test_fabrica", "tests.test_auditor"]
# Retirado o renombrado antes de que el manifiesto llevara la lista (sacado del historial de Git).
RETIRADOS_HISTORICOS = [".brain/guardianes/modo_auto.py", ".brain/guardianes/uso_tokens.py", ".claude/skills/cambio-de-ia/SKILL.md",
                        ".claude/skills/traspaso-entre-chats/SKILL.md", "tests/test_cambio_de_ia.py", "tests/test_modo_auto.py",
                        "tests/test_esperando_prueba.py"]  # 1.28.2 la repartió por error; desde 1.28.3 es test_arnes_esperando_prueba.py (solo del repo)


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


def calcular_retirados(actuales, previo):
    """Lo que alguna vez se repartió y ya no; lo que vuelve a repartirse sale de la lista."""
    return sorted((set(RETIRADOS_HISTORICOS) | set(previo.get("retirados") or []) | set(previo.get("archivos") or {})) - set(actuales))


def leer_actual():
    try:
        with open(os.path.join(RAIZ, "manifiesto.json"), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def construir():
    with open(os.path.join(RAIZ, "VERSION"), encoding="utf-8") as f:
        version = f.read().strip()
    archivos = {}
    for rel in listar():
        archivos[rel] = actualizador.huella(actualizador._normalizar(actualizador.leer_bytes(os.path.join(RAIZ, rel)), rel))
    return {"version": version, "archivos": archivos, "retirados": calcular_retirados(archivos, leer_actual() or {}),
            "pruebas": [p for p in PRUEBAS if os.path.exists(os.path.join(RAIZ, *p.split(".")) + ".py")]}


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    nuevo = construir()
    ruta = os.path.join(RAIZ, "manifiesto.json")
    actual = leer_actual()
    if "--ver" in sys.argv:
        print("al día" if actual == nuevo else "DESACTUALIZADO: lanza `python generar_manifiesto.py`")
        return 0 if actual == nuevo else 1
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        json.dump(nuevo, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")
    print("Manifiesto %s: %d archivos." % (nuevo["version"], len(nuevo["archivos"])))
    for rel in sorted(set(nuevo["retirados"]) - set((actual or {}).get("retirados") or [])):
        print("⚠️ Retirado: %s. Saldrá de los proyectos donde esté sin modificar (queda en su copia de seguridad)." % rel)
    return 0


if __name__ == "__main__":
    sys.exit(main())
