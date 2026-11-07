#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardián 12 de Cerebro Vivo · aviso de longitud de chat (spec 056).

Lo llama `cierre.py` (hook Stop de Claude Code) con el registro del chat. Mide el contexto real del último
mensaje de la IA (entrada + caché leída + caché escrita). Si pasa `longitud_aviso_tokens`, devuelve un aviso
para que la IA le diga al dueño que conviene abrir un chat nuevo, con la frase de traspaso lista. Avisa una vez por
tramo de `longitud_repetir_tokens` más; el estado se guarda por chat en `longitud_estado.json` (local).
Solo lectura del registro, solo librería estándar. Si algo falla, calla. Ajustes: guardianes.json."""

import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ESTADO = os.environ.get("CEREBRO_ESTADO_LONGITUD") or os.path.join(AQUI, "longitud_estado.json")  # la variable la usan los tests
MAX_CHATS_EN_ESTADO = 50

TRASPASO = ("Venimos de <este chat>. Qué se hizo: … Qué queda sin subir: … Qué debe probar el dueño: … "
            "Lee el índice y responde; no empieces nada por tu cuenta.")


def cargar_config():
    with open(os.path.join(AQUI, "guardianes.json"), encoding="utf-8") as f:
        return json.load(f)


def ajustes(cfg):
    return {"activo": bool(cfg.get("longitud_activa", True)),
            "aviso": int(cfg.get("longitud_aviso_tokens", 200000)),
            "repetir": int(cfg.get("longitud_repetir_tokens", 100000))}


def contexto_actual(ruta_registro):
    """Tokens de contexto del último mensaje de la IA del registro; 0 si no se puede leer."""
    ultimo = 0
    with open(ruta_registro, encoding="utf-8", errors="replace") as f:
        for linea in f:
            try:
                e = json.loads(linea)
            except ValueError:
                continue
            uso = (e.get("message") or {}).get("usage")
            if e.get("type") == "assistant" and isinstance(uso, dict):
                ultimo = sum((uso.get(k, 0) or 0) for k in ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
    return ultimo


def tramo(contexto, a):
    """0 = por debajo del umbral; 1 = pasó el primer umbral; 2 = +repetir; …"""
    if contexto < a["aviso"]:
        return 0
    return 1 + (contexto - a["aviso"]) // max(a["repetir"], 1)


def texto_aviso(contexto):
    return ("Este chat ya pesa ~%dk tokens de contexto: cada mensaje relee todo y cuesta más. Dile a Darwin, en lenguaje llano, que conviene "
            "abrir un chat nuevo. PRIMERO escribe el archivo .brain/traspaso.md (plantilla en .brain/biblioteca/PLANTILLA_TRASPASO.md: sus últimas palabras literales, decisiones, estado de cada punto, lo que no se ha subido) y luego déjale la frase corta para pegar: «%s». "
            "Si tienes la herramienta start_session (Claude Code de escritorio), abre tú el chat nuevo (contexto fresh, encargo: leer .brain/traspaso.md, ejecutar traspaso-in entro y contarlo en 4-5 viñetas), "
            "llama enseguida a detach_session con su id para que quede al mismo nivel que este chat y no colgado de él, y dile a Darwin cómo se llama el chat nuevo. "
            "Si no puedes abrirlo (no hay herramienta o falla), basta con la frase." % (round(contexto / 1000), TRASPASO))


def leer_estado():
    try:
        with open(ESTADO, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def guardar_estado(estado):
    claves = list(estado)[-MAX_CHATS_EN_ESTADO:]
    with open(ESTADO, "w", encoding="utf-8") as f:
        json.dump({k: estado[k] for k in claves}, f)


def evaluar(contexto, chat, estado, a):
    """(aviso o None, estado nuevo). Función pura, probada en tests."""
    t = tramo(contexto, a)
    if t == 0 or t <= estado.get(chat, 0):
        return None, estado
    nuevo = dict(estado)
    nuevo.pop(chat, None)
    nuevo[chat] = t
    return texto_aviso(contexto), nuevo


def aviso(ruta_registro, cfg):
    """Aviso de longitud para el hook de cierre, o None. Nunca lanza excepciones."""
    try:
        a = ajustes(cfg)
        if not a["activo"] or not ruta_registro:
            return None
        texto, estado = evaluar(contexto_actual(ruta_registro), os.path.basename(ruta_registro), leer_estado(), a)
        if texto:
            guardar_estado(estado)
        return texto
    except Exception:
        return None


def main():
    """A mano: `longitud.py RUTA_DEL_REGISTRO` muestra el contexto actual del chat."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        print("Uso: longitud.py RUTA_DEL_REGISTRO.jsonl")
        return 0
    c = contexto_actual(sys.argv[1])
    a = ajustes(cargar_config())
    print("Contexto actual: ~%dk tokens (aviso en %dk, tramo %d)." % (round(c / 1000), a["aviso"] // 1000, tramo(c, a)))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
