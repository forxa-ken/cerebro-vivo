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
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, AQUI)
from textos import t  # noqa: E402  (spec 024: mensajes en es/en)


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


def detalle_respuesta(transcript_path, raiz):
    """Para el cierre ligero (spec 002): archivos que editó la IA desde el último mensaje del usuario (rutas relativas
    al proyecto) y si el último comando de pruebas salió en verde (True/False; None si no corrió ninguno)."""
    archivos, ordenes, verde = [], {}, None
    try:
        with open(transcript_path, encoding="utf-8") as f:
            lineas = f.read().splitlines()
    except Exception:
        return [], None
    for linea in lineas:
        try:
            e = json.loads(linea)
        except ValueError:
            continue
        contenido = (e.get("message") or {}).get("content")
        if e.get("type") == "user":
            if isinstance(contenido, str) or any(isinstance(b, dict) and b.get("type") == "text" for b in (contenido or [])):
                archivos, ordenes, verde = [], {}, None  # mensaje nuevo del usuario: empieza otra respuesta
            for b in contenido if isinstance(contenido, list) else []:
                if isinstance(b, dict) and b.get("type") == "tool_result" and b.get("tool_use_id") in ordenes:
                    texto = b.get("content")
                    if isinstance(texto, list):
                        texto = " ".join(str(x.get("text", "")) for x in texto if isinstance(x, dict))
                    texto = str(texto)
                    verde = bool(re.search(r"\bOK\b|\d+ passed", texto)) and not re.search(r"FAILED|Traceback|\d+ failed|Error", texto)
        elif e.get("type") == "assistant" and isinstance(contenido, list):
            for b in contenido:
                if not (isinstance(b, dict) and b.get("type") == "tool_use"):
                    continue
                entrada = b.get("input") or {}
                if b.get("name") in ("Edit", "Write", "NotebookEdit", "MultiEdit"):
                    ruta = str(entrada.get("file_path", ""))
                    try:
                        ruta = os.path.relpath(ruta, raiz)
                    except ValueError:
                        pass
                    archivos.append(ruta.replace("\\", "/"))
                elif b.get("name") == "Bash" and re.search(r"unittest|pytest", str(entrada.get("command", ""))):
                    ordenes[b.get("id")] = True
                    verde = None  # hay una corrida nueva pendiente de resultado
    return archivos, verde


def ediciones_sin_cerrar(transcript_path, cfg, raiz):
    """Spec 033 (cierre por bloque): cuántos archivos del proyecto (no ignorados) editó el chat con Edit/Write desde la
    última vez que tocó el registro. None si no se puede leer el chat. Cuenta en todo el chat, no solo en esta respuesta."""
    nombre = os.path.basename(cfg["registro"])
    try:
        with open(transcript_path, encoding="utf-8") as f:
            lineas = f.read().splitlines()
    except Exception:
        return None
    n = 0
    for linea in lineas:
        try:
            e = json.loads(linea)
        except ValueError:
            continue
        contenido = (e.get("message") or {}).get("content")
        if e.get("type") != "assistant" or not isinstance(contenido, list):
            continue
        for b in contenido:
            if not (isinstance(b, dict) and b.get("type") == "tool_use"):
                continue
            entrada = b.get("input") or {}
            orden = str(entrada.get("command", ""))
            if b.get("name") in ("Edit", "Write", "NotebookEdit", "MultiEdit"):
                ruta = str(entrada.get("file_path", ""))
                if os.path.basename(ruta) == nombre:
                    n = 0
                    continue
                try:
                    ruta = os.path.relpath(ruta, raiz)
                except ValueError:
                    pass
                ruta = ruta.replace("\\", "/")
                if not ruta.startswith("..") and not esta_ignorada(ruta, cfg["ignorar_cambios"]):
                    n += 1
            elif nombre in orden or "cerrar.py" in orden:
                n = 0
    return n


def cierre_ligero(cfg, archivos, verde):
    """Spec 002. Devuelve el texto de la línea automática si la tarea es pequeña, no sensible y con pruebas en verde;
    None si hay que cerrar como siempre. Función pura, probada en tests."""
    lig = cfg.get("modo_ligero") or {}
    if not cfg.get("modo_ligero_activo") or verde is not True:
        return None
    propios = sorted({a for a in archivos if a and not esta_ignorada(a, cfg["ignorar_cambios"]) and not a.startswith("..")})
    if len(propios) != len(set(a for a in archivos if a and not a.startswith(".."))) or not propios:
        return None  # tocó algo de .brain/ u otra zona ignorada, o no tocó nada del proyecto: cierre normal
    if len(propios) > lig.get("max_archivos", 2):
        return None
    if any(clave in a.lower() for a in propios for clave in lig.get("sensibles", [])):
        return None
    return t(cfg, "cierre_auto", ", ".join(propios))


