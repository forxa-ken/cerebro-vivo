#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prepara una carpeta de la prueba del índice (spec 004). Copia SOLO LECTURA de un `.brain` real (LoboHook) a una
carpeta FUERA de los dos proyectos. Lados: a (con índice), b (sin índice), c (índice con 5 filas falsas).

Uso:  python bench/indice/montar.py a|b|c 1..5 [--origen RUTA_.brain] [--destino RUTA] [--nombres-planos]
`--nombres-planos`: las fichas pasan de `D-062-creditos-de-ia.md` a `D-062.md` (sin pista en el nombre) y el destino por defecto es `bench-indice-planos`.
Lo que hubiera se MUEVE a `_historial/` (no se borra). Imprime el texto exacto a pegar en el chat nuevo."""
import argparse
import os
import re
import shutil
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from preguntas import PREGUNTAS, FORMATO  # noqa: E402

REPO = os.path.dirname(os.path.dirname(AQUI))
ORIGEN = os.path.join(os.path.dirname(REPO), "LoboHook", ".brain")
DESTINO = os.path.join(os.path.dirname(REPO), "bench-indice")
DESTINO_PLANOS = os.path.join(os.path.dirname(REPO), "bench-indice-planos")

CLAUDE = {
    "a": "# Memoria del proyecto\nSolo lectura: no modifiques ningún archivo. Responde en español.\n"
         "La memoria está en `.brain/`. Empieza por los índices (`.brain/decisions/indice.md` y `.brain/archive/hechos-indice.md`) "
         "y abre solo la ficha que corresponda.\n",
    "b": "# Memoria del proyecto\nSolo lectura: no modifiques ningún archivo. Responde en español.\n"
         "La memoria está en `.brain/` (fichas de decisión en `.brain/decisions/` y hechos en `.brain/archive/hechos.md`).\n",
}
CLAUDE["c"] = CLAUDE["a"]
INDICES = [os.path.join("decisions", "indice.md"), os.path.join("archive", "hechos-indice.md")]
ARCHIVOS = [os.path.join("archive", "hechos.md"), os.path.join("archive", "hechos-indice.md")]  # solo esos dos de archive/ (el resto son traspasos y registros viejos)


def _fila(texto, ident):
    m = re.search(r"^\| \[%s\]\(([^)]+)\) \| (.*)$" % re.escape(ident), texto, re.M)
    return m


def aplanar(decisiones):
    """Quita la descripción del nombre de cada ficha (D-062-xxx.md -> D-062.md), también en `archivo/`, y arregla los enlaces del índice."""
    for raiz, _, nombres in os.walk(decisiones):
        for n in nombres:
            m = re.match(r"^(D-\d+)-.+\.md$", n)
            if m:
                os.rename(os.path.join(raiz, n), os.path.join(raiz, m.group(1) + ".md"))
    ind = os.path.join(decisiones, "indice.md")
    if os.path.isfile(ind):
        with open(ind, encoding="utf-8") as f:
            t = f.read()
        t = re.sub(r"\((archivo/)?(D-\d+)-[^)]*\.md\)", lambda m: "(%s%s.md)" % (m.group(1) or "", m.group(2)), t)
        with open(ind, "w", encoding="utf-8") as f:
            f.write(t)


def estropear(texto):
    """5 filas falsas en decisions/indice.md: 4 con el enlace cruzado (D-054↔D-062, D-055↔D-056) y D-053 con la
    descripción de D-065. Devuelve (texto, cuántas)."""
    n = 0
    for a, b in (("D-054", "D-062"), ("D-055", "D-056")):
        ma, mb = _fila(texto, a), _fila(texto, b)
        if ma and mb:
            ea, eb = ma.group(1), mb.group(1)
            texto = texto.replace("[%s](%s)" % (a, ea), "[%s](@@)" % a).replace("[%s](%s)" % (b, eb), "[%s](%s)" % (b, ea)).replace("[%s](@@)" % a, "[%s](%s)" % (a, eb))
            n += 2
    m53, m65 = _fila(texto, "D-053"), _fila(texto, "D-065")
    if m53 and m65:
        d53 = m53.group(2).split(" | ")
        d65 = m65.group(2).split(" | ")
        texto = texto.replace(m53.group(0), m53.group(0).replace(d53[0], d65[0], 1))
        n += 1
    return texto, n


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("lado", choices=["a", "b", "c"])
    ap.add_argument("pregunta", type=int, choices=sorted(PREGUNTAS))
    ap.add_argument("--origen", default=ORIGEN)
    ap.add_argument("--destino")
    ap.add_argument("--nombres-planos", action="store_true")
    a = ap.parse_args(argv)
    a.destino = a.destino or (DESTINO_PLANOS if a.nombres_planos else DESTINO)
    if not os.path.isdir(os.path.join(a.origen, "decisions")):
        print("No encuentro %s" % a.origen)
        return 1
    carpeta = os.path.normpath(os.path.join(a.destino, "lado_" + a.lado))
    os.makedirs(carpeta, exist_ok=True)
    viejos = os.listdir(carpeta)
    if viejos:
        hist = os.path.join(a.destino, "_historial", "lado_%s-%s" % (a.lado, time.strftime("%Y%m%d-%H%M%S")))
        os.makedirs(hist, exist_ok=True)
        for n in viejos:
            os.rename(os.path.join(carpeta, n), os.path.join(hist, n))
    cerebro = os.path.join(carpeta, ".brain")
    shutil.copytree(os.path.join(a.origen, "decisions"), os.path.join(cerebro, "decisions"))
    os.makedirs(os.path.join(cerebro, "archive"))
    for f in ARCHIVOS:
        shutil.copy(os.path.join(a.origen, f), os.path.join(cerebro, f))
    if a.nombres_planos:
        aplanar(os.path.join(cerebro, "decisions"))
    if a.lado == "b":
        for i in INDICES:
            os.remove(os.path.join(cerebro, i))
    if a.lado == "c":
        p = os.path.join(cerebro, INDICES[0])
        with open(p, encoding="utf-8") as f:
            t, n = estropear(f.read())
        with open(p, "w", encoding="utf-8") as f:
            f.write(t)
        if n != 5:
            print("Aviso: solo pude estropear %d filas (se esperaban 5)" % n)
    with open(os.path.join(carpeta, "CLAUDE.md"), "w", encoding="utf-8") as f:
        f.write(CLAUDE[a.lado])
    print("Carpeta lista: %s\nAbre un chat NUEVO ahí (mismo modelo y esfuerzo) y pega:\n\n%s %s\n" % (carpeta, PREGUNTAS[a.pregunta][0], FORMATO))
    return 0


if __name__ == "__main__":
    sys.exit(main())
