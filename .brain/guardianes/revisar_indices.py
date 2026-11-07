#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardián de Cerebro Vivo · revisión de los índices de IA (spec 016).

Revisa CLAUDE.md, GEMINI.md y AGENTS.md (los de `indices_entrada`) y saca un INFORME de lo que parece sobrar o estar
desfasado. NO modifica ningún índice: solo lee. Detecta cinco cosas:
  1. referencias rotas   : rutas o archivos citados que ya no existen (con el posible nuevo sitio si se halla por nombre)
  2. deriva entre índices: secciones que faltan en alguno o que difieren entre CLAUDE/GEMINI/AGENTS
  3. secciones pesadas   : las que pasan de `revision_indices_seccion_bytes`
  4. fechas viejas       : secciones cuya fecha más reciente supera `revision_indices_dias` días
  5. duplicado en .brain : párrafos que ya están en constitution, objetivo, referencias, architecture o decisions
Lo que el dueño ya descartó queda en `revision_indices.json` y no se vuelve a proponer. La verificación de cada hallazgo
(doble pasada: buscar y refutar) la hace la skill `revisar-indices-de-ia`, no este guardián.

Uso:  python revisar_indices.py            informe legible
      python revisar_indices.py --json     informe para la skill
      python revisar_indices.py --descartar CLAVE --motivo "texto"   anota un falso positivo
      python revisar_indices.py --marcar-revision                    anota hoy como fecha de la última revisión
