#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Presentaciones para humanos (spec 045): convierte un .md en un solo .html autocontenido. Solo librería estándar.

  python .brain/guardianes/diapositivas.py ARCHIVO.md [--salida RUTA.html] [--no-abrir]
  python .brain/guardianes/diapositivas.py --buscar NOMBRE
  python .brain/guardianes/diapositivas.py --comprobar ORIGINAL.md DIAPOSITIVAS.md

Las diapositivas se separan con una línea `---`. Una cabecera opcional `---` inicial admite `titulo:` e `idioma:` (es/en).
El HTML del .md se escapa; solo se admiten enlaces http(s) y relativos; el visor lleva una política que impide cargar nada de internet.
`--buscar` localiza un documento por nombre (biblioteca, specs, .brain y raíz): salida 0 = uno, 2 = ninguno, 3 = varios.
`--comprobar` falla (salida 1) si alguna sección `##` del original no aparece en las diapositivas."""
import html
import os
import re
import sys
import unicodedata
import webbrowser

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, AQUI)
from textos import t, idioma  # noqa: E402
import diagramas  # noqa: E402

AVISOS = []  # diagramas ```mermaid que no se pudieron dibujar (se cuentan al final)

MAX_POR_PARTE = 20
CARPETA_SALIDA = os.path.join(".brain", "diapositivas")
CLAVES_CABECERA = ("titulo", "título", "title", "idioma", "language")


# ---------------------------------------------------------------- lectura del .md
def leer(ruta):
    with open(ruta, "rb") as f:
        return f.read().decode("utf-8").replace("\r\n", "\n")


def separar(texto):
    """(meta, [diapositivas como texto]). Respeta los bloques de código (``` no se corta por dentro)."""
    lineas = texto.split("\n")
    meta = {}
    if lineas and lineas[0].strip() == "---":
        for i in range(1, len(lineas)):
            if lineas[i].strip() == "---":
                cabecera = lineas[1:i]
                if cabecera and all(re.match(r"^\s*[\w\-áéíóúÁÉÍÓÚ]+\s*:", l) for l in cabecera if l.strip()):
                    for l in cabecera:
                        if ":" in l:
                            k, v = l.split(":", 1)
                            meta[k.strip().lower()] = v.strip().strip("\"'")
                    lineas = lineas[i + 1:]
                break
    diapos, actual, en_codigo = [], [], False
    for l in lineas:
        if l.strip().startswith("```"):
            en_codigo = not en_codigo
        if l.strip() == "---" and not en_codigo:
            diapos.append("\n".join(actual))
            actual = []
        else:
            actual.append(l)
    diapos.append("\n".join(actual))
    return meta, [d.strip("\n") for d in diapos if d.strip()]


# ---------------------------------------------------------------- Markdown -> HTML (subconjunto pequeño)
def enlace_permitido(url):
    u = re.sub(r"[\x00-\x20]", "", url).lower()
    if u.startswith(("http://", "https://")):
        return True
    return ":" not in u and not u.startswith("//")


def inline(texto):
    """Escapa y aplica código, negrita, cursiva y enlaces. Todo lo que no sea esto queda como texto."""
    guardados = []

    def codigo(m):
        guardados.append("<code>" + html.escape(m.group(1), quote=False) + "</code>")
        return "\x00%d\x00" % (len(guardados) - 1)

    texto = re.sub(r"`([^`\n]+)`", codigo, texto)
    texto = html.escape(texto, quote=False)

    def enlace(m):
        etiqueta, url = m.group(1), html.unescape(m.group(2).strip())
        if not enlace_permitido(url):
            return etiqueta
        return '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>' % (html.escape(url, quote=True), etiqueta)

    texto = re.sub(r"(?<!!)\[([^\]\n]+)\]\(([^)\s]+)\)", enlace, texto)
    texto = re.sub(r"\*\*([^*\n]+)\*\*", r"<strong>\1</strong>", texto)
    texto = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", texto)
    return re.sub(r"\x00(\d+)\x00", lambda m: guardados[int(m.group(1))], texto)


def _celdas(linea):
    return [c.strip() for c in linea.strip().strip("|").split("|")]


_ITEM = re.compile(r"^(\s*)([-*]|\d+[.)])\s+(.*)$")


def _lista(lineas, i, nivel=0):
    """Lista con subviñetas: una línea con más sangría que la anterior cuelga de ella (hasta 3 niveles)."""
    primera = _ITEM.match(lineas[i].expandtabs(4))
    sangria = len(primera.group(1))
    ordenada = primera.group(2)[0].isdigit()
    items = []
    n = len(lineas)
    while i < n:
        m = _ITEM.match(lineas[i].expandtabs(4))
        if not m or len(m.group(1)) < sangria:
            break
        if len(m.group(1)) > sangria:
            if not items or nivel >= 2:  # sangría suelta o demasiado profunda: se trata como un elemento más
                items.append([m.group(3), ""])
                i += 1
                continue
            sub, i = _lista(lineas, i, nivel + 1)
            items[-1][1] += sub
            continue
        if m.group(2)[0].isdigit() != ordenada:
            break
        items.append([m.group(3), ""])
        i += 1
    etiqueta = "ol" if ordenada else "ul"
    return "<%s>%s</%s>" % (etiqueta, "".join("<li>%s%s</li>" % (inline(t), s) for t, s in items), etiqueta), i


def bloques(texto):
    """HTML de una diapositiva. Los comentarios <!-- ... --> se quitan (sirven para notas al autor)."""
    texto = re.sub(r"<!--.*?-->", "", texto, flags=re.S)
    lineas = texto.split("\n")
    out, i, n = [], 0, len(lineas)
    while i < n:
        l = lineas[i]
        s = l.strip()
        if not s:
            i += 1
        elif s.startswith("```"):
            i += 1
            cod = []
            while i < n and not lineas[i].strip().startswith("```"):
                cod.append(lineas[i])
                i += 1
            i += 1
            if s[3:].strip().lower() == "mermaid":
                try:
                    out.append(diagramas.pintar("\n".join(cod)))
                    continue
                except ValueError as e:
                    AVISOS.append(str(e))
            out.append("<pre><code>%s</code></pre>" % html.escape("\n".join(cod), quote=False))
        elif re.match(r"^#{1,3}\s", s):
            nivel = len(s) - len(s.lstrip("#"))
            out.append("<h%d>%s</h%d>" % (nivel, inline(s[nivel:].strip()), nivel))
            i += 1
        elif re.match(r"^[-*]\s+", s) or re.match(r"^\d+[.)]\s+", s):
            html_lista, i = _lista(lineas, i)
            out.append(html_lista)
        elif s.startswith(">"):
            cita = []
            while i < n and lineas[i].strip().startswith(">"):
                cita.append(lineas[i].strip().lstrip(">").strip())
                i += 1
            out.append("<blockquote>%s</blockquote>" % inline(" ".join(cita)))
        elif s.startswith("|") and i + 1 < n and re.match(r"^\s*\|?\s*:?-{2,}", lineas[i + 1]):
            cab = _celdas(s)
            i += 2
            filas = []
            while i < n and lineas[i].strip().startswith("|"):
                filas.append(_celdas(lineas[i]))
                i += 1
            th = "".join("<th>%s</th>" % inline(c) for c in cab)
            tr = "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c) for c in f) for f in filas)
            out.append("<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>" % (th, tr))
        else:
            par = []
            while i < n and lineas[i].strip() and not re.match(r"^(#{1,3}\s|[-*]\s|\d+[.)]\s|>|```|\|)", lineas[i].strip()):
                par.append(lineas[i].strip())
                i += 1
            if not par:  # línea que parecía otra cosa pero no cierra: se trata como texto para no quedarse en bucle
                par = [s]
                i += 1
            out.append("<p>%s</p>" % inline(" ".join(par)))
    return "\n".join(out)


# ---------------------------------------------------------------- visor
CSS = """
:root{--fondo:#ffffff;--texto:#1b1f24;--suave:#5b6573;--acento:#1f6feb;--caja:#f3f5f8;--linea:#d6dbe3}
@media (prefers-color-scheme:dark){:root{--fondo:#12161c;--texto:#e8ecf2;--suave:#9aa6b6;--acento:#6cb0ff;--caja:#1b222c;--linea:#2e3846}}
*{box-sizing:border-box}html,body{margin:0;height:100%;background:var(--fondo);color:var(--texto);
font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
body{font-size:clamp(16px,2.7vmin,34px);line-height:1.45;overflow:hidden}
.d{position:absolute;inset:0;display:none;flex-direction:column;justify-content:center;padding:6vmin 9vw 9vmin;overflow:auto}
.d.on{display:flex}
h1{font-size:2.1em;margin:0 0 .4em;line-height:1.15}h2{font-size:1.55em;margin:0 0 .5em;line-height:1.2}h3{font-size:1.15em;margin:0 0 .4em;color:var(--suave)}
p,ul,ol,blockquote,table,pre{margin:.35em 0}ul,ol{padding-left:1.3em}li{margin:.28em 0}li>ul,li>ol{margin:.1em 0;font-size:.92em}
code{background:var(--caja);padding:.08em .35em;border-radius:.3em;font-family:ui-monospace,Consolas,monospace;font-size:.88em}
pre{background:var(--caja);padding:.7em 1em;border-radius:.5em;overflow:auto}pre code{background:none;padding:0}
blockquote{border-left:.25em solid var(--acento);padding:.1em 0 .1em .8em;color:var(--suave)}
table{border-collapse:collapse;width:100%;font-size:.9em}th,td{border:1px solid var(--linea);padding:.35em .6em;text-align:left}th{background:var(--caja)}
a{color:var(--acento)}
.barra{position:fixed;left:0;top:0;height:.4vmin;min-height:3px;background:var(--acento);width:0;transition:width .2s}
.pie{position:fixed;left:0;right:0;bottom:0;display:flex;justify-content:space-between;gap:1em;padding:1.2vmin 3vw;font-size:.55em;color:var(--suave)}
.pie a{color:var(--suave)}
body.general{overflow:auto}body.general .d{position:static;display:block;float:left;width:31%;margin:1%;height:34vh;padding:2vmin;
border:1px solid var(--linea);border-radius:.5em;font-size:.38em;overflow:hidden;cursor:pointer}body.general .d.on{border-color:var(--acento)}
body.general .pie,body.general .barra{display:none}
@media print{@page{size:landscape;margin:12mm}body{overflow:visible;font-size:15pt}.d{position:static;display:flex!important;min-height:96vh;
page-break-after:always;break-after:page;padding:0}.barra,.pie{display:none}}
"""

JS = """
(function(){
var d=[].slice.call(document.querySelectorAll('.d')),n=d.length,i=0,b=document.getElementById('barra'),c=document.getElementById('cuenta');
function ir(k){i=Math.max(0,Math.min(n-1,k));d.forEach(function(e,j){e.classList.toggle('on',j===i)});
b.style.width=(n>1?(i/(n-1))*100:100)+'%';c.textContent=(i+1)+' / '+n;
try{history.replaceState(null,'','#'+(i+1))}catch(x){}
if(document.body.classList.contains('general')){d[i].scrollIntoView({block:'nearest'})}}
function general(){document.body.classList.toggle('general')}
document.addEventListener('keydown',function(e){var k=e.key;
if(k==='ArrowRight'||k==='PageDown'||k===' '){e.preventDefault();ir(i+1)}
else if(k==='ArrowLeft'||k==='PageUp'||k==='Backspace'){e.preventDefault();ir(i-1)}
else if(k==='Home'){ir(0)}else if(k==='End'){ir(n-1)}
else if(k==='o'||k==='O'){general()}
else if(k==='Escape'){document.body.classList.remove('general')}});
document.addEventListener('click',function(e){
if(e.target.closest('a'))return;
if(document.body.classList.contains('general')){var s=e.target.closest('.d');if(s){ir(d.indexOf(s));general()}return}
ir(e.clientX>window.innerWidth/2?i+1:i-1)});
var h=parseInt((location.hash||'').slice(1),10);ir(h>0?h-1:0);
})();
"""


def pagina(titulo, diapos_html, lang, parte=None, total=1, nombre_base="", textos_lang=None):
    pie_izq = html.escape(t(lang, "diap_visor_ayuda"))
    nav = ""
    if total > 1:
        piezas = [html.escape(t(lang, "diap_visor_parte", parte, total))]
        if parte > 1:
            piezas.append('<a href="%s">%s</a>' % (html.escape(_nombre_parte(nombre_base, parte - 1)), html.escape(t(lang, "diap_visor_anterior"))))
        if parte < total:
            piezas.append('<a href="%s">%s</a>' % (html.escape(_nombre_parte(nombre_base, parte + 1)), html.escape(t(lang, "diap_visor_siguiente"))))
        nav = " · ".join(piezas)
    secciones = "\n".join('<section class="d">%s</section>' % d for d in diapos_html)
    return (
        '<!doctype html>\n<html lang="%s"><head><meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'; script-src \'unsafe-inline\'; img-src data:">\n'
        "<title>%s</title>\n<style>%s%s</style></head>\n<body>\n"
        '<div class="barra" id="barra"></div>\n%s\n'
        '<div class="pie"><span>%s</span><span>%s</span><span id="cuenta"></span></div>\n'
        "<script>%s</script>\n</body></html>\n"
    ) % (lang, html.escape(titulo), CSS, diagramas.CSS, secciones, pie_izq, nav, JS)


def _nombre_parte(base, k):
    raiz, ext = os.path.splitext(base)
    return "%s-parte-%d%s" % (os.path.basename(raiz), k, ext)


def convertir(ruta_md, salida=None, abrir=True):
    """Escribe el/los .html y devuelve (rutas, n_diapositivas)."""
    del AVISOS[:]
    meta, diapos = separar(leer(ruta_md))
    lang = idioma(meta.get("idioma") or meta.get("language") or None)
    titulo = meta.get("titulo") or meta.get("título") or meta.get("title") or os.path.splitext(os.path.basename(ruta_md))[0]
    if not diapos:
        raise ValueError("sin_diapositivas")
    salida = salida or os.path.splitext(ruta_md)[0] + ".html"
    os.makedirs(os.path.dirname(os.path.abspath(salida)), exist_ok=True)
    _gitignore_local(os.path.dirname(os.path.abspath(salida)))
    trozos = [diapos[k:k + MAX_POR_PARTE] for k in range(0, len(diapos), MAX_POR_PARTE)]
    rutas = []
    for k, trozo in enumerate(trozos, 1):
        destino = salida if len(trozos) == 1 else os.path.join(os.path.dirname(os.path.abspath(salida)), _nombre_parte(salida, k))
        cuerpo = pagina(titulo, [bloques(d) for d in trozo], lang, k, len(trozos), salida)
        with open(destino + ".tmp", "wb") as f:
            f.write(cuerpo.encode("utf-8"))
        os.replace(destino + ".tmp", destino)
        rutas.append(destino)
    if abrir:
        try:
            webbrowser.open("file:///" + rutas[0].replace("\\", "/").lstrip("/"))
        except Exception:
            abrir = False
    return rutas, len(diapos), abrir, lang


def _gitignore_local(carpeta):
    """En `.brain/diapositivas/` los .html se pueden rehacer: un .gitignore local los deja fuera del control de versiones."""
    if os.path.basename(carpeta) == "diapositivas" and os.path.basename(os.path.dirname(carpeta)) == ".brain":
        ruta = os.path.join(carpeta, ".gitignore")
        if not os.path.exists(ruta):
            with open(ruta, "wb") as f:
                f.write(b"*.html\n")


# ---------------------------------------------------------------- buscar documento por nombre
def _norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "", s)


