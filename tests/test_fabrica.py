# -*- coding: utf-8 -*-
"""Spec 035 fase 2: el guardián de la fábrica (huellas, alcance del encargo, topes y parada)."""
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
_e = importlib.util.spec_from_file_location("fabrica_g", RAIZ / ".brain" / "guardianes" / "fabrica.py")
fabrica = importlib.util.module_from_spec(_e)
_e.loader.exec_module(fabrica)

ENCARGO = """# Encargo 001: icono
- Requisito que cumple: R2 (posición vertical)
- Archivos permitidos: a.lua, Modules/
- Prueba que lo da por bueno: x
"""


def git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


class FabricaTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.email", "t@t")
        git(self.repo, "config", "user.name", "t")
        for n in ("a.lua", "b.lua", "ya_sucio.txt"):
            (self.repo / n).write_text("v1", encoding="utf-8")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-q", "-m", "base")
        (self.repo / "ya_sucio.txt").write_text("v2", encoding="utf-8")  # cambio previo ajeno
        self.carta = self.repo / ".brain" / "fabrica" / "carta.md"
        self.carta.parent.mkdir(parents=True)
        self.spec = self.repo / "spec.md"
        self.spec.write_text("# Spec\n- R1 uno\n- R2 dos\n", encoding="utf-8")
        self.encargo = self.repo / ".brain" / "fabrica" / "001.md"
        self.encargo.write_text(ENCARGO, encoding="utf-8")
        self.f = fabrica.Fabrica(self.repo, {"idioma": "es"})

    def tearDown(self):
        self.tmp.cleanup()

    def _listo(self):
        self.f.congelar(self.spec)
        self.f.foto(self.repo, "001")

    def test_spec_congelada_detecta_cambios(self):
        self.assertEqual(self.f.congelar(self.spec)[0], 0)
        self.assertEqual(self.f.verificar()[0], 0)
        self.spec.write_text("# Spec\n- R1 uno\n- R2 dos\n- R3 colado\n", encoding="utf-8")
        self.assertEqual(self.f.verificar()[0], 1)

    def test_no_se_vuelve_a_congelar_sin_reemplazar(self):
        self.f.congelar(self.spec)
        self.assertEqual(self.f.congelar(self.spec)[0], 1)
        self.assertEqual(self.f.congelar(self.spec, reemplazar=True)[0], 0)

    def test_carta_sellada_detecta_cambios(self):
        self.carta.write_text("- tope_encargo_tokens: 10\n", encoding="utf-8")
        self.f.congelar(self.spec)
        self.assertEqual(self.f.sellar_carta()[0], 0)
        self.assertEqual(self.f.verificar()[0], 0)
        self.carta.write_text("- tope_encargo_tokens: 99999999\n", encoding="utf-8")
        self.assertEqual(self.f.verificar()[0], 1)

    def test_sin_spec_congelada_se_rechaza(self):
        self.assertEqual(self.f.alcance(self.encargo, self.repo, "001")[0], 1)

    def test_encargo_que_no_existe_avisa_sin_romper(self):
        self._listo()
        codigo, avisos = self.f.alcance(self.repo / "no_existe.md", self.repo, "001")
        self.assertEqual(codigo, 1)
        self.assertIn("no_existe.md", avisos[0])

    def test_encargo_sin_requisito_se_rechaza(self):
        self._listo()
        self.encargo.write_text(ENCARGO.replace("R2 (posición vertical)", "<R-n de la spec>"), encoding="utf-8")
        self.assertEqual(self.f.alcance(self.encargo, self.repo, "001")[0], 1)

    def test_requisito_que_no_esta_en_la_spec_se_rechaza(self):
        self._listo()
        self.encargo.write_text(ENCARGO.replace("R2", "R9"), encoding="utf-8")
        self.assertEqual(self.f.alcance(self.encargo, self.repo, "001")[0], 1)

    def test_dentro_del_alcance_ignora_cambio_previo_y_nota(self):
        self._listo()
        (self.repo / "a.lua").write_text("v2", encoding="utf-8")
        (self.repo / "Modules").mkdir()
        (self.repo / "Modules" / "x.lua").write_text("n", encoding="utf-8")
        (self.repo / ".brain" / "notas-chats").mkdir()
        (self.repo / ".brain" / "notas-chats" / "nota.md").write_text("n", encoding="utf-8")
        self.assertEqual(self.f.alcance(self.encargo, self.repo, "001")[0], 0)

    def test_fuera_de_alcance_se_rechaza(self):
        self._listo()
        (self.repo / "b.lua").write_text("v2", encoding="utf-8")
        codigo, msg = self.f.alcance(self.encargo, self.repo, "001")
        self.assertEqual(codigo, 1)
        self.assertIn("b.lua", "\n".join(msg))

    def test_tocar_de_nuevo_un_archivo_ya_sucio_se_detecta(self):
        self._listo()
        (self.repo / "ya_sucio.txt").write_text("v3", encoding="utf-8")
        self.assertEqual(self.f.alcance(self.encargo, self.repo, "001")[0], 1)

    def test_commit_durante_el_trabajo_se_rechaza(self):
        self._listo()
        (self.repo / "a.lua").write_text("v2", encoding="utf-8")
        git(self.repo, "commit", "-q", "-am", "colado")
        self.assertEqual(self.f.alcance(self.encargo, self.repo, "001")[0], 1)

    def test_spec_cambiada_bloquea_el_alcance(self):
        self._listo()
        self.spec.write_text("# otra\n- R2\n", encoding="utf-8")
        self.assertEqual(self.f.alcance(self.encargo, self.repo, "001")[0], 1)

    def test_topes_por_encargo_mision_y_semanal(self):
        self.assertEqual(self.f.topes("001")[0], 0)
        self.f.gasto("001", 300000, "ejecutora")
        self.assertEqual(self.f.topes("001")[0], 0)
        self.f.gasto("001", 100000, "ejecutora")
        self.assertEqual(self.f.topes("001")[0], 1)  # 400.000 = tope del encargo
        self.assertEqual(self.f.topes("002")[0], 0)
        self.assertEqual(self.f.topes("002", libre_semanal=49)[0], 1)
        self.assertEqual(self.f.topes("002", libre_semanal=50)[0], 0)
        self.f.gasto("002", 700000, "ejecutora")
        self.assertEqual(self.f.topes("003")[0], 1)  # 1.100.000 > tope de misión

    def test_dos_fallos_seguidos_paran_y_un_acierto_los_cuenta_de_nuevo(self):
        self.f.gasto("001", 10, "ejecutora", fallo=True)
        self.assertEqual(self.f.topes("001")[0], 0)
        self.f.gasto("001", 10, "ejecutora", fallo=True)
        self.assertEqual(self.f.topes("001")[0], 1)
        self.f.gasto("001", 10, "ejecutora", fallo=False)
        self.assertEqual(self.f.topes("001")[0], 0)

    def test_la_carta_cambia_los_topes(self):
        self.carta.write_text("- tope_mision_encargos: 1\n", encoding="utf-8")
        self.f.gasto("001", 1, "x")
        self.f.gasto("002", 1, "x")
        self.assertEqual(self.f.topes()[0], 1)

    def test_la_plantilla_de_la_carta_trae_los_topes_que_lee_el_guardian(self):
        txt = (RAIZ / ".brain" / "biblioteca" / "PLANTILLAS_FABRICA.md").read_text(encoding="utf-8")
        self.carta.write_text(txt, encoding="utf-8")
        self.assertEqual(self.f.topes_carta(), fabrica.TOPES_POR_DEFECTO)
        for clave in fabrica.TOPES_POR_DEFECTO:
            self.assertIn("- %s:" % clave, txt)

    def test_mensajes_en_ingles(self):
        f = fabrica.Fabrica(self.repo, {"idioma": "en"})
        self.assertIn("no frozen spec", f.verificar()[1][0])

    def test_encargo_en_ingles(self):
        self.encargo.write_text("- Requirement it meets: R1\n- Allowed files: `a.lua` `b.lua`\n", encoding="utf-8")
        self.assertEqual(fabrica.Fabrica.leer_encargo(self.encargo), ("R1", ["a.lua", "b.lua"]))


