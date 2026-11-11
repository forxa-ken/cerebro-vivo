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


if __name__ == "__main__":
    unittest.main()