def buscar(nombre, raiz=RAIZ, lang=None):
    """Rutas (relativas a la raíz) de los documentos que coinciden con `nombre`. Un nombre exacto gana a uno parcial."""
    lang = lang or idioma()
    carpetas = [os.path.join(".brain", "biblioteca"), os.path.join(".brain", "specs"), ".brain", "."]
    grupos = {}
    for carpeta in carpetas:
        base = os.path.join(raiz, carpeta)
        if not os.path.isdir(base):
            continue
        for f in sorted(os.listdir(base)):
            if not f.lower().endswith(".md") or not os.path.isfile(os.path.join(base, f)):
                continue
            if f.startswith("_") or f.startswith("PLANTILLA"):
                continue
            es_en = f.lower().endswith(".en.md")
            raiz_nombre = f[:-6] if es_en else f[:-3]
            clave = (carpeta, raiz_nombre)
            grupos.setdefault(clave, {})["en" if es_en else "es"] = os.path.normpath(os.path.join(carpeta, f))
    buscado = _norm(nombre)
    if not buscado:
        return []
    exactos, parciales = [], []
    for (carpeta, raiz_nombre), versiones in sorted(grupos.items()):
        elegido = versiones.get(lang) or versiones.get("es") or versiones.get("en")
        n = _norm(raiz_nombre)
        if n == buscado:
            exactos.append(elegido)
        elif buscado in n:
            parciales.append(elegido)
    return exactos if exactos else parciales


