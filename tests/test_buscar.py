# -*- coding: utf-8 -*-
"""Spec 049 (pendiente 46): buscar.py encuentra en .brain/ sin índice, sin tildes y con puntuación."""
import importlib.util
import os
import shutil
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_espec = importlib.util.spec_from_file_location("buscar", os.path.join(RAIZ, ".brain", "guardianes", "buscar.py"))
bu = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(bu)


def poner(raiz, rel, texto):
    ruta = os.path.join(raiz, *rel.split("/"))
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)


class TestBuscar(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.d, True)
        poner(self.d, ".brain/lecciones/a.md", "# Lecciones: heredocs\n\nUn salto de línea rompió el script.\n")
        poner(self.d, ".brain/specs/001-otra.md", "# Spec 001: otra cosa\n\nMenciona un heredoc de pasada.\n")
        poner(self.d, ".brain/archive/vieja.md", "# Vieja\n\nheredoc antiguo\n")

    def archivos(self, consulta, **kw):
        return [r["archivo"] for r in bu.buscar(self.d, consulta, **kw)]

    def test_sin_tildes_ni_mayusculas(self):
        self.assertIn(".brain/lecciones/a.md", self.archivos("LECCION"))
        self.assertIn(".brain/lecciones/a.md", self.archivos("linea"))

    def test_el_titulo_pesa_mas_que_una_mencion_de_pasada(self):
        self.assertEqual(self.archivos("heredoc")[0], ".brain/lecciones/a.md")

    def test_archive_fuera_por_defecto_y_dentro_con_archivo(self):
        self.assertNotIn(".brain/archive/vieja.md", self.archivos("heredoc"))
        self.assertIn(".brain/archive/vieja.md", self.archivos("heredoc", con_archivo=True))

    def test_solo_limita_la_carpeta(self):
        self.assertEqual(self.archivos("heredoc", solo=["specs"]), [".brain/specs/001-otra.md"])

    def test_maximo(self):
        self.assertEqual(len(bu.buscar(self.d, "heredoc", maximo=1)), 1)

    def test_palabras_vacias_y_consulta_vacia(self):
        self.assertEqual(bu.palabras("el tope de la memoria"), ["tope", "memoria"])
        self.assertEqual(bu.buscar(self.d, "de la el"), [])

    def test_sin_resultados_da_mensaje(self):
        self.assertIn("nada", bu.formatear(bu.buscar(self.d, "zzzz"), "zzzz").lower())

    def test_varias_palabras_en_el_mismo_archivo_suben(self):
        poner(self.d, ".brain/lecciones/b.md", "# B\n\ntope bytes\n")
        poner(self.d, ".brain/lecciones/c.md", "# C\n\ntope\n")
        self.assertEqual(self.archivos("tope bytes")[0], ".brain/lecciones/b.md")

    def test_un_archivo_largo_no_gana_solo_por_repetir(self):
        poner(self.d, ".brain/lecciones/largo.md", "# Largo\n\n" + "tope\n" * 500)
        poner(self.d, ".brain/lecciones/justo.md", "# Tope\n\nalgo\n")
        self.assertEqual(self.archivos("tope")[0], ".brain/lecciones/justo.md")

    def test_busca_en_decisions_log_y_no_en_notas_de_chats(self):
        poner(self.d, ".brain/decisions.log", "2026-11-14 | Claude | cambio unico\n")
        poner(self.d, ".brain/notas-chats/n.md", "cambio unico\n")
        self.assertEqual(self.archivos("unico"), [".brain/decisions.log"])

    def test_repo_real_responde_rapido(self):
        import time
        t0 = time.time()
        res = bu.buscar(RAIZ, "heredoc")
        self.assertTrue(res)
        self.assertLess(time.time() - t0, 2.0)


if __name__ == "__main__":
    unittest.main()
