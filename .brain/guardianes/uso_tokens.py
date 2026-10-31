#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardián 3 de Cerebro Vivo · medidor real de tokens.

Lee los registros de conversación que Claude Code guarda en tu PC
(~/.claude/projects/<proyecto>/*.jsonl) y muestra, por chat, cuántos tokens se usaron
de verdad. Solo lectura: no modifica ni envía nada. Solo librería estándar.

Uso:
  python uso_tokens.py                 # todos los chats del proyecto
  python uso_tokens.py --ultimos 5     # los 5 más recientes
  python uso_tokens.py --carpeta RUTA  # otra carpeta de registros

Columnas:
  Nuevos   = tokens que hubo que leer «de cero» (entrada + escritura de caché): lo que más cuesta.
  Caché    = tokens releídos de la caché (baratos, pero crecen con cada mensaje).
  Salida   = lo que escribió la IA.
  Arranque = contexto en la primera respuesta (sistema + CLAUDE.md + lo que se leyó al empezar): mide el coste de arrancar.
  Máx ctx  = el contexto más grande alcanzado en un mensaje: indica cuándo un chat ya es demasiado largo."""

import argparse
import glob
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))


def carpeta_de_registros():
    """Claude Code nombra la carpeta con la ruta del proyecto, cambiando todo lo no alfanumérico por «-»."""
    slug = re.sub(r"[^A-Za-z0-9]", "-", RAIZ)
    return os.path.join(os.path.expanduser("~"), ".claude", "projects", slug)


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
            "nuevos": nuevos, "cache": cache, "salida": salida, "maximo": maximo, "arranque": arranque, "titulo": titulo or "(sin título)"}


def k(n):
    return "%dk" % round(n / 1000) if n >= 1000 else str(n)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # consola de Windows (cp1252) no imprime ⚠ ni tildes
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Uso real de tokens por chat de Claude Code")
    ap.add_argument("--carpeta", default=carpeta_de_registros())
    ap.add_argument("--ultimos", type=int, default=0)
    ap.add_argument("--alerta", type=int, default=0, help="tokens de contexto a partir de los que marcar el chat como largo")
    a = ap.parse_args()
    if not a.alerta:
        try:
            with open(os.path.join(AQUI, "guardianes.json"), encoding="utf-8") as f:
                a.alerta = json.load(f).get("alerta_contexto_tokens", 300000)
        except Exception:
            a.alerta = 300000

    archivos = sorted(glob.glob(os.path.join(a.carpeta, "*.jsonl")), key=os.path.getmtime)
    if not archivos:
        print("No encontré registros en %s\n(Claude Code guarda ahí las conversaciones; ¿otra ruta? usa --carpeta)" % a.carpeta)
        return 1
    if a.ultimos:
        archivos = archivos[-a.ultimos:]
    chats = [leer_chat(r) for r in archivos]

    print("%-9s %-11s %5s %8s %8s %8s %8s %8s  %s" % ("Chat", "Fecha", "Msgs", "Nuevos", "Caché", "Salida", "Arranque", "Máx ctx", "Empieza con…"))
    for c in chats:
        largo = "  ⚠ largo" if c["maximo"] >= a.alerta else ""
        print("%-9s %-11s %5d %8s %8s %8s %8s %8s  %s%s" % (c["id"], c["fecha"], c["mensajes"], k(c["nuevos"]), k(c["cache"]),
                                                             k(c["salida"]), k(c["arranque"]), k(c["maximo"]), c["titulo"], largo))
    print("-" * 110)
    print("%-21s %5d %8s %8s %8s" % ("TOTAL (%d chats)" % len(chats), sum(c["mensajes"] for c in chats),
                                   k(sum(c["nuevos"] for c in chats)), k(sum(c["cache"] for c in chats)),
                                   k(sum(c["salida"] for c in chats))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
