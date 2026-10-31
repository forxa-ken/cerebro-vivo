#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardián 1 de Cerebro Vivo · aviso de cierre.

Se ejecuta como aviso de «fin de respuesta» de Claude Code (hook Stop). Si en esta
respuesta se tocaron archivos del proyecto y falta registrar la tarea (o pendientes.md
pasó su tope), devuelve el aviso por stderr con código 2: la IA lo lee y lo corrige.
Avisa una sola vez por respuesta (stop_hook_active) y nunca falla de forma ruidosa.
Solo librería estándar. Ajustes en guardianes.json."""

import fnmatch
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))


def cargar_config():
    with open(os.path.join(AQUI, "guardianes.json"), encoding="utf-8") as f:
        return json.load(f)


def cambios_git(raiz):
    """Rutas con cambios sin commitear (modificadas, nuevas o borradas)."""
    out = subprocess.run(
        ["git", "-c", "core.quotepath=false", "status", "--porcelain"],
        cwd=raiz, capture_output=True, text=True, encoding="utf-8", timeout=15,
    ).stdout
    rutas = []
    for linea in out.splitlines():
        ruta = linea[3:].strip().strip('"')
        if " -> " in ruta:
            ruta = ruta.split(" -> ")[-1]
        if ruta:
            rutas.append(ruta.replace("\\", "/"))
    return rutas


def esta_ignorada(ruta, patrones):
    return any(fnmatch.fnmatch(ruta, p) for p in patrones)


def analizar_respuesta(transcript_path, registro):
    """Mira lo que hizo la IA desde el último mensaje del usuario.
    Devuelve (editó_archivos, tocó_el_registro); (None, None) si no se puede leer el registro del chat."""
    nombre = os.path.basename(registro)
    try:
        with open(transcript_path, encoding="utf-8") as f:
            lineas = f.read().splitlines()
    except Exception:
        return None, None
    editado = registro_tocado = False
    for linea in lineas:
        try:
            e = json.loads(linea)
        except ValueError:
            continue
        msg = e.get("message") or {}
        contenido = msg.get("content")
        if e.get("type") == "user":
            es_texto = isinstance(contenido, str) or any(
                isinstance(b, dict) and b.get("type") == "text" for b in (contenido or []))
            if es_texto:
                editado = registro_tocado = False  # mensaje nuevo del usuario: empieza otra respuesta
        elif e.get("type") == "assistant" and isinstance(contenido, list):
            for b in contenido:
                if not (isinstance(b, dict) and b.get("type") == "tool_use"):
                    continue
                entrada = b.get("input") or {}
                if b.get("name") in ("Edit", "Write", "NotebookEdit"):
                    editado = True
                    if os.path.basename(str(entrada.get("file_path", ""))) == nombre:
                        registro_tocado = True
                elif nombre in str(entrada.get("command", "")) or "cerrar.py" in str(entrada.get("command", "")):
                    registro_tocado = True  # p. ej. añadir la línea con la terminal
    return editado, registro_tocado


def evaluar(cambios, tam_pendientes, cfg, hubo_ediciones=None, registro_en_respuesta=None):
    """Devuelve la lista de avisos (vacía = todo en orden). Función pura, probada en tests."""
    avisos = []
    del_proyecto = [c for c in cambios if not esta_ignorada(c, cfg["ignorar_cambios"])]
    # Si se sabe qué hizo la IA en esta respuesta, manda eso (un registro modificado de una tarea anterior
    # sin commitear no cuenta); si no, se usa el estado de git.
    if registro_en_respuesta is not None:
        registro_tocado = registro_en_respuesta
    else:
        registro_tocado = any(c == cfg["registro"] for c in cambios)
    if del_proyecto and not registro_tocado and hubo_ediciones is not False:
        avisos.append(
            "Hay cambios en el proyecto (%s) y falta la línea en %s. "
            "Cierra la tarea: línea en el registro, pendientes al día y, si hubo una decisión importante, su ficha D-NNN."
            % (", ".join(del_proyecto[:4]) + ("…" if len(del_proyecto) > 4 else ""), cfg["registro"]))
    if tam_pendientes is not None and tam_pendientes > cfg["tope_pendientes_bytes"]:
        avisos.append(
            "%s pesa %d bytes y el tope es %d. Pasa lo ya probado a archive/hechos.md "
            "(y su fila al índice) y deja aquí solo lo que falta."
            % (cfg["pendientes"], tam_pendientes, cfg["tope_pendientes_bytes"]))
    return avisos


def main():
    try:
        datos = json.load(sys.stdin)
    except Exception:
        datos = {}
    if datos.get("stop_hook_active"):
        return 0  # ya avisó una vez en esta respuesta: no insistir
    try:
        cfg = cargar_config()
        tam = None
        ruta_p = os.path.join(RAIZ, cfg["pendientes"])
        if os.path.exists(ruta_p):
            tam = os.path.getsize(ruta_p)
        ediciones, en_registro = (None, None)
        if datos.get("transcript_path"):
            ediciones, en_registro = analizar_respuesta(datos["transcript_path"], cfg["registro"])
        avisos = evaluar(cambios_git(RAIZ), tam, cfg, ediciones, en_registro)
        try:  # spec 056: aviso de longitud de chat (una vez por tramo; calla si falla)
            import importlib.util
            espec = importlib.util.spec_from_file_location("longitud", os.path.join(AQUI, "longitud.py"))
            longitud = importlib.util.module_from_spec(espec)
            espec.loader.exec_module(longitud)
            largo = longitud.aviso(datos.get("transcript_path"), cfg)
            if largo:
                avisos.append(largo)
        except Exception:
            pass
    except Exception:
        return 0  # un guardián nunca debe romper el trabajo
    if avisos:
        texto = "🐺 Cerebro Vivo · antes de dar la tarea por terminada:\n- " + "\n- ".join(avisos) + "\n"
        sys.stderr.buffer.write(texto.encode("utf-8"))  # bytes UTF-8: la consola de Windows (cp1252) rompía tildes y emoji
        sys.stderr.flush()
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
