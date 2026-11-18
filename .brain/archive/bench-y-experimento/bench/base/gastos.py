# -*- coding: utf-8 -*-
"""Resumen de gastos desde un CSV (fecha,categoria,importe)."""
import argparse
import csv


def leer(ruta):
    with open(ruta, encoding="utf-8", newline="") as f:
        return [{"fecha": r["fecha"], "categoria": r["categoria"], "importe": float(r["importe"])} for r in csv.DictReader(f)]


def por_categoria(gastos):
    totales = {}
    for g in gastos:
        totales[g["categoria"]] = totales.get(g["categoria"], 0) + g["importe"]
    return totales


def resumen(gastos):
    lineas = ["%-12s %9.2f" % (c, t) for c, t in sorted(por_categoria(gastos).items())]
    lineas.append("%-12s %9.2f" % ("TOTAL", sum(g["importe"] for g in gastos)))
    return "\n".join(lineas)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Resumen de gastos")
    ap.add_argument("archivo")
    a = ap.parse_args(argv)
    print(resumen(leer(a.archivo)))


if __name__ == "__main__":
    main()
