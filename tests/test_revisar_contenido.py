# -*- coding: utf-8 -*-
"""Spec 048 (pendiente 44): revisar_contenido.py avisa de páginas huérfanas, frases desfasadas y topes contradictorios."""
import datetime
import importlib.util
import os
import shutil
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_espec = importlib.util.spec_from_file_location("revisar_contenido", os.path.join(RAIZ, ".brain", "guardianes", "revisar_contenido.py"))
rc = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(rc)
HOY = datetime.date(2026, 11, 13)
CFG = {"idioma": "es"}


def poner(raiz, rel, texto):
    ruta = os.path.join(raiz, *rel.split("/"))
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)


class Base(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.d, True)
        poner(self.d, "VERSION", "2.0.0")

    def claves(self, cfg=None):
        return sorted(h["clave"] for h in rc.analizar(self.d, cfg or CFG)["hallazgos"])


class TestHuerfanas(Base):
    def test_pagina_que_nadie_enlaza_se_avisa_y_la_enlazada_no(self):
        poner(self.d, ".brain/lecciones/sola.md", "# sola\n")
        poner(self.d, ".brain/lecciones/viva.md", "# viva\n")
        poner(self.d, ".brain/lecciones/indice.md", "- [viva](viva.md)\n")
        self.assertEqual(self.claves(), ["huerfana:.brain/lecciones/sola.md"])

    def test_spec_enlazada_por_su_numero_no_es_huerfana(self):
        poner(self.d, ".brain/specs/007-algo.md", "# spec\n")
        poner(self.d, ".brain/pendientes.md", "Ver la spec 007.\n")
        self.assertEqual(self.claves(), [])

    def test_informe_citado_por_numero_o_en_el_registro_no_es_huerfano(self):
        poner(self.d, ".brain/specs/032-informe.md", "# informe\n")
        poner(self.d, ".brain/specs/011-otra.md", "# otra\n")
        poner(self.d, ".brain/decisions.log", "2026-11-03 | spec 011 | cerrada\n")
        poner(self.d, "CAMBIOS.md", "- Salió del informe 032.\n")
        self.assertEqual(self.claves(), [])

    def test_las_dos_ediciones_se_juzgan_juntas(self):
        poner(self.d, ".brain/biblioteca/GUIA.md", "# guia\n")
        poner(self.d, ".brain/biblioteca/GUIA.en.md", "# guide\n")
        self.assertEqual(self.claves(), ["huerfana:.brain/biblioteca/GUIA.en.md", "huerfana:.brain/biblioteca/GUIA.md"])
        poner(self.d, ".brain/pendientes.md", "Ver GUIA.md\n")
        self.assertEqual(self.claves(), [])

    def test_un_archivo_no_cuenta_como_enlace_de_si_mismo(self):
        poner(self.d, ".brain/lecciones/yo.md", "# yo\nyo.md\n")
        self.assertEqual(self.claves(), ["huerfana:.brain/lecciones/yo.md"])

    def test_archive_y_notas_de_chats_no_se_revisan(self):
        poner(self.d, ".brain/archive/viejo.md", "x")
        poner(self.d, ".brain/notas-chats/n.md", "x")
        self.assertEqual(self.claves(), [])


class TestDesfasadas(Base):
    def test_ruta_que_no_existe_en_architecture(self):
        poner(self.d, ".brain/architecture/a.md", "Usa `.brain/guardianes/viejo.py` y `.brain/guardianes/vivo.py`.\n")
        poner(self.d, ".brain/guardianes/vivo.py", "x = 1\n")
        poner(self.d, ".brain/pendientes.md", "architecture/a.md\n")
        self.assertEqual(self.claves(), ["ruta:.brain/architecture/a.md:.brain/guardianes/viejo.py"])

    def test_ejemplos_y_plantillas_no_cuentan(self):
        poner(self.d, ".brain/architecture/a.md", "Por ejemplo `.brain/x/viejo.py`; plantilla `.brain/lecciones/NNN.md`.\n")
        poner(self.d, ".brain/pendientes.md", "architecture/a.md\n")
        self.assertEqual(self.claves(), [])

    def test_version_actual_distinta_de_VERSION(self):
        poner(self.d, ".brain/biblioteca/M.md", "La versión actual del arnés es 1.9.0.\n")
        poner(self.d, ".brain/pendientes.md", "M.md\n")
        self.assertEqual(self.claves(), ["version:.brain/biblioteca/M.md:1.9.0"])

    def test_version_igual_no_avisa(self):
        poner(self.d, ".brain/biblioteca/M.md", "La versión actual del arnés es 2.0.0.\n")
        poner(self.d, ".brain/pendientes.md", "M.md\n")
        self.assertEqual(self.claves(), [])

    def test_cifra_de_skills_falsa(self):
        poner(self.d, ".claude/skills/uno/SKILL.md", "---\nname: uno\n---\n")
        poner(self.d, ".brain/biblioteca/M.md", "Hay 5 skills en el arnés.\n")
        poner(self.d, ".brain/pendientes.md", "M.md\n")
        self.assertEqual(self.claves(), ["cifra:.brain/biblioteca/M.md:skills:5"])


