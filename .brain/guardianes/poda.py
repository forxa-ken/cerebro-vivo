#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardián 6 de Cerebro Vivo · poda de memoria (spec 048). Mueve, nunca borra.

Mueve a `archivo/` las specs ya terminadas y las fichas de decisión «reemplazada», reescribe los
enlaces de los .md que las citan y mantiene un índice de una línea por spec archivada.
Lo llama `arranque.py` al abrir el chat; a mano:  poda.py --ver  (ensayo, no toca nada) · poda.py --aplicar
Solo librería estándar. Ante cualquier duda no mueve nada y avisa. Se apaga con "poda_activa": false."""

import io
import json
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, AQUI)
from textos import tp  # noqa: E402  (spec 024: mensajes en es/en)
IGNORAR_CARPETAS = {".git", "venv", "node_modules", "__pycache__", "scratch"}
ENLACE = re.compile(r"\]\(([^)\s]+)\)")


def git(raiz, *args):
    r = subprocess.run(["git", "-c", "core.quotepath=false"] + list(args), cwd=raiz,
                       capture_output=True, text=True, encoding="utf-8", timeout=30)
    return r.returncode, r.stdout


def leer(ruta):
    with io.open(ruta, encoding="utf-8", newline="") as f:
        return f.read()


def escribir(ruta, texto):
    with io.open(ruta, "w", encoding="utf-8", newline="") as f:
        f.write(texto)


def estado_de(texto):
    m = re.search(r"^- \*\*Estado:\*\*\s*(.+)$", texto, flags=re.M)
    return m.group(1).strip() if m else ""


def es_terminada(estado):
    """Terminada = implementada / hecha / reemplazada / descartada y sin nada pendiente de prueba."""
    e = estado.lower()
    if not re.match(r"(implementada|hecha|reemplazada|descartada)", e):
        return False
    return not any(p in e for p in ("pendiente", "falta", "sin probar", "fase b", "fase c"))


def candidatas(raiz):
    """[(origen, destino)] con rutas relativas a la raíz (barras /). Solo lo claramente terminado."""
    brain = os.path.join(raiz, ".brain")
    try:
        pend = leer(os.path.join(brain, "pendientes.md"))
    except Exception:
        return []
    try:
        with io.open(os.path.join(AQUI, "guardianes.json"), encoding="utf-8") as f:
            excluir = set(json.load(f).get("poda_excluir", []))  # números de spec que se quedan a la vista
    except Exception:
        excluir = set()
    out = []
    carpeta = os.path.join(brain, "specs")
    for f in sorted(os.listdir(carpeta)):
        m = re.match(r"(\d{3})-.*\.md$", f)
        if not m:
            continue
        if m.group(1) in excluir or re.search(r"(?<!\d)%s(?!\d)" % m.group(1), pend):
            continue  # sigue citada en pendientes: no está cerrada del todo
        if es_terminada(estado_de(leer(os.path.join(carpeta, f)))):
            out.append((".brain/specs/" + f, ".brain/specs/archivo/" + f))
    carpeta = os.path.join(brain, "decisions")
    for f in sorted(os.listdir(carpeta)):
        # solo «reemplazada por D-NNN» a secas: si es parcial («solo la parte de…») sigue vigente en algo
        if re.match(r"D-\d{3}-.*\.md$", f) and re.match(r"reemplazada por D-\d{3}\.?$", estado_de(leer(os.path.join(carpeta, f))), flags=re.I):
            out.append((".brain/decisions/" + f, ".brain/decisions/archivo/" + f))
    return out


def archivos_md(raiz):
    for base, dirs, files in os.walk(raiz):
        dirs[:] = [d for d in dirs if d not in IGNORAR_CARPETAS]
        for f in files:
            if f.endswith(".md"):
                yield os.path.join(base, f)


def _norm(p):
    return os.path.normpath(p)


def reescribir(texto, ruta_vieja, ruta_nueva, mapa_abs):
    """Reescribe enlaces relativos de un .md: `ruta_vieja` = dónde estaba, `ruta_nueva` = dónde queda.
    `mapa_abs` = {ruta absoluta vieja: ruta absoluta nueva} de todo lo movido."""
    viejo_dir, nuevo_dir = os.path.dirname(ruta_vieja), os.path.dirname(ruta_nueva)

    def cambia(m):
        t = m.group(1)
        if re.match(r"^([a-z][a-z0-9+.-]*:|#|/)", t, flags=re.I):
            return m.group(0)
        ruta, sep, ancla = t.partition("#")
        destino_viejo = _norm(os.path.join(viejo_dir, ruta))
        destino_nuevo = mapa_abs.get(destino_viejo, destino_viejo)
        rel = os.path.relpath(destino_nuevo, nuevo_dir).replace("\\", "/")
        return "](%s%s%s)" % (rel, sep, ancla)

    return ENLACE.sub(cambia, texto)


def enlaces_rotos(raiz):
    """{(archivo, enlace)} de los enlaces relativos a archivos que no existen."""
    rotos = set()
    for ruta in archivos_md(raiz):
        try:
            texto = leer(ruta)
        except Exception:
            continue
        for t in ENLACE.findall(texto):
            if re.match(r"^([a-z][a-z0-9+.-]*:|#|/)", t, flags=re.I):
                continue
            destino = t.partition("#")[0]
            if destino and not os.path.exists(_norm(os.path.join(os.path.dirname(ruta), destino))):
                rotos.add((os.path.relpath(ruta, raiz).replace("\\", "/"), t))
    return rotos


def sucios(raiz, rutas):
    """Rutas (relativas) con cambios sin guardar en Git; None si Git falla."""
    cod, salida = git(raiz, "status", "--porcelain")
    if cod != 0:
        return None
    modificados = {l[3:].strip().strip('"').replace("\\", "/") for l in salida.splitlines()}
    return [r for r in rutas if r in modificados]


def indice_archivo(raiz):
    carpeta = os.path.join(raiz, ".brain", "specs", "archivo")
    if not os.path.isdir(carpeta):
        return
    filas = []
    for f in sorted(os.listdir(carpeta)):
        if re.match(r"\d{3}-.*\.md$", f):
            titulo = re.search(r"^#\s*(.+)$", leer(os.path.join(carpeta, f)), flags=re.M)
            filas.append("- [%s](%s) — %s" % (f[:-3], f, titulo.group(1).strip() if titulo else f))
    escribir(os.path.join(carpeta, "indice.md"),
             "# Specs archivadas\n\nSpecs terminadas, movidas aquí por el guardián de poda (spec 048). Nada se borra.\n\n"
             + "\n".join(filas) + "\n")


def plan(raiz):
    """Ensayo: {'mover': [...], 'bloqueado': motivo o None}."""
    mover = candidatas(raiz)
    if not mover:
        return {"mover": [], "bloqueado": None}
    implicados = [o for o, _ in mover]
    sucio = sucios(raiz, implicados)
    if sucio is None:
        return {"mover": mover, "bloqueado": tp("poda_git_responde")}
    if sucio:
        return {"mover": mover, "bloqueado": tp("poda_cambios_sin_guardar") + ", ".join(sucio[:3])}
    return {"mover": mover, "bloqueado": None}


def aplicar(raiz, mover):
    """Mueve con `git mv`, reescribe enlaces y comprueba que no quedan enlaces nuevos rotos;
    si quedan, lo deshace todo. Devuelve (movidos, error o None)."""
    antes = enlaces_rotos(raiz)
    originales, hechos = {}, []
    mapa = {_norm(os.path.join(raiz, o)): _norm(os.path.join(raiz, d)) for o, d in mover}
    try:
        for o, d in mover:
            os.makedirs(os.path.dirname(os.path.join(raiz, d)), exist_ok=True)
            cod, _ = git(raiz, "mv", o, d)
            if cod != 0:
                raise RuntimeError(tp("poda_git_fallo") + o)
            hechos.append((o, d))
        inverso = {v: k for k, v in mapa.items()}
        for ruta in list(archivos_md(raiz)):
            vieja = inverso.get(_norm(ruta), _norm(ruta))
            texto = leer(ruta)
            nuevo = reescribir(texto, vieja, _norm(ruta), mapa)
            if nuevo != texto:
                originales[ruta] = texto
                escribir(ruta, nuevo)
        indice_archivo(raiz)
        nuevos = enlaces_rotos(raiz) - antes
        if nuevos:
            raise RuntimeError(tp("poda_quedarian_enlaces_rotos") % sorted(nuevos)[:3])
    except Exception as e:
        for ruta, texto in originales.items():
            escribir(ruta, texto)
        for o, d in reversed(hechos):
            git(raiz, "mv", d, o)
        return 0, str(e)
    return len(mover), None


def aviso_tamano(raiz, cfg):
    """Líneas de aviso si decisions.log o hechos.md pasan del tope (no recorta nada)."""
    tope = cfg.get("tope_registros_bytes", 61440)
    avisos = []
    for rel in (cfg.get("registro", ".brain/decisions.log"), ".brain/archive/hechos.md"):
        ruta = os.path.join(raiz, rel)
        if os.path.exists(ruta) and os.path.getsize(ruta) > tope:
            avisos.append(tp("poda_pesa_tope_conviene") %
                          (os.path.basename(rel), os.path.getsize(ruta) // 1024, tope // 1024))
    return avisos


def podar_y_resumir(raiz, cfg):
    """Lo que usa arranque.py: poda si procede y devuelve líneas para el resumen."""
    lineas = []
    if cfg.get("poda_activa", True) and not os.environ.get("CEREBRO_SIN_PODA"):  # la variable la usan los tests
        p = plan(raiz)
        if p["mover"] and p["bloqueado"]:
            lineas.append(tp("poda_poda_memoria_pospuesta") %
                          (p["bloqueado"], len(p["mover"])))
        elif p["mover"]:
            n, error = aplicar(raiz, p["mover"])
            if error:
                lineas.append(tp("poda_poda_memoria_aplicada") % error)
            else:
                lineas.append(tp("poda_poda_memoria_archivadas") % n)
                try:
                    cerrar = os.path.join(AQUI, "cerrar.py")
                    subprocess.run([sys.executable, cerrar, "--chat", "poda automática", "--quien", "Guardián",
                                    "Poda de memoria: archivadas %d specs/fichas terminadas (spec 048)" % n],
                                   cwd=raiz, capture_output=True, timeout=15)
                except Exception:
                    pass
    lineas += ["- Aviso: " + a + "." for a in aviso_tamano(raiz, cfg)]
    return lineas


def main():
    with io.open(os.path.join(AQUI, "guardianes.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    p = plan(RAIZ)
    for o, d in p["mover"]:
        print(("MOVERÍA " if "--aplicar" not in sys.argv else "") + "%s -> %s" % (o, d))
    print("Total: %d. %s" % (len(p["mover"]), ("Bloqueado: " + p["bloqueado"]) if p["bloqueado"] else ""))
    if "--aplicar" in sys.argv and p["mover"] and not p["bloqueado"]:
        n, error = aplicar(RAIZ, p["mover"])
        print("Movidos: %d%s" % (n, (" · ERROR: " + error) if error else ""))
    for a in aviso_tamano(RAIZ, cfg):
        print("Aviso:", a)
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.exit(main())
