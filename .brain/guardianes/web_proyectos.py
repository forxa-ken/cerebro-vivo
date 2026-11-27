#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Capa de reglas de la web local, fase 2 (spec 090, secciones 12 y 13): proyectos y simulaciones.

No sabe nada de HTTP: la web (web.py) es solo un cliente de `ejecutar()`. Cada acción lleva quién la pide y sobre qué proyecto,
se comprueba el permiso antes de hacerla y queda anotada (`.brain/web_actividad.log`). Lista cerrada de acciones: nada de lo que
llega de fuera se convierte en un comando. Lo único que escribe es la lista de proyectos (`.brain/web_proyectos.json`) y la
actividad; las simulaciones no cambian ningún proyecto. Solo librería estándar."""

import datetime
import importlib.util
import json
import os
import subprocess
import sys
import threading
import time
import uuid

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from textos import idioma, tp  # noqa: E402

ROLES = ("lectura", "colaborador", "dueno")  # de menos a más
# Lista cerrada de acciones y el rol mínimo de cada una. Un colaborador y las IAs conectadas (fase posterior) no entran en las que cambian algo.
ACCIONES = {"ver_proyectos": "lectura", "registrar_proyecto": "dueno", "simular_actualizar": "dueno", "simular_instalar": "dueno",
            "actualizar_real": "dueno", "instalar_real": "dueno",  # cambian el proyecto (fase 3)
            "tarea_pruebas": "dueno", "tarea_auditor": "dueno", "tarea_cerrar": "dueno", "parar_tarea": "dueno",  # tareas del método (fase 3)
            "github_estado": "dueno", "github_repos": "dueno",  # spec 097, fase 2: login local con GitHub, solo lectura; es la sesión del dueño, nadie más la usa
            "github_iniciar": "dueno", "github_sondear": "dueno", "github_salir": "dueno"}
GITHUB = {"github_estado": "estado", "github_repos": "repositorios", "github_iniciar": "iniciar", "github_sondear": "sondear",
          "github_salir": "salir"}  # acción -> función de github_login.py; nada de lo que llega de fuera elige otra cosa
REALES = {"actualizar_real": "simular_actualizar", "instalar_real": "simular_instalar"}  # cada acción real exige su simulación hecha antes
VIDA_SIMULACION = 600  # segundos que vale una simulación para autorizar la acción real
USUARIO_LOCAL = {"nombre": "local", "rol": "dueno"}  # hoy, un solo usuario: el dueño
NIVELES = ("ligero", "medio", "completo")
ARCHIVO_PROYECTOS = ".brain/web_proyectos.json"
ARCHIVO_ACTIVIDAD = ".brain/web_actividad.log"
TOPE_RUTA = 500
TOPE_NOMBRE = 60
TOPE_PENDIENTES = 6000
TOPE_ACTIVIDAD = 2_000_000  # pasado este tamaño la actividad deja de crecer (no se borra nada)


def permitido(usuario, accion):
    """Verdadero solo si el rol del usuario existe y alcanza el mínimo de una acción de la lista. Todo lo demás, denegado."""
    rol = (usuario or {}).get("rol")
    minimo = ACCIONES.get(accion)
    if rol not in ROLES or minimo is None:
        return False
    return ROLES.index(rol) >= ROLES.index(minimo)


def es_repo_arnes(raiz):
    """Esta web solo gobierna proyectos desde el repo del arnés (tiene manifiesto y VERSION)."""
    return os.path.isfile(os.path.join(raiz, "manifiesto.json")) and os.path.isfile(os.path.join(raiz, "VERSION"))


def _modulo(nombre, ruta):
    espec = importlib.util.spec_from_file_location(nombre, ruta)
    modulo = importlib.util.module_from_spec(espec)
    espec.loader.exec_module(modulo)
    return modulo


def _sin_prefijo(ruta):
    """Quita el prefijo `\\\\?\\` de Windows: con él, la misma carpeta tendría dos nombres y saltaría las comprobaciones de «ya registrado»."""
    if ruta.startswith("\\\\?\\UNC\\"):
        return "\\\\" + ruta[8:]
    return ruta[4:] if ruta.startswith("\\\\?\\") else ruta


def _clave(ruta):
    return os.path.normcase(_sin_prefijo(os.path.realpath(_sin_prefijo(ruta))))


def _atomico(ruta, texto):
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    tmp = "%s.%d.%d.tmp" % (ruta, os.getpid(), threading.get_ident())  # nombre propio de cada hilo
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(texto)
    os.replace(tmp, ruta)


CERROJO_ACTIVIDAD = threading.Lock()


def anotar(raiz, usuario, accion, proyecto, resultado):
    """Una línea JSON por acción: cuándo, quién, qué, sobre qué proyecto y cómo acabó. Nunca rompe la acción si no puede escribir."""
    ruta = os.path.join(raiz, *ARCHIVO_ACTIVIDAD.split("/"))
    try:
        with CERROJO_ACTIVIDAD:  # rotar y escribir no se mezclan entre dos hilos
            os.makedirs(os.path.dirname(ruta), exist_ok=True)
            if os.path.exists(ruta) and os.path.getsize(ruta) > TOPE_ACTIVIDAD:  # mover, no borrar: la actividad vieja pasa a archive/
                destino = os.path.join(raiz, ".brain", "archive", "web_actividad-%s-%s.log" % (
                    datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f"), uuid.uuid4().hex[:6]))  # nombre único: nunca pisa otro archivo
                os.makedirs(os.path.dirname(destino), exist_ok=True)
                os.replace(ruta, destino)
            linea = {"cuando": datetime.datetime.now().isoformat(timespec="seconds"), "quien": (usuario or {}).get("nombre", "?"),
                     "rol": (usuario or {}).get("rol", "?"), "accion": accion, "proyecto": proyecto or "", "resultado": resultado}
            with open(ruta, "a", encoding="utf-8", newline="\n") as f:
                f.write(json.dumps(linea, ensure_ascii=False) + "\n")
        return True
    except OSError as e:  # no rompe la acción, pero el fallo se dice por la salida de error y se devuelve False (las tareas no arrancan sin anotar)
        try:
            sys.stderr.write("web: no se pudo anotar la actividad (%s)\n" % type(e).__name__)
        except (OSError, ValueError):
            pass
        return False


def cargar_proyectos(raiz):
    """Lista de {'nombre', 'ruta'} registrados; vacía si no hay archivo o está roto."""
    try:
        with open(os.path.join(raiz, *ARCHIVO_PROYECTOS.split("/")), encoding="utf-8") as f:
            datos = json.load(f)
        lista = datos.get("proyectos", []) if isinstance(datos, dict) else []
        return [{"nombre": str(p["nombre"]), "ruta": str(p["ruta"])} for p in lista if isinstance(p, dict) and p.get("nombre") and p.get("ruta")]
    except (OSError, ValueError, KeyError, TypeError):
        return []


def _guardar_proyectos(raiz, lista):
    _atomico(os.path.join(raiz, *ARCHIVO_PROYECTOS.split("/")), json.dumps({"proyectos": lista}, ensure_ascii=False, indent=2) + "\n")


def _registrado(raiz, ruta):
    """El proyecto registrado que coincide con `ruta` (la misma carpeta), o None: solo se actúa sobre lo que Darwin añadió."""
    if not isinstance(ruta, str) or not ruta or "\x00" in ruta or len(ruta) > TOPE_RUTA:
        return None
    clave = _clave(ruta)
    for p in cargar_proyectos(raiz):
        if _clave(p["ruta"]) == clave:
            return p
    return None


def _version_repo(raiz):
    try:
        with open(os.path.join(raiz, "VERSION"), encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""


def _tupla(v):
    try:
        return tuple(int(x) for x in v.split("."))
    except (ValueError, AttributeError):
        return None


def info(raiz, proyecto):
    """Ficha de un proyecto registrado: versión del arnés, nivel, si va atrasado y sus pendientes (solo lectura)."""
    ruta = proyecto["ruta"]
    ficha = {"nombre": proyecto["nombre"], "ruta": ruta, "existe": os.path.isdir(ruta), "version": "", "nivel": "",
             "version_repo": _version_repo(raiz), "atrasado": False, "pendientes": ""}
    if not ficha["existe"]:
        return ficha
    try:
        reg = _modulo("actualizar_arnes", os.path.join(AQUI, "actualizar_arnes.py")).cargar_registro(ruta)
        ficha["version"] = str(reg.get("version") or "")
        ficha["nivel"] = str(reg.get("nivel") or "")
    except Exception:
        pass
    a, b = _tupla(ficha["version"]), _tupla(ficha["version_repo"])
    ficha["atrasado"] = bool(a and b and b > a)
    try:
        archivo = os.path.join(ruta, ".brain", "pendientes.md")
        base = _clave(os.path.join(ruta, ".brain"))
        if os.path.commonpath([base, _clave(archivo)]) != base:  # un enlace o junction que salga de .brain/ no se sigue
            return ficha
        tamano = os.path.getsize(archivo)
        with open(archivo, "rb") as f:
            if tamano > TOPE_PENDIENTES:
                f.seek(-TOPE_PENDIENTES, os.SEEK_END)
            ficha["pendientes"] = f.read().decode("utf-8", errors="replace")
    except (OSError, ValueError):
        pass
    return ficha


CERROJO_REGISTRO = threading.Lock()  # leer-añadir-guardar de la lista no puede mezclarse entre dos peticiones


def registrar(raiz, ruta, nombre=None):
    """Añade una carpeta existente a la lista. (True, ficha) o (False, clave de texto del motivo)."""
    if not isinstance(ruta, str) or not ruta.strip() or "\x00" in ruta or len(ruta) > TOPE_RUTA:
        return False, "web_err_ruta"
    ruta = _sin_prefijo(ruta.strip())
    if not os.path.isabs(ruta):  # una ruta relativa se resolvería contra la carpeta desde la que se lanzó el servidor
        return False, "web_err_ruta"
    ruta = os.path.abspath(ruta)
    if not os.path.isdir(ruta):
        return False, "web_err_no_existe"
    if _clave(ruta) == _clave(raiz):
        return False, "web_err_es_el_repo"
    with CERROJO_REGISTRO:
        if _registrado(raiz, ruta):
            return False, "web_err_repetido"
        nombre = (nombre if isinstance(nombre, str) else "") or os.path.basename(ruta.rstrip("\\/")) or ruta
        lista = cargar_proyectos(raiz) + [{"nombre": nombre.strip()[:TOPE_NOMBRE], "ruta": ruta}]
        _guardar_proyectos(raiz, lista)
    return True, info(raiz, lista[-1])


def simular_actualizar(raiz, proyecto):
    """Texto de lo que haría `actualizar_arnes.py` en el proyecto. No escribe nada (modo simulación del actualizador)."""
    act = _modulo("actualizar_arnes", os.path.join(AQUI, "actualizar_arnes.py"))
    motivo = act.nivel_sin_arnes(proyecto)
    if motivo:
        return act.tp("actualizar_arnes_copia_nada_este") % (motivo, proyecto)
    return act.informe(act.sincronizar(raiz, proyecto, simular=True), True)


def _archivos_del_actualizador(raiz, proyecto, creados):
    """Cuántos archivos del manifiesto, como máximo, añade el actualizador justo después de instalar (la instalación real los copia y la simulación no los cuenta)."""
    try:
        manifiesto = _modulo("actualizar_arnes", os.path.join(AQUI, "actualizar_arnes.py")).cargar_manifiesto(raiz)
    except Exception:
        return 0
    ya = {os.path.relpath(r, proyecto).replace(os.sep, "/") if os.path.isabs(r) else str(r).replace(os.sep, "/") for r in creados}
    return len([r for r in manifiesto["archivos"] if r not in ya and not os.path.exists(os.path.join(proyecto, *r.split("/")))])


def simular_instalar(raiz, proyecto, nivel):
    """Texto de lo que haría el instalador del kit de arranque en la carpeta, en modo simulación (no crea nada)."""
    if nivel not in NIVELES:
        raise ValueError("nivel")
    ruta_kit = os.path.join(AQUI, "..", "biblioteca", "kit-arranque", "instalar.py")  # el del propio arnés que corre esta web
    if not os.path.isfile(ruta_kit):
        raise OSError(ruta_kit)
    ins = _modulo("instalar_kit", ruta_kit)
    en = idioma() == "en"
    hechos = ins.instalar(proyecto, os.path.basename(proyecto.rstrip("\\/")) or proyecto, "the owner" if en else "el dueño",
                          "English" if en else "español", "python -m unittest discover tests", ["claude"], nivel, simular=True)
    L = [tp("web_sim_instalar_titulo") % nivel]
    for clave, texto in (("creados", "web_sim_creara"), ("fusionados", "web_sim_fusionara"), ("respetados", "web_sim_respetara")):
        if hechos[clave]:
            L.append(tp(texto) % len(hechos[clave]))
            L += ["  - " + os.path.relpath(r, proyecto) if os.path.isabs(r) else "  - " + str(r) for r in hechos[clave]]
    extra = _archivos_del_actualizador(raiz, proyecto, hechos["creados"])
    if extra:
        L.append(tp("web_sim_luego") % extra)
    L.append(tp("web_sim_no_escribio"))
    return "\n".join(L)


CERROJO_ESTADO = threading.Lock()
SIMULADAS = {}   # (carpeta, acción simulada, nivel) -> momento de la última simulación buena
OCUPADOS = set()  # carpetas con una acción real en marcha: una por proyecto a la vez


def _anotar_simulada(proyecto, accion, nivel=""):
    clave = _clave(proyecto)
    with CERROJO_ESTADO:
        SIMULADAS[(clave, accion, nivel)] = time.monotonic()  # quien llama tiene la carpeta reservada (ejecutar): nada cambió mientras se simulaba


def _simulada_reciente_sin_cerrojo(clave, accion, nivel=""):
    t = SIMULADAS.get((clave, accion, nivel))
    return t is not None and time.monotonic() - t <= VIDA_SIMULACION


def actualizar_real(raiz, proyecto):
    """Actualiza de verdad con `actualizar_arnes.py` (sin tocar lo modificado a mano; el actualizador hace copia de lo que pisa)."""
    act = _modulo("actualizar_arnes", os.path.join(AQUI, "actualizar_arnes.py"))
    motivo = act.nivel_sin_arnes(proyecto)
    if motivo:
        return act.tp("actualizar_arnes_copia_nada_este") % (motivo, proyecto)
    return act.informe(act.sincronizar(raiz, proyecto, simular=False), False) + "\n" + tp("web_real_sin_pruebas")


def instalar_real(proyecto, nivel):
    """Instala de verdad el kit de arranque (nunca pisa lo que ya existe: lo fusiona o lo respeta)."""
    if nivel not in NIVELES:
        raise ValueError("nivel")
    ins = _modulo("instalar_kit", os.path.join(AQUI, "..", "biblioteca", "kit-arranque", "instalar.py"))
    en = idioma() == "en"
    hechos = ins.instalar(proyecto, os.path.basename(proyecto.rstrip("\\/")) or proyecto, "the owner" if en else "el dueño",
                          "English" if en else "español", "python -m unittest discover tests", ["claude"], nivel, simular=False)
    L = [tp("web_real_instalar_titulo") % nivel]
    for clave, texto in (("creados", "web_real_creo"), ("fusionados", "web_real_fusiono"), ("respetados", "web_real_respeto")):
        if hechos[clave]:
            L.append(tp(texto) % len(hechos[clave]))
            L += ["  - " + os.path.relpath(r, proyecto) if os.path.isabs(r) else "  - " + str(r) for r in hechos[clave]]
    L += ["! " + str(a) for a in hechos.get("avisos", [])]
    return "\n".join(L)


def _real(raiz, usuario, accion, ruta, nivel):
    """Acción que cambia el proyecto. En un solo paso protegido: que no haya otra en marcha, que haya simulación reciente y gastarla
    (vale una sola vez, también si la acción falla: tras un fallo hay que simular de nuevo, el estado ya no es el que se vio)."""
    clave = _clave(ruta)
    with CERROJO_ESTADO:
        if clave in OCUPADOS:
            motivo = "ocupado"
        elif not _simulada_reciente_sin_cerrojo(clave, REALES[accion], nivel):
            motivo = "sin simulación previa"
        else:
            motivo = None
            SIMULADAS.pop((clave, REALES[accion], nivel), None)
            OCUPADOS.add(clave)
    if motivo:
        anotar(raiz, usuario, accion, ruta, motivo)
        return 409, {"error": tp("web_err_ocupado" if motivo == "ocupado" else "web_err_sin_simulacion")}
    try:
        texto = actualizar_real(raiz, ruta) if accion == "actualizar_real" else instalar_real(ruta, nivel)
        anotar(raiz, usuario, accion, ruta, "ok")
        return 200, {"texto": texto}
    finally:
        with CERROJO_ESTADO:
            OCUPADOS.discard(clave)


# ---- Tareas del método (fase 3): comandos fijos del propio proyecto, en segundo plano, con salida visible y botón de parar ----
# Lista cerrada: el comando sale de aquí, nunca del navegador. Lo único que llega de fuera es el texto de «cerrar» (un argumento, sin shell).
TAREAS = {"tarea_pruebas": ("-m", "unittest", "discover", "tests"),
          "tarea_auditor": (".brain/guardianes/auditor.py", "estado"),
          "tarea_cerrar": (".brain/guardianes/cerrar.py",)}
TOPE_SALIDA = 60_000        # caracteres que se guardan de la salida de una tarea
TOPE_TEXTO_CERRAR = 600
TOPE_CHAT = 60
LIMITE_TAREA = 600          # segundos; pasado el límite se para sola
TRABAJOS = {}               # id -> {"clave","ruta","accion","estado","salida","codigo","proc"}
MAX_TRABAJOS = 30


def _crear_grupo(proc):
    """Windows: mete el proceso en un «Job Object» que mata todo lo que cuelga de él, aunque el padre ya haya muerto (taskkill /T
    no encuentra a los hijos huérfanos). Devuelve el asa del grupo o None (entonces se usa taskkill, que es lo mejor que queda).
    Hueco conocido: un hijo creado antes de esta asignación (microsegundos tras arrancar) no entraría en el grupo."""
    if os.name != "nt":
        return None
    try:
        import ctypes
        from ctypes import wintypes
        k = ctypes.WinDLL("kernel32", use_last_error=True)
        k.CreateJobObjectW.restype = wintypes.HANDLE
        k.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
        k.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
        k.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
        k.CloseHandle.argtypes = [wintypes.HANDLE]

        class _Basico(ctypes.Structure):
            _fields_ = [("PerProcessUserTimeLimit", ctypes.c_longlong), ("PerJobUserTimeLimit", ctypes.c_longlong),
                        ("LimitFlags", wintypes.DWORD), ("MinimumWorkingSetSize", ctypes.c_size_t),
                        ("MaximumWorkingSetSize", ctypes.c_size_t), ("ActiveProcessLimit", wintypes.DWORD),
                        ("Affinity", ctypes.c_size_t), ("PriorityClass", wintypes.DWORD), ("SchedulingClass", wintypes.DWORD)]

        class _Extendido(ctypes.Structure):
            _fields_ = [("Basic", _Basico), ("IoInfo", ctypes.c_ulonglong * 6), ("ProcessMemoryLimit", ctypes.c_size_t),
                        ("JobMemoryLimit", ctypes.c_size_t), ("PeakProcessMemoryUsed", ctypes.c_size_t),
                        ("PeakJobMemoryUsed", ctypes.c_size_t)]

        asa = k.CreateJobObjectW(None, None)
        if not asa:
            return None
        info = _Extendido()
        info.Basic.LimitFlags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE: si el servidor muere, mueren las tareas
        if not k.SetInformationJobObject(asa, 9, ctypes.byref(info), ctypes.sizeof(info)) \
                or not k.AssignProcessToJobObject(asa, wintypes.HANDLE(int(proc._handle))):
            k.CloseHandle(asa)
            return None
        return asa
    except (OSError, AttributeError, ValueError, TypeError):
        return None


def _matar_grupo(proc, grupo=None):
    """Mata todo lo que queda del grupo de la tarea (hijos incluidos), esté vivo el padre o no. No falla nunca."""
    try:
        if os.name == "nt":
            if grupo:
                import ctypes
                from ctypes import wintypes
                k = ctypes.WinDLL("kernel32", use_last_error=True)
                k.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
                k.TerminateJobObject(grupo, 1)
            elif proc.poll() is None:
                subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True, timeout=15)
        else:
            import signal
            os.killpg(proc.pid, signal.SIGKILL)  # start_new_session: el grupo es el pid del padre, y sigue existiendo aunque el padre muera
    except (OSError, subprocess.SubprocessError, ProcessLookupError, AttributeError, ValueError, TypeError):
        pass


def _cerrar_asa(grupo):
    if grupo and os.name == "nt":
        try:
            import ctypes
            from ctypes import wintypes
            k = ctypes.WinDLL("kernel32", use_last_error=True)
            k.CloseHandle.argtypes = [wintypes.HANDLE]
            k.CloseHandle(grupo)
        except (OSError, AttributeError, ValueError, TypeError):
            pass


def _matar(proc, grupo=None):
    """Para el proceso y todo lo que lanzó (las pruebas lanzan procesos hijos)."""
    _matar_grupo(proc, grupo)
    try:
        proc.kill()
    except OSError:
        pass


def _comando_tarea(accion, ruta, datos):
    """(lista de argumentos, None) o (None, clave de texto del error). Comprueba que el guardián exista dentro del proyecto."""
    fijo = TAREAS[accion]
    cmd = [sys.executable] + list(fijo)
    if fijo[0] == "-m":
        if not os.path.isdir(os.path.join(ruta, "tests")):
            return None, "web_err_sin_tests"
        return cmd, None
    script = os.path.join(ruta, *fijo[0].split("/"))
    # El límite es el proyecto, no lo que `guardianes` resuelva: si .brain o .brain/guardianes es un enlace o junction hacia fuera,
    # la carpeta resuelta ya no cuelga del proyecto y se rechaza (auditoría externa, hallazgo 1).
    base = os.path.join(_clave(ruta), ".brain", "guardianes")
    try:
        dentro = (os.path.isfile(script) and _clave(os.path.join(ruta, ".brain", "guardianes")) == base
                  and os.path.commonpath([base, _clave(script)]) == base)
    except ValueError:
        dentro = False
    if not dentro:  # el guardián no existe o es un enlace que sale del proyecto
        return None, "web_err_sin_guardian"
    if accion == "tarea_cerrar":
        texto, chat = datos.get("texto"), datos.get("chat")
        if not isinstance(texto, str) or not isinstance(chat, str) or not texto.strip() or not chat.strip()                 or len(texto) > TOPE_TEXTO_CERRAR or len(chat) > TOPE_CHAT or "\x00" in texto + chat:
            return None, "web_err_datos"
        cmd += ["--chat", " ".join(chat.split()), "--", " ".join(texto.split())]  # «--»: un texto que empiece por «-» no es una opción
    return cmd, None


def _reanudar(proc):
    """Windows: reanuda un proceso creado suspendido (NtResumeProcess)."""
    import ctypes
    from ctypes import wintypes
    nt = ctypes.WinDLL("ntdll")
    nt.NtResumeProcess.argtypes = [wintypes.HANDLE]
    if nt.NtResumeProcess(wintypes.HANDLE(int(proc._handle))) != 0:
        raise OSError("reanudar")


def _arrancar(cmd, ruta, env, validar=None):
    """(proceso, grupo). En Windows el proceso nace SUSPENDIDO, entra en el grupo (Job Object) y solo entonces corre: así ningún hijo
    puede escapar antes de estar dentro. Si no se puede meter en el grupo, la tarea no arranca (taskkill no es una garantía equivalente).
    `validar()` devuelve un motivo de rechazo o None: se vuelve a llamar con el proceso ya creado y, en Windows, todavía parado, para que
    el guardián no pueda cambiarse por un enlace entre la comprobación y la ejecución (queda solo el instante entre esa llamada y reanudar)."""
    comun = dict(cwd=ruta, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, text=True, encoding="utf-8",
                 errors="replace", env=env)
    if os.name != "nt":
        proc = subprocess.Popen(cmd, start_new_session=True, **comun)
        if validar and validar():  # en POSIX ya corre: si el guardián se cambió justo ahora, se mata el grupo
            _matar(proc)
            raise OSError("guardian")
        return proc, None
    proc = subprocess.Popen(cmd, creationflags=0x00000004, **comun)  # CREATE_SUSPENDED
    try:
        grupo = _crear_grupo(proc)
        if not grupo:
            raise OSError("grupo")
        if validar and validar():
            _cerrar_asa(grupo)
            raise OSError("guardian")
        try:
            _reanudar(proc)
        except OSError:
            _cerrar_asa(grupo)
            raise
        return proc, grupo
    except OSError:
        try:
            proc.kill()
            proc.wait(timeout=10)
        except (OSError, subprocess.SubprocessError):
            pass
        raise


def _vigilar(job_id):
    job = TRABAJOS[job_id]
    proc = job["proc"]
    def leer():
        try:
            import codecs
            deco = codecs.getincrementaldecoder("utf-8")(errors="replace")
            while True:
                bruto = proc.stdout.buffer.read1(4096)  # lo que haya (no espera a llenar el trozo) y nunca más de 4096: una línea sin salto no crece sin límite
                trozo = deco.decode(bruto, final=not bruto)
                if not bruto:
                    if trozo:
                        with CERROJO_ESTADO:
                            if len(job["salida"]) < TOPE_SALIDA:
                                job["salida"] += trozo[:TOPE_SALIDA - len(job["salida"])]
                    break
                with CERROJO_ESTADO:
                    if len(job["salida"]) < TOPE_SALIDA:  # lo que sobra se lee y se descarta, para no bloquear la tarea
                        job["salida"] += trozo[:TOPE_SALIDA - len(job["salida"])]
        except (OSError, ValueError):
            pass
    lector = threading.Thread(target=leer, daemon=True)
    lector.start()
    try:
        codigo = proc.wait(timeout=LIMITE_TAREA)
    except subprocess.TimeoutExpired:
        with CERROJO_ESTADO:
            job["parada"] = "tiempo"
            _matar(proc, job.get("grupo"))
        codigo = proc.wait()
    with CERROJO_ESTADO:
        _matar_grupo(proc, job.get("grupo"))  # el padre ya acabó: lo que dejó vivo (hijos huérfanos) se acaba aquí, y la carpeta no se libera antes
    lector.join(timeout=5)
    with CERROJO_ESTADO:
        _cerrar_asa(job.get("grupo"))
        job["grupo"] = None
        job["codigo"] = codigo
        job["estado"] = "parada" if job.get("parada") else ("ok" if codigo == 0 else "error")
        OCUPADOS.discard(job["clave"])
    anotar(job["raiz"], job["usuario"], job["accion"], job["ruta"], job["estado"] + " (código %s)" % codigo)


def lanzar_tarea(raiz, usuario, accion, ruta, datos):
    """Arranca la tarea en segundo plano. (código HTTP, dict). Una acción por carpeta a la vez."""
    cmd, error = _comando_tarea(accion, ruta, datos)
    if error:
        anotar(raiz, usuario, accion, ruta, "rechazada: " + error)
        return (400 if error == "web_err_datos" else 409), {"error": tp(error)}
    clave = _clave(ruta)
    with CERROJO_ESTADO:
        if clave in OCUPADOS:
            ocupado = True
        else:
            ocupado = False
            OCUPADOS.add(clave)
            for k in [k for k in SIMULADAS if k[0] == clave]:
                del SIMULADAS[k]  # una tarea puede cambiar el proyecto: lo simulado antes ya no describe lo que hay
        for k in [k for k, j in TRABAJOS.items() if j["estado"] != "corriendo"][:max(0, len(TRABAJOS) - MAX_TRABAJOS)]:
            del TRABAJOS[k]  # los terminados más viejos se olvidan (la actividad queda en el registro)
    if ocupado:
        anotar(raiz, usuario, accion, ruta, "ocupado")
        return 409, {"error": tp("web_err_ocupado")}
    try:
        cmd, error = _comando_tarea(accion, ruta, datos)  # otra vez, ya con la carpeta reservada: se acorta la ventana entre comprobar y ejecutar
        if error:
            raise OSError(error)
        env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
        if not anotar(raiz, usuario, accion, ruta, "iniciada"):  # sin poder dejar constancia, no se ejecuta nada
            raise OSError("registro")
        proc, grupo = _arrancar(cmd, ruta, env, lambda: _comando_tarea(accion, ruta, datos)[1])
    except OSError as e:
        with CERROJO_ESTADO:
            OCUPADOS.discard(clave)
        anotar(raiz, usuario, accion, ruta, "error: " + type(e).__name__ + " " + str(e)[:80])
        if str(e) == "registro":
            return 500, {"error": tp("web_err_registro")}
        if str(e) == "guardian":
            return 409, {"error": tp("web_err_sin_guardian")}
        if str(e) in ("grupo", "reanudar"):
            return 500, {"error": tp("web_err_grupo")}
        return 500, {"error": tp("web_err_simulacion") % type(e).__name__}
    job_id = uuid.uuid4().hex[:12]
    with CERROJO_ESTADO:
        TRABAJOS[job_id] = {"clave": clave, "ruta": ruta, "raiz": raiz, "usuario": usuario, "accion": accion, "estado": "corriendo",
                            "salida": "", "codigo": None, "proc": proc, "grupo": grupo}
    threading.Thread(target=_vigilar, args=(job_id,), daemon=True).start()
    return 200, {"id": job_id}


def estado_tarea(job_id):
    """Estado y salida hasta ahora de una tarea, o None si no existe."""
    with CERROJO_ESTADO:
        j = TRABAJOS.get(job_id) if isinstance(job_id, str) else None
        if not j:
            return None
        return {"estado": j["estado"], "salida": j["salida"], "codigo": j["codigo"], "accion": j["accion"], "ruta": j["ruta"]}


def parar_tarea(raiz, usuario, job_id):
    with CERROJO_ESTADO:
        j = TRABAJOS.get(job_id) if isinstance(job_id, str) else None
        if not j or j["estado"] != "corriendo":
            return 404, {"error": tp("web_err_sin_tarea")}
        j["parada"] = "usuario"
        _matar(j["proc"], j.get("grupo"))  # bajo el cerrojo: el asa del grupo no se cierra mientras se usa
    anotar(raiz, usuario, "parar_tarea", j["ruta"], "pedida")
    return 200, {"ok": True}


def _github(raiz, usuario, accion):
    import github_login as gh  # perezoso: solo se carga si se usa
    try:
        res = getattr(gh, GITHUB[accion])()
    except gh.ErrorGitHub as e:
        anotar(raiz, usuario, accion, "", "error: " + e.clave)
        return e.codigo, {"error": e.texto()}
    except Exception as e:  # nunca se anota el mensaje: podría llevar algo sensible
        anotar(raiz, usuario, accion, "", "error: " + type(e).__name__)
        return 500, {"error": tp("web_gh_err_respuesta")}
    if accion not in ("github_estado", "github_repos"):
        anotar(raiz, usuario, accion, "", "ok")
    return 200, res


def ejecutar(raiz, usuario, accion, ruta=None, datos=None):
    """Única puerta de entrada. Devuelve (código HTTP, dict). Comprueba la acción y el permiso, y anota lo que no es solo mirar."""
    datos = datos if isinstance(datos, dict) else {}
    if accion not in ACCIONES:
        return 404, {"error": tp("web_err_accion")}
    if not permitido(usuario, accion):
        anotar(raiz, usuario, accion, ruta, "denegado")
        return 403, {"error": tp("web_err_permiso")}
    if accion in GITHUB:  # no depende de ningún proyecto; el token nunca se anota ni se devuelve
        return _github(raiz, usuario, accion)
    if not es_repo_arnes(raiz):
        return 409, {"error": tp("web_err_no_repo")}
    try:
        if accion == "parar_tarea":
            return parar_tarea(raiz, usuario, datos.get("id"))
        if accion == "ver_proyectos":
            return 200, {"rol": usuario["rol"], "version_repo": _version_repo(raiz),
                         "proyectos": [info(raiz, p) for p in cargar_proyectos(raiz)]}
        if accion == "registrar_proyecto":
            ok, res = registrar(raiz, datos.get("ruta"), datos.get("nombre"))
            anotar(raiz, usuario, accion, datos.get("ruta") if isinstance(datos.get("ruta"), str) else "", "ok" if ok else res)
            return (200, {"proyecto": res}) if ok else (400, {"error": tp(res)})
        proyecto = _registrado(raiz, ruta)
        if not proyecto:
            anotar(raiz, usuario, accion, ruta if isinstance(ruta, str) else "", "proyecto no registrado")
            return 404, {"error": tp("web_err_no_registrado")}
        if not os.path.isdir(proyecto["ruta"]):
            return 404, {"error": tp("web_err_no_existe")}
        if accion in TAREAS:
            return lanzar_tarea(raiz, usuario, accion, proyecto["ruta"], datos)
        es_instalar = accion in ("simular_instalar", "instalar_real")
        nivel = datos.get("nivel") if es_instalar else ""
        if es_instalar and nivel not in NIVELES:
            anotar(raiz, usuario, accion, proyecto["ruta"], "datos no válidos")
            return 400, {"error": tp("web_err_datos")}
        if accion in REALES:
            return _real(raiz, usuario, accion, proyecto["ruta"], nivel)
        clave = _clave(proyecto["ruta"])
        with CERROJO_ESTADO:  # una simulación también ocupa la carpeta: así ninguna acción real cambia el proyecto mientras se simula
            ocupado = clave in OCUPADOS
            if not ocupado:
                OCUPADOS.add(clave)
        if ocupado:
            anotar(raiz, usuario, accion, proyecto["ruta"], "ocupado")
            return 409, {"error": tp("web_err_ocupado")}
        try:
            texto = simular_actualizar(raiz, proyecto["ruta"]) if accion == "simular_actualizar" else simular_instalar(raiz, proyecto["ruta"], nivel)
            _anotar_simulada(proyecto["ruta"], accion, nivel)  # aún reservada: lo simulado describe el estado que de verdad había
        finally:
            with CERROJO_ESTADO:
                OCUPADOS.discard(clave)
        anotar(raiz, usuario, accion, proyecto["ruta"], "ok")
        return 200, {"texto": texto}
    except ValueError as e:  # el actualizador y el instalador explican en llano por qué no pueden (por ejemplo, manifiesto desfasado)
        anotar(raiz, usuario, accion, ruta if isinstance(ruta, str) else "", "rechazada: " + str(e)[:200])
        return 400, {"error": str(e)}
    except Exception as e:  # una simulación que falla se cuenta, no tumba el servidor
        anotar(raiz, usuario, accion, ruta if isinstance(ruta, str) else "", "error: " + type(e).__name__)
        return 500, {"error": tp("web_err_simulacion") % type(e).__name__}
