# -*- coding: utf-8 -*-
"""Spec 090, fase 2: proyectos y simulaciones. Permisos por rol, lista cerrada de acciones, solo proyectos registrados, las simulaciones
no escriben nada en el proyecto, y los POST exigen clave en la cabecera, origen propio y un token de un solo uso."""
import importlib.util
import json
import os
import shutil
import tempfile
import threading
import unittest
import urllib.error
import urllib.request

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GUARD = os.path.join(RAIZ, ".brain", "guardianes")


def _cargar(nombre, archivo):
    espec = importlib.util.spec_from_file_location(nombre, os.path.join(GUARD, archivo))
    mod = importlib.util.module_from_spec(espec)
    espec.loader.exec_module(mod)
    return mod


web = _cargar("web", "web.py")
capa = web._capa
act = _cargar("actualizar_arnes_t", "actualizar_arnes.py")


def poner(base, rel, texto):
    ruta = os.path.join(base, *rel.split("/"))
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)


def arbol(base):
    res = {}
    for carpeta, _, nombres in os.walk(base):
        for n in nombres:
            ruta = os.path.join(carpeta, n)
            with open(ruta, "rb") as f:
                res[os.path.relpath(ruta, base)] = f.read()
    return res


class Base(unittest.TestCase):
    def setUp(self):
        self.repo, self.proy, self.otro = tempfile.mkdtemp(), tempfile.mkdtemp(), tempfile.mkdtemp()
        for d in (self.repo, self.proy, self.otro):
            self.addCleanup(shutil.rmtree, d, True)
        # repo del arnés de mentira, con un solo archivo repartible
        poner(self.repo, ".brain/guardianes/uno.py", "# uno v2\n")
        huella = act.huella(act._normalizar(act.leer_bytes(os.path.join(self.repo, ".brain", "guardianes", "uno.py")), ".brain/guardianes/uno.py"))
        poner(self.repo, "manifiesto.json", json.dumps({"version": "9.9.9", "archivos": {".brain/guardianes/uno.py": huella}, "pruebas": []}))
        poner(self.repo, "VERSION", "9.9.9\n")
        # proyecto con arnés viejo
        poner(self.proy, ".brain/guardianes/guardianes.json", json.dumps({"idioma": "es"}))
        poner(self.proy, ".brain/pendientes.md", "# Pendientes\n- algo\n")
        poner(self.proy, ".brain/guardianes/uno.py", "# uno v1\n")
        self.dueno = capa.USUARIO_LOCAL
        # ruta del registro del actualizador: la leemos del propio actualizador
        self.registro = os.path.join(self.proy, act.REGISTRO)
        os.makedirs(os.path.dirname(self.registro), exist_ok=True)
        with open(self.registro, "w", encoding="utf-8") as f:
            json.dump({"version": "1.0.0", "nivel": "completo", "archivos": {}}, f)

    def registrar(self, ruta=None):
        return capa.ejecutar(self.repo, self.dueno, "registrar_proyecto", datos={"ruta": ruta or self.proy})


class TestPermisos(Base):
    def test_matriz_de_roles_y_acciones(self):
        esperado = {
            "lectura": {"ver_proyectos"},
            "colaborador": {"ver_proyectos"},
            "dueno": set(capa.ACCIONES),
        }
        for rol, validas in esperado.items():
            for accion in capa.ACCIONES:
                self.assertEqual(capa.permitido({"rol": rol}, accion), accion in validas, (rol, accion))

    def test_lo_desconocido_se_deniega(self):
        self.assertFalse(capa.permitido({"rol": "superdueno"}, "ver_proyectos"))
        self.assertFalse(capa.permitido({"rol": "dueno"}, "borrar_todo"))
        self.assertFalse(capa.permitido(None, "ver_proyectos"))
        self.assertFalse(capa.permitido({}, "ver_proyectos"))

    def test_sin_permiso_no_se_hace_y_queda_anotado(self):
        codigo, _ = capa.ejecutar(self.repo, {"nombre": "ia", "rol": "lectura"}, "registrar_proyecto", datos={"ruta": self.proy})
        self.assertEqual(codigo, 403)
        self.assertEqual(capa.cargar_proyectos(self.repo), [])
        with open(os.path.join(self.repo, ".brain", "web_actividad.log"), encoding="utf-8") as f:
            linea = json.loads(f.read().splitlines()[-1])
        self.assertEqual((linea["quien"], linea["accion"], linea["resultado"]), ("ia", "registrar_proyecto", "denegado"))

    def test_accion_desconocida(self):
        self.assertEqual(capa.ejecutar(self.repo, self.dueno, "ejecutar_comando", datos={"x": "rm -rf /"})[0], 404)


