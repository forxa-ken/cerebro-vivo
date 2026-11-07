#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardián 8 de Cerebro Vivo · defensa dentro de la base de datos SQLite (spec 050).

Cuatro cosas, solo con la librería estándar y sin nada del proyecto dentro (los ajustes salen de
guardianes.json, clave `base_datos`):
  1. Copia consistente (API de copia de SQLite) antes de cambiar tablas, con rotación, y restauración
     solo con orden expresa.
  2. Revisión de salud en solo lectura: integrity_check, foreign_key_check y triggers que deben existir.
  3. Foto del esquema (`esquema_base.json`): tablas, columnas, índices y triggers. Se renueva solo con
     --renovar-esquema --ficha D-NNN (la ficha debe existir).
Solo avisa: no bloquea nada; si algo falla, calla.
Uso a mano: base_datos.py --ver | --copia | --restaurar ARCHIVO | --renovar-esquema --ficha D-NNN"""

import datetime
import glob
import json
import os
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, AQUI)
from textos import tp  # noqa: E402  (spec 024: mensajes en es/en)
FOTO = os.path.join(AQUI, "esquema_base.json")


def cargar_config():
    with open(os.path.join(AQUI, "guardianes.json"), encoding="utf-8") as f:
        return json.load(f)


def ajustes(cfg):
    a = dict(cfg.get("base_datos", {}))
    a["activo"] = bool(cfg.get("base_datos_activo", True))
    return a


def ruta_bd(raiz, a):
    return os.path.join(raiz, a.get("ruta", "base.db"))


def _solo_lectura(bd):
    return sqlite3.connect(Path(bd).resolve().as_uri() + "?mode=ro", uri=True)


# ─── Capa 1 · copia y restauración ──────────────────────────────────
def copias(carpeta, bd):
    return sorted(glob.glob(os.path.join(carpeta, Path(bd).stem + "-*.db")))


def copiar(bd, carpeta, motivo="manual", maximo=5):
    """Copia consistente de `bd` en `carpeta`; deja las últimas `maximo`. Devuelve la ruta o None."""
    if not os.path.exists(bd):
        return None
    os.makedirs(carpeta, exist_ok=True)
    sello = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    motivo = re.sub(r"[^a-z0-9-]+", "-", motivo.lower()).strip("-") or "copia"
    destino = os.path.join(carpeta, "%s-%s-%s.db" % (Path(bd).stem, sello, motivo))
    n = 1
    while os.path.exists(destino):
        n += 1
        destino = os.path.join(carpeta, "%s-%s-%s-%d.db" % (Path(bd).stem, sello, motivo, n))
    origen = _solo_lectura(bd)
    try:
        dest = sqlite3.connect(destino)
        try:
            origen.backup(dest)
        finally:
            dest.close()
    finally:
        origen.close()
    for vieja in copias(carpeta, bd)[:-max(1, int(maximo))]:
        try:
            os.remove(vieja)
        except OSError:
            pass
    return destino


def copia_previa(raiz, bd, motivo, carpeta=None):
    """Lo que llama la app antes de cambiar tablas. Nunca lanza ni bloquea. Devuelve la ruta o None."""
    try:
        cfg = cargar_config()
        a = ajustes(cfg)
        if not a["activo"]:
            return None
        carpeta = carpeta or os.path.join(raiz, a.get("copias_carpeta", "copias_bd"))
        return copiar(bd, carpeta, motivo, a.get("copias_max", 5))
    except Exception as e:
        print(tp("base_datos_basedatos_pudo_hacer") % e)
        return None


def restaurar(copia, bd, carpeta, maximo=5):
    """Vuelve atrás: comprueba la copia, guarda antes el estado actual y la vuelca sobre `bd`."""
    c = _solo_lectura(copia)
    try:
        estado = c.execute("PRAGMA integrity_check").fetchone()[0]
        if estado != "ok":
            raise ValueError(tp("base_datos_copia_esta_danada") % estado)
        guardada = copiar(bd, carpeta, "antes-de-restaurar", maximo)
        dest = sqlite3.connect(bd)
        try:
            c.backup(dest)
        finally:
            dest.close()
    finally:
        c.close()
    return guardada


# ─── Capa 2 · salud ─────────────────────────────────────────────────
def revisar(bd, triggers=()):
    """Lista de avisos (vacía = sana). Solo lectura. Base inexistente = sin avisos."""
    if not os.path.exists(bd):
        return []
    avisos = []
    try:
        con = _solo_lectura(bd)
    except Exception as e:
        return [tp("base_datos_pudo_abrir_base") % e]
    try:
        for fila in con.execute("PRAGMA integrity_check").fetchall():
            if fila[0] != "ok":
                avisos.append("integrity_check: %s" % fila[0])
                break
        fk = con.execute("PRAGMA foreign_key_check").fetchall()
        if fk:
            avisos.append(tp("base_datos_foreign_key_check") % (len(fk), fk[0][0]))
        puestos = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='trigger'")}
        for t in triggers:
            if t not in puestos:
                avisos.append(tp("base_datos_falta_trigger") % t)
    except Exception as e:
        avisos.append(tp("base_datos_revision_fallo") % e)
    finally:
        con.close()
    return avisos


def resumen(raiz, cfg):
    """Línea para el resumen de arranque. Calla si está apagado o si algo falla."""
    a = ajustes(cfg)
    if not a["activo"]:
        return []
    try:
        avisos = revisar(ruta_bd(raiz, a), a.get("triggers", []))
    except Exception:
        return []
    if not avisos:
        return [tp("base_datos_base_datos_sana")]
    return [tp("base_datos_base_datos_aviso") % (len(avisos), "; ".join(avisos[:2]))]


# ─── Capa 3 · foto del esquema ──────────────────────────────────────
def esquema(con):
    """Estructura de la base: {tablas:{t:[[col,tipo,obligatoria,defecto,pk],…]}, indices:[…], triggers:[…]}."""
    tablas = {}
    for (t,) in con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"):
        tablas[t] = [list(c[1:]) for c in con.execute("SELECT * FROM pragma_table_info(?)", (t,))]
    nombres = lambda tipo: [r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type=? AND name NOT LIKE 'sqlite_%' ORDER BY name", (tipo,))]
    return {"tablas": tablas, "indices": nombres("index"), "triggers": nombres("trigger")}


def comparar(actual, foto):
    """Diferencias entre el esquema actual y la foto (lista de textos; vacía = igual)."""
    d = []
    for t in sorted(set(actual["tablas"]) - set(foto["tablas"])):
        d.append(tp("base_datos_tabla_nueva_sin") % t)
    for t in sorted(set(foto["tablas"]) - set(actual["tablas"])):
        d.append(tp("base_datos_tabla_desaparecida") % t)
    for t in sorted(set(actual["tablas"]) & set(foto["tablas"])):
        a = {c[0]: c for c in actual["tablas"][t]}
        f = {c[0]: c for c in foto["tablas"][t]}
        for c in sorted(set(a) - set(f)):
            d.append(tp("base_datos_columna_nueva_sin") % (t, c))
        for c in sorted(set(f) - set(a)):
            d.append(tp("base_datos_columna_desaparecida") % (t, c))
        for c in sorted(set(a) & set(f)):
            if a[c] != f[c]:
                d.append(tp("base_datos_columna_cambiada") % (t, c))
    for clave, nombre in (("indices", "índice"), ("triggers", "trigger")):
        for x in sorted(set(actual[clave]) ^ set(foto[clave])):
            d.append("%s distinto: %s" % (nombre, x))
    return d


def cargar_foto(ruta=FOTO):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)


def guardar_foto(actual, ficha, raiz=RAIZ, ruta=FOTO):
    """Renueva la foto. Exige que exista la ficha D-NNN en .brain/decisions/."""
    if not re.fullmatch(r"D-\d{3}", ficha or "") or not glob.glob(os.path.join(raiz, ".brain", "decisions", ficha + "-*.md")):
        raise ValueError(tp("base_datos_ficha_existe_brain") % ficha)
    fichas = []
    if os.path.exists(ruta):
        fichas = cargar_foto(ruta).get("fichas", [])
    fichas.append({"ficha": ficha, "fecha": datetime.date.today().isoformat()})
    foto = dict(actual)
    foto["fichas"] = fichas
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        json.dump(foto, f, ensure_ascii=False, indent=1, sort_keys=True)


def esquema_actual_del_proyecto(raiz, a):
    """Construye el esquema con la función `modulo:funcion` indicada en `esquema_desde` (devuelve un dict)."""
    modulo, funcion = a["esquema_desde"].split(":")
    codigo = ("import sys, json; sys.argv[0] = 'unittest'; sys.path[:0] = [%r, %r];"
              "import %s as m; print('@@' + json.dumps(m.%s()))" % (raiz, os.path.join(raiz, "tests"), modulo, funcion))
    salida = subprocess.run([sys.executable, "-c", codigo], cwd=raiz, capture_output=True, text=True,
                            encoding="utf-8", timeout=120)
    for linea in salida.stdout.splitlines():
        if linea.startswith("@@"):
            return json.loads(linea[2:])
    raise RuntimeError(tp("base_datos_pudo_construir_esquema") % salida.stderr[-300:])


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:
            pass
    cfg = cargar_config()
    a = ajustes(cfg)
    bd = ruta_bd(RAIZ, a)
    carpeta = os.path.join(RAIZ, a.get("copias_carpeta", "copias_bd"))
    args = sys.argv[1:]
    if "--copia" in args:
        print(tp("base_datos_copia_hecha") % copiar(bd, carpeta, "manual", a.get("copias_max", 5)))
    elif "--restaurar" in args:
        i = args.index("--restaurar")
        if i + 1 >= len(args):
            sys.exit(tp("base_datos_falta_archivo_copia") % carpeta)
        guardada = restaurar(args[i + 1], bd, carpeta, a.get("copias_max", 5))
        print(tp("base_datos_restaurada_estado_anterior") % guardada)
    elif "--renovar-esquema" in args:
        if "--ficha" not in args or args.index("--ficha") + 1 >= len(args):
            sys.exit(tp("base_datos_falta_ficha_nnn"))
        guardar_foto(esquema_actual_del_proyecto(RAIZ, a), args[args.index("--ficha") + 1])
        print(tp("base_datos_foto_esquema_renovada") % os.path.relpath(FOTO, RAIZ))
    else:
        avisos = revisar(bd, a.get("triggers", []))
        print("\n".join("- " + x for x in avisos) if avisos else tp("base_datos_base_sana"))
        print(tp("base_datos_copias_guardadas") % (len(copias(carpeta, bd)), carpeta))


if __name__ == "__main__":
    main()
