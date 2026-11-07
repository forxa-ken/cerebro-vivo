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

    def test_objetivo_se_crea_y_los_indices_lo_enlazan_primero(self):
        destino, _ = instalar()
        self.assertIn(".brain/architecture/objetivo.md", archivos(destino))
        for indice in ("CLAUDE.md", "AGENTS.md"):
            with open(os.path.join(destino, indice), encoding="utf-8") as f:
                texto = f.read()
            self.assertIn("architecture/objetivo.md", texto)
            self.assertLess(texto.index("objetivo.md"), texto.index("**Pendientes:**"))
        with open(os.path.join(destino, ".brain", "constitution.md"), encoding="utf-8") as f:
            self.assertIn("objetivo.md", f.read())

    @unittest.skipUnless(os.path.exists(os.path.join(RAIZ, "manifiesto.json")), "las skills de Codex las copia el manifiesto del repo del arnés (spec 019)")
    def test_skills_de_codex_solo_si_se_instala_codex(self):
        con, _ = instalar(ias=("claude", "codex"))
        sin, _ = instalar(ias=("claude",))
        self.assertTrue(any(a.startswith(".agents/skills/") for a in archivos(con)))
        self.assertFalse(any(a.startswith(".agents/") for a in archivos(sin)))

    def test_sin_rastros_de_lobohook(self):
        destino, _ = instalar()
        for rel in archivos(destino):
            if rel.startswith(".brain/biblioteca/") or rel == ".brain/arnes_instalado.json" or rel.startswith("tests/") or rel.startswith(".claude/skills/explicar-a-darwin-en-llano/") or rel.startswith(".agents/skills/explicar-a-darwin-en-llano/"):  # el nombre de esa skill lleva el del dueño original
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
            self.assertTrue(f.read().startswith("mío"))  # lo suyo queda intacto; el bloque se añade al final (spec 015)
        self.assertTrue(any("CLAUDE.md" in a and "adoptado" in a for a in hechos["avisos"]))
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

    @unittest.skipUnless(os.path.exists(os.path.join(RAIZ, "manifiesto.json")), "solo vale en el repo del arnés: un proyecto puede tener guardianes propios (spec 019)")
    def test_todo_guardian_nuevo_esta_en_el_kit(self):
        carpeta = os.path.join(RAIZ, ".brain", "guardianes")
        propios = {f[:-3] for f in os.listdir(carpeta) if f.endswith(".py")}
        self.assertEqual(propios - set(kit.GUARDIANES), set(), "Hay un guardián que el kit de arranque no instala: añadirlo a GUARDIANES")