class TestProyectos(Base):
    def test_registrar_y_ver(self):
        codigo, res = self.registrar()
        self.assertEqual(codigo, 200)
        self.assertEqual(res["proyecto"]["version"], "1.0.0")
        self.assertTrue(res["proyecto"]["atrasado"])
        codigo, res = capa.ejecutar(self.repo, self.dueno, "ver_proyectos")
        self.assertEqual(codigo, 200)
        self.assertEqual([p["ruta"] for p in res["proyectos"]], [os.path.abspath(self.proy)])
        self.assertIn("algo", res["proyectos"][0]["pendientes"])

    def test_no_acepta_rutas_malas_ni_repetidas(self):
        self.assertEqual(self.registrar(os.path.join(self.repo, "no_existe"))[0], 400)
        self.assertEqual(self.registrar(self.repo)[0], 400)  # el propio repo del arnés
        self.assertEqual(capa.ejecutar(self.repo, self.dueno, "registrar_proyecto", datos={"ruta": 5})[0], 400)
        self.assertEqual(capa.ejecutar(self.repo, self.dueno, "registrar_proyecto", datos={"ruta": "a\x00b"})[0], 400)
        self.assertEqual(self.registrar()[0], 200)
        self.assertEqual(self.registrar()[0], 400)
        self.assertEqual(len(capa.cargar_proyectos(self.repo)), 1)

    def test_registrar_no_toca_la_carpeta_del_proyecto(self):
        antes = arbol(self.proy)
        self.registrar()
        self.assertEqual(arbol(self.proy), antes)

    def test_fuera_del_repo_del_arnes_no_se_gobierna(self):
        os.remove(os.path.join(self.repo, "manifiesto.json"))
        self.assertEqual(capa.ejecutar(self.repo, self.dueno, "ver_proyectos")[0], 409)

    def test_el_prefijo_de_windows_no_salta_las_guardas(self):  # revisión aparte A1
        self.assertEqual(self.registrar("\\\\?\\" + os.path.abspath(self.repo))[0], 400)
        self.assertEqual(self.registrar()[0], 200)
        self.assertEqual(self.registrar("\\\\?\\" + os.path.abspath(self.proy))[0], 400)
        self.assertEqual(len(capa.cargar_proyectos(self.repo)), 1)

    def test_una_ruta_relativa_no_se_acepta(self):  # revisión aparte B2
        self.assertEqual(self.registrar("carpeta/relativa")[0], 400)
        self.assertEqual(self.registrar(".")[0], 400)

    def test_registros_a_la_vez_no_se_pisan(self):  # revisión aparte A3
        carpetas = [tempfile.mkdtemp() for _ in range(12)]
        for c in carpetas:
            self.addCleanup(shutil.rmtree, c, True)
        codigos = []
        hilos = [threading.Thread(target=lambda c=c: codigos.append(self.registrar(c)[0])) for c in carpetas]
        for h in hilos:
            h.start()
        for h in hilos:
            h.join()
        self.assertEqual(codigos, [200] * 12)
        self.assertEqual(len(capa.cargar_proyectos(self.repo)), 12)

    def test_un_enlace_que_sale_de_brain_no_se_lee_como_pendientes(self):  # revisión aparte B1
        fuera = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, fuera, True)
        poner(fuera, "secreto.md", "SECRETO")
        os.remove(os.path.join(self.proy, ".brain", "pendientes.md"))
        try:
            os.symlink(os.path.join(fuera, "secreto.md"), os.path.join(self.proy, ".brain", "pendientes.md"))
        except (OSError, NotImplementedError):
            self.skipTest("sin permiso para crear enlaces simbólicos")
        self.registrar()
        ficha = capa.ejecutar(self.repo, self.dueno, "ver_proyectos")[1]["proyectos"][0]
        self.assertNotIn("SECRETO", ficha["pendientes"])

    def test_la_actividad_no_deja_de_anotarse_al_pasar_el_tope(self):  # revisión aparte A2
        ruta = os.path.join(self.repo, ".brain", "web_actividad.log")
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("x" * (capa.TOPE_ACTIVIDAD + 10))
        capa.ejecutar(self.repo, {"nombre": "ia", "rol": "lectura"}, "registrar_proyecto", datos={"ruta": self.proy})
        with open(ruta, encoding="utf-8") as f:
            self.assertEqual(json.loads(f.read().splitlines()[-1])["resultado"], "denegado")
        archivados = os.listdir(os.path.join(self.repo, ".brain", "archive"))
        self.assertTrue(any(a.startswith("web_actividad-") for a in archivados))  # lo viejo se movió, no se borró


