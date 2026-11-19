# -*- coding: utf-8 -*-
"""Spec 044: guardián `auditor.py` (quién audita, comando de Codex, ajustes) y el aviso de `cierre.py`."""
import codecs
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
textos = cargar("textos_a", [".brain", "guardianes", "textos.py"])


def cfg_real():
    with open(os.path.join(RAIZ, ".brain", "guardianes", "guardianes.json"), encoding="utf-8") as f:
        return json.load(f)


class QuienAudita(unittest.TestCase):
    def test_por_defecto_audita_solo_el_externo_en_los_tres_modos(self):
        cfg = {}
        for modo in ("general", "cierre", "spec"):
            self.assertEqual(auditor.quien_audita(cfg, modo), ["externo"])

    def test_el_interno_es_opcional_siempre_o_solo_esta_vez(self):
        self.assertEqual(auditor.quien_audita({"auditor_interno": "siempre"}, "cierre"), ["interno", "externo"])
        self.assertEqual(auditor.quien_audita({}, "general", con_interno=True), ["interno", "externo"])

    def test_general_y_spec_deja_el_cierre_rutinario_al_interno(self):
        cfg = {"auditor_externo": "general-y-spec"}
        self.assertEqual(auditor.quien_audita(cfg, "general"), ["externo"])
        self.assertEqual(auditor.quien_audita(cfg, "cierre"), ["interno"])

    def test_no_nunca_llama_a_una_ia_externa_y_audita_el_interno(self):
        cfg = {"auditor_externo": "no"}
        for modo in ("general", "cierre", "spec"):
            self.assertEqual(auditor.quien_audita(cfg, modo), ["interno"])

    def test_valores_raros_vuelven_al_defecto(self):
        self.assertEqual(auditor.valor_externo({"auditor_externo": "quizá"}), "siempre")
        self.assertEqual(auditor.valor_interno({"auditor_interno": "quizá"}), "opcional")


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

    def test_cierre_acepta_mayusculas_y_false(self):
        auditor.modo(self.p, "cierre", "FALSE")
        self.assertIs(self.leer()["auditor_cierre"], False)
        auditor.modo(self.p, "cierre", "True")
        self.assertIs(self.leer()["auditor_cierre"], True)

    def test_json_roto_no_se_sobrescribe(self):
        roto = b'{"idioma": "es", "otro": 1,'
        with open(self.ruta, "wb") as f:
            f.write(roto)
        for aspecto, orden in (("cierre", "no"), ("externo", "siempre")):
            cod, lineas = auditor.modo(self.p, aspecto, orden)
            self.assertEqual(cod, 1)
            self.assertIn("guardianes.json", lineas[0])
        with open(self.ruta, "rb") as f:
            self.assertEqual(f.read(), roto)

    def test_raiz_que_no_es_objeto_no_se_sobrescribe(self):
        with open(self.ruta, "w", encoding="utf-8") as f:
            f.write("[1, 2]")
        self.assertEqual(auditor.modo(self.p, "cierre", "no")[0], 1)
        with open(self.ruta, encoding="utf-8") as f:
            self.assertEqual(f.read(), "[1, 2]")
        self.assertEqual(auditor.modo(self.p, "estado", "estado")[0], 0)  # leer sí se puede

    def test_con_bom_se_lee_y_se_conserva_el_resto(self):
        with open(self.ruta, "wb") as f:
            f.write(codecs.BOM_UTF8 + json.dumps({"idioma": "es", "otro": 7}).encode("utf-8"))
        self.assertEqual(auditor.modo(self.p, "cierre", "no")[0], 0)
        d = self.leer()
        self.assertEqual(d["otro"], 7)
        self.assertIs(d["auditor_cierre"], False)

    def test_json_anidado_enorme_no_da_traceback(self):
        with open(self.ruta, "w", encoding="utf-8") as f:
            f.write("[" * 100000)
        self.assertEqual(auditor.modo(self.p, "cierre", "no")[0], 1)

    def test_estado_con_json_roto_avisa_de_que_son_valores_por_defecto(self):
        with open(self.ruta, "w", encoding="utf-8") as f:
            f.write("{roto")
        cod, lineas = auditor.modo(self.p, "estado", "estado")
        self.assertEqual(cod, 0)
        self.assertIn("guardianes.json", lineas[0])

    def test_sin_archivo_se_crea(self):
        os.remove(self.ruta)
        self.assertEqual(auditor.modo(self.p, "cierre", "no")[0], 0)
        self.assertIs(self.leer()["auditor_cierre"], False)

    def test_aspecto_desconocido(self):
        self.assertEqual(auditor.modo(self.p, "raro", "estado")[0], 1)

    def test_en_ingles(self):
        with open(self.ruta, "w", encoding="utf-8") as f:
            json.dump({"idioma": "en"}, f)
        _, lineas = auditor.modo(self.p, "estado", "estado")
        self.assertIn("Closing auditor", lineas[0])


