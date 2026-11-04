#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardián 10 de Cerebro Vivo · vigilancia de librerías (spec 052).

Lee `requirements.txt`, mira la versión instalada de cada librería y consulta dos bases públicas y gratuitas:
  1. OSV.dev: vulnerabilidades conocidas de esa versión.
  2. PyPI: si hay una versión mayor más nueva (p. ej. 2.x → 3.x).
Guarda el resultado en `librerias_estado.json`; el resumen de arranque SOLO lee ese archivo (sin red).
Modos: sin argumentos = chequear y guardar (hacerlo cada semana, con el Python del venv) · --ver = detalle.
Solo avisa: nunca actualiza ni instala nada. Solo librería estándar. Si falla la red, calla y conserva el estado
anterior. Ajustes: guardianes.json (`librerias_activo` y bloque `librerias`)."""

import datetime
import json
import os
import re
import sys
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
ESTADO = os.path.join(AQUI, "librerias_estado.json")
OSV_LOTE = "https://api.osv.dev/v1/querybatch"
OSV_VULN = "https://api.osv.dev/v1/vulns/"
PYPI = "https://pypi.org/pypi/%s/json"
MAX_DETALLES = 5


def cargar_config():
    with open(os.path.join(AQUI, "guardianes.json"), encoding="utf-8") as f:
        return json.load(f)


def ajustes(cfg):
    a = dict(cfg.get("librerias", {}))
    a["activo"] = bool(cfg.get("librerias_activo", True))
    return a


def http_json(url, datos=None, timeout=7):
    """GET (o POST si hay datos) que devuelve JSON. Lanza excepción si falla; quien llama decide callar."""
    cuerpo = json.dumps(datos).encode("utf-8") if datos is not None else None
    req = urllib.request.Request(url, data=cuerpo, headers={"Content-Type": "application/json", "User-Agent": "cerebro-vivo-librerias"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def _version(v):
    """Tupla numérica comparable de una versión ('3.0.1' → (3, 0, 1)); ignora sufijos como rc1."""
    return tuple(int(x) for x in re.findall(r"\d+", v.split("+")[0])[:4]) or (0,)


def leer_requisitos(ruta):
    """[(nombre, versión mínima o '')] de un requirements.txt."""
    res = []
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            linea = linea.split("#")[0].strip()
            m = re.match(r"([A-Za-z0-9][A-Za-z0-9._-]*)(?:\[[^\]]*\])?\s*(?:(?:>=|==|~=|>|<=|<|!=)\s*([0-9][^\s,;]*))?", linea)
            if m:
                res.append((re.sub(r"[-_.]+", "-", m.group(1)).lower(), m.group(2) or ""))
    return res


def version_instalada(nombre, minima):
    try:
        from importlib.metadata import version
        return version(nombre)
    except Exception:
        return minima


def _corregida(detalle):
    for af in detalle.get("affected", []):
        for rg in af.get("ranges", []):
            for ev in rg.get("events", []):
                if ev.get("fixed"):
                    return ev["fixed"]
    return ""


def chequear(raiz, a, http=None):
    """Consulta OSV y PyPI. Devuelve el estado nuevo o None si no se pudo (entonces no se toca el anterior)."""
    http = http or http_json
    timeout = a.get("timeout", 7)
    pedidos = [(n, version_instalada(n, m)) for n, m in leer_requisitos(os.path.join(raiz, a.get("requisitos", "requirements.txt")))]
    pedidos = [(n, v) for n, v in pedidos if v]
    if not pedidos:
        return None
    try:
        osv = http(OSV_LOTE, {"queries": [{"package": {"name": n, "ecosystem": "PyPI"}, "version": v} for n, v in pedidos]}, timeout)
        resultados = osv["results"]
        if len(resultados) != len(pedidos):
            return None
    except Exception:
        return None
    paquetes = []
    for (nombre, ver), res in zip(pedidos, resultados):
        vulns = []
        for v in (res.get("vulns") or [])[:MAX_DETALLES]:
            try:
                d = http(OSV_VULN + v["id"], None, timeout)
            except Exception:
                d = {}
            vulns.append({"id": v["id"], "resumen": (d.get("summary") or "")[:100], "corregida": _corregida(d)})
        ultima = ""
        try:
            ultima = http(PYPI % nombre, None, timeout)["info"]["version"]
        except Exception:
            pass
        mayor = bool(ultima) and _version(ultima)[0] > _version(ver)[0]
        paquetes.append({"nombre": nombre, "version": ver, "ultima": ultima, "mayor": mayor, "vulns": vulns})
    return {"fecha": datetime.date.today().isoformat(), "paquetes": paquetes}


def avisos(estado, a):
    """Textos de aviso del estado guardado, ya sin los fallos ignorados."""
    ignorados = {i.get("id") for i in a.get("ignorar", [])}
    res = []
    for p in estado.get("paquetes", []):
        vulns = [v for v in p.get("vulns", []) if v["id"] not in ignorados]
        if vulns:
            fix = next((v["corregida"] for v in vulns if v.get("corregida")), "")
            res.append("%s %s con %d vulnerabilidad(es)%s" % (p["nombre"], p["version"], len(vulns), " (corregida en %s)" % fix if fix else ""))
        elif p.get("mayor") and a.get("avisar_version_mayor", True):
            res.append("%s %s: hay versión mayor (%s)" % (p["nombre"], p["version"], p["ultima"]))
    return res


def leer_estado():
    try:
        with open(ESTADO, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def resumen(raiz, cfg, hoy=None):
    """Línea para el resumen de arranque. Solo lee el estado guardado (sin red). Calla si está apagado o falla."""
    a = ajustes(cfg)
    if not a["activo"] or not os.path.exists(os.path.join(raiz, a.get("requisitos", "requirements.txt"))):
        return []  # apagado, o proyecto sin requirements.txt (p. ej. no es de Python): no hay nada que vigilar
    try:
        estado = leer_estado()
        if not estado:
            return ["- Librerías: sin chequear aún (`%s`)." % ("venv\\Scripts\\python.exe .brain\\guardianes\\librerias.py" if os.name == "nt" else "python3 .brain/guardianes/librerias.py")]
        dias = ((hoy or datetime.date.today()) - datetime.date.fromisoformat(estado["fecha"])).days
        av = avisos(estado, a)
        txt = "- Librerías: %s (chequeo de hace %d días)" % ("%d aviso(s): %s · detalle con `librerias.py --ver`" % (len(av), av[0]) if av else "sin avisos", dias)
        if dias >= a.get("dias_aviso", 10):
            txt += "; toca volver a chequear"
        return [txt + "."]
    except Exception:
        return []


def ver(a):
    estado = leer_estado()
    if not estado:
        return "Sin chequeo guardado todavía."
    ignorados = {i.get("id") for i in a.get("ignorar", [])}
    out = ["Último chequeo: %s" % estado["fecha"]]
    for p in estado["paquetes"]:
        out.append("- %s %s (última: %s)%s" % (p["nombre"], p["version"], p["ultima"] or "?", " · versión mayor disponible" if p.get("mayor") else ""))
        for v in p["vulns"]:
            out.append("    %s%s %s · https://osv.dev/%s%s" % ("(ignorada) " if v["id"] in ignorados else "", v["id"], v["resumen"], v["id"],
                                                               " · corregida en " + v["corregida"] if v["corregida"] else ""))
    return "\n".join(out)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    a = ajustes(cargar_config())
    if "--ver" in sys.argv:
        print(ver(a))
        return 0
    if not a["activo"]:
        print("Vigilancia de librerías apagada (librerias_activo).")
        return 0
    nuevo = chequear(RAIZ, a)
    if nuevo is None:
        print("No se pudo chequear (sin red o respuesta rara); se conserva el estado anterior.")
        return 0
    with open(ESTADO, "w", encoding="utf-8") as f:
        json.dump(nuevo, f, ensure_ascii=False)
    av = avisos(nuevo, a)
    print("Chequeo hecho: %s." % ("%d aviso(s)" % len(av) if av else "sin avisos"))
    for t in av:
        print("  - " + t)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
