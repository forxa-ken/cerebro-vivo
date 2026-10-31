#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardián 11 de Cerebro Vivo · memoria de pruebas (spec 053).

Cuenta los hallazgos abiertos (casillas `- [ ]`) de las campañas de `.brain/pruebas/P-NNN-*.md` y comprueba que
`indice.md` y los archivos coinciden. El resumen de arranque imprime una línea SOLO si hay hallazgos abiertos o
incoherencias (con todo cerrado cuesta 0 tokens). Modo --ver: detalle de los hallazgos abiertos.
Solo lectura, solo librería estándar. Si algo falla, calla. Ajustes: guardianes.json (`pruebas_activo`, `pruebas`)."""

import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))


def cargar_config():
    with open(os.path.join(AQUI, "guardianes.json"), encoding="utf-8") as f:
        return json.load(f)


def ajustes(cfg):
    a = dict(cfg.get("pruebas", {}))
    a["activo"] = bool(cfg.get("pruebas_activo", True))
    return a


def analizar(raiz, a):
    """([(id, texto del hallazgo abierto)], [problemas de coherencia]) de la carpeta de pruebas."""
    carpeta = os.path.join(raiz, a.get("carpeta", ".brain/pruebas"))
    with open(os.path.join(carpeta, "indice.md"), encoding="utf-8") as f:
        indexados = dict(re.findall(r"^\|\s*(P-\d+)\s*\|.*?\]\(([^)]+)\)", f.read(), re.M))
    abiertos, problemas = [], []
    for pid, archivo in indexados.items():
        ruta = os.path.join(carpeta, archivo)
        if not os.path.exists(ruta):
            problemas.append("%s está en el índice pero falta el archivo %s" % (pid, archivo))
            continue
        with open(ruta, encoding="utf-8") as f:
            abiertos += [(pid, t.strip()) for t in re.findall(r"^\s*- \[ \]\s*(.+)$", f.read(), re.M)]
    for nombre in sorted(os.listdir(carpeta)):
        if re.match(r"P-\d+-.*\.md$", nombre) and nombre not in indexados.values():
            problemas.append("%s no está en el índice de pruebas" % nombre)
    return abiertos, problemas


def resumen(raiz, cfg):
    """Línea de arranque solo si hay hallazgos abiertos o incoherencias. Calla si está apagado o falla."""
    a = ajustes(cfg)
    if not a["activo"]:
        return []
    try:
        abiertos, problemas = analizar(raiz, a)
    except Exception:
        return []
    if not abiertos and not problemas:
        return []
    ids = sorted({p for p, _ in abiertos})
    partes = []
    if abiertos:
        partes.append("%d hallazgo(s) sin cerrar (%s)" % (len(abiertos), ", ".join(ids)))
    partes += problemas[:1]
    return ["- Pruebas: %s; detalle con `pruebas.py --ver`." % "; ".join(partes)]


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    a = ajustes(cargar_config())
    abiertos, problemas = analizar(RAIZ, a)
    for pid, t in abiertos:
        print("%s · abierto: %s" % (pid, t))
    for p in problemas:
        print("Incoherencia: " + p)
    if not abiertos and not problemas:
        print("Pruebas: sin hallazgos abiertos.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
