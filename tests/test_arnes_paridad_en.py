# -*- coding: utf-8 -*-
"""Spec 024 fase 3: cada edición inglesa (`X.en.md`) sigue a su original `X.md`: mismo esqueleto, mismos marcadores y comandos."""
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CARPETAS = [".claude/skills", ".brain/biblioteca", ".brain/biblioteca/kit-arranque/plantillas", ".brain/specs", ".brain/pruebas"]


def ediciones():
    res = []
    for c in CARPETAS:
        for base, _, nombres in os.walk(os.path.join(RAIZ, *c.split("/"))):
            for n in nombres:
                m = re.match(r"^(.*)\.en(\.md)$", n)
                if m:
                    res.append((os.path.join(base, n), os.path.join(base, m.group(1) + m.group(2))))
    return res


def leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        return f.read().replace("\r\n", "\n")


def frontmatter(texto):
    m = re.match(r"^---\n(.*?)\n---\n", texto, re.S)
    return m.group(1) if m else ""


class TestParidadEn(unittest.TestCase):
    def test_cada_skill_y_documento_clave_tiene_edicion_inglesa(self):
        skills = os.path.join(RAIZ, ".claude", "skills")
        for n in sorted(os.listdir(skills)):
            self.assertTrue(os.path.isfile(os.path.join(skills, n, "SKILL.en.md")), "falta SKILL.en.md en " + n)
        for rel in (".brain/biblioteca/CEREBRO_VIVO.en.md", ".brain/biblioteca/PLANTILLA_TRASPASO.en.md",
                    ".brain/biblioteca/PLANTILLA_NOTA_CHAT.en.md", "README.en.md", "MANUAL_DE_USO.en.md",
                    ".brain/biblioteca/kit-arranque/README.en.md", ".brain/biblioteca/kit-traduccion/README.en.md",
                    ".brain/specs/_template.en.md", ".brain/pruebas/_plantilla.en.md"):
            self.assertTrue(os.path.isfile(os.path.join(RAIZ, rel)), "falta " + rel)
        plantillas = os.path.join(RAIZ, ".brain", "biblioteca", "kit-arranque", "plantillas")
        for n in sorted(os.listdir(plantillas)):
            if n.endswith(".md") and not n.endswith(".en.md"):
                self.assertTrue(os.path.isfile(os.path.join(plantillas, n[:-3] + ".en.md")), "falta la edición inglesa de " + n)

    def test_encabezado_de_las_skills_igual(self):
        for en, es in ediciones():
            if os.path.basename(es) == "SKILL.md":
                self.assertEqual(frontmatter(leer(en)), frontmatter(leer(es)), en)

    def test_mismo_esqueleto_de_titulos_y_marcadores(self):
        for en, es in ediciones():
            a, b = leer(en), leer(es)
            tit = lambda t: [len(m.group(1)) for m in re.finditer(r"^(#{1,6}) ", re.sub(r"```.*?```", "", t, flags=re.S), re.M)]
            self.assertEqual(tit(a), tit(b), "titulos distintos en " + en)
            marc = lambda t: sorted(re.findall(r"\{\{[A-Z_]+\}\}", t))
            self.assertEqual(marc(a), marc(b), "marcadores {{X}} distintos en " + en)
            self.assertEqual(len(re.findall(r"```", a)), len(re.findall(r"```", b)), "bloques de codigo distintos en " + en)

    def test_los_comandos_y_rutas_no_se_traducen(self):
        for en, es in ediciones():
            if os.path.basename(es) in ("MANUAL.md",):
                continue
            a, b = leer(en), leer(es)
            cmd = lambda t: set(re.findall(r"`((?:python|/)[a-z][^`]*)`", t))
            faltan = {c for c in cmd(b) if re.match(r"python (\.brain|actualizar|generar)", c)} - cmd(a)
            self.assertFalse(faltan, "%s: faltan comandos %s" % (en, sorted(faltan)[:3]))

    def test_la_edicion_inglesa_no_deja_frases_en_espanol(self):
        palabras = re.compile(r"\b(Cómo \(pasos\)|Error que evita|Dónde está en el repo|Usada|Veces:|Falta programar|Esperando tu prueba)\b")
        for en, es in ediciones():
            if os.path.basename(es) in ("SKILL.md",):
                self.assertFalse(palabras.search(leer(en)), "titulos en espanol en " + en)

    def test_instalar_en_ingles_trae_la_constitucion_y_el_indice_en_ingles(self):
        destino = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, destino, True)
        r = subprocess.run([sys.executable, "-I", os.path.join(RAIZ, ".brain", "biblioteca", "kit-arranque", "instalar.py"), destino,
                            "--nombre", "Demo", "--dueno", "Ana", "--nivel", "completo", "--idioma", "English", "--ias", "claude"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", stdin=subprocess.DEVNULL, timeout=600,
                           env=dict(os.environ, PYTHONIOENCODING="utf-8"))
        self.assertEqual(r.returncode, 0, r.stdout[-500:] + r.stderr[-500:])
        const = leer(os.path.join(destino, ".brain", "constitution.md"))
        self.assertIn("Constitution of Demo", const)
        self.assertIn("**English**", const)
        self.assertIn("Entry index for Claude", leer(os.path.join(destino, "CLAUDE.md")))
        skill = leer(os.path.join(destino, ".claude", "skills", "version", "SKILL.md"))
        self.assertIn("which harness version", skill)
        self.assertFalse(os.path.exists(os.path.join(destino, ".claude", "skills", "version", "SKILL.en.md")))
        self.assertIn("The \"Cerebro Vivo\" method", leer(os.path.join(destino, ".brain", "biblioteca", "CEREBRO_VIVO.md")))
        self.assertIn("Ana", leer(os.path.join(destino, ".brain", "constitution.md")))


if __name__ == "__main__":
    unittest.main()
