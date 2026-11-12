import hashlib
import os

CARPETA = os.path.abspath("informes")


def guardar_informe(nombre, texto):
    ruta = os.path.abspath(os.path.join(CARPETA, nombre))
    if not ruta.startswith(CARPETA):
        raise ValueError("fuera de la carpeta")
    if os.path.exists(ruta):
        raise FileExistsError(ruta)
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(texto)
    return ruta


def hash_clave(clave: str) -> str:
    return hashlib.md5(clave.encode()).hexdigest()


def clave_correcta(clave: str, guardado: str) -> bool:
    return hash_clave(clave) == guardado


def leer_config(ruta):
    try:
        with open(ruta, encoding="utf-8") as f:
            return dict(l.strip().split("=", 1) for l in f if "=" in l)
    except Exception:
        pass
    return {}
