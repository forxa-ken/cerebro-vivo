# -*- coding: utf-8 -*-
"""Spec 043: guardián `hermanos.py` (commits del hermano sin portar), con dos repositorios de juguete."""
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def cargar(nombre, ruta):
    e = importlib.util.spec_from_file_location(nombre, os.path.join(RAIZ, *ruta))
    m = importlib.util.module_from_spec(e)
    e.loader.exec_module(m)
    return m


hermanos = cargar("hermanos_g", [".brain", "guardianes", "hermanos.py"])
arranque = cargar("arranque_h", [".brain", "guardianes", "arranque.py"])


def git(carpeta, *args):
    r = subprocess.run(["git", "-C", carpeta, "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false"] + list(args),
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return r.stdout.strip()


def commit(carpeta, nombre, asunto):
    with open(os.path.join(carpeta, nombre), "w", encoding="utf-8") as f:
        f.write(asunto)
    git(carpeta, "add", "-A")
    git(carpeta, "commit", "-q", "-m", asunto)
    return git(carpeta, "rev-parse", "HEAD")


def portar(raiz, texto):
    os.makedirs(os.path.join(raiz, ".brain"), exist_ok=True)
    with open(os.path.join(raiz, ".brain", "portar.md"), "w", encoding="utf-8") as f:
        f.write(texto)


class HermanosTest(unittest.TestCase):
    def setUp(self):
        base = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, base, True)
        self.este = os.path.join(base, "este")
        self.otro = os.path.join(base, "otro")
        for c in (self.este, self.otro):
            os.makedirs(c)
            git(c, "init", "-q", "-b", "main")
        self.c1 = commit(self.otro, "a.txt", "uno")
        self.c2 = commit(self.otro, "b.txt", "dos")
        self.c3 = commit(self.otro, "c.txt", "tres")
        self.cfg = {"idioma": "es", "proyectos_hermanos": [
            {"nombre": "OTRO", "ruta": "../otro", "rama": "main", "archivo_portar": ".brain/portar.md"}]}

    def pendientes(self):
        return [p[0] for p in hermanos.revisar(self.este, self.cfg)[0]["pendientes"]]

    def test_sin_hermanos_calla(self):
        self.assertEqual(hermanos.lineas_arranque(self.este, {"idioma": "es"}), [])
        self.assertEqual(hermanos.lineas_arranque(self.este, {"proyectos_hermanos": []}), [])
        self.assertIn("proyectos_hermanos", hermanos.informe(self.este, {"idioma": "es"})[0])

    def test_sin_archivo_todo_es_pendiente(self):
        r = hermanos.revisar(self.este, self.cfg)[0]
        self.assertEqual(r["estado"], "sin_archivo")
        self.assertEqual(len(r["pendientes"]), 3)

    def test_ultimo_portado_y_hecho_descuentan(self):
        portar(self.este, "# Portar\n\n## Último portado\n- `%s`\n\n## Pendiente\n- nada\n\n## Hecho\n" % self.c1[:7])
        self.assertEqual(self.pendientes(), [self.c3[:7], self.c2[:7]])
        portar(self.este, "## Último portado\n- `%s`\n\n## Hecho\n### `%s` · dos\n- No portar: no aplica\n" % (self.c1[:7], self.c2[:7]))
        self.assertEqual(self.pendientes(), [self.c3[:7]])
        portar(self.este, "## Último portado\n- `%s`\n## Hecho\n- %s\n- %s\n" % (self.c1, self.c2, self.c3))
        self.assertEqual(self.pendientes(), [])

    def test_un_hash_solo_en_pendiente_sigue_pendiente(self):
        portar(self.este, "## Último portado\n- `%s`\n\n## Pendiente\n- `%s` falta\n\n## Hecho\n" % (self.c1[:7], self.c3[:7]))
        self.assertIn(self.c3[:7], self.pendientes())

    def test_encabezados_en_ingles(self):
        portar(self.este, "## Last ported\n- `%s`\n\n## Pending\n\n## Done\n- `%s`\n" % (self.c1[:7], self.c2[:7]))
        self.assertEqual(self.pendientes(), [self.c3[:7]])

    def test_hermano_inaccesible_calla_en_arranque(self):
        self.cfg["proyectos_hermanos"][0]["ruta"] = "../no-existe"
        self.assertEqual(hermanos.revisar(self.este, self.cfg)[0]["estado"], "inaccesible")
        self.assertEqual(hermanos.lineas_arranque(self.este, self.cfg), [])
        self.assertIn("no accesible", hermanos.informe(self.este, self.cfg)[0])
        self.cfg["proyectos_hermanos"][0].update(ruta="../otro", rama="no-existe")
        self.assertEqual(hermanos.revisar(self.este, self.cfg)[0]["estado"], "inaccesible")

    def test_ruta_absoluta_y_varios_hermanos(self):
        self.cfg["proyectos_hermanos"].append({"nombre": "B", "ruta": self.otro, "rama": "main", "archivo_portar": ".brain/no.md"})
        res = hermanos.revisar(self.este, self.cfg)
        self.assertEqual([r["nombre"] for r in res], ["OTRO", "B"])
        self.assertEqual(len(hermanos.lineas_arranque(self.este, self.cfg)), 2)

    def test_solo_lectura(self):
        antes = git(self.otro, "status", "--porcelain") + git(self.otro, "rev-parse", "HEAD")
        hermanos.informe(self.este, self.cfg)
        self.assertEqual(git(self.otro, "status", "--porcelain") + git(self.otro, "rev-parse", "HEAD"), antes)
        self.assertFalse(os.path.exists(os.path.join(self.este, ".brain", "portar.md")))

    def test_aviso_en_ingles_y_singular(self):
        portar(self.este, "## Último portado\n- `%s`\n## Hecho\n- `%s`\n" % (self.c1[:7], self.c2[:7]))
        self.cfg["idioma"] = "en"
        linea = hermanos.lineas_arranque(self.este, self.cfg)[0]
        self.assertIn("1 commit from OTRO", linea)

    def test_arranque_incluye_la_linea(self):
        os.makedirs(os.path.join(self.este, ".brain"), exist_ok=True)
        self.cfg.update(pendientes=".brain/pendientes.md", tope_pendientes_bytes=8192)
        texto = arranque.resumen(self.este, self.cfg)
        self.assertIn("sin portar", texto)
        self.assertIn("OTRO", texto)

    def test_config_del_repo_trae_la_lista_vacia(self):
        with open(os.path.join(RAIZ, ".brain", "guardianes", "guardianes.json"), encoding="utf-8") as f:
            self.assertEqual(json.load(f).get("proyectos_hermanos"), [])


if __name__ == "__main__":
    unittest.main()
