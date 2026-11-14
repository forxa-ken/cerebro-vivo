# -*- coding: utf-8 -*-
"""Spec 045: `/diapositivas` (diapositivas.py): conversión de .md a .html autocontenido, búsqueda por nombre y comprobación de secciones."""
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def _es_repo_arnes():
    """Solo el repo del arnés (con manifiesto.json) exige las ediciones .en.md; un proyecto en español no las recibe."""
    return os.path.isfile(os.path.join(RAIZ, "manifiesto.json"))

SCRIPT = os.path.join(RAIZ, ".brain", "guardianes", "diapositivas.py")


def cargar():
    sys.path.insert(0, os.path.dirname(SCRIPT))
    e = importlib.util.spec_from_file_location("diapositivas_t", SCRIPT)
    m = importlib.util.module_from_spec(e)
    e.loader.exec_module(m)
    return m


d = cargar()


def escribir(base, rel, texto):
    ruta = os.path.join(base, *rel.split("/"))
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        f.write(texto)
    return ruta


class Parser(unittest.TestCase):
    def test_separa_por_linea_de_tres_guiones_y_lee_la_cabecera(self):
        meta, diapos = d.separar("---\ntitulo: Hola\nidioma: en\n---\n# Uno\n\n---\n\n## Dos\n- a\n---\n\n")
        self.assertEqual(meta["titulo"], "Hola")
        self.assertEqual(meta["idioma"], "en")
        self.assertEqual(len(diapos), 2)

    def test_un_guion_inicial_sin_cabecera_no_crea_diapositiva_vacia(self):
        meta, diapos = d.separar("---\n# Uno\n---\n# Dos\n")
        self.assertEqual(meta, {})
        self.assertEqual(len(diapos), 2)

    def test_tres_guiones_dentro_de_un_bloque_de_codigo_no_cortan(self):
        _, diapos = d.separar("# A\n```\n---\n```\n---\n# B")
        self.assertEqual(len(diapos), 2)

    def test_titulos_listas_negrita_codigo_y_tablas(self):
        h = d.bloques("# T\n## S\n- uno **fuerte**\n- dos `x`\n1. a\n2. b\n\n| a | b |\n|---|---|\n| 1 | 2 |\n\n> cita")
        for esperado in ("<h1>T</h1>", "<h2>S</h2>", "<strong>fuerte</strong>", "<code>x</code>", "<ol>", "<table>", "<th>a</th>",
                         "<td>2</td>", "<blockquote>cita</blockquote>"):
            self.assertIn(esperado, h)

    def test_subvinetas_por_sangria(self):
        h = d.bloques("- a\n  - a1\n  - a2\n    - a2x\n- b")
        self.assertEqual(h, "<ul><li>a<ul><li>a1</li><li>a2<ul><li>a2x</li></ul></li></ul></li><li>b</li></ul>")

    def test_lista_plana_y_cambio_de_tipo_siguen_igual(self):
        self.assertEqual(d.bloques("- a\n- b"), "<ul><li>a</li><li>b</li></ul>")
        self.assertEqual(d.bloques("- a\n1. b"), "<ul><li>a</li></ul>\n<ol><li>b</li></ol>")

    def test_sangria_suelta_o_muy_profunda_no_rompe(self):
        h = d.bloques("  - a\n- b\n          - c")
        self.assertIn("<li>a</li>", h)
        self.assertIn("c", h)

    def test_el_html_del_md_se_escapa(self):
        h = d.bloques("# <script>alert(1)</script>\n\n<img src=x onerror=alert(1)>\n\n```\n<b>x</b>\n```")
        self.assertNotIn("<script>", h)
        self.assertNotIn("<img", h)
        self.assertIn("&lt;script&gt;", h)
        self.assertIn("&lt;b&gt;x&lt;/b&gt;", h)

    def test_solo_enlaces_http_https_y_relativos(self):
        h = d.bloques("[bien](https://a.org/x) [rel](doc.md) [mal](javascript:alert(1)) [mal2](data:text/html,x) [mal3](//otro.com)")
        self.assertIn('href="https://a.org/x"', h)
        self.assertIn('href="doc.md"', h)
        self.assertNotIn("javascript:", h)
        self.assertNotIn("data:", h)
        self.assertNotIn("//otro.com", h)

    def test_los_comentarios_html_se_quitan(self):
        self.assertNotIn("nota", d.bloques("# A\n\n<!-- nota\npara el autor -->"))


