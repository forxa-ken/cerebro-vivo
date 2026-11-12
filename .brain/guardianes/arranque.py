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
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, AQUI)
from textos import t  # noqa: E402  (spec 024: mensajes en es/en)


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
TRASPASO_COMPLETO = os.path.join(".brain", "traspaso-completo.md")  # spec 026: historial entero, no se carga solo
TRASPASO_MAX_DIAS = 3
TRASPASO_MAX_CARACTERES = 6000


def leer_traspaso(raiz, ahora=None, lengua=None):
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
            texto = texto[:TRASPASO_MAX_CARACTERES] + t(lengua, "arranque_recortado")
        if os.path.isfile(os.path.join(raiz, TRASPASO_COMPLETO)):
            texto += "\n" + t(lengua, "arranque_traspaso_completo")
        return [t(lengua, "arranque_traspaso"), texto]
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
        sello = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
        destino = os.path.join(carpeta, sello + ".md")
        shutil.move(ruta, destino)
        completo = os.path.join(raiz, TRASPASO_COMPLETO)
        if os.path.isfile(completo):  # spec 026: el historial completo va al archivo con el mismo sello
            shutil.move(completo, os.path.join(carpeta, sello + "-completo.md"))
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


def leer_notas_chats(raiz, ahora=None, lengua=None):
    """Spec 080: líneas con las notas que dejaron los chats auxiliares (`.brain/notas-chats/*.md`).
    Las de más de NOTAS_MAX_DIAS días no se muestran (solo se archivan)."""
    ahora = ahora if ahora is not None else datetime.datetime.now().timestamp()
    textos = []
    for ruta in _notas_pendientes(raiz):
        try:
            if ahora - os.path.getmtime(ruta) > NOTAS_MAX_DIAS * 86400:
                continue
            with open(ruta, encoding="utf-8") as f:
                nota = f.read().strip()
            if nota:
                textos.append(nota[:NOTAS_MAX_CARACTERES])
        except Exception:
            continue
    if not textos:
        return []
    return [t(lengua, "arranque_notas")] + textos


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


NO_AVISAR_COMMIT = ["*.migrado", "__pycache__/*", "*.pyc", "*.bak*", ".brain/decisions.log", ".brain/traspaso.md", ".brain/traspaso-completo.md", ".brain/lecciones/*",
                    ".brain/archive/traspasos/*", ".brain/guardianes/*_estado.json"]  # spec 022: lo que se genera solo


def sin_commitear(raiz, cfg):
    """Spec 022: archivos sin commitear de todo el proyecto, salvo `no_avisar_commit`. En un movido cuenta el destino."""
    patrones = cfg.get("no_avisar_commit", NO_AVISAR_COMMIT)
    sucios = []
    for l in git(raiz, "status", "--porcelain", "--untracked-files=all").splitlines():
        ruta = l[3:].split(" -> ")[-1].strip().strip('"').replace("\\", "/")
        if not any(fnmatch.fnmatch(ruta, p) for p in patrones):
            sucios.append(ruta)
    return sucios


def texto_sin_commitear(sucios, lengua=None):
    return t(lengua, "arranque_sin_commitear", len(sucios), "" if len(sucios) == 1 else "s", ", ".join(sucios[:5]),
             "…" if len(sucios) > 5 else "")


