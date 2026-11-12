import os, sys, tempfile, unittest
from datetime import date
from decimal import Decimal
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from caja import ventas, fechas, archivos


class T(unittest.TestCase):
    def test_folios_consecutivos(self):
        a = ventas.nuevo_folio()
        b = ventas.nuevo_folio()
        self.assertEqual(b, a + 1)

    def test_total_sin_descuento(self):
        self.assertEqual(ventas.total_venta(100, []), Decimal("121.00"))

    def test_total_con_descuento(self):
        self.assertEqual(ventas.total_venta(100, [0.10]), Decimal("108.90"))

    def test_bisiesto(self):
        self.assertTrue(fechas.es_bisiesto(2024))
        self.assertFalse(fechas.es_bisiesto(2023))

    def test_devolucion(self):
        self.assertTrue(fechas.devolucion_valida(date(2026, 1, 1), date(2026, 1, 10)))
        self.assertFalse(fechas.devolucion_valida(date(2026, 1, 1), date(2026, 3, 1)))

    def test_pedidos_unicos(self):
        self.assertEqual(ventas.pedidos_unicos(["a", "b", "a"]), ["a", "b"])

    def test_clave(self):
        h = archivos.hash_clave("x")
        self.assertTrue(archivos.clave_correcta("x", h))

    def test_guardar_informe(self):
        with tempfile.TemporaryDirectory() as d:
            with mock.patch.object(archivos, "CARPETA", os.path.abspath(d)):
                ruta = archivos.guardar_informe("a.txt", "hola")
                self.assertTrue(os.path.exists(ruta))

    def test_config_invalida(self):
        self.assertEqual(archivos.leer_config("no_existe.cfg"), {})


if __name__ == "__main__":
    unittest.main()
