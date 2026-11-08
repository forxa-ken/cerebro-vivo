# -*- coding: utf-8 -*-
"""Guardián 14 (spec 027): guardián con memoria del chat; la red se simula, no hay llamadas reales."""
import importlib.util
import json
import os
import sys
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GUARD = os.path.join(RAIZ, ".brain", "guardianes")
sys.path.insert(0, GUARD)
_espec = importlib.util.spec_from_file_location("eventos_chat", os.path.join(GUARD, "eventos_chat.py"))
ev = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(ev)

CFG = {"eventos_chat_activo": True, "eventos_chat_bloquear": True, "eventos_chat_sin_red_bloquear": False,
       "eventos_chat_comandos": ev.COMANDOS, "idioma": "es", "registro": "registro.log", "librerias": {"requisitos": "requirements.txt"}}


def red(vulnerables=(), caida=False):
    def http(url, datos=None, timeout=7):
        if caida:
            raise OSError("sin red")
        if url == ev.librerias.OSV_LOTE:
            return {"results": [{"vulns": [{"id": "GHSA-x"}]} if q["package"]["name"] in vulnerables else {} for q in datos["queries"]]}
        return {"summary": "fallo de prueba", "affected": [{"ranges": [{"events": [{"fixed": "9.9"}]}]}]}
    return http