def escribir_linea_auto(raiz, cfg, texto):
    import datetime
    ruta = os.path.join(raiz, cfg["registro"])
    try:  # no repetir la misma línea automática en respuestas seguidas
        with open(ruta, encoding="utf-8") as f:
            previas = [l for l in f.read().splitlines() if l.strip()]
        if previas and texto in previas[-1]:
            return
    except OSError:
        pass
    with open(ruta, "a", encoding="utf-8") as f:
        f.write("%s | Claude (auto) | %s | Fast-Track\n" % (datetime.date.today().isoformat(), texto))


def evaluar(cambios, tam_pendientes, cfg, hubo_ediciones=None, registro_en_respuesta=None, editados=None, sin_cerrar=None):
    """Devuelve la lista de avisos (vacía = todo en orden). Función pura, probada en tests.
    `editados` (spec 031): archivos que el chat editó con Edit/Write; si hay, solo cuentan esos cambios de git
    (lo que trajo `/actualizar` u otro chat no es de este chat). Sin lista, vale todo lo que git ve cambiado.
    `sin_cerrar` (spec 033, cierre por bloque): archivos editados desde el último cierre; si es menor que
    `cierre_bloque_max_ediciones` (15) no se pide la línea todavía: se cierra por bloque, no por tarea pequeña.
    Con `cierre_por_bloque` en false, o sin dato, se pide en cada respuesta como antes."""
    avisos = []
    del_proyecto = [c for c in cambios if not esta_ignorada(c, cfg["ignorar_cambios"])]
    if editados:
        del_proyecto = [c for c in del_proyecto if c in editados]
    # Si se sabe qué hizo la IA en esta respuesta, manda eso (un registro modificado de una tarea anterior
    # sin commitear no cuenta); si no, se usa el estado de git.
    if registro_en_respuesta is not None:
        registro_tocado = registro_en_respuesta
    else:
        registro_tocado = any(c == cfg["registro"] for c in cambios)
    por_bloque = bool(cfg.get("cierre_por_bloque", True)) and sin_cerrar is not None
    if por_bloque and sin_cerrar < cfg.get("cierre_bloque_max_ediciones", 15):
        del_proyecto = []  # el bloque sigue abierto: aún no toca cerrar
    if del_proyecto and not registro_tocado and hubo_ediciones is not False:
        avisos.append(t(cfg, "cierre_falta_linea",
                        ", ".join(del_proyecto[:4]) + ("…" if len(del_proyecto) > 4 else ""), cfg["registro"]))
    if tam_pendientes is not None and tam_pendientes > cfg["tope_pendientes_bytes"]:
        avisos.append(t(cfg, "cierre_tope_pendientes", cfg["pendientes"], tam_pendientes, cfg["tope_pendientes_bytes"]))
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
            if ediciones is not None and not en_registro:  # spec 002: tarea pequeña y en verde -> el guardián escribe la línea, sin vuelta extra de la IA
                try:
                    archivos, verde = detalle_respuesta(datos["transcript_path"], RAIZ)
                    if not archivos and verde is True:  # spec 003: la IA editó con la terminal (no con Edit/Write): vale lo que git ve cambiado
                        archivos = [c for c in cambios_git(RAIZ) if not esta_ignorada(c, cfg["ignorar_cambios"])]
                    linea_auto = cierre_ligero(cfg, archivos, verde)
                    if linea_auto:
                        escribir_linea_auto(RAIZ, cfg, linea_auto)
                        en_registro = True
                except Exception:
                    pass
        editados = []
        if datos.get("transcript_path"):
            try:
                editados = detalle_respuesta(datos["transcript_path"], RAIZ)[0]
            except Exception:
                editados = []
        sin_cerrar = None
        if datos.get("transcript_path"):
            try:
                sin_cerrar = ediciones_sin_cerrar(datos["transcript_path"], cfg, RAIZ)
            except Exception:
                sin_cerrar = None
        avisos = evaluar(cambios_git(RAIZ), tam, cfg, ediciones, en_registro, editados, sin_cerrar)
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
        try:  # spec 026: hito (error resuelto, archivo delicado, cambio grande) sin lección apuntada, y traspaso corto
            espec = importlib.util.spec_from_file_location("hitos", os.path.join(AQUI, "hitos.py"))
            hitos = importlib.util.module_from_spec(espec)
            espec.loader.exec_module(hitos)
            avisos += hitos.avisos(datos.get("transcript_path"), cfg, RAIZ)
        except Exception:
            pass
    except Exception:
        return 0  # un guardián nunca debe romper el trabajo
    if avisos:
        texto = t(cfg, "cierre_titulo") + "\n- " + "\n- ".join(avisos) + "\n"
        sys.stderr.buffer.write(texto.encode("utf-8"))  # bytes UTF-8: la consola de Windows (cp1252) rompía tildes y emoji
        sys.stderr.flush()
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