class ComandoSeguro(unittest.TestCase):
    def test_valores_con_caracteres_de_shell_vuelven_al_defecto(self):
        args = auditor.comando_codex({"auditor_modelo_externo": "x; rm -rf /", "auditor_esfuerzo": "$(whoami)"}, "linux")
        self.assertEqual(args[args.index("-m") + 1], "gpt-6-sol")
        self.assertIn("model_reasoning_effort=medium", args)
        self.assertEqual(args[-1], "-")

    def test_valor_que_parece_una_opcion_vuelve_al_defecto(self):
        for malo in ("-s", "--help", "-m"):
            self.assertEqual(auditor._seguro(malo, "gpt-6-sol"), "gpt-6-sol", malo)
        args = auditor.comando_codex({"auditor_modelo_externo": "-s"}, "linux")
        self.assertEqual(args[args.index("-m") + 1], "gpt-6-sol")

    def test_extensiones_vacias_o_sin_punto_no_apagan_el_aviso(self):
        self.assertTrue(auditor.hay_codigo(["server.py"], {"auditor_ignorar_extensiones": [""]}))
        self.assertTrue(auditor.hay_codigo(["a.cmd"], {"auditor_ignorar_extensiones": ["md"]}))
        self.assertFalse(auditor.hay_codigo(["a.md"], {"auditor_ignorar_extensiones": ["md"]}))
        self.assertFalse(auditor.hay_codigo(["a.md"], {"auditor_ignorar_extensiones": ["", "MD"]}))

    def test_valor_normal_se_respeta(self):
        self.assertEqual(auditor._seguro("gpt-6-sol", "x"), "gpt-6-sol")
        self.assertEqual(auditor._seguro(None, "x"), "x")


class Main(unittest.TestCase):
    """`main` por dentro: quien, codex, estado (lo pedía el informe del auditor)."""

    def setUp(self):
        self.p = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.p, True)
        os.makedirs(os.path.join(self.p, ".brain", "guardianes"))
        with open(os.path.join(self.p, ".brain", "guardianes", "guardianes.json"), "w", encoding="utf-8") as f:
            json.dump({"idioma": "es", "revision_sensibles": ["auth"]}, f)

    def correr(self, *argv):
        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            cod = auditor.main(list(argv), raiz=self.p)
        return cod, buf.getvalue().strip()

    def test_quien(self):
        self.assertEqual(self.correr("quien", "general"), (0, "externo"))
        self.assertEqual(self.correr("quien", "cierre"), (0, "externo"))
        self.assertEqual(self.correr("quien", "cierre", "--interno"), (0, "interno + externo"))
        self.assertEqual(self.correr("interno", "quizá")[0], 1)
        self.assertEqual(self.correr("interno", "siempre")[0], 0)
        self.assertEqual(self.correr("quien", "spec"), (0, "interno + externo"))
        self.assertEqual(self.correr("externo", "general-y-spec")[0], 0)
        self.assertEqual(self.correr("quien", "cierre", "src/auth.py"), (0, "interno + externo?"))

    def test_quien_modo_raro_da_uso(self):
        self.assertEqual(self.correr("quien", "otra")[0], 1)
        self.assertEqual(self.correr("quien")[0], 1)

    def test_codex_imprime_una_linea(self):
        cod, texto = self.correr("codex")
        self.assertEqual(cod, 0)
        self.assertTrue(texto.startswith("codex exec -m gpt-6-sol"))
        self.assertEqual(len(texto.splitlines()), 1)

    def test_estado_y_orden_desconocida(self):
        self.assertEqual(self.correr("estado")[0], 0)
        self.assertEqual(self.correr()[0], 0)
        self.assertEqual(self.correr("cierre", "quizá")[0], 1)


