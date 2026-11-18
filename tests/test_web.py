# -*- coding: utf-8 -*-
"""Spec 090, fase 1: la web local es de solo lectura, solo escucha en 127.0.0.1, exige la clave y no sale de `.brain/`."""
import importlib.util
import json
import os
import shutil
import tempfile
import threading
import unittest
import urllib.error
import urllib.request

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_espec = importlib.util.spec_from_file_location("web", os.path.join(RAIZ, ".brain", "guardianes", "web.py"))
web = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(web)


def poner(raiz, rel, texto):
    ruta = os.path.join(raiz, *rel.split("/"))
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)


class TestWeb(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.d, True)
        poner(self.d, ".brain/pendientes.md", "# Pendientes\n- uno\n")
        poner(self.d, ".brain/decisions.log", "linea 1\nlinea final\n")
        poner(self.d, ".brain/lecciones/a.md", "# Lección de heredocs\n\nUn heredoc roto.\n")
        poner(self.d, ".brain/guardianes/guardianes.json", '{"secreto": "no"}')
        poner(self.d, "fuera.md", "# fuera de .brain\n")
        self.srv, self.clave = web.crear(self.d, 0)
        self.puerto = self.srv.server_address[1]
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.addCleanup(self._parar)

    def _parar(self):
        self.srv.shutdown()
        self.srv.server_close()

    def pedir(self, ruta, clave="auto", metodo="GET", host=None):
        cab = {}
        if clave == "auto":
            clave = self.clave
        if clave is not None:
            cab["X-Clave"] = clave
        if host:
            cab["Host"] = host
        req = urllib.request.Request("http://127.0.0.1:%d%s" % (self.puerto, ruta), headers=cab, method=metodo,
                                     data=b"x" if metodo != "GET" else None)
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                return r.status, r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            return e.code, ""

    def test_solo_escucha_en_loopback(self):
        self.assertEqual(self.srv.server_address[0], "127.0.0.1")

    def test_sin_clave_o_con_clave_mala_no_atiende(self):
        self.assertEqual(self.pedir("/api/estado", clave=None)[0], 403)
        self.assertEqual(self.pedir("/api/estado", clave="mala")[0], 403)
        self.assertEqual(self.pedir("/?k=mala", clave=None)[0], 403)
        self.assertEqual(self.pedir("/?k=" + self.clave, clave=None)[0], 200)

    def test_host_ajeno_se_rechaza(self):
        self.assertEqual(self.pedir("/api/estado", host="malo.example")[0], 403)
        self.assertEqual(self.pedir("/api/estado", host="localhost:%d" % self.puerto)[0], 200)

    def test_ningun_metodo_escribe(self):
        for m in ("POST", "PUT", "DELETE", "PATCH"):
            self.assertEqual(self.pedir("/api/doc?r=.brain/pendientes.md", metodo=m)[0], 405, m)

    def test_estado_y_documentos(self):
        c, cuerpo = self.pedir("/api/estado")
        e = json.loads(cuerpo)
        self.assertEqual(c, 200)
        self.assertIn("uno", e["pendientes"])
        self.assertEqual(e["registro"], "linea final")
        self.assertEqual(self.pedir("/api/doc?r=.brain/lecciones/a.md")[1].splitlines()[0], "# Lección de heredocs")
        self.assertEqual(json.loads(self.pedir("/api/lista?c=lecciones")[1]), [".brain/lecciones/a.md"])
        self.assertEqual(self.pedir("/api/lista?c=nada")[0], 404)

    def test_no_sale_de_brain_ni_sirve_otros_tipos(self):
        for r in ("fuera.md", "../fuera.md", ".brain/../fuera.md", ".brain/%2e%2e/fuera.md", ".brain/guardianes/guardianes.json",
                  "/etc/passwd", "C:/Windows/win.ini", ".brain"):
            self.assertEqual(self.pedir("/api/doc?r=" + r)[0], 404, r)
        self.assertIsNone(web.ruta_segura(self.d, ".brain/lecciones/../../fuera.md"))

    def test_buscador(self):
        c, cuerpo = self.pedir("/api/buscar?q=heredocs")
        self.assertEqual(c, 200)
        self.assertEqual(json.loads(cuerpo)[0]["archivo"], ".brain/lecciones/a.md")

    def test_buscador_no_muestra_enlaces_que_salen_de_brain(self):
        poner(self.d, "../" + os.path.basename(self.d) + "_ajeno/secreto.md", "# Secreto de heredocs\n")
        ajeno = os.path.join(os.path.dirname(self.d), os.path.basename(self.d) + "_ajeno", "secreto.md")
        self.addCleanup(shutil.rmtree, os.path.dirname(ajeno), True)
        try:
            os.symlink(ajeno, os.path.join(self.d, ".brain", "lecciones", "enlace.md"))
        except (OSError, NotImplementedError):
            self.skipTest("sin permiso para crear enlaces simbólicos")
        archivos = [r["archivo"] for r in json.loads(self.pedir("/api/buscar?q=heredocs")[1])]
        self.assertNotIn(".brain/lecciones/enlace.md", archivos)
        self.assertEqual(self.pedir("/api/doc?r=.brain/lecciones/enlace.md")[0], 404)

    def test_estado_con_archivos_grandes_enseña_el_final(self):
        poner(self.d, ".brain/pendientes.md", "x" * 30000 + "\nFINAL\n")
        poner(self.d, ".brain/decisions.log", "a\n" * 600000 + "ultima\n")
        e = json.loads(self.pedir("/api/estado")[1])
        self.assertIn("FINAL", e["pendientes"])
        self.assertEqual(e["registro"], "ultima")

    def test_ningun_metodo_deja_rastro(self):
        antes = sorted(os.listdir(os.path.join(self.d, ".brain")))
        for m in ("POST", "PUT", "DELETE"):
            self.pedir("/api/doc?r=.brain/pendientes.md", metodo=m)
        self.assertEqual(sorted(os.listdir(os.path.join(self.d, ".brain"))), antes)
        with open(os.path.join(self.d, ".brain", "pendientes.md"), encoding="utf-8") as f:
            self.assertEqual(f.read(), "# Pendientes\n- uno\n")

    def test_medir_solo_acepta_la_lista_cerrada(self):
        self.assertEqual(self.pedir("/api/medir?q=skills%20--proyecto%20x")[0], 404)
        self.assertEqual(self.pedir("/api/medir?q=%3B%20rm%20-rf")[0], 404)
        self.assertEqual(sorted(web.MEDIR), ["fabrica", "ritual", "skills"])

    def test_textos_en_los_dos_idiomas_y_pagina_sin_inyeccion(self):
        es = {k for k in web.TEXTOS["es"] if k.startswith("web_")}
        en = {k for k in web.TEXTOS["en"] if k.startswith("web_")}
        self.assertEqual(es, en)
        self.assertTrue(es)
        pagina = web.PAGINA
        self.assertNotIn("innerHTML", pagina)  # los documentos se pintan con textContent
        usadas = {x for x in __import__("re").findall(r"T\.(web_\w+)", pagina)}
        self.assertTrue(usadas <= es, usadas - es)


if __name__ == "__main__":
    unittest.main()