class Conversion(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_hay_tantas_diapositivas_como_separadores_y_nada_externo(self):
        md = escribir(self.tmp, "x.md", "---\ntitulo: Prueba\nidioma: es\n---\n# A\n---\n## B\n- uno\n---\n## C\n")
        rutas, n, _, lang = d.convertir(md, abrir=False)
        self.assertEqual(n, 3)
        self.assertEqual(lang, "es")
        with open(rutas[0], encoding="utf-8") as f:
            h = f.read()
        self.assertEqual(h.count('<section class="d">'), 3)
        self.assertIn("Content-Security-Policy", h)
        self.assertIn("default-src 'none'", h)
        self.assertNotRegex(h, r'(src|href)=["\']https?://')
        self.assertNotIn("<link", h)

    def test_idioma_del_visor_sale_de_la_cabecera(self):
        md = escribir(self.tmp, "x.md", "---\ntitle: T\nlanguage: en\n---\n# A\n")
        rutas, _, _, lang = d.convertir(md, abrir=False)
        self.assertEqual(lang, "en")
        with open(rutas[0], encoding="utf-8") as f:
            self.assertIn('lang="en"', f.read())
            f.seek(0)
            self.assertIn("save as PDF", f.read())

    def test_sin_diapositivas_da_error(self):
        md = escribir(self.tmp, "vacio.md", "\n\n")
        with self.assertRaises(ValueError):
            d.convertir(md, abrir=False)

    def test_mas_de_20_se_parte_en_partes_enlazadas(self):
        md = escribir(self.tmp, "largo.md", "\n---\n".join("## S%d\n- x" % k for k in range(45)))
        rutas, n, _, _ = d.convertir(md, abrir=False)
        self.assertEqual(n, 45)
        self.assertEqual(len(rutas), 3)
        with open(rutas[0], encoding="utf-8") as f:
            h = f.read()
        self.assertIn("largo-parte-2.html", h)
        with open(rutas[2], encoding="utf-8") as f:
            self.assertIn("largo-parte-2.html", f.read())

    def test_en_brain_diapositivas_deja_un_gitignore_local_para_los_html(self):
        md = escribir(self.tmp, ".brain/diapositivas/2026-01-01-x.md", "# A\n")
        d.convertir(md, abrir=False)
        with open(os.path.join(self.tmp, ".brain", "diapositivas", ".gitignore")) as f:
            self.assertEqual(f.read().strip(), "*.html")

    def test_no_abrir_no_llama_al_navegador(self):
        md = escribir(self.tmp, "x.md", "# A\n")
        llamadas = []
        original = d.webbrowser.open
        d.webbrowser.open = lambda *a, **k: llamadas.append(a)
        try:
            d.convertir(md, abrir=False)
            self.assertEqual(llamadas, [])
            d.convertir(md, abrir=True)
            self.assertEqual(len(llamadas), 1)
        finally:
            d.webbrowser.open = original

    def test_salida_utf8_en_consola(self):
        md = escribir(self.tmp, "x.md", "# Acción ñ → ✓\n")
        r = subprocess.run([sys.executable, "-I", SCRIPT, md, "--no-abrir"], capture_output=True, env={**os.environ, "PYTHONIOENCODING": "cp1252"})
        self.assertEqual(r.returncode, 0, r.stderr.decode("utf-8", "replace"))
        self.assertIn("Listo", r.stdout.decode("utf-8"))


class Busqueda(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        for rel in (".brain/biblioteca/CARTA_EJECUTORA.md", ".brain/biblioteca/CARTA_META_ARNES.md",
                    ".brain/biblioteca/CEREBRO_VIVO.md", ".brain/biblioteca/CEREBRO_VIVO.en.md",
                    ".brain/biblioteca/PLANTILLA_TRASPASO.md", ".brain/specs/045-diapositivas-para-humanos.md",
                    ".brain/archive/informe-viejo.md", "README.md"):
            escribir(self.tmp, rel, "# x\n")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_un_nombre_con_dos_coincidencias_las_devuelve_todas(self):
        self.assertEqual(len(d.buscar("carta", self.tmp, "es")), 2)

    def test_un_nombre_unico_da_un_solo_archivo_sin_importar_tildes_ni_separadores(self):
        self.assertEqual(d.buscar("carta meta-arnés", self.tmp, "es"), [os.path.normpath(".brain/biblioteca/CARTA_META_ARNES.md")])

    def test_el_nombre_exacto_gana_al_parcial(self):
        self.assertEqual(len(d.buscar("cerebro vivo", self.tmp, "es")), 1)

    def test_elige_la_edicion_en_el_idioma_del_proyecto(self):
        self.assertTrue(d.buscar("cerebro vivo", self.tmp, "en")[0].endswith("CEREBRO_VIVO.en.md"))
        self.assertTrue(d.buscar("cerebro vivo", self.tmp, "es")[0].endswith("CEREBRO_VIVO.md"))

    def test_no_busca_en_archive_ni_en_plantillas_y_sin_coincidencia_no_inventa(self):
        self.assertEqual(d.buscar("informe viejo", self.tmp, "es"), [])
        self.assertEqual(d.buscar("traspaso", self.tmp, "es"), [])
        self.assertEqual(d.buscar("zzzz", self.tmp, "es"), [])

    def test_codigos_de_salida_de_la_linea_de_comandos(self):
        def correr(*a):
            return subprocess.run([sys.executable, "-I", SCRIPT, *a], capture_output=True, cwd=self.tmp).returncode
        self.assertEqual(correr("--buscar", "zzzz-que-no-existe-jamas"), 2)


class Comprobar(unittest.TestCase):
    ORIGINAL = "# Doc\n\n## 1. La idea\ntexto\n\n## 2. Los `principios`\ntexto\n\n```\n## no es sección\n```\n"

    def test_secciones_ignora_bloques_de_codigo(self):
        self.assertEqual(d.secciones(self.ORIGINAL), ["1. La idea", "2. Los `principios`"])

    def test_detecta_la_seccion_que_falta(self):
        self.assertEqual(d.faltan(self.ORIGINAL, "## 1. La idea\n- a\n"), ["2. Los `principios`"])

    def test_todas_presentes_no_falta_nada(self):
        self.assertEqual(d.faltan(self.ORIGINAL, "# Índice\n## 1. La idea\n---\n## 2. Los principios\n"), [])


class Reparto(unittest.TestCase):
    def test_plantilla_skill_y_textos_en_los_dos_idiomas(self):
        for rel in (".brain/biblioteca/PLANTILLA_DIAPOSITIVAS.md", ".brain/biblioteca/PLANTILLA_DIAPOSITIVAS.en.md",
                    ".claude/skills/diapositivas/SKILL.md", ".claude/skills/diapositivas/SKILL.en.md"):
            if rel.endswith(".en.md") and not _es_repo_arnes():
                continue  # un proyecto en español no recibe las .en.md (spec 024)
            self.assertTrue(os.path.isfile(os.path.join(RAIZ, *rel.split("/"))), rel)
        import textos
        claves = [k for k in textos.TEXTOS["es"] if k.startswith("diap_")]
        self.assertGreaterEqual(len(claves), 10)
        for k in claves:
            self.assertIn(k, textos.TEXTOS["en"], k)

    def test_las_plantillas_se_convierten_y_cada_seccion_aparece(self):
        tmp = tempfile.mkdtemp()
        try:
            for nombre in ("PLANTILLA_DIAPOSITIVAS.md", "PLANTILLA_DIAPOSITIVAS.en.md"):
                if nombre.endswith(".en.md") and not _es_repo_arnes():
                    continue
                origen = os.path.join(RAIZ, ".brain", "biblioteca", nombre)
                rutas, n, _, _ = d.convertir(origen, os.path.join(tmp, nombre + ".html"), abrir=False)
                self.assertGreaterEqual(n, 5)
                with open(rutas[0], encoding="utf-8") as f:
                    self.assertNotIn("<!--", f.read())
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
