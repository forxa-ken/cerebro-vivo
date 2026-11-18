#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Resume una tanda de la re-medición (spec 003): verifica cada carpeta `bench-r/<tarea>-<n>/` y compara CON y SIN.
Uso:  python bench/agregar.py t1|t2|t3 [--base RUTA]"""
import argparse
import importlib.util
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
_e = importlib.util.spec_from_file_location("medir", os.path.join(REPO, ".brain", "guardianes", "medir.py"))
medir = importlib.util.module_from_spec(_e)
_e.loader.exec_module(medir)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("tarea", choices=["t1", "t2", "t3"])
    ap.add_argument("--base", default=os.path.join(os.path.dirname(REPO), "bench-r"))
    a = ap.parse_args(argv)
    chats = {"con": [], "sin": []}
    logrados = {"con": 0, "sin": 0}
    for n in range(1, 6):
        for lado in ("con", "sin"):
            destino = os.path.join(a.base, "%s-%d" % (a.tarea, n))
            if not os.path.isdir(os.path.join(destino, lado + "_arnes")):
                continue
            r = subprocess.run([sys.executable, os.path.join(AQUI, "verificar.py"), lado, a.tarea, "--destino", destino], capture_output=True)
            logrados[lado] += r.returncode == 0
            chats[lado] += medir.chats_de(medir.carpeta_de(os.path.join(destino, lado + "_arnes")))
    print("Logradas (prueba oculta): CON %d/%d, SIN %d/%d" % (logrados["con"], len(chats["con"]), logrados["sin"], len(chats["sin"])))
    medir.comparar(chats["con"], chats["sin"])
    for lado in ("con", "sin"):
        print("%s coste por chat: %s" % (lado.upper(), " ".join("%dk" % round(c["coste"] / 1000) for c in chats[lado])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
