# -*- coding: utf-8 -*-
"""Guardián 12 (spec 056): aviso de longitud de chat, una vez por tramo."""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GUARDIANES = os.path.join(RAIZ, ".brain", "guardianes")
_espec = importlib.util.spec_from_file_location("longitud", os.path.join(GUARDIANES, "longitud.py"))
lg = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(lg)
A = {"activo": True, "aviso": 200000, "repetir": 100000}
CFG = {"longitud_activa": True, "longitud_aviso_tokens": 200000, "longitud_repetir_tokens": 100000}


def registro(*contextos, ruta=None, nombre="chat-1.jsonl"):
    """Registro de chat de ejemplo: un mensaje de la IA por contexto (repartido entre entrada y cachés)."""
    ruta = ruta or os.path.join(tempfile.mkdtemp(), nombre)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(json.dumps({"type": "user", "message": {"content": "hola"}}) + "\n")
        for i, c in enumerate(contextos):
            uso = {"input_tokens": 10, "cache_creation_input_tokens": 90, "cache_read_input_tokens": c - 100}
            f.write(json.dumps({"type": "assistant", "message": {"id": "m%d" % i, "usage": uso}}) + "\n")
        f.write("esto no es json\n")
    return ruta


class TestLongitud(unittest.TestCase):
    def setUp(self):
        self.original = lg.ESTADO
        lg.ESTADO = os.path.join(tempfile.mkdtemp(), "estado.json")

    def tearDown(self):
        lg.ESTADO = self.original

    def test_mide_el_ultimo_mensaje(self):
        self.assertEqual(lg.contexto_actual(registro(50000, 120000)), 120000)

    def test_tramos(self):
        self.assertEqual([lg.tramo(c, A) for c in (199999, 200000, 299999, 300000, 451000)], [0, 1, 1, 2, 3])

    def test_avisa_una_vez_por_tramo(self):
        ruta = registro(250000)
        texto = lg.aviso(ruta, CFG)
        self.assertIn("250k", texto)
        self.assertIn("traspaso.md", texto)
        self.assertIn("start_session", texto)  # spec 012: abre el chat nuevo...
        self.assertIn("detach_session", texto)  # ...y lo deja al mismo nivel
        self.assertIn("traspaso-in entro", texto)  # si se abre por tarjeta, se separa él al entrar
        self.assertIsNone(lg.aviso(ruta, CFG))  # siguiente respuesta en el mismo tramo: no repite
        registro(250000, 310000, ruta=ruta)  # el mismo chat crece y pasa al tramo siguiente
        self.assertIn("310k", lg.aviso(ruta, CFG))
        self.assertIsNone(lg.aviso(ruta, CFG))

    def test_no_avisa_por_debajo_del_umbral(self):
        self.assertIsNone(lg.aviso(registro(120000), CFG))
        self.assertFalse(os.path.exists(lg.ESTADO))

    def test_apagado_o_registro_roto_callan(self):
        self.assertIsNone(lg.aviso(registro(400000), dict(CFG, longitud_activa=False)))
        self.assertIsNone(lg.aviso(os.path.join(tempfile.mkdtemp(), "no-existe.jsonl"), CFG))
        self.assertIsNone(lg.aviso(None, CFG))

    def test_cada_chat_tiene_su_estado(self):
        self.assertIsNotNone(lg.aviso(registro(250000, nombre="a.jsonl"), CFG))
        self.assertIsNotNone(lg.aviso(registro(250000, nombre="b.jsonl"), CFG))

    def test_spec025_aviso_firme_por_defecto(self):
        texto, _ = lg.evaluar(250000, "c", {}, dict(A, auto=True))
        self.assertIn("start_session", texto)
        self.assertIn("Nunca digas que la app lo rechaza", texto)
        self.assertTrue(lg.ajustes({})["auto"])

    def test_modo_fabrica_el_chat_nuevo_es_la_directora(self):
        for idioma, marca in (("es", "claude-opus-5-5"), ("en", "claude-opus-5-5")):
            con, _ = lg.evaluar(250000, "c", {}, dict(A, auto=True), {"modo_fabrica": True, "idioma": idioma})
            self.assertIn(marca, con)
            self.assertIn("directora-N", con)
            self.assertIn("directora_n.txt", con)
            sin, _ = lg.evaluar(250000, "c", {}, dict(A, auto=True), {"idioma": idioma})
            self.assertNotIn("claude-opus-5-5", sin)
        manual, _ = lg.evaluar(250000, "c", {}, dict(A, auto=False), {"modo_fabrica": True})
        self.assertNotIn("claude-opus-5-5", manual)

    def test_modo_automatico_nunca_espera_una_tarjeta(self):
        for idioma in ("es", "en"):
            cfg = {"modo_fabrica": True, "fabrica_automatica": True, "idioma": idioma}
            con, _ = lg.evaluar(250000, "c", {}, dict(A, auto=True), cfg)
            self.assertIn("traspaso.md", con)
            self.assertIn("create_scheduled_task", con)
            self.assertIn("claude-opus-5-5", con)
            self.assertIn("set_session_title", con)
            solo, _ = lg.evaluar(250000, "c", {}, dict(A, auto=True), {"modo_fabrica": True, "idioma": idioma})
            self.assertNotIn("SIGUE en este chat", solo)
            self.assertNotIn("KEEP GOING in this chat", solo)

    def test_automatico_repite_el_aviso_cada_20000(self):
        self.assertEqual(lg.ajustes({"longitud_repetir_tokens": 100000})["repetir"], 100000)
        self.assertEqual(lg.ajustes({"longitud_repetir_tokens": 100000, "modo_fabrica": True})["repetir"], 100000)
        a = lg.ajustes({"longitud_repetir_tokens": 100000, "modo_fabrica": True, "fabrica_automatica": True})
        self.assertEqual(a["repetir"], 20000)
        self.assertEqual(lg.tramo(226000, a), 2)
        self.assertEqual(lg.tramo(245000, a), 3)

    def test_spec025_apagado_solo_avisa(self):
        texto, _ = lg.evaluar(250000, "c", {}, dict(A, auto=False))
        self.assertNotIn("start_session", texto)
        self.assertIn("No lo abras", texto)

    def test_spec025_comando_chat_nuevo(self):
        guardado = []
        original = lg.guardar_config
        lg.guardar_config = lambda cfg: guardado.append(dict(cfg))
        try:
            cfg = {}
            self.assertIn("DESACTIVADO", lg.chat_nuevo(cfg, "no"))
            self.assertIs(cfg["chat_nuevo_auto"], False)
            self.assertIn("ACTIVADO", lg.chat_nuevo(cfg, "sí"))
            self.assertIs(cfg["chat_nuevo_auto"], True)
            self.assertIn("ACTIVADO", lg.chat_nuevo(cfg, "estado"))
            self.assertIn("--chat-nuevo", lg.chat_nuevo(cfg, "quizá"))
            self.assertEqual(len(guardado), 2)
        finally:
            lg.guardar_config = original

    def test_el_hook_de_cierre_lo_incorpora(self):
        estado = os.path.join(tempfile.mkdtemp(), "estado.json")
        r = subprocess.run([sys.executable, os.path.join(GUARDIANES, "cierre.py")], input=json.dumps({"transcript_path": registro(260000)}),
                           capture_output=True, text=True, encoding="utf-8", env=dict(os.environ, CEREBRO_ESTADO_LONGITUD=estado))
        self.assertEqual(r.returncode, 2)
        self.assertIn("Este chat ya pesa", r.stderr)


if __name__ == "__main__":
    unittest.main()
