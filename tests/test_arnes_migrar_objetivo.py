# -*- coding: utf-8 -*-
"""Spec 008: `--migrar-objetivo` en un proyecto ya instalado."""
import importlib.util
import os
import shutil
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_espec = importlib.util.spec_from_file_location("actualizar_arnes", os.path.join(RAIZ, ".brain", "guardianes", "actualizar_arnes.py"))
act = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(act)

INDICE = "# Indice\n\n## Memoria\n* **Al iniciar:** leer.\n* **Pendientes:** [`.brain/pendientes.md`](.brain/pendientes.md) lista.\n* **Registro:** x\n"
CONSTITUCION = "# Constitucion\n\n1. **Idioma:** es.\n2. **Alcance:** poco.\n"


def escribir(base, rel, texto, nl=""):
    ruta = os.path.join(base, *rel.split("/"))
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline=nl) as f:
        f.write(texto)


def leer(base, rel):
    with open(os.path.join(base, *rel.split("/")), encoding="utf-8", newline="") as f:
        return f.read()


class TestMigrarObjetivo(unittest.TestCase):
    def setUp(self):
        self.p = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.p, True)
        escribir(self.p, "CLAUDE.md", INDICE)
        escribir(self.p, "AGENTS.md", INDICE)
        escribir(self.p, ".brain/constitution.md", CONSTITUCION)
        escribir(self.p, ".brain/biblioteca/kit-arranque/plantillas/objetivo.md", "# Objetivo de {{NOMBRE}}\n\n> {{DUENO}}\n")

    def test_simular_no_escribe_nada(self):
        res = act.migrar_objetivo(self.p, simular=True)
        self.assertIn(".brain/architecture/objetivo.md".replace("/", os.sep), res["creados"])
        self.assertEqual(sorted(res["modificados"]), sorted(["CLAUDE.md", "AGENTS.md", os.path.join(".brain", "constitution.md")]))
        self.assertFalse(os.path.exists(os.path.join(self.p, ".brain", "architecture", "objetivo.md")))
        self.assertEqual(leer(self.p, "CLAUDE.md"), INDICE)

    def test_crea_enlaza_y_añade_la_regla_con_copia(self):
        act.migrar_objetivo(self.p)
        self.assertTrue(os.path.isfile(os.path.join(self.p, ".brain", "architecture", "objetivo.md")))
        texto = leer(self.p, "CLAUDE.md")
        self.assertLess(texto.index("architecture/objetivo.md"), texto.index("**Pendientes:**"))
        self.assertEqual(texto.count("architecture/objetivo.md"), 2)  # texto del enlace y su ruta, en una sola línea
        self.assertIn("3. **El objetivo se escribe:**", leer(self.p, ".brain/constitution.md"))
        copias = os.path.join(self.p, ".brain", "copias_arnes")
        self.assertTrue(os.path.isdir(copias) and os.listdir(copias))

    def test_es_idempotente(self):
        act.migrar_objetivo(self.p)
        despues = {r: leer(self.p, r) for r in ("CLAUDE.md", "AGENTS.md", ".brain/constitution.md")}
        res = act.migrar_objetivo(self.p)
        self.assertEqual((res["creados"], res["modificados"]), ([], []))
        self.assertEqual({r: leer(self.p, r) for r in despues}, despues)

    def test_no_pisa_un_objetivo_ya_escrito(self):
        escribir(self.p, ".brain/architecture/objetivo.md", "mi objetivo real\n")
        act.migrar_objetivo(self.p)
        self.assertEqual(leer(self.p, ".brain/architecture/objetivo.md"), "mi objetivo real\n")

    def test_indice_sin_sitio_se_avisa_y_no_se_toca(self):
        escribir(self.p, "GEMINI.md", "# solo texto\n")
        res = act.migrar_objetivo(self.p)
        self.assertTrue(any("GEMINI.md" in a for a in res["avisos"]))
        self.assertEqual(leer(self.p, "GEMINI.md"), "# solo texto\n")

    def test_respeta_los_saltos_de_linea_de_windows(self):
        escribir(self.p, "CLAUDE.md", INDICE.replace("\n", "\r\n"), nl="")
        act.migrar_objetivo(self.p)
        texto = leer(self.p, "CLAUDE.md")
        self.assertNotIn("\n\n".replace("\n", "\r"), texto.replace("\r\n", ""))
        self.assertEqual(texto.count("\r\n"), texto.count("\n"))

    def test_sin_plantilla_avisa(self):
        os.remove(os.path.join(self.p, ".brain", "biblioteca", "kit-arranque", "plantillas", "objetivo.md"))
        res = act.migrar_objetivo(self.p)
        self.assertEqual(res["creados"], [])
        self.assertTrue(any("plantilla" in a for a in res["avisos"]))


if __name__ == "__main__":
    unittest.main()
