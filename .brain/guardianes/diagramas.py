#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Diagramas dentro de las diapositivas (spec 046, fase 1): un subconjunto de Mermaid dibujado como SVG. Solo librería estándar.

  from diagramas import pintar
  svg = pintar("flowchart LR\\n  A[Idea] --> B[Spec]")      # devuelve el SVG o lanza ValueError(código)

Tipos de la fase 1: `flowchart`/`graph` (LR, RL, TB, TD, BT; formas [] () {} (()) ([]); flechas --> --- -.-> ==>; etiquetas |texto|)
y `sequenceDiagram` (participant/actor, ->> -->> -> -->, Note, autonumber). Todo lo demás lanza ValueError con un código:
«tipo» (no soportado), «sintaxis» (línea que no se entiende) o «limite» (demasiado grande). El texto se escapa siempre."""
import html
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from textos import t  # noqa: E402

MAX_NODOS, MAX_PARTICIPANTES, MAX_MENSAJES = 15, 7, 24
ANCHO_CHAR, ALTO_LINEA = 8.6, 19


def _lineas_texto(txt, ancho=18):
    """Texto en líneas de unos `ancho` caracteres (salto manual con <br/>)."""
    out = []
    for parte in re.split(r"<br\s*/?>", txt):
        actual = ""
        for palabra in parte.split():
            if actual and len(actual) + 1 + len(palabra) > ancho:
                out.append(actual)
                actual = palabra
            else:
                actual = (actual + " " + palabra).strip()
        out.append(actual)
    return out or [""]


def _texto(x, y, lineas, clase="dg-t", ancla="middle"):
    y0 = y - (len(lineas) - 1) * ALTO_LINEA / 2
    t = "".join('<tspan x="%.1f" y="%.1f">%s</tspan>' % (x, y0 + k * ALTO_LINEA + 5, html.escape(l)) for k, l in enumerate(lineas))
    return '<text class="%s" text-anchor="%s">%s</text>' % (clase, ancla, t)


def _limpio(txt):
    txt = txt.strip()
    if len(txt) >= 2 and txt[0] == txt[-1] == '"':
        txt = txt[1:-1]
    return txt


_CONTADOR = [0]


def _svg(ancho, alto, cuerpo):
    # Un id de marcador distinto por dibujo: con ids repetidos el navegador usa el del primero, que puede estar en una diapositiva oculta.
    _CONTADOR[0] += 1
    mid = "dg-f%d" % _CONTADOR[0]
    marcador = ('<defs><marker id="%s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
                '<path d="M0,0 L10,5 L0,10 z" fill="currentColor"/></marker></defs>' % mid)
    # max-width: un dibujo ancho (secuencia) no se agranda hasta tener un texto mucho mayor que el de uno alto (cajas).
    return ('<svg class="dg" viewBox="0 0 %.0f %.0f" style="max-width:%.0fpx" xmlns="http://www.w3.org/2000/svg" role="img">%s%s</svg>'
            % (ancho, alto, ancho * 1.2, marcador, cuerpo.replace("url(#dg-f)", "url(#%s)" % mid)))


# ---------------------------------------------------------------- flowchart
NODO = re.compile(r'\s*([A-Za-z_][\w-]*)(?:(\(\()(.*?)\)\)|(\(\[)(.*?)\]\)|(\[)(.*?)\]|(\()(.*?)\)|(\{)(.*?)\})?')
FLECHA = re.compile(r'\s*(-->|---|-\.->|-\.-|==>|===|--\s+[^->|]+?\s+-->)\s*(?:\|([^|]*)\|)?')
FORMAS = {"((": "circulo", "([": "pastilla", "[": "caja", "(": "redonda", "{": "rombo"}


def _leer_flujo(lineas):
    nodos, orden, aristas = {}, [], []

    def nodo(m):
        ident = m.group(1)
        for g in range(2, 12, 2):
            if m.group(g):
                forma, texto = FORMAS[m.group(g)], _limpio(m.group(g + 1))
                break
        else:
            forma, texto = None, None
        if ident not in nodos:
            nodos[ident] = {"id": ident, "texto": texto if texto is not None else ident, "forma": forma or "caja"}
            orden.append(ident)
        elif forma:
            nodos[ident].update(texto=texto, forma=forma)
        return ident

    for linea in lineas:
        pos, anterior, pendiente = 0, None, None
        while True:
            m = NODO.match(linea, pos)
            if not m:
                raise ValueError("sintaxis")
            actual = nodo(m)
            if anterior is not None:
                aristas.append({"a": anterior, "b": actual, **pendiente})
            pos = m.end()
            f = FLECHA.match(linea, pos)
            if not f:
                break
            raw = f.group(1)
            etiqueta = (f.group(2) or "").strip()
            if raw.startswith("-- "):
                etiqueta, raw = raw[2:-3].strip(), "-->"
            pendiente = {"estilo": {"-->": "n", "---": "s", "-.->": "p", "-.-": "ps", "==>": "g", "===": "gs"}[raw], "etiqueta": etiqueta}
            anterior, pos = actual, f.end()
        if linea[pos:].strip():
            raise ValueError("sintaxis")
    return nodos, orden, aristas


def _capas(orden, aristas):
    """Capa de cada nodo (camino más largo ignorando las flechas que vuelven atrás) y qué flechas vuelven."""
    sal = {n: [] for n in orden}
    for k, e in enumerate(aristas):
        sal[e["a"]].append((e["b"], k))
    estado, atras = {}, set()

    def dfs(n):
        estado[n] = 1
        for b, k in sal[n]:
            if estado.get(b) == 1:
                atras.add(k)
            elif b not in estado:
                dfs(b)
        estado[n] = 2

    entran = {e["b"] for k, e in enumerate(aristas)}
    for n in [x for x in orden if x not in entran] + list(orden):
        if n not in estado:
            dfs(n)
    capa = {n: 0 for n in orden}
    for _ in range(len(orden)):
        for k, e in enumerate(aristas):
            if k not in atras and capa[e["b"]] < capa[e["a"]] + 1:
                capa[e["b"]] = capa[e["a"]] + 1
    return capa, atras


def _tamano(n):
    lin = _lineas_texto(n["texto"])
    w = max(len(l) for l in lin) * ANCHO_CHAR + 30
    h = len(lin) * ALTO_LINEA + 20
    if n["forma"] == "rombo":
        w, h = w * 1.5, h * 1.6
    elif n["forma"] == "circulo":
        w = h = max(w, h) * 1.1
    n.update(w=max(w, 76), h=max(h, 42), lin=lin)


def _recorte(n, dx, dy):
    """Factor t tal que centro + t*(dx,dy) cae en el borde del nodo."""
    a, b = n["w"] / 2, n["h"] / 2
    if n["forma"] == "rombo":
        return 1 / ((abs(dx) / a) + (abs(dy) / b) or 1)
    if n["forma"] == "circulo":
        return 1 / (math.hypot(dx / a, dy / b) or 1)
    return 1 / (max(abs(dx) / a, abs(dy) / b) or 1)


def _forma(n):
    x, y, w, h = n["x"] - n["w"] / 2, n["y"] - n["h"] / 2, n["w"], n["h"]
    if n["forma"] == "rombo":
        p = "%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" % (n["x"], y, x + w, n["y"], n["x"], y + h, x, n["y"])
        return '<polygon class="dg-c" points="%s"/>' % p
    if n["forma"] == "circulo":
        return '<ellipse class="dg-c" cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f"/>' % (n["x"], n["y"], w / 2, h / 2)
    rx = {"caja": 4, "redonda": 12, "pastilla": h / 2}[n["forma"]]
    return '<rect class="dg-c" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f"/>' % (x, y, w, h, rx)


def _posicionar(nodos, orden, capa, vertical, inverso, holgura):
    capas = {}
    for n in orden:
        capas.setdefault(capa[n], []).append(n)
    sep_cap, sep_nodo = 80, 30
    principal, y_capa = 0, {}
    for c in sorted(capas):
        m = max((nodos[n]["h"] if vertical else nodos[n]["w"]) for n in capas[c])
        y_capa[c] = principal + m / 2
        principal += m + max(sep_cap, holgura.get(c, 0))
    cruz = {c: sum((nodos[n]["w"] if vertical else nodos[n]["h"]) + sep_nodo for n in capas[c]) - sep_nodo for c in capas}
    ancho_max = max(cruz.values())
    for c, ns in capas.items():
        pos = (ancho_max - cruz[c]) / 2
        for n in ns:
            nd = nodos[n]
            tam = nd["w"] if vertical else nd["h"]
            centro_cruz, centro_pri = pos + tam / 2, y_capa[c]
            pos += tam + sep_nodo
            if inverso:
                centro_pri = (principal - sep_cap) - centro_pri
            nd["x"], nd["y"] = (centro_cruz, centro_pri) if vertical else (centro_pri, centro_cruz)
    return (ancho_max, principal - sep_cap) if vertical else (principal - sep_cap, ancho_max)


def _dibujar_flecha(e, nodos, atras_k, k):
    a, b = nodos[e["a"]], nodos[e["b"]]
    clase = "dg-l" + (" dg-p" if "p" in e["estilo"] else "") + (" dg-g" if "g" in e["estilo"] else "")
    punta = "" if e["estilo"].endswith("s") else ' marker-end="url(#dg-f)"'
    if a is b:
        x, y = a["x"] + a["w"] / 2, a["y"] - a["h"] / 4
        cuerpo = '<path class="%s" fill="none" d="M%.1f,%.1f C%.1f,%.1f %.1f,%.1f %.1f,%.1f"%s/>' % (
            clase, x, y, x + 55, y - 30, x + 55, y + 40, x, y + a["h"] / 2, punta)
        return cuerpo, (x + 55, a["y"])
    dx, dy = b["x"] - a["x"], b["y"] - a["y"]
    ctrl = None
    if k in atras_k:  # la flecha que vuelve se curva para no pisar a la de ida
        largo = math.hypot(dx, dy) or 1
        ctrl = ((a["x"] + b["x"]) / 2 - dy / largo * 70, (a["y"] + b["y"]) / 2 + dx / largo * 70)
        dx, dy = ctrl[0] - a["x"], ctrl[1] - a["y"]
    ta = _recorte(a, dx, dy)
    p0 = (a["x"] + dx * ta, a["y"] + dy * ta)
    ex, ey = (b["x"] - ctrl[0], b["y"] - ctrl[1]) if ctrl else (-(b["x"] - a["x"]), -(b["y"] - a["y"]))
    tb = _recorte(b, ex, ey)
    p1 = (b["x"] + ex * tb, b["y"] + ey * tb)
    if ctrl:
        d = "M%.1f,%.1f Q%.1f,%.1f %.1f,%.1f" % (p0[0], p0[1], ctrl[0], ctrl[1], p1[0], p1[1])
        medio = (0.25 * p0[0] + 0.5 * ctrl[0] + 0.25 * p1[0], 0.25 * p0[1] + 0.5 * ctrl[1] + 0.25 * p1[1])
    else:
        d = "M%.1f,%.1f L%.1f,%.1f" % (p0[0], p0[1], p1[0], p1[1])
        medio = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
    return '<path class="%s" fill="none" d="%s"%s/>' % (clase, d, punta), medio


def _flujo(lineas, cab):
    direccion = cab[1] if len(cab) > 1 else "TB"
    vertical, inverso = direccion in ("TB", "TD", "BT"), direccion in ("RL", "BT")
    nodos, orden, aristas = _leer_flujo(lineas)
    if not nodos:
        raise ValueError("sintaxis")
    if len(nodos) > MAX_NODOS:
        raise ValueError("limite")
    for n in nodos.values():
        _tamano(n)
    capa, atras = _capas(orden, aristas)
    holgura = {}
    if not vertical:  # entre capas tiene que caber la etiqueta más larga de las flechas que salen de la capa
        for e in aristas:
            if e["etiqueta"] and capa[e["b"]] > capa[e["a"]]:
                holgura[capa[e["a"]]] = max(holgura.get(capa[e["a"]], 0), len(e["etiqueta"]) * ANCHO_CHAR + 40)
    ancho, alto = _posicionar(nodos, orden, capa, vertical, inverso, holgura)
    margen = 70
    for n in nodos.values():
        n["x"] += margen / 2
        n["y"] += margen / 2
    partes, etiquetas = [], []
    for k, e in enumerate(aristas):
        trazo, medio = _dibujar_flecha(e, nodos, atras, k)
        partes.append(trazo)
        if e["etiqueta"]:
            etiquetas.append(_texto(medio[0], medio[1] - 12, _lineas_texto(e["etiqueta"], 22), "dg-t dg-e"))
    for n in nodos.values():
        partes.append(_forma(n) + _texto(n["x"], n["y"], n["lin"]))
    return _svg(ancho + margen + 60, alto + margen, "".join(partes + etiquetas))


# ---------------------------------------------------------------- sequenceDiagram
MENSAJE = re.compile(r"^\s*(\S+?)\s*(-->>|->>|-->|->)\s*(\S+?)\s*:\s*(.*)$")
PARTICIPANTE = re.compile(r"^\s*(?:participant|actor)\s+(\S+)(?:\s+as\s+(.+))?$")
NOTA = re.compile(r"^\s*Note\s+(over|right of|left of)\s+([^:]+?)\s*:\s*(.*)$", re.I)
NO_SOPORTADO = re.compile(r"^\s*(loop|alt|opt|par|rect|critical|break|else|and|end|activate|deactivate|box|create|destroy)\b", re.I)


def _leer_secuencia(lineas):
    nombres, partes, pasos, numerar = {}, [], [], False

    def parte(i, nombre=None):
        if i not in nombres:
            nombres[i] = {"id": i, "texto": _limpio(nombre) if nombre else i}
            partes.append(i)
        elif nombre:
            nombres[i]["texto"] = _limpio(nombre)

    for l in lineas:
        if l.strip().lower() == "autonumber":
            numerar = True
        elif NO_SOPORTADO.match(l):
            raise ValueError("tipo")
        elif PARTICIPANTE.match(l):
            m = PARTICIPANTE.match(l)
            parte(m.group(1), m.group(2))
        elif NOTA.match(l):
            m = NOTA.match(l)
            ids = [x.strip() for x in m.group(2).split(",")]
            for i in ids:
                parte(i)
            pasos.append({"nota": m.group(1).lower(), "ids": ids, "texto": _limpio(m.group(3))})
        elif MENSAJE.match(l):
            m = MENSAJE.match(l)
            parte(m.group(1))
            parte(m.group(3))
            pasos.append({"a": m.group(1), "b": m.group(3), "punteada": m.group(2).startswith("--"), "abierta": m.group(2).endswith("->") and not m.group(2).endswith(">>"),
                          "texto": _limpio(m.group(4))})
        else:
            raise ValueError("sintaxis")
    return nombres, partes, pasos, numerar


def _secuencia(lineas):
    nombres, partes, pasos, numerar = _leer_secuencia(lineas)
    if not partes or not pasos:
        raise ValueError("sintaxis")
    if len(partes) > MAX_PARTICIPANTES or len(pasos) > MAX_MENSAJES:
        raise ValueError("limite")
    col = {p: k for k, p in enumerate(partes)}
    caja = {p: max(len(nombres[p]["texto"]) * ANCHO_CHAR + 28, 90) for p in partes}
    sep = [max(170.0, (caja[partes[k]] + caja[partes[k + 1]]) / 2 + 30) for k in range(len(partes) - 1)]
    for s in pasos:
        if "a" in s and abs(col[s["a"]] - col[s["b"]]) == 1:
            k = min(col[s["a"]], col[s["b"]])
            sep[k] = max(sep[k], len(s["texto"]) * ANCHO_CHAR + 50)
    xs, x = [], 40 + caja[partes[0]] / 2
    for k, p in enumerate(partes):
        xs.append(x)
        x += sep[k] if k < len(sep) else 0
    x_de = dict(zip(partes, xs))
    y, num, cuerpo, derecha = 60.0, 0, [], 0.0
    for s in pasos:
        if "nota" in s:
            lin = _lineas_texto(s["texto"], 28)
            w = max(len(l) for l in lin) * ANCHO_CHAR + 24
            h = len(lin) * ALTO_LINEA + 14
            cx = (x_de[s["ids"][0]] + x_de[s["ids"][-1]]) / 2
            if s["nota"] == "right of":
                cx = x_de[s["ids"][0]] + w / 2 + 12
            elif s["nota"] == "left of":
                cx = x_de[s["ids"][0]] - w / 2 - 12
            if s["nota"] == "over" and len(s["ids"]) > 1:
                w = max(w, abs(x_de[s["ids"][-1]] - x_de[s["ids"][0]]) + 30)
            y += h / 2 + 12
            cuerpo.append('<rect class="dg-n" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3"/>' % (cx - w / 2, y - h / 2, w, h) + _texto(cx, y, lin))
            y += h / 2 + 8
            continue
        num += 1
        etiqueta = ("%d. " % num if numerar else "") + s["texto"]
        lin = _lineas_texto(etiqueta, 34)
        y += len(lin) * ALTO_LINEA + 18
        clase = "dg-l" + (" dg-p" if s["punteada"] else "")
        punta = "" if s["abierta"] else ' marker-end="url(#dg-f)"'
        xa, xb = x_de[s["a"]], x_de[s["b"]]
        if s["a"] == s["b"]:
            cuerpo.append('<path class="%s" fill="none" d="M%.1f,%.1f h45 v26 h-45"%s/>' % (clase, xa, y - 10, punta))
            cuerpo.append(_texto(xa + 50, y - 3, lin, "dg-t dg-e", "start"))
            derecha = max(derecha, xa + 56 + max(len(l) for l in lin) * ANCHO_CHAR)
            y += 22
        else:
            cuerpo.append('<path class="%s" fill="none" d="M%.1f,%.1f L%.1f,%.1f"%s/>' % (clase, xa, y, xb, y, punta))
            cuerpo.append(_texto((xa + xb) / 2, y - 8 - (len(lin) - 1) * ALTO_LINEA / 2 - 6, lin, "dg-t dg-e"))
    y += 30
    cabeza = "".join('<line class="dg-v" x1="%.1f" y1="38" x2="%.1f" y2="%.1f"/>' % (x_de[p], x_de[p], y - 12) for p in partes)
    for p in partes:
        for yy in (14, y - 12):
            cabeza += '<rect class="dg-c" x="%.1f" y="%.1f" width="%.1f" height="30" rx="4"/>' % (x_de[p] - caja[p] / 2, yy, caja[p])
            cabeza += _texto(x_de[p], yy + 15, [nombres[p]["texto"]])
    return _svg(max(xs[-1] + caja[partes[-1]] / 2 + 40, derecha + 20), y + 24, cabeza + "".join(cuerpo))


# ---------------------------------------------------------------- entrada
def aviso(lang, codigo):
    """Frase (en el idioma del proyecto) de por qué un diagrama no se pudo dibujar."""
    return {"tipo": t(lang, "diap_diagrama_tipo"), "sintaxis": t(lang, "diap_diagrama_sintaxis"),
            "limite": t(lang, "diap_diagrama_limite")}[codigo]


def pintar(codigo):
    """SVG del diagrama Mermaid `codigo`, o ValueError('tipo'|'sintaxis'|'limite')."""
    lineas = [l for l in (x.rstrip() for x in codigo.replace("\r\n", "\n").split("\n")) if l.strip() and not l.strip().startswith("%%")]
    if not lineas:
        raise ValueError("sintaxis")
    cab = lineas[0].split()
    tipo = cab[0] if cab else ""
    cuerpo = [l.strip().rstrip(";") for l in lineas[1:]]
    if tipo in ("flowchart", "graph"):
        if any(re.match(r"^(subgraph|end|style|classDef|class|linkStyle|click|direction)\b", l) for l in cuerpo):
            raise ValueError("tipo")
        if len(cab) > 1 and cab[1] not in ("LR", "RL", "TB", "TD", "BT"):
            raise ValueError("sintaxis")
        return _flujo(cuerpo, cab)
    if tipo == "sequenceDiagram":
        return _secuencia(cuerpo)
    raise ValueError("tipo")


CSS = """
.dg{display:block;margin:.4em auto;width:100%;max-height:62vh;color:var(--acento)}
.dg-c{fill:var(--caja);stroke:var(--acento);stroke-width:1.6}.dg-n{fill:var(--caja);stroke:var(--suave);stroke-width:1}
.dg-l{stroke:var(--acento);stroke-width:1.7}.dg-g{stroke-width:3.4}.dg-p{stroke-dasharray:6 5}
.dg-v{stroke:var(--suave);stroke-width:1;stroke-dasharray:5 5}
.dg-t{fill:var(--texto);font-size:15px;font-family:inherit}
.dg-e{paint-order:stroke;stroke:var(--fondo);stroke-width:5px;stroke-linejoin:round;fill:var(--suave)}
"""
