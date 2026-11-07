# -*- coding: utf-8 -*-
"""Spec 016: guardián que revisa CLAUDE.md, GEMINI.md y AGENTS.md (solo lectura, con descartes)."""
import datetime
import importlib.util
import json
import os
import shutil
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_espec = importlib.util.spec_from_file_location("revisar_indices", os.path.join(RAIZ, ".brain", "guardianes", "revisar_indices.py"))
rev = importlib.util.module_from_spec(_espec)
_espec.loader.exec_module(rev)

HOY = datetime.date(2026, 11, 4)
CFG = {"indices_entrada": ["CLAUDE.md"], "claude_md": "CLAUDE.md", "tope_claude_md_bytes": 5120}


def poner(base, rel, texto):
    ruta = os.path.join(base, *rel.split("/"))
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)


class Base(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.d, True)

    def informe(self, cfg=None, hoy=HOY):
        return rev.analizar(self.d, cfg or CFG, hoy)

    def tipos(self, informe):
        return sorted({h["tipo"] for h in informe["hallazgos"]})


class TestReferencias(Base):
    def test_ruta_rota_se_detecta_y_la_que_existe_no(self):
        poner(self.d, "CLAUDE.md", "# P\n\n## Mapa\nVer `src/viejo.py` y `src/vivo.py`.\n")
        poner(self.d, "src/vivo.py", "x = 1\n")
        h = self.informe()["hallazgos"]
        self.assertEqual([x["clave"] for x in h], ["referencia_rota|CLAUDE.md|src/viejo.py"])
        self.assertEqual(h[0]["nivel"], "roto")

    def test_propone_nuevo_sitio_si_hay_un_archivo_con_ese_nombre(self):
        poner(self.d, "CLAUDE.md", "## Mapa\nVer `app/utils.py`.\n")
        poner(self.d, "core/utils.py", "")
        h = self.informe()["hallazgos"][0]
        self.assertEqual(h["posible_nuevo_sitio"], ["core/utils.py"])

    def test_nombre_suelto_hallado_en_otra_carpeta_es_dudoso(self):
        poner(self.d, "CLAUDE.md", "## Mapa\nEl archivo `config.json` guarda ajustes.\n")
        poner(self.d, "datos/config.json", "{}")
        self.assertEqual(self.informe()["hallazgos"][0]["nivel"], "dudoso")

    def test_ejemplos_y_urls_y_comandos_no_cuentan(self):
        poner(self.d, "CLAUDE.md", "## Uso\nEjecuta `python -m unittest`, abre `https://x.com/a.html`, usa `*.py`, `<archivo>.md` y `../fuera/a.txt`.\n")
        self.assertEqual(self.informe()["hallazgos"], [])

    def test_frase_de_ejemplo_baja_a_dudoso(self):
        poner(self.d, "CLAUDE.md", "## Uso\nPor ejemplo `ruta/inventada.py` sirve de modelo.\n")
        self.assertEqual(self.informe()["hallazgos"][0]["nivel"], "dudoso")

    def test_lo_que_el_indice_dice_que_se_borro_baja_a_dudoso(self):
        poner(self.d, "CLAUDE.md", "## Huecos\n- Se borraron `Logros.lua` y `Miticas.lua`; ya no hay pestañas.\n")
        h = self.informe()["hallazgos"]
        self.assertEqual({x["nivel"] for x in h}, {"dudoso"})
        self.assertEqual(len(h), 2)

    def test_alternativas_con_barra_no_son_rutas(self):
        poner(self.d, "CLAUDE.md", "## Eventos\nSe usa `ENCOUNTER_START/END` y `Promote/Demote`.\n")
        self.assertEqual(self.informe()["hallazgos"], [])

    def test_lo_que_el_metodo_crea_al_usarlo_se_ignora(self):
        poner(self.d, "CLAUDE.md", "## M\nSi existe `.brain/traspaso.md` léelo; notas en `.brain/notas-chats/`.\n")
        self.assertEqual(self.informe()["hallazgos"], [])

    def test_enlace_markdown_roto(self):
        poner(self.d, "CLAUDE.md", "## M\n* [guía](docs/guia.md)\n")
        self.assertEqual(self.informe()["hallazgos"][0]["clave"], "referencia_rota|CLAUDE.md|docs/guia.md")

    def test_ruta_con_punto_inicial_no_se_estropea(self):
        poner(self.d, "CLAUDE.md", "## M\nVer `.brain/pendientes.md`.\n")
        poner(self.d, ".brain/pendientes.md", "")
        self.assertEqual(self.informe()["hallazgos"], [])

    def test_el_bloque_del_kit_no_se_revisa(self):
        poner(self.d, "CLAUDE.md", "# P\n\n<!-- cerebro-vivo:inicio -->\n## Memoria\nVer `.brain/no_existe.md`.\n<!-- cerebro-vivo:fin -->\n")
        self.assertEqual(self.informe()["hallazgos"], [])


