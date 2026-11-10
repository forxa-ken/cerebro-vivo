#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardián 9 de Cerebro Vivo · secretos (spec 051).

Busca claves y tokens que no deben estar en el código que se sube a GitHub:
  1. Patrones de secretos (alta confianza = formato real de token; baja = asignación sospechosa).
  2. Archivos secretos (`archivos_secretos`) que deben estar ignorados por Git y no subidos.
Modos: --ver (archivos que Git sigue) · --staged (lo preparado para el commit; lo usa el hook pre-commit,
sale con 1 si hay un secreto de alta confianza) · --historial (todo el historial, a mano; anota la fecha)
· --instalar-hook (crea .git/hooks/pre-commit).
Solo librería estándar. Nunca imprime un secreto entero (archivo, línea y 4 primeros caracteres).
Si el escáner falla, calla y deja pasar (el hook nunca debe romper el trabajo). Ajustes: guardianes.json."""

import datetime
import fnmatch
import json
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, AQUI)
from textos import tp  # noqa: E402  (spec 024: mensajes en es/en)
ESTADO = os.path.join(AQUI, "secretos_estado.json")
MARCAS_EJEMPLO = ("tu_", "your", "xxxx", "example", "ejemplo", "changeme", "...", "…", "<", "$", "placeholder", "fake", "dummy")
MAX_BYTES = 1_000_000


def cargar_config():
    with open(os.path.join(AQUI, "guardianes.json"), encoding="utf-8") as f:
        return json.load(f)


def ajustes(cfg):
    a = dict(cfg.get("secretos", {}))
    a["activo"] = bool(cfg.get("secretos_activo", True))
    return a


def _git(raiz, *args, entrada=None):
    return subprocess.run(["git", *args], cwd=raiz, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=60, input=entrada).stdout


def _es_ejemplo(valor):
    v = valor.lower()
    return any(m in v for m in MARCAS_EJEMPLO)


def _permitido(a, archivo, linea):
    for p in a.get("permitidos", []):
        if fnmatch.fnmatch(archivo, p.get("archivo", "*")) and p.get("contiene", "") in linea:
            return True
    return False


def escanear_texto(texto, archivo, a):
    """Hallazgos [(archivo, nº de línea, nombre, confianza, 4 primeros caracteres)] de un texto."""
    hallazgos = []
    patrones = [(p, re.compile(p["regex"])) for p in a.get("patrones", [])]
    for n, linea in enumerate(texto.splitlines(), 1):
        if "base64," in linea or _permitido(a, archivo, linea):
            continue
        for p, rx in patrones:
            m = rx.search(linea)
            if not m:
                continue
            valor = m.group(m.lastindex or 0)
            if _es_ejemplo(valor):
                continue
            hallazgos.append((archivo, n, p["nombre"], p.get("confianza", "alta"), valor[:4]))
    return hallazgos


def _texto_ok(contenido):
    return len(contenido) <= MAX_BYTES and b"\x00" not in contenido[:4096]


def escanear_archivos(raiz, a, rutas):
    hallazgos = []
    for ruta in rutas:
        try:
            with open(os.path.join(raiz, ruta), "rb") as f:
                crudo = f.read(MAX_BYTES + 1)
            if _texto_ok(crudo):
                hallazgos += escanear_texto(crudo.decode("utf-8", "replace"), ruta, a)
        except OSError:
            continue
    return hallazgos


def archivos_seguidos(raiz):
    return [r for r in _git(raiz, "ls-files").splitlines() if r]


def problemas_archivos_secretos(raiz, a):
    """Archivos secretos subidos a Git o que ya no están ignorados."""
    problemas = []
    seguidos = set(archivos_seguidos(raiz))
    for nombre in a.get("archivos_secretos", []):
        if nombre in seguidos:
            problemas.append(tp("secretos_esta_subido_git") % nombre)
        elif subprocess.run(["git", "check-ignore", "-q", nombre], cwd=raiz).returncode != 0:
            problemas.append(tp("secretos_esta_gitignore") % nombre)
    return problemas


def analizar(raiz, cfg):
    """(hallazgos de archivos seguidos, problemas de archivos secretos)."""
    a = ajustes(cfg)
    return escanear_archivos(raiz, a, archivos_seguidos(raiz)), problemas_archivos_secretos(raiz, a)


def analizar_preparados(raiz, a):
    """Hallazgos de lo preparado para el commit (versión del índice) y archivos secretos preparados."""
    hallazgos = []
    nombres = _git(raiz, "diff", "--cached", "--name-only", "--diff-filter=ACM").splitlines()
    secretos = set(a.get("archivos_secretos", []))
    for ruta in nombres:
        if os.path.basename(ruta) in secretos or ruta in secretos:
            hallazgos.append((ruta, 0, tp("secretos_archivo_secreto_preparado"), "alta", ""))
            continue
        contenido = _git(raiz, "show", ":" + ruta)
        if _texto_ok(contenido.encode("utf-8", "replace")):
            hallazgos += escanear_texto(contenido, ruta, a)
    return hallazgos


def escanear_historial(raiz, a):
    """Líneas añadidas en todo el historial (lento; a mano)."""
    hallazgos, archivo, vistos = [], "?", set()
    proc = subprocess.Popen(["git", "log", "--all", "-p", "--no-color", "--format=@@commit %h"], cwd=raiz,
                            stdout=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
    commit = "?"
    for linea in proc.stdout:
        if linea.startswith("@@commit "):
            commit = linea.split()[1]
        elif linea.startswith("+++ b/"):
            archivo = linea[6:].strip()
        elif linea.startswith("+") and not linea.startswith("+++"):
            for h in escanear_texto(linea[1:], "%s@%s" % (archivo, commit), a):
                if (h[0], h[2], h[4]) not in vistos:
                    vistos.add((h[0], h[2], h[4]))
                    hallazgos.append(h)
    proc.wait()
    return hallazgos


def _formato(h):
    return tp("secretos_empieza") % (h[0], h[1], h[2], h[3], h[4])


def dias_desde_historial():
    try:
        with open(ESTADO, encoding="utf-8") as f:
            f_ = datetime.date.fromisoformat(json.load(f)["historial"])
        return (datetime.date.today() - f_).days
    except Exception:
        return None


def resumen(raiz, cfg):
    """Línea para el resumen de arranque. Calla si está apagado o si algo falla."""
    a = ajustes(cfg)
    if not a["activo"]:
        return []
    try:
        hallazgos, problemas = analizar(raiz, cfg)
    except Exception:
        return []
    lineas = []
    if hallazgos or problemas:
        partes = [_formato(hallazgos[0])] if hallazgos else []
        partes += problemas[:1]
        lineas.append(tp("secretos_secretos_aviso_ver") % (len(hallazgos) + len(problemas), "; ".join(partes)))
    else:
        lineas.append(tp("secretos_secretos_sin_avisos"))
    dias, tope = dias_desde_historial(), a.get("dias_aviso_historial", 30)
    if dias is None or dias >= tope:
        lineas.append(tp("secretos_secretos_toca_revisar") %
                      (tp("secretos_nunca_revisado") if dias is None else tp("secretos_hace_dias") % dias))
    return lineas


HOOK = """#!/bin/sh
# Guardián 9 (spec 051): bloquea el commit si hay un secreto de alta confianza. Saltar a conciencia: git commit --no-verify
PY="venv/Scripts/python.exe"; [ -x "$PY" ] || PY=python
# El hook vive en la carpeta común de Git: en un worktree (p. ej. la página en gh-pages) no hay .brain/ aquí; se busca en el repo principal.
G=".brain/guardianes/secretos.py"
if [ ! -f "$G" ]; then
  C="$(git rev-parse --git-common-dir 2>/dev/null)"
  [ -n "$C" ] && G="$C/../.brain/guardianes/secretos.py"
