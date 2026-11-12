# -*- coding: utf-8 -*-
"""Spec 042: `/colabora` (modo colaborativo) e `indices_ajenos` (R12)."""
import importlib.util
import json
import os
import shutil
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def cargar(nombre, ruta):
    e = importlib.util.spec_from_file_location(nombre, os.path.join(RAIZ, *ruta))
    m = importlib.util.module_from_spec(e)
    e.loader.exec_module(m)
    return m


colabora = cargar("colabora_g", [".brain", "guardianes", "colabora.py"])
act = cargar("actualizar_arnes_c", [".brain", "guardianes", "actualizar_arnes.py"])

INDICE = "# Indice\n\n## Memoria\n* **Al iniciar:** leer.\n* **Pendientes:** [`.brain/pendientes.md`](.brain/pendientes.md) lista.\n* **Registro:** x\n"


def escribir(base, rel, texto):
    ruta = os.path.join(base, *rel.split("/"))
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        f.write(texto)


def leer(base, rel):
    with open(os.path.join(base, *rel.split("/")), encoding="utf-8", newline="") as f:
        return f.read()


class ColaboraTest(unittest.TestCase):
    def setUp(self):
        self.p = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.p, True)
        escribir(self.p, "CLAUDE.md", INDICE)
        escribir(self.p, "AGENTS.md", INDICE)
        escribir(self.p, ".brain/guardianes/guardianes.json", json.dumps({"idioma": "es"}))
        escribir(self.p, ".brain/biblioteca/IAS_COLABORATIVAS.md", "# Plantilla es\n")
        escribir(self.p, ".brain/biblioteca/IAS_COLABORATIVAS.en.md", "# Template en\n")

    def cfg(self):
        return json.loads(leer(self.p, ".brain/guardianes/guardianes.json"))

    def test_apagado_por_defecto_y_estado_no_cambia_nada(self):
        cod, lineas = colabora.modo(self.p, "estado")
        self.assertEqual(cod, 0)
        self.assertIn("DESACTIVADO", lineas[0])
        self.assertNotIn("modo_colaborativo", self.cfg())
        self.assertNotIn("colaboracion.md", leer(self.p, "CLAUDE.md"))

    def test_si_crea_archivo_y_una_linea_en_cada_indice(self):
        cod, lineas = colabora.modo(self.p, "si")
        self.assertEqual(cod, 0)
        self.assertIn("ACTIVADO", lineas[0])
        self.assertTrue(self.cfg()["modo_colaborativo"])
        self.assertEqual(leer(self.p, ".brain/colaboracion.md"), "# Plantilla es\n")
        for nombre in ("CLAUDE.md", "AGENTS.md"):
            self.assertEqual(sum(1 for l in leer(self.p, nombre).split("\n") if ".brain/colaboracion.md" in l), 1)
        # la línea va antes de «Pendientes», como el resto de remites
        self.assertLess(leer(self.p, "CLAUDE.md").index("colaboracion.md"), leer(self.p, "CLAUDE.md").index("* **Pendientes:**"))

    def test_si_es_idempotente(self):
        colabora.modo(self.p, "si")
        antes = leer(self.p, "CLAUDE.md")
        colabora.modo(self.p, "si")
        self.assertEqual(leer(self.p, "CLAUDE.md"), antes)

    def test_si_no_pisa_un_colaboracion_existente(self):
        escribir(self.p, ".brain/colaboracion.md", "# Mío\n")
        colabora.modo(self.p, "si")
        self.assertEqual(leer(self.p, ".brain/colaboracion.md"), "# Mío\n")

    def test_en_ingles_usa_la_plantilla_y_el_texto_en_ingles(self):
        escribir(self.p, ".brain/guardianes/guardianes.json", json.dumps({"idioma": "en"}))
        cod, lineas = colabora.modo(self.p, "si")
        self.assertEqual(leer(self.p, ".brain/colaboracion.md"), "# Template en\n")
        self.assertIn("Collaborative mode: ON", lineas[0])

    def test_no_quita_las_lineas_y_conserva_el_archivo(self):
        colabora.modo(self.p, "si")
        colabora.modo(self.p, "no")
        self.assertFalse(self.cfg()["modo_colaborativo"])
        self.assertEqual(leer(self.p, "CLAUDE.md"), INDICE)
        self.assertTrue(os.path.isfile(os.path.join(self.p, ".brain", "colaboracion.md")))

    def test_indices_ajenos_no_se_tocan_y_se_avisa(self):
        escribir(self.p, ".brain/guardianes/guardianes.json", json.dumps({"idioma": "es", "indices_ajenos": ["AGENTS.md"]}))
        cod, lineas = colabora.modo(self.p, "si")
        self.assertEqual(leer(self.p, "AGENTS.md"), INDICE)
        self.assertIn("colaboracion.md", leer(self.p, "CLAUDE.md"))
        self.assertTrue(any("AGENTS.md" in l for l in lineas[1:]))

    def test_palabra_desconocida(self):
        cod, lineas = colabora.modo(self.p, "quizas")
        self.assertEqual(cod, 1)


class IndicesAjenosTest(unittest.TestCase):
    def setUp(self):
        self.p = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.p, True)
        escribir(self.p, "CLAUDE.md", INDICE)
        escribir(self.p, "AGENTS.md", INDICE)
        escribir(self.p, ".brain/biblioteca/kit-arranque/plantillas/objetivo.md", "# Objetivo de {{NOMBRE}}\n\n> {{DUENO}}\n")
        escribir(self.p, ".brain/constitution.md", "# C\n\n1. **Idioma:** es.\n")

    def test_sin_ajuste_se_comporta_como_siempre(self):
        self.assertEqual(act.indices_ajenos(self.p), set())
        act.migrar_objetivo(self.p)
        self.assertIn("objetivo.md", leer(self.p, "AGENTS.md"))

    def test_el_actualizador_no_toca_un_indice_ajeno(self):
        escribir(self.p, ".brain/guardianes/guardianes.json", json.dumps({"indices_ajenos": ["AGENTS.md"]}))
        self.assertEqual(act.indices_ajenos(self.p), {"AGENTS.md"})
        act.migrar_objetivo(self.p)
        self.assertEqual(leer(self.p, "AGENTS.md"), INDICE)
        self.assertIn("objetivo.md", leer(self.p, "CLAUDE.md"))

    def test_json_roto_o_de_otro_tipo_no_rompe(self):
        escribir(self.p, ".brain/guardianes/guardianes.json", "{no es json")
        self.assertEqual(act.indices_ajenos(self.p), set())
        escribir(self.p, ".brain/guardianes/guardianes.json", json.dumps({"indices_ajenos": "AGENTS.md"}))
        self.assertEqual(act.indices_ajenos(self.p), set())


class PlantillaYTextosTest(unittest.TestCase):
    def test_los_textos_estan_en_los_dos_idiomas(self):
        textos = cargar("textos_c", [".brain", "guardianes", "textos.py"])
        for clave in ("colabora_si", "colabora_no", "colabora_uso", "colabora_falta_plantilla", "colabora_falta_archivo",
                      "colabora_indice_ajeno", "colabora_linea_titulo", "arranque_modo_colaborativo"):
            for idioma in ("es", "en"):
                args = ("X",) if clave == "colabora_indice_ajeno" else ()
                self.assertTrue(textos.t({"idioma": idioma}, clave, *args).strip(), (clave, idioma))


if __name__ == "__main__":
    unittest.main()