class TestOtrasDetecciones(Base):
    def test_seccion_pesada(self):
        poner(self.d, "CLAUDE.md", "## Pequeña\nhola\n\n## Enorme\n" + "linea de arquitectura\n" * 500)
        h = self.informe()["hallazgos"]
        self.assertEqual([x["tipo"] for x in h if x["tipo"] == "seccion_pesada"], ["seccion_pesada"])
        self.assertIn("Enorme", h[0]["detalle"])

    def test_fecha_vieja_y_fecha_reciente(self):
        poner(self.d, "CLAUDE.md", "## Antigua\nEstado al 2026-01-10.\n\n## Nueva\nEstado al 2026-10-30.\n")
        h = [x for x in self.informe()["hallazgos"] if x["tipo"] == "fecha_vieja"]
        self.assertEqual([x["seccion"] for x in h], ["Antigua"])

    def test_deriva_entre_indices(self):
        poner(self.d, "CLAUDE.md", "## Reglas\nUsa tabs siempre y revisa todo con cuidado antes de subir.\n\n## Solo aquí\nx\n")
        poner(self.d, "AGENTS.md", "## Reglas\nUsa espacios y nunca tabs; sube sin revisar nada de nada.\n")
        cfg = dict(CFG, indices_entrada=["CLAUDE.md", "AGENTS.md"])
        h = self.informe(cfg)["hallazgos"]
        detalles = " | ".join(x["detalle"] for x in h if x["tipo"] == "deriva")
        self.assertIn("«Reglas» difiere", detalles)
        self.assertIn("«Solo aquí» está en CLAUDE.md y falta en AGENTS.md", detalles)

    def test_indices_iguales_no_dan_deriva(self):
        texto = "## Reglas\nUsa tabs siempre.\n"
        poner(self.d, "CLAUDE.md", texto)
        poner(self.d, "AGENTS.md", texto)
        self.assertEqual(self.informe(dict(CFG, indices_entrada=["CLAUDE.md", "AGENTS.md"]))["hallazgos"], [])

    def test_parrafo_duplicado_en_la_memoria(self):
        parrafo = "Toda tarea que toque más de dos archivos pasa primero por una spec que el dueño aprueba antes de programar nada, y se registra en el diario del proyecto con su fecha, su resultado y el nombre de quien la aprobó."
        poner(self.d, "CLAUDE.md", "## Reglas\n" + parrafo + "\n")
        poner(self.d, ".brain/constitution.md", "# Constitución\n\n" + parrafo + "\n")
        h = self.informe()["hallazgos"]
        self.assertEqual([x["tipo"] for x in h], ["duplicado"])
        self.assertIn(".brain/constitution.md", h[0]["detalle"])

    def test_proyecto_sano_da_informe_vacio(self):
        poner(self.d, "CLAUDE.md", "# P\n\n## Reglas\nPocas reglas.\n")
        self.assertEqual(self.informe()["hallazgos"], [])


