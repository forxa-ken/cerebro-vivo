# -*- coding: utf-8 -*-
"""Actualizador del arnés (specs 087 y 021): simulación, modificado a mano, datos intocables, copia de seguridad, retirados,
corte a media escritura, versión honesta, huella del manifiesto y nivel del proyecto."""
import contextlib
import importlib.util
import io
import json
import os
import shutil
import tempfile
import unittest
from unittest import mock

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

    def test_nunca_toca_datos_y_la_configuracion_solo_gana_claves_nuevas(self):
        datos = {".brain/pendientes.md": "p", ".brain/decisions.log": "d", ".brain/specs/001-x.md": "s", ".brain/decisions/D-001.md": "d1"}
        for rel, t in datos.items():
            escribir(self.proy, rel, t)
        escribir(self.proy, ".brain/guardianes/guardianes.json", json.dumps({"mia": True, "a": 5}))
        res = act.sincronizar(self.repo, self.proy)
        for rel, t in datos.items():
            self.assertEqual(leer(self.proy, rel), t, rel)
        cfg = json.loads(leer(self.proy, ".brain/guardianes/guardianes.json"))
        self.assertEqual(cfg["mia"], True)
        self.assertEqual(cfg["a"], 5)  # lo que el proyecto ya tenía no se cambia (spec 019)
        self.assertEqual(cfg["arnes_repo"], os.path.abspath(self.repo))  # se anota dónde está el arnés
        self.assertEqual(res["claves_escritas"], {"arnes_repo": os.path.abspath(self.repo)})

    def test_claves_nuevas_se_anaden_y_con_simular_no_se_escribe(self):
        escribir(self.proy, ".brain/guardianes/guardianes.json", json.dumps({"mia": True}))
        res = act.sincronizar(self.repo, self.proy, simular=True)
        self.assertIn("a", res["claves_escritas"])
        self.assertEqual(json.loads(leer(self.proy, ".brain/guardianes/guardianes.json")), {"mia": True})
        act.sincronizar(self.repo, self.proy)
        self.assertEqual(json.loads(leer(self.proy, ".brain/guardianes/guardianes.json"))["a"], 1)

    def test_aviso_de_version_nueva(self):
        escribir(self.repo, "VERSION", "1.2.0\n")
        escribir(self.proy, ".brain/guardianes/guardianes.json", json.dumps({"arnes_repo": self.repo}))
        act.guardar_registro(self.proy, {"version": "1.1.0", "archivos": {}})
        self.assertEqual(act.version_disponible(self.proy), ("1.1.0", "1.2.0"))
        act.guardar_registro(self.proy, {"version": "1.2.0", "archivos": {}})
        self.assertIsNone(act.version_disponible(self.proy))
        act.guardar_registro(self.proy, {"version": "1.10.0", "archivos": {}})  # 1.10 es mayor que 1.2
        self.assertIsNone(act.version_disponible(self.proy))

    def test_fichas_de_skills_nuevas_se_anaden_al_indice(self):
        escribir(self.repo, ".brain/experiencia/indice.md", "| h |\n| [s](../../.claude/skills/s/SKILL.md) | cuando | Método | x |\n")
        escribir(self.proy, ".brain/experiencia/indice.md", "| h |\n")
        escribir(self.proy, ".claude/skills/s/SKILL.md", "skill v1\n")
        self.assertEqual(act.completar_fichas_skills(self.repo, self.proy), ["s"])
        self.assertIn("skills/s/SKILL.md", leer(self.proy, ".brain/experiencia/indice.md"))
        self.assertEqual(act.completar_fichas_skills(self.repo, self.proy), [])

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


