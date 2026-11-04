# -*- coding: utf-8 -*-
"""Interfaz del instalador (spec 055): lógica sin ventana y arranque de la ventana de Tk."""
import importlib.util
import os
import tempfile
import time
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_espec = importlib.util.spec_from_file_location("instalar_gui", os.path.join(RAIZ, ".brain", "biblioteca", "kit-arranque", "instalar_gui.py"))
gui = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(gui)


def datos(destino, **extra):
    d = dict(destino=destino, nombre="Demo", dueno="", idioma="", pruebas="", ias=["claude"], nivel="completo")
    d.update(extra)
    return d


class TestLogica(unittest.TestCase):
    def setUp(self):
        self.original = gui.PREFERENCIAS
        gui.PREFERENCIAS = os.path.join(tempfile.mkdtemp(), "preferencias.json")

    def tearDown(self):
        gui.PREFERENCIAS = self.original

    def test_validar_campos_obligatorios(self):
        self.assertEqual(gui.validar(datos("x")), {})
        mal = gui.validar(datos("  ", nombre="", ias=[], nivel="otro"))
        self.assertEqual(sorted(mal), ["destino", "ias", "nivel", "nombre"])

    def test_resumen_no_escribe_nada_y_cuenta(self):
        carpeta = tempfile.mkdtemp()
        texto = gui.texto_resumen(datos(carpeta))
        self.assertIn("nivel completo", texto)
        self.assertRegex(texto, r"Se crearán \d+ archivo")
        self.assertEqual(os.listdir(carpeta), [])

    def test_resumen_avisa_de_lo_que_ya_existe(self):
        carpeta = tempfile.mkdtemp()
        with open(os.path.join(carpeta, "CLAUDE.md"), "w", encoding="utf-8") as f:
            f.write("mío")
        self.assertIn("AÑADIRÁ lo del kit", gui.texto_resumen(datos(carpeta)))  # spec 015: se fusiona, no se pisa
        with open(os.path.join(carpeta, "CLAUDE.md"), encoding="utf-8") as f:
            self.assertEqual(f.read(), "mío")  # el resumen no escribe nada
        otra = tempfile.mkdtemp()
        os.makedirs(os.path.join(otra, ".brain"))
        with open(os.path.join(otra, ".brain", "pendientes.md"), "w", encoding="utf-8") as f:
            f.write("mío")
        self.assertIn("NO se tocarán", gui.texto_resumen(datos(otra)))

    def test_ejecutar_instala_comprueba_e_inicializa_git(self):
        carpeta = tempfile.mkdtemp()
        lineas, ok = gui.ejecutar(datos(carpeta, dueno="Ana"))
        self.assertTrue(ok, "\n".join(lineas))
        self.assertTrue(os.path.isdir(os.path.join(carpeta, ".git")))
        self.assertIn("reiniciar Claude Code", "\n".join(lineas))
        self.assertEqual(gui.cargar_preferencias().get("dueno"), "Ana")  # se recuerda para la próxima vez

    def test_sin_git_init_no_crea_git(self):
        carpeta = tempfile.mkdtemp()
        gui.ejecutar(datos(carpeta, nivel="medio"), git_init=False)
        self.assertFalse(os.path.exists(os.path.join(carpeta, ".git")))

    def test_comprobar_informa_de_un_proyecto_sin_kit(self):
        lineas, ok = gui.comprobar(datos(tempfile.mkdtemp()))
        self.assertFalse(ok)
        self.assertIn("❌", lineas[0])


class TestVentana(unittest.TestCase):
    def setUp(self):  # nunca toca las preferencias reales del equipo
        self.original = gui.PREFERENCIAS
        gui.PREFERENCIAS = os.path.join(tempfile.mkdtemp(), "preferencias.json")

    def tearDown(self):
        gui.PREFERENCIAS = self.original

    def test_la_ventana_se_construye_y_instala_en_segundo_plano(self):
        try:
            raiz, v, ias, leer, en_hilo, mostrar = gui.abrir_ventana()
        except Exception as e:  # equipo sin pantalla o sin Tk
            self.skipTest("Sin pantalla: %s" % e)
        try:
            carpeta = tempfile.mkdtemp()
            v["destino"].set(carpeta)
            v["nombre"].set("Demo")
            v["nivel"].set("medio")
            self.assertEqual(leer()["ias"], ["claude"])
            en_hilo(lambda d: gui.ejecutar(d, git_init=False), leer())
            texto_ventana = raiz.winfo_children()[0].grid_slaves(row=24)[0]
            fin = time.time() + 60
            while time.time() < fin and "Kit instalado" not in texto_ventana.get("1.0", "end"):
                raiz.update()
                time.sleep(0.05)
            self.assertIn("Kit instalado", texto_ventana.get("1.0", "end"))
            self.assertTrue(os.path.exists(os.path.join(carpeta, ".brain", "constitution.md")))
        finally:
            raiz.destroy()


if __name__ == "__main__":
    unittest.main()