# ---------------------------------------------------------------- comprobar que no se pierde ninguna sección
def secciones(texto):
    res, en_codigo = [], False
    for l in texto.split("\n"):
        if l.strip().startswith("```"):
            en_codigo = not en_codigo
        elif not en_codigo:
            m = re.match(r"^##\s+(.+?)\s*#*\s*$", l)
            if m:
                res.append(m.group(1))
    return res


def faltan(original, diapositivas):
    destino = _norm(diapositivas)
    return [s for s in secciones(original) if _norm(re.sub(r"[`*_]", "", s)) not in destino]


# ---------------------------------------------------------------- línea de comandos
def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    for flujo in (sys.stdout, sys.stderr):
        try:
            flujo.reconfigure(encoding="utf-8")
        except Exception:
            pass
    lang = idioma()
    if not argv or argv[0] in ("-h", "--help"):
        print(t(lang, "diap_uso"))
        return 0 if argv else 1
    if argv[0] == "--buscar":
        if len(argv) < 2:
            print(t(lang, "diap_uso"))
            return 1
        res = buscar(" ".join(argv[1:]))
        if not res:
            print(t(lang, "diap_buscar_ninguno", " ".join(argv[1:])))
            return 2
        if len(res) > 1:
            print(t(lang, "diap_buscar_varios", " ".join(argv[1:])))
            for r in res:
                print(r.replace("\\", "/"))
            return 3
        print(res[0].replace("\\", "/"))
        return 0
    if argv[0] == "--comprobar":
        if len(argv) != 3:
            print(t(lang, "diap_uso"))
            return 1
        for r in argv[1:]:
            if not os.path.isfile(r):
                print(t(lang, "diap_falta_archivo", r))
                return 1
        falta = faltan(leer(argv[1]), leer(argv[2]))
        if falta:
            print(t(lang, "diap_comprobar_falta", len(falta)))
            for s in falta:
                print("- " + s)
            return 1
        print(t(lang, "diap_comprobar_ok", len(secciones(leer(argv[1])))))
        return 0
    abrir = "--no-abrir" not in argv
    salida = None
    resto = []
    k = 0
    while k < len(argv):
        if argv[k] == "--salida" and k + 1 < len(argv):
            salida = argv[k + 1]
            k += 2
            continue
        if argv[k] != "--no-abrir":
            resto.append(argv[k])
        k += 1
    if len(resto) != 1:
        print(t(lang, "diap_uso"))
        return 1
    if not os.path.isfile(resto[0]):
        print(t(lang, "diap_falta_archivo", resto[0]))
        return 1
    try:
        rutas, n, abierto, lang_doc = convertir(resto[0], salida, abrir)
    except ValueError:
        print(t(lang, "diap_sin_diapositivas"))
        return 1
    if len(rutas) == 1:
        print(t(lang, "diap_listo", n, rutas[0]))
    else:
        print(t(lang, "diap_listo_partes", n, len(rutas), rutas[0]))
    for motivo in AVISOS:
        print(t(lang, "diap_diagrama_texto", diagramas.aviso(lang, motivo)))
    print(t(lang, "diap_abierto") if abierto else t(lang, "diap_no_abierto"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
