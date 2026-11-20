#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sincronizar (spec 093): deja este ordenador al día con GitHub y listo para trabajar.

Uso:  python .brain/guardianes/sincronizar.py [--simular] [--sin-arranque]
Hace: git fetch, git pull --ff-only (solo avanza; nunca mezcla, nunca pisa, nunca sube nada), y luego enseña el
resumen de arranque (estado, traspaso). Si hay cambios locales que chocan o la rama se ha separado de GitHub,
lo dice y no toca nada. Con --simular solo cuenta lo que haría. Solo librería estándar."""

import argparse
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, AQUI)
from textos import t  # noqa: E402  (spec 024: mensajes en es/en)


def git(raiz, *args):
    return subprocess.run(["git", "-c", "core.quotepath=false"] + list(args), cwd=raiz, capture_output=True,
                          text=True, encoding="utf-8", errors="replace")


def sincronizar(raiz, simular=False, lengua=None):
    """Devuelve (lineas, ok). `ok` es False si algo impide dejar el proyecto al día (la IA debe decírselo a Darwin)."""
    out = []
    r = git(raiz, "rev-parse", "--is-inside-work-tree")
    if r.returncode != 0 or r.stdout.strip() != "true":
        return [t(lengua, "sync_no_git")], False
    r = git(raiz, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    if r.returncode != 0:
        return [t(lengua, "sync_sin_remoto")], False
    remoto = r.stdout.strip()
    r = git(raiz, "fetch", "--quiet")
    if r.returncode != 0:
        return [t(lengua, "sync_fetch_error", (r.stderr or r.stdout).strip()[:200])], False
    r = git(raiz, "rev-list", "--left-right", "--count", "HEAD...@{u}")
    try:
        adelante, atras = [int(x) for x in r.stdout.split()]
    except ValueError:
        return [t(lengua, "sync_fetch_error", r.stderr.strip()[:200])], False
    ok = True
    if atras == 0:
        out.append(t(lengua, "sync_al_dia", remoto))
    elif adelante > 0:
        out.append(t(lengua, "sync_divergido", adelante, atras, remoto))
        ok = False
    elif simular:
        out.append(t(lengua, "sync_bajaria", atras, remoto))
    else:
        p = git(raiz, "pull", "--ff-only", "--quiet")
        if p.returncode == 0:
            out.append(t(lengua, "sync_baja_ok", atras, remoto))
        else:
            out.append(t(lengua, "sync_conflicto", (p.stderr or p.stdout).strip()[:300]))
            ok = False
    if adelante > 0 and atras == 0:
        out.append(t(lengua, "sync_adelantado", adelante))
    sucios = [x for x in git(raiz, "status", "--porcelain").stdout.splitlines() if x.strip()]
    if sucios:
        out.append(t(lengua, "sync_sucio", len(sucios), "; ".join(x.strip() for x in sucios[:6]) + ("…" if len(sucios) > 6 else "")))
    return out, ok


def resumen_arranque(raiz):
    """Lanza arranque.py --manual (ya con lo recién bajado) y devuelve su texto, o cadena vacía si no existe."""
    ruta = os.path.join(raiz, ".brain", "guardianes", "arranque.py")
    if not os.path.isfile(ruta):
        return ""
    r = subprocess.run([sys.executable, ruta, "--manual"], cwd=raiz, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    try:
        datos = json.loads(r.stdout)
        return datos.get("hookSpecificOutput", {}).get("additionalContext") or datos.get("systemMessage", "")
    except Exception:
        return r.stdout.strip()


def main(argv=None):
    ap = argparse.ArgumentParser(description="Deja este ordenador al día con GitHub (solo baja, nunca sube).")
    ap.add_argument("--simular", action="store_true", help="solo cuenta lo que haría")
    ap.add_argument("--sin-arranque", action="store_true", help="no enseña el resumen de arranque al final")
    a = ap.parse_args(argv)
    for flujo in (sys.stdout, sys.stderr):
        try:
            flujo.reconfigure(encoding="utf-8")
        except Exception:
            pass
    lineas, ok = sincronizar(RAIZ, a.simular)
    print(t(None, "sync_titulo"))
    for x in lineas:
        print("- " + x)
    if ok and not a.simular and not a.sin_arranque:
        texto = resumen_arranque(RAIZ)
        if texto:
            print("\n" + texto)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
