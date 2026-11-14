#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Búsqueda local sobre la memoria `.brain/` (spec 049): encuentra qué dice la memoria sobre un tema sin leer carpetas enteras.

Uso:
  python .brain/guardianes/buscar.py tope de bytes            los 10 mejores archivos, con las líneas donde sale
  python .brain/guardianes/buscar.py --max 5 heredoc          cambia el máximo
  python .brain/guardianes/buscar.py --solo lecciones heredoc limita a una carpeta (lecciones, decisions, specs, respuestas...)
  python .brain/guardianes/buscar.py --archivo hermanos       incluye `archive/` (historia; fuera por defecto)
  python .brain/guardianes/buscar.py --json hermanos          salida para otras herramientas
Recorre `.brain/**/*.md` y `decisions.log` en cada consulta (sin índice que se quede viejo). No distingue mayúsculas ni tildes.
Puntúa más si la palabra está en el título o en un encabezado y si salen varias palabras de la consulta en el mismo archivo.
Solo lectura, solo librería estándar. Si la memoria pasa de ~5 MB o tarda más de 1 s, habrá que pasar a un índice (spec 049)."""

import json
import os
import re
import sys
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, AQUI)
from textos import tp  # noqa: E402

MAX_POR_DEFECTO = 10
SALTAR = ("notas-chats", "copias_arnes", "pruebas", "diapositivas")  # datos de trabajo, no memoria; archive se controla con --archivo
PESO_TITULO, PESO_ENCABEZADO, PESO_TEXTO = 10, 4, 1
TOPE_TEXTO = 8  # un archivo larguísimo no gana solo por repetir la palabra
VACIAS = {"de", "la", "el", "en", "y", "a", "los", "las", "un", "una", "del", "al", "se", "que", "por", "con", "para", "lo", "es",
          "the", "of", "and", "to", "in", "is", "for", "on", "an", "it", "or"}


def normalizar(texto):
    """Minúsculas y sin tildes."""
    return unicodedata.normalize("NFKD", texto.lower()).encode("ascii", "ignore").decode("ascii")


def palabras(consulta):
    return [p for p in re.findall(r"[a-z0-9_]{2,}", normalizar(consulta)) if p not in VACIAS]


def archivos(raiz, solo=None, con_archivo=False):
    """[ruta relativa con /] de lo que se busca."""
    brain = os.path.join(raiz, ".brain")
    salida = []
    for base, carpetas, nombres in os.walk(brain):
        rel_base = os.path.relpath(base, raiz).replace(os.sep, "/")
        carpetas[:] = [c for c in carpetas if c not in SALTAR and (con_archivo or c != "archive" or rel_base != ".brain")]
        for n in nombres:
            rel = rel_base + "/" + n
            if not (n.endswith(".md") or n == "decisions.log"):
                continue
            if solo and not any(rel.startswith(".brain/%s/" % s) or rel == ".brain/%s" % s for s in solo):
                continue
            salida.append(rel)
    return sorted(salida)


def puntuar(texto, rel, claves):
    """(puntos, [(linea, texto)]) de un archivo; (0, []) si no sale ninguna palabra."""
    lineas = texto.splitlines()
    norm = [normalizar(l) for l in lineas]
    titulo = next((i for i, l in enumerate(lineas) if l.startswith("# ")), None)
    puntos, vistas, hallazgos, de_texto = 0, set(), [], 0
    nombre = normalizar(os.path.basename(rel))
    for c in claves:
        if c in nombre:
            puntos += PESO_TITULO
            vistas.add(c)
    for i, ln in enumerate(norm):
        dentro = [c for c in claves if c in ln]
        if not dentro:
            continue
        vistas.update(dentro)
        peso = PESO_TITULO if i == titulo else PESO_ENCABEZADO if lineas[i].startswith("#") else PESO_TEXTO
        if peso == PESO_TEXTO:
            de_texto = min(TOPE_TEXTO, de_texto + len(dentro))
        else:
            puntos += peso * len(dentro)
        hallazgos.append((i + 1, lineas[i].strip(), len(dentro) * peso))
    if not vistas:
        return 0, [], ""
    puntos += de_texto * PESO_TEXTO
    puntos += 6 * (len(vistas) - 1)  # varias palabras de la consulta en el mismo archivo: sube
    hallazgos.sort(key=lambda h: (-h[2], h[0]))
    titulo_txt = lineas[titulo][2:].strip() if titulo is not None else os.path.basename(rel)
    return puntos, [(n, t[:160]) for n, t, _ in hallazgos[:2]], titulo_txt


def buscar(raiz, consulta, maximo=MAX_POR_DEFECTO, solo=None, con_archivo=False):
    claves = palabras(consulta)
    if not claves:
        return []
    res = []
    for rel in archivos(raiz, solo, con_archivo):
        try:
            with open(os.path.join(raiz, rel), encoding="utf-8", errors="replace") as f:
                texto = f.read()
        except OSError:
            continue
        puntos, lineas, titulo = puntuar(texto, rel, claves)
        if puntos:
            res.append({"archivo": rel, "titulo": titulo, "puntos": puntos, "lineas": [{"linea": n, "texto": t} for n, t in lineas]})
    res.sort(key=lambda r: (-r["puntos"], r["archivo"]))
    return res[:maximo]


def formatear(res, consulta):
    if not res:
        return tp("buscar_sin_resultados") % consulta
    L = [tp("buscar_titulo") % (len(res), consulta), ""]
    for r in res:
        L.append("%s  (%s)" % (r["archivo"], r["titulo"]))
        L += ["    %s:%d  %s" % (r["archivo"], x["linea"], x["texto"]) for x in r["lineas"]]
    return "\n".join(L)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args, maximo, solo, con_archivo, como_json, resto = sys.argv[1:], MAX_POR_DEFECTO, None, False, False, []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--max" and i + 1 < len(args):
            try:
                maximo = max(1, int(args[i + 1]))
            except ValueError:
                pass
            i += 1
        elif a == "--solo" and i + 1 < len(args):
            solo = [s.strip().strip("/") for s in args[i + 1].split(",") if s.strip()]
            i += 1
        elif a == "--archivo":
            con_archivo = True
        elif a == "--json":
            como_json = True
        else:
            resto.append(a)
        i += 1
    consulta = " ".join(resto).strip()
    if not palabras(consulta):
        print(tp("buscar_uso"))
        return 0
    res = buscar(RAIZ, consulta, maximo, solo, con_archivo)
    print(json.dumps(res, ensure_ascii=False, indent=2) if como_json else formatear(res, consulta))
    return 0


if __name__ == "__main__":
    sys.exit(main())