class TestHooks(Base):
    """Informe 028 (3.1): el actualizador añade a .claude/settings.json los hooks de guardianes que faltan, sin tocar los que hay."""
    def hook(self, guardian, prefijo="python", matcher=None):
        e = {"hooks": [{"type": "command", "command": '%s "$CLAUDE_PROJECT_DIR/.brain/guardianes/%s.py"' % (prefijo, guardian), "timeout": 20}]}
        if matcher:
            e["matcher"] = matcher
        return [e]

    def preparar(self, prefijo="python3"):
        for g in ("arranque", "eventos_chat"):
            escribir(self.repo, ".brain/guardianes/%s.py" % g, "# %s\n" % g)
        escribir(self.repo, ".claude/settings.json", json.dumps({"hooks": {"SessionStart": self.hook("arranque"),
                                                                           "PreToolUse": self.hook("eventos_chat", matcher="Bash|PowerShell")}}))
        propio = {"hooks": {"SessionStart": self.hook("arranque", prefijo)}, "permissions": {"deny": ["Read(./.env)"]}}
        escribir(self.proy, ".claude/settings.json", json.dumps(propio))
        return propio

    def test_anade_el_hook_que_falta_con_el_interprete_del_proyecto_y_guarda_copia(self):
        self.preparar()
        self.assertEqual(act.completar_hooks(self.repo, self.proy), ["eventos_chat.py"])
        ajustes = json.loads(leer(self.proy, ".claude/settings.json"))
        nuevo = ajustes["hooks"]["PreToolUse"][0]
        self.assertEqual(nuevo["matcher"], "Bash|PowerShell")
        self.assertTrue(nuevo["hooks"][0]["command"].startswith('python3 "$CLAUDE_PROJECT_DIR'))
        self.assertEqual(ajustes["permissions"], {"deny": ["Read(./.env)"]})
        self.assertEqual(len(ajustes["hooks"]["SessionStart"]), 1)  # el que ya estaba no se duplica
        copias = os.path.join(self.proy, act.COPIAS)
        self.assertTrue(any(".claude" in c for c, _, _ in os.walk(copias)))

    def test_segunda_vez_no_hace_nada(self):
        self.preparar()
        act.completar_hooks(self.repo, self.proy)
        antes = leer(self.proy, ".claude/settings.json")
        self.assertEqual(act.completar_hooks(self.repo, self.proy), [])
        self.assertEqual(leer(self.proy, ".claude/settings.json"), antes)

    def test_simular_anuncia_pero_no_escribe(self):
        propio = self.preparar()
        self.assertEqual(act.completar_hooks(self.repo, self.proy, simular=True), ["eventos_chat.py"])
        self.assertEqual(json.loads(leer(self.proy, ".claude/settings.json")), propio)

    def test_sin_ajustes_o_roto_no_toca_nada(self):
        for g in ("eventos_chat",):
            escribir(self.repo, ".brain/guardianes/%s.py" % g, "# x\n")
        escribir(self.repo, ".claude/settings.json", json.dumps({"hooks": {"PreToolUse": self.hook("eventos_chat")}}))
        self.assertEqual(act.completar_hooks(self.repo, self.proy), [])
        self.assertFalse(os.path.exists(os.path.join(self.proy, ".claude", "settings.json")))
        escribir(self.proy, ".claude/settings.json", "{esto no es json")
        self.assertEqual(act.completar_hooks(self.repo, self.proy), [])
        self.assertEqual(leer(self.proy, ".claude/settings.json"), "{esto no es json")

    def test_sincronizar_lo_incluye_en_el_resultado_y_en_el_informe(self):
        self.preparar()
        res = act.sincronizar(self.repo, self.proy)
        self.assertEqual(res["hooks_nuevos"], ["eventos_chat.py"])
        self.assertIn("eventos_chat.py", act.informe(res, False))

    def test_el_hook_del_repo_y_el_del_instalador_coinciden(self):
        """El instalador del kit y el settings.json del repo deben pedir el mismo matcher para el guardián de eventos."""
        with open(os.path.join(RAIZ, ".claude", "settings.json"), encoding="utf-8") as f:
            repo = json.load(f)["hooks"]["PreToolUse"][0]
        with open(os.path.join(RAIZ, ".brain", "biblioteca", "kit-arranque", "instalar.py"), encoding="utf-8") as f:
            codigo = f.read()
        self.assertIn('"matcher": "%s"' % repo["matcher"], codigo)
        self.assertEqual(repo["matcher"], "Bash|PowerShell")


class TestPrograma(Base):
    def correr(self, *args, repo=None):
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            codigo = act.main(list(args), repo=repo)
        return codigo, salida.getvalue()

    def test_desde_el_repo_con_simular(self):
        escribir(self.proy, ".brain/guardianes/guardianes.json", "{}")  # spec 021: sin guardianes no se actualiza
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


