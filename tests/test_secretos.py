# -*- coding: utf-8 -*-
"""Guardián 9 (spec 051): secretos en el código, archivos secretos ignorados y hook pre-commit."""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GUARDIAN = os.path.join(RAIZ, ".brain", "guardianes", "secretos.py")
_espec = importlib.util.spec_from_file_location("secretos", GUARDIAN)
secretos = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(secretos)
CFG = secretos.cargar_config()
A = secretos.ajustes(CFG)

# Falsos tokens armados al ejecutar: el código fuente no contiene ningún secreto con formato real
FALSOS = {
    "token de bot de Discord": "M" + "A" * 23 + "." + "B" * 6 + "." + "C" * 27,
    "clave de Google/Gemini": "AIza" + "Z" * 35,
    "token de GitHub": "ghp_" + "a1" * 20,
    "clave sk-": "sk_live_" + "q" * 30,
    "token de Slack": "xoxb-" + "1234567890" * 2,
    "llave privada": "-----BEGIN " + "RSA PRIVATE KEY-----",
    "webhook de Discord": "https://discord.com/api/webhooks/" + "1" * 18 + "/" + "w" * 64,
}


def hallar(texto, archivo="x.py"):
    return secretos.escanear_texto(texto, archivo, A)


class TestPatrones(unittest.TestCase):
    def test_detecta_cada_tipo_de_secreto(self):
        for nombre, valor in FALSOS.items():
            hs = hallar("clave = %s\n" % valor)
            self.assertTrue(any(h[2] == nombre and h[3] == "alta" for h in hs), nombre)

    def test_nunca_devuelve_el_secreto_entero(self):
        for valor in FALSOS.values():
            for h in hallar(valor):
                self.assertLessEqual(len(h[4]), 4)

    def test_asignacion_sospechosa_es_de_baja_confianza(self):
        hs = hallar('api_key = "' + "k" * 30 + '"\n')
        self.assertTrue(hs and hs[0][3] == "baja")

    def test_casos_limpios_callan(self):
        limpios = ["x = 1\n", 'GEMINI_API_KEY=""\n', 'token = os.environ.get("DISCORD_BOT_TOKEN")\n',
                   'api_key = "TU_CLAVE_AQUI_RELLENA_ESTO_1234"\n',
                   '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAloAAABpCAYAAADiKo3' + FALSOS["clave de Google/Gemini"] + '">\n']
        for t in limpios:
            self.assertEqual(hallar(t), [], t[:40])

    def test_permitido_con_motivo_calla(self):
        a = dict(A, permitidos=[{"archivo": "x.py", "contiene": "gh" + "p_", "motivo": "prueba"}])
        self.assertEqual(secretos.escanear_texto(FALSOS["token de GitHub"], "x.py", a), [])


class TestRepositorioReal(unittest.TestCase):
    def test_codigo_subido_sin_secretos(self):
        hallazgos, problemas = secretos.analizar(RAIZ, CFG)
        self.assertEqual([secretos._formato(h) for h in hallazgos], [])
        self.assertEqual(problemas, [])

    def test_archivos_secretos_ignorados_y_no_subidos(self):
        self.assertEqual(secretos.problemas_archivos_secretos(RAIZ, A), [])

    def test_puede_fallar_si_un_secreto_no_esta_ignorado(self):
        a = dict(A, archivos_secretos=["README.md"])  # README.md está subido a Git
        self.assertTrue(secretos.problemas_archivos_secretos(RAIZ, a))


