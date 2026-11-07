# -*- coding: utf-8 -*-
"""Spec 022: Git automático de `traspaso-out salgo` y aviso de lo que queda sin commitear."""
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GUARDIANES = os.path.join(RAIZ, ".brain", "guardianes")
_espec = importlib.util.spec_from_file_location("arranque", os.path.join(GUARDIANES, "arranque.py"))
arranque = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(arranque)
TOKEN_FALSO = "ghp_" + "a1" * 20  # armado al ejecutar: el código fuente no contiene ningún secreto con formato real


def ejecutar_git(raiz, *args):
    r = subprocess.run(["git"] + list(args), cwd=raiz, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise AssertionError("git %s: %s" % (" ".join(args), r.stderr))
    return r.stdout.strip()


def escribir(raiz, rel, texto):
    ruta = os.path.join(raiz, rel)
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)


class Base(unittest.TestCase):
    def setUp(self):
        self.base = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.base, True)
        self.remoto = os.path.join(self.base, "remoto.git")
        self.raiz = os.path.join(self.base, "proyecto")
        os.makedirs(self.raiz)
        ejecutar_git(self.base, "init", "-q", "--bare", self.remoto)
        ejecutar_git(self.remoto, "symbolic-ref", "HEAD", "refs/heads/main")
        ejecutar_git(self.raiz, "init", "-q")
        ejecutar_git(self.raiz, "symbolic-ref", "HEAD", "refs/heads/main")
        ejecutar_git(self.raiz, "config", "user.email", "t@t")
        ejecutar_git(self.raiz, "config", "user.name", "t")
        destino = os.path.join(self.raiz, ".brain", "guardianes")
        os.makedirs(destino)
        for nombre in ("guardar_traspaso.py", "arranque.py", "secretos.py", "guardianes.json"):
            shutil.copy(os.path.join(GUARDIANES, nombre), destino)
        escribir(self.raiz, ".brain/pendientes.md", "# Pendientes\n")
        escribir(self.raiz, ".brain/decisions.log", "linea\n")
        ejecutar_git(self.raiz, "add", ".")
        ejecutar_git(self.raiz, "commit", "-q", "-m", "base")

    def conectar(self):
        ejecutar_git(self.raiz, "remote", "add", "origin", self.remoto)
        ejecutar_git(self.raiz, "push", "-q", "-u", "origin", "main")

    def guardar(self, *args):
        r = subprocess.run([sys.executable, os.path.join(self.raiz, ".brain", "guardianes", "guardar_traspaso.py")] + list(args),
                           cwd=self.raiz, capture_output=True, text=True, encoding="utf-8", errors="replace")
        self.assertEqual(r.returncode, 0, r.stderr)
        return r.stdout

    def head(self):
        return ejecutar_git(self.raiz, "rev-parse", "HEAD")

    def head_remoto(self):
        return ejecutar_git(self.remoto, "rev-parse", "refs/heads/main")

    def archivos_del_ultimo_commit(self):
        return ejecutar_git(self.raiz, "show", "--name-only", "--format=", "HEAD").splitlines()


