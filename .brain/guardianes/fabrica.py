#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Guardián de la fábrica de IA (spec 035, fase 2). Sin IA: solo comprobaciones. Solo librería estándar.

Lo usa la directora (o Darwin) entre pasos; no es un hook. Todo cuelga de `.brain/fabrica/`:
  congelar SPEC [--reemplazar]   guarda la huella de la spec aprobada por Darwin (R4)
  sellar-carta [--reemplazar]    guarda la huella de carta.md, que solo escribe Darwin (R2)
  automatico si|no|estado        modo automático (spec 050): interruptor; solo válido con el modo fábrica encendido
  sellar-negocio [--reemplazar]  guarda la huella de negocio.md (modelo de negocio de Darwin; spec 050, fase 2)
  veredicto ARCHIVO [--spec S]   valida el veredicto del revisor de spec: formato y que cada hallazgo cite una frase real
  vueltas rechazada|aprobada|reiniciar|estado
                                 cuenta las vueltas de revisión de la spec (máximo 3; a la tercera rechazada, parar y preguntar)
  verificar                      falla si la spec congelada o la carta cambiaron
  arrancar                       en modo automático bloquea si falta el criterio de «esperado» (esperado.md) o se está en main (spec 050, fase 3); `foto` lo llama sola
  foto [--repo R] --encargo N    foto del worktree antes de que trabaje la ejecutora
  alcance ENCARGO.md --encargo N [--repo R]
                                 el encargo tiene requisito en la spec congelada y la ejecutora solo tocó lo permitido (R6, R7)
  gasto --encargo N --tokens T --papel P [--fallo]
                                 anota el gasto de un papel (y si el intento falló)
  topes [--encargo N] [--libre-semanal PCT]
                                 compara el gasto con los topes de la carta (encargo, misión, freno semanal, dos fallos seguidos)
