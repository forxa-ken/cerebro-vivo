#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Web local del cerebro (spec 090): fase 1 (ver, buscar, medir) y fase 2 (proyectos y simulaciones).

Uso:
  python .brain/guardianes/web.py                abre la web en el navegador (solo escucha en 127.0.0.1)
  python .brain/guardianes/web.py --puerto 8765  puerto fijo (por defecto, uno libre)
  python .brain/guardianes/web.py --no-abrir     no abre el navegador; muestra la dirección
Cada arranque crea una clave al azar que va en la dirección: sin ella, ninguna petición se atiende, y una página abierta en
otra pestaña no puede leer ni mandar órdenes. Los documentos se leen solo de `.brain/` (`.md` y `decisions.log`). Lo único que escribe es la
lista de proyectos, la actividad de la web y, con confirmación y tras simular, instalar o actualizar un proyecto registrado
(`web_proyectos.py`). Las simulaciones no cambian ningún proyecto. No sube nada.
Solo librería estándar."""

import hmac
import http.server
import json
import os
import secrets
import subprocess
import sys
import threading
import time
import urllib.parse
import webbrowser

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, AQUI)
import buscar as _buscar  # noqa: E402
import web_proyectos as _capa  # noqa: E402
from textos import TEXTOS, idioma, tp  # noqa: E402

TOPE_DOC = 1_000_000          # un documento más grande no se sirve
TOPE_TEXTO_ESTADO = 20_000
CARPETAS = {"pendientes": ".brain/pendientes.md", "registro": ".brain/decisions.log", "decisiones": ".brain/decisions",
            "lecciones": ".brain/lecciones", "specs": ".brain/specs", "biblioteca": ".brain/biblioteca",
            "respuestas": ".brain/respuestas"}
MEDIR = {"skills": "--skills", "fabrica": "--fabrica", "ritual": "--ritual"}  # lista cerrada: nada del usuario llega al comando
HOSTS = ("127.0.0.1", "localhost")
TOPE_CUERPO = 4096         # una petición POST más grande se rechaza
VIDA_TOKEN = 300           # segundos que vale un token de acción (de un solo uso)


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
.tabs{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:8px}aside input,aside select{width:100%%;margin:6px 0}
</style></head><body>
<header><h1>Cerebro Vivo</h1><nav id="nav"></nav><span class="m" id="ro"></span></header>
<main><aside id="lado"></aside><section id="cuerpo"></section></main>
<script>
const K=new URLSearchParams(location.search).get('k')||'';let T={};
async function api(p){const r=await fetch(p,{headers:{'X-Clave':K}});if(!r.ok){let m=T.web_error||'error';try{m=(await r.clone().json()).error||m}catch(e){}throw new Error(m)}return r}
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
function el(t,txt,fn){const e=document.createElement(t);if(txt!==undefined)e.textContent=txt;if(fn)e.onclick=fn;return e}
async function post(a,d){const t=await (await api('/api/token?a='+a)).json();d.accion=a;d.token=t.token;
 const r=await fetch('/api/accion',{method:'POST',headers:{'X-Clave':K,'Content-Type':'application/json'},body:JSON.stringify(d)});
 let j={};try{j=await r.json()}catch(e){}if(!r.ok)throw new Error(j.error||T.web_error);return j}
function panel(p,tab){const c=$('cuerpo');limpia(c);const b=el('div');b.className='tabs';
 [['resumen',T.web_t_resumen],['pendientes',T.web_t_pendientes],['actualizar',T.web_t_actualizar],['instalar',T.web_t_instalar],['tareas',T.web_t_tareas]].forEach(x=>{const k=el('button',x[1],()=>ficha(p,x[0]));if(x[0]===tab)k.classList.add('on');b.appendChild(k)});
 c.appendChild(b);return c}
async function simular(p,a,d,salida){salida.textContent=T.web_cargando;d.ruta=p.ruta;try{salida.textContent=(await post(a,d)).texto}catch(x){salida.textContent=x.message}}
async function real(p,a,d,salida,msg){if(!confirm(msg+'\\n\\n'+p.ruta))return;salida.textContent=T.web_cargando;d.ruta=p.ruta;try{salida.textContent=(await post(a,d)).texto}catch(x){salida.textContent=x.message}}
async function tarea(p,a,d,salida,msg){if(!confirm(msg+'\\n\\n'+p.ruta))return;salida.textContent=T.web_cargando;d.ruta=p.ruta;
 let id;try{id=(await post(a,d)).id}catch(x){salida.textContent=x.message;return}
 const parar=el('button',T.web_tarea_parar,async()=>{try{await post('parar_tarea',{id:id})}catch(x){}});salida.parentNode.insertBefore(parar,salida);
 for(;;){await new Promise(r=>setTimeout(r,1000));let e;try{e=await (await api('/api/tarea?id='+id)).json()}catch(x){salida.textContent=x.message;break}
  salida.textContent=T['web_tarea_estado_'+e.estado]+'\\n\\n'+e.salida;if(e.estado!=='corriendo')break}
 parar.remove()}
function tareas(p,c,s){c.appendChild(el('button',T.web_tarea_pruebas,()=>tarea(p,'tarea_pruebas',{},s,T.web_confirma_tarea)));
 c.appendChild(el('button',T.web_tarea_auditor,()=>tarea(p,'tarea_auditor',{},s,T.web_confirma_tarea)));
 const ch=el('input');ch.placeholder=T.web_tarea_chat;const tx=el('input');tx.placeholder=T.web_tarea_texto;tx.style.width='100%%';
 c.appendChild(el('div'));c.appendChild(ch);c.appendChild(tx);
 c.appendChild(el('button',T.web_tarea_cerrar,()=>{if(!ch.value.trim()||!tx.value.trim())return;tarea(p,'tarea_cerrar',{chat:ch.value,texto:tx.value},s,T.web_confirma_cerrar+'\\n'+ch.value+' | '+tx.value)}));
 s.textContent=T.web_simular_ayuda}
function ficha(p,tab){const c=panel(p,tab);const s=el('pre');
 if(tab==='resumen')s.textContent=[p.nombre,p.ruta,'',T.web_version+' '+(p.version||T.web_sin_arnes),T.web_nivel+' '+(p.nivel||'-'),T.web_version_repo+' '+p.version_repo,p.atrasado?T.web_atrasado:T.web_al_dia].join('\\n')+(p.existe?'':'\\n'+T.web_err_no_existe);
 else if(tab==='pendientes')s.textContent=p.pendientes||T.web_sin_pendientes;
 else if(tab==='tareas')tareas(p,c,s);
 else if(tab==='actualizar'){c.appendChild(el('button',T.web_simular,()=>simular(p,'simular_actualizar',{},s)));
  c.appendChild(el('button',T.web_real_actualizar,()=>real(p,'actualizar_real',{},s,T.web_confirma_actualizar)));s.textContent=T.web_simular_ayuda}
 else{const n=el('select');['ligero','medio','completo'].forEach(v=>{const o=el('option',v);o.value=v;n.appendChild(o)});n.value='completo';n.style.width='auto';c.appendChild(n);
  c.appendChild(el('button',T.web_simular,()=>simular(p,'simular_instalar',{nivel:n.value},s)));
  c.appendChild(el('button',T.web_real_instalar,()=>real(p,'instalar_real',{nivel:n.value},s,T.web_confirma_instalar)));s.textContent=T.web_simular_ayuda}
 c.appendChild(s)}
async function proyectos(){marca('proyectos');limpia($('lado'));pre(T.web_cargando);try{
 const d=await (await api('/api/proyectos')).json();limpia($('lado'));
 d.proyectos.forEach(p=>$('lado').appendChild(enlace(p.nombre+(p.atrasado?' \u26a0':''),()=>ficha(p,'resumen'))));
 const f=el('input');f.placeholder=T.web_ruta;$('lado').appendChild(f);
 $('lado').appendChild(el('button',T.web_anadir,async()=>{if(!f.value.trim())return;if(!confirm(T.web_confirma_anadir+'\\n'+f.value))return;
  try{await post('registrar_proyecto',{ruta:f.value});await proyectos()}catch(x){pre(x.message)}}));
 pre(d.proyectos.length?T.web_elige_proyecto:T.web_sin_proyectos)}catch(x){pre(x.message)}}
(async()=>{try{T=await (await api('/api/textos')).json()}catch(e){document.body.textContent='?';return}
 $('ro').textContent=T.web_modo;const nav=$('nav');
 const bt=(id,txt,fn)=>{const b=document.createElement('button');b.dataset.id=id;b.textContent=txt;b.onclick=fn;nav.appendChild(b)};
 bt('inicio',T.web_inicio,inicio);
 ['decisiones','lecciones','specs','biblioteca','respuestas'].forEach(c=>bt(c,T['web_c_'+c],()=>carpeta(c)));
 bt('medir',T.web_medir,()=>medir('skills'));
 bt('proyectos',T.web_proyectos,proyectos);
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

    def _origen_propio(self, origen):
        """El `Origin` de un POST debe ser exactamente esta web: http, un host local y el puerto del servidor. Sin la cabecera
        (clientes que no son un navegador) la petición sigue necesitando la clave en cabecera y el token; los navegadores siempre
        mandan `Origin` en un POST, y «null» o cualquier otro se rechaza."""
        try:
            u = urllib.parse.urlsplit(origen)
            return u.scheme == "http" and (u.hostname or "") in HOSTS and u.port == self.server.server_address[1]
        except ValueError:
            return False

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
            if p == "/api/proyectos":
                codigo, res = _capa.ejecutar(raiz, _capa.USUARIO_LOCAL, "ver_proyectos")
                return self._responder(codigo, json.dumps(res, ensure_ascii=False), "application/json; charset=utf-8")
            if p == "/api/token":  # un token de un solo uso por acción que cambia algo (spec 090, 12.2)
                a = arg("a")
                if a not in _capa.ACCIONES or a == "ver_proyectos":
                    return self._responder(404, "404")
                return self._responder(200, json.dumps({"token": self.server.nuevo_token(a)}), "application/json; charset=utf-8")
            if p == "/api/tarea":
                e = _capa.estado_tarea(arg("id"))
                return self._responder(404, "404") if e is None else self._responder(200, json.dumps(e, ensure_ascii=False), "application/json; charset=utf-8")
            if p == "/api/medir":
                salida = medir(raiz, arg("q"))
                return self._responder(404, "404") if salida is None else self._responder(200, salida)
        except Exception as e:  # una petición mala no tumba el servidor
            return self._responder(500, type(e).__name__)
        return self._responder(404, "404")

    def _no_permitido(self):
        self._responder(405, "405")  # ningún método escribe documentos; solo POST /api/accion, con permiso, y para la capa de reglas

    def do_POST(self):
        url = urllib.parse.urlsplit(self.path)
        if url.path != "/api/accion":
            return self._no_permitido()
        origen = self.headers.get("Origin")
        if not self._autorizado({}) or (origen is not None and not self._origen_propio(origen)):
            return self._responder(403, "403")  # la clave solo vale en la cabecera, y el origen, si viene, ha de ser esta misma web (esquema, host y puerto)
        if "application/json" not in (self.headers.get("Content-Type") or ""):
            return self._responder(415, "415")
        try:
            largo = int(self.headers.get("Content-Length") or 0)
            datos = json.loads(self.rfile.read(largo).decode("utf-8")) if 0 < largo <= TOPE_CUERPO else None
        except (ValueError, OSError, RecursionError):  # un JSON anidado hasta el infinito no corta la conexión
            datos = None
        if not isinstance(datos, dict) or not isinstance(datos.get("accion"), str):
            return self._responder(400, "400")
        if not self.server.gastar_token(datos.get("token"), datos["accion"]):
            return self._responder(403, "403")
        codigo, res = _capa.ejecutar(self.server.raiz, _capa.USUARIO_LOCAL, datos["accion"], datos.get("ruta"), datos)
        self._responder(codigo, json.dumps(res, ensure_ascii=False), "application/json; charset=utf-8")

    do_PUT = do_DELETE = do_PATCH = do_OPTIONS = _no_permitido


def crear(raiz=RAIZ, puerto=0):
    """Servidor ligado solo a 127.0.0.1 (no arranca el bucle). Devuelve (servidor, clave)."""
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", puerto), Manejador)
    srv.raiz = raiz
    srv.clave = secrets.token_urlsafe(16)
    srv.tokens = {}
    srv.cerrojo = threading.Lock()

    def nuevo_token(accion):
        token = secrets.token_urlsafe(16)
        with srv.cerrojo:
            ahora = time.monotonic()
            for k in [k for k, (_, vence) in srv.tokens.items() if vence < ahora]:
                del srv.tokens[k]
            srv.tokens[token] = (accion, ahora + VIDA_TOKEN)
        return token

    def gastar_token(token, accion):
        """Verdadero una sola vez, para la acción para la que se pidió y mientras no caduque."""
        if not isinstance(token, str):
            return False
        with srv.cerrojo:
            valor = srv.tokens.pop(token, None)
        return bool(valor) and valor[0] == accion and valor[1] >= time.monotonic()

    srv.nuevo_token, srv.gastar_token = nuevo_token, gastar_token
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
