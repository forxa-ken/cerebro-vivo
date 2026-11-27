# -*- coding: utf-8 -*-
"""Spec 097, fase 2: login local con GitHub y listado de repositorios, siempre con un GitHub simulado (ninguna llamada real)."""
import importlib.util
import json
import os
import shutil
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GUARD = os.path.join(RAIZ, ".brain", "guardianes")
sys.path.insert(0, GUARD)
import github_login as gh  # noqa: E402

_e = importlib.util.spec_from_file_location("web", os.path.join(GUARD, "web.py"))
web = importlib.util.module_from_spec(_e)
_e.loader.exec_module(web)

SECRETO = "falso-acceso-PRUEBA-123"
RENOVACION = "falso-renovacion-PRUEBA-456"


class Falso:
    """GitHub simulado: guarda las llamadas y contesta lo que se le diga."""

    def __init__(self):
        self.llamadas, self.cola, self.rutas = [], [], {}

    def __call__(self, metodo, url, datos=None, token=None):
        self.llamadas.append((metodo, url, dict(datos or {}), token))
        if self.cola:
            r = self.cola.pop(0)
            if isinstance(r, Exception):
                raise r
            return r
        if url in self.rutas:
            return self.rutas[url]
        raise AssertionError("llamada no prevista: " + url)


class Base(unittest.TestCase):
    def setUp(self):
        self.f, self.alm, self.t = Falso(), gh.AlmacenMemoria(), [1000.0]
        self._viejo = (gh.HTTP, gh.ALMACEN, gh.AHORA)
        gh.HTTP, gh.ALMACEN, gh.AHORA = self.f, self.alm, lambda: self.t[0]
        gh._CODIGO.clear()
        self.addCleanup(self._restaurar)

    def _restaurar(self):
        gh.HTTP, gh.ALMACEN, gh.AHORA = self._viejo
        gh._CODIGO.clear()

    def sesion(self, vence=1000.0 + 28800, renovacion=RENOVACION, vence_renovacion=1000.0 + 86400):
        self.alm.guardar(json.dumps({"acceso": SECRETO, "vence": vence, "renovacion": renovacion, "vence_renovacion": vence_renovacion}))


