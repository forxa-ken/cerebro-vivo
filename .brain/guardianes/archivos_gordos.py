#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardián de Cerebro Vivo · archivos de memoria demasiado gordos (spec 018).

Los índices de IA (CLAUDE/GEMINI/AGENTS) tienen su tope (`tope_claude_md_bytes`) y `pendientes.md` el suyo. Los demás
archivos de lectura de `.brain/` (referencias, constitución, architecture/, decisions/, hechos…) no tenían ninguno y
tras adoptar un proyecto antiguo uno acababa con 47 KB. Este guardián (solo lectura) avisa cuando pasan de
`tope_archivo_memoria_bytes` (8 KB por defecto) y la skill `trocea` los divide por tema.
No mira: archive/, biblioteca/, copias_arnes/, specs/, pruebas/, experiencia/, notas-chats/, traspaso.md ni pendientes.md.
Uso:  python archivos_gordos.py        lista los archivos (tamaño y % del tope)
Ajustes en guardianes.json: tope_archivo_memoria_bytes, archivos_gordos_activo, archivos_gordos_aviso_porcentaje,
archivos_gordos_ignorar (patrones). Si falla en el arranque, calla. Solo librería estándar."""
import fnmatch
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
CARPETAS_FUERA = ("archive", "biblioteca", "copias_arnes", "specs", "pruebas", "experiencia", "notas-chats", "guardianes")
ARCHIVOS_FUERA = ("pendientes.md", "traspaso.md")


def cargar_config():
    with open(os.path.join(AQUI, "guardianes.json"), encoding="utf-8") as f:
        return json.load(f)


def analizar(raiz, cfg):
    """Lista de {ruta, bytes, porcentaje} de los .md de .brain/ que llegan al aviso, de mayor a menor."""
    if not cfg.get("archivos_gordos_activo", True):
        return []
    tope = max(1, int(cfg.get("tope_archivo_memoria_bytes", 8192)))
    aviso = int(cfg.get("archivos_gordos_aviso_porcentaje", 80))
    ignorar = list(cfg.get("archivos_gordos_ignorar", []))
    base = os.path.join(raiz, ".brain")
    salida = []
    for carpeta, subs, archivos in os.walk(base):
        subs[:] = [s for s in subs if not (os.path.relpath(os.path.join(carpeta, s), base).split(os.sep)[0] in CARPETAS_FUERA and carpeta == base)]
        for n in archivos:
            if not n.endswith(".md") or (carpeta == base and n in ARCHIVOS_FUERA):
                continue
            ruta = os.path.join(carpeta, n)
            rel = os.path.relpath(ruta, raiz).replace(os.sep, "/")
            if any(fnmatch.fnmatch(rel, p) for p in ignorar):
                continue
            try:
                tam = os.path.getsize(ruta)
            except OSError:
                continue
            pct = 100 * tam // tope
            if pct >= aviso:
                salida.append({"ruta": rel, "bytes": tam, "porcentaje": pct})
    return sorted(salida, key=lambda h: -h["bytes"])


def resumen(raiz, cfg):
    """Una línea para el arranque, o [] si todo cabe (0 tokens)."""
    gordos = analizar(raiz, cfg)
    if not gordos:
        return []
    nombres = ", ".join("%s (%d KB)" % (h["ruta"].replace(".brain/", ""), round(h["bytes"] / 1024)) for h in gordos[:3])
    mas = " y %d más" % (len(gordos) - 3) if len(gordos) > 3 else ""
    return ["- Memoria con archivos gordos (tope %d KB): %s%s; pide «trocea» (skill trocea)." % (int(cfg.get("tope_archivo_memoria_bytes", 8192)) // 1024, nombres, mas)]


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    cfg = cargar_config()
    gordos = analizar(RAIZ, cfg)
    if not gordos:
        print("Ningún archivo de .brain/ llega al aviso (tope %d bytes)." % int(cfg.get("tope_archivo_memoria_bytes", 8192)))
        return 0
    for h in gordos:
        print("%6d bytes  %3d %%  %s" % (h["bytes"], h["porcentaje"], h["ruta"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
