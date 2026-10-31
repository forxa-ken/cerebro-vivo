# -*- coding: utf-8 -*-
"""Kit de arranque (spec 054): instala en una carpeta vacía, comprueba la estructura y que no queden rastros de LoboHook."""
import importlib.util
import json
import os
import re
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_espec = importlib.util.spec_from_file_location("instalar", os.path.join(RAIZ, ".brain", "biblioteca", "kit-arranque", "instalar.py"))
kit = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(kit)

# Palabras que delatan un dato de LoboHook (la biblioteca copiada es la carta, que lo cita como caso real)
RASTROS = re.compile(r"lobohook|darwin|users\.db|gumroad", re.I)


def instalar(nivel="completo", ias=("claude", "codex"), destino=None):
    destino = destino or tempfile.mkdtemp()
    hechos = kit.instalar(destino, "Demo", "Ana", "español", "pytest", list(ias), nivel, hoy="2026-01-01")
    return destino, hechos


def archivos(destino):
    res = []
    for base, dirs, nombres in os.walk(destino):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        res += [os.path.relpath(os.path.join(base, n), destino).replace("\\", "/") for n in nombres]
    return sorted(res)


class TestKitArranque(unittest.TestCase):
    def test_completo_crea_estructura_y_pasa_la_autocomprobacion(self):
        destino, _ = instalar()
        lista = archivos(destino)
        for esperado in ("CLAUDE.md", "AGENTS.md", ".brain/constitution.md", ".brain/pendientes.md", ".brain/decisions.log",
                         ".brain/guardianes/arranque.py", ".brain/guardianes/guardianes.json", ".brain/pruebas/indice.md",
                         ".claude/settings.json", "tests/test_cerebro_indices.py", ".brain/specs/_template.md"):
            self.assertIn(esperado, lista)
        self.assertNotIn("GEMINI.md", lista)
        fallos = [(n, f) for n, ok, f in kit.comprobar(destino) if not ok]
        self.assertEqual(fallos, [])

    def test_sin_rastros_de_lobohook(self):
        destino, _ = instalar()
        for rel in archivos(destino):
            if rel.startswith(".brain/biblioteca/") or rel == ".brain/arnes_instalado.json" or rel.startswith("tests/") or rel.startswith(".claude/skills/explicar-a-darwin-en-llano/"):  # el nombre de esa skill lleva el del dueño original
                continue
            with open(os.path.join(destino, rel), encoding="utf-8") as f:
                m = RASTROS.search(f.read())
            self.assertIsNone(m, "Rastro de un proyecto concreto en %s: %s" % (rel, m and m.group(0)))

    def test_configuracion_neutra(self):
        destino, _ = instalar()
        with open(os.path.join(destino, ".brain", "guardianes", "guardianes.json"), encoding="utf-8") as f:
            cfg = json.load(f)
        self.assertEqual(cfg["secretos"]["permitidos"], [])
        self.assertEqual(cfg["secretos"]["archivos_secretos"], [".env"])
        self.assertEqual(cfg["indices_entrada"], ["CLAUDE.md", "AGENTS.md"])
        self.assertFalse(cfg["analisis_activo"] or cfg["base_datos_activo"])

    def test_no_pisa_lo_que_ya_existe(self):
        destino, _ = instalar(nivel="medio")
        ruta = os.path.join(destino, ".brain", "pendientes.md")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("mío")
        _, hechos = instalar(nivel="medio", destino=destino)
        with open(ruta, encoding="utf-8") as f:
            self.assertEqual(f.read(), "mío")
        self.assertIn(ruta, hechos["respetados"])

    def test_proyecto_existente_de_otro_lenguaje(self):
        destino = tempfile.mkdtemp()
        for nombre, texto in (("main.lua", 'print("hola")'), ("CLAUDE.md", "mío")):
            with open(os.path.join(destino, nombre), "w", encoding="utf-8") as f:
                f.write(texto)
        _, hechos = instalar(destino=destino)
        with open(os.path.join(destino, "CLAUDE.md"), encoding="utf-8") as f:
            self.assertEqual(f.read(), "mío")
        self.assertTrue(any("Ya tenías CLAUDE.md" in a for a in hechos["avisos"]))
        with open(os.path.join(destino, ".gitignore"), encoding="utf-8") as f:
            self.assertIn(".env", f.read().splitlines())
        espec = importlib.util.spec_from_file_location("librerias", os.path.join(destino, ".brain", "guardianes", "librerias.py"))
        lib = importlib.util.module_from_spec(espec)
        espec.loader.exec_module(lib)
        self.assertEqual(lib.resumen(destino, {"librerias_activo": True, "librerias": {}}), [])  # sin requirements.txt: calla

    def test_niveles(self):
        ligero = archivos(instalar("ligero", ("claude",))[0])
        self.assertEqual(ligero, [".brain/decisions.log", ".brain/pendientes.md", "CLAUDE.md"])
        medio = archivos(instalar("medio", ("claude",))[0])
        self.assertIn(".brain/constitution.md", medio)
        self.assertFalse([f for f in medio if f.startswith(".brain/guardianes")])

    def test_todo_guardian_nuevo_esta_en_el_kit(self):
        carpeta = os.path.join(RAIZ, ".brain", "guardianes")
        propios = {f[:-3] for f in os.listdir(carpeta) if f.endswith(".py")}
        self.assertEqual(propios - set(kit.GUARDIANES), set(), "Hay un guardián que el kit de arranque no instala: añadirlo a GUARDIANES")


if __name__ == "__main__":
    unittest.main()
