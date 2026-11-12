#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auditor (spec 044): quién audita y cómo se llama a la IA externa. Solo librería estándar.

  python .brain/guardianes/auditor.py estado
  python .brain/guardianes/auditor.py externo general-y-spec|siempre|no|estado
  python .brain/guardianes/auditor.py cierre si|no|estado
  python .brain/guardianes/auditor.py quien general|cierre|spec   (quién audita en ese modo)
  python .brain/guardianes/auditor.py codex                       (el comando de Codex, en una línea)

No lanza ninguna IA: solo guarda los ajustes y dice quién debe auditar y con qué comando. Lo lanza la IA
con la skill `auditor`. Con `auditor_externo` en «no» no se llama a ninguna IA externa."""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, AQUI)
from textos import t  # noqa: E402

EXTERNO_VALORES = ("general-y-spec", "siempre", "no")
EXTERNO_DEFECTO = "general-y-spec"
CLAVE_EXTERNO = {"general-y-spec": "auditor_externo_general_y_spec", "siempre": "auditor_externo_siempre",
                 "no": "auditor_externo_no"}
SI = ("si", "sí", "on", "yes", "activar", "activa")
NO = ("no", "off", "desactivar", "desactiva")


def _cfg(raiz):
    ruta = os.path.join(raiz, ".brain", "guardianes", "guardianes.json")
    try:
        with open(ruta, "rb") as f:
            return ruta, json.loads(f.read().decode("utf-8"))
    except (OSError, ValueError):
        return ruta, {}


def _guardar(ruta, cfg):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta + ".tmp", "wb") as f:
        f.write((json.dumps(cfg, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    os.replace(ruta + ".tmp", ruta)


def valor_externo(cfg):
    v = str(cfg.get("auditor_externo", EXTERNO_DEFECTO)).strip().lower()
    return v if v in EXTERNO_VALORES else EXTERNO_DEFECTO


def quien_audita(cfg, modo):
    """Lista de ejecutores para un modo: 'general', 'cierre' (rutinario) o 'spec' (cierre de spec de la fábrica).
    Siempre el interno; el externo entra en general y spec, y en cierre solo con `siempre`. Con `no`, nunca."""
    externo = valor_externo(cfg)
    quienes = ["interno"]
    if externo == "siempre" or (externo == "general-y-spec" and modo in ("general", "spec")):
        quienes.append("externo")
    return quienes


def comando_codex(cfg, plataforma=None):
    """Argumentos de `codex exec` para auditar en solo lectura. En Windows el sandbox por defecto de Codex no
    puede ejecutar python: se pasa `windows.sandbox="unelevated"` (comprobado en la spec 044).
    La tarea se pasa por la entrada estándar (`-`)."""
    plataforma = sys.platform if plataforma is None else plataforma
    args = ["codex", "exec", "-m", str(cfg.get("auditor_modelo_externo", "gpt-6-sol")),
            "-c", "model_reasoning_effort=" + str(cfg.get("auditor_esfuerzo", "medium"))]
    if plataforma.startswith("win"):
        args += ["-c", 'windows.sandbox="unelevated"']
    args += ["-s", "read-only", "--skip-git-repo-check", "-"]
    return args


def modo(raiz, aspecto, orden):
    """Devuelve (código, líneas). `aspecto`: 'externo', 'cierre' o 'estado'. 0 = bien, 1 = palabra desconocida."""
    ruta, cfg = _cfg(raiz)
    orden = (orden or "estado").strip().lower()
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
    lineas = [t(cfg, "auditor_cierre_si" if cfg.get("auditor_cierre", True) else "auditor_cierre_no"),
              t(cfg, CLAVE_EXTERNO[valor_externo(cfg)]),
              t(cfg, "auditor_modelos", cfg.get("auditor_modelo", "sonnet"),
                cfg.get("auditor_modelo_externo", "gpt-6-sol"), cfg.get("auditor_esfuerzo", "medium"))]
    return 0, lineas


def hay_codigo(archivos, cfg):
    """True si entre los archivos hay código o configuración (no solo documentos)."""
    docs = tuple(str(x).lower() for x in cfg.get("auditor_ignorar_extensiones", [".md", ".txt", ".log", ".rst"]))
    return any(a and not a.lower().endswith(docs) for a in archivos)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    aspecto = argv[0].lower() if argv else "estado"
    _, cfg = _cfg(RAIZ)
    if aspecto == "quien":
        m = (argv[1] if len(argv) > 1 else "").lower()
        if m not in ("general", "cierre", "spec"):
            print(t(cfg, "auditor_uso"))
            return 1
        print(" + ".join(quien_audita(cfg, m)))
        return 0
    if aspecto == "codex":
        print(" ".join(a if " " not in a else '"' + a + '"' for a in comando_codex(cfg)))
        return 0
    codigo, lineas = modo(RAIZ, aspecto, argv[1] if len(argv) > 1 else "estado")
    for l in lineas:
        print(l)
    return codigo


if __name__ == "__main__":
    sys.exit(main())