class TestRetirados(Base):
    """Spec 021: lo que el arnés deja de repartir sale de los proyectos, sin borrarse."""

    def retirar(self, *rutas, version="1.1.0"):
        ruta = os.path.join(self.repo, "manifiesto.json")
        with open(ruta, encoding="utf-8") as f:
            m = json.load(f)
        for rel in rutas:
            m["archivos"].pop(rel, None)
        m["retirados"], m["version"] = sorted(rutas), version
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(m, f)

    def en_copia(self, res, rel):
        return leer(self.proy, res["copia"].replace("\\", "/") + "/" + rel)

    def test_retirado_sin_tocar_va_a_la_copia_y_sale_del_registro(self):
        act.sincronizar(self.repo, self.proy)
        self.retirar(".claude/skills/s/SKILL.md")
        res = act.sincronizar(self.repo, self.proy)
        self.assertEqual(res["retirados"], [".claude/skills/s/SKILL.md"])
        self.assertFalse(os.path.exists(os.path.join(self.proy, ".claude", "skills", "s")), "la carpeta vacía tampoco se queda")
        self.assertEqual(self.en_copia(res, ".claude/skills/s/SKILL.md"), "skill v1\n")
        self.assertNotIn(".claude/skills/s/SKILL.md", act.cargar_registro(self.proy)["archivos"])

    def test_retirado_modificado_a_mano_no_se_toca_y_se_lista(self):
        act.sincronizar(self.repo, self.proy)
        escribir(self.proy, ".claude/skills/s/SKILL.md", "mío\n")
        self.retirar(".claude/skills/s/SKILL.md")
        res = act.sincronizar(self.repo, self.proy)
        self.assertEqual((res["retirados"], res["retirados_a_mano"]), ([], [".claude/skills/s/SKILL.md"]))
        self.assertEqual(leer(self.proy, ".claude/skills/s/SKILL.md"), "mío\n")
        self.assertIn(".claude/skills/s/SKILL.md", act.cargar_registro(self.proy)["sin_aplicar"])

    def test_retirado_sin_registro_no_se_toca(self):
        escribir(self.proy, ".claude/skills/vieja/SKILL.md", "de otro\n")
        self.retirar(".claude/skills/vieja/SKILL.md")
        res = act.sincronizar(self.repo, self.proy)
        self.assertEqual(res["retirados_a_mano"], [".claude/skills/vieja/SKILL.md"])
        self.assertEqual(leer(self.proy, ".claude/skills/vieja/SKILL.md"), "de otro\n")

    def test_forzar_retira_lo_modificado_con_copia(self):
        act.sincronizar(self.repo, self.proy)
        escribir(self.proy, ".claude/skills/s/SKILL.md", "mío\n")
        self.retirar(".claude/skills/s/SKILL.md")
        res = act.sincronizar(self.repo, self.proy, forzar=[".claude/skills/s/SKILL.md"])
        self.assertEqual(res["retirados"], [".claude/skills/s/SKILL.md"])
        self.assertEqual(self.en_copia(res, ".claude/skills/s/SKILL.md"), "mío\n")

    def test_retirado_ya_ausente_solo_sale_del_registro(self):
        act.sincronizar(self.repo, self.proy)
        os.remove(os.path.join(self.proy, ".claude", "skills", "s", "SKILL.md"))
        self.retirar(".claude/skills/s/SKILL.md")
        res = act.sincronizar(self.repo, self.proy)
        self.assertEqual((res["retirados"], res["retirados_a_mano"], res["copia"]), ([], [], None))
        self.assertNotIn(".claude/skills/s/SKILL.md", act.cargar_registro(self.proy)["archivos"])

    def test_la_copia_de_codex_tambien_se_retira(self):
        escribir(self.proy, "AGENTS.md", "# indice\n")
        act.sincronizar(self.repo, self.proy)
        self.retirar(".claude/skills/s/SKILL.md")
        res = act.sincronizar(self.repo, self.proy)
        self.assertEqual(sorted(res["retirados"]), [".agents/skills/s/SKILL.md", ".claude/skills/s/SKILL.md"])
        self.assertFalse(os.path.exists(os.path.join(self.proy, ".agents", "skills", "s")))

    def test_la_fila_de_la_skill_retirada_sale_del_indice(self):
        fila = "| [s](../../.claude/skills/s/SKILL.md) | cuando | Método | x |\n"
        otra = "| [otra](../../.claude/skills/otra/SKILL.md) | y | z | x |\n"
        escribir(self.proy, ".brain/experiencia/indice.md", "| h |\n" + fila + otra)
        escribir(self.repo, ".brain/experiencia/indice.md", "| h |\n")
        act.sincronizar(self.repo, self.proy)
        self.retirar(".claude/skills/s/SKILL.md")
        res = act.sincronizar(self.repo, self.proy)
        self.assertEqual(res["filas_quitadas"], ["s"])
        self.assertEqual(leer(self.proy, ".brain/experiencia/indice.md"), "| h |\n" + otra)
        self.assertIn(fila, self.en_copia(res, ".brain/experiencia/indice.md"))

    def test_la_fila_de_la_skill_que_se_queda_a_mano_no_se_quita(self):
        fila = "| [s](../../.claude/skills/s/SKILL.md) | cuando | Método | x |\n"
        escribir(self.proy, ".brain/experiencia/indice.md", "| h |\n" + fila)
        escribir(self.repo, ".brain/experiencia/indice.md", "| h |\n")
        act.sincronizar(self.repo, self.proy)
        escribir(self.proy, ".claude/skills/s/SKILL.md", "mío\n")
        self.retirar(".claude/skills/s/SKILL.md")
        self.assertEqual(act.sincronizar(self.repo, self.proy)["filas_quitadas"], [])
        self.assertIn(fila, leer(self.proy, ".brain/experiencia/indice.md"))

    def test_ruta_retirada_fuera_de_la_carpeta_se_rechaza(self):
        self.retirar("../fuera.txt")
        with self.assertRaises(ValueError):
            act.sincronizar(self.repo, self.proy)

    def test_simular_anuncia_lo_mismo_que_hace_y_no_escribe(self):
        # Una skill que se retira, otra que llega nueva con su fila, una clave nueva y un archivo modificado a mano.
        escribir(self.proy, ".brain/guardianes/guardianes.json", json.dumps({"arnes_repo": "x"}))
        escribir(self.proy, ".brain/experiencia/indice.md", "| h |\n| [s](../../.claude/skills/s/SKILL.md) | c | M | x |\n")
        escribir(self.repo, ".brain/experiencia/indice.md", "| h |\n| [nueva](../../.claude/skills/nueva/SKILL.md) | c | M | x |\n")
        act.sincronizar(self.repo, self.proy)
        escribir(self.proy, ".brain/guardianes/uno.py", "# a mano\n")
        self.poner_repo({".brain/guardianes/uno.py": "# uno v2\n", ".claude/skills/nueva/SKILL.md": "nueva\n"}, "1.1.0")
        self.retirar(".claude/skills/s/SKILL.md")
        antes = arbol(self.proy)
        sim = act.sincronizar(self.repo, self.proy, simular=True)
        self.assertEqual(arbol(self.proy), antes)
        self.assertEqual(sim["retirados"], [".claude/skills/s/SKILL.md"])
        self.assertEqual(sim["filas_quitadas"], ["s"])
        self.assertEqual(sim["fichas"], ["nueva"])
        self.assertEqual(sim["sin_aplicar"], [".brain/guardianes/uno.py"])
        texto = act.informe(sim, True)
        self.assertIn(".claude/skills/s/SKILL.md", texto)
        self.assertIn("nueva", texto)
        real = act.sincronizar(self.repo, self.proy)
        for clave in ("nuevos", "actualizados", "a_mano", "retirados", "retirados_a_mano", "filas_quitadas", "fichas", "sin_aplicar", "claves_escritas"):
            self.assertEqual(sim[clave], real[clave], clave)


