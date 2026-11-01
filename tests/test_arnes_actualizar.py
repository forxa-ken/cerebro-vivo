# -*- coding: utf-8 -*-
"""Actualizador del arnés (spec 087): simulación, archivo modificado a mano, datos intocables y copia de seguridad."""
import contextlib
import importlib.util
import io
import json
import os
import shutil
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_espec = importlib.util.spec_from_file_location("actualizar_arnes", os.path.join(RAIZ, ".brain", "guardianes", "actualizar_arnes.py"))
act = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(act)
_espec = importlib.util.spec_from_file_location("instalar", os.path.join(RAIZ, ".brain", "biblioteca", "kit-arranque", "instalar.py"))
kit = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(kit)


def escribir(base, rel, texto):
    ruta = os.path.join(base, *rel.split("/"))
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)


def leer(base, rel):
    with open(os.path.join(base, *rel.split("/")), encoding="utf-8", newline="") as f:
        return f.read()


def arbol(base):
    res = {}
    for carpeta, dirs, nombres in os.walk(base):
        for n in nombres:
            ruta = os.path.join(carpeta, n)
            with open(ruta, "rb") as f:
                res[os.path.relpath(ruta, base)] = f.read()
    return res


class Base(unittest.TestCase):
    def setUp(self):
        self.repo, self.proy = tempfile.mkdtemp(), tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.repo, True)
        self.addCleanup(shutil.rmtree, self.proy, True)
        self.poner_repo({".brain/guardianes/uno.py": "# uno v1 de Darwin\n", ".claude/skills/s/SKILL.md": "skill v1\n"}, "1.0.0")
        escribir(self.repo, ".brain/guardianes/guardianes.json", json.dumps({"_ayuda": "x", "a": 1, "arnes_repo": ""}))

    def poner_repo(self, archivos, version):
        for rel, texto in archivos.items():
            escribir(self.repo, rel, texto)
        m = {"version": version, "archivos": {rel: act.huella(act._normalizar(act.leer_bytes(os.path.join(self.repo, *rel.split("/"))), rel))
                                              for rel in archivos}, "pruebas": []}
        ruta = os.path.join(self.repo, "manifiesto.json")
        if os.path.exists(ruta):
            with open(ruta, encoding="utf-8") as f:
                previo = json.load(f)
            previo["archivos"].update(m["archivos"])
            m["archivos"] = previo["archivos"]
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(m, f)


