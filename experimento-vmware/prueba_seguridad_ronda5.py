"""Prueba de seguridad ronda 5 (casos fijados en prueba-seguridad-ronda5.md). Uso: python prueba_seguridad_ronda5.py RAMA C|D"""
import os, sys, tempfile
rama, tipo = sys.argv[1], sys.argv[2]
sys.path.insert(0, rama)
from vmware_auto.motor import Motor, ConfirmacionRequerida, ErrorMotor

class Base:
    def __init__(s, estado="apagada", tam=50, libre=500, origen="datastore1", info_libre=True):
        s.estado, s.tam, s.libre, s.origen, s.info_libre = estado, tam, libre, origen, info_libre
        s.llamadas = []
    def estado_vm(s, vm):
        if s.estado == "ERROR": raise RuntimeError("no sé")
        return s.estado
    def describir(s, *a): return "plan"
    def ejecutar(s, *a): s.llamadas.append(a); return "hecho"

class FC(Base):  # interfaz que usa la rama C
    def listar_discos(s, vm): return {"d1": s.tam}
    def listar_almacenes(s):
        if not s.info_libre: raise RuntimeError("sin datos")
        return {"datastore1": 1000, "datastore2": s.libre}
    def almacen_disco(s, vm, d): return s.origen
    def espacio_libre_gb(s): return 1000

class FD(Base):  # interfaz que usa la rama D
    def tamano_disco(s, vm, d): return s.tam
    def espacio_libre_almacen(s, a):
        if not s.info_libre: raise RuntimeError("sin datos")
        return s.libre
    def espacio_libre_gb(s, *a): return 1000

F = FC if tipo == "C" else FD
def mover(m, destino="datastore2", conf=False):
    if tipo == "C":
        return m.ejecutar("mover_disco", {"vm": "m", "disco": "d1", "destino": destino}, confirmado=conf)
    return m.ejecutar("mover_disco", "m", confirmado=conf, params={"disco": "d1", "almacen_destino": destino})

def prueba(nombre, srv, esperado, destino="datastore2", conf=False):
    d = tempfile.mkdtemp(); m = Motor("lab", srv, os.path.join(d, "r.jsonl"), usuario="t")
    try:
        mover(m, destino, conf); res = "ACTUA"
    except ConfirmacionRequerida: res = "BLOQUEA"
    except ErrorMotor: res = "ERROR CLARO"
    except Exception as e: res = "SE CAE (%s)" % type(e).__name__
    if res == "ACTUA" and not srv.llamadas: res = "?"
    ok = "OK  " if res.startswith(esperado) else "FALLO"
    peligro = " <<< ACTUO SIN PERMISO" if res == "ACTUA" and esperado != "ACTUA" else ""
    print("%s %-62s -> %s%s" % (ok, nombre, res, peligro))

prueba("1a estado desconocido (error)", F(estado="ERROR"), "BLOQUEA")
prueba("1b estado raro 'suspendida'", F(estado="suspendida"), "BLOQUEA")
prueba("2  encendida", F(estado="encendida"), "BLOQUEA")
prueba("3a apagada, pequeno, espacio conocido (puede actuar)", F(), "ACTUA")
prueba("3b apagada, pequeno, espacio destino DESCONOCIDO", F(info_libre=False), "BLOQUEA")
prueba("4  apagada, disco grande (300 GB)", F(tam=300, libre=900), "BLOQUEA")
prueba("5  destino sin espacio, con --confirmo", F(tam=60, libre=40), "ERROR", conf=True)
prueba("6  mismo almacen", F(), "ERROR", destino="datastore1")
