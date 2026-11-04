# -*- coding: utf-8 -*-
"""Spec 018: guardián de archivos de memoria demasiado gordos."""
import importlib.util
import os
import shutil
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_e = importlib.util.spec_from_file_location("archivos_gordos", os.path.join(RAIZ, ".brain", "guardianes", "archivos_gordos.py"))
ag = importlib.util.module_from_spec(_e)
_e.loader.exec_module(ag)
CFG = {"tope_archivo_memoria_bytes": 1000}


def poner(base, rel, n):
    ruta = os.path.join(base, *rel.split("/"))
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write("x" * n)


class ArchivosGordosTest(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.d, True)

    def test_avisa_del_gordo_y_calla_si_cabe(self):
        poner(self.d, ".brain/referencias.md", 3000)
        poner(self.d, ".brain/constitution.md", 100)
        r = ag.analizar(self.d, CFG)
        self.assertEqual([h["ruta"] for h in r], [".brain/referencias.md"])
        self.assertIn("referencias.md", ag.resumen(self.d, CFG)[0])
        os.remove(os.path.join(self.d, ".brain", "referencias.md"))
        self.assertEqual(ag.resumen(self.d, CFG), [])

    def test_ignora_archivo_pendientes_y_carpetas_de_archivo(self):
        for rel in (".brain/pendientes.md", ".brain/archive/adoptado/X.md", ".brain/biblioteca/CEREBRO_VIVO.md",
                    ".brain/specs/001.md", ".brain/traspaso.md", ".brain/experiencia/indice.md"):
            poner(self.d, rel, 5000)
        self.assertEqual(ag.analizar(self.d, CFG), [])

    def test_mira_architecture_y_se_apaga(self):
        poner(self.d, ".brain/architecture/loot.md", 2000)
        self.assertEqual(len(ag.analizar(self.d, CFG)), 1)
        self.assertEqual(ag.analizar(self.d, dict(CFG, archivos_gordos_activo=False)), [])
        self.assertEqual(ag.analizar(self.d, dict(CFG, archivos_gordos_ignorar=[".brain/architecture/*"])), [])


if __name__ == "__main__":
    unittest.main()
