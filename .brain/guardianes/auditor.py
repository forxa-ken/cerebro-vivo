#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auditor (spec 044): quién audita y cómo se llama a la IA externa. Solo librería estándar.

  python .brain/guardianes/auditor.py estado
  python .brain/guardianes/auditor.py externo general-y-spec|siempre|no|estado
  python .brain/guardianes/auditor.py cierre si|no|estado
  python .brain/guardianes/auditor.py quien general|cierre|spec [archivos…]   (quién audita; con archivos sensibles sugiere el externo)
  python .brain/guardianes/auditor.py codex                       (el comando de Codex, en una línea)

No lanza ninguna IA: solo guarda los ajustes y dice quién debe auditar y con qué comando. Lo lanza la IA
con la skill `auditor`. Con `auditor_externo` en «no» no se llama a ninguna IA externa."""
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, AQUI)
from textos import t  # noqa: E402

EXTERNO_VALORES = ("general-y-spec", "siempre", "no")
EXTERNO_DEFECTO = "general-y-spec"
CLAVE_EXTERNO = {"general-y-spec": "auditor_externo_general_y_spec", "siempre": "auditor_externo_siempre",
                 "no": "auditor_externo_no"}
SI = ("si", "sí", "on", "yes", "true", "1", "verdadero", "activar", "activa")
NO = ("no", "off", "false", "0", "falso", "desactivar", "desactiva")
EXT_DOCS = (".md", ".txt", ".log", ".rst")
NOMBRES_DOCS = ("readme", "license", "licence", "notice", "changelog", "cambios", "authors", "contributing")
SEGURO = re.compile(r"^[A-Za-z0-9._:/][A-Za-z0-9._:/-]{0,63}$")  # sin «-» delante: no puede pasar por opción


def _cfg(raiz):
    """(ruta, ajustes, legible). Si el archivo existe pero no se puede leer (JSON roto, raíz que no es objeto),
    `legible` es False y NO se debe escribir encima: se perdería el resto de los ajustes. Acepta BOM."""
    ruta = os.path.join(raiz, ".brain", "guardianes", "guardianes.json")
    if not os.path.exists(ruta):
        return ruta, {}, True
    try:
        with open(ruta, "rb") as f:
            cfg = json.loads(f.read().decode("utf-8-sig"))
    except Exception:  # OSError, JSON roto, RecursionError por anidado enorme…
        return ruta, {}, False
    return (ruta, cfg, True) if isinstance(cfg, dict) else (ruta, {}, False)


def _guardar(ruta, cfg):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta + ".tmp", "wb") as f:
        f.write((json.dumps(cfg, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    os.replace(ruta + ".tmp", ruta)


def valor_externo(cfg):
    v = str(cfg.get("auditor_externo", EXTERNO_DEFECTO)).strip().lower()
    return v if v in EXTERNO_VALORES else EXTERNO_DEFECTO


def cierre_activo(cfg):
    """Valor único de `auditor_cierre` para todo el arnés: verdadero por defecto (spec 044). Acepta booleanos y
    textos como «false»/«no»/«0»."""
    v = cfg.get("auditor_cierre", True)
    if isinstance(v, str):
        return v.strip().lower() not in NO
    return bool(v) if v is not None else True


def sensible(archivos, cfg):
    """True si algún archivo toca algo de `revision_sensibles` (pagos, auth, secretos, despliegue…)."""
    claves = cfg.get("revision_sensibles", [])
    claves = [str(c).lower() for c in claves] if isinstance(claves, (list, tuple)) else []
    return any(c and c in str(a).lower() for a in archivos or [] for c in claves)


def quien_audita(cfg, modo, archivos=None):
    """Lista de ejecutores para un modo: 'general', 'cierre' (rutinario) o 'spec' (cierre de spec de la fábrica).
    Siempre el interno; el externo entra en general y spec, y en cierre solo con `siempre`. Con `no`, nunca.
    Con `general-y-spec` y archivos sensibles en un cierre, se SUGIERE el externo («externo?»: lo decide la IA/Darwin)."""
    externo = valor_externo(cfg)
    quienes = ["interno"]
    if externo == "siempre" or (externo == "general-y-spec" and modo in ("general", "spec")):
        quienes.append("externo")
    elif externo == "general-y-spec" and modo == "cierre" and sensible(archivos, cfg):
        quienes.append("externo?")
    return quienes


def _seguro(valor, defecto):
    """El valor entra en una línea de comandos: solo letras, cifras y . _ : / - ; si no, el valor por defecto."""
    v = str(valor).strip() if valor is not None else ""
    return v if SEGURO.match(v) else defecto


def comando_codex(cfg, plataforma=None):
    """Argumentos de `codex exec` para auditar en solo lectura. En Windows el sandbox por defecto de Codex no
    puede ejecutar python: se pasa `windows.sandbox="unelevated"` (comprobado en la spec 044).
    La tarea se pasa por la entrada estándar (`-`)."""
    plataforma = sys.platform if plataforma is None else plataforma
    modelo = _seguro(cfg.get("auditor_modelo_externo"), "gpt-6-sol")
    esfuerzo = _seguro(cfg.get("auditor_esfuerzo"), "medium")
    args = ["codex", "exec", "-m", modelo, "-c", "model_reasoning_effort=" + esfuerzo]
    if plataforma.startswith("win"):
        args += ["-c", 'windows.sandbox="unelevated"']
    args += ["-s", "read-only", "--skip-git-repo-check", "-"]
    return args


def modo(raiz, aspecto, orden):
    """Devuelve (código, líneas). `aspecto`: 'externo', 'cierre' o 'estado'. 0 = bien, 1 = palabra desconocida."""
    ruta, cfg, legible = _cfg(raiz)
    orden = (orden or "estado").strip().lower()
    cambia = aspecto in ("externo", "cierre") and orden != "estado"
    if cambia and not legible:  # no pisar un archivo que no se pudo leer: se perderían los demás ajustes
        return 1, [t(cfg, "auditor_config_ilegible", ruta)]
    if aspecto == "externo" and orden != "estado":
        if orden not in EXTERNO_VALORES:
            return 1, [t(cfg, "auditor_uso")]
        cfg["auditor_externo"] = orden
        _guardar(ruta, cfg)
    elif aspecto == "cierre" and orden != "estado":
        if orden in SI:
            cfg["auditor_cierre"] = True
        elif orden in NO:
            cfg["auditor_cierre"] = False
        else:
            return 1, [t(cfg, "auditor_uso")]
        _guardar(ruta, cfg)
    elif aspecto not in ("externo", "cierre", "estado"):
        return 1, [t(cfg, "auditor_uso")]
    lineas = [] if legible else [t(cfg, "auditor_config_ilegible", ruta)]  # estado: avisa de que lo mostrado es el defecto
    lineas += [t(cfg, "auditor_cierre_si" if cierre_activo(cfg) else "auditor_cierre_no"),
              t(cfg, CLAVE_EXTERNO[valor_externo(cfg)]),
              t(cfg, "auditor_modelos", _seguro(cfg.get("auditor_modelo"), "sonnet"),
                _seguro(cfg.get("auditor_modelo_externo"), "gpt-6-sol"), _seguro(cfg.get("auditor_esfuerzo"), "medium"))]
    return 0, lineas


def hay_codigo(archivos, cfg):
    """True si entre los archivos hay código o configuración (no solo documentos). Tolera ajustes mal escritos
    (tipos raros) y no cuenta README/LICENSE/CHANGELOG sin extensión como código."""
    docs = cfg.get("auditor_ignorar_extensiones", EXT_DOCS)
    if isinstance(docs, (list, tuple)):  # «» casaría con todo y «md» con «.cmd»: se descartan vacíos y se exige el punto
        docs = tuple("." + str(x).strip().lower().lstrip(".") for x in docs if str(x).strip().lstrip("."))
    docs = docs if isinstance(docs, tuple) and docs else EXT_DOCS

    def es_codigo(a):
        a = str(a).replace("\\", "/").lower()
        base = a.rsplit("/", 1)[-1]
        return bool(a) and not a.endswith(docs) and base not in NOMBRES_DOCS
    return any(es_codigo(a) for a in archivos or [] if a)


def main(argv=None, raiz=None):
    argv = sys.argv[1:] if argv is None else argv
    raiz = RAIZ if raiz is None else raiz
    aspecto = argv[0].lower() if argv else "estado"
    _, cfg, _ = _cfg(raiz)
    if aspecto == "quien":
        m = (argv[1] if len(argv) > 1 else "").lower()
        if m not in ("general", "cierre", "spec"):
            print(t(cfg, "auditor_uso"))
            return 1
        print(" + ".join(quien_audita(cfg, m, argv[2:])))
        return 0
    if aspecto == "codex":
        print(" ".join(a if " " not in a else '"' + a + '"' for a in comando_codex(cfg)))
        return 0
    codigo, lineas = modo(raiz, aspecto, argv[1] if len(argv) > 1 else "estado")
    for l in lineas:
        print(l)
    return codigo


if __name__ == "__main__":
    sys.exit(main())
