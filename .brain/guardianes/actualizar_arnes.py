#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Actualizador del meta-arnés de Cerebro Vivo (spec 087).

Trae a un proyecto las mejoras del arnés (guardianes, skills, manual, kits, pruebas del método) desde el repo `cerebro-vivo`.

Uso dentro de un proyecto (este archivo vive en `.brain/guardianes/actualizar_arnes.py`):
    python .brain/guardianes/actualizar_arnes.py --simular          # solo muestra qué cambiaría
    python .brain/guardianes/actualizar_arnes.py                    # actualiza (copia de seguridad antes)
Uso desde el repo del arnés (`actualizar.py` en su raíz):
    python actualizar.py RUTA_DEL_PROYECTO [--simular]

Reglas: solo toca los archivos del manifiesto (`manifiesto.json`); si el proyecto modificó a mano uno de ellos NO lo pisa
(se lista; `--forzar RUTA` lo pisa tras guardar copia); nunca toca pendientes, specs, decisiones, registro ni `guardianes.json`
(si el arnés trae claves nuevas de configuración, las AÑADE sin tocar las que ya hay; anota `arnes_repo` si falta y es una
carpeta local; y añade a la ficha de skills `.brain/experiencia/indice.md` las filas de las skills nuevas). Spec 019: el arranque
avisa cuando el repo del arnés tiene una versión más nueva (`aviso_arnes`), y la skill `/actualizar` lo hace todo.
Spec 021: lo retirado del arnés (`retirados` del manifiesto) pasa a la copia de seguridad si no se modificó; cada archivo se escribe
de forma atómica; la versión se anota con lo que quedó sin aplicar (`sin_aplicar`); se comprueba la huella del manifiesto antes de
escribir; y un proyecto de nivel ligero o medio no recibe nada. Solo librería estándar."""

import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from textos import tp  # noqa: E402  (spec 024: mensajes en es/en)
RAIZ_PROPIA = os.path.abspath(os.path.join(AQUI, "..", ".."))
MANIFIESTO = "manifiesto.json"
REGISTRO = os.path.join(".brain", "arnes_instalado.json")
COPIAS = os.path.join(".brain", "copias_arnes")
INDICE_SKILLS = os.path.join(".brain", "experiencia", "indice.md")
TEXTO = (".py", ".md", ".txt")
DUENO_ORIGINAL = "Dar" + "win"  # partido a propósito: el kit cambia el nombre del dueño en los textos y no debe cambiar este


def _normalizar(datos, rel):
    """Bytes con saltos de línea unificados (en texto), para que Windows y Linux den la misma huella."""
    return datos.replace(b"\r\n", b"\n") if rel.lower().endswith(TEXTO + (".json", ".js", ".ts", ".tsx", ".html", ".bat", ".command", ".sh")) else datos


def huella(datos):
    return hashlib.sha256(datos).hexdigest()


def leer_bytes(ruta):
    with open(ruta, "rb") as f:
        return f.read()


def ruta_segura(base, rel):
    """Ruta absoluta de `rel` dentro de `base`, o None si intenta salirse de la carpeta."""
    base = os.path.abspath(base)
    ruta = os.path.abspath(os.path.join(base, rel))
    if os.path.isabs(rel) or not (ruta + os.sep).startswith(base + os.sep) or ruta == base:
        return None
    return ruta


def cargar_manifiesto(repo):
    with open(os.path.join(repo, MANIFIESTO), encoding="utf-8") as f:
        m = json.load(f)
    if not isinstance(m.get("archivos"), dict):
        raise ValueError(tp("actualizar_arnes_manifiesto_tiene_lista"))
    return m


def cargar_registro(proyecto):
    try:
        with open(os.path.join(proyecto, REGISTRO), encoding="utf-8") as f:
            r = json.load(f)
        return r if isinstance(r, dict) else {}
    except Exception:
        return {}


def escribir_atomico(ruta, datos):
    """Spec 021: escribe en un temporal de la misma carpeta y lo cambia de golpe; un corte deja el archivo viejo o el nuevo, entero."""
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    temporal = "%s.%d.tmp" % (ruta, os.getpid())
    try:
        with open(temporal, "wb") as f:
            f.write(datos)
            f.flush()
            os.fsync(f.fileno())
        if os.path.exists(ruta):
            shutil.copymode(ruta, temporal)  # instalar_kit.command debe seguir siendo ejecutable
        os.replace(temporal, ruta)
    except BaseException:
        try:
            os.remove(temporal)
        except OSError:
            pass
        raise


def guardar_registro(proyecto, registro):
    texto = json.dumps(registro, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    escribir_atomico(os.path.join(proyecto, REGISTRO), texto.encode("utf-8"))


def comprobar_manifiesto(repo, manifiesto=None):
    """Spec 021: cada archivo del manifiesto debe existir en el repo con su huella. Si no, ValueError antes de escribir nada."""
    manifiesto = manifiesto or cargar_manifiesto(repo)
    mal = []
    for rel, esperada in sorted(manifiesto["archivos"].items()):
        ruta = ruta_segura(repo, rel)
        if ruta is None:
            raise ValueError(tp("actualizar_arnes_ruta_permitida_manifiesto") % rel)
        if not os.path.isfile(ruta) or huella(_normalizar(leer_bytes(ruta), rel)) != esperada:
            mal.append(rel)
    if mal:
        raise ValueError(tp("actualizar_arnes_manifiesto_coincide_archivos") % (len(mal), ", ".join(mal[:5]) + (", …" if len(mal) > 5 else "")))


def esperado(repo, rel, dueno):
    """Contenido que debe tener `rel` en el proyecto: el del repo, con el nombre del dueño cambiado en los textos."""
    datos = _normalizar(leer_bytes(os.path.join(repo, rel)), rel)
    if dueno and dueno != DUENO_ORIGINAL and rel.lower().endswith(TEXTO):
        datos = datos.replace(DUENO_ORIGINAL.encode("utf-8"), dueno.encode("utf-8"))
    return datos


def claves_nuevas(repo, proyecto):
    """Claves de primer nivel que el arnés trae en `guardianes.json` y el proyecto aún no tiene (`completar_configuracion` las añade)."""
    try:
        with open(os.path.join(repo, ".brain", "guardianes", "guardianes.json"), encoding="utf-8") as f:
            del_arnes = json.load(f)
        with open(os.path.join(proyecto, ".brain", "guardianes", "guardianes.json"), encoding="utf-8") as f:
            del_proyecto = json.load(f)
    except Exception:
        return {}
    return {k: v for k, v in del_arnes.items() if k not in del_proyecto and k not in ("_ayuda", "arnes_repo")}


def completar_configuracion(repo, proyecto, simular=False):
    """Spec 019: añade a `guardianes.json` las claves que le faltan (nunca cambia una que ya existe) y anota `arnes_repo` si falta
    y el repo es una carpeta local. Devuelve las claves añadidas (o que se añadirían)."""
    ruta = os.path.join(proyecto, ".brain", "guardianes", "guardianes.json")
    try:
        with open(ruta, encoding="utf-8") as f:
            cfg = json.load(f)
    except Exception:
        return {}
    nuevas = dict(claves_nuevas(repo, proyecto))
    if not cfg.get("arnes_repo") and os.path.isabs(repo):
        nuevas["arnes_repo"] = os.path.abspath(repo)
    if nuevas and not simular:
        cfg.update(nuevas)
        escribir_atomico(ruta, (json.dumps(cfg, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    return nuevas


def completar_fichas_skills(repo, proyecto, simular=False, llegan=(), salen=()):
    """Spec 019: las skills que hay en `.claude/skills/` sin fila en `.brain/experiencia/indice.md` reciben la fila del arnés
    (una prueba lo exige). Devuelve los nombres añadidos (o que se añadirían). `llegan` y `salen`: skills que la simulación
    daría por copiadas o retiradas (spec 021)."""
    indice = os.path.join(proyecto, ".brain", "experiencia", "indice.md")
    fuente = os.path.join(repo, ".brain", "experiencia", "indice.md")
    carpeta = os.path.join(proyecto, ".claude", "skills")
    if not (os.path.isfile(indice) and os.path.isfile(fuente)):
        return []
    presentes = {n for n in (os.listdir(carpeta) if os.path.isdir(carpeta) else []) if os.path.isfile(os.path.join(carpeta, n, "SKILL.md"))}
    presentes = (presentes | set(llegan)) - set(salen)
    texto = leer_bytes(indice).decode("utf-8")
    hay = set(re.findall(r"skills/([^/]+)/SKILL\.md\)", texto))
    filas_arnes = leer_bytes(fuente).decode("utf-8").splitlines()
    anadir, nombres = [], []
    for n in sorted(presentes):
        if n in hay:
            continue
        fila = next((l for l in filas_arnes if "skills/%s/SKILL.md)" % n in l), None)
        if fila:
            anadir.append(fila)
            nombres.append(n)
    if anadir and not simular:
        fin = "\r\n" if "\r\n" in texto else "\n"
        if not texto.endswith(fin):
            texto += fin
        escribir_atomico(indice, (texto + fin.join(anadir) + fin).encode("utf-8"))
    return nombres


def _skill_de(rel):
    """Nombre de la skill si `rel` es su `SKILL.md` (de Claude o de Codex); si no, None."""
    m = re.fullmatch(r"\.(?:claude|agents)/skills/([^/]+)/SKILL\.md", rel)
    return m.group(1) if m else None


def filas_de_retiradas(manifiesto, proyecto, salen):
    """Spec 021: skills retiradas que ya no estarán en `.claude/skills/` y siguen con fila en el índice. `salen`: las que se van ahora."""
    indice = os.path.join(proyecto, INDICE_SKILLS)
    if not os.path.isfile(indice):
        return []
    texto = leer_bytes(indice).decode("utf-8")
    res = []
    for rel in manifiesto.get("retirados") or []:
        n = _skill_de(rel)
        if n and n not in res and "skills/%s/SKILL.md)" % n in texto and (n in salen or not os.path.isfile(os.path.join(proyecto, ".claude", "skills", n, "SKILL.md"))):
            res.append(n)
    return sorted(res)


def quitar_filas(proyecto, nombres):
    """Quita del índice de skills las filas de `nombres`, para no dejar enlaces rotos."""
    indice = os.path.join(proyecto, INDICE_SKILLS)
    lineas = leer_bytes(indice).decode("utf-8").splitlines(True)
    escribir_atomico(indice, "".join(l for l in lineas if not any("skills/%s/SKILL.md)" % n in l for n in nombres)).encode("utf-8"))


def version_disponible(proyecto, cfg=None):
    """Spec 019: (versión instalada, versión del repo del arnés) si el repo es una carpeta local con una versión MÁS NUEVA; si no, None.
    Solo lee dos archivos pequeños: sin red."""
    try:
        if cfg is None:
            with open(os.path.join(proyecto, ".brain", "guardianes", "guardianes.json"), encoding="utf-8") as f:
                cfg = json.load(f)
        origen = cfg.get("arnes_repo") or ""
        if not origen or origen.startswith(("http://", "https://", "git@", "ssh://")) or origen.endswith(".git"):
            return None
        carpeta = origen if os.path.isabs(origen) else os.path.join(proyecto, origen)
        with open(os.path.join(carpeta, "VERSION"), encoding="utf-8") as f:
            nueva = f.read().strip()
        actual = (cargar_registro(proyecto).get("version") or "").strip()
        if not actual or not nueva or os.path.abspath(carpeta) == os.path.abspath(proyecto):
            return None
        clave = lambda v: tuple(int(x) for x in v.split("."))
        return (actual, nueva) if clave(nueva) > clave(actual) else None
    except Exception:
        return None


def destinos(manifiesto, proyecto):
    """Pares (ruta en el repo, ruta en el proyecto). Con `AGENTS.md` (Codex) las skills de `.claude/skills/` también van a `.agents/skills/`."""
    pares = [(rel, rel) for rel in sorted(manifiesto["archivos"])]
    if os.path.isfile(os.path.join(proyecto, "AGENTS.md")):
        pares += [(rel, ".agents/skills/" + rel[len(".claude/skills/"):]) for rel in sorted(manifiesto["archivos"]) if rel.startswith(".claude/skills/")]
    return pares


def destinos_retirados(manifiesto):
    """Rutas retiradas del arnés que pueden seguir en el proyecto, con su copia de Codex en `.agents/skills/` (spec 021)."""
    res = []
    for rel in sorted(set(manifiesto.get("retirados") or []) - set(manifiesto["archivos"])):
        res.append(rel)
        if rel.startswith(".claude/skills/"):
            res.append(".agents/skills/" + rel[len(".claude/skills/"):])
    return res


def quitar_carpetas_vacias(proyecto, ruta):
    """Sube desde el archivo retirado borrando las carpetas que quedan vacías, sin salir del proyecto."""
    carpeta = os.path.dirname(ruta)
    while os.path.abspath(carpeta) != os.path.abspath(proyecto):
        try:
            os.rmdir(carpeta)
        except OSError:
            return
        carpeta = os.path.dirname(carpeta)


def sincronizar(repo, proyecto, dueno=None, simular=False, forzar=(), adoptar=(), ahora=None, forzar_todo=False):
    """Compara el proyecto con el repo y (si no es simulación) copia lo que toca.
    Devuelve {'version_antes', 'version', 'nuevos', 'actualizados', 'sin_cambios', 'a_mano', 'forzados', 'retirados', 'retirados_a_mano',
    'filas_quitadas', 'sin_aplicar', 'fichas', 'copia', 'claves_nuevas', 'claves_escritas'}. La simulación anuncia lo mismo que hace la ejecución real.
    `adoptar`: rutas absolutas que el kit de arranque acaba de crear (se tratan como no modificadas a mano).
    `forzar_todo`: pisa (con copia de seguridad) también todo lo modificado a mano; para la primera adopción de un proyecto antiguo."""
    repo, proyecto = os.path.abspath(repo), os.path.abspath(proyecto)
    if repo == proyecto:
        raise ValueError(tp("actualizar_arnes_proyecto_repo_arnes"))
    manifiesto = cargar_manifiesto(repo)
    comprobar_manifiesto(repo, manifiesto)
    registro = cargar_registro(proyecto)
    dueno = dueno or registro.get("dueno")
    archivos_reg = dict(registro.get("archivos") or {})
    adoptar = {os.path.normcase(os.path.abspath(a)) for a in adoptar}
    forzar = {f.replace("\\", "/") for f in forzar}
    res = {"version_antes": registro.get("version"), "version": manifiesto.get("version"), "nuevos": [], "actualizados": [],
           "sin_cambios": [], "a_mano": [], "forzados": [], "copia": None, "claves_nuevas": claves_nuevas(repo, proyecto),
           "claves_escritas": {}, "fichas": [], "retirados": [], "retirados_a_mano": [], "filas_quitadas": [], "sin_aplicar": []}
    por_escribir = []  # (rel, destino, contenido, existia)
    for fuente, rel in destinos(manifiesto, proyecto):
        destino = ruta_segura(proyecto, rel)
        if destino is None or ruta_segura(repo, fuente) is None:
            raise ValueError(tp("actualizar_arnes_ruta_permitida_manifiesto2") % rel)
        nuevo = esperado(repo, fuente, dueno)
        h_nuevo = huella(nuevo)
        if not os.path.exists(destino):
            res["nuevos"].append(rel)
            por_escribir.append((rel, destino, nuevo, False))
            archivos_reg[rel] = h_nuevo
            continue
        h_actual = huella(_normalizar(leer_bytes(destino), rel))
        if h_actual == h_nuevo:
            res["sin_cambios"].append(rel)
            archivos_reg[rel] = h_nuevo
        elif archivos_reg.get(rel) == h_actual or os.path.normcase(destino) in adoptar:
            res["actualizados"].append(rel)
            por_escribir.append((rel, destino, nuevo, True))
            archivos_reg[rel] = h_nuevo
        elif rel in forzar or forzar_todo:
            res["forzados"].append(rel)
            por_escribir.append((rel, destino, nuevo, True))
            archivos_reg[rel] = h_nuevo
        else:
            res["a_mano"].append(rel)  # modificado a mano (o sin registro previo): no se pisa
    por_retirar = []  # (rel, destino)
    for rel in destinos_retirados(manifiesto):
        destino = ruta_segura(proyecto, rel)
        if destino is None:
            raise ValueError(tp("actualizar_arnes_ruta_permitida_manifiesto3") % rel)
        if not os.path.exists(destino):
            archivos_reg.pop(rel, None)
        elif archivos_reg.get(rel) == huella(_normalizar(leer_bytes(destino), rel)) or rel in forzar or forzar_todo:
            res["retirados"].append(rel)
            por_retirar.append((rel, destino))
            archivos_reg.pop(rel, None)
        else:
            res["retirados_a_mano"].append(rel)  # modificado a mano o sin registro: no se toca
    res["sin_aplicar"] = sorted(res["a_mano"] + res["retirados_a_mano"])
    salen = {_skill_de(rel) for rel in res["retirados"] if rel.startswith(".claude/")} - {None}
    res["filas_quitadas"] = filas_de_retiradas(manifiesto, proyecto, salen)
    if simular:
        res["claves_escritas"] = completar_configuracion(repo, proyecto, simular=True)
        llegan = [_skill_de(rel) for rel in res["nuevos"] if rel.startswith(".claude/") and _skill_de(rel)]
        res["fichas"] = completar_fichas_skills(repo, proyecto, simular=True, llegan=llegan, salen=salen)
        return res
    respaldos = [(p[0], p[1]) for p in por_escribir if p[3] and os.path.normcase(p[1]) not in adoptar] + por_retirar  # lo que acaba de crear el kit no necesita copia
    if res["filas_quitadas"]:
        respaldos.append((INDICE_SKILLS, os.path.join(proyecto, INDICE_SKILLS)))
    if respaldos:
        sello = (ahora or datetime.datetime.now()).strftime("%Y%m%d-%H%M%S")
        res["copia"] = os.path.join(COPIAS, sello)
        for rel, destino in respaldos:
            copia = os.path.join(proyecto, res["copia"], rel)
            os.makedirs(os.path.dirname(copia), exist_ok=True)
            shutil.copyfile(destino, copia)
    for rel, destino, contenido, _ in por_escribir:
        escribir_atomico(destino, contenido)
    for rel, destino in por_retirar:
        os.remove(destino)  # ya está en la copia de seguridad
        quitar_carpetas_vacias(proyecto, destino)
    if res["filas_quitadas"]:
        quitar_filas(proyecto, res["filas_quitadas"])
    guardar_registro(proyecto, {"version": manifiesto.get("version"), "dueno": dueno, "archivos": archivos_reg,
                                "nivel": "completo", "sin_aplicar": res["sin_aplicar"]})
    res["claves_escritas"] = completar_configuracion(repo, proyecto)
    res["fichas"] = completar_fichas_skills(repo, proyecto)
    return res


def correr_pruebas(repo, proyecto):
    """Pasa las pruebas del método que el proyecto tiene. Devuelve (ok, texto) o (None, aviso) si no hay ninguna."""
    modulos = [m for m in cargar_manifiesto(repo).get("pruebas", []) if os.path.exists(os.path.join(proyecto, *m.split(".")) + ".py")]
    if not modulos:
        return None, tp("actualizar_arnes_proyecto_tiene_pruebas")
    env = dict(os.environ, CEREBRO_SIN_PODA="1", PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-m", "unittest"] + modulos, cwd=proyecto, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=env, stdin=subprocess.DEVNULL, timeout=900)
    return r.returncode == 0, (r.stderr or r.stdout).strip()[-600:]


def localizar_repo(proyecto, indicado):
    """(carpeta del repo, carpeta temporal a borrar o None). Acepta carpeta local o dirección git."""
    origen = indicado or os.environ.get("CEREBRO_ARNES_REPO")
    if not origen:
        try:
            with open(os.path.join(proyecto, ".brain", "guardianes", "guardianes.json"), encoding="utf-8") as f:
                origen = json.load(f).get("arnes_repo")
        except Exception:
            origen = None
    if not origen:
        raise ValueError(tp("actualizar_arnes_donde_esta_repo"))
    if origen.startswith(("http://", "https://", "git@", "ssh://")) or origen.endswith(".git"):
        tmp = tempfile.mkdtemp(prefix="cerebro-vivo-")
        r = subprocess.run(["git", "clone", "--depth", "1", "-q", origen, tmp], capture_output=True, text=True, timeout=180)
        if r.returncode != 0:
            shutil.rmtree(tmp, ignore_errors=True)
            raise ValueError(tp("actualizar_arnes_pude_bajar_repo") % r.stderr.strip()[-200:])
        return tmp, tmp
    carpeta = origen if os.path.isabs(origen) else os.path.join(proyecto, origen)
    return os.path.abspath(carpeta), None


OBJETIVO = os.path.join(".brain", "architecture", "objetivo.md")
PLANTILLA_OBJETIVO = os.path.join(".brain", "biblioteca", "kit-arranque", "plantillas", "objetivo.md")
INDICES_ENTRADA = ("CLAUDE.md", "GEMINI.md", "AGENTS.md")
LINEA_OBJETIVO = "* **Objetivo del proyecto (leer primero):** [`.brain/architecture/objetivo.md`](.brain/architecture/objetivo.md)."


def migrar_objetivo(proyecto, simular=False, ahora=None):
    """Spec 008: en un proyecto ya instalado crea `objetivo.md`, lo enlaza en los índices de entrada y añade la regla a la constitución.
    Idempotente; no pisa nada (solo añade) y guarda copia de lo que modifica. Devuelve {'creados', 'modificados', 'avisos'}."""
    proyecto = os.path.abspath(proyecto)
    res = {"creados": [], "modificados": [], "avisos": []}
    dueno = cargar_registro(proyecto).get("dueno") or DUENO_ORIGINAL
    cambios = []  # (ruta relativa, texto nuevo)
    ruta_obj = os.path.join(proyecto, OBJETIVO)
    if not os.path.exists(ruta_obj):
        plantilla = os.path.join(proyecto, PLANTILLA_OBJETIVO)
        if os.path.isfile(plantilla):
            texto = leer_bytes(plantilla).decode("utf-8").replace("{{NOMBRE}}", os.path.basename(proyecto)).replace("{{DUENO}}", dueno)
            res["creados"].append(OBJETIVO)
            cambios.append((OBJETIVO, texto))
        else:
            res["avisos"].append(tp("actualizar_arnes_falta_plantilla_objetivo"))
    for nombre in INDICES_ENTRADA:
        ruta = os.path.join(proyecto, nombre)
        if not os.path.isfile(ruta):
            continue
        texto = leer_bytes(ruta).decode("utf-8")
        if "architecture/objetivo.md" in texto:
            continue
        salto = "\r\n" if "\r\n" in texto else "\n"
        lineas = texto.split(salto)
        donde = next((i for i, l in enumerate(lineas) if l.lstrip().startswith("* **Pendientes:**")), None)
        if donde is None:
            res["avisos"].append(tp("actualizar_arnes_encuentro_donde_insertarlo") % (nombre, LINEA_OBJETIVO))
            continue
        lineas.insert(donde, LINEA_OBJETIVO)
        res["modificados"].append(nombre)
        cambios.append((nombre, salto.join(lineas)))
    ruta = os.path.join(proyecto, ".brain", "constitution.md")
    if os.path.isfile(ruta):
        texto = leer_bytes(ruta).decode("utf-8")
        if "objetivo.md" not in texto:
            salto = "\r\n" if "\r\n" in texto else "\n"
            numeros = [int(m) for m in re.findall(r"^(\d+)\.", texto, re.M)]
            regla = ("%d. **El objetivo se escribe:** todo objetivo o cambio de objetivo que %s dé en un chat se anota en "
                     "`.brain/architecture/objetivo.md` en esa misma respuesta; lo que solo está en el chat se pierde.") % (max(numeros, default=0) + 1, dueno)
            res["modificados"].append(os.path.join(".brain", "constitution.md"))
            cambios.append((os.path.join(".brain", "constitution.md"), texto.rstrip("\r\n") + salto + regla + salto))
    else:
        res["avisos"].append(tp("actualizar_arnes_brain_constitution_anadio"))
    if simular or not cambios:
        return res
    sello = (ahora or datetime.datetime.now()).strftime("%Y%m%d-%H%M%S")
    for rel, texto in cambios:
        destino = os.path.join(proyecto, rel)
        if os.path.exists(destino):
            copia = os.path.join(proyecto, COPIAS, sello, rel)
            os.makedirs(os.path.dirname(copia), exist_ok=True)
            shutil.copyfile(destino, copia)
        escribir_atomico(destino, texto.encode("utf-8"))
    return res


def informe_migracion(res, simular):
    L = [tp("actualizar_arnes_migracion_objetivo") % (tp("actualizar_arnes_simulacion_escribio_nada") if simular else tp("actualizar_arnes_aplicada"))]
    L += ["  + creado %s" % r for r in res["creados"]] + ["  ~ modificado %s" % r for r in res["modificados"]]
    if not res["creados"] and not res["modificados"]:
        L.append(tp("actualizar_arnes_nada_cambiar_proyecto"))
    L += ["  ⚠ " + a for a in res["avisos"]]
    return "\n".join(L)


def informe(res, simular):
    L = [tp("actualizar_arnes_arnes") % (res["version_antes"] or tp("actualizar_arnes_sin_registrar"), res["version"], tp("actualizar_arnes_simulacion_escribio_nada2") if simular else "")]
    for clave, titulo in (("nuevos", tp("actualizar_arnes_archivos_nuevos")), ("actualizados", tp("actualizar_arnes_archivos_actualizan")), ("forzados", tp("actualizar_arnes_archivos_pisados_forzar"))):
        if res[clave]:
            L.append("%s (%d):" % (titulo, len(res[clave])))
            L += ["  + " + r for r in res[clave]]
    if res.get("retirados"):
        L.append(tp("actualizar_arnes_retirados_arnes_copia") % (tp("actualizar_arnes_irian") if simular else tp("actualizar_arnes_movidos"), len(res["retirados"])))
        L += ["  - " + r for r in res["retirados"]]
    L.append(tp("actualizar_arnes_sin_cambios_archivo") % len(res["sin_cambios"]))
    if res["a_mano"]:
        L.append(tp("actualizar_arnes_modificados_mano_sin") % len(res["a_mano"]))
        L += ["  ! " + r for r in res["a_mano"]]
    if res.get("retirados_a_mano"):
        L.append(tp("actualizar_arnes_retirados_arnes_pero") % len(res["retirados_a_mano"]))
        L += ["  ! " + r for r in res["retirados_a_mano"]]
    if res.get("sin_aplicar"):
        L.append(tp("actualizar_arnes_version_aplicada_salvo") % (res["version"], len(res["sin_aplicar"])))
    if res.get("claves_escritas"):
        L.append(tp("actualizar_arnes_configuracion_clave_nueva") % (
            tp("actualizar_arnes_anadirian2") if simular else tp("actualizar_arnes_anadieron"), len(res["claves_escritas"]), ", ".join(sorted(res["claves_escritas"]))))
    if res.get("fichas"):
        L.append(tp("actualizar_arnes_fichas_skills_brain") % (tp("actualizar_arnes_anadirian") if simular else tp("actualizar_arnes_anadidas"), ", ".join(res["fichas"])))
    if res.get("filas_quitadas"):
        L.append(tp("actualizar_arnes_filas_skills_retiradas") % (tp("actualizar_arnes_quitarian") if simular else tp("actualizar_arnes_quitadas"), ", ".join(res["filas_quitadas"])))
    if res["copia"]:
        L.append(tp("actualizar_arnes_copia_seguridad_sustituido") % res["copia"])
    return "\n".join(L)


def nivel_sin_arnes(proyecto, forzar_todo=False):
    """Spec 021 (punto 14): el motivo para no actualizar un proyecto sin guardianes, o None si se puede. Un proyecto antiguo sin
    nivel anotado se adopta a propósito con `--forzar-todo`; uno de nivel ligero o medio sube con el kit."""
    nivel = cargar_registro(proyecto).get("nivel")
    if nivel:
        return None if nivel == "completo" else tp("actualizar_arnes_esta_nivel") % nivel
    if forzar_todo or os.path.isfile(os.path.join(proyecto, ".brain", "guardianes", "guardianes.json")):
        return None
    return tp("actualizar_arnes_tiene_guardianes_brain")


def main(argv=None, repo=None):
    """`repo` indica que se lanza desde el repo del arnés (entonces el proyecto es un argumento)."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Actualiza un proyecto con las mejoras del arnés de Cerebro Vivo")
    if repo:
        ap.add_argument("proyecto", help="carpeta del proyecto que se actualiza")
    else:
        ap.add_argument("--repo", help="carpeta o dirección git del repo del arnés (si no, `arnes_repo` de guardianes.json)")
    ap.add_argument("--simular", action="store_true", help="muestra qué cambiaría sin escribir nada")
    ap.add_argument("--forzar", action="append", default=[], metavar="RUTA", help="pisa este archivo aunque se haya modificado a mano")
    ap.add_argument("--forzar-todo", action="store_true", help="pisa TODO lo modificado a mano (con copia); para adoptar el arnés por primera vez en un proyecto antiguo")
    ap.add_argument("--dueno", help="nombre del dueño (si el proyecto no lo tiene registrado)")
    ap.add_argument("--migrar-objetivo", action="store_true", help="crea objetivo.md, lo enlaza en los índices y añade la regla a la constitución (solo añade; con --simular no escribe)")
    ap.add_argument("--sin-pruebas", action="store_true", help="no corre las pruebas del método al terminar")
    a = ap.parse_args(argv)
    proyecto = os.path.abspath(a.proyecto if repo else RAIZ_PROPIA)
    temporal = None
    if a.migrar_objetivo:
        if not os.path.isdir(proyecto):
            print(tp("actualizar_arnes_existe_carpeta_proyecto") % proyecto)
            return 2
        print(informe_migracion(migrar_objetivo(proyecto, simular=a.simular), a.simular))
        return 0
    try:
        if not repo:
            repo, temporal = localizar_repo(proyecto, a.repo)
        if not os.path.isfile(os.path.join(repo, MANIFIESTO)):
            print(tp("actualizar_arnes_repo_arnes_falta") % (repo, MANIFIESTO))
            return 2
        if not os.path.isdir(proyecto):
            print(tp("actualizar_arnes_existe_carpeta_proyecto2") % proyecto)
            return 2
        motivo = nivel_sin_arnes(proyecto, a.forzar_todo)
        if motivo:
            print(tp("actualizar_arnes_copia_nada_este") % (motivo, proyecto))
            return 0
        res = sincronizar(repo, proyecto, dueno=a.dueno, simular=a.simular, forzar=a.forzar, forzar_todo=a.forzar_todo)
        print(informe(res, a.simular))
        if a.simular or a.sin_pruebas:
            return 0
        ok, texto = correr_pruebas(repo, proyecto)
        if ok is None:
            print("ℹ️ " + texto)
        elif ok:
            print(tp("actualizar_arnes_pruebas_metodo_proyecto"))
        else:
            print(tp("actualizar_arnes_pruebas_metodo_fallan") + texto)
            return 1
        return 0
    except (ValueError, OSError, subprocess.SubprocessError) as e:
        print("❌ %s" % e)
        return 2
    finally:
        if temporal:
            shutil.rmtree(temporal, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