fi
[ -f "$G" ] || { echo "Guardián de secretos no encontrado ($G). Commit bloqueado; instálalo o usa --no-verify a conciencia." >&2; exit 1; }
exec "$PY" "$G" --staged
"""


def instalar_hook(raiz):
    ruta = os.path.join(raiz, ".git", "hooks", "pre-commit")
    if os.path.exists(ruta):
        with open(ruta, encoding="utf-8", errors="replace") as f:
            if "secretos.py" not in f.read():
                return tp("secretos_existe_otro_hook")
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write(HOOK)
    return tp("secretos_hook_instalado") % os.path.relpath(ruta, raiz)


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:
            pass
    args = sys.argv[1:]
    try:
        cfg = cargar_config()
        a = ajustes(cfg)
        if "--instalar-hook" in args:
            print(instalar_hook(RAIZ))
            return
        if "--staged" in args:
            if not a["activo"]:
                return
            raiz = _git(os.getcwd(), "rev-parse", "--show-toplevel").strip() or os.getcwd()
            altos = [h for h in analizar_preparados(raiz, a) if h[3] == "alta"]
            if altos:
                print(tp("secretos_commit_bloqueado_posible"), file=sys.stderr)
                for h in altos:
                    print("   - " + _formato(h), file=sys.stderr)
                print(tp("secretos_quitalo_era_real"),
                      file=sys.stderr)
                sys.exit(1)
            return
        if "--historial" in args:
            hs = escanear_historial(RAIZ, a)
            with open(ESTADO, "w", encoding="utf-8", newline="\n") as f:
                json.dump({"historial": datetime.date.today().isoformat(), "hallazgos": len(hs)}, f)
            print("\n".join("- " + _formato(h) for h in hs) if hs else tp("secretos_historial_sin_hallazgos"))
            print(tp("secretos_total_fecha_anotada") % len(hs))
            return
        hs, pr = analizar(RAIZ, cfg)
        print("\n".join(["- " + _formato(h) for h in hs] + ["- " + p for p in pr]) if hs or pr else tp("secretos_sin_avisos"))
        print("Total: %d." % (len(hs) + len(pr)))
    except SystemExit:
        raise
    except Exception as e:
        print("secretos.py: omitido (%s)" % e, file=sys.stderr)


if __name__ == "__main__":
    main()
