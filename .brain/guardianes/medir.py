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
  python medir.py --ritual                 # coste de los rituales del arnés frente al trabajo y avisos del guardián (informe 032)
  python medir.py --fabrica --proyecto RUTA   # gasto de Codex por encargo de la fábrica (spec 035; lee ~/.codex/sessions)
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


def cierres_de_chat(ruta):
    """Spec 038: tareas terminadas que se ven en el chat = veces que la IA escribió en `decisions.log` (Edit/Write) o lanzó
    `cerrar.py`. La línea automática del hook Stop (modo ligero) no sale en el registro del chat y no se cuenta."""
    vistos = set()
    try:
        with open(ruta, encoding="utf-8", errors="replace") as f:
            for linea in f:
                try:
                    e = json.loads(linea)
                except ValueError:
                    continue
                contenido = (e.get("message") or {}).get("content")
                if e.get("type") != "assistant" or not isinstance(contenido, list):
                    continue
                for b in contenido:
                    if not isinstance(b, dict) or b.get("type") != "tool_use":
                        continue
                    entrada = b.get("input") or {}
                    cierra = ("cerrar.py" in str(entrada.get("command", "")) if b.get("name") in ("Bash", "PowerShell")
                              else os.path.basename(str(entrada.get("file_path", ""))) == "decisions.log")
                    if cierra:
                        vistos.add(b.get("id") or len(vistos))
    except OSError:
        pass
    return len(vistos)


def por_tarea(chats):
    """(tokens nuevos + salida por tarea terminada, tareas, chats con alguna tarea) de una lista de chats; None si no hay tareas."""
    tareas = sum(c.get("cierres", 0) for c in chats)
    if not tareas:
        return None
    con = [c for c in chats if c.get("cierres", 0)]
    return sum(c["nuevos"] + c["salida"] for c in con) / tareas, tareas, len(con)


def medir_chat(ruta):
    d = leer_chat(ruta)
    d["cierres"] = cierres_de_chat(ruta)
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
    a, b = por_tarea(con), por_tarea(sin)
    if a and b:
        print(tp("medir_por_tarea_comparar") % (k(a[0]), a[1], k(b[0]), b[1]))


def skills_usadas(ruta):
    """{skill: veces} de UN chat. Cuenta las llamadas a la herramienta Skill y los comandos «/skill» escritos por Darwin;
    como un comando suele acabar en una llamada, por skill se toma el mayor de los dos números (no se suman)."""
    llamadas, comandos = {}, {}
    with open(ruta, encoding="utf-8", errors="replace") as f:
        for linea in f:
            try:
                e = json.loads(linea)
            except ValueError:
                continue
            contenido = (e.get("message") or {}).get("content")
            bloques = contenido if isinstance(contenido, list) else [{"type": "text", "text": contenido}] if isinstance(contenido, str) else []
            for b in bloques:
                if not isinstance(b, dict):
                    continue
                if b.get("type") == "tool_use" and b.get("name") == "Skill":
                    nombre = str((b.get("input") or {}).get("skill") or "").split(":")[-1]
                    if nombre:
                        llamadas[nombre] = llamadas.get(nombre, 0) + 1
                elif e.get("type") == "user" and b.get("type") == "text":
                    for nombre in re.findall(r"<command-name>/?([^<\s]+)</command-name>", b.get("text") or ""):
                        nombre = nombre.split(":")[-1]
                        comandos[nombre] = comandos.get(nombre, 0) + 1
    return {n: max(llamadas.get(n, 0), comandos.get(n, 0)) for n in set(llamadas) | set(comandos)}


def uso_de_skills(carpeta, raiz):
    """Tabla [(skill, veces, chats, última fecha)] de las skills del proyecto (las no usadas salen con 0), de más a menos usadas.
    Informe 028 (3.2): sustituye al campo «Veces» de cada skill, que nadie actualizaba."""
    ruta_skills = os.path.join(raiz, ".claude", "skills")
    nombres = sorted(d for d in os.listdir(ruta_skills) if os.path.isdir(os.path.join(ruta_skills, d))) if os.path.isdir(ruta_skills) else []
    veces, chats, ultima = {n: 0 for n in nombres}, {n: 0 for n in nombres}, {n: "" for n in nombres}
    for ruta in glob.glob(os.path.join(carpeta, "*.jsonl")):
        try:
            usos = skills_usadas(ruta)
            fecha = leer_chat(ruta)["fecha"]
        except Exception:
            continue
        for n, v in usos.items():
            if n in veces:
                veces[n] += v
                chats[n] += 1
                ultima[n] = max(ultima[n], fecha or "")
    return sorted(((n, veces[n], chats[n], ultima[n]) for n in nombres), key=lambda f: (-f[1], f[0]))


