#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prototipo del guardián de alcance de la fábrica (spec 035, fase 2).

Comprueba que una ejecutora solo ha tocado los archivos que el encargo permite,
aunque el repositorio ya tuviera otros cambios sin commitear antes de empezar.

Uso:
  python alcance.py snapshot --repo RUTA --salida foto.json
  (la ejecutora trabaja)
  python alcance.py comprobar --repo RUTA --foto foto.json --permitidos a.lua b.lua dir/

Un permitido que termina en / o es una carpeta admite todo lo que cuelgue de ella.
Código de salida: 0 = dentro del alcance, 1 = se tocó algo no permitido.
"""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


def _git(repo, *args):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise SystemExit(f"git falló: {r.stderr.strip()}")
    return r.stdout


def _huella(ruta: Path) -> str:
    if not ruta.is_file():
        return "borrado"
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def estado(repo) -> dict:
    """Archivos con cambios (modificados, borrados o nuevos) y su huella de contenido."""
    repo = Path(repo)
    nombres = set(_git(repo, "ls-files", "-m", "-d", "-o", "--exclude-standard").split("\n"))
    nombres.discard("")
    return {n: _huella(repo / n) for n in sorted(nombres)}


def tomar_foto(repo) -> dict:
    return {"cabeza": _git(repo, "rev-parse", "HEAD").strip(), "archivos": estado(repo)}


def tocados(repo, foto) -> list:
    """Archivos cuyo contenido cambió desde la foto (nuevos, editados, borrados o revertidos)."""
    ahora = estado(repo)
    antes = foto["archivos"]
    if _git(repo, "rev-parse", "HEAD").strip() != foto["cabeza"]:
        raise SystemExit("HEAD cambió desde la foto: hubo un commit durante el trabajo (no permitido).")
    cambiados = {n for n in set(ahora) | set(antes) if ahora.get(n) != antes.get(n)}
    return sorted(cambiados)


def permitido(nombre, permitidos) -> bool:
    nombre = nombre.replace("\\", "/")
    for p in permitidos:
        p = p.replace("\\", "/")
        if p.endswith("/"):
            if nombre.startswith(p):
                return True
        elif nombre == p:
            return True
    return False


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="orden", required=True)
    s = sub.add_parser("snapshot")
    s.add_argument("--repo", required=True)
    s.add_argument("--salida", required=True)
    c = sub.add_parser("comprobar")
    c.add_argument("--repo", required=True)
    c.add_argument("--foto", required=True)
    c.add_argument("--permitidos", nargs="+", required=True)
    a = ap.parse_args(argv)

    if a.orden == "snapshot":
        Path(a.salida).write_text(json.dumps(tomar_foto(a.repo), indent=1), encoding="utf-8")
        print(f"Foto guardada: {a.salida}")
        return 0

    foto = json.loads(Path(a.foto).read_text(encoding="utf-8"))
    cambiados = tocados(a.repo, foto)
    fuera = [n for n in cambiados if not permitido(n, a.permitidos)]
    print(f"Archivos tocados por la tarea: {len(cambiados)}")
    for n in cambiados:
        print(("  FUERA DE ALCANCE  " if n in fuera else "  ok                ") + n)
    if fuera:
        print(f"RECHAZADO: {len(fuera)} archivo(s) fuera del encargo. No se gasta revisión.")
        return 1
    print("DENTRO DEL ALCANCE.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
