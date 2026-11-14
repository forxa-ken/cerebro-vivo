# -*- coding: utf-8 -*-
"""Spec 035 fase 2: el guardián de la fábrica (huellas, alcance del encargo, topes y parada)."""
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

def _falta_en(nombre):
    """Un proyecto en español no recibe las ediciones .en.md (spec 024): solo en el repo del arnés (hay manifiesto.json) son obligatorias."""
    ruta = RAIZ / ".brain" / "biblioteca" / nombre
    if ruta.is_file():
        return False
    assert not (RAIZ / "manifiesto.json").is_file(), "falta " + nombre
    return True

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

    def test_requisito_con_guion_vale_como_sin_guion(self):
        """Hallazgo de la fase 6 (spec 050): la plantilla dice «R-n» y el guardián solo entendía «R1»."""
        self.spec.write_text("# Spec\n- **R-1** uno\n- R-2 dos\n", encoding="utf-8")
        self.f.congelar(self.spec)
        for req, esperado in (("R1", 0), ("R-1", 0), ("R-2", 0), ("R-9", 1)):
            self.encargo.write_text(ENCARGO.replace("R2", req), encoding="utf-8")
            self.f.foto(self.repo, "001")  # el encargo se escribe antes de la foto
            self.assertEqual(self.f.alcance(self.encargo, self.repo, "001")[0], esperado, req)

    def test_la_spec_corregida_y_recongelada_no_cuenta_como_cambio_de_la_ejecutora(self):
        self._listo()
        self.spec.write_text("# Spec\n- R1 uno corregido\n- R2 dos\n", encoding="utf-8")
        self.f.congelar(self.spec, reemplazar=True)
        self.assertEqual(self.f.alcance(self.encargo, self.repo, "001")[0], 0)

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
        (self.raiz / ".brain" / "fabrica" / "esperado.md").write_text(ESPERADO_BUENO, encoding="utf-8")
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


ESPERADO_BUENO = ("# Criterio de «esperado»: prueba\n- Cómo se sabe que salió bien: el comando imprime OK con datos válidos\n"
                  "- Casos malos (deben rechazarse): un archivo vacío termina con código 1\n")