class TestSimulaciones(Base):
    def test_simular_actualizar_cuenta_y_no_escribe(self):
        self.registrar()
        antes = arbol(self.proy)
        codigo, res = capa.ejecutar(self.repo, self.dueno, "simular_actualizar", ruta=self.proy)
        self.assertEqual(codigo, 200, res)
        self.assertIn("9.9.9", res["texto"])
        self.assertEqual(arbol(self.proy), antes)  # ni un archivo cambiado ni creado (ni copias de seguridad)

    def test_simular_instalar_no_escribe_en_una_carpeta_vacia(self):
        self.registrar(self.otro)
        for nivel in capa.NIVELES:
            codigo, res = capa.ejecutar(self.repo, self.dueno, "simular_instalar", ruta=self.otro, datos={"nivel": nivel})
            self.assertEqual(codigo, 200, (nivel, res))
            self.assertIn(nivel, res["texto"])
            self.assertEqual(os.listdir(self.otro), [], nivel)

    def test_simular_instalar_avisa_de_lo_que_copia_el_actualizador(self):
        poner(self.repo, ".brain/guardianes/dos.py", "# dos\n")
        import json as _j
        with open(os.path.join(self.repo, "manifiesto.json"), encoding="utf-8") as f:
            m = _j.load(f)
        m["archivos"][".brain/guardianes/dos.py"] = "x"
        with open(os.path.join(self.repo, "manifiesto.json"), "w", encoding="utf-8") as f:
            _j.dump(m, f)
        self.assertEqual(capa._archivos_del_actualizador(self.repo, self.otro, []), 2)  # carpeta vacía: faltan los dos
        self.assertEqual(capa._archivos_del_actualizador(self.repo, self.proy, []), 1)  # uno.py ya lo tiene, dos.py no
        self.assertEqual(capa._archivos_del_actualizador(self.repo, self.otro, [os.path.join(self.otro, ".brain", "guardianes", "uno.py")]), 1)

    def test_nivel_no_valido(self):
        self.registrar(self.otro)
        self.assertEqual(capa.ejecutar(self.repo, self.dueno, "simular_instalar", ruta=self.otro, datos={"nivel": "ligero; rm"})[0], 400)
        self.assertEqual(capa.ejecutar(self.repo, self.dueno, "simular_instalar", ruta=self.otro, datos={})[0], 400)

    def test_solo_proyectos_registrados(self):
        for ruta in (self.proy, os.path.join(self.proy, ".."), "", None, 7, "x\x00"):
            self.assertEqual(capa.ejecutar(self.repo, self.dueno, "simular_actualizar", ruta=ruta)[0], 404, ruta)
        self.registrar()
        self.assertEqual(capa.ejecutar(self.repo, self.dueno, "simular_actualizar", ruta=self.otro)[0], 404)


