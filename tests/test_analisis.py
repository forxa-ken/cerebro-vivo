# -*- coding: utf-8 -*-
"""Guardián 7 (spec 049): análisis AST de SQL inseguro, límites y reglas del proyecto."""
import importlib.util
import json
import os
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_espec = importlib.util.spec_from_file_location("analisis", os.path.join(RAIZ, ".brain", "guardianes", "analisis.py"))
analisis = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(analisis)

REGLAS = {"analisis": {
    "archivos": ["*.py"], "tope_funcion_nueva": 5, "margen_crecimiento": 2, "margen_archivo_lineas": 1000,
    "sql_excepciones": [{"archivo": "ok.py", "contiene": "ALTER TABLE", "motivo": "x"}],
    "reglas": [
        {"tipo": "llamada_con_timeout", "llamadas": ["urllib.request.urlopen"]},
        {"tipo": "ruta_escritura_audita", "archivos": ["rutas.py"], "patron": "^/api/admin", "excepciones": ["eximida"]},
        {"tipo": "sin_dml_sobre", "tabla": "audit_log"}]}}


def avisos_de(codigo, nombre="x.py", base=None):
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, nombre), "w", encoding="utf-8") as f:
            f.write(codigo)
        return analisis.analizar(d, REGLAS, base if base is not None else {})


class TestSql(unittest.TestCase):
    def test_detecta_sql_armado(self):
        for linea in ('c.execute(f"SELECT * FROM t WHERE a={a}")', 'c.execute("SELECT " + a)',
                      'c.execute("SELECT %s" % a)', 'c.execute("SELECT {}".format(a))'):
            self.assertEqual(len(avisos_de(linea)), 1, linea)

    def test_calla_con_parametros_y_con_excepcion(self):
        self.assertEqual(avisos_de('c.execute("SELECT * FROM t WHERE a=?", (a,))'), [])
        self.assertEqual(avisos_de('c.execute(f"ALTER TABLE {t} ADD COLUMN c")', "ok.py"), [])
        self.assertEqual(len(avisos_de('c.execute(f"ALTER TABLE {t} ADD COLUMN c")', "otro.py")), 1)


class TestLimites(unittest.TestCase):
    LARGA = "def g():\n" + "    a = 1\n" * 9

    def test_funcion_nueva_larga_avisa_y_corta_no(self):
        self.assertEqual(len(avisos_de(self.LARGA, base={"x.py": {"lineas": 1, "funciones": {}}})), 1)
        self.assertEqual(avisos_de("def g():\n    a = 1\n", base={"x.py": {"lineas": 1, "funciones": {}}}), [])

    def test_funcion_existente_solo_avisa_si_crece(self):
        self.assertEqual(avisos_de(self.LARGA, base={"x.py": {"lineas": 10, "funciones": {"g": 10}}}), [])
        self.assertEqual(len(avisos_de(self.LARGA, base={"x.py": {"lineas": 10, "funciones": {"g": 6}}})), 1)

    def test_sin_base_no_avisa(self):
        self.assertEqual(avisos_de(self.LARGA), [])


class TestReglas(unittest.TestCase):
    def test_timeout(self):
        self.assertEqual(len(avisos_de("import urllib.request\nurllib.request.urlopen(u)")), 1)
        self.assertEqual(avisos_de("import urllib.request\nurllib.request.urlopen(u, timeout=5)"), [])

    def test_ruta_de_escritura_sin_auditoria(self):
        malo = '@app.route("/api/admin/x", methods=["POST"])\ndef f():\n    return 1\n'
        bueno = '@app.route("/api/admin/x", methods=["POST"])\ndef f():\n    audit_event("A", "SUCCESS")\n'
        lectura = '@app.route("/api/admin/x")\ndef f():\n    return 1\n'
        eximida = '@app.post("/api/admin/x")\ndef eximida():\n    return 1\n'
        self.assertEqual(len(avisos_de(malo, "rutas.py")), 1)
        self.assertEqual(avisos_de(bueno, "rutas.py"), [])
        self.assertEqual(avisos_de(lectura, "rutas.py"), [])
        self.assertEqual(avisos_de(eximida, "rutas.py"), [])
        self.assertEqual(len(avisos_de(eximida.replace("eximida", "otra"), "rutas.py")), 1)

    def test_tabla_protegida(self):
        self.assertEqual(len(avisos_de('c.execute("DELETE FROM audit_log WHERE id=?", (1,))')), 1)
        self.assertEqual(avisos_de('c.execute("CREATE TRIGGER t BEFORE UPDATE ON audit_log BEGIN SELECT 1; END")'), [])


class TestCodigoReal(unittest.TestCase):
    def test_el_proyecto_sin_avisos(self):
        with open(os.path.join(RAIZ, ".brain", "guardianes", "guardianes.json"), encoding="utf-8") as f:
            cfg = json.load(f)
        avisos = analisis.analizar(RAIZ, cfg)
        self.assertEqual(avisos, [], "El análisis de código tiene avisos: revisar o anotar la excepción con su motivo")

    def test_resumen_apagado_calla(self):
        self.assertEqual(analisis.resumen(RAIZ, {"analisis_activo": False}), [])


if __name__ == "__main__":
    unittest.main()