class ArrancarTest(unittest.TestCase):
    """Spec 050, fase 3: en modo automático no arranca un encargo sin criterio de «esperado» o estando en main."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.raiz = Path(self.tmp.name)
        self.git("init", "-q", "-b", "main")
        self.git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "--allow-empty", "-m", "i")
        self.esperado = self.raiz / ".brain" / "fabrica" / "esperado.md"
        self.f = fabrica.Fabrica(self.raiz, {"idioma": "es"})

    def git(self, *a):
        subprocess.run(["git", "-C", str(self.raiz), *a], check=True, capture_output=True)

    def activar(self):
        self.f.modo("si")
        self.f.automatico("si")

    def criterio(self, texto):
        self.esperado.parent.mkdir(parents=True, exist_ok=True)
        self.esperado.write_text(texto, encoding="utf-8")

    def test_no_aplica_fuera_del_modo_automatico(self):
        self.assertEqual(self.f.arrancar()[0], 0)  # ni modo fábrica
        self.f.modo("si")
        codigo, lineas = self.f.arrancar()  # fábrica normal, en main y sin criterio
        self.assertEqual(codigo, 0)
        self.assertIn("no aplica", lineas[0])

    def test_bloquea_sin_criterio_y_en_main(self):
        self.activar()
        codigo, lineas = self.f.arrancar()
        texto = "\n".join(lineas)
        self.assertEqual(codigo, 1)
        self.assertIn("Falta: el criterio", texto)
        self.assertIn("Falta: una rama", texto)
        self.assertIn("BLOQUEADO", texto)

    def test_criterio_bueno_pero_en_main_sigue_bloqueado(self):
        self.activar()
        self.criterio(ESPERADO_BUENO)
        codigo, lineas = self.f.arrancar()
        self.assertEqual(codigo, 1)
        self.assertNotIn("Falta: el criterio", "\n".join(lineas))
        self.assertNotIn("Falta rellenar", "\n".join(lineas))
        self.assertIn("Falta: una rama", "\n".join(lineas))

    def test_rama_buena_pero_criterio_plantilla_bloquea(self):
        self.activar()
        self.git("checkout", "-q", "-b", "linea/orden-1")
        self.criterio("# C\n- Cómo se sabe que salió bien: <comprobación observable>\n- Casos malos: <lista>\n")
        codigo, lineas = self.f.arrancar()
        self.assertEqual(codigo, 1)
        self.assertIn("Cómo se sabe que salió bien, Casos malos", "\n".join(lineas))

    def test_criterio_corto_o_a_medias_bloquea(self):
        self.activar()
        self.git("checkout", "-q", "-b", "linea/orden-1")
        self.criterio("- Cómo se sabe que salió bien: ok\n- Casos malos: un archivo vacío falla\n")
        self.assertIn("Cómo se sabe que salió bien", self.f.arrancar()[1][0])
        self.criterio("")
        self.assertIn("Falta: el criterio", self.f.arrancar()[1][0])

    def test_todo_en_regla_arranca(self):
        self.activar()
        self.git("checkout", "-q", "-b", "linea/orden-1")
        self.criterio(ESPERADO_BUENO)
        codigo, lineas = self.f.arrancar()
        self.assertEqual(codigo, 0)
        self.assertIn("linea/orden-1", lineas[0])

    def test_criterio_en_ingles(self):
        self.activar()
        self.git("checkout", "-q", "-b", "line/order-1")
        self.criterio("- How we know it went well: prints OK with valid data\n- Bad cases (must be rejected): empty file exits 1\n")
        self.assertEqual(self.f.arrancar()[0], 0)

    def test_foto_en_automatico_no_se_hace_si_bloquea(self):
        self.activar()
        codigo, _ = self.f.foto(self.raiz, "001")
        self.assertEqual(codigo, 1)
        self.assertFalse((self.raiz / ".brain" / "fabrica" / "estado" / "001.foto.json").exists())
        self.git("checkout", "-q", "-b", "linea/orden-1")
        self.criterio(ESPERADO_BUENO)
        self.assertEqual(self.f.foto(self.raiz, "001")[0], 0)

    def test_el_flag_como_texto_no_activa(self):
        cfg = self.raiz / ".brain" / "guardianes" / "guardianes.json"
        cfg.parent.mkdir(parents=True, exist_ok=True)
        cfg.write_text('{"modo_fabrica": true, "fabrica_automatica": "false"}', encoding="utf-8")
        self.assertIn("no aplica", self.f.arrancar()[1][0])

    def test_mensajes_en_ingles(self):
        f = fabrica.Fabrica(self.raiz, {"idioma": "en"})
        f.modo("si"); f.automatico("si")
        self.assertIn("BLOCKED", "\n".join(f.arrancar()[1]))

    def test_las_plantillas_traen_el_criterio_con_sus_campos(self):
        for nombre, campos in (("PLANTILLAS_FABRICA.md", ("Cómo se sabe que salió bien", "Casos malos")),
                               ("PLANTILLAS_FABRICA.en.md", ("How we know it went well", "Bad cases"))):
            if _falta_en(nombre):
                continue
            txt = (RAIZ / ".brain" / "biblioteca" / nombre).read_text(encoding="utf-8")
            for c in campos:
                self.assertIn("- %s" % c, txt)


class EntregarTest(unittest.TestCase):
    """Spec 050, fase 4: sin evidencia de uso real completa no se da un requisito por entregado."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.raiz = Path(self.tmp.name)
        self.fab = self.raiz / ".brain" / "fabrica"
        self.f = fabrica.Fabrica(self.raiz, {"idioma": "es"})
        self.f.modo("si")
        self.f.automatico("si")
        self.fab.mkdir(parents=True, exist_ok=True)
        (self.fab / "esperado.md").write_text(ESPERADO_BUENO, encoding="utf-8")
        (self.fab / "evidencia" / "R1").mkdir(parents=True)
        (self.fab / "evidencia" / "R1" / "salida.txt").write_text("OK\n", encoding="utf-8")

    def evidencia(self, **cambios):
        campos = {"Construyó": "Codex", "Probó": "Claude (otro chat)",
                  "Criterio probado": "«el comando imprime OK con datos válidos»",
                  "Casos buenos ejecutados": "cmd datos.csv → OK",
                  "Casos malos ejecutados": "cmd vacio.csv → código 1",
                  "Resultado": "verde", "No probado": "nada: no hay aspecto visual",
                  "Evidencia guardada": ".brain/fabrica/evidencia/R1/salida.txt"}
        campos.update(cambios)
        texto = "# Evidencia\n" + "".join("- %s: %s\n" % (k, v) for k, v in campos.items() if v is not None)
        (self.fab / "evidencia" / "R1.md").write_text(texto, encoding="utf-8")

    def test_no_aplica_fuera_del_automatico(self):
        self.f.automatico("no")
        self.assertEqual(self.f.entregar("R1")[0], 0)  # aunque no exista evidencia

    def test_sin_archivo_bloquea(self):
        codigo, lineas = self.f.entregar("R1")
        self.assertEqual(codigo, 1)
        self.assertIn("Sin evidencia, no está hecho", lineas[0])

    def test_evidencia_completa_se_entrega(self):
        self.evidencia()
        codigo, lineas = self.f.entregar("R1")
        self.assertEqual(codigo, 0, lineas)

    def test_quien_construyo_no_puede_probar(self):
        self.evidencia(**{"Probó": "codex"})
        self.assertIn("quien probó es quien construyó", "\n".join(self.f.entregar("R1")[1]))

    def test_criterio_inventado_o_sin_cita_bloquea(self):
        self.evidencia(**{"Criterio probado": "«se ve bonito y rápido»"})
        self.assertIn("debe citar", "\n".join(self.f.entregar("R1")[1]))
        self.evidencia(**{"Criterio probado": "el comando imprime OK con datos válidos"})  # sin comillas
        self.assertEqual(self.f.entregar("R1")[0], 1)

    def test_campo_vacio_o_plantilla_bloquea(self):
        self.evidencia(**{"Casos malos ejecutados": "<lista>"})
        self.assertIn("Casos malos ejecutados", self.f.entregar("R1")[1][0])
        self.evidencia(**{"No probado": None})
        self.assertIn("No probado", self.f.entregar("R1")[1][0])

    def test_archivo_de_evidencia_falso_vacio_o_fuera_bloquea(self):
        self.evidencia(**{"Evidencia guardada": ".brain/fabrica/evidencia/R1/no_existe.txt"})
        self.assertIn("no existe", "\n".join(self.f.entregar("R1")[1]))
        (self.fab / "evidencia" / "R1" / "vacio.txt").write_text("", encoding="utf-8")
        self.evidencia(**{"Evidencia guardada": ".brain/fabrica/evidencia/R1/vacio.txt"})
        self.assertEqual(self.f.entregar("R1")[0], 1)
        (self.raiz / "fuera.txt").write_text("x", encoding="utf-8")
        self.evidencia(**{"Evidencia guardada": "fuera.txt"})
        self.assertEqual(self.f.entregar("R1")[0], 1)
        self.evidencia(**{"Evidencia guardada": "../../../fuera.txt"})
        self.assertEqual(self.f.entregar("R1")[0], 1)

    def test_rojo_y_no_probado_no_se_entregan(self):
        self.evidencia(Resultado="rojo: falla el caso malo")
        self.assertIn("ROJO", "\n".join(self.f.entregar("R1")[1]))
        self.evidencia(Resultado="no probado: aspecto visual")
        self.assertIn("no se declara hecho", "\n".join(self.f.entregar("R1")[1]))
        self.evidencia(Resultado="quizás")
        self.assertEqual(self.f.entregar("R1")[0], 1)

    def test_sin_criterio_de_esperado_bloquea(self):
        self.evidencia()
        (self.fab / "esperado.md").unlink()
        self.assertIn("no hay criterio", "\n".join(self.f.entregar("R1")[1]))

    def test_requisito_con_ruta_rara_no_se_cae(self):
        self.assertEqual(self.f.entregar("../x")[0], 1)

    def test_en_ingles(self):
        f = fabrica.Fabrica(self.raiz, {"idioma": "en"})
        self.evidencia(**{"Built by": "Codex", "Tested by": "Claude", "Criterion tested": None})
        texto = "# Evidence\n- Built by: Codex\n- Tested by: Codex\n"
        (self.fab / "evidencia" / "R1.md").write_text(texto, encoding="utf-8")
        self.assertIn("still to fill in", f.entregar("R1")[1][0])
        self.assertIn("Criterion tested", f.entregar("R1")[1][0])

    def test_plantilla_trae_los_campos(self):
        for nombre, campos in (("PLANTILLAS_FABRICA.md", [e[0] for e in fabrica.Fabrica.EVID.values()]),
                               ("PLANTILLAS_FABRICA.en.md", [e[1] for e in fabrica.Fabrica.EVID.values()])):
            if _falta_en(nombre):
                continue
            txt = (RAIZ / ".brain" / "biblioteca" / nombre).read_text(encoding="utf-8")
            for c in campos:
                self.assertIn("- %s:" % c, txt)

    def test_la_plantilla_sin_rellenar_no_pasa(self):
        txt = (RAIZ / ".brain" / "biblioteca" / "PLANTILLAS_FABRICA.md").read_text(encoding="utf-8")
        bloque = txt.split("## 10.")[1].split("```markdown")[1].split("```")[0]
        (self.fab / "evidencia" / "R1.md").write_text(bloque, encoding="utf-8")
        self.assertEqual(self.f.entregar("R1")[0], 1)