# Informe 032: coste de los rituales del arnés. Se clasifica cada llamada de la IA por lo que hizo (por reglas sobre el texto
# de sus herramientas; una llamada mixta cuenta como trabajo) y se cuentan los avisos del guardián de cierre.
RITUAL_ORDEN = re.compile(r"cerrar\.py|lecciones\.py|arranque\.py|cierre\.py|hitos\.py|traspaso|decisions\.log|hechos|\.brain/lecciones|pendientes|\.brain/notas|\.brain/constitution|\.brain/decisions", re.I)
MANT_ORDEN = re.compile(r"CAMBIOS\.md|manifiesto|actualizar_arnes|medir\.py|VERSION")
APP_HERRAMIENTAS = ("mcp__ccd_turn__update_plan", "mcp__ccd_turn__wrap_up", "mcp__ccd_session__mark_chapter")
CATEGORIAS = ("trabajo", "memoria", "chat_nuevo", "aviso", "app", "mant")


def tipo_aviso(texto):
    if re.search(r"Hito sin lecci|milestone without a lesson", texto, re.I):
        return "hito"
    if re.search(r"decisions\.log|línea de registro|cerrar\.py|Close the task", texto, re.I):
        return "registro"
    if re.search(r"ya pesa|chat nuevo|new chat|traspaso|handover", texto, re.I):
        return "largo"
    return "otros"


def ritual_de_chat(ruta, skills_arnes):
    """(coste por categoría, avisos por tipo, llamadas) de UN chat. Solo lectura."""
    entradas = []
    with open(ruta, encoding="utf-8", errors="replace") as f:
        for linea in f:
            try:
                entradas.append(json.loads(linea))
            except ValueError:
                pass
    llamadas, aviso_pendiente, avisos = {}, False, {}
    for e in entradas:
        m = e.get("message") or {}
        if e.get("type") == "user":
            c = m.get("content")
            texto = c if isinstance(c, str) else " ".join(str(b.get("text", "")) for b in (c or []) if isinstance(b, dict))
            if texto.startswith("Stop hook feedback"):
                aviso_pendiente = True
                tipo = tipo_aviso(texto)
                avisos[tipo] = avisos.get(tipo, 0) + 1
        elif e.get("type") == "assistant" and isinstance(m.get("usage"), dict):
            clave = m.get("id") or e.get("uuid") or len(llamadas)
            previa = llamadas.get(clave)
            bloques = [b for b in (m.get("content") or []) if isinstance(b, dict)]
            if previa:
                previa["bloques"] += bloques
                previa["uso"] = m["usage"]
            else:
                llamadas[clave] = {"uso": m["usage"], "bloques": bloques, "aviso": aviso_pendiente}
                aviso_pendiente = False
    coste_por = {c: 0.0 for c in CATEGORIAS}
    for ll in llamadas.values():
        u = ll["uso"]
        cats = []
        for b in ll["bloques"]:
            if b.get("type") != "tool_use":
                continue
            nombre, entrada = b.get("name", ""), json.dumps(b.get("input", {}), ensure_ascii=False)
            if nombre == "Skill":
                cats.append("memoria" if str((b.get("input") or {}).get("skill", "")).split(":")[-1] in skills_arnes else "trabajo")
            elif nombre in APP_HERRAMIENTAS:
                cats.append("app")
            elif nombre.startswith("mcp__ccd_session") or re.search(r"start_session|detach_session|get_session", entrada):
                cats.append("chat_nuevo")
            elif MANT_ORDEN.search(entrada):
                cats.append("mant")
            elif RITUAL_ORDEN.search(entrada):
                cats.append("memoria")
            else:
                cats.append("trabajo")
        cat = max(set(cats), key=cats.count) if cats and "trabajo" not in cats else "trabajo"
        if ll["aviso"]:
            cat = "aviso"
        coste_por[cat] += coste(u.get("input_tokens", 0) or 0, u.get("cache_creation_input_tokens", 0) or 0,
                                u.get("cache_read_input_tokens", 0) or 0, u.get("output_tokens", 0) or 0)
    return coste_por, avisos, len(llamadas)


def ritual_de_proyecto(carpeta, raiz):
    """Suma de todos los chats (los de menos de 3 llamadas se descartan): (coste por categoría, avisos por tipo, chats, llamadas)."""
    ruta_skills = os.path.join(raiz, ".claude", "skills")
    skills = set(os.listdir(ruta_skills)) if os.path.isdir(ruta_skills) else set()
    total, avisos, chats, llamadas = {c: 0.0 for c in CATEGORIAS}, {}, 0, 0
    for ruta in glob.glob(os.path.join(carpeta, "*.jsonl")):
        try:
            por, av, n = ritual_de_chat(ruta, skills)
        except Exception:
            continue
        if n < 3:
            continue
        chats += 1
        llamadas += n
        for c, v in por.items():
            total[c] += v
        for tipo, v in av.items():
            avisos[tipo] = avisos.get(tipo, 0) + v
    return total, avisos, chats, llamadas


