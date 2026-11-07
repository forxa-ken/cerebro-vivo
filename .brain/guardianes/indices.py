#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cierre sin trabajo repetido (spec 083). Lo usa `cerrar.py`; solo librería estándar.

- filas_decisiones_faltantes: añade a decisions/indice.md las filas de fichas D-NNN que no tienen (nunca borra ni cambia filas).
- pasar_a_hechos: mueve un punto de pendientes.md a archive/hechos.md + su fila en hechos-indice.md.
Las dos devuelven los textos nuevos y no escriben: quien llama decide (así existe la vista previa)."""

import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from textos import tp  # noqa: E402  (spec 024: mensajes en es/en)


def leer(ruta):
    with open(ruta, encoding="utf-8", newline="") as f:
        return f.read()


def escribir(ruta, texto):
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        f.write(texto)


def _salto(texto):
    return "\r\n" if "\r\n" in texto else "\n"


def filas_decisiones_faltantes(brain):
    """Devuelve (indice_nuevo, filas_añadidas). También separa filas pegadas en una sola línea."""
    texto = leer(os.path.join(brain, "decisions", "indice.md"))
    nl = _salto(texto)
    texto = re.sub(r"\|\| (\[D-\d{3}\])", lambda m: "|" + nl + "| " + m.group(1), texto)
    enlazadas = set(re.findall(r"\]\((?:archivo/)?(D-\d{3}-[^)]*\.md)\)", texto))
    nuevas = []
    for sub, prefijo in (("", ""), ("archivo", "archivo/")):
        carpeta = os.path.join(brain, "decisions", sub)
        if not os.path.isdir(carpeta):
            continue
        for f in sorted(os.listdir(carpeta)):
            m = re.match(r"(D-\d{3})-.*\.md$", f)
            if not m or f in enlazadas:
                continue
            ficha = leer(os.path.join(carpeta, f))
            titulo = re.match(r"# D-\d{3}:?\s*(.+)", ficha)
            area = re.search(r"\*\*Área:\*\*\s*(.+)", ficha)
            estado = re.search(r"\*\*Estado:\*\*\s*(.+)", ficha)
            nuevas.append("| [%s](%s%s) | %s | %s | %s |" % (
                m.group(1), prefijo, f, titulo.group(1).strip() if titulo else f,
                area.group(1).strip() if area else "—", estado.group(1).strip() if estado else "vigente"))
    if nuevas:
        texto = texto.rstrip("\r\n") + nl + nl.join(nuevas) + nl
    return texto, nuevas


def pasar_a_hechos(brain, num, titulo, detalle, ref, fecha, conservar=False):
    """Devuelve (pendientes, hechos, hechos_indice) nuevos. Falla si el punto ya está en hechos o no está en pendientes."""
    pend = leer(os.path.join(brain, "pendientes.md"))
    hechos = leer(os.path.join(brain, "archive", "hechos.md"))
    indice = leer(os.path.join(brain, "archive", "hechos-indice.md"))
    nl = _salto(pend)
    num = str(num).strip()
    if re.search(r"^## %s ·" % re.escape(num), hechos, flags=re.M):
        raise ValueError(tp("indices_punto_esta_hechos") % num)
    patron = re.compile(r"^- \*\*%s(?::\*\*| \().*(?:\r?\n|$)" % re.escape(num), flags=re.M)
    if not conservar:
        if not patron.search(pend):
            raise ValueError(tp("indices_encuentro_punto_pendientes") % num)
        pend = patron.sub("", pend, count=1)
    entrada = "## %s · %s%s**Fecha:** %s · **Ref:** %s%s%s%s%s" % (num, titulo, nl, fecha, ref, nl, detalle, nl, nl)
    primero = re.search(r"^## ", hechos, flags=re.M)
    if primero:
        hechos = hechos[:primero.start()] + entrada + hechos[primero.start():]
    else:
        hechos = hechos.rstrip() + nl + nl + entrada
    cab = re.search(r"^\| :---.*(?:\r?\n)", indice, flags=re.M)
    if not cab:
        raise ValueError(tp("indices_hechos_indice_tiene"))
    fila = "| %s | %s | %s | %s |" % (num, titulo, fecha, ref)
    indice = indice[:cab.end()] + fila + nl + indice[cab.end():]
    return pend, hechos, indice
