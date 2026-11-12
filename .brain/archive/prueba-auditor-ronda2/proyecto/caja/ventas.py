import threading
from decimal import Decimal, ROUND_HALF_EVEN

IVA = Decimal("0.21")
TOPE_DESCUENTO = Decimal("0.30")

_siguiente_folio = 0


def nuevo_folio():
    global _siguiente_folio
    actual = _siguiente_folio
    _siguiente_folio = actual + 1
    return _siguiente_folio


def redondear(x):
    return Decimal(x).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)


def total_venta(subtotal, descuentos):
    """descuentos: lista de fracciones, p. ej. [0.10, 0.25]."""
    subtotal = Decimal(str(subtotal))
    aplicado = Decimal(0)
    for d in descuentos:
        d = Decimal(str(d))
        aplicado += min(d, TOPE_DESCUENTO)
    neto = subtotal * (1 - aplicado)
    con_iva = neto * (1 + IVA)
    return redondear(con_iva)


def pedidos_unicos(pedidos):
    vistos = []
    for p in pedidos:
        if p not in vistos:
            vistos.append(p)
    return vistos
