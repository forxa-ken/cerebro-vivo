#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Medidor de ahorro y efectividad de Cerebro Vivo (spec 001). Solo lectura, solo librería estándar.

Lee los registros de Claude Code (~/.claude/projects/<proyecto>/*.jsonl) y por chat saca:
tokens nuevos, salida, arranque, mensajes tuyos y correcciones (mensajes tuyos que empiezan por «no», «otra vez», «te dije»…).

Uso:
  python medir.py                          # chats de este proyecto
  python medir.py --proyecto RUTA          # otro proyecto
  python medir.py --comparar RUTA_CON RUTA_SIN   # medias de dos proyectos lado a lado, con la diferencia en %
  python medir.py --ultimos 5
  python medir.py --desglose ID            # coste mensaje a mensaje de un chat
  (--comparar solo compara chats con la misma caché: fría con fría, caliente con caliente)
  python medir.py --comparar RUTA_CON RUTA_SIN --tarea [T3]   # solo un tipo de tarea"""

import argparse
import glob
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, AQUI)
from textos import tp  # noqa: E402  (spec 024: mensajes en es/en)


def leer_chat(ruta):
    """Devuelve dict con los totales de un chat, sin contar dos veces el mismo mensaje
    (Claude Code repite la línea mientras la respuesta se va escribiendo)."""
    por_mensaje = {}
    primera_fecha, titulo = None, ""
    with open(ruta, encoding="utf-8", errors="replace") as f:
        for linea in f:
            try:
                e = json.loads(linea)
            except ValueError:
                continue
            if not primera_fecha and e.get("timestamp"):
                primera_fecha = e["timestamp"][:10]
            msg = e.get("message") or {}
            if e.get("type") == "user" and not titulo:
                c = msg.get("content")
                if isinstance(c, list):
                    c = " ".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")
                if isinstance(c, str) and c.strip() and not c.lstrip().startswith("<"):
                    titulo = " ".join(c.split())[:45]
            uso = msg.get("usage")
            if e.get("type") == "assistant" and isinstance(uso, dict):
                por_mensaje[msg.get("id") or e.get("uuid") or len(por_mensaje)] = uso
    nuevos = cache = salida = maximo = 0
    primero = list(por_mensaje.values())[:1]
    arranque = sum((primero[0].get(x, 0) or 0) for x in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")) if primero else 0
    for u in por_mensaje.values():
        ent = u.get("input_tokens", 0) or 0
        esc = u.get("cache_creation_input_tokens", 0) or 0
        lec = u.get("cache_read_input_tokens", 0) or 0
        nuevos += ent + esc
        cache += lec
        salida += u.get("output_tokens", 0) or 0
        maximo = max(maximo, ent + esc + lec)
    return {"id": os.path.basename(ruta)[:8], "fecha": primera_fecha or "?", "mensajes": len(por_mensaje),
            "nuevos": nuevos, "cache": cache, "salida": salida, "maximo": maximo, "arranque": arranque, "titulo": titulo or tp("medir_sin_titulo")}


def k(n):
    return "%dk" % round(n / 1000) if n >= 1000 else str(n)


AVISOS = re.compile(r"<system-reminder>.*?</system-reminder>", re.S)
# Palabras con las que empieza un mensaje tuyo cuando estás corrigiendo o repitiendo algo.
CORRECCION = re.compile(r"^\W*(no[\s,.!]|no$|otra vez|de nuevo|te dije|ya te|repite|sigue sin|sigue fallando|eso no|mal\b|incorrecto)", re.I)


def carpeta_de(ruta):
    slug = re.sub(r"[^A-Za-z0-9]", "-", os.path.abspath(ruta))
    return os.path.join(os.path.expanduser("~"), ".claude", "projects", slug)


def mensajes_usuario(ruta):
    """Textos escritos por la persona (sin resultados de herramientas ni avisos automáticos)."""
    textos = []
    with open(ruta, encoding="utf-8", errors="replace") as f:
        for linea in f:
            try:
                e = json.loads(linea)
            except ValueError:
                continue
            if e.get("type") != "user" or e.get("isMeta"):
                continue
            c = (e.get("message") or {}).get("content")
            if isinstance(c, list):
                c = " ".join(b.get("text", "") for b in c if isinstance(b, dict) and b.get("type") == "text")
            if isinstance(c, str):
                c = AVISOS.sub("", c).strip()  # quita los avisos automáticos que la app pega delante del mensaje
                if c and not c.startswith("<"):
                    textos.append(c)
    return textos


# Pesos de precio relativos a un token de entrada normal (spec 003; revisar si cambian las tarifas; datos de 2026-11).
PESOS = {"entrada": 1.0, "escritura": 1.25, "lectura": 0.1, "salida": 5.0}
FRIO_LECTURA_MAX = 50000  # primer mensaje con menos de esto leído de caché: la caché del prefijo estaba fría


def mensajes_ia(ruta):
    """Por mensaje de la IA (sin contar dos veces el mismo): (entrada, escritura, lectura, salida, herramientas)."""
    por_id = {}
    with open(ruta, encoding="utf-8", errors="replace") as f:
        for linea in f:
            try:
                e = json.loads(linea)
            except ValueError:
                continue
            m = e.get("message") or {}
            if e.get("type") == "assistant" and isinstance(m.get("usage"), dict):
                u = m["usage"]
                tools = [b.get("name", "") for b in (m.get("content") or []) if isinstance(b, dict) and b.get("type") == "tool_use"]
                por_id[m.get("id") or e.get("uuid") or len(por_id)] = (
                    u.get("input_tokens", 0) or 0, u.get("cache_creation_input_tokens", 0) or 0,
                    u.get("cache_read_input_tokens", 0) or 0, u.get("output_tokens", 0) or 0, tools)
    return list(por_id.values())


def coste(ent, esc, lec, sal):
    return ent * PESOS["entrada"] + esc * PESOS["escritura"] + lec * PESOS["lectura"] + sal * PESOS["salida"]


def medir_chat(ruta):
    d = leer_chat(ruta)
    msgs = mensajes_ia(ruta)
    d["coste"] = sum(coste(*m[:4]) for m in msgs)
    d["frio"] = bool(msgs) and msgs[0][2] < FRIO_LECTURA_MAX
    textos = mensajes_usuario(ruta)
    d["encargo"] = " ".join(textos[0].split()) if textos else ""
    d["turnos"] = len(textos)
    d["correcciones"] = sum(1 for t in textos[1:] if CORRECCION.match(t))  # el primero es el encargo, no una corrección
    return d


def chats_de(carpeta, ultimos=0, tarea=""):
    archivos = sorted(glob.glob(os.path.join(carpeta, "*.jsonl")), key=os.path.getmtime)
    chats = [medir_chat(r) for r in (archivos[-ultimos:] if ultimos else archivos)]
    return [c for c in chats if tarea.lower() in c["encargo"].lower()]


def media(chats, clave):
    return sum(c[clave] for c in chats) / len(chats) if chats else 0


CLAVES = (("coste", tp("medir_coste_pond")), ("nuevos", tp("medir_tokens_nuevos")), ("salida", tp("medir_salida")), ("arranque", tp("medir_arranque")), ("mensajes", tp("medir_mensajes")),
          ("turnos", tp("medir_tus_mensajes")), ("correcciones", tp("medir_correcciones")))


def comparar(con, sin, igualar=True):
    if igualar:  # solo frío con frío y caliente con caliente
        for frio in (True, False):
            a, b = [c for c in con if c["frio"] == frio], [c for c in sin if c["frio"] == frio]
            if a and b:
                print(tp("medir_cache_titulo") % (tp("medir_fria") if frio else tp("medir_caliente")))
                comparar(a, b, igualar=False)
            elif a or b:
                print(tp("medir_cache_solo_chats") % (tp("medir_fria") if frio else tp("medir_caliente"), len(a), len(b)))
        return
    print("%-14s %12s %12s %10s" % (tp("medir_media_chat"), tp("medir_arnes"), tp("medir_sin_arnes"), tp("medir_diferencia")))
    for clave, nombre in CLAVES:
        a, b = media(con, clave), media(sin, clave)
        dif = "%+.0f%%" % ((a - b) / b * 100) if b else "-"
        print("%-14s %12.1f %12.1f %10s" % (nombre, a, b, dif))
    print(tp("medir_chats_medidos_arnes") % (len(con), len(sin)))


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=tp("ayuda_medir_descripcion"))
    ap.add_argument("--proyecto", default=RAIZ)
    ap.add_argument("--comparar", nargs=2, metavar=("CON", "SIN"))
    ap.add_argument("--desglose", metavar="ID", help=tp("ayuda_medir_desglose"))
    ap.add_argument("--ultimos", type=int, default=0)
    ap.add_argument("--tarea", default="", help=tp("ayuda_medir_tarea"))
    a = ap.parse_args(argv)
    if a.comparar:
        comparar(chats_de(carpeta_de(a.comparar[0]), a.ultimos, a.tarea), chats_de(carpeta_de(a.comparar[1]), a.ultimos, a.tarea))
        return 0
    if a.desglose:
        carpeta = carpeta_de(a.proyecto)
        rutas = [r for r in glob.glob(os.path.join(carpeta, "*.jsonl")) if os.path.basename(r).startswith(a.desglose)]
        if not rutas:
            print(tp("medir_encontre_chat") % (a.desglose, carpeta))
            return 1
        print("%3s %8s %8s %8s %7s %9s  %s" % ("#", "Escribe", "Lee", "Salida", "Coste", "Acumul.", "Herramientas"))
        total = 0
        for i, (ent, esc, lec, sal, tools) in enumerate(mensajes_ia(rutas[0]), 1):
            c = coste(ent, esc, lec, sal)
            total += c
            print("%3d %8d %8d %8d %7s %9s  %s" % (i, esc, lec, sal, k(c), k(total), ", ".join(tools)))
        return 0
    chats = chats_de(carpeta_de(a.proyecto), a.ultimos, a.tarea)
    if not chats:
        print(tp("medir_encontre_registros") % a.proyecto)
        return 1
    print("%-9s %-11s %5s %8s %8s %8s %8s %6s %6s %-6s %s" % ("Chat", tp("medir_fecha"), "IA", "Coste", "Nuevos", "Salida", tp("medir_arranque2"), tp("medir_tuyos"), tp("medir_corr"), tp("medir_cache"), tp("medir_empieza")))
    for c in chats:
        print("%-9s %-11s %5d %8s %8s %8s %8s %6d %6d %-6s %s" % (c["id"], c["fecha"], c["mensajes"], k(c["coste"]), k(c["nuevos"]), k(c["salida"]),
                                                              k(c["arranque"]), c["turnos"], c["correcciones"], tp("medir_fria2") if c["frio"] else tp("medir_caliente2"), (c["encargo"] or c["titulo"])[:40]))
    print("-" * 100)
    print(tp("medir_chat_media_coste")
          % (k(media(chats, "coste")), k(media(chats, "nuevos")), k(media(chats, "salida")), k(media(chats, "arranque")),
             media(chats, "turnos"), media(chats, "correcciones")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
