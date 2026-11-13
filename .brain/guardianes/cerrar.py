#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cierre rápido de Cerebro Vivo (spec 047): añade la línea de la tarea al registro con el formato correcto.

Uso:  python .brain/guardianes/cerrar.py "qué se hizo" --chat "Proyecto #40" [--quien Claude] [--carril "Cambio pequeño"|"Small change"|SDD]
Cambio de una línea: basta con esta línea (sin tocar pendientes ni fichas salvo que corresponda).
Solo librería estándar. Los ajustes (ruta del registro) salen de guardianes.json."""

import argparse
import datetime
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
# «Fast-Track» sigue aceptándose como alias del carril corto (registros y órdenes antiguos).
CARRILES = ("Cambio pequeño", "Small change", "Fast-Track", "SDD")
# Spec 048: tipo fijo de cada línea nueva del registro (las líneas antiguas no lo llevan). «auto» y «guardian» los escriben los guardianes.
TIPOS = ("arnes", "leccion", "decision", "spec", "pendiente", "memoria", "otro", "auto", "guardian")
sys.path.insert(0, AQUI)
from textos import t  # noqa: E402  (spec 024: mensajes en es/en)


def cargar_config():
    try:
        with open(os.path.join(AQUI, "guardianes.json"), encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def linea_registro(fecha, quien, chat, texto, carril, lengua=None, tipo="otro"):
    """Formato de decisions.log (spec 048): `AAAA-MM-DD | tipo | quién (chat) | qué | carril`.
    El tipo es una palabra fija (TIPOS) para filtrar con grep: `grep "| arnes |" .brain/decisions.log`."""
    texto = " ".join(texto.split())
    if not texto:
        raise ValueError(t(lengua, "cerrar_falta_texto"))
    if carril not in CARRILES:
        raise ValueError(t(lengua, "cerrar_carril", ", ".join(CARRILES)))
    if tipo not in TIPOS:
        raise ValueError(t(lengua, "cerrar_tipo", ", ".join(TIPOS)))
    return "%s | %s | %s (%s) | %s | %s" % (fecha, tipo, quien, chat, texto, carril)


def _indices_o_hecho(a, cfg=None):
    """Spec 083: filas de índice de decisiones y paso de un punto a hechos (con --simular no escribe)."""
    import indices
    brain = os.path.join(RAIZ, ".brain")
    try:
        if a.indices:
            texto, filas = indices.filas_decisiones_faltantes(brain)
            if not a.simular:
                indices.escribir(os.path.join(brain, "decisions", "indice.md"), texto)
            salida = t(cfg, "cerrar_filas", len(filas), "\n".join(filas))
        else:
            if not a.titulo:
                raise ValueError(t(cfg, "cerrar_falta_titulo"))
            pend, hechos, indice = indices.pasar_a_hechos(brain, a.hecho, a.titulo, a.detalle, a.ref, a.fecha, a.conservar)
            if not a.simular:
                indices.escribir(os.path.join(brain, "pendientes.md"), pend)
                indices.escribir(os.path.join(brain, "archive", "hechos.md"), hechos)
                indices.escribir(os.path.join(brain, "archive", "hechos-indice.md"), indice)
            salida = t(cfg, "cerrar_hecho", a.hecho)
    except Exception as e:
        sys.stderr.write(t(cfg, "cerrar_no_se_pudo", e))
        return 1
    sys.stdout.buffer.write(((t(cfg, "cerrar_simulacion") if a.simular else "") + salida + "\n").encode("utf-8"))
    return 0


def main():
    cfg = cargar_config()
    ap = argparse.ArgumentParser(description=t(cfg, "cerrar_descripcion"))
    ap.add_argument("texto", nargs="?", default="", help=t(cfg, "ayuda_cerrar_texto"))
    ap.add_argument("--chat", help=t(cfg, "ayuda_cerrar_chat"))
    ap.add_argument("--quien", default="Claude")
    ap.add_argument("--carril", default=t(cfg, "carril_corto"), choices=CARRILES)
    ap.add_argument("--tipo", default="otro", choices=TIPOS, help=t(cfg, "ayuda_cerrar_tipo"))
    ap.add_argument("--fecha", default=datetime.date.today().isoformat())
    ap.add_argument("--indices", action="store_true", help=t(cfg, "ayuda_cerrar_indices"))
    ap.add_argument("--hecho", help=t(cfg, "ayuda_cerrar_hecho"))
    ap.add_argument("--titulo")
    ap.add_argument("--detalle", default="")
    ap.add_argument("--ref", default="")
    ap.add_argument("--conservar", action="store_true", help=t(cfg, "ayuda_cerrar_conservar"))
    ap.add_argument("--simular", action="store_true", help=t(cfg, "ayuda_cerrar_simular"))
    a = ap.parse_args()
    if a.indices or a.hecho:
        return _indices_o_hecho(a, cfg)
    if not a.chat:
        ap.error(t(cfg, "cerrar_falta_chat"))
    try:
        linea = linea_registro(a.fecha, a.quien, a.chat, a.texto, a.carril, cfg, a.tipo)
        registro = os.path.join(RAIZ, cfg["registro"])
        with open(registro, "a", encoding="utf-8", newline="") as f:
            f.write(linea + "\n")
    except Exception as e:
        sys.stderr.write(t(cfg, "cerrar_no_cerrar", e))
        return 1
    sys.stdout.buffer.write(t(cfg, "cerrar_registrado", linea).encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