def imprimir_ritual(total, avisos, chats, llamadas):
    suma = sum(total.values())
    if not suma:
        print(tp("medir_encontre_registros") % "")
        return
    print(tp("medir_ritual_cabecera") % (chats, llamadas))
    nombres = {"trabajo": tp("medir_ritual_trabajo"), "memoria": tp("medir_ritual_memoria"), "chat_nuevo": tp("medir_ritual_chat_nuevo"),
               "aviso": tp("medir_ritual_aviso"), "app": tp("medir_ritual_app"), "mant": tp("medir_ritual_mant")}
    for c in CATEGORIAS:
        print("  %-38s %5.1f %%" % (nombres[c], 100 * total[c] / suma))
    print(tp("medir_ritual_total") % (100 * (total["memoria"] + total["chat_nuevo"] + total["aviso"]) / suma))
    n = sum(avisos.values())
    print(tp("medir_ritual_avisos") % (n, n / chats if chats else 0, avisos.get("hito", 0), avisos.get("registro", 0),
                                      avisos.get("largo", 0), avisos.get("otros", 0)))


def carpeta_codex():
    return os.path.join(os.path.expanduser("~"), ".codex", "sessions")


def gasto_codex(ruta):
    """(cwd, tokens gastados) de UNA sesión de Codex, o None si no es de una persona (revisiones internas) o no trae cuenta.
    Gastado = total - leído de caché: es la cifra que Codex llama «tokens used» y la que usa el tope de la fábrica."""
    cwd, origen, ultimo = "", "", None
    with open(ruta, encoding="utf-8", errors="replace") as f:
        for linea in f:
            try:
                e = json.loads(linea)
            except ValueError:
                continue
            p = e.get("payload") or {}
            if e.get("type") == "session_meta":
                cwd, origen = str(p.get("cwd") or ""), str(p.get("thread_source") or "")
            elif p.get("type") == "token_count" and isinstance(p.get("info"), dict):
                ultimo = p["info"].get("total_token_usage") or ultimo
    if not ultimo or origen != "user":
        return None
    return cwd, max(0, (ultimo.get("total_tokens") or 0) - (ultimo.get("cached_input_tokens") or 0))


def fabrica_de_proyecto(proyecto, carpeta=None):
    """{carpeta de trabajo: [sesiones, tokens]} de las sesiones de Codex cuyo cwd empieza por la ruta del proyecto
    (los encargos de la fábrica viven en carpetas hermanas «Proyecto-encargo-NNN»). Solo lectura."""
    base = os.path.normcase(os.path.abspath(proyecto))
    por = {}
    for ruta in sorted(glob.glob(os.path.join(carpeta or carpeta_codex(), "**", "rollout-*.jsonl"), recursive=True)):
        try:
            r = gasto_codex(ruta)
        except Exception:
            continue
        if r and os.path.normcase(os.path.abspath(r[0])).startswith(base):
            fila = por.setdefault(r[0], [0, 0])
            fila[0] += 1
            fila[1] += r[1]
    return por


def imprimir_fabrica(por, proyecto):
    if not por:
        print(tp("medir_fabrica_vacio") % proyecto)
        return
    print("%-52s %8s %10s" % (tp("medir_fabrica_carpeta"), tp("medir_fabrica_sesiones"), tp("medir_fabrica_tokens")))
    for cwd, (n, t) in sorted(por.items()):
        print("%-52s %8d %10s" % (cwd[-52:], n, k(t)))
    print(tp("medir_fabrica_total") % (sum(v[0] for v in por.values()), sum(v[1] for v in por.values())))
    print(tp("medir_fabrica_nota"))


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
    ap.add_argument("--skills", action="store_true", help=tp("ayuda_medir_skills"))
    ap.add_argument("--fabrica", action="store_true", help=tp("ayuda_medir_fabrica"))
    ap.add_argument("--ritual", action="store_true", help=tp("ayuda_medir_ritual"))
    a = ap.parse_args(argv)
    if a.fabrica:
        imprimir_fabrica(fabrica_de_proyecto(a.proyecto), a.proyecto)
        return 0
    if a.ritual:
        imprimir_ritual(*ritual_de_proyecto(carpeta_de(a.proyecto), a.proyecto))
        return 0
    if a.skills:
        tabla = uso_de_skills(carpeta_de(a.proyecto), a.proyecto)
        print("%-34s %6s %6s  %s" % (tp("medir_skill"), tp("medir_veces"), "Chats", tp("medir_ultima")))
        for nombre, veces, chats, ultima in tabla:
            print("%-34s %6d %6d  %s" % (nombre, veces, chats, ultima or "-"))
        print(tp("medir_skills_resumen") % (sum(1 for f in tabla if f[1]), len(tabla)))
        return 0
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
    pt = por_tarea(chats)
    if pt:
        print(tp("medir_por_tarea") % (k(pt[0]), pt[1], pt[2]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