class TestSincronizar(Base):
    def test_con_codex_las_skills_tambien_van_a_agents_skills(self):
        escribir(self.proy, "AGENTS.md", "# indice" + chr(10))
        res = act.sincronizar(self.repo, self.proy)
        self.assertIn(".agents/skills/s/SKILL.md", res["nuevos"])
        self.assertTrue(os.path.isfile(os.path.join(self.proy, ".agents", "skills", "s", "SKILL.md")))
        self.assertEqual(act.sincronizar(self.repo, self.proy, simular=True)["nuevos"], [])

    def test_sin_codex_no_se_crea_agents_skills(self):
        act.sincronizar(self.repo, self.proy)
        self.assertFalse(os.path.exists(os.path.join(self.proy, ".agents")))

    def test_simular_no_escribe_nada(self):
        escribir(self.proy, ".brain/pendientes.md", "mío")
        antes = arbol(self.proy)
        res = act.sincronizar(self.repo, self.proy, simular=True)
        self.assertEqual(sorted(res["nuevos"]), [".brain/guardianes/uno.py", ".claude/skills/s/SKILL.md"])
        self.assertEqual(arbol(self.proy), antes)

    def test_instala_y_anota_la_version(self):
        res = act.sincronizar(self.repo, self.proy)
        self.assertEqual(len(res["nuevos"]), 2)
        self.assertEqual(leer(self.proy, ".claude/skills/s/SKILL.md"), "skill v1\n")
        self.assertEqual(act.cargar_registro(self.proy)["version"], "1.0.0")
        self.assertEqual(act.sincronizar(self.repo, self.proy)["sin_cambios"].__len__(), 2)

    def test_actualiza_lo_que_no_se_tocó_y_guarda_copia(self):
        act.sincronizar(self.repo, self.proy)
        self.poner_repo({".claude/skills/s/SKILL.md": "skill v2\n"}, "1.1.0")
        res = act.sincronizar(self.repo, self.proy)
        self.assertEqual(res["actualizados"], [".claude/skills/s/SKILL.md"])
        self.assertEqual(leer(self.proy, ".claude/skills/s/SKILL.md"), "skill v2\n")
        self.assertEqual(leer(self.proy, os.path.join(res["copia"], ".claude", "skills", "s", "SKILL.md").replace("\\", "/")), "skill v1\n")
        self.assertEqual(act.cargar_registro(self.proy)["version"], "1.1.0")

    def test_no_pisa_lo_modificado_a_mano(self):
        act.sincronizar(self.repo, self.proy)
        escribir(self.proy, ".claude/skills/s/SKILL.md", "skill con mis cambios\n")
        self.poner_repo({".claude/skills/s/SKILL.md": "skill v2\n"}, "1.1.0")
        res = act.sincronizar(self.repo, self.proy)
        self.assertEqual(res["a_mano"], [".claude/skills/s/SKILL.md"])
        self.assertEqual(leer(self.proy, ".claude/skills/s/SKILL.md"), "skill con mis cambios\n")
        self.assertIsNone(res["copia"])

    def test_forzar_pisa_con_copia(self):
        act.sincronizar(self.repo, self.proy)
        escribir(self.proy, ".claude/skills/s/SKILL.md", "mío\n")
        self.poner_repo({".claude/skills/s/SKILL.md": "skill v2\n"}, "1.1.0")
        res = act.sincronizar(self.repo, self.proy, forzar=[".claude/skills/s/SKILL.md"])
        self.assertEqual(res["forzados"], [".claude/skills/s/SKILL.md"])
        self.assertEqual(leer(self.proy, ".claude/skills/s/SKILL.md"), "skill v2\n")
        self.assertTrue(res["copia"])

    def test_forzar_todo_adopta_un_proyecto_antiguo_con_copia(self):
        escribir(self.proy, ".claude/skills/s/SKILL.md", "versión antigua sin registro\n")
        res = act.sincronizar(self.repo, self.proy, forzar_todo=True)
        self.assertEqual(res["forzados"], [".claude/skills/s/SKILL.md"])
        self.assertEqual(leer(self.proy, ".claude/skills/s/SKILL.md"), "skill v1\n")
        self.assertEqual(leer(self.proy, os.path.join(res["copia"], ".claude", "skills", "s", "SKILL.md").replace("\\", "/")), "versión antigua sin registro\n")

    def test_archivo_existente_sin_registro_distinto_no_se_pisa(self):
        escribir(self.proy, ".claude/skills/s/SKILL.md", "otra cosa\n")
        res = act.sincronizar(self.repo, self.proy)
        self.assertEqual(res["a_mano"], [".claude/skills/s/SKILL.md"])
        self.assertEqual(leer(self.proy, ".claude/skills/s/SKILL.md"), "otra cosa\n")

    def test_saltos_de_linea_de_windows_no_cuentan_como_cambio(self):
        ruta = os.path.join(self.proy, ".claude", "skills", "s", "SKILL.md")
        os.makedirs(os.path.dirname(ruta))
        with open(ruta, "wb") as f:
            f.write(b"skill v1\r\n")
        self.assertIn(".claude/skills/s/SKILL.md", act.sincronizar(self.repo, self.proy)["sin_cambios"])

    def test_nunca_toca_datos_ni_configuracion_y_solo_propone_claves(self):
        datos = {".brain/pendientes.md": "p", ".brain/decisions.log": "d", ".brain/specs/001-x.md": "s", ".brain/decisions/D-001.md": "d1",
                 ".brain/guardianes/guardianes.json": json.dumps({"mia": True})}
        for rel, t in datos.items():
            escribir(self.proy, rel, t)
        res = act.sincronizar(self.repo, self.proy)
        for rel, t in datos.items():
            self.assertEqual(leer(self.proy, rel), t, rel)
        self.assertEqual(res["claves_nuevas"], {"a": 1})  # propuesta, sin `_ayuda` ni `arnes_repo`

    def test_el_nombre_del_dueño_se_cambia_en_los_textos(self):
        act.sincronizar(self.repo, self.proy, dueno="Ana")
        self.assertEqual(leer(self.proy, ".brain/guardianes/uno.py"), "# uno v1 de Ana\n")
        self.assertEqual(act.sincronizar(self.repo, self.proy)["sin_cambios"].__len__(), 2)  # el dueño queda registrado

    def test_rutas_fuera_de_la_carpeta_se_rechazan(self):
        with open(os.path.join(self.repo, "manifiesto.json"), "w", encoding="utf-8") as f:
            json.dump({"version": "9", "archivos": {"../fuera.txt": "x"}}, f)
        with self.assertRaises(ValueError):
            act.sincronizar(self.repo, self.proy)

    def test_mismo_repo_y_proyecto_se_rechaza(self):
        with self.assertRaises(ValueError):
            act.sincronizar(self.repo, self.repo)