class TestLogin(Base):
    def codigo(self, **extra):
        r = {"device_code": "DC-1", "user_code": "ABCD-1234", "verification_uri": "https://github.com/login/device",
             "expires_in": 900, "interval": 5}
        r.update(extra)
        self.f.cola.append((200, r))
        return gh.iniciar()

    def test_iniciar_pide_codigo_con_el_client_id_y_no_enseña_el_codigo_de_dispositivo(self):
        r = self.codigo()
        self.assertEqual(r["codigo"], "ABCD-1234")
        self.assertNotIn("DC-1", json.dumps(r))
        metodo, url, datos, token = self.f.llamadas[0]
        self.assertEqual((metodo, url, datos, token), ("POST", "https://github.com/login/device/code", {"client_id": gh.CLIENT_ID}, None))

    def test_direccion_de_otro_sitio_se_rechaza(self):
        for mala in ("https://github.com.evil.com/x", "http://github.com/login/device", "https://evil.com/login/device"):
            self.f.cola.append((200, {"device_code": "d", "user_code": "u", "verification_uri": mala}))
            with self.assertRaises(gh.ErrorGitHub):
                gh.iniciar()

    def test_sondear_pendiente_respeta_el_intervalo(self):
        self.codigo()
        self.f.cola.append((200, {"error": "authorization_pending"}))
        self.assertEqual(gh.sondear()["estado"], "pendiente")
        n = len(self.f.llamadas)
        self.assertEqual(gh.sondear()["estado"], "pendiente")  # antes de 5 s: no vuelve a preguntar a GitHub
        self.assertEqual(len(self.f.llamadas), n)

    def test_sondear_ok_guarda_el_token_solo_en_el_almacen(self):
        self.codigo()
        self.f.cola.append((200, {"access_token": SECRETO, "expires_in": 28800, "refresh_token": RENOVACION, "refresh_token_expires_in": 15000000}))
        r = gh.sondear()
        self.assertEqual(r, {"estado": "ok"})
        self.assertNotIn(SECRETO, json.dumps(r))
        self.assertEqual(json.loads(self.alm.leer())["acceso"], SECRETO)
        _, _, datos, _ = self.f.llamadas[-1]
        self.assertEqual(datos["grant_type"], gh.TIPO_DISPOSITIVO)
        self.assertEqual(datos["device_code"], "DC-1")
        self.assertEqual(gh._CODIGO, {})  # el código de dispositivo no se reutiliza

    def test_slow_down_sube_el_intervalo(self):
        self.codigo()
        self.f.cola.append((200, {"error": "slow_down", "interval": 10}))
        self.assertEqual(gh.sondear()["espera"], 10)
        self.t[0] += 6  # con 10 s de intervalo, 6 s no bastan
        n = len(self.f.llamadas)
        gh.sondear()
        self.assertEqual(len(self.f.llamadas), n)

    def test_denegado_caducado_y_sin_codigo(self):
        self.assertEqual(gh.sondear()["estado"], "sin_codigo")
        self.codigo()
        self.f.cola.append((200, {"error": "access_denied"}))
        self.assertEqual(gh.sondear()["estado"], "denegado")
        self.assertEqual(self.alm.leer(), None)
        self.codigo()
        self.t[0] += 901
        self.assertEqual(gh.sondear()["estado"], "caducado")

    def test_error_de_red_se_explica(self):
        self.codigo()
        self.f.cola.append(gh.ErrorGitHub("web_gh_err_red"))
        with self.assertRaises(gh.ErrorGitHub) as c:
            gh.sondear()
        self.assertEqual(c.exception.clave, "web_gh_err_red")

    def test_renovacion_antes_de_caducar(self):
        self.sesion(vence=1000.0 + 30)  # caduca en 30 s: dentro del margen
        self.f.cola.append((200, {"access_token": "falso-acceso-NUEVO", "expires_in": 28800, "refresh_token": "falso-renovacion-NUEVO", "refresh_token_expires_in": 15000000}))
        self.assertTrue(gh.estado()["sesion"])
        _, url, datos, _ = self.f.llamadas[0]
        self.assertEqual(url, "https://github.com/login/oauth/access_token")
        self.assertEqual((datos["grant_type"], datos["refresh_token"]), ("refresh_token", RENOVACION))
        self.assertEqual(json.loads(self.alm.leer())["acceso"], "falso-acceso-NUEVO")

    def test_sin_renovacion_posible_se_cierra_la_sesion(self):
        self.sesion(vence=900.0, renovacion="", vence_renovacion=0)
        self.assertFalse(gh.estado()["sesion"])
        self.assertIsNone(self.alm.leer())

    def test_salir_borra_el_token(self):
        self.sesion()
        gh.salir()
        self.assertIsNone(self.alm.leer())
        self.assertFalse(gh.estado()["sesion"])


def repo(nombre, kb=10, **k):
    d = {"full_name": nombre, "private": True, "fork": False, "archived": False, "size": kb}
    d.update(k)
    return d