class FrenosTest(unittest.TestCase):
    """Spec 050, fase 5: tope de 3 fallos y de 30 minutos sin avance por encargo; solo Darwin reanuda."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.raiz = Path(self.tmp.name)
        self.f = fabrica.Fabrica(self.raiz, {"idioma": "es"})
        self.f.modo("si")
        self.f.automatico("si")

    def test_no_aplica_fuera_del_automatico(self):
        self.f.automatico("no")
        for _ in range(5):
            self.f.gasto("001", 1, "x", fallo=True)
        self.assertEqual(self.f.frenos("001")[0], 0)
        self.assertEqual(self.f.avance("001")[0], 0)
        self.assertFalse((self.raiz / ".brain" / "fabrica" / "estado" / "frenos.json").exists())

    def test_tres_fallos_paran_y_dejan_informe(self):
        self.f.gasto("001", 1, "x", fallo=True)
        self.f.gasto("001", 1, "x", fallo=True)
        self.assertEqual(self.f.frenos("001")[0], 0)
        self.f.gasto("001", 1, "x", fallo=True)
        codigo, lineas = self.f.frenos("001")
        self.assertEqual(codigo, 1)
        self.assertIn("3 fallos", lineas[0])
        parada = self.raiz / ".brain" / "fabrica" / "estado" / "parada-001.md"
        self.assertIn("Fallos desde el último arranque: 3", parada.read_text(encoding="utf-8"))
        self.assertIn("parada-001.md", "\n".join(lineas))

    def test_un_acierto_no_borra_los_fallos_pero_otro_encargo_no_cuenta(self):
        for _ in range(2):
            self.f.gasto("001", 1, "x", fallo=True)
        self.f.gasto("001", 1, "x", fallo=False)
        self.f.gasto("002", 1, "x", fallo=True)
        self.assertEqual(self.f.frenos("001")[0], 0)
        self.f.gasto("001", 1, "x", fallo=True)
        self.assertEqual(self.f.frenos("001")[0], 1)
        self.assertEqual(self.f.frenos("002")[0], 0)

    def test_atasco_a_los_30_minutos(self):
        self.f.avance("001", "empezó", ahora=1000.0)
        self.assertEqual(self.f.frenos("001", ahora=1000.0 + 29 * 60)[0], 0)
        codigo, lineas = self.f.frenos("001", ahora=1000.0 + 30 * 60)
        self.assertEqual(codigo, 1)
        self.assertIn("30 minutos sin avance", lineas[0])
        texto = (self.raiz / ".brain" / "fabrica" / "estado" / "parada-001.md").read_text(encoding="utf-8")
        self.assertIn("empezó", texto)

    def test_avance_reinicia_el_reloj(self):
        self.f.avance("001", ahora=1000.0)
        self.f.avance("001", ahora=1000.0 + 25 * 60)
        self.assertEqual(self.f.frenos("001", ahora=1000.0 + 50 * 60)[0], 0)

    def test_sin_marca_de_avance_no_hay_atasco(self):
        self.assertEqual(self.f.frenos("001", ahora=10 ** 10)[0], 0)

    def test_reanudar_pone_todo_a_cero(self):
        for _ in range(3):
            self.f.gasto("001", 1, "x", fallo=True)
        self.assertEqual(self.f.frenos("001")[0], 1)
        self.assertEqual(self.f.frenos("001", reanudar=True)[0], 0)
        self.assertEqual(self.f.frenos("001")[0], 0)
        for _ in range(3):
            self.f.gasto("001", 1, "x", fallo=True)
        self.assertEqual(self.f.frenos("001")[0], 1)

    def test_la_carta_cambia_los_topes(self):
        (self.raiz / ".brain" / "fabrica").mkdir(parents=True, exist_ok=True)
        (self.raiz / ".brain" / "fabrica" / "carta.md").write_text("- auto_reintentos_max: 1\n- auto_atasco_minutos: 5\n", encoding="utf-8")
        self.f.gasto("001", 1, "x", fallo=True)
        self.assertEqual(self.f.frenos("001")[0], 1)
        self.f.avance("002", ahora=0.0)
        self.assertEqual(self.f.frenos("002", ahora=6 * 60.0)[0], 1)

    def test_archivo_de_frenos_roto_no_tumba(self):
        est = self.raiz / ".brain" / "fabrica" / "estado"
        est.mkdir(parents=True, exist_ok=True)
        (est / "frenos.json").write_text("[1, 2", encoding="utf-8")
        self.assertEqual(self.f.frenos("001")[0], 0)
        (est / "frenos.json").write_text("[1]", encoding="utf-8")
        self.assertEqual(self.f.avance("001")[0], 0)

    def test_foto_se_para_con_tres_fallos(self):
        subprocess.run(["git", "-C", str(self.raiz), "init", "-q", "-b", "main"], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(self.raiz), "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q",
                        "--allow-empty", "-m", "i"], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(self.raiz), "checkout", "-q", "-b", "linea/x"], check=True, capture_output=True)
        (self.raiz / ".brain" / "fabrica" / "esperado.md").write_text(ESPERADO_BUENO, encoding="utf-8")
        self.assertEqual(self.f.foto(self.raiz, "001")[0], 0)
        for _ in range(3):
            self.f.gasto("001", 1, "x", fallo=True)
        self.assertEqual(self.f.foto(self.raiz, "001")[0], 1)

    def test_en_ingles(self):
        f = fabrica.Fabrica(self.raiz, {"idioma": "en"})
        for _ in range(3):
            f.gasto("001", 1, "x", fallo=True)
        self.assertIn("failures", f.frenos("001")[1][0])


INFORME_BUENO = """# Informe de entrega: prueba
## Lo pedido
- Un comando que imprime OK con datos válidos
## Lo hecho
- El comando y su prueba, requisito R1
## Lo extra
- nada: no apareció nada fuera de lo pedido
## Lo probado de verdad
- Otra IA ejecutó el comando con casos buenos y malos; evidencia en R1/salida.txt
## Lo no probado
- nada: no hay aspecto visual que juzgar
## Decisiones de la línea por su cuenta
- Nombre del archivo elegido por la línea: datos.csv
"""


class InformeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.raiz = Path(self.tmp.name)
        self.f = fabrica.Fabrica(self.raiz, {"idioma": "es"})
        self.ruta = self.raiz / ".brain" / "fabrica" / "informe.md"
        self.ruta.parent.mkdir(parents=True)

    def test_informe_completo_pasa_por_defecto_y_por_ruta(self):
        self.ruta.write_text(INFORME_BUENO, encoding="utf-8")
        self.assertEqual(self.f.informe()[0], 0)
        otra = self.raiz / "otro.md"
        otra.write_text(INFORME_BUENO, encoding="utf-8")
        self.assertEqual(self.f.informe(otra)[0], 0)

    def test_sin_archivo_falla(self):
        self.assertEqual(self.f.informe()[0], 1)

    def test_falta_una_seccion(self):
        self.ruta.write_text(INFORME_BUENO.replace("## Lo no probado", "## Otra cosa"), encoding="utf-8")
        codigo, lineas = self.f.informe()
        self.assertEqual(codigo, 1)
        self.assertIn("Lo no probado", lineas[0])

    def test_seccion_vacia_o_con_plantilla_o_con_nada_a_secas(self):
        self.ruta.write_text(INFORME_BUENO.replace("- nada: no hay aspecto visual que juzgar", ""), encoding="utf-8")
        self.assertIn("Lo no probado", self.f.informe()[1][0])
        self.ruta.write_text(INFORME_BUENO.replace("- nada: no hay aspecto visual que juzgar", "- <lista>"), encoding="utf-8")
        self.assertEqual(self.f.informe()[0], 1)
        self.ruta.write_text(INFORME_BUENO.replace("- nada: no hay aspecto visual que juzgar", "- nada"), encoding="utf-8")
        self.assertEqual(self.f.informe()[0], 1)  # un «nada» sin motivo no vale

    def test_en_ingles(self):
        f = fabrica.Fabrica(self.raiz, {"idioma": "en"})
        txt = ("# Report\n## What was asked\n- The order and its criterion\n## What was done\n- Built the command\n"
               "## Extras\n- nothing: all asked\n## Really tested\n- Another AI ran it, evidence saved\n"
               "## Not tested\n- nothing: no visuals\n## Decisions the line made on its own\n- File name chosen: data.csv\n")
        self.ruta.write_text(txt, encoding="utf-8")
        self.assertEqual(f.informe()[0], 0)
        self.ruta.write_text(txt.replace("## Not tested", "## X"), encoding="utf-8")
        self.assertIn("Not tested", f.informe()[1][0])

    def test_la_plantilla_sin_rellenar_no_pasa_y_rellena_si(self):
        txt = (RAIZ / ".brain" / "biblioteca" / "PLANTILLAS_FABRICA.md").read_text(encoding="utf-8")
        bloque = txt.split("## 11.")[1].split("```markdown")[1].split("```")[0]
        self.ruta.write_text(bloque, encoding="utf-8")
        self.assertEqual(self.f.informe()[0], 1)  # todo son <…>
        txt_en = None if _falta_en("PLANTILLAS_FABRICA.en.md") else (RAIZ / ".brain" / "biblioteca" / "PLANTILLAS_FABRICA.en.md").read_text(encoding="utf-8")
        for es, en in fabrica.Fabrica.INFORME:
            self.assertIn("## " + es, bloque)
            if txt_en is not None:
                self.assertIn("## " + en, txt_en)


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
