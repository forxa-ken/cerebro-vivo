"""El resumen de arranque lanzado a mano (--manual) no debe quedarse esperando el teclado."""
import json
import os
import importlib.util
import subprocess
import sys
import tempfile
import time
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(RAIZ, ".brain", "guardianes", "arranque.py")


def _indices():
    """Índices de entrada que el proyecto tiene (CLAUDE.md, GEMINI.md, AGENTS.md)."""
    return [n for n in ("CLAUDE.md", "GEMINI.md", "AGENTS.md") if os.path.exists(os.path.join(RAIZ, n))]


class ArranqueManualTest(unittest.TestCase):
    def test_manual_no_espera_stdin(self):
        # stdin abierto y sin cerrar, como en una consola de Gemini/Codex
        p = subprocess.Popen([sys.executable, SCRIPT, "--manual"], stdin=subprocess.PIPE, env=dict(os.environ, CEREBRO_NO_ARCHIVAR_TRASPASO="1"),
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            p.wait(timeout=60)  # sin communicate(): este cerraría stdin y taparía el bloqueo
            salida = p.stdout.read()
        finally:
            p.stdout.close()
            p.stdin.close()
            if p.poll() is None:
                p.kill()
        datos = json.loads(salida.decode("utf-8"))
        self.assertIn("additionalContext", datos["hookSpecificOutput"])


def _cargar_arranque():
    espec = importlib.util.spec_from_file_location("arranque_078", SCRIPT)
    modulo = importlib.util.module_from_spec(espec)
    espec.loader.exec_module(modulo)
    return modulo


class TraspasoTest(unittest.TestCase):
    """Spec 078: el chat nuevo recibe el traspaso del anterior."""

    def setUp(self):
        self.a = _cargar_arranque()
        self.tmp = tempfile.TemporaryDirectory()
        self.raiz = self.tmp.name
        os.makedirs(os.path.join(self.raiz, ".brain"))
        self.ruta = os.path.join(self.raiz, ".brain", "traspaso.md")

    def tearDown(self):
        self.tmp.cleanup()

    def _escribir(self, texto):
        with open(self.ruta, "w", encoding="utf-8") as f:
            f.write(texto)

    def test_sin_traspaso_no_cambia_nada(self):
        self.assertEqual(self.a.leer_traspaso(self.raiz), [])
        self.assertIsNone(self.a.archivar_traspaso(self.raiz))

    def test_traspaso_se_muestra_y_se_archiva(self):
        self._escribir("Darwin dijo: «hazlo así»")
        lineas = self.a.leer_traspaso(self.raiz)
        self.assertIn("Darwin dijo", "\n".join(lineas))
        destino = self.a.archivar_traspaso(self.raiz)
        self.assertTrue(os.path.isfile(destino))
        self.assertFalse(os.path.exists(self.ruta))
        self.assertEqual(self.a.leer_traspaso(self.raiz), [])

    def test_vacio_o_antiguo_se_ignora(self):
        self._escribir("   \n")
        self.assertEqual(self.a.leer_traspaso(self.raiz), [])
        self._escribir("algo")
        self.assertEqual(self.a.leer_traspaso(self.raiz, ahora=time.time() + 4 * 86400), [])

    def test_texto_muy_largo_se_recorta(self):
        self._escribir("x" * 20000)
        texto = "\n".join(self.a.leer_traspaso(self.raiz))
        self.assertLess(len(texto), 7000)
        self.assertIn("recortado", texto)

    def test_reglas_y_plantilla_existen(self):
        for nombre in _indices():
            with open(os.path.join(RAIZ, nombre), encoding="utf-8") as f:
                self.assertIn(".brain/traspaso.md", f.read(), nombre)
        self.assertTrue(os.path.isfile(os.path.join(RAIZ, ".brain", "biblioteca", "PLANTILLA_TRASPASO.md")))


class PluginsRequeridosTest(unittest.TestCase):
    """Spec 085: aviso si falta un plugin del meta-arnés."""

    def setUp(self):
        self.a = _cargar_arranque()
        self.tmp = tempfile.TemporaryDirectory()
        self.ruta = os.path.join(self.tmp.name, "installed_plugins.json")

    def tearDown(self):
        self.tmp.cleanup()

    def _escribir(self, plugins):
        with open(self.ruta, "w", encoding="utf-8") as f:
            json.dump({"version": 2, "plugins": plugins}, f)

    def test_instalado_no_avisa(self):
        self._escribir({"p@m": [{"scope": "user"}]})
        self.assertEqual(self.a.plugins_que_faltan({"plugins_requeridos": ["p@m"]}, self.ruta), [])

    def test_no_instalado_avisa(self):
        self._escribir({})
        self.assertEqual(self.a.plugins_que_faltan({"plugins_requeridos": ["p@m"]}, self.ruta), ["p@m"])

    def test_sin_lista_o_sin_archivo_calla(self):
        self.assertEqual(self.a.plugins_que_faltan({}, self.ruta), [])
        self.assertEqual(self.a.plugins_que_faltan({"plugins_requeridos": ["p@m"]}, self.ruta), [])


class NotasChatsTest(unittest.TestCase):
    """Spec 080: el chat principal ve las notas que dejaron los chats auxiliares."""

    def setUp(self):
        self.a = _cargar_arranque()
        self.tmp = tempfile.TemporaryDirectory()
        self.raiz = self.tmp.name
        self.carpeta = os.path.join(self.raiz, ".brain", "notas-chats")
        os.makedirs(self.carpeta)

    def tearDown(self):
        self.tmp.cleanup()

    def _nota(self, nombre, texto):
        ruta = os.path.join(self.carpeta, nombre)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(texto)
        return ruta

    def test_sin_notas_no_cambia_nada(self):
        self.assertEqual(self.a.leer_notas_chats(self.raiz), [])
        self.assertEqual(self.a.archivar_notas_chats(self.raiz), [])

    def test_notas_se_muestran_y_se_archivan(self):
        self._nota("a.md", "Hice X")
        self._nota("b.md", "Hice Y")
        texto = "\n".join(self.a.leer_notas_chats(self.raiz))
        self.assertIn("Hice X", texto)
        self.assertIn("Hice Y", texto)
        movidas = self.a.archivar_notas_chats(self.raiz)
        self.assertEqual(len(movidas), 2)
        self.assertTrue(all(os.path.isfile(m) for m in movidas))
        self.assertEqual(self.a.leer_notas_chats(self.raiz), [])

    def test_nota_antigua_o_vacia_no_se_muestra(self):
        self._nota("vacia.md", "  \n")
        self.assertEqual(self.a.leer_notas_chats(self.raiz), [])
        self._nota("vieja.md", "algo")
        self.assertEqual(self.a.leer_notas_chats(self.raiz, ahora=time.time() + 4 * 86400), [])

    def test_reglas_y_plantilla_existen(self):
        for nombre in _indices():
            with open(os.path.join(RAIZ, nombre), encoding="utf-8") as f:
                self.assertIn(".brain/notas-chats/", f.read(), nombre)
        self.assertTrue(os.path.isfile(os.path.join(RAIZ, ".brain", "biblioteca", "PLANTILLA_NOTA_CHAT.md")))


if __name__ == "__main__":
    unittest.main()


class NotasAbiertasTest(unittest.TestCase):
    """Spec 081: el chat ya abierto recibe cada nota nueva una sola vez."""

    def setUp(self):
        espec = importlib.util.spec_from_file_location("notas_abiertas", os.path.join(RAIZ, ".brain", "guardianes", "notas_abiertas.py"))
        self.m = importlib.util.module_from_spec(espec)
        espec.loader.exec_module(self.m)
        self.tmp = tempfile.TemporaryDirectory()
        self.raiz = self.tmp.name
        self.carpeta = os.path.join(self.raiz, ".brain", "notas-chats")
        os.makedirs(self.carpeta)

    def tearDown(self):
        self.tmp.cleanup()

    def _nota(self, nombre, texto="# Nota\n- Hecho: algo"):
        with open(os.path.join(self.carpeta, nombre), "w", encoding="utf-8") as f:
            f.write(texto)

    def test_sin_notas_o_sin_carpeta_no_imprime(self):
        self.assertEqual(self.m.avisar(self.raiz, "s1"), [])
        self.assertEqual(self.m.avisar(os.path.join(self.raiz, "no-existe"), "s1"), [])

    def test_avisa_una_vez_y_no_repite(self):
        self._nota("a.md")
        self.assertIn("algo", "\n".join(self.m.avisar(self.raiz, "s1")))
        self.assertEqual(self.m.avisar(self.raiz, "s1"), [])
        self._nota("b.md")
        self.assertIn("b.md", "\n".join(self.m.avisar(self.raiz, "s1")))

    def test_cada_chat_recibe_la_suya_y_no_mueve_archivos(self):
        self._nota("a.md")
        self.assertTrue(self.m.avisar(self.raiz, "s1"))
        self.assertTrue(self.m.avisar(self.raiz, "s2"))
        self.assertTrue(os.path.exists(os.path.join(self.carpeta, "a.md")))

    def test_nota_ilegible_o_estado_roto_no_rompe_y_respeta_tope(self):
        with open(os.path.join(self.carpeta, ".avisadas.json"), "w") as f:
            f.write("{roto")
        self._nota("a.md", "x" * 5000)
        salida = "\n".join(self.m.avisar(self.raiz, "s1"))
        self.assertLess(len(salida), 1000)


class HookCodexTest(unittest.TestCase):
    """Spec 081 para Codex: `.codex/hooks.json` llama al mismo script que Claude Code (sin comprobar en vivo)."""

    @unittest.skipUnless(os.path.exists(os.path.join(RAIZ, ".codex", "hooks.json")), "el proyecto no usa Codex")
    def test_codex_hooks_apunta_al_script_de_notas(self):
        with open(os.path.join(RAIZ, ".codex", "hooks.json"), encoding="utf-8") as f:
            datos = json.load(f)
        comando = datos["hooks"]["UserPromptSubmit"][0]["hooks"][0]["command"]
        self.assertIn("notas_abiertas.py", comando)
        self.assertTrue(os.path.exists(os.path.join(RAIZ, ".brain", "guardianes", "notas_abiertas.py")))


class NotasAntigravityTest(NotasAbiertasTest):
    """Spec 082: el mismo aviso para Antigravity (PreInvocation, conversationId, injectSteps)."""

    def test_primera_llamada_avisa_en_json_con_inject_steps(self):
        self._nota("a.md")
        out = self.m.salida({"conversationId": "c1", "invocationNum": 1}, self.raiz)
        datos = json.loads(out)
        self.assertIn("algo", datos["injectSteps"][0]["ephemeralMessage"])

    def test_llamadas_siguientes_callan_y_no_gastan_la_nota(self):
        self._nota("a.md")
        self.assertEqual(self.m.salida({"conversationId": "c1", "invocationNum": 2}, self.raiz), "")
        self.assertTrue(self.m.salida({"conversationId": "c1", "invocationNum": 1}, self.raiz))
        self.assertEqual(self.m.salida({"conversationId": "c1", "invocationNum": 1}, self.raiz), "")

    def test_sin_notas_no_imprime_y_claude_sigue_en_texto(self):
        self.assertEqual(self.m.salida({"conversationId": "c1", "invocationNum": 1}, self.raiz), "")
        self._nota("a.md")
        out = self.m.salida({"session_id": "s1"}, self.raiz)
        self.assertTrue(out.startswith("NOTA NUEVA"))

    @unittest.skipUnless(os.path.exists(os.path.join(RAIZ, ".agents", "hooks.json")), "el proyecto no usa Antigravity")
    def test_agents_hooks_apunta_al_script(self):
        with open(os.path.join(RAIZ, ".agents", "hooks.json"), encoding="utf-8") as f:
            datos = json.load(f)
        comando = datos["guardia-notas"]["PreInvocation"][0]["command"]
        self.assertIn("notas_abiertas.py", comando)

