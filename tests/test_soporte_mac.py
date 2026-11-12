# -*- coding: utf-8 -*-
"""Spec 013: portabilidad a Mac. Lo de Mac solo se simula aquí; la prueba real la hace quien tenga un Mac."""
import importlib.util
import os
import tempfile
import unittest
from unittest import mock

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_espec = importlib.util.spec_from_file_location("instalar", os.path.join(RAIZ, ".brain", "biblioteca", "kit-arranque", "instalar.py"))
instalar = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(instalar)


class TestSoporteMac(unittest.TestCase):
    def test_gancho_usa_python3_en_mac_sin_python(self):
        vacio = tempfile.mkdtemp()
        sin_python = lambda nombre: "/usr/bin/python3" if nombre == "python3" else None
        with mock.patch.object(instalar.os, "name", "posix"), mock.patch.object(instalar.shutil, "which", sin_python):
            self.assertEqual(instalar.python_del_proyecto(vacio), ("python3", "python3"))

    def test_gancho_sigue_con_python_si_existe(self):
        vacio = tempfile.mkdtemp()
        with mock.patch.object(instalar.os, "name", "posix"), mock.patch.object(instalar.shutil, "which", lambda n: "/x/" + n):
            self.assertEqual(instalar.python_del_proyecto(vacio), ("python", "python"))
        with mock.patch.object(instalar.os, "name", "nt"), mock.patch.object(instalar.shutil, "which", lambda n: None):
            self.assertEqual(instalar.python_del_proyecto(vacio), ("python", "python"))  # Windows no cambia

    def test_instalador_de_mac_existe_con_fin_de_linea_unix_y_va_en_el_manifiesto(self):
        ruta_manifiesto = os.path.join(RAIZ, "manifiesto.json")
        if not os.path.isfile(ruta_manifiesto):
            # Solo el repo del arnés es la fuente del instalador. En un proyecto, Git de Windows puede haberlo
            # pasado a fin de línea CRLF al bajarlo y eso no es un fallo del método (punto 37-b).
            self.skipTest("solo se comprueba en el repo del arnés")
        ruta = os.path.join(RAIZ, "instalar_kit.command")
        with open(ruta, "rb") as f:
            datos = f.read()
        self.assertTrue(datos.startswith(b"#!/bin/sh"))
        self.assertNotIn(b"\r\n", datos)
        self.assertIn(b"instalar_gui.py", datos)
        with open(ruta_manifiesto, encoding="utf-8") as f:
            self.assertIn("instalar_kit.command", f.read())


if __name__ == "__main__":
    unittest.main()