class AvisoDeCierre(unittest.TestCase):
    """Spec 092: el auditor avisa SOLO si hay un cierre marcado como terminado y sin auditar."""
    MARCA = {"que": "spec 092", "sensible": False}

    def setUp(self):
        self.cfg = dict(cfg_real(), auditor_cierre=True)

    def avisos(self, archivos, cfg=None, marca=MARCA):
        return cierre.evaluar(archivos, 1000, cfg or self.cfg, True, True, archivos, sin_cerrar=None, auditor_pendiente=marca)

    def hay(self, av):
        return any("auditor" in a.lower() for a in av)

    def test_sin_marca_no_avisa_aunque_haya_codigo_sin_commitear(self):
        self.assertFalse(self.hay(self.avisos(["server.py"], marca=None)))

    def test_con_marca_avisa_y_dice_que_se_cerro(self):
        av = self.avisos(["server.py"])
        self.assertTrue(self.hay(av), av)
        self.assertTrue(any("spec 092" in a for a in av), av)

    def test_el_aviso_pide_dar_por_auditada(self):
        self.assertTrue(any("auditada" in a for a in self.avisos([])))

    def test_no_avisa_si_el_ajuste_esta_apagado(self):
        self.assertFalse(self.hay(self.avisos(["server.py"], dict(self.cfg, auditor_cierre=False))))

    def test_avisa_si_el_ajuste_no_existe_verdadero_por_defecto(self):
        cfg = {k: v for k, v in self.cfg.items() if k != "auditor_cierre"}
        self.assertTrue(self.hay(self.avisos(["server.py"], cfg)))
        self.assertTrue(auditor.cierre_activo(cfg))

    def test_texto_false_cuenta_como_apagado(self):
        for v in ("false", "FALSE", "no", "0", False):
            self.assertFalse(auditor.cierre_activo({"auditor_cierre": v}), v)
        self.assertFalse(self.hay(self.avisos(["server.py"], dict(self.cfg, auditor_cierre="false"))))

    def test_bloque_abierto_no_apaga_el_aviso_de_un_cierre_marcado(self):
        av = cierre.evaluar(["server.py"], 1000, self.cfg, True, False, ["server.py"], sin_cerrar=3, auditor_pendiente=self.MARCA)
        self.assertTrue(self.hay(av), av)

    def test_auditor_aparte_recibe_el_aviso_y_avisos_no(self):
        aparte = []
        av = cierre.evaluar(["server.py"], 1000, self.cfg, True, True, ["server.py"], None, aparte, self.MARCA)
        self.assertFalse(self.hay(av), av)
        self.assertTrue(self.hay(aparte), aparte)

    def test_readme_y_license_sin_extension_no_cuentan_como_codigo(self):
        self.assertFalse(auditor.hay_codigo(["README", "LICENSE", "docs/CHANGELOG"], {}))
        self.assertTrue(auditor.hay_codigo(["Makefile"], {}))

    def test_marca_sensible_sugiere_el_externo(self):
        av = self.avisos([], dict(self.cfg, auditor_externo="general-y-spec"), {"que": "spec 1", "sensible": True})
        self.assertTrue(any("sensibles" in a.lower() for a in av), av)
        self.assertFalse(any("sensibles" in a.lower() for a in self.avisos([])))

    def test_archivos_sensibles_sugieren_el_externo(self):
        cfg = dict(self.cfg, auditor_externo="general-y-spec")
        self.assertTrue(auditor.sensible(["src/payment.py"], cfg))
        self.assertFalse(auditor.sensible(["src/util.py"], cfg))
        self.assertEqual(auditor.quien_audita(cfg, "cierre", ["src/payment.py"]), ["interno", "externo?"])
        self.assertEqual(auditor.quien_audita(cfg, "cierre", ["src/util.py"]), ["interno"])
        self.assertEqual(auditor.quien_audita(dict(cfg, auditor_externo="no"), "cierre", ["src/payment.py"]), ["interno"])

    def test_solo_memoria_no_avisa(self):
        self.assertEqual([a for a in self.avisos([".brain/pendientes.md"], marca=None) if "auditor" in a.lower()], [])

    def test_ajustes_por_defecto_del_repo(self):
        cfg = cfg_real()
        self.assertIs(cfg["auditor_cierre"], True)
        # 1.60.8: el valor es del proyecto (uno antiguo con «general-y-spec» sigue siendo válido): solo se comprueba que sea reconocible
        self.assertIn(auditor.valor_externo(cfg), auditor.EXTERNO_VALORES)
        self.assertIn(auditor.valor_interno(cfg), auditor.INTERNO_VALORES)