class TestContradicciones(Base):
    def test_mismo_archivo_con_topes_distintos_en_dos_documentos(self):
        poner(self.d, ".brain/biblioteca/A.md", "El tope de `CLAUDE.md` es 5120 bytes.\n")
        poner(self.d, ".brain/biblioteca/B.md", "Límite de `CLAUDE.md`: 8 KB.\n")
        poner(self.d, ".brain/pendientes.md", "A.md B.md\n")
        self.assertEqual(self.claves(), ["tope:CLAUDE.md"])

    def test_mismo_valor_en_unidades_distintas_no_contradice(self):
        poner(self.d, ".brain/biblioteca/A.md", "El tope de `CLAUDE.md` es 8192 bytes.\n")
        poner(self.d, ".brain/biblioteca/B.md", "Límite de `CLAUDE.md`: 8 KB.\n")
        poner(self.d, ".brain/pendientes.md", "A.md B.md\n")
        self.assertEqual(self.claves(), [])


class TestDescartesYAviso(Base):
    def setUp(self):
        super().setUp()
        poner(self.d, ".brain/lecciones/sola.md", "# sola\n")
        poner(self.d, ".brain/guardianes/x.txt", "")

    def test_lo_descartado_no_vuelve(self):
        rc.descartar(self.d, "huerfana:.brain/lecciones/sola.md", "historica", HOY)
        informe = rc.analizar(self.d, CFG)
        self.assertEqual(informe["hallazgos"], [])
        self.assertEqual(informe["descartados"], 1)

    def test_aviso_de_arranque_una_linea_solo_si_hay_hallazgos(self):
        lineas = rc.resumen(self.d, CFG, HOY)
        self.assertEqual(len(lineas), 1)
        self.assertIn("1 hallazgo", lineas[0])
        rc.descartar(self.d, "huerfana:.brain/lecciones/sola.md", "m", HOY)
        self.assertEqual(rc.resumen(self.d, CFG, HOY), [])

    def test_revision_reciente_calla_y_vieja_vuelve_a_avisar(self):
        rc.marcar_revision(self.d, HOY)
        self.assertEqual(rc.resumen(self.d, CFG, HOY + datetime.timedelta(days=10)), [])
        self.assertEqual(len(rc.resumen(self.d, CFG, HOY + datetime.timedelta(days=40))), 1)

    def test_se_apaga_con_el_ajuste(self):
        self.assertEqual(rc.resumen(self.d, {"idioma": "es", "revision_contenido_activa": False}, HOY), [])

    def test_aviso_en_ingles(self):
        poner(self.d, ".brain/guardianes/guardianes.json", '{"idioma": "en"}')
        # el idioma de tp() sale del guardianes.json del proyecto real, así que solo se comprueba que el texto existe en inglés
        import sys
        sys.path.insert(0, os.path.join(RAIZ, ".brain", "guardianes"))
        import textos
        self.assertIn("finding", textos.t("en", "revisar_contenido_aviso") % 2)


class TestRepoReal(unittest.TestCase):
    def test_no_rompe_con_el_repo_real(self):
        informe = rc.analizar(RAIZ, {"idioma": "es"})
        self.assertIn("hallazgos", informe)


if __name__ == "__main__":
    unittest.main()
