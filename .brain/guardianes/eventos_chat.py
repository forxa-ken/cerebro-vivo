#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardián 14 de Cerebro Vivo · guardián con memoria del chat (spec 027).

Se ejecuta como hook `PreToolUse` de Claude Code (antes de cada orden de terminal y de cada edición). Recuerda, por chat,
qué librerías se instalaron (`pip install`, `npm install`…) y, al ver `git push`, hace él mismo la revisión de las
nuevas con `librerias.py` (OSV.dev): limpio → deja pasar sin molestar; vulnerabilidad conocida → detiene el `git push`
(exit 2) y lo explica; sin red → no bloquea y lo recuerda en el siguiente `git push`. No depende de la IA ni de Darwin.
Revisa Python (PyPI), npm, cargo y go (spec 036; lee la versión del archivo de bloqueo del proyecto); de otros avisa una vez.
Para seguir tras un bloqueo, con el visto bueno de Darwin: `python eventos_chat.py permitir "motivo"` (queda en el registro).
Estado en `eventos_chat_estado.json` (ignorado por Git). Ante cualquier fallo propio deja pasar. Solo librería estándar.
Ajustes: guardianes.json (`eventos_chat_activo`, `eventos_chat_comandos`, `eventos_chat_bloquear`, `eventos_chat_sin_red_bloquear`)."""

import argparse
import datetime
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, AQUI)
from textos import t, tp  # noqa: E402  (spec 024: mensajes en es/en)
import librerias  # noqa: E402
ESTADO = os.path.join(AQUI, "eventos_chat_estado.json")
MAX_CHATS = 20
COMANDOS = ["pip install", "pip3 install", "uv add", "uv pip install", "poetry add", "npm install", "npm i", "npm add",
            "yarn add", "pnpm add", "cargo add", "go get"]
ECOSISTEMA = {"pip": "pypi", "pip3": "pypi", "uv": "pypi", "poetry": "pypi", "npm": "npm", "yarn": "npm", "pnpm": "npm",
              "cargo": "cargo", "go": "go"}
CON_VALOR = {"-r", "--requirement", "-c", "--constraint", "-e", "--editable", "-i", "--index-url", "--extra-index-url",
             "-t", "--target", "--prefix", "--python", "-f", "--find-links"}


def cargar_config():
    with open(os.path.join(AQUI, "guardianes.json"), encoding="utf-8") as f:
        return json.load(f)


def activo(cfg):
    return bool(cfg.get("eventos_chat_activo", True))


def leer_estado():
    try:
        with open(ESTADO, encoding="utf-8") as f:
            datos = json.load(f)
        return datos if isinstance(datos, dict) else {}
    except Exception:
        return {}


def guardar_estado(estado):
    chats = estado.get("chats", {})
    for viejo in list(chats)[:-MAX_CHATS]:
        del chats[viejo]
    with open(ESTADO, "w", encoding="utf-8") as f:
        json.dump(estado, f, ensure_ascii=False)


def trozos(comando):
    """Trozos de una orden de terminal separados por &&, ||, ;, | o salto de línea, ya en palabras."""
    res = []
    for parte in re.split(r"&&|\|\||;|\||\n", comando or ""):
        try:
            palabras = shlex.split(parte, posix=False)
        except ValueError:
            palabras = parte.split()
        palabras = [p.strip("\"'") for p in palabras]
        if palabras:
            res.append(palabras)
    return res


def _contiene(palabras, secuencia):
    n = len(secuencia)
    for i in range(len(palabras) - n + 1):
        if [p.lower() for p in palabras[i:i + n]] == secuencia:
            return i + n
    return -1


def _nombre(token, eco):
    if eco == "npm":
        m = re.match(r"(@[^/@\s]+/[^@\s]+|[^@\s]+)", token)
    elif eco == "go":
        m = re.match(r"([^@\s]+)", token)
    else:
        m = re.match(r"([A-Za-z0-9][A-Za-z0-9._-]*)", token)
    return re.sub(r"[-_.]+", "-", m.group(1)).lower() if (m and eco == "pypi") else (m.group(1) if m else "")


def instalaciones(comando, cfg):
    """[(ecosistema, [nombres], archivo_de_requisitos o '')] de las instalaciones que hay en la orden."""
    res = []
    lista = cfg.get("eventos_chat_comandos") or COMANDOS
    for palabras in trozos(comando):
        for cmd in lista:
            sec = cmd.lower().split()
            fin = _contiene(palabras, sec)
            if fin < 0:
                continue
            eco = ECOSISTEMA.get(sec[0], "otro")
            nombres, requisitos, i = [], "", fin
            resto = palabras[fin:]
            while i - fin < len(resto):
                tok = resto[i - fin]
                if tok in ("-r", "--requirement") and i - fin + 1 < len(resto):
                    requisitos = resto[i - fin + 1]
                    i += 2
                    continue
                if tok in CON_VALOR:
                    i += 2
                    continue
                if tok.startswith("-") or re.match(r"^(\.|/|[A-Za-z]:\\|https?:|git\+|[0-9]*[<>&])", tok):  # spec 030: `2>&1` no es una librería
                    i += 1
                    continue
                n = _nombre(tok, eco)
                if n:
                    nombres.append(n)
                i += 1
            if nombres or requisitos:
                res.append((eco, nombres, requisitos))
            break
    return res


FIJADA = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)(?:\[[^\]]*\])?==([0-9][A-Za-z0-9._+!-]*)$")


def versiones_fijadas(comando, cfg):
    """{nombre: versión} de lo que la orden fija con `nombre==versión` (solo PyPI). Spec 029."""
    res = {}
    for palabras in trozos(comando):
        for cmd in (cfg.get("eventos_chat_comandos") or COMANDOS):
            sec = cmd.lower().split()
            fin = _contiene(palabras, sec)
            if fin < 0:
                continue
            if ECOSISTEMA.get(sec[0], "otro") == "pypi":
                for tok in palabras[fin:]:
                    m = FIJADA.match(tok)
                    if m:
                        res[re.sub(r"[-_.]+", "-", m.group(1)).lower()] = m.group(2)
            break
    return res


def python_del_entorno(raiz):
    """Ruta del Python del entorno virtual del proyecto (`.venv` o `venv`), o '' si no hay. Spec 029."""
    for carpeta in (".venv", "venv"):
        for rel in (("Scripts", "python.exe"), ("bin", "python")):
            ruta = os.path.join(raiz, carpeta, *rel)
            if os.path.isfile(ruta):
                return ruta
    return ""


def versiones_en_entorno(python, nombres, timeout=5):
    """{nombre: versión} de lo que está instalado en ese Python (una sola llamada). Ante cualquier fallo, {}."""
    codigo = ("import sys, json\nfrom importlib.metadata import version\nr = {}\nfor n in sys.argv[1:]:\n"
              "    try:\n        r[n] = version(n)\n    except Exception:\n        pass\nprint(json.dumps(r))")
    try:
        r = subprocess.run([python, "-c", codigo] + list(nombres), capture_output=True, text=True, timeout=timeout)
        datos = json.loads(r.stdout) if r.returncode == 0 else {}
        return datos if isinstance(datos, dict) else {}
    except Exception:
        return {}


def versiones_a_revisar(nombres, chat, raiz):
    """[(nombre, versión)] con lo que de verdad hay que consultar. Orden de confianza (spec 029):
    1) lo instalado en el `.venv` del proyecto; 2) la versión fijada en el propio comando; 3) el Python que ejecuta el hook."""
    python = python_del_entorno(raiz)
    del_venv = versiones_en_entorno(python, nombres) if python else {}
    fijadas = chat.get("versiones") or {}
    res = []
    for n in nombres:
        v = del_venv.get(n) or fijadas.get(n) or librerias.version_instalada(n, "")
        if v:
            res.append((n, v))
    return res


def es_push(comando):
    for palabras in trozos(comando):
        bajas = [p.lower() for p in palabras]
        if bajas and bajas[0] == "git" and "push" in bajas[1:5]:
            return True
    return False


def huella_requisitos(raiz, cfg):
    ruta = os.path.join(raiz, (cfg.get("librerias") or {}).get("requisitos", "requirements.txt"))
    try:
        with open(ruta, "rb") as f:
            return hashlib.sha1(f.read().replace(b"\r\n", b"\n")).hexdigest()
    except Exception:
        return ""


def del_chat(estado, sesion):
    chats = estado.setdefault("chats", {})
    chat = chats.pop(sesion, None) or {}
    chats[sesion] = chat  # el último usado va al final
    chat.setdefault("pendientes", [])   # [nombre] de PyPI instalados y sin revisar
    chat.setdefault("pendientes_eco", [])  # ["npm:nombre", "cargo:nombre", "go:módulo"] instalados y sin revisar (spec 036)
    chat.setdefault("otros", [])        # ["eco:nombre"] que no se pueden revisar solos
    chat.setdefault("avisados_otros", [])
    return chat


def recordar(chat, comando, raiz, cfg):
    """Apunta lo que instala la orden. Devuelve True si había alguna instalación."""
    hubo = False
    for eco, nombres, requisitos in instalaciones(comando, cfg):
        hubo = True
        if eco == "pypi":
            if requisitos:
                try:
                    nombres = nombres + [n for n, _ in librerias.leer_requisitos(os.path.join(raiz, requisitos))]
                except Exception:
                    pass
            for n in nombres:
                if n not in chat["pendientes"]:
                    chat["pendientes"].append(n)
            chat.setdefault("versiones", {}).update(versiones_fijadas(comando, cfg))
        elif eco in librerias.ECO_OSV:
            for n in nombres:
                clave = "%s:%s" % (eco, n)
                if clave not in chat["pendientes_eco"]:
                    chat["pendientes_eco"].append(clave)
        else:
            for n in nombres:
                clave = "%s:%s" % (eco, n)
                if clave not in chat["otros"]:
                    chat["otros"].append(clave)
    return hubo


def olvidar_no_instaladas(chat, raiz):
    """Spec 030: quita del recuerdo del chat lo que ya no está instalado (se desinstaló, o la orden se detuvo antes de
    ejecutarse). Solo si hay `.venv` y la librería no está ni en él ni en el Python del hook; se llama ANTES de apuntar
    la orden actual, para no olvidar lo que esa misma orden instala."""
    python = python_del_entorno(raiz)
    if not python or not chat["pendientes"]:
        return
    en_venv = versiones_en_entorno(python, chat["pendientes"])
    ausentes = [n for n in chat["pendientes"] if not en_venv.get(n) and not librerias.version_instalada(n, "")]
    if not ausentes:
        return
    chat["pendientes"] = [n for n in chat["pendientes"] if n not in ausentes]
    for n in ausentes:
        (chat.get("versiones") or {}).pop(n, None)
    chat["bloqueados"] = [b for b in chat.get("bloqueados", []) if b.split("==")[0] not in ausentes]
    if not chat["bloqueados"]:
        chat.pop("bloqueados", None)


def pendientes_por_requisitos(chat, raiz, cfg):
    """Si requirements.txt cambió desde que se vio por primera vez en este chat, sus librerías cuentan como nuevas."""
    actual = huella_requisitos(raiz, cfg)
    base = chat.get("requisitos")
    if base is None:
        chat["requisitos"] = actual
        return
    if actual and actual != base:
        try:
            ruta = os.path.join(raiz, (cfg.get("librerias") or {}).get("requisitos", "requirements.txt"))
            for n, _ in librerias.leer_requisitos(ruta):
                if n not in chat["pendientes"]:
                    chat["pendientes"].append(n)
        except Exception:
            pass
        chat["requisitos"] = actual


def _permitidos(estado):
    return set(estado.get("permitidos", []))


def revisar_push(estado, chat, cfg, raiz, http=None):
    """Decide ante un `git push`. Devuelve (exit, texto): 0 con texto vacío = dejar pasar sin decir nada."""
    a = librerias.ajustes(cfg)
    a["timeout"] = min(a.get("timeout", 7), 6)
    avisos = []
    nuevos_otros = [o for o in chat["otros"] if o not in chat["avisados_otros"]]
    if nuevos_otros:
        avisos.append(tp("eventos_chat_no_revisable") % ", ".join(nuevos_otros))
        chat["avisados_otros"] += nuevos_otros
    nombres = [n for n in chat["pendientes"]]
    if not nombres and not chat["pendientes_eco"]:
        return 0, " ".join(avisos)
    pedidos = versiones_a_revisar(nombres, chat, raiz) if nombres else []
    sin_version = [n for n in nombres if n not in {p[0] for p in pedidos}]
    for clave in list(chat["pendientes_eco"]):  # spec 036: la versión sale del archivo de bloqueo del proyecto
        eco, n = clave.split(":", 1)
        v = librerias.versiones_del_proyecto(raiz, eco, a).get(n)
        if v:
            pedidos.append((n, v, eco))
        else:
            sin_version.append(clave)
    if sin_version:  # spec 029: no dejar pasar en silencio lo que no se pudo mirar (antes ocultaba los .venv)
        avisos.append(tp("eventos_chat_sin_version") % ", ".join(sin_version))
        chat["pendientes"] = [n for n in chat["pendientes"] if n not in sin_version]  # se avisa una vez
        chat["pendientes_eco"] = [n for n in chat["pendientes_eco"] if n not in sin_version]
    if not pedidos:
        chat["pendientes"] = []
        chat["pendientes_eco"] = []
        return 0, " ".join(avisos)
    est = librerias.consultar(pedidos, a, http, con_pypi=False)
    if est is None:
        if cfg.get("eventos_chat_sin_red_bloquear", False):
            return 2, " ".join(avisos + [tp("eventos_chat_sin_red_bloqueo") % ", ".join(p[0] for p in pedidos)])
        return 0, " ".join(avisos + [tp("eventos_chat_sin_red") % ", ".join(p[0] for p in pedidos)])
    permitidos = _permitidos(estado)
    ignorados = {i.get("id") for i in a.get("ignorar", [])}
    problemas, limpios = [], []
    for p in est["paquetes"]:
        vulns = [v for v in p["vulns"] if v["id"] not in ignorados]
        etiqueta = "%s:%s" % (p["eco"], p["nombre"]) if p.get("eco") else p["nombre"]  # npm:x, cargo:x, go:x; Python sin prefijo
        clave = "%s==%s" % (etiqueta, p["version"])
        if vulns and clave not in permitidos:
            fix = next((v["corregida"] for v in vulns if v.get("corregida")), "")
            problemas.append(tp("eventos_chat_vuln_linea") % (etiqueta, p["version"], len(vulns),
                                                              tp("eventos_chat_corregida") % fix if fix else ""))
        else:
            limpios.append(etiqueta)
    if problemas:
        chat["bloqueados"] = [("%s:%s" % (p["eco"], p["nombre"]) if p.get("eco") else p["nombre"]) + "==" + p["version"] for p in est["paquetes"]
                              if any(v["id"] not in ignorados for v in p["vulns"])
                              and ("%s:%s==%s" % (p["eco"], p["nombre"], p["version"]) if p.get("eco") else "%s==%s" % (p["nombre"], p["version"])) not in permitidos]
        chat["pendientes"] = [n for n in chat["pendientes"] if n not in limpios]
        chat["pendientes_eco"] = [n for n in chat["pendientes_eco"] if n not in limpios]
        if not cfg.get("eventos_chat_bloquear", True):
            return 0, " ".join(avisos + [tp("eventos_chat_aviso_vuln") % "; ".join(problemas)])
        return 2, " ".join(avisos + [tp("eventos_chat_bloqueo") % "; ".join(problemas)])
    chat["pendientes"] = []
    chat["pendientes_eco"] = []
    chat.pop("bloqueados", None)
    return 0, " ".join(avisos)


def procesar(datos, cfg, raiz=RAIZ, http=None):
    """Núcleo del hook. Devuelve (exit, texto). Cualquier excepción la atrapa `main` y deja pasar."""
    if not activo(cfg):
        return 0, ""
    sesion = str(datos.get("session_id") or "sin-sesion")
    herramienta = str(datos.get("tool_name") or "")
    comando = str((datos.get("tool_input") or {}).get("command") or "")
    estado = leer_estado()
    chat = del_chat(estado, sesion)
    pendientes_por_requisitos(chat, raiz, cfg)
    salida = (0, "")
    if herramienta in ("Bash", "PowerShell") and comando:
        olvidar_no_instaladas(chat, raiz)
        recordar(chat, comando, raiz, cfg)
        if es_push(comando):
            salida = revisar_push(estado, chat, cfg, raiz, http)
    guardar_estado(estado)
    return salida


def permitir(motivo, raiz=RAIZ, cfg=None):
    """Autoriza el `git push` con las librerías que el guardián bloqueó, y lo anota en el registro. Devuelve el texto de respuesta."""
    cfg = cfg or cargar_config()
    estado = leer_estado()
    bloqueadas = sorted({b for c in estado.get("chats", {}).values() for b in c.get("bloqueados", [])})
    if not bloqueadas:
        return t(cfg, "eventos_chat_nada_que_permitir")
    estado["permitidos"] = sorted(_permitidos(estado) | set(bloqueadas))
    for c in estado.get("chats", {}).values():
        c.pop("bloqueados", None)
    guardar_estado(estado)
    linea = "%s | guardian | Guardián (eventos del chat) | %s | %s" % (
        datetime.date.today().isoformat(), t(cfg, "eventos_chat_registro", ", ".join(bloqueadas), motivo), t(cfg, "carril_corto"))
    try:
        with open(os.path.join(raiz, cfg.get("registro", ".brain/decisions.log")), "a", encoding="utf-8", newline="") as f:
            f.write(linea + "\n")
    except Exception:
        pass
    return t(cfg, "eventos_chat_permitido", ", ".join(bloqueadas))


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) > 1:  # uso a mano: `permitir "motivo"` o --help
        cfg = cargar_config()
        ap = argparse.ArgumentParser(description=t(cfg, "eventos_chat_descripcion"))
        ap.add_argument("accion", choices=["permitir"], help=t(cfg, "ayuda_eventos_chat_accion"))
        ap.add_argument("motivo", help=t(cfg, "ayuda_eventos_chat_motivo"))
        a = ap.parse_args()
        print(permitir(a.motivo, RAIZ, cfg))
        return 0
    try:
        datos = json.loads(sys.stdin.read() or "{}")
        codigo, texto = procesar(datos, cargar_config())
    except Exception:
        return 0  # el guardián nunca debe romper el trabajo
    if codigo == 2:
        sys.stderr.write(texto + "\n")
        return 2
    if texto:
        sys.stdout.buffer.write(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": texto}},
                                           ensure_ascii=False).encode("utf-8"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
