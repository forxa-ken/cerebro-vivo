#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Juzga la respuesta de un chat de la prueba del índice (spec 004).
Uso:  python bench/indice/verificar.py 1..5 "texto de la respuesta"   (o --archivo RUTA)
Imprime acierta | falla | inventa (esta última solo en la pregunta sin respuesta)."""
import argparse
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from preguntas import PREGUNTAS, juzgar  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("pregunta", type=int, choices=sorted(PREGUNTAS))
    ap.add_argument("respuesta", nargs="?", default="")
    ap.add_argument("--archivo")
    a = ap.parse_args(argv)
    texto = a.respuesta
    if a.archivo:
        with open(a.archivo, encoding="utf-8") as f:
            texto = f.read()
    r = juzgar(a.pregunta, texto)
    print(r)
    return 0 if r == "acierta" else 1


if __name__ == "__main__":
    sys.exit(main())