class TestReales(Base):
    """Fase 3: lo que cambia el proyecto. Solo el dueño, solo tras simular, una sola vez y una a la vez por carpeta."""

    def ejecutar(self, accion, usuario=None, **datos):
        return capa.ejecutar(self.repo, usuario or self.dueno, accion, os.path.abspath(self.proy), datos)

    def test_actualizar_real_exige_simulacion_previa(self):
        self.registrar()
        antes = arbol(self.proy)
        codigo, res = self.ejecutar("actualizar_real")
        self.assertEqual(codigo, 409)
        self.assertEqual(arbol(self.proy), antes)

    def test_actualizar_real_tras_simular_cambia_el_proyecto_una_vez(self):
        rel = ".brain/guardianes/uno.py"  # el archivo del proyecto coincide con lo que el actualizador instaló: no está «tocado a mano»
        with open(self.registro, "w", encoding="utf-8") as f:
            json.dump({"version": "1.0.0", "nivel": "completo", "archivos": {rel: act.huella(act._normalizar(b"# uno v1\n", rel))}}, f)
        self.registrar()
        self.assertEqual(self.ejecutar("simular_actualizar")[0], 200)
        codigo, res = self.ejecutar("actualizar_real")
        self.assertEqual(codigo, 200, res)
        with open(os.path.join(self.proy, ".brain", "guardianes", "uno.py"), encoding="utf-8") as f:
            self.assertIn("v2", f.read())
        self.assertEqual(self.ejecutar("actualizar_real")[0], 409)  # la simulación vale una sola vez

    def test_la_simulacion_caduca(self):
        self.registrar()
        self.ejecutar("simular_actualizar")
        with capa.CERROJO_ESTADO:
            for k in list(capa.SIMULADAS):
                capa.SIMULADAS[k] -= capa.VIDA_SIMULACION + 5
        self.assertEqual(self.ejecutar("actualizar_real")[0], 409)

    def test_solo_el_dueno_y_queda_anotado(self):
        self.registrar()
        self.ejecutar("simular_actualizar")
        for rol in ("lectura", "colaborador"):
            self.assertEqual(self.ejecutar("actualizar_real", {"nombre": "x", "rol": rol})[0], 403)
        with open(os.path.join(self.repo, ".brain", "web_actividad.log"), encoding="utf-8") as f:
            self.assertIn('"resultado": "denegado"', f.read())

    def test_proyecto_no_registrado_no_se_toca(self):
        antes = arbol(self.otro)
        self.assertEqual(capa.ejecutar(self.repo, self.dueno, "actualizar_real", os.path.abspath(self.otro))[0], 404)
        self.assertEqual(capa.ejecutar(self.repo, self.dueno, "instalar_real", os.path.abspath(self.otro), {"nivel": "ligero"})[0], 404)
        self.assertEqual(arbol(self.otro), antes)

    def test_una_accion_por_proyecto_a_la_vez(self):
        self.registrar()
        self.ejecutar("simular_actualizar")
        with capa.CERROJO_ESTADO:
            capa.OCUPADOS.add(capa._clave(self.proy))
        try:
            codigo, res = self.ejecutar("actualizar_real")
            self.assertEqual(codigo, 409)
            self.assertIn("en marcha", res["error"])
        finally:
            with capa.CERROJO_ESTADO:
                capa.OCUPADOS.clear()

    def test_la_simulacion_se_gasta_aunque_la_accion_falle_y_no_autoriza_dos(self):  # revisión aparte, hallazgos 1 y 2
        self.registrar()
        self.ejecutar("simular_actualizar")
        original = capa.actualizar_real
        capa.actualizar_real = lambda *a: (_ for _ in ()).throw(OSError("falla"))
        try:
            self.assertEqual(self.ejecutar("actualizar_real")[0], 500)
        finally:
            capa.actualizar_real = original
        self.assertEqual(self.ejecutar("actualizar_real")[0], 409)  # hay que simular otra vez

    def test_una_simulacion_hecha_durante_otra_accion_no_se_hace_ni_vale(self):  # hallazgo 3 (auditoría externa): la simulación ocupa la carpeta
        self.registrar()
        with capa.CERROJO_ESTADO:
            capa.OCUPADOS.add(capa._clave(self.proy))
        try:
            self.assertEqual(self.ejecutar("simular_actualizar")[0], 409)
            self.assertEqual(self.ejecutar("simular_instalar", nivel="ligero")[0], 409)
        finally:
            with capa.CERROJO_ESTADO:
                capa.OCUPADOS.clear()
        self.assertEqual(self.ejecutar("actualizar_real")[0], 409)  # no quedó ninguna simulación que autorice

    def test_la_simulacion_reserva_la_carpeta_mientras_corre_y_la_libera(self):  # hallazgo 3
        self.registrar()
        visto = []
        original = capa.simular_actualizar
        capa.simular_actualizar = lambda *a: visto.append(capa._clave(self.proy) in capa.OCUPADOS) or "x"
        try:
            self.assertEqual(self.ejecutar("simular_actualizar")[0], 200)
        finally:
            capa.simular_actualizar = original
        self.assertEqual(visto, [True])
        self.assertEqual(capa.OCUPADOS, set())

    def test_la_simulacion_libera_la_carpeta_aunque_falle(self):
        self.registrar()
        original = capa.simular_actualizar
        capa.simular_actualizar = lambda *a: (_ for _ in ()).throw(OSError("falla"))
        try:
            self.assertEqual(self.ejecutar("simular_actualizar")[0], 500)
        finally:
            capa.simular_actualizar = original
        self.assertEqual(capa.OCUPADOS, set())

    def test_se_libera_aunque_falle(self):
        self.registrar()
        self.ejecutar("simular_actualizar")
        original = capa.actualizar_real
        capa.actualizar_real = lambda *a: (_ for _ in ()).throw(OSError("falla"))
        try:
            with self.assertRaises(OSError):
                capa._real(self.repo, self.dueno, "actualizar_real", os.path.abspath(self.proy), "")
        finally:
            capa.actualizar_real = original
        self.assertEqual(capa.OCUPADOS, set())

    def test_instalar_real_exige_simular_ese_mismo_nivel(self):
        self.registrar(self.otro)
        self.assertEqual(capa.ejecutar(self.repo, self.dueno, "simular_instalar", os.path.abspath(self.otro), {"nivel": "ligero"})[0], 200)
        antes = arbol(self.otro)
        codigo, _ = capa.ejecutar(self.repo, self.dueno, "instalar_real", os.path.abspath(self.otro), {"nivel": "medio"})
        self.assertEqual(codigo, 409)
        self.assertEqual(arbol(self.otro), antes)
        self.assertEqual(capa.ejecutar(self.repo, self.dueno, "instalar_real", os.path.abspath(self.otro), {"nivel": "ninguno"})[0], 400)

    def test_textos_de_la_fase_3_en_los_dos_idiomas(self):
        textos = _cargar("textos_t", "textos.py").TEXTOS
        for clave in ("web_real_sin_pruebas", "web_real_instalar_titulo", "web_real_creo", "web_err_sin_simulacion", "web_err_ocupado",
                      "web_real_actualizar", "web_real_instalar", "web_confirma_actualizar", "web_confirma_instalar"):
            self.assertTrue(textos["es"].get(clave) and textos["en"].get(clave), clave)


