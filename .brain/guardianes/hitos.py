#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardián de hitos de Cerebro Vivo (spec 026): obliga a apuntar la lección en el momento.

Lo llama `cierre.py` (hook Stop) con el registro del chat. Busca desde la última lección apuntada (o «ninguna») estas señales:
  - un error que se resolvió (una herramienta falló, la IA editó y la misma herramienta funcionó después);
  - cambios en archivos que el proyecto marca como delicados (`lecciones_vigiladas`: tema → patrones);
  - una modificación grande (`hitos_max_archivos` archivos propios editados).
Si hay alguna, devuelve un aviso: no se da la tarea por cerrada hasta lanzar `lecciones.py --tema …` o `lecciones.py ninguna "motivo"`.
También avisa si el traspaso corto (`.brain/traspaso.md`) escrito en esta respuesta pasa de `traspaso_corto_max` caracteres.
Solo lectura del registro, solo librería estándar. Si algo falla, calla. Ajustes: guardianes.json."""

import fnmatch
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, AQUI)
from textos import t  # noqa: E402  (spec 024: mensajes en es/en)

EDITORES = ("Edit", "Write", "NotebookEdit", "MultiEdit")
FALLO = re.compile(r"Traceback|Error|FAILED|\d+ failed|No such file|not found|denied|timed? ?out|Exit code [1-9]|SyntaxError", re.I)


def ajustes(cfg):
    return {"activo": bool(cfg.get("lecciones_activas", True)),
            "vigiladas": cfg.get("lecciones_vigiladas") or {},
            "max_archivos": int(cfg.get("hitos_max_archivos", 5)),
            "errores_min": int(cfg.get("hitos_errores_min", 1)),
            "ignorar": cfg.get("ignorar_cambios", [".brain/*", ".claude/*"]),
            "traspaso_max": int(cfg.get("traspaso_corto_max", 2500))}


def texto_resultado(bloque):
    contenido = bloque.get("content")
    if isinstance(contenido, list):
        contenido = " ".join(str(x.get("text", "")) for x in contenido if isinstance(x, dict))
    return str(contenido or "")


def relativa(ruta, raiz):
    try:
        ruta = os.path.relpath(ruta, raiz)
    except ValueError:
        pass
    return ruta.replace("\\", "/")


def es_marca(nombre, entrada):
    """¿Esta llamada de la IA apunta una lección (o cierra el hito con «ninguna»)?"""
    if nombre in ("Bash", "PowerShell"):  # en Windows la IA suele usar PowerShell (hallado por Modelo #61)
        return "lecciones.py" in str(entrada.get("command", ""))
    if nombre in EDITORES:
        return "/lecciones/" in str(entrada.get("file_path", "")).replace("\\", "/")
    return False


def analizar(ruta_registro, cfg, raiz=RAIZ):
    """(señales pendientes, traspaso corto demasiado largo o None). Función probada en tests."""
    a = ajustes(cfg)
    senales = {"errores": 0, "vigilados": {}, "archivos": set()}
    pendientes = {}  # id de llamada -> nombre de la herramienta, a la espera de su resultado
    fallidas = {}    # nombre de la herramienta -> hubo un fallo sin editar todavía
    arreglando = {}  # nombre de la herramienta -> falló y la IA ya editó después
    traspaso_largo = None
    with open(ruta_registro, encoding="utf-8", errors="replace") as f:
        for linea in f:
            try:
                e = json.loads(linea)
            except ValueError:
                continue
            contenido = (e.get("message") or {}).get("content")
            if not isinstance(contenido, list):
                if e.get("type") == "user" and isinstance(contenido, str):
                    traspaso_largo = None  # mensaje nuevo del usuario: empieza otra respuesta
                continue
            if e.get("type") == "user":
                if any(isinstance(b, dict) and b.get("type") == "text" for b in contenido):
                    traspaso_largo = None
                for b in contenido:
                    if isinstance(b, dict) and b.get("type") == "tool_result":
                        nombre = pendientes.pop(b.get("tool_use_id"), None)
                        if not nombre:
                            continue
                        mal = bool(b.get("is_error")) or bool(FALLO.search(texto_resultado(b)[:2000]))
                        if mal:
                            fallidas[nombre] = True
                            arreglando.pop(nombre, None)
                        elif arreglando.pop(nombre, None):
                            senales["errores"] += 1  # falló, se editó y ahora funciona
            elif e.get("type") == "assistant":
                for b in contenido:
                    if not (isinstance(b, dict) and b.get("type") == "tool_use"):
                        continue
                    nombre, entrada = b.get("name", ""), b.get("input") or {}
                    if es_marca(nombre, entrada):
                        senales = {"errores": 0, "vigilados": {}, "archivos": set()}
                        pendientes, fallidas, arreglando = {}, {}, {}
                        continue
                    pendientes[b.get("id")] = nombre
                    if nombre in EDITORES:
                        for n in list(fallidas):
                            arreglando[n] = True
                        fallidas = {}
                        ruta = relativa(str(entrada.get("file_path", "")), raiz)
                        if ruta.startswith(".."):
                            continue
                        for tema, patrones in a["vigiladas"].items():
                            if any(fnmatch.fnmatch(ruta, p) or fnmatch.fnmatch(os.path.basename(ruta), p) for p in patrones):
                                senales["vigilados"].setdefault(tema, set()).add(ruta)
                        if not any(fnmatch.fnmatch(ruta, p) for p in a["ignorar"]):
                            senales["archivos"].add(ruta)
                        if ruta == ".brain/traspaso.md":
                            texto = str(entrada.get("content", ""))
                            traspaso_largo = len(texto) if len(texto) > a["traspaso_max"] else None
    return senales, traspaso_largo


def avisos(ruta_registro, cfg, raiz=RAIZ):
    """Lista de avisos para el hook de cierre (vacía = nada pendiente). Nunca lanza excepciones."""
    try:
        a = ajustes(cfg)
        if not a["activo"] or not ruta_registro:
            return []
        senales, largo = analizar(ruta_registro, cfg, raiz)
        motivos = []
        if senales["errores"] >= a["errores_min"]:
            motivos.append(t(cfg, "hito_error", senales["errores"]))
        for tema, rutas in sorted(senales["vigilados"].items()):
            motivos.append(t(cfg, "hito_vigilado", tema, ", ".join(sorted(rutas)[:3])))
        if len(senales["archivos"]) >= a["max_archivos"]:
            motivos.append(t(cfg, "hito_grande", len(senales["archivos"])))
        res = []
        if motivos:
            res.append(t(cfg, "hito_aviso", "; ".join(motivos)))
        if largo:
            res.append(t(cfg, "traspaso_largo", largo, a["traspaso_max"]))
        return res
    except Exception:
        return []


def main():
    """A mano: `hitos.py RUTA_DEL_REGISTRO` muestra los hitos pendientes de ese chat."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        with open(os.path.join(AQUI, "guardianes.json"), encoding="utf-8") as f:
            cfg = json.load(f)
    except Exception:
        cfg = {}
    if len(sys.argv) < 2:
        print(t(cfg, "hitos_uso"))
        return 0
    lista = avisos(sys.argv[1], cfg)
    print("\n".join(lista) if lista else t(cfg, "hitos_nada"))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
