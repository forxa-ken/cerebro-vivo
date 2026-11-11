#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardián 10 de Cerebro Vivo · vigilancia de librerías (spec 052).

Lee `requirements.txt` (Python) y, si existen, `package-lock.json` (npm), `Cargo.lock` (cargo) y `go.mod` (go; spec 036),
mira la versión de cada librería y consulta dos bases públicas y gratuitas:
  1. OSV.dev: vulnerabilidades conocidas de esa versión (ecosistemas PyPI, npm, crates.io y Go).
  2. PyPI: si hay una versión mayor más nueva (p. ej. 2.x → 3.x); solo para Python.
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
sys.path.insert(0, AQUI)
from textos import tp  # noqa: E402  (spec 024: mensajes en es/en)
ESTADO = os.path.join(AQUI, "librerias_estado.json")
OSV_LOTE = "https://api.osv.dev/v1/querybatch"
OSV_VULN = "https://api.osv.dev/v1/vulns/"
PYPI = "https://pypi.org/pypi/%s/json"
MAX_DETALLES = 5
MAX_PAQUETES = 500  # tope de consultas por chequeo (los archivos de bloqueo pueden traer miles)
# Spec 036: ecosistema del guardián → nombre que usa OSV.dev, y archivo de versiones fijadas de cada uno
ECO_OSV = {"pypi": "PyPI", "npm": "npm", "cargo": "crates.io", "go": "Go"}
ARCHIVO_ECO = {"npm": "package-lock.json", "cargo": "Cargo.lock", "go": "go.mod"}


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


def leer_npm(ruta):
    """{nombre: versión} de un package-lock.json (formatos v1, v2 y v3)."""
    with open(ruta, encoding="utf-8") as f:
        datos = json.load(f)
    res = {}
    for clave, info in (datos.get("packages") or {}).items():
        if clave and isinstance(info, dict) and info.get("version") and not info.get("link"):
            res[clave.split("node_modules/")[-1]] = info["version"]
    if not res:  # formato v1
        for nombre, info in (datos.get("dependencies") or {}).items():
            if isinstance(info, dict) and info.get("version"):
                res[nombre] = info["version"]
    return res


def leer_cargo(ruta):
    """{nombre: versión} de un Cargo.lock; se saltan los paquetes locales (sin `source`)."""
    res = {}
    with open(ruta, encoding="utf-8") as f:
        texto = f.read()
    for bloque in texto.split("[[package]]")[1:]:
        n = re.search(r'^name\s*=\s*"([^"]+)"', bloque, re.M)
        v = re.search(r'^version\s*=\s*"([^"]+)"', bloque, re.M)
        if n and v and re.search(r"^source\s*=", bloque, re.M):
            res[n.group(1)] = v.group(1)
    return res


def leer_go(ruta):
    """{módulo: versión} de las líneas `require` de un go.mod (sin la «v» inicial)."""
    res, dentro = {}, False
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            linea = linea.split("//")[0].strip()
            if linea.startswith("require ("):
                dentro = True
                continue
            if dentro and linea == ")":
                dentro = False
                continue
            m = re.match(r"(?:require\s+)?(\S+)\s+v([0-9][^\s]*)$", linea) if (dentro or linea.startswith("require ")) else None
            if m:
                res[m.group(1)] = m.group(2)
    return res


LECTORES = {"npm": leer_npm, "cargo": leer_cargo, "go": leer_go}


def versiones_del_proyecto(raiz, eco, a=None):
    """{nombre: versión} fijadas en el archivo de bloqueo del ecosistema (npm, cargo o go), o {} si no hay o falla."""
    try:
        ruta = os.path.join(raiz, ((a or {}).get("archivos") or {}).get(eco, ARCHIVO_ECO[eco]))
        return LECTORES[eco](ruta) if os.path.isfile(ruta) else {}
    except Exception:
        return {}


def hay_que_vigilar(raiz, a):
    """True si el proyecto tiene algún archivo que vigilar (requirements.txt o un archivo de bloqueo de npm, cargo o go)."""
    if os.path.exists(os.path.join(raiz, a.get("requisitos", "requirements.txt"))):
        return True
    return any(os.path.isfile(os.path.join(raiz, ((a.get("archivos") or {}).get(e, f)))) for e, f in ARCHIVO_ECO.items()
               if e in a.get("ecosistemas", list(ARCHIVO_ECO)))


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
    ruta = os.path.join(raiz, a.get("requisitos", "requirements.txt"))
    pedidos = []
    if os.path.exists(ruta):
        pedidos = [(n, version_instalada(n, m)) for n, m in leer_requisitos(ruta)]
    pedidos = [(n, v) for n, v in pedidos if v]
    for eco in ARCHIVO_ECO:  # spec 036: npm, cargo y go desde su archivo de bloqueo
        if eco in a.get("ecosistemas", list(ARCHIVO_ECO)):
            pedidos += [(n, v, eco) for n, v in sorted(versiones_del_proyecto(raiz, eco, a).items())]
    return consultar(pedidos[:MAX_PAQUETES], a, http)


