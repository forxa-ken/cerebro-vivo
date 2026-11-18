#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prepara la carpeta gemela de una ejecución (spec 001, parte A). Las carpetas viven FUERA del repo
(si no, el CLAUDE.md del repo contaminaría el lado SIN).

Uso:  python bench/montar.py con|sin t1|t2|t3 [--destino RUTA]
Lo que hubiera en la carpeta se MUEVE a `_historial/` (no se borra). Imprime el texto exacto a pegar en el chat nuevo."""
import argparse
import os
import re
import shutil
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
DESTINO = os.path.join(os.path.dirname(REPO), "bench-cerebro")
PROMPTS = {
    "t1": "[T1] En este proyecto, añade la opción `--min IMPORTE` a la línea de comandos de `gastos.py`: solo cuenta los gastos con importe mayor o igual a ese valor. Añade su prueba.",
    "t2": "[T2] El resumen de `datos/ejemplo.csv` sale con categorías duplicadas (Comida y comida, Transporte con espacio delante). Arréglalo y añade una prueba.",
    "t3": "[T3] Termina lo que quedó a medias en este proyecto (la exportación a JSON).",
}
CLAUDE_SIN = "# Proyecto gastos\nResumen de gastos desde un CSV. Responde en español.\nPruebas: `python -m unittest discover tests`\n"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("lado", choices=["con", "sin"])
    ap.add_argument("tarea", choices=sorted(PROMPTS))
    ap.add_argument("--destino", default=DESTINO)
    a = ap.parse_args(argv)
    carpeta = os.path.normpath(os.path.join(a.destino, a.lado + "_arnes"))
    os.makedirs(carpeta, exist_ok=True)
    viejos = [n for n in os.listdir(carpeta) if n != ".git"]  # .git se queda (puede estar en uso); se vuelve a confirmar el punto de partida
    if viejos:
        hist = os.path.join(a.destino, "_historial", "%s_arnes-%s" % (a.lado, time.strftime("%Y%m%d-%H%M%S")))
        n_ = 1
        while os.path.exists(hist):
            n_ += 1
            hist = hist.split("+")[0] + "+%d" % n_
        os.makedirs(hist)
        for n in viejos:
            os.rename(os.path.join(carpeta, n), os.path.join(hist, n))  # rename: mismo disco, y .git tiene archivos de solo lectura
    shutil.copytree(os.path.join(AQUI, "base"), carpeta, dirs_exist_ok=True)
    if a.tarea == "t3":
        with open(os.path.join(carpeta, "gastos.py"), "a", encoding="utf-8") as f, open(os.path.join(AQUI, "tarea3", "gastos_parche.py"), encoding="utf-8") as p:
            f.write(p.read())
        shutil.copy(os.path.join(AQUI, "tarea3", "tests", "test_exportar.py"), os.path.join(carpeta, "tests", "test_exportar.py"))
    if a.lado == "con":
        r = subprocess.run([sys.executable, os.path.join(REPO, ".brain", "biblioteca", "kit-arranque", "instalar.py"), carpeta,
                            "--nombre", "Gastos", "--dueno", "Darwin", "--nivel", "completo"], capture_output=True, text=True)
        if r.returncode:
            print(r.stdout, r.stderr)
            return 1
        if a.tarea == "t3":
            shutil.copy(os.path.join(AQUI, "tarea3", "traspaso_con.md"), os.path.join(carpeta, ".brain", "traspaso.md"))
    else:
        with open(os.path.join(carpeta, "CLAUDE.md"), "w", encoding="utf-8") as f:
            f.write(CLAUDE_SIN)
    subprocess.run(["git", "init", "-q"], cwd=carpeta)
    subprocess.run(["git", "add", "-A"], cwd=carpeta)
    subprocess.run(["git", "-c", "user.name=bench", "-c", "user.email=b@b", "commit", "-qm", "punto de partida " + time.strftime("%H%M%S")], cwd=carpeta)
    print("Carpeta lista: %s\nAbre un chat NUEVO ahí (mismo modelo y esfuerzo en los dos lados) y pega:\n\n%s\n" % (carpeta, PROMPTS[a.tarea]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