class TestListado(Base):
    def prepara(self, instalaciones, repos_por_instalacion):
        self.sesion()
        self.f.rutas["https://api.github.com/user"] = (200, {"login": "forxa-ken"})
        self.f.rutas["https://api.github.com/user/installations?per_page=100&page=1"] = (200, {"installations": instalaciones})
        for i, lista in repos_por_instalacion.items():
            self.f.rutas["https://api.github.com/user/installations/%d/repositories?per_page=100&page=1" % i] = (200, {"repositories": lista})

    def test_lista_marca_los_normales_y_desmarca_forks_y_archivados(self):
        self.prepara([{"id": 7, "account": {"login": "forxa-ken", "type": "User"}, "repository_selection": "all"}],
                     {7: [repo("forxa-ken/a", 100), repo("forxa-ken/b", fork=True), repo("forxa-ken/c", archived=True)]})
        r = gh.repositorios()
        self.assertEqual(r["usuario"], "forxa-ken")
        self.assertEqual({x["nombre"]: x["marcado"] for x in r["repos"]}, {"forxa-ken/a": True, "forxa-ken/b": False, "forxa-ken/c": False})
        self.assertEqual(r["instalaciones"][0]["seleccion"], "all")

    def test_el_token_solo_va_en_la_cabecera_nunca_en_la_direccion(self):
        self.prepara([{"id": 7, "account": {"login": "x"}}], {7: [repo("x/a")]})
        gh.repositorios()
        for _, url, datos, token in self.f.llamadas:
            self.assertNotIn(SECRETO, url)
            self.assertNotIn(SECRETO, json.dumps(datos))
            self.assertEqual(token, SECRETO)
            self.assertTrue(url.startswith("https://api.github.com/"))

    def test_pagina_hasta_agotar(self):
        self.sesion()
        self.f.rutas["https://api.github.com/user"] = (200, {"login": "u"})
        self.f.rutas["https://api.github.com/user/installations?per_page=100&page=1"] = (200, {"installations": [{"id": 1, "account": {"login": "u"}}]})
        self.f.rutas["https://api.github.com/user/installations/1/repositories?per_page=100&page=1"] = (200, {"repositories": [repo("u/r%d" % i) for i in range(100)]})
        self.f.rutas["https://api.github.com/user/installations/1/repositories?per_page=100&page=2"] = (200, {"repositories": [repo("u/ultimo")]})
        r = gh.repositorios()
        self.assertEqual(len(r["repos"]), 101)
        self.assertFalse(r["cortado"])

    def test_sin_sesion_no_llama_a_github(self):
        with self.assertRaises(gh.ErrorGitHub) as c:
            gh.repositorios()
        self.assertEqual(c.exception.codigo, 401)
        self.assertEqual(self.f.llamadas, [])

    def test_401_cierra_la_sesion_y_403_pide_esperar(self):
        self.sesion()
        self.f.cola.append((401, {"message": "Bad credentials"}))
        with self.assertRaises(gh.ErrorGitHub) as c:
            gh.repositorios()
        self.assertEqual(c.exception.clave, "web_gh_err_sesion")
        self.assertIsNone(self.alm.leer())
        self.sesion()
        self.f.cola.append((403, {"message": "rate limit"}))
        with self.assertRaises(gh.ErrorGitHub) as c:
            gh.repositorios()
        self.assertEqual(c.exception.clave, "web_gh_err_limite")

    def test_datos_raros_de_github_no_rompen(self):
        self.prepara([{"id": 7, "account": None}, "basura", {"sin": "id"}], {7: [None, 5, {"full_name": 3}, repo("a/b")]})
        r = gh.repositorios()
        self.assertEqual([x["nombre"] for x in r["repos"]], ["a/b"])


class TestRealSeguro(unittest.TestCase):
    def test_http_real_solo_habla_con_github_por_https(self):
        for url in ("http://github.com/x", "https://evil.com/x", "https://github.com.evil.com/x", "file:///etc/passwd"):
            with self.assertRaises(gh.ErrorGitHub):
                gh.http_real("GET", url)

    def test_http_real_no_sigue_redirecciones(self):
        self.assertIsNone(gh._SinRedirecciones().redirect_request(None, None, 302, "", {}, "https://evil.com"))


@unittest.skipUnless(sys.platform == "win32", "solo Windows")
class TestAlmacenWindows(unittest.TestCase):
    def test_guarda_lee_y_borra_con_un_valor_falso_en_una_entrada_de_prueba(self):
        viejo = gh.OBJETIVO_ALMACEN
        gh.OBJETIVO_ALMACEN = "CerebroVivo:prueba-automatica"  # nunca la entrada real de la sesión de la persona
        self.addCleanup(setattr, gh, "OBJETIVO_ALMACEN", viejo)
        a = gh.AlmacenWindows()
        self.addCleanup(a.borrar)
        a.borrar()
        self.assertIsNone(a.leer())
        a.guardar('{"acceso": "valor-falso-áé"}')
        self.assertEqual(a.leer(), '{"acceso": "valor-falso-áé"}')
        a.borrar()
        self.assertIsNone(a.leer())


