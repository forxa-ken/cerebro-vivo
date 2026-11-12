from datetime import date

PLAZO_DEVOLUCION = 30


def es_bisiesto(anio):
    return anio % 4 == 0 and anio % 100 != 0


def devolucion_valida(compra: date, hoy: date) -> bool:
    return (hoy - compra).days < PLAZO_DEVOLUCION