class TestDescartesYSoloLectura(Base):
    def test_lo_descartado_no_se_repite_y_se_cuenta(self):
        poner(self.d, "CLAUDE.md", "## M\nVer `src/viejo.py`.\n")
        os.makedirs(os.path.join(self.d, ".brain", "guardianes"))
        clave = "referencia_rota|CLAUDE.md|src/viejo.py"
        rev.descartar(self.d, clave, "es un ejemplo", HOY)
        rev.descartar(self.d, clave, "otra vez", HOY)  # no duplica
        informe = self.informe()
        self.assertEqual(informe["hallazgos"], [])
        self.assertEqual(informe["descartados"], 1)
        self.assertEqual(len(rev.leer_estado(self.d)["descartes"]), 1)

    def test_analizar_no_escribe_ni_modifica_nada(self):
        poner(self.d, "CLAUDE.md", "## M\nVer `src/viejo.py` y `src/otro.py`.\n" + "x\n" * 3000)
        antes = {}
        for base, _, nombres in os.walk(self.d):
            for n in nombres:
                with open(os.path.join(base, n), "rb") as f:
                    antes[os.path.join(base, n)] = f.read()
        rev.analizar(self.d, CFG, HOY)
        rev.resumen(self.d, CFG, HOY)
        despues = {}
        for base, _, nombres in os.walk(self.d):
            for n in nombres:
                with open(os.path.join(base, n), "rb") as f:
                    despues[os.path.join(base, n)] = f.read()
        self.assertEqual(antes, despues)

    def test_marcar_revision_guarda_la_fecha(self):
        os.makedirs(os.path.join(self.d, ".brain", "guardianes"))
        rev.marcar_revision(self.d, HOY)
        self.assertEqual(rev.leer_estado(self.d)["ultima_revision"], "2026-11-04")


class TestResumenDeArranque(Base):
    def test_sano_no_dice_nada(self):
        poner(self.d, "CLAUDE.md", "## Reglas\nPocas.\n")
        self.assertEqual(rev.resumen(self.d, CFG, HOY), [])

    def test_avisa_por_tope_referencias_y_antiguedad(self):
        poner(self.d, "CLAUDE.md", "## M\nVer `src/viejo.py`.\n" + "relleno de texto largo\n" * 230)
        os.makedirs(os.path.join(self.d, ".brain", "guardianes"))
        rev.marcar_revision(self.d, HOY - datetime.timedelta(days=100))
        linea = rev.resumen(self.d, CFG, HOY)
        self.assertEqual(len(linea), 1)
        for trozo in ("del tope", "1 referencia(s) rota(s)", "100 días", "revisa los índices", "/adopta"):
            self.assertIn(trozo, linea[0])

    def test_sin_tope_pasado_no_recomienda_adopta(self):
        poner(self.d, "CLAUDE.md", "## M\nVer `src/viejo.py`.\n")
        linea = rev.resumen(self.d, CFG, HOY)
        self.assertIn("revisa los índices", linea[0])
        self.assertNotIn("/adopta", linea[0])

    def test_un_dudoso_no_dispara_el_aviso(self):
        poner(self.d, "CLAUDE.md", "## M\nPor ejemplo `ruta/inventada.py`.\n")
        self.assertEqual(rev.resumen(self.d, CFG, HOY), [])

    def test_se_apaga_con_el_ajuste(self):
        poner(self.d, "CLAUDE.md", "## M\nVer `src/viejo.py`.\n")
        self.assertEqual(rev.resumen(self.d, dict(CFG, revision_indices_activa=False), HOY), [])

    def test_el_arranque_lo_incluye(self):
        poner(self.d, "CLAUDE.md", "## M\nVer `src/viejo.py`.\n")
        shutil.copytree(os.path.join(RAIZ, ".brain", "guardianes"), os.path.join(self.d, ".brain", "guardianes"),
                        ignore=shutil.ignore_patterns("__pycache__", "*_estado.json"))
        espec = importlib.util.spec_from_file_location("arranque_t", os.path.join(self.d, ".brain", "guardianes", "arranque.py"))
        arr = importlib.util.module_from_spec(espec)
        espec.loader.exec_module(arr)
        cfg = arr.cargar_config()
        cfg.update(CFG)
        self.assertIn("Índices de IA", arr.resumen(self.d, cfg))


class TestEnElRepo(unittest.TestCase):
    def test_los_ajustes_estan_en_guardianes_json(self):
        with open(os.path.join(RAIZ, ".brain", "guardianes", "guardianes.json"), encoding="utf-8") as f:
            cfg = json.load(f)
        for clave in ("revision_indices_activa", "revision_indices_dias", "revision_indices_seccion_bytes"):
            self.assertIn(clave, cfg)

    def test_el_kit_instala_el_guardian_y_la_skill_existe(self):
        with open(os.path.join(RAIZ, ".brain", "biblioteca", "kit-arranque", "instalar.py"), encoding="utf-8") as f:
            self.assertIn('"revisar_indices"', f.read())
        self.assertTrue(os.path.isfile(os.path.join(RAIZ, ".claude", "skills", "revisar-indices-de-ia", "SKILL.md")))


if __name__ == "__main__":
    unittest.main()
