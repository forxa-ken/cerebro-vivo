# -*- coding: utf-8 -*-
"""Spec 048: la poda de memoria mueve (no borra) lo terminado y no deja enlaces rotos."""

import importlib.util
import os
import shutil
import subprocess
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GUARDIANES = os.path.join(RAIZ, ".brain", "guardianes")


def cargar_poda():
    spec = importlib.util.spec_from_file_location("poda", os.path.join(GUARDIANES, "poda.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def leer(raiz, rel):
    with open(os.path.join(raiz, rel), encoding="utf-8") as f:
        return f.read()


class TestPoda(unittest.TestCase):

    def montar(self):
        raiz = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, raiz, True)

        def g(*a):
            subprocess.run(["git"] + list(a), cwd=raiz, check=True, capture_output=True)

        def w(rel, txt):
            ruta = os.path.join(raiz, rel)
            os.makedirs(os.path.dirname(ruta), exist_ok=True)
            with open(ruta, "w", encoding="utf-8", newline="") as f:
                f.write(txt)

        g("init", "-q")
        g("config", "user.email", "t@t")
        g("config", "user.name", "t")
        w(".brain/pendientes.md", "# P\n- **9:** algo de la spec 003\n")
        w(".brain/specs/001-vieja.md",
          "# Spec 001: Vieja\n- **Estado:** implementada\nVer [otra](002-nueva.md) y [arq](../architecture/a.md)\n")
        w(".brain/specs/002-nueva.md", "# Spec 002\n- **Estado:** implementada (pendiente prueba de Darwin)\n")
        w(".brain/specs/003-citada.md", "# Spec 003\n- **Estado:** implementada\n")
        w(".brain/architecture/a.md", "# A\nMira [la vieja](../specs/001-vieja.md) y `specs/001-vieja.md`\n")
        w(".brain/decisions/D-001-parcial.md", "# D\n- **Estado:** reemplazada por D-002 (solo la parte de datos)\n")
        w(".brain/decisions/D-002-total.md", "# D\n- **Estado:** reemplazada por D-003\n")
        g("add", ".")
        g("commit", "-q", "-m", "a")
        return raiz

    def test_solo_se_eligen_las_terminadas_y_no_citadas(self):
        poda = cargar_poda()
        raiz = self.montar()
        origenes = [o for o, _ in poda.candidatas(raiz)]
        self.assertEqual(origenes, [".brain/specs/001-vieja.md", ".brain/decisions/D-002-total.md"])

    def test_aplicar_mueve_sin_borrar_y_sin_enlaces_rotos(self):
        poda = cargar_poda()
        raiz = self.montar()
        n, error = poda.aplicar(raiz, poda.candidatas(raiz))
        self.assertEqual((n, error), (2, None))
        self.assertFalse(os.path.exists(os.path.join(raiz, ".brain/specs/001-vieja.md")))
        movida = leer(raiz, ".brain/specs/archivo/001-vieja.md")
        self.assertIn("](../002-nueva.md)", movida)
        self.assertIn("](../../architecture/a.md)", movida)
        arq = leer(raiz, ".brain/architecture/a.md")
        self.assertIn("](../specs/archivo/001-vieja.md)", arq)
        self.assertEqual(poda.enlaces_rotos(raiz), set())
        self.assertIn("001-vieja", leer(raiz, ".brain/specs/archivo/indice.md"))

    def test_con_cambios_sin_guardar_no_actua(self):
        poda = cargar_poda()
        raiz = self.montar()
        with open(os.path.join(raiz, ".brain/specs/001-vieja.md"), "a", encoding="utf-8") as f:
            f.write("cambio\n")
        self.assertIn("cambios sin guardar", poda.plan(raiz)["bloqueado"])

    def test_si_quedarian_enlaces_rotos_lo_deshace(self):
        poda = cargar_poda()
        raiz = self.montar()
        original = leer(raiz, ".brain/specs/001-vieja.md")
        poda.reescribir = lambda texto, *a: texto + "\n[roto](no-existe.md)\n"
        n, error = poda.aplicar(raiz, poda.candidatas(raiz))
        self.assertEqual(n, 0)
        self.assertIn("enlaces rotos", error)
        self.assertEqual(leer(raiz, ".brain/specs/001-vieja.md"), original)


if __name__ == "__main__":
    unittest.main()
