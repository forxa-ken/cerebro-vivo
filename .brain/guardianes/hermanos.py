#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Proyectos hermanos (spec 043): qué commits de un proyecto hermano faltan por portar a este. Solo lectura, solo librería estándar.

  python .brain/guardianes/hermanos.py

Lee `proyectos_hermanos` de guardianes.json: lista de {nombre, ruta, rama, archivo_portar}. Para cada hermano compara con git sus
commits con el archivo de portar de ESTE proyecto (formato en biblioteca/PLANTILLA_PORTAR.md):
- «Último portado»: un commit del hermano; solo cuentan los posteriores.
- «Hecho»: cada commit que aparece ahí (portado o «no aplica») ya no es pendiente.
No hace `fetch` ni cambia nada. Si el hermano no es accesible, calla (solo el comando manual lo dice). Sin hermanos, no dice nada."""
import json
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, AQUI)
from textos import t  # noqa: E402

TOPE_COMMITS = 300
SECCIONES = {
    "ultimo": ("último portado", "ultimo portado", "last ported"),
    "pendiente": ("pendiente", "pending"),
    "hecho": ("hecho", "done"),
}
HASH = re.compile(r"\b[0-9a-f]{7,40}\b")


def _git(carpeta, *args):
    """Salida de git en `carpeta`, o None si falla (no es repositorio, no existe, git ausente)."""
    try:
        r = subprocess.run(["git", "-C", carpeta] + list(args), capture_output=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    return r.stdout.decode("utf-8", "replace") if r.returncode == 0 else None


def _leer(ruta):
    try:
        with open(ruta, "rb") as f:
            return f.read().decode("utf-8", "replace")
    except OSError:
        return None


def secciones(texto):
    """Reparte el archivo de portar en {'ultimo','pendiente','hecho'} según sus encabezados «## ...» (es/en)."""
    res = {"ultimo": "", "pendiente": "", "hecho": ""}
    actual = None
    for linea in texto.splitlines():
        m = re.match(r"^#{1,3}\s+(.*?)\s*$", linea)
        if m and linea.startswith("##") and not linea.startswith("###"):
            nombre = m.group(1).lower().rstrip(":")
            actual = next((k for k, alias in SECCIONES.items() if any(nombre.startswith(a) for a in alias)), None)
            continue
        if actual:
            res[actual] += linea + "\n"
    return res


def _hashes(texto):
    return set(HASH.findall(texto.lower()))


def _cubierto(commit, conocidos):
    """Un commit está cubierto si su hash completo o un prefijo de 7 o más caracteres figura en `conocidos`."""
    return any(commit.startswith(h) for h in conocidos)


def _ruta(raiz, ruta):
    return ruta if os.path.isabs(ruta) else os.path.normpath(os.path.join(raiz, ruta))


def revisar_uno(raiz, hermano):
    """Devuelve {'nombre','estado','pendientes':[(hash corto, asunto)]}; estado: 'ok', 'inaccesible' o 'sin_archivo'."""
    nombre = str(hermano.get("nombre") or hermano.get("ruta") or "?")
    res = {"nombre": nombre, "estado": "ok", "pendientes": []}
    carpeta = _ruta(raiz, str(hermano.get("ruta", "")))
    rama = str(hermano.get("rama") or "HEAD")
    if not hermano.get("ruta") or not os.path.isdir(carpeta) or _git(carpeta, "rev-parse", "--verify", rama + "^{commit}") is None:
        res["estado"] = "inaccesible"
        return res
    texto = _leer(os.path.join(raiz, str(hermano.get("archivo_portar", ""))))
    if texto is None:
        res["estado"] = "sin_archivo"
        texto = ""
    sec = secciones(texto)
    rango = rama
    for h in sorted(_hashes(sec["ultimo"]), key=len, reverse=True):
        if _git(carpeta, "rev-parse", "--verify", h + "^{commit}") is not None:
            rango = h + ".." + rama
            break
    salida = _git(carpeta, "log", "--no-merges", "--format=%H\t%h\t%s", "-n", str(TOPE_COMMITS), rango)
    if salida is None:
        res["estado"] = "inaccesible"
        return res
    hechos = _hashes(sec["hecho"])
    for linea in salida.splitlines():
        partes = (linea.split("\t", 2) + ["", ""])[:3]
        completo, corto, asunto = partes
        if completo and not _cubierto(completo, hechos):
            res["pendientes"].append((corto, asunto))
    return res


def hermanos_configurados(cfg):
    datos = cfg.get("proyectos_hermanos") if isinstance(cfg, dict) else None
    return [h for h in datos if isinstance(h, dict)] if isinstance(datos, list) else []


def revisar(raiz, cfg):
    return [revisar_uno(raiz, h) for h in hermanos_configurados(cfg)]


def lineas_arranque(raiz, cfg):
    """Una línea por hermano con commits sin portar. Silencio si no hay hermanos, no son accesibles o no falta nada."""
    salida = []
    for r in revisar(raiz, cfg):
        n = len(r["pendientes"])
        if r["estado"] != "inaccesible" and n:
            salida.append(t(cfg, "hermanos_aviso_arranque", n, "" if n == 1 else "s", r["nombre"]))
    return salida


def informe(raiz, cfg):
    """Texto completo para el comando manual."""
    hermanos = hermanos_configurados(cfg)
    if not hermanos:
        return [t(cfg, "hermanos_sin_config")]
    lineas = []
    for r in revisar(raiz, cfg):
        if r["estado"] == "inaccesible":
            lineas.append(t(cfg, "hermanos_inaccesible", r["nombre"]))
            continue
        if r["estado"] == "sin_archivo":
            lineas.append(t(cfg, "hermanos_sin_archivo", r["nombre"]))
        if not r["pendientes"]:
            lineas.append(t(cfg, "hermanos_al_dia", r["nombre"]))
            continue
        lineas.append(t(cfg, "hermanos_cabecera", r["nombre"], len(r["pendientes"])))
        lineas += ["  " + corto + " " + asunto for corto, asunto in r["pendientes"][:30]]
        if len(r["pendientes"]) > 30:
            lineas.append(t(cfg, "hermanos_mas", len(r["pendientes"]) - 30))
    return lineas


def main(argv=None):
    try:
        with open(os.path.join(AQUI, "guardianes.json"), "rb") as f:
            cfg = json.loads(f.read().decode("utf-8"))
    except (OSError, ValueError):
        cfg = {}
    for l in informe(RAIZ, cfg):
        print(l)
    return 0


if __name__ == "__main__":
    sys.exit(main())
