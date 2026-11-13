#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardián de Cerebro Vivo · revisión del CONTENIDO de `.brain/` (spec 048).

Avisa, sin bloquear nunca y sin modificar nada, de tres cosas que pudren la memoria del proyecto:
  1. páginas huérfanas  : archivos .md de `.brain/` que ningún otro documento enlaza ni nombra
  2. frases desfasadas  : rutas que ya no existen, «versión actual» distinta de VERSION, cifras («hay N skills») falsas
  3. candidatos a contradicción: el mismo tope (en bytes o KB) de un mismo archivo con valores distintos en documentos distintos
Lo comprobable lo decide este script con reglas, sin IA. Lo que requiere entender el sentido (y la refutación de cada
hallazgo por otra pasada independiente) lo hace la skill `revisar-contenido`. Lo descartado queda en `revision_contenido.json`.

Uso:  python revisar_contenido.py            informe legible
      python revisar_contenido.py --json     informe para la skill
      python revisar_contenido.py --descartar CLAVE --motivo "texto"
      python revisar_contenido.py --marcar-revision
Solo librería estándar. Si algo falla en el resumen de arranque, calla. Ajustes: guardianes.json (`revision_contenido_*`)."""

import datetime
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, AQUI)
from textos import tp  # noqa: E402

ESTADO = "revision_contenido.json"
# Carpetas de .brain/ que son historia o datos de trabajo: no se revisan ni cuentan como huérfanas
SALTAR = ("archive", "notas-chats", "copias_arnes", "pruebas", "diapositivas", "fabrica", "biblioteca/kit-arranque", "biblioteca/kit-traduccion")
# Archivos que nadie enlaza a propósito
SIEMPRE_ENLAZADOS = {"indice.md", "readme.md", "constitution.md", "pendientes.md", "traspaso.md", "traspaso-completo.md", "referencias.md"}
# Carpetas con texto «vivo» donde una frase desfasada importa (el resto es registro histórico)
VIVAS = ("biblioteca", "architecture")
# Donde las rutas citadas describen ESTE proyecto (en biblioteca/ describen archivos que crean los proyectos al usar el método)
RUTAS_PROPIAS = ("architecture",)
PALABRAS_EJEMPLO = re.compile(r"ejemplo|p\. ?ej|e\.g\.|example|si existe|if it exists|opcional|optional|antes se llamaba|antiguo|histórico|"
                              r"historico|se borr|borrad|elimin|se quit|ya no existe|ya no hay|retirad|removed|deleted|no longer", re.I)


def cargar_config():
    with open(os.path.join(AQUI, "guardianes.json"), encoding="utf-8") as f:
        return json.load(f)


def ajustes(cfg):
    return {"activo": bool(cfg.get("revision_contenido_activa", True)),
            "aviso_dias": int(cfg.get("revision_contenido_dias", 30)),
            "ignorar": list(cfg.get("revision_contenido_ignorar", []))}


def _leer(ruta):
    try:
        with open(ruta, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def _md_del_brain(raiz):
    """[ruta relativa con /] de los .md de .brain/ que se revisan."""
    brain = os.path.join(raiz, ".brain")
    salida = []
    for base, carpetas, archivos in os.walk(brain):
        rel_base = os.path.relpath(base, raiz).replace(os.sep, "/")
        carpetas[:] = [c for c in carpetas if not any((rel_base + "/" + c).startswith(".brain/" + s) for s in SALTAR)]
        for n in archivos:
            if n.endswith(".md"):
                salida.append(rel_base + "/" + n)
    return sorted(salida)


def _corpus(raiz, archivos):
    """Texto donde se busca si algo está enlazado: los .md revisados, los índices de IA, las skills y los guardianes."""
    piezas = {}
    for rel in archivos:
        piezas[rel] = _leer(os.path.join(raiz, rel))
    for n in ("CLAUDE.md", "GEMINI.md", "AGENTS.md"):
        if os.path.isfile(os.path.join(raiz, n)):
            piezas[n] = _leer(os.path.join(raiz, n))
    skills = os.path.join(raiz, ".claude", "skills")
    if os.path.isdir(skills):
        for d in sorted(os.listdir(skills)):
            p = os.path.join(skills, d, "SKILL.md")
            if os.path.isfile(p):
                piezas[".claude/skills/%s/SKILL.md" % d] = _leer(p)
    guard = os.path.join(raiz, ".brain", "guardianes")
    if os.path.isdir(guard):
        for n in sorted(os.listdir(guard)):
            if n.endswith((".py", ".json")) and n != ESTADO:  # el archivo de descartes cita las claves: no cuenta como enlace
                piezas[".brain/guardianes/" + n] = _leer(os.path.join(guard, n))
    return piezas


def _ignorado(rel, a):
    import fnmatch
    return any(fnmatch.fnmatch(rel, p) for p in a["ignorar"])


# ---------- 1. huérfanas ----------
def hallazgos_huerfanas(raiz, archivos, piezas, a):
    res = []
    for rel in archivos:
        nombre = os.path.basename(rel)
        if nombre.lower() in SIEMPRE_ENLAZADOS or _ignorado(rel, a):
            continue
        base = nombre[:-6] if nombre.endswith(".en.md") else nombre[:-3]  # la edición en inglés cuenta como la española
        claves = {base + ".md", base + ".en.md", rel}
        m = re.match(r"^(\d{3})-", base)
        extras = [re.compile(r"\b[Ss]pec(?:s)? %s\b" % m.group(1))] if m else []
        m = re.match(r"^(D-\d{3})", base)
        if m:
            claves.add(m.group(1))
        enlazada = False
        for otra, texto in piezas.items():
            if otra == rel or otra == rel.replace(".en.md", ".md") or otra == rel[:-3] + ".en.md":
                continue
            if any(c in texto for c in claves) or any(x.search(texto) for x in extras):
                enlazada = True
                break
        if not enlazada:
            res.append({"tipo": "huerfana", "clave": "huerfana:" + rel, "archivo": rel,
                        "detalle": tp("revisar_contenido_huerfana") % rel})
    return res


# ---------- 2. frases desfasadas ----------
def _version_actual(raiz):
    v = _leer(os.path.join(raiz, "VERSION")).strip()
    return v if re.fullmatch(r"\d+\.\d+\.\d+", v) else ""


def _contar_skills(raiz):
    carpeta = os.path.join(raiz, ".claude", "skills")
    try:
        return sum(1 for d in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, d, "SKILL.md")))
    except OSError:
        return None


def _contar_guardianes(raiz):
    try:
        cfg = os.path.join(raiz, ".brain", "guardianes")
        return sum(1 for n in os.listdir(cfg) if n.endswith(".py"))
    except OSError:
        return None


def hallazgos_desfasadas(raiz, archivos, piezas, a):
    res = []
    version = _version_actual(raiz)
    skills, guardianes = _contar_skills(raiz), _contar_guardianes(raiz)
    for rel in archivos:
        if not any(rel.startswith(".brain/%s/" % v) for v in VIVAS) or _ignorado(rel, a):
            continue
        for n, linea in enumerate(piezas.get(rel, "").splitlines(), 1):
            if PALABRAS_EJEMPLO.search(linea):
                continue
            for ruta in (re.findall(r"`(\.brain/[\w./\-]+)`", linea) if any(rel.startswith(".brain/%s/" % v) for v in RUTAS_PROPIAS) else []):
                if any(x in ruta for x in ("NNN", "AAAA", "*", "<", "{")) or any(("/" + s) in ruta or ruta.endswith(s) for s in SALTAR):
                    continue
                if ruta.endswith("/") or not os.path.splitext(ruta)[1]:
                    continue
                if not os.path.exists(os.path.join(raiz, ruta)):
                    res.append({"tipo": "desfasada", "clave": "ruta:%s:%s" % (rel, ruta), "archivo": rel, "linea": n,
                                "detalle": tp("revisar_contenido_ruta") % (rel, n, ruta)})
            if version:
                for v in re.findall(r"(?:versión actual|version actual|current version)[^\d\n]{0,25}(\d+\.\d+\.\d+)", linea, re.I):
                    if v != version:
                        res.append({"tipo": "desfasada", "clave": "version:%s:%s" % (rel, v), "archivo": rel, "linea": n,
                                    "detalle": tp("revisar_contenido_version") % (rel, n, v, version)})
            for cifra, que in re.findall(r"(?:hay|son|total(?: de)?|there are|have)\s+(\d+)\s+(skills|guardianes|guardians)\b", linea, re.I):
                real = skills if que.lower() == "skills" else guardianes
                if real is not None and int(cifra) != real:
                    res.append({"tipo": "desfasada", "clave": "cifra:%s:%s:%s" % (rel, que.lower(), cifra), "archivo": rel, "linea": n,
                                "detalle": tp("revisar_contenido_cifra") % (rel, n, cifra, que, real)})
    return res


# ---------- 3. candidatos a contradicción ----------
def _a_bytes(numero, unidad):
    try:
        v = float(numero.replace(",", "."))
    except ValueError:
        return None
    return int(v * 1024) if unidad.upper() == "KB" else int(v)


def hallazgos_contradicciones(raiz, archivos, piezas, a):
    """Mismo archivo con «tope» en la línea y valores distintos en documentos distintos."""
    vistos = {}
    for rel in archivos:
        if not any(rel.startswith(".brain/%s/" % v) for v in VIVAS) and rel.count("/") != 1:
            continue  # biblioteca, architecture y los .md sueltos de .brain/
        if _ignorado(rel, a):
            continue
        for n, linea in enumerate(piezas.get(rel, "").splitlines(), 1):
            if not re.search(r"\b(tope|límite|limite|cap|limit)\b", linea, re.I) or PALABRAS_EJEMPLO.search(linea):
                continue
            sujetos = re.findall(r"`([\w.\-/]+\.[a-z]{2,4})`", linea)
            valores = [(_a_bytes(num, u)) for num, u in re.findall(r"\b(\d[\d.,]*)\s*(KB|bytes)\b", linea)]
            valores = [v for v in valores if v]
            if len(sujetos) == 1 and len(valores) == 1:
                vistos.setdefault(sujetos[0], []).append((valores[0], rel, n))
    res = []
    for sujeto, lista in sorted(vistos.items()):
        if len({v for v, _, _ in lista}) > 1 and len({r for _, r, _ in lista}) > 1:
            donde = "; ".join("%s:%d → %d bytes" % (r, n, v) for v, r, n in lista)
            res.append({"tipo": "contradiccion", "clave": "tope:" + sujeto, "archivo": lista[0][1], "linea": lista[0][2],
                        "detalle": tp("revisar_contenido_tope") % (sujeto, donde)})
    return res


# ---------- estado y descartes ----------
def leer_estado(raiz):
    try:
        with open(os.path.join(raiz, ".brain", "guardianes", ESTADO), encoding="utf-8") as f:
            e = json.load(f)
        e.setdefault("descartes", [])
        e.setdefault("ultima_revision", "")
        return e
    except Exception:
        return {"ultima_revision": "", "descartes": []}


def guardar_estado(raiz, estado):
    ruta = os.path.join(raiz, ".brain", "guardianes", ESTADO)
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(estado, ensure_ascii=False, indent=2) + "\n")


def descartar(raiz, clave, motivo, hoy=None):
    estado = leer_estado(raiz)
    if not any(d["clave"] == clave for d in estado["descartes"]):
        estado["descartes"].append({"clave": clave, "motivo": motivo, "fecha": (hoy or datetime.date.today()).isoformat()})
        guardar_estado(raiz, estado)


def marcar_revision(raiz, hoy=None):
    estado = leer_estado(raiz)
    estado["ultima_revision"] = (hoy or datetime.date.today()).isoformat()
    guardar_estado(raiz, estado)


# ---------- informe ----------
def analizar(raiz, cfg):
    a = ajustes(cfg)
    archivos = _md_del_brain(raiz)
    piezas = _corpus(raiz, archivos)
    todos = (hallazgos_huerfanas(raiz, archivos, piezas, a) + hallazgos_desfasadas(raiz, archivos, piezas, a)
             + hallazgos_contradicciones(raiz, archivos, piezas, a))
    estado = leer_estado(raiz)
    descartadas = {d["clave"] for d in estado["descartes"]}
    return {"hallazgos": [h for h in todos if h["clave"] not in descartadas],
            "descartados": sum(1 for h in todos if h["clave"] in descartadas),
            "ultima_revision": estado["ultima_revision"]}


def formatear(informe, cfg):
    L = [tp("revisar_contenido_titulo"), ""]
    if not informe["hallazgos"]:
        L.append(tp("revisar_contenido_sin_hallazgos"))
    nombres = {"huerfana": tp("revisar_contenido_t_huerfana"), "desfasada": tp("revisar_contenido_t_desfasada"),
               "contradiccion": tp("revisar_contenido_t_contradiccion")}
    for tipo in ("huerfana", "desfasada", "contradiccion"):
        lista = [h for h in informe["hallazgos"] if h["tipo"] == tipo]
        if lista:
            L.append("## %s (%d)" % (nombres[tipo], len(lista)))
            L += ["- %s  [%s]" % (h["detalle"], h["clave"]) for h in lista]
            L.append("")
    if informe["descartados"]:
        L.append(tp("revisar_contenido_descartados") % informe["descartados"])
    L.append(tp("revisar_contenido_ultima") % (informe["ultima_revision"] or tp("revisar_contenido_ninguna")))
    return "\n".join(L)


def resumen(raiz, cfg, hoy=None):
    """Una línea para el resumen de arranque, o [] si no hay nada que decir (cuesta 0 tokens)."""
    a, hoy = ajustes(cfg), hoy or datetime.date.today()
    if not a["activo"] or not os.path.isdir(os.path.join(raiz, ".brain")):
        return []
    informe = analizar(raiz, cfg)
    if not informe["hallazgos"]:
        return []
    if informe["ultima_revision"]:
        try:
            if (hoy - datetime.date.fromisoformat(informe["ultima_revision"])).days <= a["aviso_dias"]:
                return []
        except ValueError:
            pass
    return [tp("revisar_contenido_aviso") % len(informe["hallazgos"])]


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    cfg = cargar_config()
    args = sys.argv[1:]
    if "--descartar" in args:
        i = args.index("--descartar")
        motivo = args[args.index("--motivo") + 1] if "--motivo" in args else tp("revisar_contenido_sin_motivo")
        descartar(RAIZ, args[i + 1], motivo)
        print(tp("revisar_contenido_descartado") % args[i + 1])
        return 0
    if "--marcar-revision" in args:
        marcar_revision(RAIZ)
        print(tp("revisar_contenido_revision_anotada"))
        return 0
    informe = analizar(RAIZ, cfg)
    print(json.dumps(informe, ensure_ascii=False, indent=2) if "--json" in args else formatear(informe, cfg))
    return 0


if __name__ == "__main__":
    sys.exit(main())
