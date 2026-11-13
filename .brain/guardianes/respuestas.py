#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Respuestas guardadas de Cerebro Vivo (spec 045): archiva en `.brain/respuestas/` una respuesta o comparación útil
de un chat, con su fuente, aunque no venga de un fallo (las lecciones solo nacen de un problema resuelto).

Uso:
  python .brain/guardianes/respuestas.py --titulo "Qué es" --fuente "chat cerebro-vivo #19" "texto de la respuesta"
  python .brain/guardianes/respuestas.py --titulo "Qué es" --fuente "..." -        (lee el texto de la entrada estándar)
  python .brain/guardianes/respuestas.py --indice                                  (rehace el índice)
Cada respuesta es un archivo `.brain/respuestas/AAAA-MM-DD-titulo.md`; el índice `.brain/respuestas/indice.md` las lista.
No pisa una respuesta ya guardada con el mismo título y fecha. Tope de 8 KB por respuesta (si es más larga, resumirla).
Solo librería estándar. Si algo falla, avisa y sale con 0."""

import argparse
import datetime
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, AQUI)
from textos import t  # noqa: E402

CARPETA = os.path.join(".brain", "respuestas")
TOPE_BYTES = 8192


def cargar_config():
    with open(os.path.join(AQUI, "guardianes.json"), encoding="utf-8") as f:
        return json.load(f)


def limpiar_titulo(titulo):
    """Nombre de archivo: minúsculas sin tildes, solo letras, números y guiones."""
    import unicodedata
    base = unicodedata.normalize("NFKD", (titulo or "").strip().lower()).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", base).strip("-")[:60].strip("-")


def listar(raiz):
    """[(archivo, título, fecha, fuente)] de las respuestas guardadas, la más nueva primero."""
    carpeta = os.path.join(raiz, CARPETA)
    try:
        nombres = sorted((n for n in os.listdir(carpeta) if n.endswith(".md") and n != "indice.md"), reverse=True)
    except OSError:
        return []
    salida = []
    for n in nombres:
        titulo, fuente = n[:-3], ""
        try:
            with open(os.path.join(carpeta, n), encoding="utf-8") as f:
                for linea in f.read().splitlines()[:8]:
                    if linea.startswith("# "):
                        titulo = linea[2:].strip()
                    elif linea.lower().startswith(("- **fuente:**", "- **source:**")):
                        fuente = linea.split(":**", 1)[1].strip()
        except OSError:
            pass
        salida.append((n, titulo, n[:10], fuente))
    return salida


def escribir_indice(raiz):
    filas = ["| %s | [%s](%s) | %s |" % (fecha, titulo.replace("|", "/"), n, fuente.replace("|", "/")) for n, titulo, fecha, fuente in listar(raiz)]
    texto = ("# Índice de respuestas guardadas\n\n> Lo genera `respuestas.py`: no editar a mano. Leer aquí antes de volver a preguntar lo mismo.\n\n"
             "| Fecha | Respuesta | Fuente |\n| :--- | :--- | :--- |\n" + "\n".join(filas) + "\n")
    os.makedirs(os.path.join(raiz, CARPETA), exist_ok=True)
    with open(os.path.join(raiz, CARPETA, "indice.md"), "w", encoding="utf-8") as f:
        f.write(texto)


def guardar(raiz, titulo, fuente, texto, hoy=None):
    """Escribe la respuesta. Devuelve (estado, archivo) con estado 'nueva' o 'repetida'.
    Lanza ValueError si falta título, fuente o texto, o si pasa del tope."""
    titulo, fuente, texto = " ".join((titulo or "").split()), " ".join((fuente or "").split()), (texto or "").strip()
    if not titulo or not limpiar_titulo(titulo):
        raise ValueError("titulo")
    if not fuente:
        raise ValueError("fuente")
    if not texto:
        raise ValueError("texto")
    fecha = (hoy or datetime.date.today()).isoformat()
    nombre = "%s-%s.md" % (fecha, limpiar_titulo(titulo))
    ruta = os.path.join(raiz, CARPETA, nombre)
    contenido = "# %s\n\n- **Fuente:** %s\n- **Fecha:** %s\n\n%s\n" % (titulo, fuente, fecha, texto)
    if len(contenido.encode("utf-8")) > TOPE_BYTES:
        raise ValueError("tope")
    if os.path.exists(ruta):
        return "repetida", nombre
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write(contenido)
    escribir_indice(raiz)
    return "nueva", nombre


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        cfg = cargar_config()
    except Exception:
        cfg = {}
    ap = argparse.ArgumentParser(description=t(cfg, "respuestas_descripcion"))
    ap.add_argument("texto", nargs="?", default="", help=t(cfg, "respuestas_ayuda_texto"))
    ap.add_argument("--titulo", default="")
    ap.add_argument("--fuente", default="", help=t(cfg, "respuestas_ayuda_fuente"))
    ap.add_argument("--indice", action="store_true", help=t(cfg, "respuestas_ayuda_indice"))
    a = ap.parse_args(argv)
    try:
        if a.indice:
            escribir_indice(RAIZ)
            print(t(cfg, "respuestas_indice"))
            return 0
        texto = sys.stdin.buffer.read().decode("utf-8", "replace") if a.texto == "-" else a.texto
        estado, nombre = guardar(RAIZ, a.titulo, a.fuente, texto)
        print(t(cfg, "respuestas_nueva" if estado == "nueva" else "respuestas_repetida", nombre))
    except ValueError as e:
        motivo = str(e)
        if motivo == "titulo":
            print(t(cfg, "respuestas_falta_titulo"))
        elif motivo == "fuente":
            print(t(cfg, "respuestas_falta_fuente"))
        elif motivo == "texto":
            print(t(cfg, "respuestas_falta_texto"))
        else:
            print(t(cfg, "respuestas_tope", TOPE_BYTES))
    except Exception as e:
        print(t(cfg, "respuestas_error", str(e)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
