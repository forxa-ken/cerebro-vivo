# -*- coding: utf-8 -*-
"""Informe 028, 3.4: los puntos 14, 21 y 26 de «esperando tu prueba» comprobados de punta a punta con el arnés REAL
(kit instalado en una carpeta temporal), sin que Darwin tenga que probarlos a mano."""
import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def cargar(nombre, ruta):
    espec = importlib.util.spec_from_file_location(nombre, ruta)
    modulo = importlib.util.module_from_spec(espec)
    espec.loader.exec_module(modulo)
    return modulo


act = cargar("actualizar_arnes", os.path.join(RAIZ, ".brain", "guardianes", "actualizar_arnes.py"))
kit = cargar("instalar", os.path.join(RAIZ, ".brain", "biblioteca", "kit-arranque", "instalar.py"))


def git(cwd, *args):
    r = subprocess.run(["git"] + list(args), cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise AssertionError("git %s: %s" % (" ".join(args), r.stderr))
    return r.stdout.strip()


def escribir(base, rel, texto):
    ruta = os.path.join(base, *rel.split("/"))
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)


def leer(base, rel):
    with open(os.path.join(base, *rel.split("/")), encoding="utf-8", newline="") as f:
        return f.read()


class ProyectoReal(unittest.TestCase):
    def setUp(self):
        self.base = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.base, True)
        self.proy = os.path.join(self.base, "proyecto")
        os.makedirs(self.proy)
        kit.instalar(self.proy, "Demo", "Ana", "español", "python -m unittest discover tests", ["claude"], "completo", hoy="2026-01-01")

    def ruta(self, rel):
        return os.path.join(self.proy, *rel.split("/"))


class TestPunto14ActualizadorFiable(ProyectoReal):
    """Punto 14 (spec 021): lo faltante vuelve, lo tocado a mano se respeta y lo retirado va a copias_arnes."""

    def test_repone_lo_borrado_respeta_lo_tocado_y_retira_lo_viejo(self):
        borrado = ".brain/guardianes/longitud.py"
        tocado = ".brain/guardianes/poda.py"
        retirado = ".claude/skills/traspaso-entre-chats/SKILL.md"
        os.remove(self.ruta(borrado))
        escribir(self.proy, tocado, leer(self.proy, tocado) + "\n# mi cambio\n")
        escribir(self.proy, retirado, "skill vieja\n")
        registro = act.cargar_registro(self.proy)
        registro["archivos"][retirado] = act.huella(act._normalizar(act.leer_bytes(self.ruta(retirado)), retirado))
        act.guardar_registro(self.proy, registro)

        simulado = act.sincronizar(RAIZ, self.proy, simular=True)
        self.assertTrue(os.path.exists(self.ruta(retirado)), "simular no debe mover nada")
        self.assertFalse(os.path.exists(self.ruta(borrado)))
        self.assertIn(retirado, str(simulado))

        act.sincronizar(RAIZ, self.proy)
        self.assertTrue(os.path.isfile(self.ruta(borrado)), "lo borrado debe volver")
        self.assertIn("# mi cambio", leer(self.proy, tocado), "lo modificado a mano no se pisa")
        self.assertFalse(os.path.exists(self.ruta(retirado)), "lo retirado sale del proyecto")
        copias = os.path.join(self.proy, ".brain", "copias_arnes")
        guardado = [os.path.relpath(os.path.join(c, n), copias) for c, _, ns in os.walk(copias) for n in ns]
        copia = [f for f in guardado if f.endswith(os.path.join("traspaso-entre-chats", "SKILL.md"))]
        self.assertEqual(len(copia), 1, "lo retirado se conserva en .brain/copias_arnes/")
        self.assertEqual(leer(copias, copia[0].replace(os.sep, "/")), "skill vieja\n")

        otra_vez = act.sincronizar(RAIZ, self.proy, simular=True)
        self.assertEqual((otra_vez["nuevos"], otra_vez["actualizados"], otra_vez["forzados"]), ([], [], []),
                         "segunda pasada: nada que hacer")


class TestPunto26Version(ProyectoReal):
    """Punto 26 (spec 023): /version lee `arnes_instalado.json` y el `VERSION` del repo; todo lo que necesita existe."""

    def test_la_skill_y_los_datos_que_lee_existen_y_coinciden(self):
        skill = leer(self.proy, ".claude/skills/version/SKILL.md")
        for dato in ("arnes_instalado.json", "arnes_repo", "VERSION", "CAMBIOS.md", "/actualizar"):
            self.assertIn(dato, skill)
        self.assertTrue(os.path.isfile(self.ruta(".brain/arnes_instalado.json")))
        version_repo = leer(RAIZ, "VERSION").strip()
        self.assertEqual(act.cargar_registro(self.proy)["version"], version_repo)
        self.assertIsNone(act.version_disponible(self.proy), "al día: no hay versión más nueva")

    def test_con_version_vieja_avisa_y_los_titulos_estan_en_cambios(self):
        registro = act.cargar_registro(self.proy)
        registro["version"] = "1.0.0"
        act.guardar_registro(self.proy, registro)
        version_repo = leer(RAIZ, "VERSION").strip()
        self.assertEqual(act.version_disponible(self.proy), ("1.0.0", version_repo))
        self.assertIn(version_repo, leer(RAIZ, "CAMBIOS.md"), "el aviso puede citar el título de la versión nueva")

    def test_la_edicion_en_ingles_lleva_lo_mismo(self):
        self.assertIn("arnes_instalado.json", leer(RAIZ, ".claude/skills/version/SKILL.en.md"))


class TestPunto21NadaSueltoNiViejo(ProyectoReal):
    """Punto 21 (spec 022): `traspaso-out salgo` hace commit de la memoria, la sube y lista el código suelto sin meterlo."""

    def test_salgo_sube_la_memoria_y_avisa_del_codigo_suelto(self):
        remoto = os.path.join(self.base, "remoto.git")
        git(self.base, "init", "-q", "--bare", remoto)
        git(remoto, "symbolic-ref", "HEAD", "refs/heads/main")
        git(self.proy, "init", "-q")
        git(self.proy, "symbolic-ref", "HEAD", "refs/heads/main")
        git(self.proy, "config", "user.email", "t@t")
        git(self.proy, "config", "user.name", "t")
        git(self.proy, "add", ".")
        git(self.proy, "commit", "-q", "-m", "base")
        git(self.proy, "remote", "add", "origin", remoto)
        git(self.proy, "push", "-q", "-u", "origin", "main")

        escribir(self.proy, ".brain/traspaso.md", "traspaso\n")
        escribir(self.proy, "codigo_suelto.py", "x = 1\n")
        r = subprocess.run([sys.executable, self.ruta(".brain/guardianes/guardar_traspaso.py")], cwd=self.proy,
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(git(self.proy, "show", "--name-only", "--format=", "HEAD").splitlines(), [".brain/traspaso.md"])
        self.assertEqual(git(self.proy, "rev-parse", "HEAD"), git(remoto, "rev-parse", "refs/heads/main"), "la memoria se subió")
        self.assertIn("codigo_suelto.py", r.stdout, "el código suelto se lista")
        self.assertIn("?? codigo_suelto.py", git(self.proy, "status", "--porcelain"), "y no se mete en el commit")


if __name__ == "__main__":
    unittest.main()
