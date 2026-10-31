#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Actualiza un proyecto con las mejoras del arnés desde este repo.

    python actualizar.py RUTA_DEL_PROYECTO --simular     (mira qué cambiaría)
    python actualizar.py RUTA_DEL_PROYECTO               (actualiza, con copia de seguridad)

Es la misma lógica que `actualizar_arnes.py` dentro de cada proyecto (ver ese archivo para las reglas)."""

import importlib.util
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
_espec = importlib.util.spec_from_file_location("actualizar_arnes", os.path.join(RAIZ, ".brain", "guardianes", "actualizar_arnes.py"))
actualizador = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(actualizador)

if __name__ == "__main__":
    sys.exit(actualizador.main(repo=RAIZ))