class TestPrograma(Base):
    def correr(self, *args, repo=None):
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            codigo = act.main(list(args), repo=repo)
        return codigo, salida.getvalue()

    def test_desde_el_repo_con_simular(self):
        antes = arbol(self.proy)
        codigo, texto = self.correr(self.proy, "--simular", repo=self.repo)
        self.assertEqual(codigo, 0)
        self.assertIn("simulación", texto)
        self.assertIn("+ .claude/skills/s/SKILL.md", texto)
        self.assertEqual(arbol(self.proy), antes)

    def test_dentro_del_proyecto_lee_arnes_repo_de_guardianes_json(self):
        escribir(self.proy, ".brain/guardianes/guardianes.json", json.dumps({"arnes_repo": self.repo}))
        repo, tmp = act.localizar_repo(self.proy, None)
        self.assertEqual((repo, tmp), (os.path.abspath(self.repo), None))

    def test_sin_saber_donde_esta_el_repo_avisa(self):
        with self.assertRaises(ValueError):
            act.localizar_repo(self.proy, None)

    def test_carpeta_que_no_es_el_repo(self):
        codigo, texto = self.correr(self.proy, "--simular", repo=self.proy)
        self.assertEqual(codigo, 2)
        self.assertIn("no es el repo del arnés", texto)

    def test_informe_avisa_de_los_modificados_a_mano(self):
        act.sincronizar(self.repo, self.proy)
        escribir(self.proy, ".claude/skills/s/SKILL.md", "mío\n")
        self.poner_repo({".claude/skills/s/SKILL.md": "skill v2\n"}, "1.1.0")
        codigo, texto = self.correr(self.proy, "--simular", repo=self.repo)
        self.assertIn("NO pisados", texto)
        self.assertIn("! .claude/skills/s/SKILL.md", texto)
        self.assertIn("1.0.0 → 1.1.0", texto)


class TestConElRepoReal(unittest.TestCase):
    """El kit instala el arnés real en un proyecto nuevo y el actualizador lo reconoce como al día."""

    def test_proyecto_nuevo_queda_al_dia_y_la_simulacion_funciona(self):
        proy = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, proy, True)
        kit.instalar(proy, "Demo", "Ana", "español", "python -m unittest discover tests", ["claude"], "completo", hoy="2026-01-01")
        res = act.sincronizar(RAIZ, proy, simular=True)
        self.assertEqual((res["nuevos"], res["actualizados"], res["a_mano"], res["forzados"]), ([], [], [], []))
        self.assertEqual(act.cargar_registro(proy)["dueno"], "Ana")
        self.assertFalse(os.path.exists(os.path.join(proy, ".brain", "copias_arnes")), "instalar no debe dejar copias de seguridad")
        with open(os.path.join(proy, ".brain", "guardianes", "guardianes.json"), encoding="utf-8") as f:
            self.assertEqual(json.load(f)["arnes_repo"], RAIZ)
        self.assertTrue(os.path.isfile(os.path.join(proy, ".brain", "guardianes", "actualizar_arnes.py")))
        espec = importlib.util.spec_from_file_location("actualizar_del_proyecto", os.path.join(proy, ".brain", "guardianes", "actualizar_arnes.py"))
        copia = importlib.util.module_from_spec(espec)
        espec.loader.exec_module(copia)  # la copia instalada (con el nombre del dueño cambiado) debe seguir reconociendo todo
        res = copia.sincronizar(RAIZ, proy, simular=True)
        self.assertEqual((res["nuevos"], res["actualizados"], res["a_mano"]), ([], [], []))
        for skill in ("prompt-inicial", "resumen", "pendiente"):
            self.assertTrue(os.path.isdir(os.path.join(proy, ".claude", "skills", skill)))
        self.assertTrue(os.path.isfile(os.path.join(proy, ".brain", "biblioteca", "kit-traduccion", "i18n_motor.js")))


if __name__ == "__main__":
    unittest.main()
