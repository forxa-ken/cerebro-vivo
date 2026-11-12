# -*- coding: utf-8 -*-
"""Spec 044: guardián `auditor.py` (quién audita, comando de Codex, ajustes) y el aviso de `cierre.py`."""
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


auditor = cargar("auditor_g", [".brain", "guardianes", "auditor.py"])
cierre = cargar("cierre_a", [".brain", "guardianes", "cierre.py"])


def cfg_real():
    with open(os.path.join(RAIZ, ".brain", "guardianes", "guardianes.json"), encoding="utf-8") as f:
        return json.load(f)


class QuienAudita(unittest.TestCase):
    def test_por_defecto_el_externo_entra_en_general_y_spec_pero_no_en_cierre(self):
        cfg = {}
        self.assertEqual(auditor.quien_audita(cfg, "general"), ["interno", "externo"])
        self.assertEqual(auditor.quien_audita(cfg, "spec"), ["interno", "externo"])
        self.assertEqual(auditor.quien_audita(cfg, "cierre"), ["interno"])

    def test_siempre_incluye_el_cierre_rutinario(self):
        cfg = {"auditor_externo": "siempre"}
        self.assertEqual(auditor.quien_audita(cfg, "cierre"), ["interno", "externo"])

    def test_no_nunca_llama_a_una_ia_externa(self):
        cfg = {"auditor_externo": "no"}
        for modo in ("general", "cierre", "spec"):
            self.assertEqual(auditor.quien_audita(cfg, modo), ["interno"])

    def test_valor_raro_vuelve_al_defecto(self):
        self.assertEqual(auditor.valor_externo({"auditor_externo": "quizá"}), "general-y-spec")


class ComandoCodex(unittest.TestCase):
    def test_en_windows_lleva_sandbox_unelevated_y_solo_lectura(self):
        args = auditor.comando_codex({}, "win32")
        self.assertIn('windows.sandbox="unelevated"', args)
        self.assertEqual(args[args.index("-s") + 1], "read-only")
        self.assertEqual(args[-1], "-")
        self.assertEqual(args[args.index("-m") + 1], "gpt-6-sol")

    def test_fuera_de_windows_no_lleva_el_ajuste(self):
        self.assertNotIn('windows.sandbox="unelevated"', auditor.comando_codex({}, "linux"))

    def test_modelo_y_esfuerzo_se_leen_de_los_ajustes(self):
        args = auditor.comando_codex({"auditor_modelo_externo": "otro", "auditor_esfuerzo": "high"}, "linux")
        self.assertEqual(args[args.index("-m") + 1], "otro")
        self.assertIn("model_reasoning_effort=high", args)


class Ajustes(unittest.TestCase):
    def setUp(self):
        self.p = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.p, True)
        os.makedirs(os.path.join(self.p, ".brain", "guardianes"))
        self.ruta = os.path.join(self.p, ".brain", "guardianes", "guardianes.json")
        with open(self.ruta, "w", encoding="utf-8") as f:
            json.dump({"idioma": "es"}, f)

    def leer(self):
        with open(self.ruta, encoding="utf-8") as f:
            return json.load(f)

    def test_estado_no_escribe(self):
        cod, lineas = auditor.modo(self.p, "estado", "estado")
        self.assertEqual(cod, 0)
        self.assertEqual(self.leer(), {"idioma": "es"})
        self.assertIn("ACTIVADO", lineas[0])

    def test_externo_se_guarda_y_se_describe(self):
        cod, lineas = auditor.modo(self.p, "externo", "no")
        self.assertEqual(cod, 0)
        self.assertEqual(self.leer()["auditor_externo"], "no")
        self.assertIn("APAGADA", lineas[1])

    def test_externo_palabra_desconocida_no_cambia_nada(self):
        cod, _ = auditor.modo(self.p, "externo", "mucho")
        self.assertEqual(cod, 1)
        self.assertEqual(self.leer(), {"idioma": "es"})

    def test_cierre_si_no(self):
        auditor.modo(self.p, "cierre", "no")
        self.assertIs(self.leer()["auditor_cierre"], False)
        auditor.modo(self.p, "cierre", "si")
        self.assertIs(self.leer()["auditor_cierre"], True)

    def test_aspecto_desconocido(self):
        self.assertEqual(auditor.modo(self.p, "raro", "estado")[0], 1)

    def test_en_ingles(self):
        with open(self.ruta, "w", encoding="utf-8") as f:
            json.dump({"idioma": "en"}, f)
        _, lineas = auditor.modo(self.p, "estado", "estado")
        self.assertIn("Closing auditor", lineas[0])


class AvisoDeCierre(unittest.TestCase):
    def setUp(self):
        self.cfg = dict(cfg_real(), auditor_cierre=True)

    def avisos(self, archivos, cfg=None):
        return self.cierre_evaluar(archivos, cfg or self.cfg)

    def cierre_evaluar(self, archivos, cfg):
        return cierre.evaluar(archivos, 1000, cfg, True, True, archivos, sin_cerrar=None)

    def test_avisa_con_cambios_de_codigo(self):
        avisos = self.avisos(["server.py"])
        self.assertTrue(any("auditor" in a.lower() for a in avisos), avisos)

    def test_avisa_con_configuracion(self):
        self.assertTrue(any("auditor" in a.lower() for a in self.avisos(["ajustes.toml"])))

    def test_no_avisa_si_solo_hay_documentos(self):
        self.assertFalse(any("auditor" in a.lower() for a in self.avisos(["README.md", "notas.txt"])))

    def test_no_avisa_si_el_ajuste_esta_apagado(self):
        cfg = dict(self.cfg, auditor_cierre=False)
        self.assertFalse(any("auditor" in a.lower() for a in self.avisos(["server.py"], cfg)))

    def test_no_avisa_si_el_ajuste_no_existe(self):
        cfg = {k: v for k, v in self.cfg.items() if k != "auditor_cierre"}
        self.assertFalse(any("auditor" in a.lower() for a in self.avisos(["server.py"], cfg)))

    def test_solo_memoria_no_avisa(self):
        self.assertEqual([a for a in self.avisos([".brain/pendientes.md"]) if "auditor" in a.lower()], [])

    def test_ajustes_por_defecto_del_repo(self):
        cfg = cfg_real()
        self.assertIs(cfg["auditor_cierre"], True)
        self.assertEqual(cfg["auditor_externo"], "general-y-spec")


class Reparto(unittest.TestCase):
    def test_plantilla_e_informe_existen_en_los_dos_idiomas(self):
        for n in ("PLANTILLA_INFORME_REVISION.md", "PLANTILLA_INFORME_REVISION.en.md"):
            self.assertTrue(os.path.isfile(os.path.join(RAIZ, ".brain", "biblioteca", n)), n)

    def test_plantilla_va_en_el_manifiesto(self):
        with open(os.path.join(RAIZ, "generar_manifiesto.py"), encoding="utf-8") as f:
            self.assertIn("PLANTILLA_INFORME_REVISION.en.md", f.read())

    def test_la_skill_esta_en_los_dos_idiomas(self):
        for n in ("SKILL.md", "SKILL.en.md"):
            self.assertTrue(os.path.isfile(os.path.join(RAIZ, ".claude", "skills", "auditor", n)), n)


if __name__ == "__main__":
    unittest.main()