class ModoFabricaTest(unittest.TestCase):
    """Spec 040: interruptor persistente `modo_fabrica` y su aviso en el arranque."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.raiz = Path(self.tmp.name)
        self.f = fabrica.Fabrica(self.raiz, {"idioma": "es"})
        self.cfg = self.raiz / ".brain" / "guardianes" / "guardianes.json"

    def _valor(self):
        import json
        return json.loads(self.cfg.read_text(encoding="utf-8")).get("modo_fabrica")

    def test_activa_apaga_y_persiste(self):
        self.assertEqual(self.f.modo("si")[0], 0)
        self.assertTrue(self._valor())
        self.assertTrue((self.raiz / ".brain" / "fabrica" / "encargos").is_dir())
        # otra instancia (otro chat) lo sigue viendo activo
        self.assertIn("ACTIVADO", fabrica.Fabrica(self.raiz, {"idioma": "es"}).modo("estado")[1][0])
        self.f.modo("no")
        self.assertFalse(self._valor())

    def test_si_no_pisa_lo_existente_ni_no_borra(self):
        carta = self.raiz / ".brain" / "fabrica" / "carta.md"
        carta.parent.mkdir(parents=True)
        carta.write_text("mi carta", encoding="utf-8")
        self.f.modo("si")
        self.f.modo("no")
        self.assertEqual(carta.read_text(encoding="utf-8"), "mi carta")

    def test_estado_no_escribe_y_palabra_mala_da_uso(self):
        self.assertEqual(self.f.modo("estado")[0], 0)
        self.assertFalse(self.cfg.exists())
        codigo, lineas = self.f.modo("quizas")
        self.assertEqual(codigo, 1)
        self.assertIn("modo si|no|estado", lineas[0])

    def test_topes_no_falla_con_consola_cp1252(self):
        """Consola de Windows (cp1252): el emoji del mensaje no debe romper el guardián."""
        import os
        import sys
        env = dict(os.environ, PYTHONIOENCODING="cp1252")
        r = subprocess.run([sys.executable, str(RAIZ / ".brain" / "guardianes" / "fabrica.py"), "--raiz", str(self.raiz), "topes"],
                           capture_output=True, env=env)
        self.assertEqual(r.returncode, 0, r.stderr.decode("utf-8", "replace"))

    def test_estado_dice_si_falta_la_carta(self):
        self.f.modo("si")
        self.assertIn("sin escribir", self.f.modo("estado")[1][1])

    def test_arranque_avisa_solo_con_el_modo_activo(self):
        e = importlib.util.spec_from_file_location("arranque_g", RAIZ / ".brain" / "guardianes" / "arranque.py")
        arranque = importlib.util.module_from_spec(e)
        e.loader.exec_module(arranque)
        base = {"idioma": "es", "pendientes": ".brain/pendientes.md", "registro": ".brain/decisions.log",
                "tope_pendientes_bytes": 8192}
        (self.raiz / ".brain").mkdir(exist_ok=True)
        (self.raiz / ".brain" / "pendientes.md").write_text("", encoding="utf-8")
        apagado = arranque.resumen(str(self.raiz), dict(base))
        encendido = arranque.resumen(str(self.raiz), dict(base, modo_fabrica=True))
        self.assertNotIn("MODO FÁBRICA", apagado)
        self.assertIn("MODO FÁBRICA ACTIVADO", encendido)


class AutomaticoTest(unittest.TestCase):
    """Spec 050, fase 1: interruptor `fabrica_automatica`, solo válido con `modo_fabrica`."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.raiz = Path(self.tmp.name)
        self.f = fabrica.Fabrica(self.raiz, {"idioma": "es"})
        self.cfg = self.raiz / ".brain" / "guardianes" / "guardianes.json"

    def _cfg(self):
        import json
        return json.loads(self.cfg.read_text(encoding="utf-8"))

    def test_sin_modo_fabrica_no_se_activa(self):
        codigo, lineas = self.f.automatico("si")
        self.assertEqual(codigo, 1)
        self.assertIn("modo fábrica encendido", lineas[0])
        self.assertFalse(self.cfg.exists())

    def test_activa_persiste_y_estado_dice_que_falta(self):
        self.f.modo("si")
        self.assertEqual(self.f.automatico("si")[0], 0)
        self.assertTrue(self._cfg()["fabrica_automatica"])
        codigo, lineas = fabrica.Fabrica(self.raiz, {"idioma": "es"}).automatico("estado")
        self.assertEqual(codigo, 0)
        texto = "\n".join(lineas)
        self.assertIn("AUTOMÁTICO: ACTIVADO", texto)
        self.assertIn("Falta: la carta sellada", texto)
        self.assertIn("Falta: el criterio", texto)
        self.assertIn("Falta: una rama", texto)

    def test_estado_ve_criterio_y_carta(self):
        self.f.modo("si")
        self.f.automatico("si")
        (self.raiz / ".brain" / "fabrica" / "esperado.md").write_text("x", encoding="utf-8")
        (self.raiz / ".brain" / "fabrica" / "carta.md").write_text("carta", encoding="utf-8")
        self.f.sellar_carta()
        texto = "\n".join(self.f.automatico("estado")[1])
        self.assertIn("sellada.", texto)
        self.assertIn("escrito", texto)

    def test_apagar_la_fabrica_apaga_el_automatico(self):
        self.f.modo("si")
        self.f.automatico("si")
        self.f.modo("no")
        self.assertFalse(self._cfg()["fabrica_automatica"])
        self.assertIn("desactivado", self.f.automatico("estado")[1][0])

    def test_modo_normal_y_palabra_mala(self):
        self.f.modo("si")
        self.f.automatico("si")
        self.f.modo("normal")
        self.assertFalse(self._cfg()["modo_fabrica"])
        self.assertFalse(self._cfg()["fabrica_automatica"])
        codigo, lineas = self.f.automatico("quizas")
        self.assertEqual(codigo, 1)
        self.assertIn("automatico si|no|estado", lineas[0])

    def test_arranque_avisa_automatico_solo_con_ambos(self):
        e = importlib.util.spec_from_file_location("arranque_a", RAIZ / ".brain" / "guardianes" / "arranque.py")
        arranque = importlib.util.module_from_spec(e)
        e.loader.exec_module(arranque)
        base = {"idioma": "es", "pendientes": ".brain/pendientes.md", "registro": ".brain/decisions.log",
                "tope_pendientes_bytes": 8192}
        (self.raiz / ".brain").mkdir(exist_ok=True)
        (self.raiz / ".brain" / "pendientes.md").write_text("", encoding="utf-8")
        solo_fabrica = arranque.resumen(str(self.raiz), dict(base, modo_fabrica=True))
        solo_auto = arranque.resumen(str(self.raiz), dict(base, fabrica_automatica=True))
        ambos = arranque.resumen(str(self.raiz), dict(base, modo_fabrica=True, fabrica_automatica=True))
        self.assertNotIn("AUTOMÁTICO", solo_fabrica)
        self.assertNotIn("AUTOMÁTICO", solo_auto)
        self.assertIn("Modo fábrica AUTOMÁTICO", ambos)