class TestWeb(Base):
    def setUp(self):
        super().setUp()
        self.d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.d, True)
        os.makedirs(os.path.join(self.d, ".brain"))
        self.srv, self.clave = web.crear(self.d, 0)
        self.puerto = self.srv.server_address[1]
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.addCleanup(lambda: (self.srv.shutdown(), self.srv.server_close()))

    def pedir(self, ruta, cuerpo=None, clave=True, origen=None, host=None):
        h = {"X-Clave": self.clave} if clave else {}
        if origen:
            h["Origin"] = origen
        if host:
            h["Host"] = host
        if cuerpo is not None:
            h["Content-Type"] = "application/json"
        req = urllib.request.Request("http://127.0.0.1:%d%s" % (self.puerto, ruta), headers=h, method="POST" if cuerpo is not None else "GET",
                                     data=json.dumps(cuerpo).encode() if cuerpo is not None else None)
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                return r.status, json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            return e.code, None

    def token(self, a):
        return self.pedir("/api/token?a=" + a)[1]["token"]

    def test_estado_sin_sesion_y_sin_clave(self):
        self.assertEqual(self.pedir("/api/github/estado")[1]["sesion"], False)
        self.assertEqual(self.pedir("/api/github/estado", clave=False)[0], 403)
        self.assertEqual(self.pedir("/api/github/repos", clave=False)[0], 403)

    def test_acciones_exigen_token_de_un_solo_uso_y_origen_propio(self):
        mala = [{"accion": "github_iniciar"}, {"accion": "github_iniciar", "token": "inventado"}]
        for cuerpo in mala:
            self.assertEqual(self.pedir("/api/accion", cuerpo)[0], 403)
        self.assertEqual(self.f.llamadas, [])  # sin token válido, GitHub ni se entera
        t = self.token("github_iniciar")
        self.assertEqual(self.pedir("/api/accion", {"accion": "github_iniciar", "token": t}, origen="http://evil.com")[0], 403)
        self.assertEqual(self.pedir("/api/accion", {"accion": "github_iniciar", "token": t}, host="evil.com")[0], 403)
        self.f.cola.append((200, {"device_code": "d", "user_code": "ABCD", "verification_uri": "https://github.com/login/device"}))
        t = self.token("github_iniciar")
        c, r = self.pedir("/api/accion", {"accion": "github_iniciar", "token": t}, origen="http://127.0.0.1:%d" % self.puerto)
        self.assertEqual((c, r["codigo"]), (200, "ABCD"))
        self.assertEqual(self.pedir("/api/accion", {"accion": "github_iniciar", "token": t})[0], 403)  # el token ya se gastó

    def test_un_token_de_otra_accion_no_vale_para_salir(self):
        self.sesion()
        t = self.token("github_sondear")
        self.assertEqual(self.pedir("/api/accion", {"accion": "github_salir", "token": t})[0], 403)
        self.assertIsNotNone(self.alm.leer())

    def test_el_token_de_github_nunca_sale_por_la_web_ni_al_registro(self):
        self.sesion()
        self.f.rutas["https://api.github.com/user"] = (200, {"login": "u"})
        self.f.rutas["https://api.github.com/user/installations?per_page=100&page=1"] = (200, {"installations": []})
        salidas = [self.pedir("/api/github/estado")[1], self.pedir("/api/github/repos")[1]]
        self.assertNotIn(SECRETO, json.dumps(salidas))
        self.assertNotIn(RENOVACION, json.dumps(salidas))
        t = self.token("github_salir")
        self.assertEqual(self.pedir("/api/accion", {"accion": "github_salir", "token": t})[0], 200)
        log = os.path.join(self.d, ".brain", "web_actividad.log")
        texto = ""
        if os.path.isfile(log):
            with open(log, encoding="utf-8") as f:
                texto = f.read()
        self.assertNotIn(SECRETO, texto)
        self.assertIn("github_salir", texto)

    def test_errores_de_github_llegan_en_llano(self):
        c, _ = self.pedir("/api/github/repos")
        self.assertEqual(c, 401)

    def test_pagina_y_textos_en_los_dos_idiomas(self):
        es = {k for k in web.TEXTOS["es"] if k.startswith("web_gh")}
        en = {k for k in web.TEXTOS["en"] if k.startswith("web_gh")}
        self.assertEqual(es, en)
        self.assertGreater(len(es), 20)
        with open(os.path.join(GUARD, "github_login.py"), encoding="utf-8") as f:
            usados = set(__import__("re").findall(r"web_gh_err_\w+", f.read()))
        self.assertLessEqual(usados, es)  # cada error que puede dar el módulo tiene su texto


if __name__ == "__main__":
    unittest.main()
