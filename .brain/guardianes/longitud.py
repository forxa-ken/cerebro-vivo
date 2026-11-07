#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardián 12 de Cerebro Vivo · aviso de longitud de chat (spec 056).

Lo llama `cierre.py` (hook Stop de Claude Code) con el registro del chat. Mide el contexto real del último
mensaje de la IA (entrada + caché leída + caché escrita). Si pasa `longitud_aviso_tokens`, devuelve un aviso
para que la IA le diga al dueño que conviene abrir un chat nuevo, con la frase de traspaso lista. Avisa una vez por
tramo de `longitud_repetir_tokens` más; el estado se guarda por chat en `longitud_estado.json` (local).
Con `chat_nuevo_auto` (spec 025, por defecto sí) el aviso manda a la IA abrir ella misma el chat nuevo; sin él, solo avisa.
`longitud.py --chat-nuevo si|no|estado` cambia o muestra ese ajuste (skill /chat-nuevo).
Solo lectura del registro, solo librería estándar. Si algo falla, calla. Ajustes: guardianes.json."""

import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ESTADO = os.environ.get("CEREBRO_ESTADO_LONGITUD") or os.path.join(AQUI, "longitud_estado.json")  # la variable la usan los tests
MAX_CHATS_EN_ESTADO = 50
sys.path.insert(0, AQUI)
from textos import t  # noqa: E402  (spec 024: mensajes en es/en)

TRASPASO = t("es", "longitud_frase")


def cargar_config():
    with open(os.path.join(AQUI, "guardianes.json"), encoding="utf-8") as f:
        return json.load(f)


def guardar_config(cfg):
    ruta = os.path.join(AQUI, "guardianes.json")
    temporal = ruta + ".tmp"
    with open(temporal, "w", encoding="utf-8") as f:
        f.write(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n")
    os.replace(temporal, ruta)


def ajustes(cfg):
    return {"activo": bool(cfg.get("longitud_activa", True)),
            "auto": bool(cfg.get("chat_nuevo_auto", True)),
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


def texto_aviso(contexto, lengua=None, auto=True):
    clave = "longitud_aviso" if auto else "longitud_aviso_manual"
    return t(lengua, clave, round(contexto / 1000), t(lengua, "longitud_frase"))


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


def evaluar(contexto, chat, estado, a, lengua=None):
    """(aviso o None, estado nuevo). Función pura, probada en tests."""
    paso = tramo(contexto, a)
    if paso == 0 or paso <= estado.get(chat, 0):
        return None, estado
    nuevo = dict(estado)
    nuevo.pop(chat, None)
    nuevo[chat] = paso
    return texto_aviso(contexto, lengua, a.get("auto", True)), nuevo


def aviso(ruta_registro, cfg):
    """Aviso de longitud para el hook de cierre, o None. Nunca lanza excepciones."""
    try:
        a = ajustes(cfg)
        if not a["activo"] or not ruta_registro:
            return None
        texto, estado = evaluar(contexto_actual(ruta_registro), os.path.basename(ruta_registro), leer_estado(), a, cfg)
        if texto:
            guardar_estado(estado)
        return texto
    except Exception:
        return None


def chat_nuevo(cfg, orden):
    """Spec 025: `si`/`no` cambia `chat_nuevo_auto`; `estado` (o nada) solo lo muestra. Devuelve el texto para el dueño."""
    orden = (orden or "estado").strip().lower()
    if orden in ("si", "sí", "on", "yes", "activar", "activa"):
        cfg["chat_nuevo_auto"] = True
        guardar_config(cfg)
    elif orden in ("no", "off", "desactivar", "desactiva"):
        cfg["chat_nuevo_auto"] = False
        guardar_config(cfg)
    elif orden != "estado":
        return t(cfg, "longitud_chat_uso")
    return t(cfg, "longitud_chat_si" if ajustes(cfg)["auto"] else "longitud_chat_no")


def main():
    """A mano: `longitud.py RUTA_DEL_REGISTRO` muestra el contexto actual del chat; `--chat-nuevo si|no|estado`, el ajuste."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        cfg = cargar_config()
    except Exception:
        cfg = {}
    if len(sys.argv) >= 2 and sys.argv[1] == "--chat-nuevo":
        print(chat_nuevo(cfg, sys.argv[2] if len(sys.argv) > 2 else "estado"))
        return 0
    if len(sys.argv) < 2:
        print(t(cfg, "longitud_uso"))
        return 0
    c = contexto_actual(sys.argv[1])
    a = ajustes(cfg)
    print(t(cfg, "longitud_actual", round(c / 1000), a["aviso"] // 1000, tramo(c, a)))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