class TestCorteAMediaEscritura(Base):
    """Spec 021: un corte deja cada archivo viejo o nuevo entero, y al relanzar se completa."""

    def test_si_falla_la_escritura_el_archivo_sigue_entero_y_sin_temporales(self):
        ruta = os.path.join(self.proy, "a.txt")
        act.escribir_atomico(ruta, b"viejo")
        with mock.patch.object(act.os, "replace", side_effect=OSError("corte")):
            with self.assertRaises(OSError):
                act.escribir_atomico(ruta, b"nuevo")
        self.assertEqual(act.leer_bytes(ruta), b"viejo")
        self.assertEqual(os.listdir(self.proy), ["a.txt"])

    @unittest.skipIf(os.name == "nt", "los permisos de ejecución no existen en Windows")
    def test_conserva_los_permisos_del_archivo(self):
        ruta = os.path.join(self.proy, "a.command")
        act.escribir_atomico(ruta, b"v1")
        os.chmod(ruta, 0o755)
        act.escribir_atomico(ruta, b"v2")
        self.assertEqual(os.stat(ruta).st_mode & 0o777, 0o755)

    def test_corte_a_mitad_de_la_copia_y_relanzar_completa_sin_marcar_a_mano(self):
        act.sincronizar(self.repo, self.proy)
        self.poner_repo({".brain/guardianes/uno.py": "# uno v2\n", ".claude/skills/s/SKILL.md": "skill v2\n"}, "1.1.0")
        real, llamadas = os.replace, []

        def cortar(origen, destino):
            llamadas.append(destino)
            if len(llamadas) == 2:
                raise OSError("corte")
            real(origen, destino)

        with mock.patch.object(act.os, "replace", side_effect=cortar):
            with self.assertRaises(OSError):
                act.sincronizar(self.repo, self.proy)
        self.assertEqual(act.cargar_registro(self.proy)["version"], "1.0.0", "a medias no se anota la versión nueva")
        res = act.sincronizar(self.repo, self.proy)
        self.assertEqual(res["a_mano"], [])
        self.assertEqual(leer(self.proy, ".brain/guardianes/uno.py"), "# uno v2\n")
        self.assertEqual(leer(self.proy, ".claude/skills/s/SKILL.md"), "skill v2\n")
        self.assertEqual(act.cargar_registro(self.proy)["version"], "1.1.0")


