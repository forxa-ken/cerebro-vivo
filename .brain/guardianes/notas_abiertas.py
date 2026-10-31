#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardián 13 de Cerebro Vivo · aviso de notas de chats auxiliares en un chat ya abierto (spec 081).

Se ejecuta como hook `UserPromptSubmit` de Claude Code: cuando Darwin envía un mensaje, si hay
notas nuevas en `.brain/notas-chats/` que ESTE chat aún no ha recibido, las imprime (Claude las
lee como contexto). No mueve ni borra nada (el archivado es del arranque, spec 080).
Sin notas nuevas no imprime nada; ante cualquier fallo calla. Solo librería estándar.

Spec 082: también lo lanza el hook `PreInvocation` de Antigravity (`.agents/hooks.json`): entrada con `conversationId`,
solo actúa en `invocationNum == 1` y responde un JSON con `injectSteps` (formato según Gemini, sin comprobar en vivo)."""

import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
CARPETA = os.path.join(".brain", "notas-chats")
ESTADO = ".avisadas.json"
MAX_NOTAS = 3
MAX_CARACTERES = 600


def _leer_estado(carpeta):
    try:
        with open(os.path.join(carpeta, ESTADO), encoding="utf-8") as f:
            datos = json.load(f)
        return datos if isinstance(datos, dict) else {}
    except Exception:
        return {}


def avisar(raiz, sesion):
    """Líneas de aviso con las notas que `sesion` aún no ha recibido; las marca como avisadas."""
    carpeta = os.path.join(raiz, CARPETA)
    try:
        nombres = sorted(n for n in os.listdir(carpeta) if n.endswith(".md"))
    except Exception:
        return []
    estado = _leer_estado(carpeta)
    vistas = set(estado.get(sesion, []))
    nuevas = [n for n in nombres if n not in vistas]
    if not nuevas:
        return []
    lineas = ["NOTA NUEVA DE UN CHAT AUXILIAR (spec 081; cuéntasela a Darwin en una frase y sigue con lo suyo):"]
    for n in nuevas[:MAX_NOTAS]:
        try:
            with open(os.path.join(carpeta, n), encoding="utf-8") as f:
                texto = f.read().strip()
        except Exception:
            continue
        if len(texto) > MAX_CARACTERES:
            texto = texto[:MAX_CARACTERES] + "…"
        lineas.append("— " + n + "\n" + texto)
    if len(nuevas) > MAX_NOTAS:
        lineas.append("(y %d más en .brain/notas-chats/)" % (len(nuevas) - MAX_NOTAS))
    estado[sesion] = sorted(vistas | set(nuevas))
    try:
        with open(os.path.join(carpeta, ESTADO), "w", encoding="utf-8") as f:
            json.dump(estado, f)
    except Exception:
        pass
    return lineas


def decidir(datos):
    """Devuelve (modo, sesion) según quién llama: Antigravity manda `conversationId`; Claude Code y Codex, `session_id`."""
    if "conversationId" in datos:
        return "antigravity", str(datos.get("conversationId") or "sin-sesion")
    return "texto", str(datos.get("session_id") or "sin-sesion")


def salida(datos, raiz=RAIZ):
    """Texto que se imprime para este hook (vacío si no hay nada que avisar). Spec 081 y 082."""
    modo, sesion = decidir(datos)
    if modo == "antigravity" and datos.get("invocationNum") != 1:
        return ""  # PreInvocation salta antes de cada llamada al modelo: solo la primera tras el mensaje de Darwin
    lineas = avisar(raiz, sesion)
    if not lineas:
        return ""
    texto = "\n".join(lineas) + "\n"
    if modo == "antigravity":
        return json.dumps({"injectSteps": [{"ephemeralMessage": texto}]}, ensure_ascii=False)
    return texto


def main():
    try:
        datos = json.loads(sys.stdin.read() or "{}")
        texto = salida(datos)
        if texto:
            sys.stdout.buffer.write(texto.encode("utf-8"))
    except Exception:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