class TestTareas(Base):
    """Fase 3: tareas del método en segundo plano. Comando fijo, solo en proyectos registrados, una por carpeta, con salida y parada."""

    def setUp(self):
        super().setUp()
        poner(self.proy, "tests/test_ok.py", "import unittest\nclass T(unittest.TestCase):\n    def test_a(self):\n        print('HOLA-PRUEBA')\n")
        poner(self.proy, ".brain/guardianes/cerrar.py", "import sys\nprint('ARGS', sys.argv[1:])\n")
        poner(self.proy, ".brain/guardianes/auditor.py", "import time\nprint('empieza', flush=True)\ntime.sleep(60)\n")
        self.registrar()
        self.ruta = os.path.abspath(self.proy)

    def tearDown(self):
        with capa.CERROJO_ESTADO:
            for j in capa.TRABAJOS.values():
                if j["estado"] == "corriendo":
                    j["proc"].kill()
        self.esperar_libre()

    def esperar_libre(self):
        import time
        for _ in range(100):
            with capa.CERROJO_ESTADO:
                if not capa.OCUPADOS:
                    return
            time.sleep(0.1)

    def lanzar(self, accion, usuario=None, **datos):
        return capa.ejecutar(self.repo, usuario or self.dueno, accion, self.ruta, datos)

    def terminar(self, job_id):
        import time
        for _ in range(150):
            e = capa.estado_tarea(job_id)
            if e["estado"] != "corriendo":
                return e
            time.sleep(0.1)
        self.fail("la tarea no terminó")

    def test_pruebas_corren_en_segundo_plano_y_dejan_salida(self):
        codigo, res = self.lanzar("tarea_pruebas")
        self.assertEqual(codigo, 200, res)
        e = self.terminar(res["id"])
        self.assertEqual((e["estado"], e["codigo"]), ("ok", 0))
        self.assertIn("Ran 1 test", e["salida"])
        with open(os.path.join(self.repo, ".brain", "web_actividad.log"), encoding="utf-8") as f:
            self.assertIn("iniciada", f.read())

    def test_cerrar_pasa_el_texto_como_argumento_no_como_orden(self):
        codigo, res = self.lanzar("tarea_cerrar", chat="proy #1", texto="--quien x; rm -rf / && echo hola")
        self.assertEqual(codigo, 200, res)
        e = self.terminar(res["id"])
        self.assertIn("['--chat', 'proy #1', '--', '--quien x; rm -rf / && echo hola']", e["salida"])

    def test_cerrar_valida_los_datos(self):
        for datos in ({}, {"chat": "a"}, {"texto": "a"}, {"chat": "a", "texto": "x" * 700}, {"chat": 5, "texto": "a"}, {"chat": "a", "texto": "  "}):
            self.assertEqual(self.lanzar("tarea_cerrar", **datos)[0], 400, datos)
        self.assertEqual(capa.OCUPADOS, set())

    def test_una_tarea_por_proyecto_a_la_vez_y_se_puede_parar(self):
        codigo, res = self.lanzar("tarea_auditor")
        self.assertEqual(codigo, 200, res)
        self.assertEqual(self.lanzar("tarea_pruebas")[0], 409)  # ocupado
        self.assertEqual(self.lanzar("actualizar_real")[0], 409)
        self.assertEqual(capa.ejecutar(self.repo, self.dueno, "parar_tarea", None, {"id": res["id"]})[0], 200)
        e = self.terminar(res["id"])
        self.assertEqual(e["estado"], "parada")
        self.esperar_libre()
        self.assertEqual(self.lanzar("tarea_pruebas")[0], 200)  # libre otra vez

    def test_parar_una_que_no_existe(self):
        self.assertEqual(capa.ejecutar(self.repo, self.dueno, "parar_tarea", None, {"id": "nada"})[0], 404)
        self.assertEqual(capa.ejecutar(self.repo, self.dueno, "parar_tarea", None, {"id": 5})[0], 404)

    def test_solo_el_dueno_y_solo_registrados(self):
        for rol in ("lectura", "colaborador"):
            for accion in ("tarea_pruebas", "tarea_auditor", "tarea_cerrar", "parar_tarea"):
                self.assertEqual(capa.ejecutar(self.repo, {"nombre": "x", "rol": rol}, accion, self.ruta, {})[0], 403, (rol, accion))
        self.assertEqual(capa.ejecutar(self.repo, self.dueno, "tarea_pruebas", os.path.abspath(self.otro), {})[0], 404)
        self.assertEqual(capa.OCUPADOS, set())

    def test_sin_tests_o_sin_guardian_no_arranca(self):
        shutil.rmtree(os.path.join(self.proy, "tests"))
        os.remove(os.path.join(self.proy, ".brain", "guardianes", "cerrar.py"))
        self.assertEqual(self.lanzar("tarea_pruebas")[0], 409)
        self.assertEqual(self.lanzar("tarea_cerrar", chat="a", texto="b")[0], 409)
        self.assertEqual(capa.OCUPADOS, set())

    def test_parar_mata_tambien_los_procesos_hijos(self):
        import time
        poner(self.proy, ".brain/guardianes/auditor.py", "import subprocess, sys, time\nh = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'])\nprint('HIJO', h.pid, flush=True)\ntime.sleep(60)\n")
        codigo, res = self.lanzar("tarea_auditor")
        self.assertEqual(codigo, 200, res)
        pid = None
        for _ in range(100):
            salida = capa.estado_tarea(res["id"])["salida"]
            if "HIJO" in salida:
                pid = int(salida.split("HIJO")[1].split()[0])
                break
            time.sleep(0.1)
        self.assertIsNotNone(pid)
        capa.ejecutar(self.repo, self.dueno, "parar_tarea", None, {"id": res["id"]})
        self.terminar(res["id"])
        vivo = True
        for _ in range(50):
            if os.name == "nt":
                import subprocess
                vivo = str(pid) in subprocess.run(["tasklist", "/FI", "PID eq %d" % pid], capture_output=True, text=True).stdout
            else:
                try:
                    os.kill(pid, 0)
                except OSError:
                    vivo = False
            if not vivo:
                break
            time.sleep(0.1)
        self.assertFalse(vivo, "el proceso hijo sigue vivo")

    @staticmethod
    def _vivo(pid):
        if os.name == "nt":
            import subprocess
            return str(pid) in subprocess.run(["tasklist", "/FI", "PID eq %d" % pid], capture_output=True, text=True).stdout
        try:
            os.kill(pid, 0)
        except OSError:
            return False
        return True

    def test_un_hijo_huerfano_no_sobrevive_a_la_tarea(self):  # hallazgo 2 (auditoría externa): el padre acaba y el hijo queda vivo
        import time
        poner(self.proy, ".brain/guardianes/auditor.py", "import subprocess, sys\nh = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'])\nprint('HIJO', h.pid, flush=True)\n")
        codigo, res = self.lanzar("tarea_auditor")
        self.assertEqual(codigo, 200, res)
        e = self.terminar(res["id"])
        pid = int(e["salida"].split("HIJO")[1].split()[0])
        for _ in range(50):
            if not self._vivo(pid):
                break
            time.sleep(0.1)
        self.assertFalse(self._vivo(pid), "el hijo huérfano sigue vivo tras acabar la tarea")
        self.esperar_libre()
        self.assertEqual(capa.OCUPADOS, set())

    def test_el_limite_de_tiempo_tambien_mata_a_los_hijos(self):  # hallazgo 2
        import time
        poner(self.proy, ".brain/guardianes/auditor.py", "import subprocess, sys, time\nh = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'])\nprint('HIJO', h.pid, flush=True)\ntime.sleep(60)\n")
        anterior, capa.LIMITE_TAREA = capa.LIMITE_TAREA, 2
        try:
            codigo, res = self.lanzar("tarea_auditor")
            self.assertEqual(codigo, 200, res)
            e = self.terminar(res["id"])
        finally:
            capa.LIMITE_TAREA = anterior
        self.assertEqual(e["estado"], "parada")
        pid = int(e["salida"].split("HIJO")[1].split()[0])
        for _ in range(50):
            if not self._vivo(pid):
                break
            time.sleep(0.1)
        self.assertFalse(self._vivo(pid))

    def _enlazar(self, destino, enlace):
        """Junction en Windows (no pide permisos), enlace simbólico en el resto. Devuelve False si el sistema no deja crearlo."""
        import subprocess
        try:
            if os.name == "nt":
                r = subprocess.run(["cmd", "/c", "mklink", "/J", enlace, destino], capture_output=True)
                return r.returncode == 0
            os.symlink(destino, enlace, target_is_directory=True)
            return True
        except OSError:
            return False

    def test_guardianes_enlazado_fuera_del_proyecto_no_se_ejecuta(self):  # hallazgo 1 (auditoría externa)
        fuera = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, fuera, True)
        poner(fuera, "auditor.py", "print('SE-EJECUTO-FUERA')\n")
        poner(fuera, "cerrar.py", "print('SE-EJECUTO-FUERA')\n")
        shutil.rmtree(os.path.join(self.proy, ".brain", "guardianes"))
        if not self._enlazar(fuera, os.path.join(self.proy, ".brain", "guardianes")):
            self.skipTest("este sistema no deja crear enlaces")
        try:
            self.assertEqual(self.lanzar("tarea_auditor")[0], 409)
            self.assertEqual(self.lanzar("tarea_cerrar", chat="a", texto="b")[0], 409)
            self.assertEqual(capa.OCUPADOS, set())
            self.assertTrue(os.path.isfile(os.path.join(fuera, "auditor.py")))  # el rechazo no tocó lo de fuera
        finally:
            try:
                os.rmdir(os.path.join(self.proy, ".brain", "guardianes"))  # quita solo el enlace, nunca lo de dentro
            except OSError:
                pass

    def test_brain_enlazado_fuera_del_proyecto_no_se_ejecuta(self):  # hallazgo 1, variante: el enlace está un nivel más arriba
        fuera = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, fuera, True)
        poner(fuera, "guardianes/auditor.py", "print('SE-EJECUTO-FUERA')\n")
        shutil.rmtree(os.path.join(self.proy, ".brain"))
        if not self._enlazar(fuera, os.path.join(self.proy, ".brain")):
            self.skipTest("este sistema no deja crear enlaces")
        try:
            self.assertEqual(self.lanzar("tarea_auditor")[0], 409)
        finally:
            try:
                os.rmdir(os.path.join(self.proy, ".brain"))
            except OSError:
                pass

    def test_textos_de_tareas_en_los_dos_idiomas(self):
        textos = _cargar("textos_t2", "textos.py").TEXTOS
        for clave in [k for k in textos["es"] if k.startswith("web_tarea") or k in ("web_t_tareas", "web_confirma_tarea", "web_confirma_cerrar", "web_err_sin_tests", "web_err_sin_guardian", "web_err_sin_tarea")]:
            self.assertTrue(textos["en"].get(clave), clave)