NEGOCIO = ("# Negocio\n- Los usuarios pagan una cuota mensual fija por el servicio.\n"
           "- El administrador puede dar de baja a cualquier usuario en un solo paso.\n")
SPEC = ("# Spec\n## R1\nEl sistema cobra una cuota mensual fija a cada usuario.\n"
        "## R2\nEl sistema ofrece descuentos por volumen a empresas grandes.\n")


class RevisorSpecTest(unittest.TestCase):
    """Spec 050, fase 2: negocio sellado, veredicto con citas obligatorias y tope de vueltas."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.raiz = Path(self.tmp.name)
        (self.raiz / ".brain" / "fabrica").mkdir(parents=True)
        self.negocio = self.raiz / ".brain" / "fabrica" / "negocio.md"
        self.negocio.write_text(NEGOCIO, encoding="utf-8")
        self.spec = self.raiz / "spec.md"
        self.spec.write_text(SPEC, encoding="utf-8")
        self.f = fabrica.Fabrica(self.raiz, {"idioma": "es"})
        self.ver = self.raiz / "veredicto.md"
        self.f.sellar_negocio()

    def _v(self, texto, crudo=None):
        if crudo is not None:
            self.ver.write_bytes(crudo)
        else:
            self.ver.write_text(texto, encoding="utf-8")
        return self.f.veredicto(self.ver, self.spec)

    @staticmethod
    def _cuerpo(veredicto, a="- Ninguno", b="- Ninguno", c="- Ninguno", d="- Ninguna"):
        """Un veredicto con las cuatro secciones; cada argumento es el contenido de una sección."""
        return (f"Veredicto: {veredicto}\n\n## (a) Negocio no cubierto\n{a}\n## (b) Requisitos inventados\n{b}\n"
                f"## (c) Huecos y ambigüedades\n{c}\n## (d) Contradicciones\n{d}\n")

    def test_negocio_sellado_detecta_cambios(self):
        self.assertEqual(self.f.sellar_negocio()[0], 1)  # ya sellado en setUp
        self.assertEqual(self.f.sellar_negocio(True)[0], 0)
        self.negocio.write_text(NEGOCIO + "- algo nuevo\n", encoding="utf-8")
        self.f.congelar(self.spec)
        codigo, lineas = self.f.verificar()
        self.assertEqual(codigo, 1)
        self.assertIn("negocio.md cambió", "\n".join(lineas))

    def test_rechazo_con_cita_real_cuenta(self):
        codigo, lineas = self._v(self._cuerpo(
            "RECHAZADA", a="- «puede dar de baja a cualquier usuario» — la spec no lo tiene",
            b="- «descuentos por volumen a empresas grandes» — el negocio no lo pide"))
        self.assertEqual(codigo, 0, lineas)
        self.assertIn("RECHAZADA con 2", lineas[-1])

    def test_rechazo_sin_cita_o_con_cita_falsa_no_cuenta(self):
        codigo, lineas = self._v(self._cuerpo(
            "RECHAZADA", a="- falta lo de las bajas", b="- «esto no está escrito en ningún sitio» — x"))
        self.assertEqual(codigo, 1)
        texto = "\n".join(lineas)
        self.assertIn("SIN cita", texto)
        self.assertIn("no aparece", texto)
        self.assertIn("el rechazo no cuenta", texto)

    def test_aprobada_limpia_y_con_hueco_grande(self):
        codigo, lineas = self._v(self._cuerpo(
            "APROBADA", c="- [GRANDE] «cuota mensual fija» — ¿incluye impuestos?"))
        self.assertEqual(codigo, 0, lineas)
        self.assertIn("APROBADA", lineas[0])
        self.assertIn("GRANDE", lineas[1])

    def test_hueco_grande_sube_aunque_su_cita_no_valga(self):
        codigo, lineas = self._v(self._cuerpo("APROBADA", c="- [GRANDE] sin cita ninguna"))
        self.assertEqual(codigo, 0)
        self.assertIn("SIN cita", "\n".join(lineas))
        self.assertIn("GRANDE", lineas[-1])

    def test_aprobada_con_hallazgo_grave_es_incoherente(self):
        codigo, lineas = self._v(self._cuerpo(
            "APROBADA", b="- «descuentos por volumen a empresas grandes» — no está en el negocio"))
        self.assertEqual(codigo, 1)
        self.assertIn("incoherente", "\n".join(lineas))

    def test_sin_linea_de_veredicto_e_ingles(self):
        self.assertEqual(self._v("## (a) x\n- Ninguno\n")[0], 1)
        codigo, _ = self._v(self._cuerpo("REJECTED", a="- «cuota mensual fija» — whatever"))
        self.assertEqual(codigo, 0)

    def test_cita_vale_con_markdown_y_saltos(self):
        codigo, _ = self._v(self._cuerpo(
            "RECHAZADA", a="- «Los usuarios **pagan** una  cuota mensual fija» — x"))
        self.assertEqual(codigo, 0)

    def test_aprobada_vacia_o_sin_secciones_no_vale(self):
        self.assertEqual(self._v("Veredicto: APROBADA\n")[0], 1)
        codigo, lineas = self._v("Veredicto: APROBADA\n## (a) x\n- Ninguno\n")
        self.assertEqual(codigo, 1)
        self.assertIn("secciones", "\n".join(lineas))

    def test_lista_numerada_encabezado_distinto_y_suelto_no_se_cuelan(self):
        cita = "«puede dar de baja a cualquier usuario»"
        # lista numerada: ahora cuenta como hallazgo (APROBADA con (a) válido es incoherente)
        self.assertEqual(self._v(self._cuerpo("APROBADA", a=f"1. {cita} — x"))[0], 1)
        # encabezados con #### o en negrita también abren sección
        cuerpo = (f"Veredicto: APROBADA\n#### (a) x\n- {cita} — x\n**(b) x**\n- Ninguno\n"
                  "### (c) x\n- Ninguno\n## (d) x\n- Ninguna\n")
        self.assertEqual(self._v(cuerpo)[0], 1)
        # una viñeta con cita fuera de toda sección no se descarta en silencio
        suelto = "Veredicto: APROBADA\n- «puede dar de baja a cualquier usuario» — x\n" + self._cuerpo("APROBADA").split("\n", 1)[1]
        codigo, lineas = self._v(suelto)
        self.assertEqual(codigo, 1)
        self.assertIn("FUERA", "\n".join(lineas))

    def test_cada_seccion_cita_su_fuente(self):
        # (a) debe citar el negocio, no la spec; (b) debe citar la spec, no el negocio
        self.assertEqual(self._v(self._cuerpo("RECHAZADA", a="- «descuentos por volumen a empresas grandes» — x"))[0], 1)
        self.assertEqual(self._v(self._cuerpo("RECHAZADA", b="- «puede dar de baja a cualquier usuario» — x"))[0], 1)

    def test_todas_las_citas_deben_existir_y_minimo_12(self):
        self.assertEqual(self._v(self._cuerpo(
            "RECHAZADA", a="- «cuota mensual fija» y «frase inventada que no existe» — x"))[0], 1)
        self.assertEqual(self._v(self._cuerpo("RECHAZADA", a="- «el usuario» — x"))[0], 1)  # corta y común

    def test_archivos_que_no_son_utf8_no_hacen_caer_el_guardian(self):
        self.assertEqual(self._v("", crudo="Veredicto: APROBADA\n".encode("utf-16"))[0], 1)
        self.negocio.write_bytes("Negocio con acentos: cuota mensual fija ñ".encode("cp1252"))
        codigo, lineas = self._v(self._cuerpo("APROBADA"))
        self.assertEqual(codigo, 1)  # el negocio cambió respecto al sellado: no se valida nada

    def test_sin_negocio_sellado_no_se_valida(self):
        self.negocio.write_text(NEGOCIO + "- otro\n", encoding="utf-8")
        self.assertEqual(self._v(self._cuerpo("APROBADA"))[0], 1)
        otra = fabrica.Fabrica(self.raiz / "otro", {"idioma": "es"})
        self.assertEqual(otra.veredicto(self.ver, self.spec)[0], 1)

    def test_no_se_sella_un_negocio_vacio(self):
        self.negocio.write_text("  \n", encoding="utf-8")
        self.assertEqual(self.f.sellar_negocio(True)[0], 1)

    def test_vueltas_con_json_corrupto_o_raro_no_cae(self):
        ruta = self.raiz / ".brain" / "fabrica" / "estado" / "revision_spec.json"
        ruta.parent.mkdir(parents=True, exist_ok=True)
        for malo in ('{"vueltas": "x"}', '{"vueltas": null}', '[1]', '{{{', '{"vueltas": -4}'):
            ruta.write_text(malo, encoding="utf-8")
            codigo, lineas = self.f.vueltas("estado")
            self.assertEqual(codigo, 0, malo)
            self.assertIn("0 de 3", lineas[0])

    def test_vueltas_a_la_tercera_se_para_y_aprobar_reinicia(self):
        self.assertEqual(self.f.vueltas("rechazada")[0], 0)
        self.assertEqual(self.f.vueltas("rechazada")[0], 0)
        codigo, lineas = self.f.vueltas("rechazada")
        self.assertEqual(codigo, 1)
        self.assertIn("pregunta a Darwin", lineas[0])
        self.assertEqual(self.f.vueltas("estado")[0], 1)  # sigue parada hasta que alguien la reinicie
        self.assertEqual(self.f.vueltas("aprobada")[0], 0)
        self.assertEqual(self.f.vueltas("quizas")[0], 1)


if __name__ == "__main__":
    unittest.main()