def resumen(raiz, cfg):
    lineas = [t(cfg, "arranque_titulo")]
    if cfg.get("modo_fabrica"):  # spec 040: el modo fábrica se recuerda entre chats
        lineas.append(t(cfg, "arranque_modo_fabrica"))
    if cfg.get("modo_colaborativo"):  # spec 042: el modo colaborativo se recuerda entre chats
        lineas.append(t(cfg, "arranque_modo_colaborativo"))
    if str(cfg.get("auditor_externo", "general-y-spec")) in ("siempre", "no"):  # spec 044: ajuste no habitual del auditor
        lineas.append(t(cfg, "arranque_auditor_externo", cfg.get("auditor_externo")))
    try:  # spec 043: commits de proyectos hermanos sin portar (silencio si no hay hermanos o no son accesibles)
        import hermanos
        lineas.extend(hermanos.lineas_arranque(raiz, cfg))
    except Exception:
        pass
    try:
        ruta_p = os.path.join(raiz, cfg["pendientes"])
        with open(ruta_p, encoding="utf-8") as f:
            cuentas = contar_pendientes(f.read())
        tam = os.path.getsize(ruta_p)
        detalle = ", ".join("%s: %d" % (k, v) for k, v in cuentas.items())
        lineas.append(t(cfg, "arranque_pendientes", detalle or t(cfg, "arranque_vacio"), tam, cfg["tope_pendientes_bytes"]))
    except Exception:
        pass
    try:
        sin_subir = git(raiz, "rev-list", "--count", "@{u}..HEAD").strip()
        if sin_subir.isdigit():
            lineas.append(t(cfg, "arranque_sin_subir", sin_subir))
    except Exception:
        pass
    try:
        sucios = sin_commitear(raiz, cfg)
        if sucios:
            lineas.append(texto_sin_commitear(sucios, cfg))
    except Exception:
        pass
    try:
        with open(os.path.join(raiz, cfg["registro"]), encoding="utf-8") as f:
            ultima = [l for l in f.read().splitlines() if l.strip()][-1]
        lineas.append(t(cfg, "arranque_registro", ultima[:110]))
    except Exception:
        pass
    try:
        rev = fichas_a_revisar(raiz)
        if rev:
            lineas.append(t(cfg, "arranque_fichas",
                            ", ".join("%s (%s)" % (n[:5], r) for n, r, _ in rev[:4])))
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
    try:  # spec 016: salud de los índices de IA (línea solo si hace falta revisarlos; se apaga con revision_indices_activa)
        import importlib.util
        espec = importlib.util.spec_from_file_location("revisar_indices", os.path.join(AQUI, "revisar_indices.py"))
        revisar = importlib.util.module_from_spec(espec)
        espec.loader.exec_module(revisar)
        lineas += revisar.resumen(raiz, cfg)
    except Exception:
        pass
    try:  # spec 018: archivos de .brain/ que pasan de su tope (línea solo si hace falta trocearlos)
        import importlib.util
        espec = importlib.util.spec_from_file_location("archivos_gordos", os.path.join(AQUI, "archivos_gordos.py"))
        gordos = importlib.util.module_from_spec(espec)
        espec.loader.exec_module(gordos)
        lineas += gordos.resumen(raiz, cfg)
    except Exception:
        pass
    try:  # spec 019: hay una versión nueva del arnés (línea solo si la hay; se apaga con aviso_arnes_activo)
        if cfg.get("aviso_arnes_activo", True):
            import importlib.util
            espec = importlib.util.spec_from_file_location("actualizar_arnes", os.path.join(AQUI, "actualizar_arnes.py"))
            act = importlib.util.module_from_spec(espec)
            espec.loader.exec_module(act)
            v = act.version_disponible(raiz, cfg)
            if v:
                lineas.append(t(cfg, "arranque_arnes", *v))
    except Exception:
        pass
    try:  # spec 085: plugins del meta-arnés que no están instalados
        falta = plugins_que_faltan(cfg)
        if falta:
            lineas.append(t(cfg, "arranque_plugins", ", ".join(falta)))
    except Exception:
        pass
    if cfg.get("modo_ligero_activo"):  # spec 002: el resumen solo lleva lo que pide acción
        lineas = [l for l in lineas if not re.search(r"sin avisos|sin hallazgos|todo en orden|al día\.?$|no warnings|no findings|all in order|up to date\.?$", l)]
    try:  # spec 026: temas con lecciones aprendidas (línea solo si las hay)
        import lecciones
        temas = lecciones.resumen_temas(raiz)
        if temas and cfg.get("lecciones_activas", True):
            lineas.append(t(cfg, "arranque_lecciones", temas))
    except Exception:
        pass
    lineas += leer_traspaso(raiz, lengua=cfg)
    lineas += leer_notas_chats(raiz, lengua=cfg)
    lineas.append(t(cfg, "arranque_leer"))
    return "\n".join(lineas) + "\n"


# La app de escritorio no pinta el `systemMessage` del hook: se pide a la IA que lo muestre ella.
ORDEN_A_LA_IA = t("es", "arranque_orden")  # main() la pide en el idioma del proyecto


TIEMPOS = os.path.join(AQUI, "arranque_estado.json")
LENTO_SEG = 8  # pasados estos segundos se vuelca dónde está parado el arranque (el hook se corta a los 20)


def _guardar_tiempos(**nuevo):
    """Registro de tiempos del arranque (para ver por qué a veces pasa de 20 s). Nunca debe romper el hook."""
    try:
        try:
            with open(TIEMPOS, encoding="utf-8") as f:
                datos = json.load(f)
        except (OSError, ValueError):
            datos = {}
        datos.update(nuevo)
        with open(TIEMPOS, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=1)
    except Exception:
        pass


def _vigilar(hilo_principal):
    """Si el arranque sigue vivo pasados LENTO_SEG, guarda la pila del hilo principal (dónde está parado)."""
    try:
        import traceback
        marco = sys._current_frames().get(hilo_principal)
        pila = "".join(traceback.format_stack(marco))[-1500:] if marco else ""
        _guardar_tiempos(ultimo_lento={"fecha": datetime.datetime.now().isoformat(timespec="seconds"),
                                       "pila": pila})
    except Exception:
        pass


def main():
    import threading
    inicio = time.time()
    vigia = threading.Timer(LENTO_SEG, _vigilar, args=(threading.get_ident(),))
    vigia.daemon = True
    vigia.start()
    if "--manual" not in sys.argv and not sys.stdin.isatty():
        try:
            sys.stdin.read()  # el hook envía datos que no necesitamos
        except Exception:
            pass  # con `--manual` (Codex, Gemini, a mano) no se espera nada del teclado
    try:
        cfg = cargar_config()
        texto = resumen(RAIZ, cfg)
    except Exception:
        return 0
    finally:
        vigia.cancel()
        try:
            with open(TIEMPOS, encoding="utf-8") as f:
                ultimos = json.load(f).get("ultimos", [])
        except (OSError, ValueError):
            ultimos = []
        ultimos.append({"fecha": datetime.datetime.now().isoformat(timespec="seconds"),
                        "segundos": round(time.time() - inicio, 2)})
        _guardar_tiempos(ultimos=ultimos[-20:])
    if not os.environ.get("CEREBRO_NO_ARCHIVAR_TRASPASO"):  # la variable la usan los tests
        archivar_traspaso(RAIZ)
        archivar_notas_chats(RAIZ)
    # JSON (ASCII escapado, sin problemas de consola): `systemMessage` lo ve Darwin en pantalla y
    # `additionalContext` llega a la IA como contexto.
    salida = {"systemMessage": texto.rstrip("\n"),
              "hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": texto + t(cfg, "arranque_orden")}}
    sys.stdout.write(json.dumps(salida))
    sys.stdout.flush()
    return 0


if __name__ == "__main__":
    sys.exit(main())