class TestGuardarTraspaso(Base):
    def test_commit_de_la_memoria_sin_el_codigo_y_sube(self):
        self.conectar()
        escribir(self.raiz, ".brain/traspaso.md", "traspaso\n")
        escribir(self.raiz, ".brain/pendientes.md", "# Pendientes\n- **1:** algo\n")
        escribir(self.raiz, ".brain/archive/traspasos/viejo.md", "viejo\n")
        escribir(self.raiz, ".brain/specs/001-algo.md", "spec\n")
        escribir(self.raiz, "codigo.py", "x = 1\n")
        salida = self.guardar()
        self.assertEqual(sorted(self.archivos_del_ultimo_commit()),
                         [".brain/archive/traspasos/viejo.md", ".brain/pendientes.md", ".brain/specs/001-algo.md", ".brain/traspaso.md"])
        self.assertEqual(self.head(), self.head_remoto())
        self.assertIn("Subido a GitHub", salida)
        self.assertIn("codigo.py", salida)  # lo que no entra se le dice al dueño
        self.assertIn("?? codigo.py", ejecutar_git(self.raiz, "status", "--porcelain"))

    def test_lo_preparado_fuera_de_la_memoria_no_entra(self):
        self.conectar()
        escribir(self.raiz, "codigo.py", "x = 1\n")
        ejecutar_git(self.raiz, "add", "codigo.py")
        escribir(self.raiz, ".brain/traspaso.md", "traspaso\n")
        self.guardar()
        self.assertEqual(self.archivos_del_ultimo_commit(), [".brain/traspaso.md"])
        self.assertIn("A  codigo.py", ejecutar_git(self.raiz, "status", "--porcelain"))

    def test_con_un_secreto_no_hace_commit_ni_sube(self):
        self.conectar()
        antes = self.head()
        escribir(self.raiz, ".brain/traspaso.md", "clave = %s\n" % TOKEN_FALSO)
        salida = self.guardar()
        self.assertEqual(self.head(), antes)
        self.assertEqual(self.head_remoto(), antes)
        self.assertIn("revisión de secretos", salida)
        self.assertEqual(ejecutar_git(self.raiz, "diff", "--cached", "--name-only"), "")

    def test_sin_remoto_deja_el_commit_y_lo_dice(self):
        escribir(self.raiz, ".brain/traspaso.md", "traspaso\n")
        salida = self.guardar()
        self.assertEqual(self.archivos_del_ultimo_commit(), [".brain/traspaso.md"])
        self.assertIn("no tiene remoto", salida)

    def test_otros_commits_pendientes_paran_la_subida_hasta_el_si(self):
        self.conectar()
        antes = self.head()
        escribir(self.raiz, "codigo.py", "x = 1\n")
        ejecutar_git(self.raiz, "add", "codigo.py")
        ejecutar_git(self.raiz, "commit", "-q", "-m", "codigo sin probar")
        escribir(self.raiz, ".brain/traspaso.md", "traspaso\n")
        salida = self.guardar()
        self.assertEqual(self.archivos_del_ultimo_commit(), [".brain/traspaso.md"])
        self.assertEqual(self.head_remoto(), antes)
        self.assertIn("codigo sin probar", salida)
        self.assertIn("--subir-todo", salida)
        self.guardar("--subir-todo")
        self.assertEqual(self.head(), self.head_remoto())

    def test_commit_anterior_solo_de_memoria_no_para_la_subida(self):
        self.conectar()
        escribir(self.raiz, ".brain/decisions.log", "linea\notra\n")
        ejecutar_git(self.raiz, "add", ".brain/decisions.log")
        ejecutar_git(self.raiz, "commit", "-q", "-m", "registro")
        escribir(self.raiz, ".brain/traspaso.md", "traspaso\n")
        self.guardar()
        self.assertEqual(self.head(), self.head_remoto())

    def test_si_github_rechaza_lo_dice_sin_mezclar(self):
        self.conectar()
        otra = os.path.join(self.base, "otra")
        ejecutar_git(self.base, "clone", "-q", self.remoto, otra)
        ejecutar_git(otra, "config", "user.email", "t@t")
        ejecutar_git(otra, "config", "user.name", "t")
        escribir(otra, "otra.txt", "otro ordenador\n")
        ejecutar_git(otra, "add", ".")
        ejecutar_git(otra, "commit", "-q", "-m", "otro ordenador")
        ejecutar_git(otra, "push", "-q")
        ajeno = self.head_remoto()
        escribir(self.raiz, ".brain/traspaso.md", "traspaso\n")
        salida = self.guardar()
        self.assertIn("no he mezclado nada", salida)
        self.assertEqual(self.head_remoto(), ajeno)
        self.assertFalse(os.path.exists(os.path.join(self.raiz, "otra.txt")))
        self.assertEqual(self.archivos_del_ultimo_commit(), [".brain/traspaso.md"])

    def test_nada_nuevo_y_al_dia(self):
        self.conectar()
        antes = self.head()
        salida = self.guardar()
        self.assertEqual(self.head(), antes)
        self.assertIn("nada nuevo", salida)
        self.assertIn("al día", salida)

    def test_sin_git_no_rompe(self):
        suelta = os.path.join(self.base, "sin_git")
        shutil.copytree(os.path.join(self.raiz, ".brain"), os.path.join(suelta, ".brain"))
        r = subprocess.run([sys.executable, os.path.join(suelta, ".brain", "guardianes", "guardar_traspaso.py")], cwd=suelta,
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Sin Git", r.stdout)


class TestAvisoSinCommitear(Base):
    def test_avisa_de_brain_y_claude_pero_no_de_lo_generado(self):
        for rel in (".brain/specs/001-algo.md", ".claude/skills/x/SKILL.md", ".brain/traspaso.md",
                    ".brain/archive/traspasos/2026.md", ".brain/guardianes/secretos_estado.json", ".brain/decisions.log"):
            escribir(self.raiz, rel, "cambio\n")
        self.assertEqual(sorted(arranque.sin_commitear(self.raiz, {})), [".brain/specs/001-algo.md", ".claude/skills/x/SKILL.md"])

    def test_un_movido_cuenta_por_su_destino(self):
        ejecutar_git(self.raiz, "mv", ".brain/pendientes.md", ".brain/otro.md")
        self.assertEqual(arranque.sin_commitear(self.raiz, {}), [".brain/otro.md"])

    def test_la_clave_del_proyecto_manda_sobre_la_lista_por_defecto(self):
        escribir(self.raiz, ".brain/specs/001-algo.md", "cambio\n")
        self.assertEqual(arranque.sin_commitear(self.raiz, {"no_avisar_commit": [".brain/*"]}), [])

    def test_guardianes_json_y_el_kit_llevan_la_misma_lista(self):
        import json
        with open(os.path.join(GUARDIANES, "guardianes.json"), encoding="utf-8") as f:
            self.assertEqual(json.load(f)["no_avisar_commit"], arranque.NO_AVISAR_COMMIT)
        with open(os.path.join(RAIZ, ".brain", "biblioteca", "kit-arranque", "ajustes_neutros.json"), encoding="utf-8") as f:
            self.assertEqual(json.load(f)["no_avisar_commit"], arranque.NO_AVISAR_COMMIT)

    def test_el_texto_da_el_total_y_hasta_cinco_rutas(self):
        self.assertEqual(arranque.texto_sin_commitear(["a"]), "- Sin commitear: 1 archivo (a).")
        texto = arranque.texto_sin_commitear(list("abcdefgh"))
        self.assertEqual(texto, "- Sin commitear: 8 archivos (a, b, c, d, e…).")


if __name__ == "__main__":
    unittest.main()
