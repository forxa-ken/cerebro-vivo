#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardián 4 de Cerebro Vivo · resumen de arranque (spec 047).

Se ejecuta como aviso de «inicio de sesión» de Claude Code (hook SessionStart): lo que imprime
llega a la IA como contexto. Resume el estado REAL del proyecto (pendientes, commits sin subir,
cambios sin commitear, fichas de decisión a revisar) para que la IA no dependa de leer bien.
También contiene fichas_a_revisar(), que usa el test de índices (guardián 5).
Solo lectura, solo librería estándar. Si algo falla, calla."""

import datetime
import fnmatch
import json
import os
import re
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))


def cargar_config():
    with open(os.path.join(AQUI, "guardianes.json"), encoding="utf-8") as f:
        return json.load(f)


def git(raiz, *args):
    return subprocess.run(["git", "-c", "core.quotepath=false"] + list(args), cwd=raiz,
                          capture_output=True, text=True, encoding="utf-8", timeout=15).stdout


def contar_pendientes(texto):
    """{sección: nº de puntos} de pendientes.md (un punto = línea que empieza por «- **»)."""
    secciones, actual = {}, None
    for linea in texto.splitlines():
        if linea.startswith("## "):
            actual = linea[3:].strip()
            secciones[actual] = 0
        elif linea.startswith("- **") and actual is not None:
            secciones[actual] += 1
    return {k: v for k, v in secciones.items() if v}


def fichas_a_revisar(raiz):
    """Fichas de decisión cuyos archivos citados cambiaron en Git DESPUÉS de su fecha (o de su
    última revisión). Una ficha declara `- **Archivos:** `a.py`, `b.py`` y, al revisarla,
    `- **Revisada:** AAAA-MM-DD`. Devuelve [(ficha, archivo, fecha_del_cambio)]."""
    carpeta = os.path.join(raiz, ".brain", "decisions")
    pendientes = []
    for nombre in sorted(os.listdir(carpeta)):
        if not re.match(r"D-\d{3}-.*\.md$", nombre):
            continue
        with open(os.path.join(carpeta, nombre), encoding="utf-8") as f:
            txt = f.read()
        arch = re.search(r"^- \*\*Archivos:\*\*\s*(.+)$", txt, flags=re.M)
        if not arch:
            continue
        fechas = re.findall(r"^- \*\*(?:Fecha|Revisada):\*\*\s*(\d{4}-\d{2}-\d{2})", txt, flags=re.M)
        if not fechas:
            continue
        desde = max(fechas)
        for ruta in re.findall(r"`([^`]+)`", arch.group(1)):
            cambio = git(raiz, "log", "-1", "--format=%cs", "--", ruta).strip()
            if cambio and cambio > desde:
                pendientes.append((nombre, ruta, cambio))
    return pendientes


TRASPASO_RUTA = os.path.join(".brain", "traspaso.md")
TRASPASO_CARPETA = os.path.join(".brain", "archive", "traspasos")
TRASPASO_MAX_DIAS = 3
TRASPASO_MAX_CARACTERES = 6000


def leer_traspaso(raiz, ahora=None):
    """Spec 078: líneas con el traspaso del chat anterior (`.brain/traspaso.md`), o [] si no hay,
    está vacío o tiene más de TRASPASO_MAX_DIAS días."""
    ruta = os.path.join(raiz, TRASPASO_RUTA)
    try:
        if not os.path.isfile(ruta):
            return []
        ahora = ahora if ahora is not None else datetime.datetime.now().timestamp()
        if ahora - os.path.getmtime(ruta) > TRASPASO_MAX_DIAS * 86400:
            return []
        with open(ruta, encoding="utf-8") as f:
            texto = f.read().strip()
        if not texto:
            return []
        if len(texto) > TRASPASO_MAX_CARACTERES:
            texto = texto[:TRASPASO_MAX_CARACTERES] + "\n[…recortado; el original queda archivado]"
        return ["- TRASPASO DEL CHAT ANTERIOR (lo hablado justo antes; resúmeselo a Darwin y sigue desde ahí):", texto]
    except Exception:
        return []


def archivar_traspaso(raiz):
    """Mueve (no borra) el traspaso ya mostrado a archive/traspasos/ para que no se repita en el chat siguiente."""
    ruta = os.path.join(raiz, TRASPASO_RUTA)
    try:
        if not os.path.isfile(ruta):
            return None
        carpeta = os.path.join(raiz, TRASPASO_CARPETA)
        os.makedirs(carpeta, exist_ok=True)
        destino = os.path.join(carpeta, datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S") + ".md")
        shutil.move(ruta, destino)
        return destino
    except Exception:
        return None


NOTAS_CARPETA = os.path.join(".brain", "notas-chats")
NOTAS_ARCHIVO = os.path.join(".brain", "archive", "notas-chats")
NOTAS_MAX_DIAS = 3
NOTAS_MAX_CARACTERES = 4000


def _notas_pendientes(raiz):
    carpeta = os.path.join(raiz, NOTAS_CARPETA)
    try:
        return sorted(os.path.join(carpeta, n) for n in os.listdir(carpeta) if n.endswith(".md"))
    except Exception:
        return []


def leer_notas_chats(raiz, ahora=None):
    """Spec 080: líneas con las notas que dejaron los chats auxiliares (`.brain/notas-chats/*.md`).
    Las de más de NOTAS_MAX_DIAS días no se muestran (solo se archivan)."""
    ahora = ahora if ahora is not None else datetime.datetime.now().timestamp()
    textos = []
    for ruta in _notas_pendientes(raiz):
        try:
            if ahora - os.path.getmtime(ruta) > NOTAS_MAX_DIAS * 86400:
                continue
            with open(ruta, encoding="utf-8") as f:
                t = f.read().strip()
            if t:
                textos.append(t[:NOTAS_MAX_CARACTERES])
        except Exception:
            continue
    if not textos:
        return []
    return ["- NOTAS DE CHATS AUXILIARES (lo que hicieron otros chats mientras tanto; resúmeselo a Darwin):"] + textos


def archivar_notas_chats(raiz):
    """Mueve (no borra) las notas ya mostradas a archive/notas-chats/ para que no se repitan."""
    movidas = []
    try:
        for ruta in _notas_pendientes(raiz):
            carpeta = os.path.join(raiz, NOTAS_ARCHIVO)
            os.makedirs(carpeta, exist_ok=True)
            destino = os.path.join(carpeta, os.path.basename(ruta))
            if os.path.exists(destino):
                destino = os.path.join(carpeta, datetime.datetime.now().strftime("%H%M%S-") + os.path.basename(ruta))
            shutil.move(ruta, destino)
            movidas.append(destino)
    except Exception:
        pass
    return movidas


PLUGINS_INSTALADOS = os.path.join(os.path.expanduser("~"), ".claude", "plugins", "installed_plugins.json")


def plugins_que_faltan(cfg, ruta=None):
    """Spec 085: `plugins_requeridos` (nombre@marketplace) de guardianes.json que Claude no tiene
    instalados. Si no hay lista, o el archivo de Claude no se puede leer, no avisa (lista vacía)."""
    requeridos = cfg.get("plugins_requeridos") or []
    try:
        with open(ruta or PLUGINS_INSTALADOS, encoding="utf-8") as f:
            instalados = json.load(f).get("plugins", {})
    except Exception:
        return []
    return [p for p in requeridos if not instalados.get(p)]


def resumen(raiz, cfg):
    lineas = ["🐺 Cerebro Vivo · estado real al abrir el chat:"]
    try:
        ruta_p = os.path.join(raiz, cfg["pendientes"])
        with open(ruta_p, encoding="utf-8") as f:
            cuentas = contar_pendientes(f.read())
        tam = os.path.getsize(ruta_p)
        detalle = ", ".join("%s: %d" % (k, v) for k, v in cuentas.items())
        lineas.append("- Pendientes: %s (%d de %d bytes)." % (detalle or "vacío", tam, cfg["tope_pendientes_bytes"]))
    except Exception:
        pass
    try:
        sin_subir = git(raiz, "rev-list", "--count", "@{u}..HEAD").strip()
        if sin_subir.isdigit():
            lineas.append("- Commits sin subir a GitHub: %s (no subir sin orden de Darwin)." % sin_subir)
    except Exception:
        pass
    try:
        sucios = []
        for l in git(raiz, "status", "--porcelain").splitlines():
            ruta = l[3:].strip().strip('"').replace("\\", "/")
            if not any(fnmatch.fnmatch(ruta, p) for p in cfg["ignorar_cambios"]):
                sucios.append(ruta)
        if sucios:
            lineas.append("- Sin commitear (del proyecto): %s." % ", ".join(sucios[:5]) + (" …" if len(sucios) > 5 else ""))
    except Exception:
        pass
    try:
        with open(os.path.join(raiz, cfg["registro"]), encoding="utf-8") as f:
            ultima = [l for l in f.read().splitlines() if l.strip()][-1]
        lineas.append("- Última línea del registro: %s" % ultima[:110])
    except Exception:
        pass
    try:
        rev = fichas_a_revisar(raiz)
        if rev:
            lineas.append("- Fichas de decisión a revisar (sus archivos cambiaron después): %s." %
                          ", ".join("%s (%s)" % (n[:5], r) for n, r, _ in rev[:4]))
    except Exception:
        pass
    try:  # spec 048: poda de memoria (mueve lo terminado a archivo/; se apaga con poda_activa)
        import importlib.util
        espec = importlib.util.spec_from_file_location("poda", os.path.join(AQUI, "poda.py"))
        poda = importlib.util.module_from_spec(espec)
        espec.loader.exec_module(poda)
        lineas += poda.podar_y_resumir(raiz, cfg)
    except Exception:
        pass
    try:  # spec 049: análisis AST (SQL inseguro, límites y reglas; se apaga con analisis_activo)
        import importlib.util
        espec = importlib.util.spec_from_file_location("analisis", os.path.join(AQUI, "analisis.py"))
        analisis = importlib.util.module_from_spec(espec)
        espec.loader.exec_module(analisis)
        lineas += analisis.resumen(raiz, cfg)
    except Exception:
        pass
    try:  # spec 050: salud de la base de datos (integridad y triggers; se apaga con base_datos_activo)
        import importlib.util
        espec = importlib.util.spec_from_file_location("base_datos", os.path.join(AQUI, "base_datos.py"))
        base_datos = importlib.util.module_from_spec(espec)
        espec.loader.exec_module(base_datos)
        lineas += base_datos.resumen(raiz, cfg)
    except Exception:
        pass
    try:  # spec 051: secretos (patrones, archivos secretos ignorados, revisión periódica del historial)
        import importlib.util
        espec = importlib.util.spec_from_file_location("secretos", os.path.join(AQUI, "secretos.py"))
        secretos = importlib.util.module_from_spec(espec)
        espec.loader.exec_module(secretos)
        lineas += secretos.resumen(raiz, cfg)
    except Exception:
        pass
    try:  # spec 052: librerías (solo lee el estado guardado; el chequeo con red es librerias.py)
        import importlib.util
        espec = importlib.util.spec_from_file_location("librerias", os.path.join(AQUI, "librerias.py"))
        librerias = importlib.util.module_from_spec(espec)
        espec.loader.exec_module(librerias)
        lineas += librerias.resumen(raiz, cfg)
    except Exception:
        pass
    try:  # spec 053: memoria de pruebas (línea solo si hay hallazgos abiertos)
        import importlib.util
        espec = importlib.util.spec_from_file_location("pruebas", os.path.join(AQUI, "pruebas.py"))
        pruebas = importlib.util.module_from_spec(espec)
        espec.loader.exec_module(pruebas)
        lineas += pruebas.resumen(raiz, cfg)
    except Exception:
        pass
    try:  # spec 085: plugins del meta-arnés que no están instalados
        falta = plugins_que_faltan(cfg)
        if falta:
            lineas.append("- Plugins sin instalar: %s (pasos en el README de github.com/forxa-ken/cerebro-vivo)." % ", ".join(falta))
    except Exception:
        pass
    if cfg.get("modo_ligero_activo"):  # spec 002: el resumen solo lleva lo que pide acción
        lineas = [l for l in lineas if not re.search(r"sin avisos|sin hallazgos|todo en orden|al día\.?$", l)]
    lineas += leer_traspaso(raiz)
    lineas += leer_notas_chats(raiz)
    lineas.append("- Lee CLAUDE.md, la constitución y pendientes.md; cierra cada tarea con su línea en el registro.")
    return "\n".join(lineas) + "\n"


# La app de escritorio no pinta el `systemMessage` del hook: se pide a la IA que lo muestre ella.
ORDEN_A_LA_IA = ("INSTRUCCIÓN para el asistente: en tu primera respuesta de esta sesión, dile a Darwin el resumen en "
                 "4-5 viñetas sin jerga (o en una línea si no hay nada que requiera acción) antes de seguir con lo que pida.\n")


def main():
    if "--manual" not in sys.argv and not sys.stdin.isatty():
        try:
            sys.stdin.read()  # el hook envía datos que no necesitamos
        except Exception:
            pass  # con `--manual` (Codex, Gemini, a mano) no se espera nada del teclado
    try:
        texto = resumen(RAIZ, cargar_config())
    except Exception:
        return 0
    if not os.environ.get("CEREBRO_NO_ARCHIVAR_TRASPASO"):  # la variable la usan los tests
        archivar_traspaso(RAIZ)
        archivar_notas_chats(RAIZ)
    # JSON (ASCII escapado, sin problemas de consola): `systemMessage` lo ve Darwin en pantalla y
    # `additionalContext` llega a la IA como contexto.
    salida = {"systemMessage": texto.rstrip("\n"),
              "hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": texto + ORDEN_A_LA_IA}}
    sys.stdout.write(json.dumps(salida))
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
