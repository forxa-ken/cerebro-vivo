# -*- coding: utf-8 -*-
"""Guardián 10 (spec 052): vigilancia de librerías, con respuestas simuladas (sin internet)."""
import datetime
import importlib.util
import os
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_espec = importlib.util.spec_from_file_location("librerias", os.path.join(RAIZ, ".brain", "guardianes", "librerias.py"))
lib = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(lib)

A = {"activo": True, "requisitos": "requirements.txt", "timeout": 1, "dias_aviso": 10, "avisar_version_mayor": True, "ignorar": []}


def carpeta(requisitos="flask>=3.0\ndiscord.py>=2.3  # bot\n"):
    d = tempfile.mkdtemp()
    with open(os.path.join(d, "requirements.txt"), "w", encoding="utf-8") as f:
        f.write(requisitos)
    return d


def falso(vulnerables=(), ultimas=None, version="1.0.0"):
    """Red simulada: OSV marca como vulnerables los paquetes de `vulnerables`; PyPI devuelve `ultimas`."""
    ultimas = ultimas or {}

    def http(url, datos=None, timeout=7):
        if url == lib.OSV_LOTE:
            return {"results": [{"vulns": [{"id": "GHSA-x"}]} if q["package"]["name"] in vulnerables else {} for q in datos["queries"]]}
        if url.startswith(lib.OSV_VULN):
            return {"summary": "fallo de prueba", "affected": [{"ranges": [{"events": [{"introduced": "0"}, {"fixed": "9.9"}]}]}]}
        return {"info": {"version": ultimas.get(url.split("/")[-2], version)}}
    return http


class TestChequeo(unittest.TestCase):
    def setUp(self):  # la versión "instalada" es la mínima del requirements de prueba, no la real del equipo
        self.original = lib.version_instalada
        lib.version_instalada = lambda nombre, minima: minima

    def tearDown(self):
        lib.version_instalada = self.original

    def test_lee_requisitos(self):
        self.assertEqual(lib.leer_requisitos(os.path.join(carpeta(), "requirements.txt")), [("flask", "3.0"), ("discord-py", "2.3")])

    def test_detecta_vulnerabilidad(self):
        est = lib.chequear(carpeta(), A, falso(vulnerables=("flask",)))
        av = lib.avisos(est, A)
        self.assertEqual(len(av), 1)
        self.assertIn("flask", av[0])
        self.assertIn("9.9", av[0])

    def test_detecta_version_mayor_y_calla_en_menor(self):
        d = carpeta("flask==2.0.0\n")
        self.assertEqual(len(lib.avisos(lib.chequear(d, A, falso(ultimas={"flask": "3.1.0"})), A)), 1)
        self.assertEqual(lib.avisos(lib.chequear(d, A, falso(ultimas={"flask": "2.9.0"})), A), [])

    def test_calla_si_falla_la_red(self):
        def roto(url, datos=None, timeout=7):
            raise TimeoutError("sin red")
        self.assertIsNone(lib.chequear(carpeta(), A, roto))
        self.assertIsNone(lib.chequear(carpeta(), A, lambda *a, **k: {"basura": 1}))

    def test_respeta_ignorar_y_avisar_mayor(self):
        est = lib.chequear(carpeta(), A, falso(vulnerables=("flask",)))
        self.assertEqual(lib.avisos(est, dict(A, ignorar=[{"id": "GHSA-x", "motivo": "no nos afecta"}])), [])
        est = lib.chequear(carpeta("flask==2.0.0\n"), A, falso(ultimas={"flask": "3.0.0"}))
        self.assertEqual(lib.avisos(est, dict(A, avisar_version_mayor=False)), [])


class TestResumen(unittest.TestCase):
    def setUp(self):
        self.estado_original = lib.ESTADO
        lib.ESTADO = os.path.join(tempfile.mkdtemp(), "estado.json")

    def tearDown(self):
        lib.ESTADO = self.estado_original

    def guardar(self, dias, vuln=False):
        import json
        fecha = (datetime.date.today() - datetime.timedelta(days=dias)).isoformat()
        vulns = [{"id": "GHSA-x", "resumen": "", "corregida": ""}] if vuln else []
        with open(lib.ESTADO, "w", encoding="utf-8") as f:
            json.dump({"fecha": fecha, "paquetes": [{"nombre": "flask", "version": "1", "ultima": "1", "mayor": False, "vulns": vulns}]}, f)

    def test_lineas(self):
        if not os.path.exists(os.path.join(RAIZ, "requirements.txt")):
            self.skipTest("el proyecto no es de Python")
        cfg = {"librerias_activo": True, "librerias": A}
        self.assertIn("sin chequear", lib.resumen(RAIZ, cfg)[0])
        self.guardar(3)
        self.assertIn("sin avisos", lib.resumen(RAIZ, cfg)[0])
        self.assertNotIn("toca", lib.resumen(RAIZ, cfg)[0])
        self.guardar(12)
        self.assertIn("toca volver a chequear", lib.resumen(RAIZ, cfg)[0])
        self.guardar(1, vuln=True)
        self.assertIn("1 aviso", lib.resumen(RAIZ, cfg)[0])

    def test_apagado_calla(self):
        self.guardar(30, vuln=True)
        self.assertEqual(lib.resumen(RAIZ, {"librerias_activo": False, "librerias": A}), [])

    def test_resumen_no_usa_red(self):
        original = lib.http_json
        lib.http_json = lambda *a, **k: self.fail("el resumen no debe usar la red")
        try:
            self.guardar(1)
            lib.resumen(RAIZ, {"librerias_activo": True, "librerias": A})
        finally:
            lib.http_json = original

    @unittest.skipUnless(os.path.exists(os.path.join(RAIZ, "requirements.txt")), "el proyecto no es de Python")
    def test_configuracion_real_presente(self):
        a = lib.ajustes(lib.cargar_config())
        self.assertTrue(a["activo"])
        self.assertTrue(os.path.exists(os.path.join(RAIZ, a["requisitos"])))


if __name__ == "__main__":
    unittest.main()