Solo librería estándar. Si algo falla en el resumen de arranque, calla. Ajustes: guardianes.json (`revision_indices_*`)."""

import datetime
import difflib
import fnmatch
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
ESTADO = "revision_indices.json"
MARCA_INI = "<!-- cerebro-vivo:inicio -->"
MARCA_FIN = "<!-- cerebro-vivo:fin -->"
EXTENSIONES = (".py", ".md", ".json", ".js", ".ts", ".tsx", ".html", ".css", ".bat", ".command", ".sh", ".toc", ".lua", ".xml",
               ".txt", ".yml", ".yaml", ".cfg", ".ini", ".toml", ".db", ".sql", ".log", ".csv", ".png", ".jpg", ".svg", ".tga", ".blp")
SALTAR_CARPETAS = {".git", "node_modules", "__pycache__", "venv", ".venv", "archive"}
MAX_ARCHIVOS_BUSQUEDA = 30000
# Referencias que el propio método cita aunque todavía no existan (se crean al usar el método)
IGNORAR_POR_DEFECTO = [".brain/traspaso.md", ".brain/notas-chats*", ".brain/copias_arnes*", "*_estado.json", ".brain/archive*",
                       ".brain/pruebas/P-*", ".brain/specs/NNN*", ".brain/decisions/D-*", ".env"]
PALABRAS_EJEMPLO = re.compile(r"ejemplo|p\. ?ej|e\.g\.|si existe|opcional|por ejemplo|antes se llamaba|antiguo|histórico|historico|se borr|borrad|elimin|se quit|ya no existe|ya no hay|retirad", re.I)


def cargar_config():
    with open(os.path.join(AQUI, "guardianes.json"), encoding="utf-8") as f:
        return json.load(f)


def ajustes(cfg):
    return {"activo": bool(cfg.get("revision_indices_activa", True)),
            "dias": int(cfg.get("revision_indices_dias", 90)),
            "seccion_bytes": int(cfg.get("revision_indices_seccion_bytes", 6000)),
            "aviso_dias": int(cfg.get("revision_indices_aviso_dias", 60)),
            "aviso_porcentaje": int(cfg.get("revision_indices_aviso_porcentaje", 80)),
            "ignorar": list(IGNORAR_POR_DEFECTO) + list(cfg.get("revision_indices_ignorar", []))}


def leer(ruta):
    with open(ruta, encoding="utf-8", errors="replace") as f:
        return f.read()


def sin_bloque_del_kit(texto):
    """El bloque que añade el instalador (spec 015) es del método, no del proyecto: no se revisa."""
    while MARCA_INI in texto and MARCA_FIN in texto:
        a, b = texto.index(MARCA_INI), texto.index(MARCA_FIN) + len(MARCA_FIN)
        texto = texto[:a] + texto[b:]
    return texto


def secciones(texto):
    """[(título, texto)] partiendo por líneas `## `. La cabecera previa va con el título ''."""
    partes, titulo, cuerpo = [], "", []
    for linea in texto.splitlines():
        if linea.startswith("## "):
            partes.append((titulo, "\n".join(cuerpo)))
            titulo, cuerpo = linea[3:].strip(), [linea]
        else:
            cuerpo.append(linea)
    partes.append((titulo, "\n".join(cuerpo)))
    return [(t, c) for t, c in partes if t or c.strip()]


def normalizar(texto):
    return re.sub(r"\s+", " ", texto.replace("`", "").replace("*", "")).strip().lower()


# ---------- 1. referencias rotas ----------
def _candidata(token):
    t = token.strip().lstrip("(\"'").rstrip(".,;:)\"'")
    t = re.sub(r"[#:]\d+(-\d+)?$", "", t)  # archivo.py:42
    t = t.split("#")[0]
    if not t or len(t) > 200 or re.match(r"^[a-z][a-z0-9+.-]*://", t, re.I) or t.startswith(("-", "~", "/", "@")):
        return None
    if re.search(r"[*<>{}$%|=?\s]|\.\.\.", t) or "\\" in t and ":" in t[:3]:
        return None
    if "/" in t and not t.lower().endswith(EXTENSIONES) and not t.endswith("/"):
        return None  # `ENCOUNTER_START/END`, `Promote/Demote`: alternativas, no rutas
    if "/" in t or t.lower().endswith(EXTENSIONES):
        if "/" not in t and not re.search(r"[A-Za-z]", t.rsplit(".", 1)[0]):
            return None
        t = t.replace("\\", "/")
        while t.startswith("./"):
            t = t[2:]
        return t
    return None


def referencias(texto):
    """[(ruta, línea)] de lo que el texto cita entre comillas inversas o en enlaces markdown."""
    res = []
    for n, linea in enumerate(texto.splitlines(), 1):
        for token in re.findall(r"`([^`\n]+)`", linea) + re.findall(r"\]\(([^)\s]+)\)", linea):
            ruta = _candidata(token)
            if ruta:
                res.append((ruta, n))
    return res


def _nombres_del_proyecto(raiz):
    """{nombre_de_archivo: [rutas relativas]} (tope de archivos para no tardar en proyectos enormes)."""
    mapa, contados = {}, 0
    for base, dirs, nombres in os.walk(raiz):
        dirs[:] = [d for d in dirs if d not in SALTAR_CARPETAS]
        for n in nombres:
            contados += 1
            if contados > MAX_ARCHIVOS_BUSQUEDA:
                return mapa
            mapa.setdefault(n.lower(), []).append(os.path.relpath(os.path.join(base, n), raiz).replace("\\", "/"))
    return mapa


def _ignorada(ruta, ignorar):
    return any(fnmatch.fnmatch(ruta, p) or fnmatch.fnmatch(os.path.basename(ruta), p) for p in ignorar)


def hallazgos_referencias(raiz, indice, texto, a):
    pendientes, nombres = [], None
    lineas = texto.splitlines()
    for ruta, n in referencias(texto):
        if _ignorada(ruta, a["ignorar"]) or ruta.startswith("../"):  # fuera del proyecto: no se puede comprobar
            continue
        if os.path.exists(os.path.normpath(os.path.join(raiz, ruta))):
            continue
        pendientes.append((ruta, n))
    res = []
    for ruta, n in dict.fromkeys(pendientes):
        if nombres is None:
            nombres = _nombres_del_proyecto(raiz)
        donde = [r for r in nombres.get(os.path.basename(ruta).lower(), []) if r != ruta][:3]
        contexto = lineas[n - 1] if n <= len(lineas) else ""
        nivel = "dudoso" if PALABRAS_EJEMPLO.search(contexto) or ("/" not in ruta and donde) or ruta.endswith("/") else "roto"  # nombre suelto hallado en otra carpeta: ambiguo
        detalle = "cita `%s` (línea %d) y no existe" % (ruta, n)
        if donde:
            detalle += "; hay un archivo con ese nombre en: %s" % ", ".join(donde)
        res.append({"tipo": "referencia_rota", "indice": indice, "seccion": _seccion_de(texto, n), "detalle": detalle,
                    "clave": "referencia_rota|%s|%s" % (indice, ruta), "nivel": nivel, "posible_nuevo_sitio": donde})
    return res


def _seccion_de(texto, n):
    titulo = ""
    for linea in texto.splitlines()[:n]:
        if linea.startswith("## "):
            titulo = linea[3:].strip()
    return titulo


# ---------- 2. deriva entre índices ----------
def hallazgos_deriva(textos):
    """textos: {indice: texto}. Compara secciones por título entre todos los índices existentes."""
    if len(textos) < 2:
        return []
    mapas = {i: {t: c for t, c in secciones(sin_bloque_del_kit(x)) if t} for i, x in textos.items()}
    titulos = sorted({t for m in mapas.values() for t in m})
    res = []
    for t in titulos:
        tienen = [i for i in mapas if t in mapas[i]]
        faltan = [i for i in mapas if t not in mapas[i]]
        if faltan:
            res.append({"tipo": "deriva", "indice": ", ".join(tienen), "seccion": t,
                        "detalle": "la sección «%s» está en %s y falta en %s" % (t, ", ".join(tienen), ", ".join(faltan)),
                        "clave": "deriva|%s|falta" % t, "nivel": "dudoso"})
            continue
        base = tienen[0]
        for otro in tienen[1:]:
            a, b = normalizar(mapas[base][t]).split(". "), normalizar(mapas[otro][t]).split(". ")
            if difflib.SequenceMatcher(None, a, b, autojunk=False).ratio() < 0.9:
                res.append({"tipo": "deriva", "indice": "%s / %s" % (base, otro), "seccion": t,
                            "detalle": "la sección «%s» difiere entre %s y %s" % (t, base, otro),
                            "clave": "deriva|%s|%s" % (t, otro), "nivel": "dudoso"})
    return res


# ---------- 3. secciones pesadas y 4. fechas viejas ----------
def hallazgos_peso_y_fechas(indice, texto, a, hoy):
    total = max(1, len(texto.encode("utf-8")))
    res = []
    for titulo, cuerpo in secciones(sin_bloque_del_kit(texto)):
        if not titulo:
            continue
        peso = len(cuerpo.encode("utf-8"))
        if peso > a["seccion_bytes"]:
            res.append({"tipo": "seccion_pesada", "indice": indice, "seccion": titulo, "nivel": "dudoso",
                        "detalle": "«%s» pesa %d bytes (%d %% del índice); candidata a una ficha en .brain/architecture/" % (titulo, peso, 100 * peso // total),
                        "clave": "seccion_pesada|%s|%s" % (indice, titulo)})
        fechas = []
        for y, m, d in re.findall(r"\b(20\d\d)-(\d\d)-(\d\d)\b", cuerpo):
            try:
                fechas.append(datetime.date(int(y), int(m), int(d)))
            except ValueError:
                pass
        if fechas and (hoy - max(fechas)).days > a["dias"]:
            res.append({"tipo": "fecha_vieja", "indice": indice, "seccion": titulo, "nivel": "dudoso",
                        "detalle": "«%s»: su fecha más reciente es %s (hace %d días)" % (titulo, max(fechas), (hoy - max(fechas)).days),
                        "clave": "fecha_vieja|%s|%s" % (indice, titulo)})
    return res


# ---------- 5. duplicado en .brain ----------
def _archivos_de_memoria(raiz):
    brain = os.path.join(raiz, ".brain")
    fijos = ["constitution.md", "referencias.md", os.path.join("architecture", "objetivo.md")]
    lista = [os.path.join(brain, f) for f in fijos]
    for carpeta in ("architecture", "decisions"):
        d = os.path.join(brain, carpeta)
        if os.path.isdir(d):
            lista += [os.path.join(d, n) for n in sorted(os.listdir(d)) if n.endswith(".md")]
    return [os.path.relpath(r, raiz).replace("\\", "/") for r in dict.fromkeys(lista) if os.path.isfile(r)]


def hallazgos_duplicados(raiz, indice, texto):
    destinos = {r: normalizar(leer(os.path.join(raiz, r))) for r in _archivos_de_memoria(raiz)}
    res = []
    for titulo, cuerpo in secciones(sin_bloque_del_kit(texto)):
        sin_titulos = "\n".join(l for l in cuerpo.splitlines() if not l.startswith("#"))
        for parrafo in re.split(r"\n\s*\n", sin_titulos):
            p = normalizar(parrafo)
            if len(p) < 200:
                continue
            for r, contenido in destinos.items():
                if p in contenido:
                    res.append({"tipo": "duplicado", "indice": indice, "seccion": titulo or "(cabecera)", "nivel": "dudoso",
                                "detalle": "un párrafo de «%s» ya está en %s (empieza: «%s…»)" % (titulo or "cabecera", r, parrafo.strip()[:50]),
                                "clave": "duplicado|%s|%s|%s" % (indice, titulo, p[:40])})
                    break
    return res


# ---------- estado: descartes y última revisión ----------
def leer_estado(raiz):
    try:
        with open(os.path.join(raiz, ".brain", "guardianes", ESTADO), encoding="utf-8") as f:
            e = json.load(f)
        e.setdefault("descartes", [])
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
def indices_del_proyecto(raiz, cfg):
    nombres = cfg.get("indices_entrada") or [cfg.get("claude_md", "CLAUDE.md")]
    return {n: leer(os.path.join(raiz, n)) for n in nombres if os.path.isfile(os.path.join(raiz, n))}


def analizar(raiz, cfg, hoy=None):
    """{'indices': {nombre: bytes}, 'hallazgos': [...], 'descartados': n, 'ultima_revision': 'AAAA-MM-DD' o ''}."""
    a, hoy = ajustes(cfg), hoy or datetime.date.today()
    textos = indices_del_proyecto(raiz, cfg)
    hallazgos = hallazgos_deriva(textos)
    for nombre, texto in textos.items():
        propio = sin_bloque_del_kit(texto)
        hallazgos += hallazgos_referencias(raiz, nombre, propio, a)
        hallazgos += hallazgos_peso_y_fechas(nombre, texto, a, hoy)
        hallazgos += hallazgos_duplicados(raiz, nombre, texto)
    estado = leer_estado(raiz)
    descartadas = {d["clave"] for d in estado["descartes"]}
    utiles = [h for h in hallazgos if h["clave"] not in descartadas]
    return {"indices": {n: len(t.encode("utf-8")) for n, t in textos.items()}, "hallazgos": utiles,
            "descartados": len(hallazgos) - len(utiles), "ultima_revision": estado.get("ultima_revision", "")}


def formatear(informe, cfg):
    tope = int(cfg.get("tope_claude_md_bytes", 5120))
    lineas = ["Revisión de los índices de IA (solo lectura; no se ha cambiado nada)"]
    for n, b in informe["indices"].items():
        lineas.append("- %s: %d bytes (%d %% del tope de %d)" % (n, b, 100 * b // max(1, tope), tope))
    if not informe["indices"]:
        lineas.append("- No hay índices de IA que revisar.")
    nombres = {"referencia_rota": "Referencias rotas", "deriva": "Deriva entre índices", "seccion_pesada": "Secciones pesadas",
               "fecha_vieja": "Fechas viejas", "duplicado": "Ya está en .brain/"}
    for tipo, titulo in nombres.items():
        grupo = [h for h in informe["hallazgos"] if h["tipo"] == tipo]
        if grupo:
            lineas.append("\n%s (%d)" % (titulo, len(grupo)))
            lineas += ["  [%s] %s\n      clave: %s" % (h["nivel"], h["detalle"], h["clave"]) for h in grupo]
    if not informe["hallazgos"]:
        lineas.append("\nSin hallazgos.")
    if informe["descartados"]:
        lineas.append("\n(%d hallazgo(s) ya descartados antes no se repiten.)" % informe["descartados"])
    lineas.append("Última revisión anotada: %s" % (informe["ultima_revision"] or "ninguna"))
    return "\n".join(lineas)


# ---------- resumen de arranque ----------
def resumen(raiz, cfg, hoy=None):
    """Una línea para el resumen de arranque, o [] si todo está en orden (cuesta 0 tokens)."""
    a, hoy = ajustes(cfg), hoy or datetime.date.today()
    if not a["activo"]:
        return []
    textos = indices_del_proyecto(raiz, cfg)
    if not textos:
        return []
    tope = int(cfg.get("tope_claude_md_bytes", 5120))
    motivos = []
    llenos = [n for n, t in textos.items() if 100 * len(t.encode("utf-8")) // max(1, tope) >= a["aviso_porcentaje"]]
    if llenos:
        motivos.append("%s al %s del tope" % (", ".join(llenos), "/".join("%d %%" % (100 * len(textos[n].encode("utf-8")) // max(1, tope)) for n in llenos)))
    descartadas = {d["clave"] for d in leer_estado(raiz)["descartes"]}
    rotas = 0
    for n, t in textos.items():
        rotas += sum(1 for h in hallazgos_referencias(raiz, n, sin_bloque_del_kit(t), a) if h["nivel"] == "roto" and h["clave"] not in descartadas)
    if rotas:
        motivos.append("%d referencia(s) rota(s)" % rotas)
    ultima = leer_estado(raiz).get("ultima_revision", "")
    if ultima:
        try:
            dias = (hoy - datetime.date.fromisoformat(ultima)).days
            if dias > a["aviso_dias"]:
                motivos.append("sin revisar desde hace %d días" % dias)
        except ValueError:
            pass
    if not motivos:
        return []
    paso = "escribe /adopta (reparte, acorta y trocea) o pide «revisa los índices»" if llenos else "pide «revisa los índices»"
    return ["- Índices de IA: %s; %s (skills adopta y revisar-indices-de-ia)." % (", ".join(motivos), paso)]


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    cfg = cargar_config()
    args = sys.argv[1:]
    if "--descartar" in args:
        i = args.index("--descartar")
        motivo = args[args.index("--motivo") + 1] if "--motivo" in args else "sin motivo anotado"
        descartar(RAIZ, args[i + 1], motivo)
        print("Descartado: %s" % args[i + 1])
        return 0
    if "--marcar-revision" in args:
        marcar_revision(RAIZ)
        print("Revisión anotada con fecha de hoy.")
        return 0
    informe = analizar(RAIZ, cfg)
    print(json.dumps(informe, ensure_ascii=False, indent=2) if "--json" in args else formatear(informe, cfg))
    return 0


if __name__ == "__main__":
    sys.exit(main())
