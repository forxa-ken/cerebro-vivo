#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Actualizador del meta-arnés de Cerebro Vivo (spec 087).

Trae a un proyecto las mejoras del arnés (guardianes, skills, manual, kits, pruebas del método) desde el repo `cerebro-vivo`.

Uso dentro de un proyecto (este archivo vive en `.brain/guardianes/actualizar_arnes.py`):
    python .brain/guardianes/actualizar_arnes.py --simular          # solo muestra qué cambiaría
    python .brain/guardianes/actualizar_arnes.py                    # actualiza (copia de seguridad antes)
Uso desde el repo del arnés (`actualizar.py` en su raíz):
    python actualizar.py RUTA_DEL_PROYECTO [--simular]

Reglas: solo toca los archivos del manifiesto (`manifiesto.json`); si el proyecto modificó a mano uno de ellos NO lo pisa
(se lista; `--forzar RUTA` lo pisa tras guardar copia); nunca toca pendientes, specs, decisiones, registro ni `guardianes.json`
(si el arnés trae claves nuevas de configuración, las propone). Solo librería estándar."""

import argparse
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ_PROPIA = os.path.abspath(os.path.join(AQUI, "..", ".."))
MANIFIESTO = "manifiesto.json"
REGISTRO = os.path.join(".brain", "arnes_instalado.json")
COPIAS = os.path.join(".brain", "copias_arnes")
TEXTO = (".py", ".md", ".txt")
DUENO_ORIGINAL = "Dar" + "win"  # partido a propósito: el kit cambia el nombre del dueño en los textos y no debe cambiar este


def _normalizar(datos, rel):
    """Bytes con saltos de línea unificados (en texto), para que Windows y Linux den la misma huella."""
    return datos.replace(b"\r\n", b"\n") if rel.lower().endswith(TEXTO + (".json", ".js", ".ts", ".tsx", ".html", ".bat")) else datos


def huella(datos):
    return hashlib.sha256(datos).hexdigest()


def leer_bytes(ruta):
    with open(ruta, "rb") as f:
        return f.read()


def ruta_segura(base, rel):
    """Ruta absoluta de `rel` dentro de `base`, o None si intenta salirse de la carpeta."""
    base = os.path.abspath(base)
    ruta = os.path.abspath(os.path.join(base, rel))
    if os.path.isabs(rel) or not (ruta + os.sep).startswith(base + os.sep) or ruta == base:
        return None
    return ruta


def cargar_manifiesto(repo):
    with open(os.path.join(repo, MANIFIESTO), encoding="utf-8") as f:
        m = json.load(f)
    if not isinstance(m.get("archivos"), dict):
        raise ValueError("El manifiesto no tiene la lista de archivos.")
    return m


def cargar_registro(proyecto):
    try:
        with open(os.path.join(proyecto, REGISTRO), encoding="utf-8") as f:
            r = json.load(f)
        return r if isinstance(r, dict) else {}
    except Exception:
        return {}


def guardar_registro(proyecto, registro):
    ruta = os.path.join(proyecto, REGISTRO)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        json.dump(registro, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")


def esperado(repo, rel, dueno):
    """Contenido que debe tener `rel` en el proyecto: el del repo, con el nombre del dueño cambiado en los textos."""
    datos = _normalizar(leer_bytes(os.path.join(repo, rel)), rel)
    if dueno and dueno != DUENO_ORIGINAL and rel.lower().endswith(TEXTO):
        datos = datos.replace(DUENO_ORIGINAL.encode("utf-8"), dueno.encode("utf-8"))
    return datos


def claves_nuevas(repo, proyecto):
    """Claves de primer nivel que el arnés trae en `guardianes.json` y el proyecto aún no tiene (solo se proponen)."""
    try:
        with open(os.path.join(repo, ".brain", "guardianes", "guardianes.json"), encoding="utf-8") as f:
            del_arnes = json.load(f)
        with open(os.path.join(proyecto, ".brain", "guardianes", "guardianes.json"), encoding="utf-8") as f:
            del_proyecto = json.load(f)
    except Exception:
        return {}
    return {k: v for k, v in del_arnes.items() if k not in del_proyecto and k not in ("_ayuda", "arnes_repo")}


def destinos(manifiesto, proyecto):
    """Pares (ruta en el repo, ruta en el proyecto). Con `AGENTS.md` (Codex) las skills de `.claude/skills/` también van a `.agents/skills/`."""
    pares = [(rel, rel) for rel in sorted(manifiesto["archivos"])]
    if os.path.isfile(os.path.join(proyecto, "AGENTS.md")):
        pares += [(rel, ".agents/skills/" + rel[len(".claude/skills/"):]) for rel in sorted(manifiesto["archivos"]) if rel.startswith(".claude/skills/")]
    return pares


def sincronizar(repo, proyecto, dueno=None, simular=False, forzar=(), adoptar=(), ahora=None, forzar_todo=False):
    """Compara el proyecto con el repo y (si no es simulación) copia lo que toca.
    Devuelve {'version_antes', 'version', 'nuevos', 'actualizados', 'sin_cambios', 'a_mano', 'forzados', 'copia', 'claves_nuevas'}.
    `adoptar`: rutas absolutas que el kit de arranque acaba de crear (se tratan como no modificadas a mano).
    `forzar_todo`: pisa (con copia de seguridad) también todo lo modificado a mano; para la primera adopción de un proyecto antiguo."""
    repo, proyecto = os.path.abspath(repo), os.path.abspath(proyecto)
    if repo == proyecto:
        raise ValueError("El proyecto y el repo del arnés son la misma carpeta.")
    manifiesto = cargar_manifiesto(repo)
    registro = cargar_registro(proyecto)
    dueno = dueno or registro.get("dueno")
    archivos_reg = dict(registro.get("archivos") or {})
    adoptar = {os.path.normcase(os.path.abspath(a)) for a in adoptar}
    forzar = {f.replace("\\", "/") for f in forzar}
    res = {"version_antes": registro.get("version"), "version": manifiesto.get("version"), "nuevos": [], "actualizados": [],
           "sin_cambios": [], "a_mano": [], "forzados": [], "copia": None, "claves_nuevas": claves_nuevas(repo, proyecto)}
    por_escribir = []  # (rel, destino, contenido, existia)
    for fuente, rel in destinos(manifiesto, proyecto):
        destino = ruta_segura(proyecto, rel)
        if destino is None or ruta_segura(repo, fuente) is None:
            raise ValueError("Ruta no permitida en el manifiesto: %s" % rel)
        nuevo = esperado(repo, fuente, dueno)
        h_nuevo = huella(nuevo)
        if not os.path.exists(destino):
            res["nuevos"].append(rel)
            por_escribir.append((rel, destino, nuevo, False))
            archivos_reg[rel] = h_nuevo
            continue
        h_actual = huella(_normalizar(leer_bytes(destino), rel))
        if h_actual == h_nuevo:
            res["sin_cambios"].append(rel)
            archivos_reg[rel] = h_nuevo
        elif archivos_reg.get(rel) == h_actual or os.path.normcase(destino) in adoptar:
            res["actualizados"].append(rel)
            por_escribir.append((rel, destino, nuevo, True))
            archivos_reg[rel] = h_nuevo
        elif rel in forzar or forzar_todo:
            res["forzados"].append(rel)
            por_escribir.append((rel, destino, nuevo, True))
            archivos_reg[rel] = h_nuevo
        else:
            res["a_mano"].append(rel)  # modificado a mano (o sin registro previo): no se pisa
    if simular:
        return res
    sobrescritos = [p for p in por_escribir if p[3] and os.path.normcase(p[1]) not in adoptar]  # lo que acaba de crear el kit no necesita copia
    if sobrescritos:
        sello = (ahora or datetime.datetime.now()).strftime("%Y%m%d-%H%M%S")
        res["copia"] = os.path.join(COPIAS, sello)
        for rel, destino, _, _ in sobrescritos:
            copia = os.path.join(proyecto, res["copia"], rel)
            os.makedirs(os.path.dirname(copia), exist_ok=True)
            shutil.copyfile(destino, copia)
    for rel, destino, contenido, _ in por_escribir:
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        with open(destino, "wb") as f:
            f.write(contenido)
    guardar_registro(proyecto, {"version": manifiesto.get("version"), "dueno": dueno, "archivos": archivos_reg})
    return res


def correr_pruebas(repo, proyecto):
    """Pasa las pruebas del método que el proyecto tiene. Devuelve (ok, texto) o (None, aviso) si no hay ninguna."""
    modulos = [m for m in cargar_manifiesto(repo).get("pruebas", []) if os.path.exists(os.path.join(proyecto, *m.split(".")) + ".py")]
    if not modulos:
        return None, "El proyecto no tiene pruebas del método que correr."
    env = dict(os.environ, CEREBRO_SIN_PODA="1", PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-m", "unittest"] + modulos, cwd=proyecto, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=env, stdin=subprocess.DEVNULL, timeout=900)
    return r.returncode == 0, (r.stderr or r.stdout).strip()[-600:]


def localizar_repo(proyecto, indicado):
    """(carpeta del repo, carpeta temporal a borrar o None). Acepta carpeta local o dirección git."""
    origen = indicado or os.environ.get("CEREBRO_ARNES_REPO")
    if not origen:
        try:
            with open(os.path.join(proyecto, ".brain", "guardianes", "guardianes.json"), encoding="utf-8") as f:
                origen = json.load(f).get("arnes_repo")
        except Exception:
            origen = None
    if not origen:
        raise ValueError("No sé dónde está el repo del arnés: indícalo con --repo o anota `arnes_repo` en guardianes.json.")
    if origen.startswith(("http://", "https://", "git@", "ssh://")) or origen.endswith(".git"):
        tmp = tempfile.mkdtemp(prefix="cerebro-vivo-")
        r = subprocess.run(["git", "clone", "--depth", "1", "-q", origen, tmp], capture_output=True, text=True, timeout=180)
        if r.returncode != 0:
            shutil.rmtree(tmp, ignore_errors=True)
            raise ValueError("No pude bajar el repo del arnés: %s" % r.stderr.strip()[-200:])
        return tmp, tmp
    carpeta = origen if os.path.isabs(origen) else os.path.join(proyecto, origen)
    return os.path.abspath(carpeta), None


def informe(res, simular):
    L = ["Arnés %s → %s%s" % (res["version_antes"] or "sin registrar", res["version"], " (simulación: no se escribió nada)" if simular else "")]
    for clave, titulo in (("nuevos", "Archivos nuevos"), ("actualizados", "Archivos que se actualizan"), ("forzados", "Archivos pisados con --forzar")):
        if res[clave]:
            L.append("%s (%d):" % (titulo, len(res[clave])))
            L += ["  + " + r for r in res[clave]]
    L.append("Sin cambios: %d archivo(s)." % len(res["sin_cambios"]))
    if res["a_mano"]:
        L.append("⚠️ Modificados a mano (o sin registro previo) y NO pisados (%d). Decide tú; si quieres la versión nueva usa --forzar RUTA:" % len(res["a_mano"]))
        L += ["  ! " + r for r in res["a_mano"]]
    if res["claves_nuevas"]:
        L.append("Claves nuevas de configuración que el arnés propone (no se escribieron; cópialas a .brain/guardianes/guardianes.json si las quieres):")
        L.append(json.dumps(res["claves_nuevas"], ensure_ascii=False, indent=2))
    if res["copia"]:
        L.append("Copia de seguridad de lo sustituido en %s" % res["copia"])
    return "\n".join(L)


def main(argv=None, repo=None):
    """`repo` indica que se lanza desde el repo del arnés (entonces el proyecto es un argumento)."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Actualiza un proyecto con las mejoras del arnés de Cerebro Vivo")
    if repo:
        ap.add_argument("proyecto", help="carpeta del proyecto que se actualiza")
    else:
        ap.add_argument("--repo", help="carpeta o dirección git del repo del arnés (si no, `arnes_repo` de guardianes.json)")
    ap.add_argument("--simular", action="store_true", help="muestra qué cambiaría sin escribir nada")
    ap.add_argument("--forzar", action="append", default=[], metavar="RUTA", help="pisa este archivo aunque se haya modificado a mano")
    ap.add_argument("--forzar-todo", action="store_true", help="pisa TODO lo modificado a mano (con copia); para adoptar el arnés por primera vez en un proyecto antiguo")
    ap.add_argument("--dueno", help="nombre del dueño (si el proyecto no lo tiene registrado)")
    ap.add_argument("--sin-pruebas", action="store_true", help="no corre las pruebas del método al terminar")
    a = ap.parse_args(argv)
    proyecto = os.path.abspath(a.proyecto if repo else RAIZ_PROPIA)
    temporal = None
    try:
        if not repo:
            repo, temporal = localizar_repo(proyecto, a.repo)
        if not os.path.isfile(os.path.join(repo, MANIFIESTO)):
            print("❌ %s no es el repo del arnés (falta %s)." % (repo, MANIFIESTO))
            return 2
        if not os.path.isdir(proyecto):
            print("❌ No existe la carpeta del proyecto: %s" % proyecto)
            return 2
        res = sincronizar(repo, proyecto, dueno=a.dueno, simular=a.simular, forzar=a.forzar, forzar_todo=a.forzar_todo)
        print(informe(res, a.simular))
        if a.simular or a.sin_pruebas:
            return 0
        ok, texto = correr_pruebas(repo, proyecto)
        if ok is None:
            print("ℹ️ " + texto)
        elif ok:
            print("✅ Pruebas del método del proyecto: en verde.")
        else:
            print("❌ Las pruebas del método fallan tras actualizar (la copia de seguridad está arriba):\n" + texto)
            return 1
        return 0
    except (ValueError, OSError, subprocess.SubprocessError) as e:
        print("❌ %s" % e)
        return 2
    finally:
        if temporal:
            shutil.rmtree(temporal, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