class TestVersionHonesta(Base):
    def test_lo_que_se_queda_viejo_queda_anotado_y_se_dice(self):
        act.sincronizar(self.repo, self.proy)
        self.assertEqual(act.cargar_registro(self.proy)["sin_aplicar"], [])
        escribir(self.proy, ".claude/skills/s/SKILL.md", "mío\n")
        self.poner_repo({".claude/skills/s/SKILL.md": "skill v2\n"}, "1.1.0")
        res = act.sincronizar(self.repo, self.proy)
        r = act.cargar_registro(self.proy)
        self.assertEqual((r["version"], r["sin_aplicar"]), ("1.1.0", [".claude/skills/s/SKILL.md"]))
        self.assertIn("1.1.0 aplicada salvo 1 archivo", act.informe(res, False))
        act.sincronizar(self.repo, self.proy, forzar=[".claude/skills/s/SKILL.md"])
        self.assertEqual(act.cargar_registro(self.proy)["sin_aplicar"], [])


class TestHuellaDelManifiesto(Base):
    def test_huella_falsa_para_sin_escribir_nada(self):
        escribir(self.repo, ".claude/skills/s/SKILL.md", "cambiado sin regenerar\n")
        antes = arbol(self.proy)
        with self.assertRaises(ValueError) as e:
            act.sincronizar(self.repo, self.proy)
        self.assertIn(".claude/skills/s/SKILL.md", str(e.exception))
        self.assertEqual(arbol(self.proy), antes)

    def test_archivo_del_manifiesto_que_falta_en_el_repo(self):
        os.remove(os.path.join(self.repo, ".claude", "skills", "s", "SKILL.md"))
        with self.assertRaises(ValueError):
            act.sincronizar(self.repo, self.proy)

    def test_el_programa_lo_explica_con_error(self):
        escribir(self.proy, ".brain/guardianes/guardianes.json", "{}")
        escribir(self.repo, ".claude/skills/s/SKILL.md", "cambiado\n")
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            codigo = act.main([self.proy, "--simular"], repo=self.repo)
        self.assertEqual(codigo, 2)
        self.assertIn("generar_manifiesto", salida.getvalue())


