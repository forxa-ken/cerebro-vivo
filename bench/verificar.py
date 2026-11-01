#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Dice si una ejecución de la prueba lo logró (prueba oculta en bench/hechas/) y si sus pruebas propias pasan.
Uso:  python bench/verificar.py con|sin t1|t2|t3 [--destino RUTA]"""
import argparse
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from montar import DESTINO  # noqa: E402


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("lado", choices=["con", "sin"])
    ap.add_argument("tarea", choices=["t1", "t2", "t3"])
    ap.add_argument("--destino", default=DESTINO)
    a = ap.parse_args(argv)
    carpeta = os.path.join(a.destino, a.lado + "_arnes")
    meta = subprocess.run([sys.executable, os.path.join(AQUI, "hechas", a.tarea + ".py"), carpeta])
    propias = subprocess.run([sys.executable, "-m", "unittest", "discover", "tests"], cwd=carpeta, capture_output=True, text=True)
    print("Pruebas propias del proyecto:", "pasan" if propias.returncode == 0 else "FALLAN")
    return meta.returncode


if __name__ == "__main__":
    sys.exit(main())
