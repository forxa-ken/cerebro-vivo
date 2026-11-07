#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kit de arranque de Cerebro Vivo (spec 054): monta la memoria y los guardianes en un proyecto nuevo.

Uso:  python .brain/biblioteca/kit-arranque/instalar.py DESTINO [--nombre N] [--dueno D] [--idioma I]
                                                       [--pruebas "comando"] [--ias claude,gemini,codex]
                                                       [--nivel ligero|medio|completo]
      python .brain/biblioteca/kit-arranque/instalar.py --comprobar DESTINO

Los guardianes se copian de este mismo proyecto (una sola fuente de verdad) y se les quitan los datos propios
mezclando `ajustes_neutros.json` sobre `guardianes.json`. Nunca pisa un archivo que ya exista. Solo librería estándar."""

import argparse
import datetime
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
PLANTILLAS = os.path.join(AQUI, "plantillas")
BRAIN_FUENTE = os.path.abspath(os.path.join(AQUI, "..", ".."))
GUARDIANES_FUENTE = os.path.join(BRAIN_FUENTE, "guardianes")
RAIZ_FUENTE = os.path.abspath(os.path.join(BRAIN_FUENTE, ".."))
GUARDIANES = ["textos", "arranque", "guardar_traspaso", "cierre", "cerrar", "poda", "medir", "secretos", "librerias", "pruebas", "longitud", "analisis", "base_datos", "indices", "notas_abiertas", "revisar_indices", "archivos_gordos", "actualizar_arnes"]
IAS = {"claude": ("CLAUDE.md", "Claude"), "gemini": ("GEMINI.md", "Antigravity/Gemini"), "codex": ("AGENTS.md", "GPT Codex")}
NIVELES = ("ligero", "medio", "completo")
BIBLIOTECA = ["CARTA_META_ARNES.md", "CEREBRO_VIVO.md"]
KIT_TRADUCCION = os.path.join(BRAIN_FUENTE, "biblioteca", "kit-traduccion")  # spec 057 (opcional)


def leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        return f.read()


def escribir_sin_pisar(ruta, texto, hechos):
    """Crea el archivo solo si no existe. Anota en `hechos` lo creado y lo respetado."""
    if os.path.exists(ruta):
        hechos["respetados"].append(ruta)
        return
    if hechos.get("simulacion"):  # solo contar lo que se crearía
        hechos["creados"].append(ruta)
        return
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)
    hechos["creados"].append(ruta)


MARCA_INI = "<!-- cerebro-vivo:inicio -->"
MARCA_FIN = "<!-- cerebro-vivo:fin -->"
COPIA = ".antes-de-cerebro-vivo"


def copia_de_seguridad(ruta, hechos):
    """Guarda `ruta` + COPIA al lado, una sola vez (si la copia ya existe no se sobrescribe)."""
    copia = ruta + COPIA
    if not os.path.exists(copia) and not hechos.get("simulacion"):
        shutil.copy2(ruta, copia)


def fusionar_indice(ruta, bloque, destino, hechos):
    """Índice de IA que ya existe: añade al final el bloque marcado (spec 015) y guarda una copia íntegra del original
    en `.brain/archive/adoptado/`. Devuelve True si lo fusionó; si el bloque ya estaba, lo cuenta como respetado."""
    with open(ruta, "rb") as f:
        crudo = f.read()
    contenido = crudo.decode("utf-8", errors="replace")
    if MARCA_INI in contenido:
        hechos["respetados"].append(ruta)
        return False
    hechos["fusionados"].append(ruta)
    if hechos.get("simulacion"):
        return True
    copia_de_seguridad(ruta, hechos)
    nombre = os.path.splitext(os.path.basename(ruta))[0] + ".original.md"
    adoptado = os.path.join(destino, ".brain", "archive", "adoptado", nombre)
    if not os.path.exists(adoptado):
        os.makedirs(os.path.dirname(adoptado), exist_ok=True)
        with open(adoptado, "wb") as f:  # byte a byte: ni los saltos de línea cambian
            f.write(crudo)
    nl = "\r\n" if b"\r\n" in crudo else "\n"  # el bloque usa los saltos de línea del archivo
    sep = "" if contenido.endswith("\n") else nl
    lineas = [sep, MARCA_INI] + bloque.strip("\n").split("\n") + [MARCA_FIN]
    with open(ruta, "ab") as f:
        f.write((nl.join(lineas) + nl).encode("utf-8"))
    return True


def _llama_a(entradas, guardian):
    return any(guardian in h.get("command", "") for e in entradas if isinstance(e, dict) for h in e.get("hooks", []) if isinstance(h, dict))


def fusionar_ajustes(ruta, nuevos, hechos):
    """`.claude/settings.json` que ya existe: añade los hooks del kit que falten y une `permissions.deny`, sin quitar nada.
    Si el JSON no se puede leer, no lo toca y avisa con lo que hay que pegar a mano."""
    try:
        actual = json.loads(leer(ruta))
        if not isinstance(actual, dict):
            raise ValueError("no es un objeto")
        hooks = actual.get("hooks", {})
        deny = actual.get("permissions", {}).get("deny", [])
        if not isinstance(hooks, dict) or not isinstance(deny, list) or not isinstance(actual.get("permissions", {}), dict):
            raise ValueError("estructura inesperada")
        if any(not isinstance(v, list) for v in hooks.values()):
            raise ValueError("hooks inesperados")
    except (ValueError, OSError) as e:
        hechos["avisos"].append("No pude leer %s (%s) y no se tocó. Pega a mano esto dentro:\n%s" % (ruta, e, json.dumps(nuevos, ensure_ascii=False, indent=2)))
        hechos["respetados"].append(ruta)
        return False
    cambios = False
    for evento, entradas in nuevos["hooks"].items():
        guardian = re.search(r"([a-z_]+)\.py", entradas[0]["hooks"][0]["command"]).group(1) + ".py"
        previas = hooks.get(evento, [])
        if _llama_a(previas, guardian):
            continue
        if previas:
            hechos["avisos"].append("%s ya tenía un hook en %s: ahora corren los dos (el orden no está garantizado)." % (os.path.basename(ruta), evento))
        hooks[evento] = previas + entradas
        cambios = True
    faltan = [d for d in nuevos["permissions"]["deny"] if d not in deny]
    if faltan:
        deny = deny + faltan
        cambios = True
    if not cambios:
        hechos["respetados"].append(ruta)
        return False
    hechos["fusionados"].append(ruta)
    if hechos.get("simulacion"):
        return True
    copia_de_seguridad(ruta, hechos)
    actual["hooks"] = hooks
    actual.setdefault("permissions", {})["deny"] = deny
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(actual, ensure_ascii=False, indent=2) + "\n")
    return True


def rellenar(texto, valores):
    for k, v in valores.items():
        texto = texto.replace("{{%s}}" % k, v)
    return texto


def mezclar(base, extra):
    """Mezcla recursiva: los diccionarios se fusionan, lo demás (listas, valores) se sustituye."""
    res = dict(base)
    for k, v in extra.items():
        if k == "_ayuda":
            continue
        res[k] = mezclar(res[k], v) if isinstance(v, dict) and isinstance(res.get(k), dict) else v
    return res


def python_del_proyecto(destino):
    """(comando para el hook, comando para escribir en los índices) según el entorno virtual del destino."""
    if os.path.exists(os.path.join(destino, "venv", "Scripts", "python.exe")):
        return '"$CLAUDE_PROJECT_DIR/venv/Scripts/python.exe"', "venv\\Scripts\\python.exe"
    if os.path.exists(os.path.join(destino, "venv", "bin", "python")):
        return '"$CLAUDE_PROJECT_DIR/venv/bin/python"', "venv/bin/python"
    if os.name != "nt" and not shutil.which("python") and shutil.which("python3"):  # Mac/Linux sin `python` (spec 013)
        return "python3", "python3"
    return "python", "python"


def bloque_ia(ia, nivel, py):
    if nivel != "completo":
        return "* **Al iniciar:** leer este índice y `.brain/pendientes.md`. **Al terminar cada tarea:** añadir una línea en `.brain/decisions.log`."
    manual = ("* **Al iniciar sesión**, antes de nada: leer `.brain/constitution.md` y `.brain/pendientes.md`, y ejecutar el resumen de arranque, "
              "mostrándolo en 4-5 viñetas (`--manual` es obligatorio):\n  ```\n  %s .brain/guardianes/arranque.py --manual\n  ```\n"
              "* **Al terminar cada tarea**, registrar la línea con el cierre rápido (no hay aviso automático):\n  ```\n"
              "  %s .brain/guardianes/cerrar.py --chat \"{{NOMBRE}} #N\" --quien \"%s\" \"qué se hizo, en una frase\"\n  ```" % (py, py, ia))
    if ia == "Claude":
        return ("* **Al iniciar sesión** el resumen de arranque llega solo (hook `SessionStart`) con el estado real; no hace falta releer nada para una tarea pequeña. "
                "Leer `.brain/constitution.md` y `.brain/pendientes.md` solo si la tarea es grande, toca una decisión o hay duda de reglas.\n* **Al terminar cada tarea pequeña** (hasta 2 archivos, nada sensible, pruebas en verde): NO escribas la línea del registro, el hook `Stop` la pone solo (modo ligero). "
                "**Tarea grande, sensible o con una decisión:** cierre rápido: `%s .brain/guardianes/cerrar.py --chat \"{{NOMBRE}} #N\" \"qué se hizo\"`." % py)
    return manual


def mapa(nivel):
    lineas = []
    if nivel != "ligero":
        lineas.append("* **Objetivo del proyecto (leer primero):** [`.brain/architecture/objetivo.md`](.brain/architecture/objetivo.md).")
    lineas += ["* **Pendientes:** [`.brain/pendientes.md`](.brain/pendientes.md) es la lista viva de **solo lo que falta**; leerla al iniciar.",
              "* **Registro:** [`.brain/decisions.log`](.brain/decisions.log): una línea por tarea terminada."]
    if nivel != "ligero":
        lineas += ["* **Cambio de IA (Claude, Gemini, Codex):** si existe `.brain/traspaso.md`, léelo primero; al abrir un chat nuevo con la misma IA usa `traspaso-in entro`, y al cambiar de IA `traspaso-out salgo` / `traspaso-out entro` (en Codex, con `$`).",
                   "* **Reglas innegociables:** [`.brain/constitution.md`](.brain/constitution.md).",
                   "* **Decisiones y su porqué:** [`.brain/decisions/indice.md`](.brain/decisions/indice.md); consultarlo antes de cambiar algo ya decidido.",
                   "* **Historial:** `.brain/archive/` (**no abrirlo completo**; consultar `hechos-indice.md`).",
                   "* **Mapa y hoja de ruta:** [`.brain/referencias.md`](.brain/referencias.md) (consultar solo si toca)."]
    if nivel == "completo":
        lineas += ["* **Traspaso entre chats:** si existe `.brain/traspaso.md`, el arranque lo muestra solo; al proponer un chat nuevo se escribe antes (plantilla en `.brain/biblioteca/PLANTILLA_TRASPASO.md`).",
                   "* **Notas de chats auxiliares:** el chat que recibe un encargo de otro deja su nota en `.brain/notas-chats/` (plantilla en `.brain/biblioteca/PLANTILLA_NOTA_CHAT.md`).",
                   "* **Biblioteca:** [`.brain/biblioteca/README.md`](.brain/biblioteca/README.md): método «Cerebro Vivo» y carta del meta-arnés.",
                   "* **Pruebas con hallazgos:** `.brain/pruebas/` (el arranque avisa si queda alguno abierto)."]
    return "\n".join(lineas)


def codigo_idioma(idioma):
    """Spec 024: «English», «inglés», «en»… -> "en"; cualquier otro idioma -> "es" (los avisos solo están en es/en)."""
    espec = importlib.util.spec_from_file_location("textos", os.path.join(GUARDIANES_FUENTE, "textos.py"))
    textos = importlib.util.module_from_spec(espec)
    espec.loader.exec_module(textos)
    return textos.idioma(idioma)


def configuracion(ias, idioma="español"):
    cfg = json.loads(leer(os.path.join(GUARDIANES_FUENTE, "guardianes.json")))
    cfg = mezclar(cfg, json.loads(leer(os.path.join(AQUI, "ajustes_neutros.json"))))
    cfg["idioma"] = codigo_idioma(idioma)  # spec 024: idioma de los avisos de los guardianes
    archivos = [IAS[i][0] for i in ias]
    cfg["indices_entrada"] = archivos
    cfg["claude_md"] = archivos[0]
    if os.path.exists(os.path.join(RAIZ_FUENTE, "manifiesto.json")):  # spec 087: de dónde se actualiza el proyecto
        cfg["arnes_repo"] = RAIZ_FUENTE
    return cfg


def cargar_actualizador():
    espec = importlib.util.spec_from_file_location("actualizar_arnes", os.path.join(GUARDIANES_FUENTE, "actualizar_arnes.py"))
    actualizador = importlib.util.module_from_spec(espec)
    espec.loader.exec_module(actualizador)
    return actualizador


def repo_del_arnes(cfg):
    """Carpeta del repo del arnés con su manifiesto, o None."""
    repo = RAIZ_FUENTE if os.path.exists(os.path.join(RAIZ_FUENTE, "manifiesto.json")) else cfg.get("arnes_repo")
    return repo if repo and os.path.exists(os.path.join(repo, "manifiesto.json")) else None


def comprobar_arnes(ias):
    """Spec 021: con el manifiesto desfasado, parar antes de escribir nada en vez de quedarse a medias."""
    repo = repo_del_arnes(configuracion(ias))
    if repo:
        cargar_actualizador().comprobar_manifiesto(repo)


def instalar(destino, nombre, dueno, idioma, pruebas, ias, nivel, hoy=None, simular=False, git_init=False, traduccion=False):
    """Monta el kit en `destino` (con `simular` solo cuenta). Devuelve {'creados': [...], 'fusionados': [...], 'respetados': [...], 'avisos': [...]}.
    Con `traduccion` añade además el kit de traducción es/en/pt (spec 057) en `static/i18n/`."""
    if nivel == "completo":
        comprobar_arnes(ias)
    hechos = {"creados": [], "fusionados": [], "respetados": [], "avisos": [], "simulacion": simular}
    destino = os.path.abspath(destino)
    if not simular:
        os.makedirs(destino, exist_ok=True)
    hook_py, py = python_del_proyecto(destino)
    valores = {"NOMBRE": nombre, "DUENO": dueno, "IDIOMA": idioma, "PRUEBAS": pruebas, "FECHA": hoy or datetime.date.today().isoformat()}

    def plantilla(nombre_archivo):
        return rellenar(leer(os.path.join(PLANTILLAS, nombre_archivo)), valores)

    def fuente(*partes):  # texto de este proyecto con el nombre del dueño cambiado
        return leer(os.path.join(*partes)).replace("Darwin", dueno)

    def poner(rel, texto):
        escribir_sin_pisar(os.path.normpath(os.path.join(destino, rel)), texto, hechos)

    todos = [IAS[i][0] for i in ias]
    adoptados = []
    for i in ias:
        archivo, ia = IAS[i]
        texto = leer(os.path.join(PLANTILLAS, "indice_ia.md"))
        texto = texto.replace("{{BLOQUE_IA}}", bloque_ia(ia, nivel, py)).replace("{{MAPA}}", mapa(nivel))
        texto = texto.replace("{{IA}}", ia).replace("{{ARCHIVO}}", archivo)
        texto = texto.replace("{{OTROS}}", ", ".join("`%s`" % t for t in todos if t != archivo) or "ninguno más por ahora")
        texto = rellenar(texto, valores)
        ruta_indice = os.path.normpath(os.path.join(destino, archivo))
        if os.path.exists(ruta_indice):
            bloque = texto[texto.index("## Memoria persistente"):texto.index("## Reglas esenciales")]
            if fusionar_indice(ruta_indice, bloque, destino, hechos):
                adoptados.append(archivo)
        else:
            poner(archivo, texto)
    pendientes = plantilla("pendientes.md")
    if adoptados:  # spec 015: la IA reparte lo que el proyecto ya tenía en los archivos de la memoria
        tarea = ("- **2:** adaptar lo que ya tenía el proyecto (%s) a la memoria `.brain/`: escribe `/adopta` (reparte, acorta y trocea, pidiendo tu sí en cada paso; skill `adoptar-indice-existente`); "
                 "originales en `.brain/archive/adoptado/`.\n" % ", ".join(adoptados))
        pendientes = pendientes.replace("\n## Esperando", tarea + "\n## Esperando", 1)
        hechos["avisos"].append("Se añadió el bloque de memoria al final de %s (copia del original en .brain/archive/adoptado/). "
                                "En el primer chat escribe /adopta (reparte, acorta y trocea; te pide el sí en cada paso)." % ", ".join(adoptados))
    poner(".brain/pendientes.md", pendientes)
    poner(".brain/decisions.log", "")
    if traduccion:
        clave = re.sub(r"[^a-z0-9]+", "_", nombre.lower()).strip("_") or "proyecto"
        for archivo in ("i18n_motor.js", "idiomas.js", "ejemplo.html"):
            texto = leer(os.path.join(KIT_TRADUCCION, archivo))
            poner("static/i18n/" + archivo, texto.replace("mi_proyecto_lang", clave + "_lang"))
        poner("static/i18n/LEEME.md", leer(os.path.join(KIT_TRADUCCION, "README.md")))
        poner("tests/test_paridad_idiomas.py", leer(os.path.join(KIT_TRADUCCION, "paridad_idiomas.py")))
    if nivel != "completo":  # spec 021: el actualizador sabe que aquí no hay guardianes que actualizar
        poner(".brain/arnes_instalado.json", json.dumps({"archivos": {}, "dueno": dueno, "nivel": nivel}, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    if nivel == "ligero":
        return hechos

    poner(".brain/constitution.md", plantilla("constitution.md"))
    poner(".brain/decisions/indice.md", plantilla("decisions_indice.md"))
    poner(".brain/archive/hechos.md", plantilla("hechos.md"))
    poner(".brain/archive/hechos-indice.md", plantilla("hechos_indice.md"))
    poner(".brain/referencias.md", plantilla("referencias.md"))
    poner(".brain/specs/_template.md", fuente(BRAIN_FUENTE, "specs", "_template.md"))
    poner(".brain/architecture/objetivo.md", plantilla("objetivo.md"))
    poner(".brain/architecture/README.md", "# Arquitectura\n\nUna ficha corta por área del proyecto. Se leen solo las del área en la que se trabaja.\n")
    if nivel == "medio":
        return hechos

    cfg = configuracion(ias, idioma)
    for g in GUARDIANES:
        texto = fuente(GUARDIANES_FUENTE, g + ".py")
        poner(".brain/guardianes/%s.py" % g, texto)
    poner(".brain/guardianes/guardianes.json", json.dumps(cfg, ensure_ascii=False, indent=2) + "\n")
    poner("tests/test_cerebro_indices.py", fuente(RAIZ_FUENTE, "tests", "test_cerebro_indices.py"))
    for b in BIBLIOTECA:
        poner(".brain/biblioteca/" + b, leer(os.path.join(BRAIN_FUENTE, "biblioteca", b)))
    poner(".brain/biblioteca/README.md", "# Biblioteca\n\nMaterial reutilizable: `CEREBRO_VIVO.md` (el método) y `CARTA_META_ARNES.md` (carta maestra). No se lee al arrancar.\n")
    poner(".brain/pruebas/indice.md", plantilla("pruebas_indice.md"))
    poner(".brain/pruebas/_plantilla.md", fuente(BRAIN_FUENTE, "pruebas", "_plantilla.md"))
    ajustes_claude = {
        "hooks": {
            "SessionStart": [{"hooks": [{"type": "command", "command": '%s "$CLAUDE_PROJECT_DIR/.brain/guardianes/arranque.py"' % hook_py, "timeout": 20}]}],
            "Stop": [{"hooks": [{"type": "command", "command": '%s "$CLAUDE_PROJECT_DIR/.brain/guardianes/cierre.py"' % hook_py, "timeout": 20}]}],
            "UserPromptSubmit": [{"hooks": [{"type": "command", "command": '%s "$CLAUDE_PROJECT_DIR/.brain/guardianes/notas_abiertas.py"' % hook_py, "timeout": 10}]}],
        },
        "permissions": {"deny": ["Read(./%s)" % a for a in cfg["secretos"]["archivos_secretos"]]},
    }
    ruta_ajustes = os.path.normpath(os.path.join(destino, ".claude", "settings.json"))
    if os.path.exists(ruta_ajustes):
        fusionar_ajustes(ruta_ajustes, ajustes_claude, hechos)
    else:
        poner(".claude/settings.json", json.dumps(ajustes_claude, ensure_ascii=False, indent=2) + "\n")
    if simular:
        return hechos
    repo_arnes = repo_del_arnes(cfg)
    if repo_arnes and destino != repo_arnes:  # spec 087: skills, kits, manual y pruebas del método, con su registro de versión
        res = cargar_actualizador().sincronizar(repo_arnes, destino, dueno=dueno, adoptar=hechos["creados"])
        hechos["creados"] += [os.path.join(destino, r) for r in res["nuevos"]]
        hechos["avisos"].append("Arnés %s instalado: se actualiza con `python .brain/guardianes/actualizar_arnes.py --simular`." % res["version"])
    ignorar = os.path.join(destino, ".gitignore")
    previo = leer(ignorar) if os.path.exists(ignorar) else ""
    secretos = [a for a in cfg["secretos"]["archivos_secretos"] if a not in previo.splitlines()]
    nuevas = [l for l in ["__pycache__/", "/.brain/guardianes/librerias_estado.json", "/.brain/guardianes/longitud_estado.json", "/.brain/guardianes/secretos_estado.json", "/.brain/copias_arnes/"] + secretos if l not in previo.splitlines()]
    if nuevas:
        with open(ignorar, "a", encoding="utf-8", newline="\n") as f:
            f.write(("" if not previo or previo.endswith("\n") else "\n") + "\n".join(nuevas) + "\n")
    if git_init and not os.path.isdir(os.path.join(destino, ".git")):
        subprocess.run(["git", "init", "-q"], cwd=destino, capture_output=True, timeout=30)
    if os.path.isdir(os.path.join(destino, ".git")):
        r = subprocess.run([sys.executable, os.path.join(destino, ".brain", "guardianes", "secretos.py"), "--instalar-hook"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=destino, timeout=30)
        hechos["avisos"].append(r.stdout.strip() or "No se pudo instalar el hook de secretos.")
    else:
        hechos["avisos"].append("Sin repositorio Git: cuando hagas `git init`, ejecuta `python .brain/guardianes/secretos.py --instalar-hook`.")
    return hechos


def _ejecutar(args, destino, entrada=None, timeout=90):
    env = dict(os.environ, CEREBRO_SIN_PODA="1", PYTHONIOENCODING="utf-8")
    return subprocess.run(args, cwd=destino, capture_output=True, text=True, encoding="utf-8", errors="replace",
                          input=entrada, stdin=None if entrada is not None else subprocess.DEVNULL, timeout=timeout, env=env)


def comprobar(destino):
    """[(guardián, funciona, frase en lenguaje llano)] de un proyecto con el kit instalado."""
    destino = os.path.abspath(destino)
    gd = os.path.join(destino, ".brain", "guardianes")
    res = []

    def probar(nombre, args, entrada=None, ok=lambda r: r.returncode == 0, bien="funciona", mal="falló"):
        try:
            r = _ejecutar(args, destino, entrada)
            correcto = ok(r)
            res.append((nombre, correcto, bien if correcto else "%s: %s" % (mal, (r.stderr or r.stdout).strip()[-200:])))
        except Exception as e:
            res.append((nombre, False, "%s: %s" % (mal, e)))

    if os.path.exists(os.path.join(destino, "tests", "test_paridad_idiomas.py")):
        probar("Idiomas (kit de traducción)", [sys.executable, "-m", "unittest", "tests.test_paridad_idiomas"],
               bien="todos los idiomas tienen las mismas frases", mal="faltan traducciones")
    if not os.path.isdir(gd):
        return res + [("Guardianes", False, "No están instalados (nivel ligero o medio, o falta el kit).")]
    for g in GUARDIANES:
        ruta = os.path.join(gd, g + ".py")
        try:
            compile(leer(ruta), ruta, "exec")
        except Exception as e:
            res.append((g, False, "no se puede leer el guardián: %s" % e))
    py = sys.executable
    probar("Resumen de arranque", [py, os.path.join(gd, "arranque.py"), "--manual"],
           ok=lambda r: r.returncode == 0 and "Cerebro Vivo" in r.stdout, bien="se muestra al abrir un chat")
    probar("Aviso de cierre", [py, os.path.join(gd, "cierre.py")], entrada='{"stop_hook_active": true}', bien="no rompe el fin de respuesta")
    probar("Secretos", [py, os.path.join(gd, "secretos.py"), "--ver"], bien="escanea sin errores")
    probar("Memoria de pruebas", [py, os.path.join(gd, "pruebas.py")], bien="lee el índice sin errores")
    probar("Índices de la memoria (tests)", [py, "-m", "unittest", "tests.test_cerebro_indices"], bien="los índices y topes están en orden", mal="hay incoherencias")
    ajustes = os.path.join(destino, ".claude", "settings.json")
    try:
        h = json.dumps(json.loads(leer(ajustes))["hooks"])
        res.append(("Hooks de Claude Code", "arranque.py" in h and "cierre.py" in h, "configurados en .claude/settings.json" if "arranque.py" in h and "cierre.py" in h else "faltan en .claude/settings.json"))
    except Exception:
        res.append(("Hooks de Claude Code", False, "falta .claude/settings.json (hay que reiniciar Claude Code tras crearlo)"))
    return res


def pedir(valor, pregunta, defecto):
    if valor:
        return valor
    if sys.stdin.isatty():
        try:
            return input("%s [%s]: " % (pregunta, defecto)).strip() or defecto
        except EOFError:  # sin teclado (p. ej. NUL en Windows): se usa el valor por defecto
            return defecto
    return defecto


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Instala el kit de arranque de Cerebro Vivo")
    ap.add_argument("destino")
    ap.add_argument("--nombre")
    ap.add_argument("--dueno")
    ap.add_argument("--idioma")
    ap.add_argument("--pruebas")
    ap.add_argument("--ias")
    ap.add_argument("--nivel", choices=NIVELES)
    ap.add_argument("--traduccion", action="store_true", help="añade el kit de traducción es/en/pt (static/i18n/)")
    ap.add_argument("--comprobar", action="store_true", help="comprueba un proyecto ya instalado")
    a = ap.parse_args()
    if a.comprobar:
        resultados = comprobar(a.destino)
        for nombre, ok, frase in resultados:
            print("%s %s: %s" % ("✅" if ok else "❌", nombre, frase))
        return 0 if all(ok for _, ok, _ in resultados) else 1
    nivel = pedir(a.nivel, "Nivel (ligero/medio/completo)", "completo")
    ias = [i.strip() for i in pedir(a.ias, "IA que se usarán (claude,gemini,codex)", "claude").split(",") if i.strip()]
    if nivel not in NIVELES or not ias or any(i not in IAS for i in ias):
        print("Nivel o IA no válidos. Niveles: %s. IA: %s." % (", ".join(NIVELES), ", ".join(IAS)))
        return 2
    try:
        hechos = instalar(a.destino, pedir(a.nombre, "Nombre del proyecto", os.path.basename(os.path.abspath(a.destino))),
                          pedir(a.dueno, "Nombre del dueño", "el dueño"), pedir(a.idioma, "Idioma de las respuestas", "español"),
                          pedir(a.pruebas, "Comando de pruebas", "python -m unittest discover tests"), ias, nivel,
                          traduccion=a.traduccion)
    except ValueError as e:
        print("❌ %s" % e)
        return 2
    print("Kit instalado (nivel %s): %d archivo(s) creados, %d fusionados con lo que ya tenías, %d ya existían y no se tocaron." % (nivel, len(hechos["creados"]), len(hechos["fusionados"]), len(hechos["respetados"])))
    if hechos["fusionados"]:
        print("- Reinicia Claude Code en el proyecto para que cuenten los cambios en .claude/settings.json.")
    for t in hechos["avisos"]:
        print("- " + t)
    if nivel == "completo":
        print("Siguiente paso: reiniciar Claude Code en el proyecto y ejecutar `instalar.py --comprobar`.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