Código de salida: 0 = en regla, 1 = incumple (parar y avisar a Darwin), 2 = uso incorrecto."""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from textos import t  # noqa: E402  (spec 024: mensajes en es/en)

# Topes aprobados por Darwin el 2026-11-10 (spec 035, sección 7); la carta los puede cambiar.
TOPES_POR_DEFECTO = {"tope_encargo_tokens": 400000, "tope_mision_encargos": 10, "tope_mision_tokens": 1000000,
                     "libre_semanal_minimo": 50, "fallos_seguidos_max": 2}
# Siempre permitido a la ejecutora: su nota, y el estado interno de este guardián.
SIEMPRE_PERMITIDO = (".brain/notas-chats/", ".brain/fabrica/estado/")


def cargar_cfg():
    try:
        with open(os.path.join(AQUI, "guardianes.json"), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def huella(ruta) -> str:
    return hashlib.sha256(Path(ruta).read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def _json(ruta, defecto):
    try:
        return json.loads(Path(ruta).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return defecto


def _guardar(ruta, datos):
    Path(ruta).parent.mkdir(parents=True, exist_ok=True)
    Path(ruta).write_text(json.dumps(datos, indent=1, ensure_ascii=False), encoding="utf-8")


class Fabrica:
    def __init__(self, raiz, cfg=None):
        self.raiz = Path(raiz)
        self.cfg = cfg if cfg is not None else cargar_cfg()
        self.dir = self.raiz / ".brain" / "fabrica"
        self.estado = self.dir / "estado"
        self.carta = self.dir / "carta.md"
        self.negocio = self.dir / "negocio.md"

    def t(self, clave, *args):
        return t(self.cfg, clave, *args)

    # --- modo fábrica: interruptor persistente por proyecto (spec 040) --------------------------
    def modo(self, orden):
        orden = (orden or "estado").strip().lower()
        ruta = str(self.raiz / ".brain" / "guardianes" / "guardianes.json")
        cfg = _json(ruta, {})
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        if orden in ("si", "sí", "on", "yes", "activar", "activa"):
            cfg["modo_fabrica"] = True
            self.estado.mkdir(parents=True, exist_ok=True)
            (self.dir / "encargos").mkdir(parents=True, exist_ok=True)
        elif orden in ("no", "off", "desactivar", "desactiva", "normal"):
            cfg["modo_fabrica"] = False
            cfg["fabrica_automatica"] = False  # spec 050: apagar la fábrica apaga el automático al instante
        elif orden != "estado":
            return 1, [self.t("fabrica_modo_uso")]
        if orden != "estado":
            with open(ruta + ".tmp", "w", encoding="utf-8", newline="\n") as f:
                f.write(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n")
            os.replace(ruta + ".tmp", ruta)
        activo = bool(cfg.get("modo_fabrica"))
        lineas = [self.t("fabrica_modo_si" if activo else "fabrica_modo_no")]
        if activo:
            lineas.append(self.t("fabrica_modo_carta_ok" if self.carta.is_file() else "fabrica_modo_falta"))
        return 0, lineas

    # --- modo automático (spec 050, fase 1): interruptor, solo válido con modo_fabrica -----------
    def automatico(self, orden):
        orden = (orden or "estado").strip().lower()
        ruta = str(self.raiz / ".brain" / "guardianes" / "guardianes.json")
        cfg = _json(ruta, {})
        if orden in ("si", "sí", "on", "yes", "activar", "activa"):
            if not cfg.get("modo_fabrica"):
                return 1, [self.t("fabrica_auto_sin_modo")]
            cfg["fabrica_automatica"] = True
        elif orden in ("no", "off", "desactivar", "desactiva", "normal"):
            cfg["fabrica_automatica"] = False
        elif orden != "estado":
            return 1, [self.t("fabrica_auto_uso")]
        if orden != "estado":
            os.makedirs(os.path.dirname(ruta), exist_ok=True)
            with open(ruta + ".tmp", "w", encoding="utf-8", newline="\n") as f:
                f.write(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n")
            os.replace(ruta + ".tmp", ruta)
        activo = bool(cfg.get("fabrica_automatica")) and bool(cfg.get("modo_fabrica"))
        lineas = [self.t("fabrica_auto_si" if activo else "fabrica_auto_no")]
        if activo:
            h = self._huellas()
            lineas.append(self.t("fabrica_auto_carta_ok" if "carta" in h else "fabrica_auto_carta_falta"))
            lineas += self._criterio_lineas()
            lineas.append(self._rama_linea())
        return 0, lineas

    # --- criterio de «esperado» y rama de trabajo (spec 050, fase 3) -------------------------------
    ESPERADO_CAMPOS = (("Cómo se sabe que salió bien", "How we know it went well"),
                       ("Casos malos", "Bad cases"))

    def criterio_faltante(self):
        """None = criterio listo. Si no: 'falta' (no existe o vacío) o la lista de campos obligatorios sin rellenar.
        Un valor que sigue siendo la plantilla (<…>) o muy corto (<8 letras) cuenta como vacío."""
        ruta = self.dir / "esperado.md"
        try:
            texto = ruta.read_text(encoding="utf-8-sig")
        except (OSError, ValueError):
            return "falta"
        if not texto.strip():
            return "falta"
        faltan = []
        for es, en in self.ESPERADO_CAMPOS:
            ok = False
            for et in (es, en):
                m = re.search(r"^[-*]\s*" + re.escape(et) + r"[^:\n]*:\s*(.+)$", texto, re.M | re.I)
                if m and not m.group(1).strip().startswith("<") and len(m.group(1).strip()) >= 8:
                    ok = True
            if not ok:
                faltan.append(es if (self.cfg or {}).get("idioma", "es") != "en" else en)
        return ", ".join(faltan) if faltan else None

    def _criterio_lineas(self):
        falta = self.criterio_faltante()
        if falta is None:
            return [self.t("fabrica_auto_criterio_ok")]
        if falta == "falta":
            return [self.t("fabrica_auto_criterio_falta")]
        return [self.t("fabrica_auto_criterio_incompleto", falta)]

    def rama_actual(self):
        try:
            return self._git(self.raiz, "rev-parse", "--abbrev-ref", "HEAD").strip()
        except (RuntimeError, OSError):
            return ""

    def _rama_linea(self):
        rama = self.rama_actual()
        if not rama or rama in ("main", "master", "HEAD"):  # HEAD = cabeza suelta, sin rama
            return self.t("fabrica_auto_rama_falta")
        return self.t("fabrica_auto_rama_ok", rama)

    def _auto_activa(self):
        cfg = _json(self.raiz / ".brain" / "guardianes" / "guardianes.json", {})
        return isinstance(cfg, dict) and cfg.get("fabrica_automatica") is True and cfg.get("modo_fabrica") is True

    def arrancar(self):
        """Puerta de arranque de un encargo. Fuera del modo automático no aplica (0). En automático bloquea (1)
        si falta el criterio de «esperado» o si se está en main/master/cabeza suelta."""
        if not self._auto_activa():
            return 0, [self.t("fabrica_arrancar_no_aplica")]
        bloqueos = []
        if self.criterio_faltante() is not None:
            bloqueos += self._criterio_lineas()
        rama = self._rama_linea()
        if rama == self.t("fabrica_auto_rama_falta"):
            bloqueos.append(rama)
        if bloqueos:
            return 1, bloqueos + [self.t("fabrica_arrancar_bloqueado")]
        return 0, [self.t("fabrica_arrancar_ok", self.rama_actual())]

    # --- huellas: spec congelada y carta sellada -------------------------------------------------
    def _huellas(self):
        return _json(self.estado / "huellas.json", {})

    def congelar(self, spec, reemplazar=False):
        spec = Path(spec)
        if not spec.is_file():
            return 1, [self.t("fabrica_no_existe", str(spec))]
        h = self._huellas()
        if "spec" in h and not reemplazar:
            return 1, [self.t("fabrica_ya_congelada")]
        rel = os.path.relpath(spec.resolve(), self.raiz.resolve()).replace("\\", "/")
        h["spec"] = {"ruta": rel, "sha256": huella(spec)}
        _guardar(self.estado / "huellas.json", h)
        return 0, [self.t("fabrica_congelada", rel)]

    def sellar_carta(self, reemplazar=False):
        if not self.carta.is_file():
            return 1, [self.t("fabrica_no_existe", str(self.carta))]
        h = self._huellas()
        if "carta" in h and not reemplazar:
            return 1, [self.t("fabrica_carta_ya_sellada")]
        h["carta"] = {"sha256": huella(self.carta)}
        _guardar(self.estado / "huellas.json", h)
        return 0, [self.t("fabrica_carta_sellada")]

    # --- revisor de spec (spec 050, fase 2) --------------------------------------------------------
    def sellar_negocio(self, reemplazar=False):
        """Guarda la huella de negocio.md (modelo de negocio, lo escribe Darwin; la IA no lo edita)."""
        if not self.negocio.is_file():
            return 1, [self.t("fabrica_no_existe", str(self.negocio))]
        if not self.negocio.read_bytes().strip():
            return 1, [self.t("fabrica_negocio_vacio")]
        h = self._huellas()
        if "negocio" in h and not reemplazar:
            return 1, [self.t("fabrica_negocio_ya_sellado")]
        h["negocio"] = {"sha256": huella(self.negocio)}
        _guardar(self.estado / "huellas.json", h)
        return 0, [self.t("fabrica_negocio_sellado")]

    @staticmethod
    def _norm(s):
        s = re.sub(r"[*_`]", "", s)
        return re.sub(r"\s+", " ", s).strip().lower()

    @staticmethod
    def _leer(ruta):
        """Texto normalizado de un archivo, o None si no existe o no es UTF-8 (no se cae)."""
        try:
            return Fabrica._norm(Path(ruta).read_text(encoding="utf-8-sig"))
        except (OSError, ValueError):
            return None

    def _corpus_citas(self, spec):
        """Dónde vale una cita: negocio, la spec revisada y las specs/decisiones anteriores (por separado)."""
        previas = []
        for carpeta in ("specs", "decisions"):
            d = self.raiz / ".brain" / carpeta
            for r in (sorted(d.glob("*.md")) if d.is_dir() else []):
                if spec and Path(r).resolve() == Path(spec).resolve():
                    continue
                previas.append(self._leer(r) or "")
        return {"negocio": self._leer(self.negocio), "spec": self._leer(spec) if spec else None,
                "previas": "\n".join(previas)}

    def veredicto(self, ruta, spec=None):
        """Valida un veredicto del revisor de spec: formato completo, y que todo hallazgo cite frases que existen
        en la fuente que le toca. Un rechazo sin cita válida no cuenta. 0 = veredicto válido, 1 = inválido."""
        try:
            texto = Path(ruta).read_text(encoding="utf-8-sig")
        except (OSError, ValueError):
            return 1, [self.t("fabrica_vered_ilegible", str(ruta))]
        h = self._huellas()
        if not self.negocio.is_file() or "negocio" not in h or huella(self.negocio) != h["negocio"]["sha256"]:
            return 1, [self.t("fabrica_vered_sin_negocio")]
        m = re.search(r"^\W*(?:veredicto|verdict)\s*:\s*\W*(aprobada|rechazada|approved|rejected)\b", texto, re.M | re.I)
        if not m:
            return 1, [self.t("fabrica_vered_sin_linea")]
        aprobada = m.group(1).lower() in ("aprobada", "approved")
        corpus = self._corpus_citas(spec)
        if corpus["negocio"] is None or (spec and corpus["spec"] is None):
            return 1, [self.t("fabrica_vered_ilegible", str(spec or self.negocio))]
        # Fuentes válidas por sección: (a) el negocio; (b) la spec; (c) negocio o spec; (d) cualquiera.
        fuentes = {"a": ("negocio",), "b": ("spec",), "c": ("negocio", "spec"), "d": ("negocio", "spec", "previas")}
        secciones, vistas, sueltos = {}, [], []
        actual = None
        for linea in texto.splitlines():
            if re.match(r"^\s*(#{1,6}\s|\*\*|__)", linea) and re.search(r"\(([a-d])\)", linea, re.I):
                actual = re.search(r"\(([a-d])\)", linea, re.I).group(1).lower()
                vistas.append(actual)
                continue
            if re.match(r"^\s*(#{1,6}\s)", linea):
                actual = None
                continue
            mi = re.match(r"^\s*(?:[-*]|\d+[.)])\s+(\S.*)$", linea)
            if not mi:
                continue
            item = mi.group(1).strip()
            if re.fullmatch(r"(ninguno|ninguna|none|n/a|-|—)\.?", self._norm(item)):
                continue
            if actual:
                secciones.setdefault(actual, []).append(item)
            elif re.search(r"[«“\"]", item):
                sueltos.append(item[:80])
        faltan = [x for x in "abcd" if x not in vistas]
        if faltan or len(vistas) != len(set(vistas)):
            return 1, [self.t("fabrica_vered_secciones", ", ".join("(%s)" % x for x in faltan) or "-")]
        validos, sin_cita, citas_falsas, grandes = {}, [], [], 0
        for letra, items in secciones.items():
            for item in items:
                es_grande = letra == "c" and re.search(r"\[(grande|big)\]", item, re.I)
                if es_grande:
                    grandes += 1  # sube a Darwin aunque su cita no valga
                citas = [next(x for x in grupo if x) for grupo in re.findall(r"«([^»]+)»|\"([^\"]+)\"|“([^”]+)”", item)]
                citas = [c for c in citas if len(self._norm(c)) >= 12]
                if not citas:
                    sin_cita.append(item[:80])
                    continue
                en = lambda c, fs: any(corpus[f] and self._norm(c) in corpus[f] for f in fs)  # noqa: E731
                # todas las citas existen en algún sitio, y al menos una sale de la fuente que le toca a la sección
                if not (all(en(c, ("negocio", "spec", "previas")) for c in citas) and any(en(c, fuentes[letra]) for c in citas)):
                    citas_falsas.append(item[:80])
                    continue
                validos.setdefault(letra, []).append(item)
        avisos = [self.t("fabrica_vered_sin_cita", i) for i in sin_cita]
        avisos += [self.t("fabrica_vered_cita_falsa", i) for i in citas_falsas]
        avisos += [self.t("fabrica_vered_suelto", i) for i in sueltos]
        if sueltos:
            return 1, avisos
        total = sum(len(v) for v in validos.values())
        if not aprobada and total == 0:
            return 1, avisos + [self.t("fabrica_vered_rechazo_vacio")]
        if aprobada and any(validos.get(x) for x in "abd"):
            return 1, avisos + [self.t("fabrica_vered_incoherente")]
        res = [self.t("fabrica_vered_aprobada" if aprobada else "fabrica_vered_rechazada", total)]
        if grandes:
            res.append(self.t("fabrica_vered_huecos_grandes", grandes))
        return 0, avisos + res

    def vueltas(self, resultado):
        """Cuenta las vueltas de revisión de la spec (máximo 3). resultado: rechazada | aprobada | reiniciar | estado."""
        ruta = self.estado / "revision_spec.json"
        d = _json(ruta, {"vueltas": 0})
        try:
            n = max(0, int(d.get("vueltas", 0))) if isinstance(d, dict) else 0
        except (TypeError, ValueError):
            n = 0
        tope = 3
        if resultado in ("aprobada", "approved", "reiniciar", "reset"):
            n = 0
            _guardar(ruta, {"vueltas": 0})
        elif resultado in ("rechazada", "rejected"):
            n += 1
            _guardar(ruta, {"vueltas": n})
        elif resultado != "estado":
            return 1, [self.t("fabrica_vueltas_uso")]
        if n >= tope:
            return 1, [self.t("fabrica_vueltas_tope", n, tope)]
        return 0, [self.t("fabrica_vueltas_ok", n, tope)]

    def verificar(self):
        h = self._huellas()
        avisos = []
        if "negocio" in h and (not self.negocio.is_file() or huella(self.negocio) != h["negocio"]["sha256"]):
            avisos.append(self.t("fabrica_negocio_cambio"))
        if "spec" not in h:
            avisos.append(self.t("fabrica_sin_spec"))
        else:
            ruta = self.raiz / h["spec"]["ruta"]
            if not ruta.is_file() or huella(ruta) != h["spec"]["sha256"]:
                avisos.append(self.t("fabrica_spec_cambio", h["spec"]["ruta"]))
        if "carta" in h and (not self.carta.is_file() or huella(self.carta) != h["carta"]["sha256"]):
            avisos.append(self.t("fabrica_carta_cambio"))
        return (1 if avisos else 0), (avisos or [self.t("fabrica_verificada")])

    # --- encargo y alcance ----------------------------------------------------------------------
    @staticmethod
    def leer_encargo(ruta):
        """(requisito, [permitidos]) de un encargo. Acepta las etiquetas en español y en inglés; un valor que sigue
        siendo la plantilla (<…>) cuenta como vacío."""
        texto = Path(ruta).read_text(encoding="utf-8")

        def campo(*etiquetas):
            for et in etiquetas:
                m = re.search(r"^[-*]\s*" + re.escape(et) + r"\s*:\s*(.+)$", texto, re.M | re.I)
                if m and not m.group(1).strip().startswith("<"):
                    return m.group(1).strip()
            return ""
        req = campo("Requisito que cumple", "Requirement it meets")
        perm = campo("Archivos permitidos", "Allowed files")
        trozos = re.split(r"\s*[,;]\s*", perm) if re.search(r"[,;]", perm) else perm.split()
        lista = [p.strip(" `*") for p in trozos if p.strip(" `*")]
        return req, [p.replace("\\", "/") for p in lista]

    def comprobar_encargo(self, ruta):
        """Un encargo sin requisito aprobado y congelado se rechaza solo (R6)."""
        try:
            req, permitidos = self.leer_encargo(ruta)
        except OSError:
            return [self.t("fabrica_encargo_no_existe", str(ruta))], "", []
        if not req:
            return [self.t("fabrica_encargo_sin_requisito")], req, permitidos
        h = self._huellas()
        if "spec" not in h:
            return [self.t("fabrica_sin_spec")], req, permitidos
        ids = re.findall(r"\bR\d+\b", req)
        spec = (self.raiz / h["spec"]["ruta"]).read_text(encoding="utf-8") if (self.raiz / h["spec"]["ruta"]).is_file() else ""
        if not ids or any(not re.search(r"\b" + i + r"\b", spec) for i in ids):
            return [self.t("fabrica_requisito_no_esta", req)], req, permitidos
        if not permitidos:
            return [self.t("fabrica_encargo_sin_archivos")], req, permitidos
        return [], req, permitidos

    @staticmethod
    def _git(repo, *args):
        r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
        if r.returncode != 0:
            raise RuntimeError(r.stderr.strip())
        return r.stdout

    def estado_repo(self, repo):
        repo = Path(repo)
        nombres = set(self._git(repo, "ls-files", "-m", "-d", "-o", "--exclude-standard").split("\n")) - {""}
        return {n: (huella(repo / n) if (repo / n).is_file() else "borrado") for n in sorted(nombres)}

    def foto(self, repo, encargo):
        codigo, lineas = self.arrancar()  # spec 050, fase 3: en modo automático la foto es el arranque del encargo
        if codigo:
            return codigo, lineas
        _guardar(self.estado / f"{encargo}.foto.json",
                 {"cabeza": self._git(repo, "rev-parse", "HEAD").strip(), "archivos": self.estado_repo(repo)})
        return 0, [self.t("fabrica_foto", str(encargo))]

    @staticmethod
    def permitido(nombre, permitidos):
        nombre = nombre.replace("\\", "/")
        return any(nombre.startswith(p) if p.endswith("/") else nombre == p for p in permitidos)

    def alcance(self, ruta_encargo, repo, encargo):
        avisos, _req, permitidos = self.comprobar_encargo(ruta_encargo)
        v, av = self.verificar()
        if v:
            avisos += av
        if avisos:
            return 1, avisos + [self.t("fabrica_rechazado_sin_revision")]
        foto = _json(self.estado / f"{encargo}.foto.json", None)
        if foto is None:
            return 1, [self.t("fabrica_sin_foto", str(encargo))]
        try:
            if self._git(repo, "rev-parse", "HEAD").strip() != foto["cabeza"]:
                return 1, [self.t("fabrica_commit_colado")]
            ahora = self.estado_repo(repo)
        except RuntimeError as e:
            return 1, [self.t("fabrica_git_fallo", str(e))]
        antes = foto["archivos"]
        cambiados = sorted(n for n in set(ahora) | set(antes) if ahora.get(n) != antes.get(n))
        fuera = [n for n in cambiados if not self.permitido(n, list(permitidos) + list(SIEMPRE_PERMITIDO))]
        if fuera:
            return 1, [self.t("fabrica_fuera_de_alcance", len(fuera), ", ".join(fuera))]
        return 0, [self.t("fabrica_dentro", len(cambiados))]

    # --- gasto, topes y parada --------------------------------------------------------------------
    def _gasto(self):
        return _json(self.estado / "gasto.json", [])

    def gasto(self, encargo, tokens, papel, fallo=False):
        g = self._gasto()
        g.append({"encargo": str(encargo), "tokens": int(tokens), "papel": papel, "fallo": bool(fallo)})
        _guardar(self.estado / "gasto.json", g)
        return 0, [self.t("fabrica_gasto_anotado", papel, int(tokens), str(encargo))]

    def topes_carta(self):
        """Los topes numéricos de carta.md (líneas `- clave: número`); lo que falte usa el valor aprobado."""
        topes = dict(TOPES_POR_DEFECTO)
        if self.carta.is_file():
            texto = self.carta.read_text(encoding="utf-8")
            for clave in topes:
                m = re.search(r"^[-*]\s*" + clave + r"\s*:\s*(\d+)", texto, re.M)
                if m:
                    topes[clave] = int(m.group(1))
        return topes

    def topes(self, encargo=None, libre_semanal=None):
        tp_ = self.topes_carta()
        g = self._gasto()
        avisos = []
        total = sum(x["tokens"] for x in g)
        if total > tp_["tope_mision_tokens"]:
            avisos.append(self.t("fabrica_tope_mision_tokens", total, tp_["tope_mision_tokens"]))
        n_enc = len({x["encargo"] for x in g})
        if n_enc > tp_["tope_mision_encargos"]:
            avisos.append(self.t("fabrica_tope_mision_encargos", n_enc, tp_["tope_mision_encargos"]))
        if encargo is not None:
            propios = [x for x in g if x["encargo"] == str(encargo)]
            gastado = sum(x["tokens"] for x in propios)
            if gastado >= tp_["tope_encargo_tokens"]:
                avisos.append(self.t("fabrica_tope_encargo", str(encargo), gastado, tp_["tope_encargo_tokens"]))
            seguidos = 0
            for x in reversed(propios):
                if not x["fallo"]:
                    break
                seguidos += 1
            if seguidos >= tp_["fallos_seguidos_max"]:
                avisos.append(self.t("fabrica_dos_fallos", str(encargo), seguidos))
        if libre_semanal is not None and libre_semanal < tp_["libre_semanal_minimo"]:
            avisos.append(self.t("fabrica_freno_semanal", libre_semanal, tp_["libre_semanal_minimo"]))
        if avisos:
            return 1, avisos + [self.t("fabrica_parar")]
        return 0, [self.t("fabrica_topes_ok", total, n_enc)]


def main(argv=None):
    for s in (sys.stdout, sys.stderr):  # consolas de Windows (cp1252) no aguantan emojis ni acentos
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:
            pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raiz", default=str(Path(AQUI).parents[1]), help="raíz del proyecto (por defecto, la de este guardián)")
    sub = ap.add_subparsers(dest="orden", required=True)
    s = sub.add_parser("congelar"); s.add_argument("spec"); s.add_argument("--reemplazar", action="store_true")
    s = sub.add_parser("sellar-carta"); s.add_argument("--reemplazar", action="store_true")
    sub.add_parser("verificar")
    sub.add_parser("arrancar")
    s = sub.add_parser("modo"); s.add_argument("palabra", nargs="?", default="estado")
    s = sub.add_parser("automatico"); s.add_argument("palabra", nargs="?", default="estado")
    s = sub.add_parser("sellar-negocio"); s.add_argument("--reemplazar", action="store_true")
    s = sub.add_parser("veredicto"); s.add_argument("archivo"); s.add_argument("--spec", default=None)
    s = sub.add_parser("vueltas"); s.add_argument("resultado", nargs="?", default="estado")
    s = sub.add_parser("foto"); s.add_argument("--repo", default=None); s.add_argument("--encargo", required=True)
    s = sub.add_parser("alcance"); s.add_argument("encargo_md"); s.add_argument("--repo", default=None); s.add_argument("--encargo", required=True)
    s = sub.add_parser("gasto"); s.add_argument("--encargo", required=True); s.add_argument("--tokens", type=int, required=True)
    s.add_argument("--papel", required=True); s.add_argument("--fallo", action="store_true")
    s = sub.add_parser("topes"); s.add_argument("--encargo", default=None); s.add_argument("--libre-semanal", type=float, default=None)
    a = ap.parse_args(argv)

    f = Fabrica(a.raiz)
    repo = getattr(a, "repo", None) or a.raiz
    if a.orden == "congelar":
        codigo, lineas = f.congelar(a.spec, a.reemplazar)
    elif a.orden == "sellar-carta":
        codigo, lineas = f.sellar_carta(a.reemplazar)
    elif a.orden == "modo":
        codigo, lineas = f.modo(a.palabra)
    elif a.orden == "automatico":
        codigo, lineas = f.automatico(a.palabra)
    elif a.orden == "sellar-negocio":
        codigo, lineas = f.sellar_negocio(a.reemplazar)
    elif a.orden == "veredicto":
        codigo, lineas = f.veredicto(a.archivo, a.spec)
    elif a.orden == "vueltas":
        codigo, lineas = f.vueltas(a.resultado)
    elif a.orden == "verificar":
        codigo, lineas = f.verificar()
    elif a.orden == "arrancar":
        codigo, lineas = f.arrancar()
    elif a.orden == "foto":
        codigo, lineas = f.foto(repo, a.encargo)
    elif a.orden == "alcance":
        codigo, lineas = f.alcance(a.encargo_md, repo, a.encargo)
    elif a.orden == "gasto":
        codigo, lineas = f.gasto(a.encargo, a.tokens, a.papel, a.fallo)
    else:
        codigo, lineas = f.topes(a.encargo, a.libre_semanal)
    for linea in lineas:
        print(linea)
    return codigo


if __name__ == "__main__":
    sys.exit(main())