class Base(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.estado_original, self.version_original = ev.ESTADO, ev.librerias.version_instalada
        ev.ESTADO = os.path.join(self.dir, "estado.json")
        ev.librerias.version_instalada = lambda nombre, minima: "1.0.0"

    def tearDown(self):
        ev.ESTADO, ev.librerias.version_instalada = self.estado_original, self.version_original

    def orden(self, comando, sesion="s1", cfg=None, http=None, herramienta="Bash"):
        datos = {"session_id": sesion, "tool_name": herramienta, "tool_input": {"command": comando}}
        return ev.procesar(datos, cfg or CFG, self.dir, http or red())


class TestDeteccion(unittest.TestCase):
    def test_detecta_instalaciones_de_varios_ecosistemas(self):
        self.assertEqual(ev.instalaciones("python -m pip install requests==2.0 flask[async]>=3 --upgrade", CFG), [("pypi", ["requests", "flask"], "")])
        self.assertEqual(ev.instalaciones("npm install @scope/pkg@1.2 left-pad", CFG), [("npm", ["@scope/pkg", "left-pad"], "")])
        self.assertEqual(ev.instalaciones("cd x && uv add rich; cargo add serde", CFG), [("pypi", ["rich"], ""), ("cargo", ["serde"], "")])

    def test_requirements_y_orden_sin_instalar(self):
        self.assertEqual(ev.instalaciones("pip install -r requirements.txt", CFG), [("pypi", [], "requirements.txt")])
        self.assertEqual(ev.instalaciones("pip list && git status", CFG), [])

    def test_detecta_git_push(self):
        self.assertTrue(ev.es_push("git push origin main"))
        self.assertTrue(ev.es_push("git -C repo push"))
        self.assertFalse(ev.es_push("git status"))
        self.assertFalse(ev.es_push("echo git push"))


class TestGuardian(Base):
    def test_instala_y_sube_limpio_pasa_en_silencio(self):
        self.assertEqual(self.orden("pip install requests"), (0, ""))
        self.assertEqual(self.orden("git push"), (0, ""))
        self.assertEqual(self.orden("git push"), (0, ""))  # ya revisado: no vuelve a consultar

    def test_instala_y_sube_con_vulnerabilidad_para(self):
        self.orden("pip install viejo")
        codigo, texto = self.orden("git push origin main", http=red(vulnerables=("viejo",)))
        self.assertEqual(codigo, 2)
        self.assertIn("viejo", texto)
        self.assertIn("9.9", texto)
        self.assertIn("permitir", texto)

    def test_push_sin_instalacion_calla(self):
        self.assertEqual(self.orden("git push", http=red(caida=True)), (0, ""))

    def test_sin_red_no_bloquea_y_lo_recuerda(self):
        self.orden("pip install requests")
        codigo, texto = self.orden("git push", http=red(caida=True))
        self.assertEqual(codigo, 0)
        self.assertIn("requests", texto)
        codigo, texto = self.orden("git push", http=red(caida=True))  # sigue sin revisar: lo repite
        self.assertIn("requests", texto)
        self.assertEqual(self.orden("git push"), (0, ""))  # con red revisa y calla

    def test_sin_red_puede_bloquear_si_se_pide(self):
        self.orden("pip install requests")
        cfg = dict(CFG, eventos_chat_sin_red_bloquear=True)
        self.assertEqual(self.orden("git push", cfg=cfg, http=red(caida=True))[0], 2)

    def test_otro_ecosistema_avisa_una_sola_vez(self):
        self.orden("npm install left-pad")
        codigo, texto = self.orden("git push")
        self.assertEqual(codigo, 0)
        self.assertIn("npm:left-pad", texto)
        self.assertEqual(self.orden("git push"), (0, ""))

    def test_bloqueo_apagado_solo_avisa(self):
        self.orden("pip install viejo")
        codigo, texto = self.orden("git push", cfg=dict(CFG, eventos_chat_bloquear=False), http=red(vulnerables=("viejo",)))
        self.assertEqual(codigo, 0)
        self.assertIn("viejo", texto)

    def test_guardian_apagado_no_hace_nada(self):
        cfg = dict(CFG, eventos_chat_activo=False)
        self.orden("pip install viejo", cfg=cfg)
        self.assertEqual(self.orden("git push", cfg=cfg, http=red(vulnerables=("viejo",))), (0, ""))

    def test_cada_chat_tiene_su_memoria(self):
        self.orden("pip install viejo", sesion="a")
        self.assertEqual(self.orden("git push", sesion="b", http=red(vulnerables=("viejo",))), (0, ""))
        self.assertEqual(self.orden("git push", sesion="a", http=red(vulnerables=("viejo",)))[0], 2)

    def test_cambio_en_requirements_cuenta_como_nuevo(self):
        ruta = os.path.join(self.dir, "requirements.txt")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("flask\n")
        self.orden("ls", herramienta="Edit")  # primera vez que lo ve: toma la base
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("flask\nviejo\n")
        self.assertEqual(self.orden("git push", http=red(vulnerables=("viejo",)))[0], 2)

    def test_error_interno_deja_pasar(self):
        import io
        original, entrada, argumentos = ev.procesar, sys.stdin, sys.argv
        ev.procesar = lambda *a, **k: 1 / 0
        sys.stdin, sys.argv = io.StringIO("{}"), ["eventos_chat.py"]  # el hook se llama sin argumentos
        try:
            self.assertEqual(ev.main(), 0)
        finally:
            ev.procesar, sys.stdin, sys.argv = original, entrada, argumentos


class TestPermitir(Base):
    def test_permitir_deja_pasar_solo_esas_librerias_y_queda_en_el_registro(self):
        self.orden("pip install viejo otra")
        self.assertEqual(self.orden("git push", http=red(vulnerables=("viejo",)))[0], 2)
        texto = ev.permitir("Darwin lo aprobó en el chat", self.dir, CFG)
        self.assertIn("viejo==1.0.0", texto)
        self.assertEqual(self.orden("git push", http=red(vulnerables=("viejo",))), (0, ""))
        with open(os.path.join(self.dir, "registro.log"), encoding="utf-8") as f:
            self.assertIn("Darwin lo aprobó", f.read())
        self.orden("pip install nueva")  # otra librería con problema sigue bloqueando
        self.assertEqual(self.orden("git push", http=red(vulnerables=("nueva",)))[0], 2)

    def test_permitir_sin_bloqueo_no_hace_nada(self):
        self.assertIn("No hay", ev.permitir("x", self.dir, CFG))


class TestIngles(Base):
    def test_mensaje_en_ingles(self):
        import textos
        original = textos.idioma_del_proyecto
        textos.idioma_del_proyecto = lambda: "en"
        try:
            self.orden("pip install viejo")
            codigo, texto = self.orden("git push", http=red(vulnerables=("viejo",)))
        finally:
            textos.idioma_del_proyecto = original
        self.assertEqual(codigo, 2)
        self.assertIn("git push stopped", texto)


if __name__ == "__main__":
    unittest.main()
