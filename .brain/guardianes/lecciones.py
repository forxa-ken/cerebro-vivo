#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lecciones aprendidas de Cerebro Vivo (spec 026): guarda cada lección en `.brain/lecciones/<tema>.md`.

Uso (lo lanza la IA al resolver un hito, skill /leccion):
  python .brain/guardianes/lecciones.py --tema TEMA "problema | causa | regla"
  python .brain/guardianes/lecciones.py ninguna "motivo"      (cierra un hito sin lección)
  python .brain/guardianes/lecciones.py --indice               (rehace el índice)
Cada lección es una línea `- **problema** → causa → **regla** (fecha)`. No repite una lección ya escrita.
El guardián `hitos.py` detecta que se lanzó este script para dar el hito por resuelto.
Solo librería estándar. Si algo falla, avisa y sale con 0."""

import datetime
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, AQUI)
from textos import t  # noqa: E402  (spec 024: mensajes en es/en)

CARPETA = os.path.join(".brain", "lecciones")
LINEA = re.compile(r"^\s*(?:-|\d+\.)\s+\*\*")
ESCRITA = re.compile(r"^- \*\*(.+?)\*\* → .*? → \*\*(.+?)\*\*")


def cargar_config():
    with open(os.path.join(AQUI, "guardianes.json"), encoding="utf-8") as f:
        return json.load(f)


def limpiar_tema(tema):
    tema = re.sub(r"[^a-z0-9_-]+", "-", (tema or "general").strip().lower()).strip("-")
    return tema or "general"


def normalizar(texto):
    return re.sub(r"\W+", " ", texto.lower()).strip()


def contar(ruta):
    try:
        with open(ruta, encoding="utf-8") as f:
            return sum(1 for l in f if LINEA.match(l))
    except OSError:
        return 0


def temas(raiz):
    """[(tema, número de lecciones)] de los archivos de `.brain/lecciones/` (sin el índice)."""
    carpeta = os.path.join(raiz, CARPETA)
    try:
        nombres = sorted(n for n in os.listdir(carpeta) if n.endswith(".md") and n != "indice.md")
    except OSError:
        return []
    return [(n[:-3], contar(os.path.join(carpeta, n))) for n in nombres]


def resumen_temas(raiz):
    """Texto corto para el arranque («video (11), instalacion (2)»); vacío si no hay lecciones."""
    return ", ".join("%s (%d)" % (n, c) for n, c in temas(raiz) if c)


def escribir_indice(raiz, cfg=None):
    filas = ["| [%s](%s.md) | %d |" % (n, n, c) for n, c in temas(raiz)]
    texto = ("# Índice de lecciones\n\n> Lo generan `lecciones.py` y `hitos.py`: no editar a mano. Leer el tema antes de repetir ese trabajo.\n\n"
             "| Tema | Lecciones |\n| :--- | :---: |\n" + "\n".join(filas) + "\n")
    os.makedirs(os.path.join(raiz, CARPETA), exist_ok=True)
    with open(os.path.join(raiz, CARPETA, "indice.md"), "w", encoding="utf-8") as f:
        f.write(texto)


def agregar(raiz, tema, problema, causa, regla, hoy=None):
    """Escribe la lección. Devuelve 'nueva' o 'repetida'. Lanza ValueError si falta el problema o la regla."""
    problema, causa, regla = problema.strip(), causa.strip(), regla.strip()
    if not problema or not regla:
        raise ValueError("falta el problema o la regla")
    tema = limpiar_tema(tema)
    ruta = os.path.join(raiz, CARPETA, tema + ".md")
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    previo = ""
    if os.path.isfile(ruta):
        with open(ruta, encoding="utf-8") as f:
            previo = f.read()
    clave = normalizar(problema + " " + regla)
    for l in previo.splitlines():
        m = ESCRITA.match(l)
        if m and clave == normalizar(m.group(1) + " " + m.group(2)):
            return "repetida"
    fecha = (hoy or datetime.date.today()).isoformat()
    linea = "- **%s** → %s → **%s** (%s)" % (problema, causa or "—", regla, fecha)
    if not previo:
        previo = "# Lecciones: %s\n\nFormato: problema → causa → regla. Las escribe `lecciones.py` en el momento del hito (spec 026).\n\n" % tema
    elif not previo.endswith("\n"):
        previo += "\n"
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(previo + linea + "\n")
    escribir_indice(raiz)
    return "nueva"


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        cfg = cargar_config()
    except Exception:
        cfg = {}
    try:
        if argv[:1] == ["--indice"]:
            escribir_indice(RAIZ)
            print(t(cfg, "lecciones_indice"))
        elif argv[:1] == ["ninguna"]:
            motivo = " ".join(argv[1:]).strip()
            if not motivo:
                print(t(cfg, "lecciones_falta_motivo"))
            else:
                print(t(cfg, "lecciones_ninguna", motivo))
        elif argv[:1] == ["--tema"] and len(argv) >= 3:
            trozos = [p.strip() for p in " ".join(argv[2:]).split("|")]
            if len(trozos) == 2:
                trozos.insert(1, "")
            if len(trozos) != 3 or not trozos[0] or not trozos[2]:
                print(t(cfg, "lecciones_uso"))
            else:
                estado = agregar(RAIZ, argv[1], *trozos)
                print(t(cfg, "lecciones_nueva" if estado == "nueva" else "lecciones_repetida", limpiar_tema(argv[1])))
        else:
            print(t(cfg, "lecciones_uso"))
    except Exception as e:
        print(t(cfg, "lecciones_error", str(e)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