class TestFusionConLoExistente(unittest.TestCase):
    """Spec 015: el kit se añade a un proyecto que ya tiene índice de IA y ajustes de Claude, sin quitar nada."""

    def proyecto(self, claude="# Mi proyecto\n\nRegla: nada de tabs.\n", ajustes=None):
        destino = tempfile.mkdtemp()
        if claude is not None:
            with open(os.path.join(destino, "CLAUDE.md"), "w", encoding="utf-8", newline="\n") as f:
                f.write(claude)
        if ajustes is not None:
            os.makedirs(os.path.join(destino, ".claude"))
            with open(os.path.join(destino, ".claude", "settings.json"), "w", encoding="utf-8") as f:
                f.write(ajustes if isinstance(ajustes, str) else json.dumps(ajustes))
        return destino

    def leer(self, destino, rel):
        with open(os.path.join(destino, *rel.split("/")), encoding="utf-8") as f:
            return f.read()

    def test_indice_conserva_lo_suyo_y_guarda_copia_integra(self):
        original = "# Mi proyecto\n\nRegla: nada de tabs.\n"
        destino = self.proyecto(original)
        _, hechos = instalar(destino=destino, ias=("claude",))
        texto = self.leer(destino, "CLAUDE.md")
        self.assertTrue(texto.startswith(original))
        self.assertIn(kit.MARCA_INI, texto)
        self.assertIn("Memoria persistente", texto)
        self.assertEqual(self.leer(destino, ".brain/archive/adoptado/CLAUDE.original.md"), original)
        self.assertEqual(self.leer(destino, "CLAUDE.md" + kit.COPIA), original)
        self.assertIn(os.path.join(destino, "CLAUDE.md"), hechos["fusionados"])
        self.assertIn("adoptar-indice-existente", self.leer(destino, ".brain/pendientes.md"))

    def test_segunda_instalacion_no_duplica(self):
        destino = self.proyecto()
        instalar(destino=destino, ias=("claude",))
        una_vez = self.leer(destino, "CLAUDE.md")
        _, hechos = instalar(destino=destino, ias=("claude",))
        self.assertEqual(self.leer(destino, "CLAUDE.md"), una_vez)
        self.assertEqual(una_vez.count(kit.MARCA_INI), 1)
        self.assertEqual(hechos["fusionados"], [])

    def test_ajustes_propios_se_conservan_y_se_anaden_los_del_kit(self):
        propios = {"model": "opus", "hooks": {"Stop": [{"hooks": [{"type": "command", "command": "echo mio"}]}]},
                   "permissions": {"allow": ["Bash(ls)"], "deny": ["Read(./secreto.txt)"]}}
        destino = self.proyecto(ajustes=propios)
        _, hechos = instalar(destino=destino, ias=("claude",))
        ajustes = json.loads(self.leer(destino, ".claude/settings.json"))
        self.assertEqual(ajustes["model"], "opus")
        self.assertEqual(ajustes["permissions"]["allow"], ["Bash(ls)"])
        self.assertIn("Read(./secreto.txt)", ajustes["permissions"]["deny"])
        self.assertIn("Read(./.env)", ajustes["permissions"]["deny"])
        stop = json.dumps(ajustes["hooks"]["Stop"])
        self.assertIn("echo mio", stop)
        self.assertIn("cierre.py", stop)
        self.assertIn("arranque.py", json.dumps(ajustes["hooks"]["SessionStart"]))
        self.assertEqual(json.loads(self.leer(destino, ".claude/settings.json" + kit.COPIA)), propios)
        self.assertTrue(any("ya tenía un hook en Stop" in a for a in hechos["avisos"]))
        instalar(destino=destino, ias=("claude",))  # idempotente
        self.assertEqual(json.loads(self.leer(destino, ".claude/settings.json")), ajustes)
        self.assertEqual(json.dumps(ajustes["hooks"]["Stop"]).count("cierre.py"), 1)

    def test_json_roto_no_se_toca_y_avisa(self):
        destino = self.proyecto(ajustes="{esto no es json")
        _, hechos = instalar(destino=destino, ias=("claude",))
        self.assertEqual(self.leer(destino, ".claude/settings.json"), "{esto no es json")
        self.assertTrue(any("No pude leer" in a and "cierre.py" in a for a in hechos["avisos"]))

    def test_simular_no_escribe_nada(self):
        destino = self.proyecto(ajustes={"hooks": {}})
        antes = archivos(destino)
        hechos = kit.instalar(destino, "Demo", "Ana", "español", "pytest", ["claude"], "completo", simular=True)
        self.assertEqual(archivos(destino), antes)
        self.assertEqual(self.leer(destino, "CLAUDE.md"), "# Mi proyecto\n\nRegla: nada de tabs.\n")
        self.assertEqual(len(hechos["fusionados"]), 2)

    def test_saltos_de_linea_de_windows_se_respetan_y_la_copia_es_identica(self):
        original = b"# Mio\nRegla uno\nRegla dos\n"
        destino = self.proyecto(None)
        with open(os.path.join(destino, "CLAUDE.md"), "wb") as f:
            f.write(original)
        instalar(destino=destino, ias=("claude",))
        with open(os.path.join(destino, ".brain", "archive", "adoptado", "CLAUDE.original.md"), "rb") as f:
            self.assertEqual(f.read(), original)
        with open(os.path.join(destino, "CLAUDE.md"), "rb") as f:
            nuevo = f.read()
        self.assertTrue(nuevo.startswith(original))
        self.assertNotIn(b"\n", nuevo.replace(b"\n", b""))  # ningún salto suelto: todo CRLF

    def test_indice_adoptado_grande_no_pone_en_rojo_la_comprobacion(self):
        destino = self.proyecto("# Mio\n" + "linea de reglas propias\n" * 600)
        instalar(destino=destino, ias=("claude",))
        self.assertTrue(all(ok for nombre, ok, _ in kit.comprobar(destino) if "Índices" in nombre))

    def test_copia_de_seguridad_no_se_sobrescribe(self):
        destino = self.proyecto("uno\n")
        instalar(destino=destino, ias=("claude",))
        ruta = os.path.join(destino, "CLAUDE.md")
        with open(ruta, "w", encoding="utf-8", newline="\n") as f:
            f.write("dos\n")  # el dueño reescribe y quita el bloque
        instalar(destino=destino, ias=("claude",))
        self.assertEqual(self.leer(destino, "CLAUDE.md" + kit.COPIA), "uno\n")


if __name__ == "__main__":
    unittest.main()
