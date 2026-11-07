#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guarda la memoria al salir de una IA (spec 022): lo llama `traspaso-out salgo`.

Hace commit solo de la memoria (traspaso, traspasos archivados, registro, pendientes y specs) y lo sube
a GitHub. El código suelto no entra: se lista para que el dueño decida. Nunca fuerza la subida ni mezcla
nada. Si hay otros commits sin subir que no son de memoria, no sube: los lista, y con el sí del dueño
se relanza con --subir-todo. Si Git falla, avisa y el traspaso sigue adelante (siempre sale con 0).
Uso: python .brain/guardianes/guardar_traspaso.py [--subir-todo]. Solo librería estándar."""

import datetime
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, AQUI)
from textos import tp  # noqa: E402  (spec 024: mensajes en es/en)
sys.path.insert(0, AQUI)
import arranque  # noqa: E402  (mismo aviso de lo suelto que el resumen de arranque)


def g(raiz, *args, timeout=30):
    """(código, salida, error) de un comando de Git; nunca lanza excepción ni se queda esperando una clave."""
    entorno = dict(os.environ, GIT_TERMINAL_PROMPT="0")
    try:
        r = subprocess.run(["git", "-c", "core.quotepath=false"] + list(args), cwd=raiz, env=entorno, capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except Exception as e:
        return 1, "", str(e)


def rutas_memoria(cfg):
    return [".brain/traspaso.md", ".brain/archive/traspasos", cfg.get("registro", ".brain/decisions.log"),
            cfg.get("pendientes", ".brain/pendientes.md"), ".brain/specs"]


def es_memoria(ruta, memoria):
    return any(ruta == m or ruta.startswith(m + "/") for m in memoria)


def cambios(raiz, memoria):
    """Archivos de la memoria con cambios; en uno movido, las dos rutas para que el commit lleve el movimiento."""
    cod, salida, _ = g(raiz, "status", "--porcelain", "-z", "--untracked-files=all", "--", *memoria)
    if cod != 0:
        return []
    trozos, rutas, i = salida.split("\0"), [], 0
    while i < len(trozos):
        t = trozos[i]
        i += 1
        if len(t) < 4:
            continue
        rutas.append(t[3:])
        if t[0] in "RC" and i < len(trozos):
            rutas.append(trozos[i])
            i += 1
    return rutas


def hay_secreto(raiz):
    """(True, motivo) si no se puede hacer commit. Sin revisor no se guarda: la subida automática lo necesita."""
    revisor = os.path.join(AQUI, "secretos.py")
    if not os.path.isfile(revisor):
        return True, tp("guardar_traspaso_encuentro_secretos_revisar")
    try:
        r = subprocess.run([sys.executable, revisor, "--staged"], cwd=raiz, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=60)
    except Exception as e:
        return True, tp("guardar_traspaso_revision_secretos_fallo") % e
    return r.returncode != 0, r.stderr.strip()


def hacer_commit(raiz, archivos):
    """(¿sigue adelante?, líneas)."""
    if not archivos:
        return True, [tp("guardar_traspaso_memoria_nada_nuevo")]
    cod, _, err = g(raiz, "add", "-A", "--", *archivos)
    if cod != 0:
        return False, [tp("guardar_traspaso_hecho_commit_memoria") % err.strip()]
    bloqueado, motivo = hay_secreto(raiz)
    if bloqueado:
        g(raiz, "reset", "-q", "--", *archivos)
        return False, [tp("guardar_traspaso_hecho_commit_subido"), motivo]
    mensaje = "chore: memoria del traspaso (%s)" % datetime.date.today().isoformat()
    cod, _, err = g(raiz, "commit", "-q", "-m", mensaje, "--", *archivos)
    if cod != 0:
        g(raiz, "reset", "-q", "--", *archivos)
        return False, [tp("guardar_traspaso_hecho_commit_memoria2") % (err.strip() or tp("guardar_traspaso_git_fallo"))]
    _, corto, _ = g(raiz, "rev-parse", "--short", "HEAD")
    return True, [tp("guardar_traspaso_memoria_guardada_commit") % (corto.strip(), len(archivos))]


def solo_memoria(raiz, commit, memoria):
    cod, salida, _ = g(raiz, "diff-tree", "--no-commit-id", "--name-only", "-r", commit)
    rutas = [r for r in salida.splitlines() if r]
    return cod == 0 and bool(rutas) and all(es_memoria(r, memoria) for r in rutas)


def subir(raiz, memoria, subir_todo):
    """Sube la rama actual a su remoto, sin forzar. Devuelve líneas para el dueño."""
    _, rama, _ = g(raiz, "rev-parse", "--abbrev-ref", "HEAD")
    rama = rama.strip()
    _, remoto, _ = g(raiz, "config", "branch.%s.remote" % rama)
    _, destino, _ = g(raiz, "config", "branch.%s.merge" % rama)
    remoto, destino = remoto.strip(), destino.strip()
    if rama in ("", "HEAD") or not remoto or not destino:
        return [tp("guardar_traspaso_sin_subir_esta")]
    cod, salida, err = g(raiz, "rev-list", "@{u}..HEAD")
    if cod != 0:
        return [tp("guardar_traspaso_sin_subir_podido") % err.strip()]
    pendientes = salida.split()
    if not pendientes:
        return [tp("guardar_traspaso_github_esta_dia")]
    otros = [c for c in pendientes if not solo_memoria(raiz, c, memoria)]
    if otros and not subir_todo:
        lineas = [tp("guardar_traspaso_sin_subir_commits") % len(otros)]
        for c in otros:
            _, texto, _ = g(raiz, "log", "-1", "--format=%h %s", c)
            lineas.append("- " + texto.strip()[:100])
        lineas.append(tp("guardar_traspaso_preguntale_dueno_python"))
        return lineas
    cod, _, err = g(raiz, "push", remoto, "HEAD:%s" % destino, timeout=60)
    if cod != 0:
        return [tp("guardar_traspaso_sin_subir_github"),
                (err.strip().splitlines() or [tp("guardar_traspaso_sin_detalle")])[-1]]
    return [tp("guardar_traspaso_subido_github_commits") % (len(pendientes), rama)]


def guardar(raiz, cfg, subir_todo=False):
    cod, _, _ = g(raiz, "rev-parse", "--is-inside-work-tree")
    if cod != 0:
        return [tp("guardar_traspaso_sin_git_este")]
    memoria = rutas_memoria(cfg)
    sigue, lineas = hacer_commit(raiz, cambios(raiz, memoria))
    if not sigue:
        return lineas
    lineas += subir(raiz, memoria, subir_todo)
    try:
        resto = arranque.sin_commitear(raiz, cfg)
    except Exception:
        resto = []
    if resto:
        lineas.append(arranque.texto_sin_commitear(resto) + tp("guardar_traspaso_entran_este_commit"))
    return lineas


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        cfg = arranque.cargar_config()
    except Exception:
        cfg = {}
    try:
        print("\n".join(guardar(RAIZ, cfg, "--subir-todo" in sys.argv[1:])))
    except Exception as e:
        print(tp("guardar_traspaso_podido_guardar_memoria") % e)
    return 0


if __name__ == "__main__":
    sys.exit(main())