class TestNivel(Base):
    """Spec 021 (punto 14): en un proyecto sin guardianes el actualizador no copia nada."""

    def correr(self, *args):
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            codigo = act.main([self.proy] + list(args), repo=self.repo)
        return codigo, salida.getvalue()

    def test_nivel_medio_no_copia_nada_y_explica_como_subir(self):
        escribir(self.proy, ".brain/arnes_instalado.json", json.dumps({"nivel": "medio", "archivos": {}}))
        antes = arbol(self.proy)
        codigo, texto = self.correr()
        self.assertEqual(codigo, 0)
        self.assertIn("medio", texto)
        self.assertIn("--nivel completo", texto)
        self.assertEqual(arbol(self.proy), antes)

    def test_nivel_medio_tampoco_con_forzar_todo(self):
        escribir(self.proy, ".brain/arnes_instalado.json", json.dumps({"nivel": "medio", "archivos": {}}))
        antes = arbol(self.proy)
        self.assertIn("--nivel completo", self.correr("--forzar-todo")[1])
        self.assertEqual(arbol(self.proy), antes)

    def test_proyecto_antiguo_sin_nivel_ni_guardianes_no_copia(self):
        escribir(self.proy, ".brain/pendientes.md", "p")
        antes = arbol(self.proy)
        self.assertIn("--nivel completo", self.correr()[1])
        self.assertEqual(arbol(self.proy), antes)

    def test_proyecto_antiguo_sin_guardianes_se_adopta_con_forzar_todo(self):
        codigo, _ = self.correr("--forzar-todo", "--sin-pruebas")
        self.assertEqual(codigo, 0)
        self.assertTrue(os.path.isfile(os.path.join(self.proy, ".claude", "skills", "s", "SKILL.md")))
        self.assertEqual(act.cargar_registro(self.proy)["nivel"], "completo")

    def test_nivel_completo_y_proyecto_con_guardianes_si_actualizan(self):
        escribir(self.proy, ".brain/guardianes/guardianes.json", "{}")
        self.assertEqual(self.correr("--sin-pruebas")[0], 0)
        self.assertEqual(act.cargar_registro(self.proy)["nivel"], "completo")
        self.assertTrue(os.path.isfile(os.path.join(self.proy, ".claude", "skills", "s", "SKILL.md")))

    def test_el_kit_anota_el_nivel_y_al_subir_a_completo_cambia(self):
        proy = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, proy, True)
        kit.instalar(proy, "Demo", "Ana", "español", "x", ["claude"], "medio", hoy="2026-01-01")
        r = act.cargar_registro(proy)
        self.assertEqual((r["nivel"], r["dueno"]), ("medio", "Ana"))
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            act.main([proy, "--simular"], repo=RAIZ)
        self.assertIn("--nivel completo", salida.getvalue())
        kit.instalar(proy, "Demo", "Ana", "español", "x", ["claude"], "completo", hoy="2026-01-01")
        self.assertEqual(act.cargar_registro(proy)["nivel"], "completo")

    def test_el_kit_con_manifiesto_desfasado_no_empieza(self):
        proy = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, proy, True)
        with mock.patch.object(kit, "comprobar_arnes", side_effect=ValueError("desfasado")):
            with self.assertRaises(ValueError):
                kit.instalar(proy, "Demo", "Ana", "español", "x", ["claude"], "completo", hoy="2026-01-01")
        self.assertEqual(os.listdir(proy), [])


class TestGenerarManifiesto(unittest.TestCase):
    def test_lista_de_retirados(self):
        espec = importlib.util.spec_from_file_location("generar_manifiesto", os.path.join(RAIZ, "generar_manifiesto.py"))
        gen = importlib.util.module_from_spec(espec)
        espec.loader.exec_module(gen)
        previo = {"archivos": {"a.py": "1", "b.py": "2"}, "retirados": ["c.py", "d.py"]}
        res = gen.calcular_retirados(["a.py", "d.py"], previo)  # b.py se va, d.py vuelve
        self.assertEqual(set(res) - set(gen.RETIRADOS_HISTORICOS), {"b.py", "c.py"})
        self.assertEqual(res, sorted(res))
        with open(os.path.join(RAIZ, "manifiesto.json"), encoding="utf-8") as f:
            m = json.load(f)
        self.assertIn(".claude/skills/traspaso-entre-chats/SKILL.md", m["retirados"])
        self.assertFalse(set(m["retirados"]) & set(m["archivos"]), "un archivo no puede repartirse y estar retirado a la vez")


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