class TestHook(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="lobo_t051_")
        self.addCleanup(shutil.rmtree, self.d, ignore_errors=True)
        subprocess.run(["git", "init", "-q"], cwd=self.d, check=True)

    def preparar(self, nombre, texto):
        with open(os.path.join(self.d, nombre), "w", encoding="utf-8") as f:
            f.write(texto)
        subprocess.run(["git", "add", nombre], cwd=self.d, check=True)

    def correr(self):
        return subprocess.run([sys.executable, GUARDIAN, "--staged"], cwd=self.d, capture_output=True,
                              text=True, encoding="utf-8")

    def test_bloquea_secreto_y_no_lo_imprime_entero(self):
        self.preparar("a.py", "T = '%s'\n" % FALSOS["token de bot de Discord"])
        r = self.correr()
        self.assertEqual(r.returncode, 1)
        self.assertIn("COMMIT BLOQUEADO", r.stderr)
        self.assertNotIn(FALSOS["token de bot de Discord"], r.stderr + r.stdout)

    def test_bloquea_archivo_secreto_preparado(self):
        self.preparar(A["archivos_secretos"][0], "{}\n")
        self.assertEqual(self.correr().returncode, 1)

    def test_deja_pasar_commit_limpio_y_baja_confianza(self):
        self.preparar("b.py", "x = 1\napi_key = \"%s\"\n" % ("k" * 30))
        self.assertEqual(self.correr().returncode, 0)

    def test_hook_instalado_apunta_al_guardian(self):
        os.makedirs(os.path.join(self.d, ".git", "hooks"), exist_ok=True)
        self.assertIn("Hook instalado", secretos.instalar_hook(self.d))
        with open(os.path.join(self.d, ".git", "hooks", "pre-commit"), encoding="utf-8") as f:
            contenido = f.read()
            self.assertIn("secretos.py", contenido)
            self.assertIn("git-common-dir", contenido)

    def test_el_hook_funciona_desde_un_worktree_sin_el_guardian(self):
        """Punto 38: en un worktree no existe .brain/; el hook debe hallar el guardián en el repo principal y bloquear."""
        def git(cwd, *a):
            return subprocess.run(["git"] + list(a), cwd=cwd, capture_output=True, text=True, encoding="utf-8")
        if git(self.d, "init").returncode != 0:
            self.skipTest("git no disponible")
        gd = os.path.join(self.d, ".brain", "guardianes")
        os.makedirs(gd, exist_ok=True)
        for n in ("secretos.py", "textos.py", "guardianes.json"):
            shutil.copy(os.path.join(RAIZ, ".brain", "guardianes", n), gd)
        secretos.instalar_hook(self.d)
        git(self.d, "config", "user.email", "t@t"); git(self.d, "config", "user.name", "t")
        git(self.d, "add", "-A"); git(self.d, "commit", "--no-verify", "-m", "base")
        wt = self.d + "_wt"
        self.addCleanup(shutil.rmtree, wt, True)
        if git(self.d, "worktree", "add", "-b", "pag", wt).returncode != 0:
            self.skipTest("worktree no disponible")
        shutil.rmtree(os.path.join(wt, ".brain"), True)
        with open(os.path.join(wt, "x.py"), "w", encoding="utf-8") as f:
            f.write("clave = %s\n" % FALSOS["token de GitHub"])
        git(wt, "add", "x.py")
        r = git(wt, "commit", "-m", "con secreto")
        self.assertNotEqual(r.returncode, 0)
        self.assertNotIn("No such file", r.stderr)
        self.assertNotIn("no encontrado", r.stderr)
        os.remove(os.path.join(wt, "x.py")); git(wt, "rm", "--cached", "-q", "x.py")
        with open(os.path.join(wt, "ok.txt"), "w", encoding="utf-8") as f:
            f.write("hola\n")
        git(wt, "add", "ok.txt")
        self.assertEqual(git(wt, "commit", "-m", "limpio").returncode, 0)

    def test_apagado_no_habla(self):
        self.assertEqual(secretos.resumen(RAIZ, {"secretos_activo": False}), [])


class TestAvisoPeriodico(unittest.TestCase):
    def test_avisa_si_el_historial_no_se_revisa_hace_tiempo(self):
        original = secretos.dias_desde_historial
        try:
            secretos.dias_desde_historial = lambda: 99
            self.assertTrue(any("historial" in l for l in secretos.resumen(RAIZ, CFG)))
            secretos.dias_desde_historial = lambda: 1
            self.assertFalse(any("historial" in l for l in secretos.resumen(RAIZ, CFG)))
        finally:
            secretos.dias_desde_historial = original


class TestClaudeNoLeeSecretos(unittest.TestCase):
    def test_cada_archivo_secreto_tiene_regla_de_no_lectura(self):
        with open(os.path.join(RAIZ, ".claude", "settings.json"), encoding="utf-8") as f:
            deny = json.load(f).get("permissions", {}).get("deny", [])
        for nombre in A["archivos_secretos"]:
            self.assertIn("Read(./%s)" % nombre, deny, "Claude podría leer %s" % nombre)


if __name__ == "__main__":
    unittest.main()