if __name__ == "__main__":
    unittest.main()


class MarcaDeCierre(unittest.TestCase):
    """Spec 092: `terminada` marca, `auditada` quita, y la marca ilegible no tumba nada."""
    def setUp(self):
        import tempfile
        self.dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.dir, ".brain", "guardianes"))
        self.addCleanup(__import__("shutil").rmtree, self.dir, True)

    def cfg(self, **kw):
        with open(os.path.join(self.dir, ".brain", "guardianes", "guardianes.json"), "w", encoding="utf-8") as f:
            json.dump(kw, f)

    def test_terminada_con_codigo_marca_y_auditada_quita(self):
        self.cfg()
        self.assertEqual(auditor.marcar_pendiente(self.dir, "spec 092", ["a.py"])[0], 0)
        self.assertEqual(auditor.pendiente(self.dir)["que"], "spec 092")
        self.assertEqual(auditor.quitar_pendiente(self.dir)[0], 0)
        self.assertIsNone(auditor.pendiente(self.dir))
        self.assertEqual(auditor.quitar_pendiente(self.dir)[0], 0)  # sin marca: no falla

    def test_solo_documentos_no_marca(self):
        self.cfg()
        auditor.marcar_pendiente(self.dir, "spec 1", ["notas.md", ".brain/decisions.log"])
        self.assertIsNone(auditor.pendiente(self.dir))

    def test_forzar_marca_sin_mirar_el_codigo(self):
        self.cfg()
        auditor.marcar_pendiente(self.dir, "encargo 3", [], forzar=True)
        self.assertEqual(auditor.pendiente(self.dir)["que"], "encargo 3")

    def test_apagado_no_marca(self):
        self.cfg(auditor_cierre=False)
        auditor.marcar_pendiente(self.dir, "spec 1", ["a.py"], forzar=True)
        self.assertIsNone(auditor.pendiente(self.dir))

    def test_marca_ilegible_es_sin_marca(self):
        ruta = os.path.join(self.dir, ".brain", "guardianes", "auditor_pendiente.json")
        for roto in ("{no json", "[]", '{"que": ""}'):
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(roto)
            self.assertIsNone(auditor.pendiente(self.dir), roto)

    def test_marca_sensible_solo_con_externo_general_y_spec(self):
        self.cfg(auditor_externo="general-y-spec", revision_sensibles=["payment"])
        auditor.marcar_pendiente(self.dir, "spec 1", ["src/payment.py"])
        self.assertTrue(auditor.pendiente(self.dir)["sensible"])

    def test_textos_nuevos_en_los_dos_idiomas(self):
        for idioma in ("es", "en"):
            for clave in ("cierre_auditor", "auditor_terminada_ok"):
                self.assertIn("x", textos.t({"idioma": idioma}, clave, "x"))
            for clave in ("auditor_terminada_apagado", "auditor_terminada_sin_codigo", "auditor_auditada_ok", "auditor_auditada_nada"):
                self.assertTrue(textos.t({"idioma": idioma}, clave))
