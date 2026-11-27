#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sugeridor de lecciones de Cerebro Vivo (spec 095): avisa de lo que no dejó huella mecánica y quizá merece apuntarse.

Lo llama `cierre.py` (hook Stop) con el registro del chat. Desde la última marca (una lección apuntada, `lecciones.py ninguna`
o una edición de `.brain/propuestas.md`) busca tres señales baratas, sin llamar a ninguna IA externa:
  - correcciones de Darwin («no, así no», «te dije», «otra vez»);
  - decisiones («descartado», «vamos con», «mejor usa»);
  - una misma orden de consola repetida 3 veces o más (candidata a skill).
Antes de avisar descarta lo que la memoria ya recoge (búsqueda en lecciones y decisiones). Solo AVISA: la IA del chat decide si lo
apunta (`lecciones.py`), lo propone en `.brain/propuestas.md` o responde «ninguna»; nada entra solo en la memoria.
Solo lectura del registro, solo librería estándar. Si algo falla, calla. Ajustes en guardianes.json:
`sugeridor_activo` ("auto" = solo en el repo del arnés, donde existe manifiesto.json; true/false lo fuerzan),
`sugeridor_max` (señales por aviso, 3), `sugeridor_repeticiones` (3), `sugeridor_dedup_puntos` (40)."""

import importlib.util
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, AQUI)
from textos import t  # noqa: E402  (spec 024: mensajes en es/en)

EDITORES = ("Edit", "Write", "NotebookEdit", "MultiEdit")
CONSOLAS = ("Bash", "PowerShell")
CORRECCION = re.compile(
    r"^\s*(no\s*[,.!]|no\s+(es|era|eso|así|asi|quiero|hagas|toques|lo|me|te)\b|mal\b|eso no|así no|asi no|that'?s not|wrong\b|not like that)"
    r"|\b(te dije|ya te dije|te lo dije|otra vez|i told you)\b", re.I)
DECISION = re.compile(
    r"\b(descart\w+|vamos con|decidid[oa]|dejemos|mejor (que|usa|haz|hagamos|dejemos)|let'?s go with|we decided|instead of)\b", re.I)
# Órdenes que se repiten por oficio y no enseñan nada: lectura, git, pruebas y las propias herramientas de memoria.
IGNORAR_ORDEN = re.compile(r"\b(git|unittest|pytest|cerrar\.py|lecciones\.py|sugeridor\.py|hitos\.py|buscar\.py|arranque\.py)\b", re.I)
LECTURA = ("sed", "cat", "head", "tail", "grep", "rg", "ls", "awk", "find", "wc", "du", "echo", "type", "findstr", "get-content",
           "select-string", "get-childitem", "test-path", "diff", "sort", "uniq", "stat", "cd", "set-location")


def ajustes(cfg, raiz=RAIZ):
    activo = cfg.get("sugeridor_activo", "auto")
    if activo == "auto":
        activo = os.path.exists(os.path.join(raiz, "manifiesto.json"))
    return {"activo": bool(activo),
            "max": max(1, int(cfg.get("sugeridor_max", 3))),
            "repeticiones": max(2, int(cfg.get("sugeridor_repeticiones", 3))),
            "dedup": int(cfg.get("sugeridor_dedup_puntos", 40))}


def texto_de_usuario(contenido):
    """Texto escrito por Darwin en un mensaje, o '' si es otra cosa (avisos de hooks, recordatorios, resultados de herramientas)."""
    if isinstance(contenido, list):
        partes = [str(b.get("text", "")) for b in contenido if isinstance(b, dict) and b.get("type") == "text"]
        contenido = " ".join(partes)
    if not isinstance(contenido, str):
        return ""
    contenido = contenido.strip()
    if not contenido or contenido.startswith("<") or "system-reminder" in contenido or "hook feedback" in contenido.lower():
        return ""
    return contenido[:300]


def es_marca(nombre, entrada):
    """¿Esta llamada apunta algo (lección, «ninguna», propuesta)? Entonces se vuelve a empezar a contar."""
    if nombre in CONSOLAS:
        orden = str(entrada.get("command", ""))
        return "lecciones.py" in orden or "sugeridor.py" in orden
    if nombre in EDITORES:
        ruta = str(entrada.get("file_path", "")).replace("\\", "/")
        return "/lecciones/" in ruta or ruta.endswith("/propuestas.md")
    return False


def orden_repetible(entrada):
    """La orden de consola normalizada, o None si es de las que se repiten por oficio."""
    orden = " ".join(str(entrada.get("command", "")).split())
    if len(orden) < 12 or IGNORAR_ORDEN.search(orden):
        return None
    primera = orden.split()[0].lower()
    if primera in LECTURA:
        return None
    return orden[:160]


def analizar(ruta_registro):
    """([frases de corrección], [frases de decisión], [órdenes repetidas con su cuenta]) desde la última marca. Probada en tests."""
    correcciones, decisiones, ordenes = [], [], {}
    with open(ruta_registro, encoding="utf-8", errors="replace") as f:
        for linea in f:
            try:
                e = json.loads(linea)
            except ValueError:
                continue
            contenido = (e.get("message") or {}).get("content")
            if e.get("type") == "user":
                texto = texto_de_usuario(contenido)
                if texto:
                    if CORRECCION.search(texto):
                        correcciones.append(texto)
                    elif DECISION.search(texto):
                        decisiones.append(texto)
            elif e.get("type") == "assistant" and isinstance(contenido, list):
                for b in contenido:
                    if not (isinstance(b, dict) and b.get("type") == "tool_use"):
                        continue
                    nombre, entrada = b.get("name", ""), b.get("input") or {}
                    if es_marca(nombre, entrada):
                        correcciones, decisiones, ordenes = [], [], {}
                    elif nombre in CONSOLAS:
                        orden = orden_repetible(entrada)
                        if orden:
                            ordenes[orden] = ordenes.get(orden, 0) + 1
    return correcciones, decisiones, ordenes


def ya_apuntado(frase, cfg, raiz, umbral):
    """¿La memoria (lecciones y decisiones) ya recoge algo muy parecido? Si la búsqueda falla, se cuenta como no apuntado."""
    try:
        espec = importlib.util.spec_from_file_location("buscar", os.path.join(AQUI, "buscar.py"))
        buscar = importlib.util.module_from_spec(espec)
        espec.loader.exec_module(buscar)
        res = buscar.buscar(raiz, frase, 1, solo=["lecciones", "decisions"])
        return bool(res) and res[0]["puntos"] >= umbral
    except Exception:
        return False


def corta(frase, n=110):
    frase = " ".join(frase.split())
    return frase if len(frase) <= n else frase[:n - 1] + "…"


def avisos(ruta_registro, cfg, raiz=RAIZ):
    """Lista de avisos para el hook de cierre (vacía = nada que sugerir). Nunca lanza excepciones."""
    try:
        a = ajustes(cfg, raiz)
        if not a["activo"] or not ruta_registro:
            return []
        correcciones, decisiones, ordenes = analizar(ruta_registro)
        senales = []
        for frase in correcciones:
            if not ya_apuntado(frase, cfg, raiz, a["dedup"]):
                senales.append(t(cfg, "sugeridor_correccion", corta(frase)))
        for frase in decisiones:
            if not ya_apuntado(frase, cfg, raiz, a["dedup"]):
                senales.append(t(cfg, "sugeridor_decision", corta(frase)))
        for orden, veces in sorted(ordenes.items(), key=lambda x: -x[1]):
            if veces >= a["repeticiones"]:
                senales.append(t(cfg, "sugeridor_orden", veces, corta(orden)))
        if not senales:
            return []
        return [t(cfg, "sugeridor_aviso", "; ".join(senales[:a["max"]]))]
    except Exception:
        return []


def main():
    """A mano: `sugeridor.py RUTA_DEL_REGISTRO` muestra lo que sugeriría para ese chat."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        with open(os.path.join(AQUI, "guardianes.json"), encoding="utf-8") as f:
            cfg = json.load(f)
    except Exception:
        cfg = {}
    if len(sys.argv) < 2:
        print(t(cfg, "sugeridor_uso"))
        return 0
    lista = avisos(sys.argv[1], cfg)
    print("\n".join(lista) if lista else t(cfg, "sugeridor_nada"))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
