#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardián 7 de Cerebro Vivo · análisis AST del código (spec 049).

Lee la estructura del código Python (módulo estándar `ast`) y avisa de tres cosas:
  1. SQL inseguro: execute/executemany/executescript con texto armado (f-string, +, %, .format).
  2. Límites (trinquete): funciones o archivos que crecen respecto a la base guardada; nunca exige refactorizar.
  3. Reglas del proyecto declaradas en guardianes.json (timeout en llamadas de red, auditoría en rutas
     de escritura sensibles, nadie edita/borra una tabla protegida).
Solo avisa: no bloquea nada. Solo lectura, solo librería estándar. Los ajustes viven en guardianes.json;
la base de tamaños en analisis_base.json (se renueva solo con --renovar-base y orden del dueño).
Uso a mano: analisis.py --ver | --renovar-base"""

import ast
import glob
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, AQUI)
from textos import tp  # noqa: E402  (spec 024: mensajes en es/en)
BASE = os.path.join(AQUI, "analisis_base.json")
METODOS_SQL = ("execute", "executemany", "executescript")
METODOS_ESCRITURA = ("POST", "PUT", "DELETE", "PATCH")


def cargar_config():
    with open(os.path.join(AQUI, "guardianes.json"), encoding="utf-8") as f:
        return json.load(f)


def archivos_del_proyecto(raiz, ajustes):
    vistos = []
    for patron in ajustes.get("archivos", ["*.py"]):
        vistos += glob.glob(os.path.join(raiz, patron))
    return sorted(set(vistos))


def _nombre_llamada(n):
    try:
        return ast.unparse(n.func)
    except Exception:
        return ""


def _es_sql_armado(arg):
    if isinstance(arg, (ast.JoinedStr, ast.BinOp)):
        return True
    return isinstance(arg, ast.Call) and getattr(arg.func, "attr", "") == "format"


def _funciones(arbol):
    return [n for n in ast.walk(arbol) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]


def _tamanos(arbol):
    t = {}
    for f in _funciones(arbol):
        t[f.name] = max(t.get(f.name, 0), f.end_lineno - f.lineno + 1)
    return t


def _rutas_de_escritura(f):
    """Devuelve (camino, es_escritura) de cada decorador de ruta Flask de la función."""
    salida = []
    for d in f.decorator_list:
        if not (isinstance(d, ast.Call) and d.args and isinstance(d.args[0], ast.Constant)):
            continue
        atributo = getattr(d.func, "attr", "")
        if atributo not in ("route", "get", "post", "put", "delete", "patch"):
            continue
        escribe = atributo in ("post", "put", "delete", "patch")
        for k in d.keywords:
            if k.arg == "methods":
                escribe = escribe or any(isinstance(c, ast.Constant) and str(c.value).upper() in METODOS_ESCRITURA
                                         for c in ast.walk(k.value))
        salida.append((str(d.args[0].value), escribe))
    return salida


def _avisos_sql(ruta, arbol, texto, ajustes):
    excepciones = ajustes.get("sql_excepciones", [])
    avisos = []
    for n in ast.walk(arbol):
        if isinstance(n, ast.Call) and getattr(n.func, "attr", "") in METODOS_SQL and n.args and _es_sql_armado(n.args[0]):
            fuente = ast.get_source_segment(texto, n.args[0]) or ""
            if any(e["archivo"] == ruta and e["contiene"] in fuente for e in excepciones):
                continue
            avisos.append(tp("analisis_sql_armado_texto")
                          % (ruta, n.lineno, " ".join(fuente.split())[:70]))
    return avisos


def _avisos_reglas(ruta, arbol, texto, ajustes):
    avisos = []
    for r in ajustes.get("reglas", []):
        tipo = r.get("tipo")
        if tipo == "llamada_con_timeout":
            for n in ast.walk(arbol):
                if isinstance(n, ast.Call) and _nombre_llamada(n) in r["llamadas"] \
                        and not any(k.arg == "timeout" for k in n.keywords):
                    avisos.append(tp("analisis_llamada_red_sin") % (ruta, n.lineno, _nombre_llamada(n)))
        elif tipo == "ruta_escritura_audita":
            patron = re.compile(r["patron"])
            if ruta not in r.get("archivos", [ruta]):
                continue
            for f in _funciones(arbol):
                rutas = [c for c, escribe in _rutas_de_escritura(f) if escribe and patron.search(c)]
                if rutas and f.name not in r.get("excepciones", []) and not any(
                        isinstance(c, ast.Call) and _nombre_llamada(c).endswith("audit_event") for c in ast.walk(f)):
                    avisos.append(tp("analisis_ruta_escritura_sin") % (ruta, f.lineno, f.name, rutas[0]))
        elif tipo == "sin_dml_sobre":
            dml = re.compile(r"\b(UPDATE|DELETE\s+FROM|INSERT\s+OR\s+REPLACE\s+INTO)\s+%s\b" % re.escape(r["tabla"]), re.I)
            for n in ast.walk(arbol):
                if isinstance(n, ast.Constant) and isinstance(n.value, str) and dml.search(n.value):
                    avisos.append(tp("analisis_modifica_borra_tabla") % (r["tabla"], ruta, n.lineno))
    return avisos


def _avisos_limites(ruta, arbol, texto, ajustes, base):
    tope = ajustes.get("tope_funcion_nueva", 150)
    margen = ajustes.get("margen_crecimiento", 20)
    margen_arch = ajustes.get("margen_archivo_lineas", 300)
    avisos = []
    previo = base.get(ruta)
    if previo is None:
        return avisos  # archivo nuevo o sin base: no hay con qué comparar
    for nombre, lineas in sorted(_tamanos(arbol).items()):
        antes = previo.get("funciones", {}).get(nombre)
        if lineas > tope and (antes is None or lineas > antes + margen):
            avisos.append(tp("analisis_funcion_mide_lineas") % (
                nombre, ruta, lineas, tp("analisis_nueva_tope") % tope if antes is None else tp("analisis_antes") % antes))
    total = len(texto.splitlines())
    if total > previo.get("lineas", total) + margen_arch:
        avisos.append(tp("analisis_crecio_lineas") % (ruta, previo["lineas"], total))
    return avisos


def cargar_base():
    try:
        with open(BASE, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def foto_actual(raiz, ajustes):
    base = {}
    for ruta in archivos_del_proyecto(raiz, ajustes):
        with open(ruta, encoding="utf-8") as f:
            texto = f.read()
        base[os.path.relpath(ruta, raiz).replace("\\", "/")] = {"lineas": len(texto.splitlines()),
                                                                   "funciones": _tamanos(ast.parse(texto))}
    return base


def analizar(raiz, cfg, base=None):
    """Devuelve la lista de avisos (vacía si todo está en orden). Un archivo ilegible se salta."""
    ajustes = cfg.get("analisis", {})
    base = cargar_base() if base is None else base
    avisos = []
    for ruta_abs in archivos_del_proyecto(raiz, ajustes):
        ruta = os.path.relpath(ruta_abs, raiz).replace("\\", "/")
        try:
            with open(ruta_abs, encoding="utf-8") as f:
                texto = f.read()
            arbol = ast.parse(texto)
        except (OSError, SyntaxError, ValueError):
            continue
        avisos += _avisos_sql(ruta, arbol, texto, ajustes)
        avisos += _avisos_limites(ruta, arbol, texto, ajustes, base)
        avisos += _avisos_reglas(ruta, arbol, texto, ajustes)
    return avisos


def resumen(raiz, cfg):
    """Línea(s) para el resumen de arranque. Calla si está apagado o si algo falla."""
    if not cfg.get("analisis_activo"):
        return []
    try:
        avisos = analizar(raiz, cfg)
    except Exception:
        return []
    if not avisos:
        return [tp("analisis_analisis_codigo_sin")]
    return [tp("analisis_analisis_codigo_aviso") % (len(avisos), avisos[0])]


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:
            pass
    cfg = cargar_config()
    if "--renovar-base" in sys.argv:
        with open(BASE, "w", encoding="utf-8", newline="\n") as f:
            json.dump(foto_actual(RAIZ, cfg.get("analisis", {})), f, ensure_ascii=False, indent=1, sort_keys=True)
        print(tp("analisis_base_tamanos_renovada") % os.path.relpath(BASE, RAIZ))
        return
    avisos = analizar(RAIZ, cfg)
    print("\n".join("- " + a for a in avisos) if avisos else tp("analisis_sin_avisos"))
    print("Total: %d." % len(avisos))


if __name__ == "__main__":
    main()
