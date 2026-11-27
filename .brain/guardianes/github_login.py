#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Login local con GitHub y listado de repositorios (spec 097, fase 2). Solo lectura: no clona nada.

Flujo de dispositivo de la GitHub App «Cerebro Vivo» (sin secreto de cliente ni clave privada, no hacen falta): se pide un código a
GitHub, el usuario lo aprueba en github.com y GitHub entrega un token de usuario que caduca a las 8 h (con token de renovación).
El token vive SOLO en el almacén de credenciales de Windows (ctypes sobre advapi32) o, donde no existe, en memoria del proceso:
nunca en un archivo, en una dirección, en un argumento de comando ni en un registro. Toda llamada externa lleva tiempo máximo,
solo habla con https://github.com y https://api.github.com, no sigue redirecciones y no sigue enlaces que devuelva GitHub.
Sin nada que instalar: solo librería estándar."""

import json
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request

from textos import tp  # noqa: E402  (los mensajes salen de textos.py, es/en)

CLIENT_ID = "Iv23liCXSlLiXiOOndBi"        # identificador público de la app (no es un secreto)
URL_INSTALAR = "https://github.com/apps/cerebro-vivo/installations/new"
HOSTS_PERMITIDOS = ("github.com", "api.github.com")
TIMEOUT = 15                               # segundos por llamada externa (regla 8)
TOPE_RESPUESTA = 2_000_000
POR_PAGINA = 100
TOPE_PAGINAS = 30                          # 3000 repositorios por instalación; más, se corta y se avisa
TOPE_INSTALACIONES = 50
MARGEN_RENOVAR = 60                        # segundos antes de caducar en que ya se renueva
OBJETIVO_ALMACEN = "CerebroVivo:github"
TIPO_DISPOSITIVO = "urn:ietf:params:oauth:grant-type:device_code"


class ErrorGitHub(Exception):
    """Falla con una clave de texto de la web (`web_gh_err_*`) que explica en llano qué pasó."""

    def __init__(self, clave, codigo=502):
        super().__init__(clave)
        self.clave, self.codigo = clave, codigo

    def texto(self):
        return tp(self.clave)


# ---------------------------------------------------------------- almacén del token
class AlmacenMemoria:
    """Donde no hay almacén del sistema: el token solo vive mientras viva el proceso. Nunca va a un archivo."""
    nombre = "memoria"

    def __init__(self):
        self._v = None

    def guardar(self, texto):
        self._v = texto

    def leer(self):
        return self._v

    def borrar(self):
        self._v = None


class AlmacenWindows:
    """Administrador de credenciales de Windows: CredWriteW / CredReadW / CredDeleteW (ligado al usuario de Windows)."""
    nombre = "windows"
    _GENERICA, _LOCAL = 1, 2  # CRED_TYPE_GENERIC, CRED_PERSIST_LOCAL_MACHINE

    def __init__(self):
        import ctypes
        from ctypes import wintypes
        self._ct = ctypes
        w = wintypes

        class CRED(ctypes.Structure):
            _fields_ = [("Flags", w.DWORD), ("Type", w.DWORD), ("TargetName", w.LPWSTR), ("Comment", w.LPWSTR),
                        ("LastWritten", w.FILETIME), ("CredentialBlobSize", w.DWORD),
                        ("CredentialBlob", ctypes.POINTER(ctypes.c_ubyte)), ("Persist", w.DWORD),
                        ("AttributeCount", w.DWORD), ("Attributes", ctypes.c_void_p), ("TargetAlias", w.LPWSTR),
                        ("UserName", w.LPWSTR)]
        self._CRED = CRED
        a = ctypes.windll.advapi32
        a.CredWriteW.argtypes, a.CredWriteW.restype = [ctypes.POINTER(CRED), w.DWORD], w.BOOL
        a.CredReadW.argtypes, a.CredReadW.restype = [w.LPCWSTR, w.DWORD, w.DWORD, ctypes.POINTER(ctypes.POINTER(CRED))], w.BOOL
        a.CredDeleteW.argtypes, a.CredDeleteW.restype = [w.LPCWSTR, w.DWORD, w.DWORD], w.BOOL
        a.CredFree.argtypes, a.CredFree.restype = [ctypes.c_void_p], None
        self._a = a

    def guardar(self, texto):
        ct = self._ct
        datos = texto.encode("utf-8")
        if len(datos) > 2000:
            raise ErrorGitHub("web_gh_err_almacen", 500)
        buf = (ct.c_ubyte * len(datos)).from_buffer_copy(datos)
        c = self._CRED()
        c.Type, c.TargetName, c.Persist = self._GENERICA, OBJETIVO_ALMACEN, self._LOCAL
        c.CredentialBlobSize, c.CredentialBlob, c.UserName = len(datos), ct.cast(buf, ct.POINTER(ct.c_ubyte)), "cerebro-vivo"
        if not self._a.CredWriteW(ct.byref(c), 0):
            raise ErrorGitHub("web_gh_err_almacen", 500)

    def leer(self):
        ct = self._ct
        p = ct.POINTER(self._CRED)()
        if not self._a.CredReadW(OBJETIVO_ALMACEN, self._GENERICA, 0, ct.byref(p)):
            return None
        try:
            c = p.contents
            return ct.string_at(c.CredentialBlob, c.CredentialBlobSize).decode("utf-8", errors="replace")
        finally:
            self._a.CredFree(p)

    def borrar(self):
        self._a.CredDeleteW(OBJETIVO_ALMACEN, self._GENERICA, 0)  # si no existía, no pasa nada


def almacen_del_sistema():
    if sys.platform == "win32":
        try:
            return AlmacenWindows()
        except (ImportError, AttributeError, OSError):
            pass
    return AlmacenMemoria()


# ---------------------------------------------------------------- llamadas externas
class _SinRedirecciones(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):  # una redirección podría llevar el token a otro sitio: no se sigue
        return None


def http_real(metodo, url, datos=None, token=None):
    """(código, JSON). Solo https a los hosts permitidos, con tiempo máximo y sin redirecciones."""
    p = urllib.parse.urlsplit(url)
    if p.scheme != "https" or p.hostname not in HOSTS_PERMITIDOS:
        raise ErrorGitHub("web_gh_err_host", 500)
    cuerpo = urllib.parse.urlencode(datos).encode("utf-8") if datos is not None else None
    req = urllib.request.Request(url, data=cuerpo, method=metodo, headers={
        "Accept": "application/json", "User-Agent": "cerebro-vivo", "X-GitHub-Api-Version": "2022-11-28"})
    if token:
        req.add_header("Authorization", "Bearer " + token)
    try:
        try:
            with urllib.request.build_opener(_SinRedirecciones).open(req, timeout=TIMEOUT) as r:
                codigo, crudo = r.status, r.read(TOPE_RESPUESTA + 1)
        except urllib.error.HTTPError as e:
            codigo, crudo = e.code, e.read(TOPE_RESPUESTA + 1)
    except (urllib.error.URLError, OSError):  # incluye tiempo agotado y sin conexión
        raise ErrorGitHub("web_gh_err_red")
    if len(crudo) > TOPE_RESPUESTA:
        raise ErrorGitHub("web_gh_err_respuesta")
    try:
        return codigo, json.loads(crudo.decode("utf-8"))
    except ValueError:
        raise ErrorGitHub("web_gh_err_respuesta")


HTTP = http_real          # las pruebas ponen aquí un GitHub simulado
ALMACEN = almacen_del_sistema()
AHORA = time.time         # idem: reloj sustituible en pruebas
_CERROJO = threading.Lock()
_CODIGO = {}              # código de dispositivo en curso; el navegador nunca lo ve


def _cargar():
    try:
        v = json.loads(ALMACEN.leer() or "")
        return v if isinstance(v, dict) and isinstance(v.get("acceso"), str) else None
    except ValueError:
        return None


def _guardar_respuesta(r):
    """Guarda los tokens de una respuesta correcta de GitHub (código nuevo o renovación)."""
    ahora = AHORA()
    ALMACEN.guardar(json.dumps({
        "acceso": r["access_token"], "vence": ahora + int(r.get("expires_in") or 28800),
        "renovacion": r.get("refresh_token") or "", "vence_renovacion": ahora + int(r.get("refresh_token_expires_in") or 0)}))


def _token():
    """Token de usuario vigente; lo renueva si va a caducar. None si no hay sesión o ya no se puede renovar."""
    v = _cargar()
    if not v:
        return None
    ahora = AHORA()
    if v.get("vence", 0) - MARGEN_RENOVAR > ahora:
        return v["acceso"]
    if v.get("renovacion") and v.get("vence_renovacion", 0) > ahora:
        c, r = HTTP("POST", "https://github.com/login/oauth/access_token", {
            "client_id": CLIENT_ID, "grant_type": "refresh_token", "refresh_token": v["renovacion"]})
        if c == 200 and isinstance(r, dict) and r.get("access_token"):
            _guardar_respuesta(r)
            return r["access_token"]
    ALMACEN.borrar()
    return None


# ---------------------------------------------------------------- acciones
def iniciar():
    """Pide a GitHub un código de dispositivo. Devuelve lo que el usuario ve: el código y dónde aprobarlo."""
    c, r = HTTP("POST", "https://github.com/login/device/code", {"client_id": CLIENT_ID})
    if c != 200 or not isinstance(r, dict) or not r.get("device_code") or not r.get("user_code"):
        raise ErrorGitHub("web_gh_err_iniciar")
    dir_ok = r.get("verification_uri") or ""
    if urllib.parse.urlsplit(dir_ok).hostname != "github.com" or not dir_ok.startswith("https://"):
        raise ErrorGitHub("web_gh_err_iniciar")  # solo se enseña una dirección de aprobación de github.com
    ahora = AHORA()
    with _CERROJO:
        _CODIGO.clear()
        _CODIGO.update({"device_code": r["device_code"], "vence": ahora + int(r.get("expires_in") or 900),
                        "intervalo": max(5, int(r.get("interval") or 5)), "ultimo": 0})
    return {"codigo": str(r["user_code"])[:20], "direccion": dir_ok, "caduca_en": int(r.get("expires_in") or 900),
            "espera": _CODIGO["intervalo"]}


def sondear():
    """Pregunta a GitHub si el usuario ya aprobó. Estados: pendiente, ok, caducado, denegado, sin_codigo."""
    ahora = AHORA()
    with _CERROJO:
        if not _CODIGO:
            return {"estado": "sin_codigo"}
        if ahora >= _CODIGO["vence"]:
            _CODIGO.clear()
            return {"estado": "caducado"}
        if ahora - _CODIGO["ultimo"] < _CODIGO["intervalo"]:  # respeta el intervalo que pidió GitHub
            return {"estado": "pendiente", "espera": _CODIGO["intervalo"]}
        _CODIGO["ultimo"] = ahora
        dispositivo = _CODIGO["device_code"]
    c, r = HTTP("POST", "https://github.com/login/oauth/access_token", {
        "client_id": CLIENT_ID, "device_code": dispositivo, "grant_type": TIPO_DISPOSITIVO})
    if not isinstance(r, dict):
        raise ErrorGitHub("web_gh_err_respuesta")
    if r.get("access_token"):
        _guardar_respuesta(r)
        with _CERROJO:
            _CODIGO.clear()
        return {"estado": "ok"}
    e = r.get("error")
    if e == "authorization_pending":
        return {"estado": "pendiente", "espera": _CODIGO.get("intervalo", 5)}
    if e == "slow_down":
        with _CERROJO:
            if _CODIGO:
                _CODIGO["intervalo"] = int(r.get("interval") or _CODIGO["intervalo"] + 5)
        return {"estado": "pendiente", "espera": _CODIGO.get("intervalo", 10)}
    with _CERROJO:
        _CODIGO.clear()
    if e == "access_denied":
        return {"estado": "denegado"}
    if e in ("expired_token", "token_expired"):
        return {"estado": "caducado"}
    raise ErrorGitHub("web_gh_err_respuesta")


def salir():
    ALMACEN.borrar()
    with _CERROJO:
        _CODIGO.clear()
    return {"ok": True}


def _pedir(token, ruta):
    c, r = HTTP("GET", "https://api.github.com" + ruta, None, token)
    if c == 401:
        ALMACEN.borrar()
        raise ErrorGitHub("web_gh_err_sesion", 401)
    if c == 403 or c == 429:
        raise ErrorGitHub("web_gh_err_limite", 429)
    if c != 200 or not isinstance(r, dict):
        raise ErrorGitHub("web_gh_err_respuesta")
    return r


def estado():
    """¿Hay sesión? Sin llamadas a GitHub salvo la renovación, si toca."""
    try:
        return {"sesion": _token() is not None, "almacen": ALMACEN.nombre, "instalar": URL_INSTALAR, "en_curso": bool(_CODIGO)}
    except ErrorGitHub:
        return {"sesion": False, "almacen": ALMACEN.nombre, "instalar": URL_INSTALAR, "en_curso": bool(_CODIGO)}


def repositorios():
    """Repositorios que la persona puede ver Y que la app tiene instalados, paginando la respuesta de GitHub.
    Marcados por defecto los normales; forks y archivados, desmarcados (la web los oculta tras un botón)."""
    token = _token()
    if not token:
        raise ErrorGitHub("web_gh_err_sesion", 401)
    yo = _pedir(token, "/user")
    instalaciones, repos, cortado = [], [], False
    pagina = 1
    while pagina <= TOPE_PAGINAS and len(instalaciones) < TOPE_INSTALACIONES:
        r = _pedir(token, "/user/installations?per_page=%d&page=%d" % (POR_PAGINA, pagina))
        lote = r.get("installations") if isinstance(r.get("installations"), list) else []
        instalaciones += [i for i in lote if isinstance(i, dict) and isinstance(i.get("id"), int)]
        if len(lote) < POR_PAGINA:
            break
        pagina += 1
    for inst in instalaciones[:TOPE_INSTALACIONES]:
        cuenta = inst.get("account") if isinstance(inst.get("account"), dict) else {}
        pagina = 1
        while True:
            if pagina > TOPE_PAGINAS:
                cortado = True
                break
            r = _pedir(token, "/user/installations/%d/repositories?per_page=%d&page=%d" % (inst["id"], POR_PAGINA, pagina))
            lote = r.get("repositories") if isinstance(r.get("repositories"), list) else []
            for x in lote:
                if not isinstance(x, dict) or not isinstance(x.get("full_name"), str):
                    continue
                normal = not x.get("fork") and not x.get("archived")
                repos.append({"nombre": x["full_name"], "privado": bool(x.get("private")), "fork": bool(x.get("fork")),
                              "archivado": bool(x.get("archived")), "kb": int(x.get("size") or 0), "marcado": normal,
                              "instalacion": str(cuenta.get("login") or "")})
            if len(lote) < POR_PAGINA:
                break
            pagina += 1
    return {"usuario": str(yo.get("login") or ""), "repos": repos, "cortado": cortado, "instalar": URL_INSTALAR,
            "instalaciones": [{"cuenta": str((i.get("account") or {}).get("login") or ""),
                               "tipo": str((i.get("account") or {}).get("type") or ""),
                               "seleccion": str(i.get("repository_selection") or "")} for i in instalaciones[:TOPE_INSTALACIONES]]}
