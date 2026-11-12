#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Modo colaborativo (spec 042): varias IA con papeles distintos en un mismo proyecto. Solo librería estándar.

  python .brain/guardianes/colabora.py si|no|estado

`si`: enciende `modo_colaborativo` en guardianes.json, crea `.brain/colaboracion.md` desde la plantilla
      `biblioteca/IAS_COLABORATIVAS.md` (o `.en.md`) si no existe y añade UNA línea que remite a él en los
      índices que existan (CLAUDE.md, AGENTS.md, GEMINI.md), salvo los de `indices_ajenos`.
`no`: lo apaga y quita esas líneas. `colaboracion.md` se conserva (mover, no borrar).
`estado` (o sin palabra): solo muestra cómo está. No abre ningún chat."""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, AQUI)
from textos import t  # noqa: E402

INDICES = ("CLAUDE.md", "AGENTS.md", "GEMINI.md")
DESTINO = os.path.join(".brain", "colaboracion.md")
MARCA = ".brain/colaboracion.md"


def _leer(ruta):
    with open(ruta, "rb") as f:
        return f.read().decode("utf-8")


def _escribir(ruta, texto):
    with open(ruta + ".tmp", "wb") as f:
        f.write(texto.encode("utf-8"))
    os.replace(ruta + ".tmp", ruta)


def _cfg(raiz):
    ruta = os.path.join(raiz, ".brain", "guardianes", "guardianes.json")
    try:
        return ruta, json.loads(_leer(ruta))
    except (OSError, ValueError):
        return ruta, {}


def _linea(cfg):
    return "* **" + t(cfg, "colabora_linea_titulo") + "** [`" + MARCA + "`](" + MARCA + ")."


def _con_linea(texto, linea):
    if MARCA in texto:
        return texto, False
    salto = "\r\n" if "\r\n" in texto else "\n"
    lineas = texto.split(salto)
    donde = next((i for i, l in enumerate(lineas) if l.lstrip().startswith("* **Pendientes:**")), None)
    if donde is None:
        lineas.append(linea)
    else:
        lineas.insert(donde, linea)
    return salto.join(lineas), True


def _sin_linea(texto):
    salto = "\r\n" if "\r\n" in texto else "\n"
    lineas = texto.split(salto)
    nuevas = [l for l in lineas if not (MARCA in l and l.lstrip().startswith("* **"))]
    return salto.join(nuevas), len(nuevas) != len(lineas)


def modo(raiz, orden):
    """Devuelve (código, líneas). 0 = bien, 1 = palabra desconocida."""
    orden = (orden or "estado").strip().lower()
    ruta, cfg = _cfg(raiz)
    ajenos = {str(x) for x in cfg.get("indices_ajenos", [])} if isinstance(cfg.get("indices_ajenos"), list) else set()
    avisos = []
    if orden in ("si", "sí", "on", "yes", "activar", "activa"):
        cfg["modo_colaborativo"] = True
        destino = os.path.join(raiz, DESTINO)
        if not os.path.exists(destino):
            base = os.path.join(raiz, ".brain", "biblioteca", "IAS_COLABORATIVAS")
            en = str(cfg.get("idioma", "es")).lower().startswith("en")
            origen = base + (".en.md" if en and os.path.isfile(base + ".en.md") else ".md")
            if os.path.isfile(origen):
                _escribir(destino, _leer(origen))
            else:
                avisos.append(t(cfg, "colabora_falta_plantilla"))
        for nombre in INDICES:
            r = os.path.join(raiz, nombre)
            if not os.path.isfile(r):
                continue
            if nombre in ajenos:
                avisos.append(t(cfg, "colabora_indice_ajeno", nombre))
                continue
            nuevo, cambio = _con_linea(_leer(r), _linea(cfg))
            if cambio:
                _escribir(r, nuevo)
    elif orden in ("no", "off", "desactivar", "desactiva"):
        cfg["modo_colaborativo"] = False
        for nombre in INDICES:
            r = os.path.join(raiz, nombre)
            if os.path.isfile(r) and nombre not in ajenos:
                nuevo, cambio = _sin_linea(_leer(r))
                if cambio:
                    _escribir(r, nuevo)
    elif orden != "estado":
        return 1, [t(cfg, "colabora_uso")]
    if orden != "estado":
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        _escribir(ruta, json.dumps(cfg, ensure_ascii=False, indent=2) + "\n")
    activo = bool(cfg.get("modo_colaborativo"))
    lineas = [t(cfg, "colabora_si" if activo else "colabora_no")]
    if activo and not os.path.isfile(os.path.join(raiz, DESTINO)):
        lineas.append(t(cfg, "colabora_falta_archivo"))
    return 0, lineas + avisos


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    codigo, lineas = modo(RAIZ, argv[0] if argv else "estado")
    for l in lineas:
        print(l)
    return codigo


if __name__ == "__main__":
    sys.exit(main())
