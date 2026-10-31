import importlib.util
import json
import os
import shutil
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
espec = importlib.util.spec_from_file_location("modo_auto", os.path.join(RAIZ, ".brain", "guardianes", "modo_auto.py"))
ma = importlib.util.module_from_spec(espec)
espec.loader.exec_module(ma)

A = {"activo": True, "mensajes_chat_nuevo": 4, "contexto": 200000, "base": "copias_bd/b.db", "prueba": "copias_bd/p.db", "origen": "users.db"}
SPEC = "# Spec 900: x\n\n- **Estado:** %s\n\n- [ ] Tocar `app/uno.py` y `tests/`\n"


class ModoAutoTest(unittest.TestCase):
    def setUp(self):
        self.raiz = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.raiz, ".brain", "specs"))
        self.addCleanup(shutil.rmtree, self.raiz, True)
        self.spec("aprobada")
        self.estado = {"activo": True, "cola": ["900"], "chat_inicio": "s1", "relevo": False, "parado": "", "fallos": {}, "otros_sitios": []}

    def spec(self, estado):
        with open(os.path.join(self.raiz, ".brain", "specs", "900-x.md"), "w", encoding="utf-8") as f:
            f.write(SPEC % estado)

    def decide(self, herramienta, datos, estado=None, **kw):
        entrada = {"tool_name": herramienta, "tool_input": datos, "session_id": kw.pop("sesion", "s1")}
        return ma.decidir(entrada, estado or self.estado, A, self.raiz, **kw)

    def edita(self, ruta, **kw):
        return self.decide("Edit", {"file_path": os.path.join(self.raiz, ruta)}, **kw)[0]

    def test_apagado_deja_pasar_todo(self):
        self.estado["activo"] = False
        self.assertIsNone(self.edita("cualquier/cosa.py"))

    def test_archivos_de_la_spec_y_brain(self):
        self.assertIsNone(self.edita("app/uno.py"))
        self.assertIsNone(self.edita("tests/test_x.py"))
        self.assertIsNone(self.edita(".brain/decisions.log"))

    def test_archivo_fuera_de_la_spec_se_bloquea(self):
        self.assertIn("no está en la spec", self.edita("server.py"))

    def test_guardian_protegido_salvo_que_la_spec_lo_nombre(self):
        self.assertIn("guardián", self.edita(".brain/guardianes/cierre.py"))

    def test_otro_sitio_documentado_se_permite(self):
        self.estado["otros_sitios"] = ["server.py"]
        self.assertIsNone(self.edita("server.py"))

    def test_spec_sin_aprobar_bloquea(self):
        self.spec("borrador")
        self.assertIn("no está aprobada", self.edita("app/uno.py"))

    def test_cola_vacia_bloquea(self):
        self.estado["cola"] = []
        self.assertIn("sin specs", self.edita("app/uno.py"))

    def test_chat_no_nuevo_bloquea_y_nuevo_se_adopta(self):
        self.estado["chat_inicio"] = ""
        self.assertIn("NUEVO", self.edita("app/uno.py", mensajes=30))
        motivo, nuevo = self.decide("Edit", {"file_path": os.path.join(self.raiz, "app/uno.py")}, mensajes=2)
        self.assertIsNone(motivo)
        self.assertEqual(nuevo["chat_inicio"], "s1")

    def test_otro_chat_solo_con_relevo(self):
        self.assertIn("otro chat", self.edita("app/uno.py", sesion="s2"))
        self.estado["relevo"] = True
        motivo, nuevo = self.decide("Edit", {"file_path": os.path.join(self.raiz, "app/uno.py")}, sesion="s2")
        self.assertIsNone(motivo)
        self.assertEqual((nuevo["chat_inicio"], nuevo["relevo"]), ("s2", False))

    def test_200k_pide_relevo_y_solo_deja_escribir_el_traspaso(self):
        motivo, nuevo = self.decide("Edit", {"file_path": os.path.join(self.raiz, "app/uno.py")}, contexto=210000)
        self.assertIn("relevo", motivo)
        self.assertTrue(nuevo["relevo"])
        self.assertIsNone(self.decide("Write", {"file_path": os.path.join(self.raiz, ".brain", "traspaso.md")}, contexto=210000)[0])

    def test_parado_bloquea_salvo_continuar(self):
        self.estado["parado"] = "x falló 2 veces"
        self.assertIn("PARADO", self.edita("app/uno.py"))
        self.assertIsNone(self.decide("Bash", {"command": "python .brain/guardianes/modo_auto.py continuar"})[0])

    def test_bash_prohibe_push_y_base_real(self):
        self.assertIn("GitHub", self.decide("Bash", {"command": "git push origin main"})[0])
        self.assertIn("base de datos real", self.decide("Bash", {"command": "sqlite3 users.db .tables"})[0])
        self.assertIsNone(self.decide("Bash", {"command": "sqlite3 copias_bd/modo_auto_prueba.db .tables"})[0])
        self.assertIsNone(self.decide("Bash", {"command": "python -m unittest tests.test_modo_auto"})[0])


class ComandosTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.viejo = ma.ESTADO
        ma.ESTADO = os.path.join(self.tmp, "modo_auto.json")
        self.addCleanup(setattr, ma, "ESTADO", self.viejo)

    def test_activar_exige_spec_aprobada(self):
        self.assertIn("no existe", ma.activar(["999"]).lower())
        self.assertFalse(ma.leer_estado().get("activo"))

    def test_dos_fallos_paran_y_continuar_levanta(self):
        ma.guardar_estado({"activo": True, "cola": ["900"], "fallos": {}})
        self.assertNotIn("falló", ma.registrar_fallo("prueba_x"))
        self.assertIn("2 veces", ma.registrar_fallo("prueba_x"))
        self.assertTrue(ma.leer_estado()["parado"])
        ma.continuar()
        self.assertEqual(ma.leer_estado()["parado"], "")

    def test_fallo_arreglado_al_momento_no_para(self):
        ma.guardar_estado({"activo": True, "cola": ["900"], "fallos": {}})
        ma.registrar_fallo("prueba_x")
        ma.resuelto("prueba_x")
        ma.registrar_fallo("prueba_x")
        self.assertEqual(ma.leer_estado().get("parado", ""), "")

    def test_hecha_avanza_la_cola(self):
        ma.guardar_estado({"activo": True, "cola": ["900", "901"], "otros_sitios": ["a.py"]})
        ma.hecha()
        e = ma.leer_estado()
        self.assertEqual((e["cola"], e["otros_sitios"]), (["901"], []))

    def test_base_de_prueba_fija_no_se_sobrescribe(self):
        raiz = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, raiz, True)
        viejo_raiz, ma.RAIZ = ma.RAIZ, raiz
        self.addCleanup(setattr, ma, "RAIZ", viejo_raiz)
        with open(os.path.join(raiz, "users.db"), "w") as f:
            f.write("original")
        a = dict(A)
        ma.base_prueba("crear", a)
        with open(os.path.join(raiz, "users.db"), "w") as f:
            f.write("cambiada")
        self.assertIn("ya existe", ma.base_prueba("crear", a))
        with open(os.path.join(raiz, "copias_bd", "p.db"), "w") as f:
            f.write("ensuciada")
        ma.base_prueba("restaurar", a)
        with open(os.path.join(raiz, "copias_bd", "p.db")) as f:
            self.assertEqual(f.read(), "original")


if __name__ == "__main__":
    unittest.main()
