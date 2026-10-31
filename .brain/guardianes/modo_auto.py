#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardián de Cerebro Vivo · modo auto (spec 086).

Dos usos:
  * Hook PreToolUse de Claude Code (sin argumentos, lee el JSON de la herramienta por la entrada estándar). Si el modo
    auto está activo, BLOQUEA lo que se sale de los límites: archivos fuera de la spec, base de datos real, subir a GitHub,
    chat que no es nuevo, spec sin aprobar, fallo repetido, contexto de 200k.
  * Comandos a mano: activar SPEC..., desactivar, estado, fallo CLAVE, resuelto CLAVE, otro-sitio ARCHIVO QUE_FALLABA QUE_CAMBIE,
    continuar, hecha, base-prueba crear|restaurar.
Si el modo no está activo, o si algo falla dentro del hook, calla y deja pasar. Solo librería estándar."""

import fnmatch
import glob
import json
import os
import re
import shutil
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
ESTADO = os.environ.get("CEREBRO_ESTADO_MODO_AUTO") or os.path.join(RAIZ, ".brain", "modo_auto.json")  # la variable la usan los tests
SIEMPRE_PERMITIDO = (".brain/",)  # registro, pendientes, hechos, traspaso, specs...
SIEMPRE_PROTEGIDO = (".brain/guardianes/", ".claude/settings")  # solo si la spec los nombra
HERRAMIENTAS_ARCHIVO = ("Edit", "Write", "NotebookEdit", "MultiEdit")
FALLOS_MAX = 2


def cargar_config():
    with open(os.path.join(AQUI, "guardianes.json"), encoding="utf-8") as f:
        return json.load(f)


def ajustes(cfg):
    m = cfg.get("modo_auto") or {}
    return {"activo": bool(cfg.get("modo_auto_activo", True)),
            "mensajes_chat_nuevo": int(m.get("chat_nuevo_max_mensajes", 4)),
            "contexto": int(m.get("relevo_tokens", cfg.get("longitud_aviso_tokens", 200000))),
            "base": m.get("base_fija", "copias_bd/modo_auto_base.db"),
            "prueba": m.get("base_prueba", "copias_bd/modo_auto_prueba.db"),
            "origen": (cfg.get("base_datos") or {}).get("ruta", "base.db")}


# ---------- estado ----------
def leer_estado():
    try:
        with open(ESTADO, encoding="utf-8") as f:
            e = json.load(f)
        return e if isinstance(e, dict) else {}
    except Exception:
        return {}


def guardar_estado(e):
    with open(ESTADO, "w", encoding="utf-8") as f:
        json.dump(e, f, ensure_ascii=False, indent=2)


# ---------- specs ----------
def ruta_spec(numero, raiz=RAIZ):
    hallados = sorted(glob.glob(os.path.join(raiz, ".brain", "specs", "%s-*.md" % numero)))
    return hallados[0] if hallados else None


def leer_spec(numero, raiz=RAIZ):
    r = ruta_spec(numero, raiz)
    if not r:
        return None, ""
    with open(r, encoding="utf-8") as f:
        t = f.read()
    m = re.search(r"\*\*Estado:\*\*\s*([A-Za-zÁÉÍÓÚáéíóú]+)", t)
    return (m.group(1).lower() if m else ""), t


def spec_aprobada(numero, raiz=RAIZ):
    estado, _ = leer_spec(numero, raiz)
    return estado in ("aprobada", "implementada")


def archivos_de_spec(texto):
    """Rutas entre comillas invertidas del texto de la spec (con '/' o con extensión)."""
    fichas = set()
    for t in re.findall(r"`([^`\s]+)`", texto):
        t = t.replace("\\", "/")
        if t.startswith("./"):
            t = t[2:]
        if "/" in t or re.search(r"\.\w{1,6}$", t):
            fichas.add(t)
    return fichas


def coincide(rel, ficha):
    if ficha.endswith("/"):
        return rel.startswith(ficha) or ("/" + ficha) in ("/" + rel)
    return rel == ficha or rel.endswith("/" + ficha)


def relativa(ruta, raiz=RAIZ):
    r = os.path.abspath(ruta if os.path.isabs(ruta) else os.path.join(raiz, ruta))
    return os.path.relpath(r, raiz).replace("\\", "/")


def archivo_permitido(rel, estado, raiz=RAIZ):
    """(True, '') o (False, motivo)."""
    if rel.startswith(".."):
        return False, "«%s» está fuera del proyecto." % rel
    cola = estado.get("cola") or []
    nombrados = set()
    if cola:
        _, texto = leer_spec(cola[0], raiz)
        nombrados = archivos_de_spec(texto)
    if any(coincide(rel, f) for f in nombrados):
        return True, ""
    if any(coincide(rel, f) for f in estado.get("otros_sitios", [])):
        return True, ""
    if any(rel.startswith(p) for p in SIEMPRE_PROTEGIDO):
        return False, "«%s» es un guardián o ajuste del arnés y la spec no lo nombra." % rel
    if any(rel.startswith(p) for p in SIEMPRE_PERMITIDO):
        return True, ""
    return False, ("«%s» no está en la spec %s. Si es un error de otro sitio, documéntalo antes con: "
                   "modo_auto.py otro-sitio %s «qué fallaba» «qué cambias»." % (rel, cola[0] if cola else "?", rel))


# ---------- contexto y chat ----------
def mensajes_de_usuario(ruta_registro):
    n = 0
    with open(ruta_registro, encoding="utf-8", errors="replace") as f:
        for linea in f:
            try:
                if json.loads(linea).get("type") == "user":
                    n += 1
            except ValueError:
                continue
    return n


def contexto_actual(ruta_registro):
    sys.path.insert(0, AQUI)
    import longitud
    return longitud.contexto_actual(ruta_registro)


# ---------- decisión del hook (función pura, probada en tests) ----------
def decidir(entrada, estado, a, raiz=RAIZ, contexto=0, mensajes=0):
    """(None | motivo_de_bloqueo, estado nuevo)."""
    if not estado.get("activo"):
        return None, estado
    nuevo = dict(estado)
    herramienta = entrada.get("tool_name", "")
    datos = entrada.get("tool_input") or {}
    sesion = entrada.get("session_id", "")
    cola = estado.get("cola") or []

    if sesion:
        if not estado.get("chat_inicio"):
            if mensajes > a["mensajes_chat_nuevo"]:
                return "El modo auto solo empieza en un chat NUEVO y este ya tiene %d mensajes. Abre uno nuevo y escribe «modo auto»." % mensajes, estado
            nuevo["chat_inicio"] = sesion
        elif estado["chat_inicio"] != sesion:
            if estado.get("relevo"):
                nuevo["chat_inicio"], nuevo["relevo"] = sesion, False
            else:
                return "El modo auto pertenece a otro chat. Abre un chat nuevo con el traspaso o escribe «modo normal».", estado

    if not cola:
        return "Modo auto activo pero sin specs en la cola. Añade specs aprobadas (activar NNN) o escribe «modo normal».", nuevo
    for s in cola:
        if not spec_aprobada(s, raiz):
            return "La spec %s no está aprobada. El modo auto solo trabaja con specs aprobadas por Darwin." % s, nuevo
    if estado.get("parado"):
        es_continuar = herramienta == "Bash" and "modo_auto.py" in (datos.get("command") or "") and "continuar" in (datos.get("command") or "")
        if not es_continuar:
            return "PARADO: %s. Avisa a Darwin; solo él puede decir «continuar»." % estado["parado"], nuevo

    escribe = herramienta in HERRAMIENTAS_ARCHIVO
    if contexto >= a["contexto"]:
        nuevo["relevo"] = True
        destino = relativa(datos.get("file_path") or datos.get("notebook_path") or "", raiz) if escribe else ""
        if not (escribe and destino == ".brain/traspaso.md"):
            return ("Contexto de ~%dk tokens: toca relevo. Escribe .brain/traspaso.md (specs hechas y las que quedan en la cola) y abre tú el chat nuevo "
                    "con la herramienta de sesiones (el nuevo sigue en modo auto con el resto de la cola); si la app lo rechaza, avisa a Darwin." % round(contexto / 1000)), nuevo

    if escribe:
        rel = relativa(datos.get("file_path") or datos.get("notebook_path") or "", raiz)
        ok, motivo = archivo_permitido(rel, nuevo, raiz)
        if not ok:
            return motivo, nuevo
    elif herramienta == "Bash":
        orden = datos.get("command") or ""
        if re.search(r"\bgit\s+push\b", orden):
            return "Subir a GitHub está prohibido en modo auto; solo con orden de Darwin.", nuevo
        if re.search(re.escape(os.path.basename(a["origen"])) + r"(?!\w)", orden) and "copias_bd" not in orden and "modo_auto" not in orden:
            return "La base de datos real no se toca en modo auto: usa la copia fija (modo_auto.py base-prueba restaurar).", nuevo
    return None, nuevo


# ---------- hook ----------
def hook():
    try:
        entrada = json.load(sys.stdin)
        a = ajustes(cargar_config())
        estado = leer_estado()
        if not a["activo"] or not estado.get("activo"):
            return 0
        ruta = entrada.get("transcript_path") or ""
        contexto = mensajes = 0
        if ruta and os.path.exists(ruta):
            contexto, mensajes = contexto_actual(ruta), mensajes_de_usuario(ruta)
        motivo, nuevo = decidir(entrada, estado, a, RAIZ, contexto, mensajes)
        if nuevo != estado:
            guardar_estado(nuevo)
        if motivo:
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "deny",
                                                      "permissionDecisionReason": "🐺 Modo auto: " + motivo}}, ensure_ascii=False))
    except Exception:
        pass
    return 0


# ---------- comandos a mano ----------
def activar(numeros):
    if not numeros:
        return "Uso: modo_auto.py activar 086 [087 ...] (specs ya aprobadas)"
    for n in numeros:
        if not ruta_spec(n):
            return "No existe la spec %s." % n
        if not spec_aprobada(n):
            return "La spec %s no está aprobada: no entra en el modo auto." % n
    guardar_estado({"activo": True, "cola": list(numeros), "chat_inicio": "", "relevo": False, "parado": "",
                    "fallos": {}, "otros_sitios": [], "inicio": time.strftime("%Y-%m-%d %H:%M")})
    return "Modo auto ACTIVO con la cola: %s. Empieza en este chat nuevo." % ", ".join(numeros)


def desactivar():
    e = leer_estado()
    e["activo"] = False
    guardar_estado(e)
    return "Modo normal: el modo auto queda apagado."


def registrar_fallo(clave):
    e = leer_estado()
    f = e.setdefault("fallos", {})
    f[clave] = f.get(clave, 0) + 1
    if f[clave] >= FALLOS_MAX:
        e["parado"] = "«%s» ha fallado %d veces" % (clave, f[clave])
    guardar_estado(e)
    return e.get("parado") or "Fallo %d de %d anotado para «%s»." % (f[clave], FALLOS_MAX, clave)


def resuelto(clave):
    """Un fallo arreglado al momento no cuenta: borra su contador."""
    e = leer_estado()
    e.setdefault("fallos", {}).pop(clave, None)
    guardar_estado(e)
    return "«%s» arreglado: su contador de fallos vuelve a cero." % clave


def continuar():
    e = leer_estado()
    e["parado"], e["fallos"] = "", {}
    guardar_estado(e)
    return "Parada levantada por Darwin: contadores de fallos a cero."


def hecha():
    e = leer_estado()
    cola = e.get("cola") or []
    if cola:
        cola.pop(0)
    e["cola"], e["otros_sitios"], e["fallos"] = cola, [], {}
    guardar_estado(e)
    return "Quedan en la cola: %s." % (", ".join(cola) if cola else "ninguna (modo auto sin trabajo: escribe «modo normal»)")


def otro_sitio(archivo, fallaba, cambio, cfg=None):
    e = leer_estado()
    rel = relativa(archivo)
    e.setdefault("otros_sitios", []).append(rel)
    guardar_estado(e)
    cfg = cfg or cargar_config()
    linea = "%s | Claude (modo auto) | Corrección en otro sitio: %s. Fallaba: %s. Cambio: %s | Modo auto\n" % (time.strftime("%Y-%m-%d"), rel, fallaba, cambio)
    ruta = os.path.join(RAIZ, cfg.get("registro", ".brain/decisions.log"))
    with open(ruta, "a", encoding="utf-8", newline="") as f:
        if os.path.getsize(ruta) and not _termina_en_salto(ruta):
            f.write("\n")
        f.write(linea)
    return "Anotado en el registro; ya puedes corregir %s." % rel


def _termina_en_salto(ruta):
    with open(ruta, "rb") as f:
        f.seek(-1, os.SEEK_END)
        return f.read(1) == b"\n"


def base_prueba(accion, a=None):
    a = a or ajustes(cargar_config())
    base, prueba, origen = (os.path.join(RAIZ, a[k]) for k in ("base", "prueba", "origen"))
    os.makedirs(os.path.dirname(base), exist_ok=True)
    if accion == "crear":
        if os.path.exists(base):
            return "La copia fija ya existe (no se sobrescribe): %s" % a["base"]
        shutil.copyfile(origen, base)
        shutil.copyfile(base, prueba)
        return "Copia fija creada en %s y copia de trabajo en %s." % (a["base"], a["prueba"])
    if accion == "restaurar":
        if not os.path.exists(base):
            return "Aún no hay copia fija: primero «base-prueba crear»."
        shutil.copyfile(base, prueba)
        return "Base de prueba restaurada desde la copia fija."
    return "Uso: modo_auto.py base-prueba crear|restaurar"


def estado_texto():
    e = leer_estado()
    if not e.get("activo"):
        return "Modo normal (modo auto apagado)."
    return "Modo auto ACTIVO · cola: %s · parado: %s · fallos: %s · otros sitios corregidos: %s" % (
        ", ".join(e.get("cola") or []) or "vacía", e.get("parado") or "no", e.get("fallos") or {}, e.get("otros_sitios") or [])


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        return hook()
    c, resto = sys.argv[1], sys.argv[2:]
    if c == "activar":
        print(activar(resto))
    elif c == "desactivar":
        print(desactivar())
    elif c == "estado":
        print(estado_texto())
    elif c == "fallo" and resto:
        print(registrar_fallo(resto[0]))
    elif c == "resuelto" and resto:
        print(resuelto(resto[0]))
    elif c == "continuar":
        print(continuar())
    elif c == "hecha":
        print(hecha())
    elif c == "otro-sitio" and len(resto) >= 3:
        print(otro_sitio(*resto[:3]))
    elif c == "base-prueba":
        print(base_prueba(resto[0] if resto else ""))
    else:
        print(__doc__)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
