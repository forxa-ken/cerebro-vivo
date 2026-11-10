"""Prueba (manual: python -m unittest discover .brain/fabrica -p "test_*.py") del prototipo de guardián de alcance de la fábrica (spec 035)."""
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("alcance", RAIZ / ".brain" / "fabrica" / "alcance.py")
alcance = importlib.util.module_from_spec(spec)
spec.loader.exec_module(alcance)


def git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


class AlcanceTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.email", "t@t")
        git(self.repo, "config", "user.name", "t")
        (self.repo / "a.lua").write_text("a", encoding="utf-8")
        (self.repo / "b.lua").write_text("b", encoding="utf-8")
        (self.repo / "ya_sucio.txt").write_text("v1", encoding="utf-8")
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-q", "-m", "base")
        (self.repo / "ya_sucio.txt").write_text("v2", encoding="utf-8")  # cambio previo ajeno
        self.foto = alcance.tomar_foto(self.repo)

    def tearDown(self):
        self.tmp.cleanup()

    def test_sin_cambios_no_toca_nada(self):
        self.assertEqual(alcance.tocados(self.repo, self.foto), [])

    def test_cambio_previo_ajeno_no_cuenta(self):
        (self.repo / "a.lua").write_text("a2", encoding="utf-8")
        self.assertEqual(alcance.tocados(self.repo, self.foto), ["a.lua"])

    def test_archivo_nuevo_y_editado_se_detectan(self):
        (self.repo / "nuevo.lua").write_text("n", encoding="utf-8")
        (self.repo / "b.lua").write_text("b2", encoding="utf-8")
        self.assertEqual(alcance.tocados(self.repo, self.foto), ["b.lua", "nuevo.lua"])

    def test_tocar_de_nuevo_un_archivo_ya_sucio_se_detecta(self):
        (self.repo / "ya_sucio.txt").write_text("v3", encoding="utf-8")
        self.assertEqual(alcance.tocados(self.repo, self.foto), ["ya_sucio.txt"])

    def test_permitidos_archivo_y_carpeta(self):
        self.assertTrue(alcance.permitido("a.lua", ["a.lua"]))
        self.assertTrue(alcance.permitido("Modules/x.lua", ["Modules/"]))
        self.assertFalse(alcance.permitido("Core.lua", ["Modules/", "a.lua"]))

    def test_commit_durante_el_trabajo_se_rechaza(self):
        (self.repo / "a.lua").write_text("a2", encoding="utf-8")
        git(self.repo, "commit", "-q", "-am", "colado")
        with self.assertRaises(SystemExit):
            alcance.tocados(self.repo, self.foto)


if __name__ == "__main__":
    unittest.main()