def consultar(pedidos, a, http=None, con_pypi=True):
    """Consulta OSV (y PyPI si `con_pypi`) para una lista [(nombre, versión)] o [(nombre, versión, ecosistema)]
    (ecosistema: pypi, npm, cargo o go; por defecto pypi). Devuelve el estado o None si no se pudo.
    Spec 027: el guardián de eventos del chat lo usa con `con_pypi=False` para revisar solo lo recién instalado."""
    http = http or http_json
    timeout = a.get("timeout", 7)
    if not pedidos:
        return None
    pedidos = [(p + ("pypi",))[:3] for p in pedidos]
    try:
        osv = http(OSV_LOTE, {"queries": [{"package": {"name": n, "ecosystem": ECO_OSV.get(e, "PyPI")}, "version": v} for n, v, e in pedidos]}, timeout)
        resultados = osv["results"]
        if len(resultados) != len(pedidos):
            return None
    except Exception:
        return None
    paquetes = []
    for (nombre, ver, eco), res in zip(pedidos, resultados):
        vulns = []
        for v in (res.get("vulns") or [])[:MAX_DETALLES]:
            try:
                d = http(OSV_VULN + v["id"], None, timeout)
            except Exception:
                d = {}
            vulns.append({"id": v["id"], "resumen": (d.get("summary") or "")[:100], "corregida": _corregida(d)})
        ultima = ""
        if con_pypi and eco == "pypi":
            try:
                ultima = http(PYPI % nombre, None, timeout)["info"]["version"]
            except Exception:
                pass
        mayor = bool(ultima) and _version(ultima)[0] > _version(ver)[0]
        paquete = {"nombre": nombre, "version": ver, "ultima": ultima, "mayor": mayor, "vulns": vulns}
        if eco != "pypi":
            paquete["eco"] = eco
        paquetes.append(paquete)
    return {"fecha": datetime.date.today().isoformat(), "paquetes": paquetes}


def avisos(estado, a):
    """Textos de aviso del estado guardado, ya sin los fallos ignorados."""
    ignorados = {i.get("id") for i in a.get("ignorar", [])}
    res = []
    for p in estado.get("paquetes", []):
        vulns = [v for v in p.get("vulns", []) if v["id"] not in ignorados]
        if vulns:
            fix = next((v["corregida"] for v in vulns if v.get("corregida")), "")
            res.append(tp("librerias_vulnerabilidad") % (p["nombre"], p["version"], len(vulns), tp("librerias_corregida") % fix if fix else ""))
        elif p.get("mayor") and a.get("avisar_version_mayor", True):
            res.append(tp("librerias_version_mayor") % (p["nombre"], p["version"], p["ultima"]))
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
    if not a["activo"] or not hay_que_vigilar(raiz, a):
        return []  # apagado, o proyecto sin requirements.txt ni archivos de bloqueo de npm, cargo o go: no hay nada que vigilar
    try:
        estado = leer_estado()
        if not estado:
            return [tp("librerias_librerias_sin_chequear") % ("venv\\Scripts\\python.exe .brain\\guardianes\\librerias.py" if os.name == "nt" else "python3 .brain/guardianes/librerias.py")]
        dias = ((hoy or datetime.date.today()) - datetime.date.fromisoformat(estado["fecha"])).days
        av = avisos(estado, a)
        txt = tp("librerias_librerias_chequeo_hace") % (tp("librerias_aviso_detalle_librerias") % (len(av), av[0]) if av else tp("librerias_sin_avisos"), dias)
        if dias >= a.get("dias_aviso", 10):
            txt += tp("librerias_toca_volver_chequear")
        return [txt + "."]
    except Exception:
        return []


def ver(a):
    estado = leer_estado()
    if not estado:
        return tp("librerias_sin_chequeo_guardado")
    ignorados = {i.get("id") for i in a.get("ignorar", [])}
    out = [tp("librerias_ultimo_chequeo") % estado["fecha"]]
    for p in estado["paquetes"]:
        out.append(tp("librerias_ultima") % (p["nombre"], p["version"], p["ultima"] or "?", tp("librerias_version_mayor_disponible") if p.get("mayor") else ""))
        for v in p["vulns"]:
            out.append("    %s%s %s · https://osv.dev/%s%s" % ("(ignorada) " if v["id"] in ignorados else "", v["id"], v["resumen"], v["id"],
                                                               tp("librerias_corregida2") + v["corregida"] if v["corregida"] else ""))
    return "\n".join(out)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    a = ajustes(cargar_config())
    if "--ver" in sys.argv:
        print(ver(a))
        return 0
    if not a["activo"]:
        print(tp("librerias_vigilancia_librerias_apagada"))
        return 0
    nuevo = chequear(RAIZ, a)
    if nuevo is None:
        print(tp("librerias_pudo_chequear_sin"))
        return 0
    with open(ESTADO, "w", encoding="utf-8") as f:
        json.dump(nuevo, f, ensure_ascii=False)
    av = avisos(nuevo, a)
    print(tp("librerias_chequeo_hecho") % ("%d aviso(s)" % len(av) if av else tp("librerias_sin_avisos2")))
    for t in av:
        print("  - " + t)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
