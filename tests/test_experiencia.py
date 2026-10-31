"""Spec 079: las skills de experiencia (.claude/skills) y su índice (.brain/experiencia/indice.md)."""
import os
import re
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(RAIZ, ".claude", "skills")
INDICE = os.path.join(RAIZ, ".brain", "experiencia", "indice.md")
TOPE_LINEAS = 60


def _skills():
    return sorted(d for d in os.listdir(SKILLS) if os.path.isfile(os.path.join(SKILLS, d, "SKILL.md")))


def _leer(nombre):
    with open(os.path.join(SKILLS, nombre, "SKILL.md"), encoding="utf-8") as f:
        return f.read()


class ExperienciaTest(unittest.TestCase):
    def test_cada_skill_tiene_cabecera_valida(self):
        for n in _skills():
            m = re.match(r"---\nname: ([^\n]+)\ndescription: ([^\n]+)\n---\n", _leer(n))
            self.assertIsNotNone(m, n)
            self.assertEqual(m.group(1), n, "name debe coincidir con la carpeta")
            self.assertRegex(n, r"^[a-z0-9]+(-[a-z0-9]+)*$")
            self.assertTrue(m.group(2).strip(), n)
            self.assertLess(len(m.group(2)), 300, n)

    def test_cuerpo_no_pasa_del_tope_y_tiene_secciones(self):
        for n in _skills():
            texto = _leer(n)
            self.assertLessEqual(len(texto.splitlines()), TOPE_LINEAS, n)
            for seccion in ("## Cómo (pasos)", "## Error que evita", "## Dónde está en el repo", "## Fuente", "## Usada"):
                self.assertIn(seccion, texto, "%s: falta %s" % (n, seccion))

    @unittest.skipUnless(os.path.exists(INDICE), "el proyecto no lleva índice de experiencia")
    def test_indice_y_carpetas_coinciden(self):
        with open(INDICE, encoding="utf-8") as f:
            en_indice = sorted(re.findall(r"^\| \[([a-z0-9-]+)\]\(", f.read(), re.M))
        self.assertEqual(en_indice, _skills())


if __name__ == "__main__":
    unittest.main()
