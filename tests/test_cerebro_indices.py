# -*- coding: utf-8 -*-
"""Guardián 2 de Cerebro Vivo (spec 046): los índices de .brain/ no pueden desfasarse.
Si alguien añade una decisión sin fila, un enlace roto o deja crecer pendientes.md, este test se pone en rojo."""

import importlib.util
import json
import os
import re
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BRAIN = os.path.join(RAIZ, ".brain")
GUARDIANES = os.path.join(BRAIN, "guardianes")


def leer(*partes):
    with open(os.path.join(*partes), encoding="utf-8") as f:
        return f.read()


def cfg():
    return json.loads(leer(GUARDIANES, "guardianes.json"))


def cargar_cierre():
    spec = importlib.util.spec_from_file_location("cierre", os.path.join(GUARDIANES, "cierre.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestIndicesCerebro(unittest.TestCase):

    def test_cada_decision_tiene_fila_y_cada_fila_su_ficha(self):
        carpeta = os.path.join(BRAIN, "decisions")
        fichas = {f for f in os.listdir(carpeta) if re.match(r"D-\d{3}-.*\.md$", f)}
        archivadas = os.path.join(carpeta, "archivo")  # spec 048: fichas «reemplazada» movidas por la poda
        if os.path.isdir(archivadas):
            fichas |= {f for f in os.listdir(archivadas) if re.match(r"D-\d{3}-.*\.md$", f)}
        indice = leer(carpeta, "indice.md")
        enlazadas = set(re.findall(r"\]\((?:archivo/)?(D-\d{3}-[^)]*\.md)\)", indice))
        self.assertEqual(fichas - enlazadas, set(), "Fichas sin fila en decisions/indice.md")
        self.assertEqual(enlazadas - fichas, set(), "Filas del índice que apuntan a una ficha que no existe")

    def test_ids_de_decision_sin_repetir(self):
        carpeta = os.path.join(BRAIN, "decisions")
        ids = [f[:5] for base in (carpeta, os.path.join(carpeta, "archivo")) if os.path.isdir(base)
               for f in os.listdir(base) if re.match(r"D-\d{3}-.*\.md$", f)]
        self.assertEqual(len(ids), len(set(ids)), "Hay dos fichas con el mismo D-NNN")

    def test_indice_de_hechos_coincide_con_hechos(self):
        carpeta = os.path.join(BRAIN, "archive")
        indice = leer(carpeta, "hechos-indice.md")
        hechos = leer(carpeta, "hechos.md")
        etiquetas = re.findall(r"^\|\s*([^|\s][^|]*?)\s*\|", indice, flags=re.M)
        etiquetas = [e for e in etiquetas if e not in ("Nº", ":---") and not e.startswith(":")]
        self.assertTrue(etiquetas, "El índice de hechos está vacío")
        self.assertEqual(len(etiquetas), len(set(etiquetas)), "Etiquetas repetidas en hechos-indice.md")
        encabezados = re.findall(r"^## (.+?) ·", hechos, flags=re.M)
        self.assertEqual(sorted(etiquetas), sorted(encabezados),
                         "hechos-indice.md y hechos.md no tienen las mismas entradas")

    def test_un_punto_no_esta_a_la_vez_en_pendientes_y_en_hechos(self):
        pendientes = leer(BRAIN, "pendientes.md")
        en_pendientes = {m.rstrip(":").strip() for m in re.findall(r"^- \*\*([^*]+)\*\*", pendientes, flags=re.M)}
        indice = leer(BRAIN, "archive", "hechos-indice.md")
        en_hechos = set(re.findall(r"^\|\s*([^|\s][^|]*?)\s*\|", indice, flags=re.M))
        self.assertEqual(en_pendientes & en_hechos, set(),
                         "Un punto figura a la vez como pendiente y como hecho")

    def test_enlaces_de_los_indices_apuntan_a_archivos_reales(self):
        for rel in ("decisions/indice.md", "../CLAUDE.md", "../GEMINI.md", "../AGENTS.md", "referencias.md"):
            if not os.path.exists(os.path.join(BRAIN, rel)):
                continue  # kit de arranque: solo existen los índices de las IA elegidas
            base = os.path.dirname(os.path.join(BRAIN, rel))
            for destino in re.findall(r"\]\(([^)#\s]+)\)", leer(BRAIN, rel)):
                if destino.startswith(("http://", "https://", "mailto:")):
                    continue
                self.assertTrue(os.path.exists(os.path.join(base, destino)),
                                "Enlace roto en %s: %s" % (rel, destino))

    def test_topes_de_tamano(self):
        c = cfg()
        self.assertLessEqual(os.path.getsize(os.path.join(RAIZ, c["pendientes"])), c["tope_pendientes_bytes"],
                             "pendientes.md pasó su tope: transferir lo probado a archive/hechos.md")
        for indice in c.get("indices_entrada", [c["claude_md"]]):
            copia = os.path.join(BRAIN, "archive", "adoptado", os.path.splitext(indice)[0] + ".original.md")
            if os.path.exists(copia):  # spec 015: índice adoptado, su reparto en .brain/ está pendiente; el tope vuelve al acortarlo
                continue
            self.assertLessEqual(os.path.getsize(os.path.join(RAIZ, indice)), c["tope_claude_md_bytes"],
                                 "%s pasó su tope: es un índice, no un manual" % indice)

    def test_cada_spec_declara_su_estado(self):
        carpeta = os.path.join(BRAIN, "specs")
        for f in sorted(os.listdir(carpeta)):
            if f.endswith(".md") and "borrador" not in f:  # los «borrador-*» son textos de ayuda, no specs
                self.assertRegex(leer(carpeta, f), r"(?i)estado|status", "La spec %s no declara su estado" % f)

    def test_registro_de_decisiones_con_formato_de_linea(self):
        # Solo se exige a las entradas recientes: las antiguas tienen formatos anteriores.
        lineas = [l for l in leer(BRAIN, "decisions.log").splitlines() if l.strip()][-10:]
        malas = [l[:60] for l in lineas if not re.match(r"^\d{4}-\d{2}-\d{2} \|", l)]
        self.assertEqual(malas, [], "Entradas recientes de decisions.log sin fecha al inicio")


class TestGuardianCierre(unittest.TestCase):

    def setUp(self):
        self.cierre = cargar_cierre()
        self.cfg = cfg()

    def test_codigo_sin_registro_avisa(self):
        avisos = self.cierre.evaluar(["server.py"], 1000, self.cfg)
        self.assertEqual(len(avisos), 1)
        self.assertIn("decisions.log", avisos[0])

    def test_codigo_con_registro_no_avisa(self):
        self.assertEqual(self.cierre.evaluar(["server.py", ".brain/decisions.log"], 1000, self.cfg), [])

    def test_archivos_ignorados_no_cuentan(self):
        cambios = ["__pycache__/x.pyc", "component_flows.json.migrado", ".brain/pendientes.md"]
        self.assertEqual(self.cierre.evaluar(cambios, 1000, self.cfg), [])

    def test_respuesta_sin_ediciones_no_avisa(self):
        self.assertEqual(self.cierre.evaluar(["server.py"], 1000, self.cfg, hubo_ediciones=False), [])

    def test_pendientes_grande_avisa(self):
        avisos = self.cierre.evaluar([], self.cfg["tope_pendientes_bytes"] + 1, self.cfg)
        self.assertEqual(len(avisos), 1)
        self.assertIn("hechos.md", avisos[0])

    def test_registro_de_tarea_anterior_sin_commitear_no_tapa_el_aviso(self):
        cambios = ["server.py", ".brain/decisions.log"]
        avisos = self.cierre.evaluar(cambios, 1000, self.cfg, True, registro_en_respuesta=False)
        self.assertEqual(len(avisos), 1)

    def test_spec031_cambio_ajeno_no_se_atribuye_al_chat(self):
        # el chat solo editó un archivo ignorado; tests/x.py lo trajo /actualizar
        cambios = ["tests/x.py", ".brain/guardianes/guardianes.json"]
        self.assertEqual(self.cierre.evaluar(cambios, 1000, self.cfg, True, False, [".brain/guardianes/guardianes.json"]), [])

    def test_spec031_lo_que_edito_el_chat_si_avisa(self):
        cambios = ["tests/x.py", "server.py"]
        avisos = self.cierre.evaluar(cambios, 1000, self.cfg, True, False, ["server.py"])
        self.assertEqual(len(avisos), 1)
        self.assertIn("server.py", avisos[0])
        self.assertNotIn("tests/x.py", avisos[0])

    def test_spec031_chat_solo_de_terminal_avisa_como_antes(self):
        avisos = self.cierre.evaluar(["server.py"], 1000, self.cfg, True, False, [])
        self.assertEqual(len(avisos), 1)

    def test_spec033_bloque_abierto_no_pide_linea(self):
        self.assertEqual(self.cierre.evaluar(["server.py"], 1000, self.cfg, True, False, ["server.py"], sin_cerrar=3), [])

    def test_spec033_bloque_grande_pide_linea(self):
        avisos = self.cierre.evaluar(["server.py"], 1000, self.cfg, True, False, ["server.py"], sin_cerrar=15)
        self.assertEqual(len(avisos), 1)

    def test_spec033_desactivado_pide_en_cada_respuesta(self):
        cfg2 = dict(self.cfg, cierre_por_bloque=False)
        self.assertEqual(len(self.cierre.evaluar(["server.py"], 1000, cfg2, True, False, ["server.py"], sin_cerrar=1)), 1)

    def test_spec033_sin_dato_se_comporta_como_antes(self):
        self.assertEqual(len(self.cierre.evaluar(["server.py"], 1000, self.cfg, True, False, ["server.py"], sin_cerrar=None)), 1)

    def test_spec033_pendientes_gordo_avisa_aunque_el_bloque_siga_abierto(self):
        avisos = self.cierre.evaluar([], self.cfg["tope_pendientes_bytes"] + 1, self.cfg, True, False, [], sin_cerrar=0)
        self.assertEqual(len(avisos), 1)

    def test_spec033_cuenta_ediciones_desde_el_ultimo_cierre(self):
        import tempfile
        cfg = self.cfg
        def uso(nombre, ruta=None, cmd=None):
            entrada = {"file_path": os.path.join(RAIZ, ruta)} if ruta else {"command": cmd}
            return {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": nombre, "input": entrada}]}}
        filas = [uso("Edit", "a.py"), uso("Edit", "b.py"), uso("Bash", cmd="python cerrar.py x"),
                 uso("Edit", "c.py"), uso("Write", ".brain/pendientes.md"), uso("Edit", "d.py")]
        ruta = os.path.join(tempfile.mkdtemp(), "t.jsonl")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("\n".join(json.dumps(x) for x in filas))
        self.assertEqual(self.cierre.ediciones_sin_cerrar(ruta, cfg, RAIZ), 2)  # c.py y d.py; .brain/ no cuenta
        self.assertIsNone(self.cierre.ediciones_sin_cerrar(ruta + ".no", cfg, RAIZ))

    def _transcript(self, bloques):
        import json, tempfile
        ruta = os.path.join(tempfile.mkdtemp(), "t.jsonl")
        filas = [{"type": "user", "message": {"content": "hola"}},
                 {"type": "assistant", "message": {"content": bloques}}]
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("\n".join(json.dumps(x) for x in filas))
        return ruta

    def test_analiza_respuesta_edicion_y_registro(self):
        solo_codigo = self._transcript([{"type": "tool_use", "name": "Edit", "input": {"file_path": "C:/x/server.py"}}])
        self.assertEqual(self.cierre.analizar_respuesta(solo_codigo, ".brain/decisions.log"), (True, False))
        con_registro = self._transcript([
            {"type": "tool_use", "name": "Edit", "input": {"file_path": "C:/x/server.py"}},
            {"type": "tool_use", "name": "Bash", "input": {"command": "echo x >> .brain/decisions.log"}}])
        self.assertEqual(self.cierre.analizar_respuesta(con_registro, ".brain/decisions.log"), (True, True))

    def test_cerrar_py_cuenta_como_registro(self):
        ruta = self._transcript([
            {"type": "tool_use", "name": "Edit", "input": {"file_path": "C:/x/server.py"}},
            {"type": "tool_use", "name": "Bash", "input": {"command": "python .brain/guardianes/cerrar.py \"algo\" --chat X"}}])
        self.assertEqual(self.cierre.analizar_respuesta(ruta, ".brain/decisions.log"), (True, True))

    def test_aviso_sale_en_utf8(self):
        import subprocess, sys
        ruta = self._transcript([{"type": "tool_use", "name": "Edit", "input": {"file_path": "C:/x/README.md"}}])
        entrada = '{"transcript_path": %s}' % __import__("json").dumps(ruta)
        r = subprocess.run([sys.executable, os.path.join(GUARDIANES, "cierre.py")], input=entrada,
                           capture_output=True, text=True, encoding="utf-8")
        if r.returncode == 2:  # solo hay aviso si el repo tiene cambios sin registrar
            self.assertIn("línea", r.stderr)


def cargar_guardian(nombre):
    spec = importlib.util.spec_from_file_location(nombre, os.path.join(GUARDIANES, nombre + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestGuardianArranqueYCierreRapido(unittest.TestCase):
    """Spec 047: guardián de arranque, fichas con archivos y cierre rápido."""

    def test_cuenta_puntos_de_pendientes_por_seccion(self):
        arranque = cargar_guardian("arranque")
        texto = "# P\n## Falta\n- **1:** a\n- **2:** b\n## Prueba\n- **3:** c\n## Vacía\nsolo texto\n"
        self.assertEqual(arranque.contar_pendientes(texto), {"Falta": 2, "Prueba": 1})

    def test_resumen_de_arranque_del_proyecto_real(self):
        arranque = cargar_guardian("arranque")
        texto = arranque.resumen(RAIZ, dict(cfg(), poda_activa=False))  # el test nunca mueve archivos reales
        self.assertIn("Pendientes:", texto)
        self.assertIn("pendientes.md", texto)

    def test_ficha_desfasada_se_detecta_y_la_revisada_no(self):
        import subprocess, tempfile
        arranque = cargar_guardian("arranque")
        raiz = tempfile.mkdtemp()

        def g(*a, fecha=None):
            entorno = dict(os.environ, GIT_AUTHOR_DATE=fecha or "", GIT_COMMITTER_DATE=fecha or "") if fecha else None
            subprocess.run(["git"] + list(a), cwd=raiz, check=True, capture_output=True, env=entorno)

        g("init", "-q")
        g("config", "user.email", "t@t")
        g("config", "user.name", "t")
        os.makedirs(os.path.join(raiz, ".brain", "decisions"))
        with open(os.path.join(raiz, "mod.py"), "w") as f:
            f.write("x = 1\n")
        ficha = os.path.join(raiz, ".brain", "decisions", "D-001-prueba.md")
        with open(ficha, "w", encoding="utf-8") as f:
            f.write("# D-001\n- **Fecha:** 2026-01-01\n- **Archivos:** `mod.py`\n")
        g("add", ".")
        g("commit", "-q", "-m", "a", fecha="2026-02-01T10:00:00")
        self.assertEqual(arranque.fichas_a_revisar(raiz), [("D-001-prueba.md", "mod.py", "2026-02-01")])
        with open(ficha, "a", encoding="utf-8") as f:
            f.write("- **Revisada:** 2026-03-01\n")
        self.assertEqual(arranque.fichas_a_revisar(raiz), [])

    def test_arranque_imprime_json_visible_y_de_contexto(self):
        import subprocess, sys
        r = subprocess.run([sys.executable, os.path.join(GUARDIANES, "arranque.py")], input="{}",
                           capture_output=True, text=True, encoding="utf-8",
                           env=dict(os.environ, CEREBRO_SIN_PODA="1", CEREBRO_NO_ARCHIVAR_TRASPASO="1"))  # el test nunca mueve archivos reales (ni archiva el traspaso)
        datos = json.loads(r.stdout)
        self.assertIn("Pendientes:", datos["systemMessage"])
        self.assertEqual(datos["hookSpecificOutput"]["hookEventName"], "SessionStart")
        self.assertIn("Pendientes:", datos["hookSpecificOutput"]["additionalContext"])

    def test_linea_de_registro_con_formato(self):
        cerrar = cargar_guardian("cerrar")
        self.assertEqual(cerrar.linea_registro("2026-10-28", "Claude", "Proyecto #39", "  hizo   algo ", "SDD"),
                         "2026-10-28 | Claude (Proyecto #39) | hizo algo | SDD")
        with self.assertRaises(ValueError):
            cerrar.linea_registro("2026-10-28", "Claude", "x", "", "SDD")
        with self.assertRaises(ValueError):
            cerrar.linea_registro("2026-10-28", "Claude", "x", "algo", "Otro")

    def _cerebro_falso(self):
        """Copia mínima de .brain/ en una carpeta temporal (spec 083): nunca se toca el cerebro real."""
        import tempfile
        base = tempfile.mkdtemp()
        self.addCleanup(__import__("shutil").rmtree, base, True)
        for sub in ("decisions", "archive"):
            os.makedirs(os.path.join(base, sub))
        esc = lambda ruta, txt: open(os.path.join(base, *ruta), "w", encoding="utf-8", newline="").write(txt)
        esc(("decisions", "indice.md"), "# Índice\n\n| ID | Decisión | Área | Estado |\n| :--- | :--- | :--- | :--- |\n"
            "| [D-001](D-001-uno.md) | Uno | Proceso | vigente || [D-002](D-002-dos.md) | Dos | Proceso | vigente |\n")
        esc(("decisions", "D-001-uno.md"), "# D-001: Uno\n\n- **Estado:** vigente\n- **Área:** Proceso\n")
        esc(("decisions", "D-002-dos.md"), "# D-002: Dos\n\n- **Estado:** vigente\n- **Área:** Proceso\n")
        esc(("decisions", "D-003-tres.md"), "# D-003: Tres\n\n- **Estado:** vigente\n- **Área:** Negocio\n")
        esc(("pendientes.md",),"# P\n\n## Falta\n- **7:** algo\n- **8 (resto):** otro\n")
        esc(("archive", "hechos.md"), "# Hechos\n\n## 5 · Viejo\n**Fecha:** 2026-01-01 · **Ref:** x\nd\n")
        esc(("archive", "hechos-indice.md"), "# Índice\n\n| Nº | Qué | Fecha | Ref. |\n| :--- | :--- | :--- | :--- |\n| 5 | Viejo | 2026-01-01 | x |\n")
        return base

    def test_indices_anade_solo_lo_que_falta_y_separa_filas_pegadas(self):
        ind = cargar_guardian("indices")
        base = self._cerebro_falso()
        texto, filas = ind.filas_decisiones_faltantes(base)
        self.assertEqual(len(filas), 1)
        self.assertIn("[D-003](D-003-tres.md) | Tres | Negocio | vigente", filas[0])
        self.assertNotIn("||", texto)
        self.assertEqual(texto.count("| [D-001]"), 1)
        ind.escribir(os.path.join(base, "decisions", "indice.md"), texto)
        self.assertEqual(ind.filas_decisiones_faltantes(base)[1], [])  # segunda vez: nada que añadir

    def test_hecho_mueve_el_punto_y_el_indice_lo_acepta(self):
        ind = cargar_guardian("indices")
        base = self._cerebro_falso()
        pend, hechos, indice = ind.pasar_a_hechos(base, "7", "Tarea siete", "Probada.", "spec 1", "2026-11-01")
        self.assertNotIn("**7:**", pend)
        self.assertIn("**8 (resto):**", pend)
        self.assertLess(hechos.index("## 7 · Tarea siete"), hechos.index("## 5 · Viejo"))
        self.assertIn("| 7 | Tarea siete | 2026-11-01 | spec 1 |", indice)
        etiquetas = re.findall(r"^\|\s*(\d+)\s*\|", indice, flags=re.M)
        self.assertEqual(sorted(etiquetas), sorted(re.findall(r"^## (\d+) ·", hechos, flags=re.M)))

    def test_hecho_no_duplica_ni_inventa_y_conservar_deja_el_punto(self):
        ind = cargar_guardian("indices")
        base = self._cerebro_falso()
        with self.assertRaises(ValueError):
            ind.pasar_a_hechos(base, "5", "x", "x", "x", "2026-11-01")   # ya está en hechos
        with self.assertRaises(ValueError):
            ind.pasar_a_hechos(base, "99", "x", "x", "x", "2026-11-01")  # no está en pendientes
        pend, _, _ = ind.pasar_a_hechos(base, "8 (resto)".split()[0], "Parte", "d", "r", "2026-11-01", conservar=True)
        self.assertIn("**8 (resto):**", pend)

    def test_hooks_de_arranque_y_cierre_configurados(self):
        hooks = json.loads(leer(RAIZ, ".claude", "settings.json"))["hooks"]
        self.assertIn("arranque.py", json.dumps(hooks["SessionStart"]))
        self.assertIn("cierre.py", json.dumps(hooks["Stop"]))


if __name__ == "__main__":
    unittest.main()

