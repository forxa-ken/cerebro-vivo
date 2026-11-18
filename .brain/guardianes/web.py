#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Web local del cerebro, fase 1 (spec 090): ver, buscar y medir el uso. SOLO LECTURA.

Uso:
  python .brain/guardianes/web.py                abre la web en el navegador (solo escucha en 127.0.0.1)
  python .brain/guardianes/web.py --puerto 8765  puerto fijo (por defecto, uno libre)
  python .brain/guardianes/web.py --no-abrir     no abre el navegador; muestra la dirección
Cada arranque crea una clave al azar que va en la dirección: sin ella, ninguna petición se atiende, y una página abierta en
otra pestaña no puede leer ni mandar órdenes. Solo se leen `.md` y `decisions.log` de `.brain/`; no escribe nada, no sube nada.
Solo librería estándar."""

import hmac
import http.server
import json
import os
import secrets
import subprocess
import sys
import threading
import urllib.parse
import webbrowser

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, AQUI)
import buscar as _buscar  # noqa: E402
from textos import TEXTOS, idioma, tp  # noqa: E402

TOPE_DOC = 1_000_000          # un documento más grande no se sirve
TOPE_TEXTO_ESTADO = 20_000
CARPETAS = {"pendientes": ".brain/pendientes.md", "registro": ".brain/decisions.log", "decisiones": ".brain/decisions",
            "lecciones": ".brain/lecciones", "specs": ".brain/specs", "biblioteca": ".brain/biblioteca",
            "respuestas": ".brain/respuestas"}
MEDIR = {"skills": "--skills", "fabrica": "--fabrica", "ritual": "--ritual"}  # lista cerrada: nada del usuario llega al comando
HOSTS = ("127.0.0.1", "localhost")


def ruta_segura(raiz, rel):
    """Ruta absoluta de `rel` si es un `.md` o `decisions.log` dentro de `.brain/` (sin salir por `..` ni enlaces); si no, None."""
    if not rel or "\x00" in rel:
        return None
    rel = rel.replace("\\", "/").lstrip("/")
    if not rel.startswith(".brain/"):
        return None
    base = os.path.realpath(os.path.join(raiz, ".brain"))
    ruta = os.path.realpath(os.path.join(raiz, *rel.split("/")))
    try:
        if os.path.commonpath([base, ruta]) != base or ruta == base:
            return None
    except ValueError:
        return None
    if not (ruta.endswith(".md") or os.path.basename(ruta) == "decisions.log"):
        return None
    return ruta if os.path.isfile(ruta) else None


def leer(ruta, tope=TOPE_DOC, cortar=False):
    """Texto del archivo; si pasa de `tope`, None (o, con `cortar`, solo el final: lo último es lo que importa)."""
    grande = os.path.getsize(ruta) > tope
    if grande and not cortar:
        return None
    with open(ruta, "rb") as f:
        if grande:
            f.seek(-tope, os.SEEK_END)
        return f.read().decode("utf-8", errors="replace")


def _git(raiz, *args):
    try:
        r = subprocess.run(["git", *args], cwd=raiz, capture_output=True, text=True, timeout=10)
        return r.stdout.strip() if r.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


def estado(raiz):
    pend = ruta_segura(raiz, ".brain/pendientes.md")
    reg = ruta_segura(raiz, ".brain/decisions.log")
    texto = (leer(pend, TOPE_TEXTO_ESTADO, cortar=True) if pend else "") or ""
    ultima = ""
    if reg:
        lineas = [l for l in (leer(reg, TOPE_DOC, cortar=True) or "").splitlines() if l.strip()]
        ultima = lineas[-1] if lineas else ""
    cambios = _git(raiz, "status", "--short")
    sin_subir = _git(raiz, "rev-list", "--count", "@{u}..HEAD")
    return {"pendientes": texto, "registro": ultima,
            "sin_commitear": len(cambios.splitlines()) if cambios is not None else None,
            "sin_subir": int(sin_subir) if sin_subir and sin_subir.isdigit() else None}


def lista(raiz, carpeta):
    """Archivos `.md` de una carpeta permitida (nombre de CARPETAS), ruta relativa con /; [] si no existe."""
    rel = CARPETAS.get(carpeta)
    if not rel:
        return None
    ruta = os.path.join(raiz, *rel.split("/"))
    if os.path.isfile(ruta):
        return [rel]
    salida = []
    for base, carpetas, nombres in os.walk(ruta):
        carpetas[:] = [c for c in carpetas if c not in ("archive", "copias_arnes", "__pycache__")]
        for n in nombres:
            if n.endswith(".md"):
                salida.append(os.path.relpath(os.path.join(base, n), raiz).replace(os.sep, "/"))
    return sorted(salida)


def medir(raiz, que):
    """Salida de `medir.py` con una opción de la lista cerrada; None si `que` no está en la lista."""
    opcion = MEDIR.get(que)
    if not opcion:
        return None
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    try:
        r = subprocess.run([sys.executable, os.path.join(AQUI, "medir.py"), opcion], cwd=raiz, capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=120, env=env)
        return (r.stdout or "") + (r.stderr or "")
    except (OSError, subprocess.SubprocessError) as e:
        return "%s: %s" % (type(e).__name__, e)


def textos_web():
    return {k: v for k, v in TEXTOS[idioma()].items() if k.startswith("web_")}


PAGINA = """<!doctype html><html lang="%(lang)s"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Cerebro Vivo</title><style>
:root{--f:#f6f6f2;--t:#1d1d1b;--c:#fff;--b:#d9d8d0;--a:#2f5d50}
@media(prefers-color-scheme:dark){:root{--f:#161715;--t:#e8e8e2;--c:#202220;--b:#34372f;--a:#7fc4ad}}
*{box-sizing:border-box}body{margin:0;font:15px/1.5 system-ui,sans-serif;background:var(--f);color:var(--t)}
header{padding:12px 16px;border-bottom:1px solid var(--b);display:flex;gap:12px;flex-wrap:wrap;align-items:center}
h1{font-size:17px;margin:0}nav{display:flex;gap:6px;flex-wrap:wrap}
button,input{font:inherit;color:inherit;background:var(--c);border:1px solid var(--b);border-radius:6px;padding:6px 10px}
button{cursor:pointer}button.on{background:var(--a);color:var(--f);border-color:var(--a)}
main{display:grid;grid-template-columns:minmax(200px,280px) 1fr;gap:12px;padding:12px 16px}
@media(max-width:700px){main{grid-template-columns:1fr}}
aside,section{background:var(--c);border:1px solid var(--b);border-radius:8px;padding:12px;overflow:auto;max-height:80vh}
aside a{display:block;padding:3px 0;color:var(--a);cursor:pointer;word-break:break-all}
pre{white-space:pre-wrap;word-break:break-word;margin:0;font:13px/1.5 ui-monospace,Consolas,monospace}
.m{opacity:.7;font-size:13px}
</style></head><body>
<header><h1>Cerebro Vivo</h1><nav id="nav"></nav><span class="m" id="ro"></span></header>
<main><aside id="lado"></aside><section id="cuerpo"></section></main>
<script>
const K=new URLSearchParams(location.search).get('k')||'';let T={};
async function api(p){const r=await fetch(p,{headers:{'X-Clave':K}});if(!r.ok)throw new Error(T.web_error||'error');return r}
const $=id=>document.getElementById(id);
function limpia(n){while(n.firstChild)n.removeChild(n.firstChild)}
function pre(txt){const p=document.createElement('pre');p.textContent=txt;limpia($('cuerpo'));$('cuerpo').appendChild(p);$('cuerpo').scrollIntoView()}
function marca(id){document.querySelectorAll('#nav button').forEach(b=>b.classList.toggle('on',b.dataset.id===id))}
function enlace(txt,fn){const a=document.createElement('a');a.textContent=txt;a.onclick=fn;return a}
async function doc(r){try{pre(await (await api('/api/doc?r='+encodeURIComponent(r))).text())}catch(e){pre(e.message)}}
async function inicio(){marca('inicio');limpia($('lado'));try{const e=await (await api('/api/estado')).json();
 const L=[T.web_pendientes,'',e.pendientes,'',T.web_registro,e.registro,''];
 if(e.sin_commitear!==null)L.push(T.web_sin_commitear+' '+e.sin_commitear);
 if(e.sin_subir!==null)L.push(T.web_sin_subir+' '+e.sin_subir);pre(L.join('\\n'))}catch(x){pre(x.message)}}
async function carpeta(c){marca(c);limpia($('lado'));pre(T.web_cargando);try{const l=await (await api('/api/lista?c='+c)).json();
 limpia($('lado'));l.forEach(r=>$('lado').appendChild(enlace(r.replace('.brain/',''),()=>doc(r))));
 if(l.length===1)doc(l[0]);else pre(l.length?T.web_elige:T.web_vacio)}catch(x){pre(x.message)}}
async function buscar(q){if(!q.trim())return;marca('buscar');limpia($('lado'));pre(T.web_cargando);try{
 const l=await (await api('/api/buscar?q='+encodeURIComponent(q))).json();limpia($('lado'));
 l.forEach(r=>$('lado').appendChild(enlace(r.titulo+' · '+r.archivo.replace('.brain/',''),()=>doc(r.archivo))));
 pre(l.length?T.web_elige:T.web_sin_resultados)}catch(x){pre(x.message)}}
async function medir(q){marca('medir');limpia($('lado'));['skills','fabrica','ritual'].forEach(n=>$('lado').appendChild(enlace(T['web_medir_'+n],()=>medir(n))));
 pre(T.web_cargando+' '+T['web_medir_'+q]);try{pre(await (await api('/api/medir?q='+q)).text())}catch(x){pre(x.message)}}
(async()=>{try{T=await (await api('/api/textos')).json()}catch(e){document.body.textContent='?';return}
 $('ro').textContent=T.web_solo_lectura;const nav=$('nav');
 const bt=(id,txt,fn)=>{const b=document.createElement('button');b.dataset.id=id;b.textContent=txt;b.onclick=fn;nav.appendChild(b)};
 bt('inicio',T.web_inicio,inicio);
 ['decisiones','lecciones','specs','biblioteca','respuestas'].forEach(c=>bt(c,T['web_c_'+c],()=>carpeta(c)));
 bt('medir',T.web_medir,()=>medir('skills'));
 const f=document.createElement('input');f.type='search';f.placeholder=T.web_buscar;f.onkeydown=e=>{if(e.key==='Enter')buscar(f.value)};nav.appendChild(f);
 inicio()})();
</script></body></html>
"""


class Manejador(http.server.BaseHTTPRequestHandler):
    server_version = "CerebroWeb"

    def log_message(self, *a):  # sin ruido en la terminal
        pass

    def _responder(self, codigo, cuerpo, tipo="text/plain; charset=utf-8"):
        datos = cuerpo.encode("utf-8") if isinstance(cuerpo, str) else cuerpo
        self.send_response(codigo)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(datos)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'")
        self.end_headers()
        self.wfile.write(datos)

    def _autorizado(self, consulta):
        host = (self.headers.get("Host") or "").rsplit(":", 1)[0].strip("[]")
        if host not in HOSTS:  # contra «DNS rebinding»: otra web que apunte su nombre a 127.0.0.1
            return False
        clave = self.headers.get("X-Clave") or (consulta.get("k") or [""])[0]
        return hmac.compare_digest(clave.encode("utf-8"), self.server.clave.encode("utf-8"))

    def do_GET(self):
        url = urllib.parse.urlsplit(self.path)
        consulta = urllib.parse.parse_qs(url.query)
        if not self._autorizado(consulta):
            return self._responder(403, "403")
        raiz, p = self.server.raiz, url.path
        arg = lambda n: (consulta.get(n) or [""])[0]  # noqa: E731
        try:
            if p == "/":
                return self._responder(200, PAGINA % {"lang": idioma()}, "text/html; charset=utf-8")
            if p == "/api/textos":
                return self._responder(200, json.dumps(textos_web(), ensure_ascii=False), "application/json; charset=utf-8")
            if p == "/api/estado":
                return self._responder(200, json.dumps(estado(raiz), ensure_ascii=False), "application/json; charset=utf-8")
            if p == "/api/lista":
                l = lista(raiz, arg("c"))
                return self._responder(404, "404") if l is None else self._responder(200, json.dumps(l), "application/json; charset=utf-8")
            if p == "/api/doc":
                ruta = ruta_segura(raiz, arg("r"))
                texto = leer(ruta) if ruta else None
                return self._responder(404, "404") if texto is None else self._responder(200, texto)
            if p == "/api/buscar":
                res = [r for r in _buscar.buscar(raiz, arg("q")[:200], 15) if ruta_segura(raiz, r["archivo"])]  # un enlace que salga de .brain/ no se muestra
                return self._responder(200, json.dumps(res, ensure_ascii=False), "application/json; charset=utf-8")
            if p == "/api/medir":
                salida = medir(raiz, arg("q"))
                return self._responder(404, "404") if salida is None else self._responder(200, salida)
        except Exception as e:  # una petición mala no tumba el servidor
            return self._responder(500, type(e).__name__)
        return self._responder(404, "404")

    def _no_permitido(self):
        self._responder(405, "405")  # solo lectura: ningún método escribe

    do_POST = do_PUT = do_DELETE = do_PATCH = do_OPTIONS = _no_permitido


def crear(raiz=RAIZ, puerto=0):
    """Servidor ligado solo a 127.0.0.1 (no arranca el bucle). Devuelve (servidor, clave)."""
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", puerto), Manejador)
    srv.raiz = raiz
    srv.clave = secrets.token_urlsafe(16)
    return srv, srv.clave


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = list(sys.argv[1:] if argv is None else argv)
    puerto, abrir = 0, True
    if "--no-abrir" in args:
        abrir = False
    if "--puerto" in args:
        try:
            puerto = int(args[args.index("--puerto") + 1])
        except (IndexError, ValueError):
            print(tp("web_uso"))
            return 1
    srv, clave = crear(RAIZ, puerto)
    url = "http://127.0.0.1:%d/?k=%s" % (srv.server_address[1], clave)
    print(tp("web_arrancada") % url, flush=True)
    if abrir:
        threading.Timer(0.3, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