class TestHttp(Base):
    def setUp(self):
        super().setUp()
        self.srv, self.clave = web.crear(self.repo, 0)
        self.puerto = self.srv.server_address[1]
        threading.Thread(target=self.srv.serve_forever, daemon=True).start()
        self.addCleanup(self._parar)

    def _parar(self):
        self.srv.shutdown()
        self.srv.server_close()

    def pedir(self, ruta, metodo="GET", cuerpo=None, clave="auto", extra=None, tipo="application/json"):
        cab = dict(extra or {})
        if clave == "auto":
            clave = self.clave
        if clave is not None:
            cab["X-Clave"] = clave
        datos = None
        if cuerpo is not None:
            datos = cuerpo if isinstance(cuerpo, bytes) else json.dumps(cuerpo).encode("utf-8")
            cab["Content-Type"] = tipo
        req = urllib.request.Request("http://127.0.0.1:%d%s" % (self.puerto, ruta), data=datos, headers=cab, method=metodo)
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.status, r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode("utf-8")

    def token(self, accion):
        return json.loads(self.pedir("/api/token?a=" + accion)[1])["token"]

    def accion(self, accion, **datos):
        datos.update(accion=accion, token=self.token(accion))
        return self.pedir("/api/accion", "POST", datos)

    def test_flujo_completo_por_http(self):
        c, cuerpo = self.accion("registrar_proyecto", ruta=self.proy)
        self.assertEqual(c, 200, cuerpo)
        c, cuerpo = self.pedir("/api/proyectos")
        self.assertEqual(json.loads(cuerpo)["proyectos"][0]["nombre"], os.path.basename(self.proy))
        antes = arbol(self.proy)
        c, cuerpo = self.accion("simular_actualizar", ruta=self.proy)
        self.assertEqual(c, 200, cuerpo)
        self.assertEqual(arbol(self.proy), antes)

    def test_el_token_vale_una_vez_y_para_su_accion(self):
        t = self.token("registrar_proyecto")
        self.assertEqual(self.pedir("/api/accion", "POST", {"accion": "simular_actualizar", "token": t, "ruta": self.proy})[0], 403)
        t = self.token("registrar_proyecto")
        self.assertEqual(self.pedir("/api/accion", "POST", {"accion": "registrar_proyecto", "token": t, "ruta": self.proy})[0], 200)
        self.assertEqual(self.pedir("/api/accion", "POST", {"accion": "registrar_proyecto", "token": t, "ruta": self.otro})[0], 403)
        self.assertEqual(len(capa.cargar_proyectos(self.repo)), 1)

    def test_sin_token_o_con_token_inventado_no_hace_nada(self):
        for cuerpo in ({"accion": "registrar_proyecto", "ruta": self.proy}, {"accion": "registrar_proyecto", "token": "inventado", "ruta": self.proy},
                       {"accion": "registrar_proyecto", "token": 5, "ruta": self.proy}):
            self.assertEqual(self.pedir("/api/accion", "POST", cuerpo)[0], 403)
        self.assertEqual(capa.cargar_proyectos(self.repo), [])

    def test_post_exige_clave_en_cabecera_origen_propio_y_json(self):
        cuerpo = {"accion": "registrar_proyecto", "ruta": self.proy, "token": self.token("registrar_proyecto")}
        self.assertEqual(self.pedir("/api/accion", "POST", cuerpo, clave=None)[0], 403)
        self.assertEqual(self.pedir("/api/accion?k=" + self.clave, "POST", cuerpo, clave=None)[0], 403)  # la clave en la dirección no vale para POST
        self.assertEqual(self.pedir("/api/accion", "POST", cuerpo, extra={"Origin": "http://malo.example"})[0], 403)
        self.assertEqual(self.pedir("/api/accion", "POST", cuerpo, tipo="text/plain")[0], 415)
        self.assertEqual(capa.cargar_proyectos(self.repo), [])
        self.assertEqual(self.pedir("/api/accion", "POST", cuerpo, extra={"Origin": "http://127.0.0.1:%d" % self.puerto})[0], 200)

    def test_origen_exacto_esquema_host_y_puerto(self):  # hallazgo 5 (auditoría externa)
        for malo in ("http://127.0.0.1:9", "https://127.0.0.1:%d" % self.puerto, "http://127.0.0.1", "null", "", "http://127.0.0.1:%d.malo.example" % self.puerto,
                     "http://malo.example:%d" % self.puerto, "ftp://127.0.0.1:%d" % self.puerto):
            cuerpo = {"accion": "registrar_proyecto", "ruta": self.proy, "token": self.token("registrar_proyecto")}
            self.assertEqual(self.pedir("/api/accion", "POST", cuerpo, extra={"Origin": malo})[0], 403, malo)
        self.assertEqual(capa.cargar_proyectos(self.repo), [])
        for bueno in ("http://127.0.0.1:%d" % self.puerto, "http://localhost:%d" % self.puerto):
            cuerpo = {"accion": "registrar_proyecto", "ruta": "relativa", "token": self.token("registrar_proyecto")}  # llega a la capa de reglas: 400, no 403
            self.assertEqual(self.pedir("/api/accion", "POST", cuerpo, extra={"Origin": bueno})[0], 400, bueno)

    def test_post_malformado_o_enorme(self):
        self.assertEqual(self.pedir("/api/accion", "POST", b"no es json")[0], 400)
        self.assertEqual(self.pedir("/api/accion", "POST", [1, 2])[0], 400)
        self.assertEqual(self.pedir("/api/accion", "POST", {"accion": "registrar_proyecto", "ruta": "x" * 10000})[0], 400)
        self.assertEqual(self.pedir("/api/accion", "POST", {"accion": 5})[0], 400)
        self.assertEqual(self.pedir("/api/accion", "POST", ("[" * 3000 + "]" * 3000).encode())[0], 400)  # revisión aparte B3: sin cortar la conexión

    def test_token_solo_para_acciones_que_lo_piden(self):
        self.assertEqual(self.pedir("/api/token?a=ver_proyectos")[0], 404)
        self.assertEqual(self.pedir("/api/token?a=borrar")[0], 404)
        self.assertEqual(self.pedir("/api/token?a=registrar_proyecto", clave=None)[0], 403)

    def test_otros_metodos_y_rutas_siguen_cerrados(self):
        self.assertEqual(self.pedir("/api/doc?r=.brain/pendientes.md", "POST", {"a": 1})[0], 405)
        for m in ("PUT", "DELETE", "PATCH"):
            self.assertEqual(self.pedir("/api/accion", m, {"a": 1})[0], 405, m)

    def test_textos_de_la_fase_2_en_los_dos_idiomas(self):
        es = {k for k in web.TEXTOS["es"] if k.startswith("web_")}
        en = {k for k in web.TEXTOS["en"] if k.startswith("web_")}
        self.assertEqual(es, en)
        with open(os.path.join(GUARD, "web_proyectos.py"), encoding="utf-8") as f:
            usadas = set(__import__("re").findall(r'tp\("(web_\w+)"\)', f.read()))
        self.assertTrue(usadas <= es, usadas - es)


if __name__ == "__main__":
    unittest.main()
