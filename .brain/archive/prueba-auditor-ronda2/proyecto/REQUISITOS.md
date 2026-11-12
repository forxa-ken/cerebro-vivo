# Requisitos de «caja» (v2)

1. **Folios:** cada venta recibe un folio único y consecutivo (1, 2, 3...), aunque varios hilos vendan a la vez.
2. **Descuentos:** se acumulan, pero el descuento total de una venta no puede pasar del 30 % del subtotal.
3. **IVA:** 21 %, se calcula sobre el importe **ya descontado**. Los importes se redondean a 2 decimales, mitad hacia arriba.
4. **Devoluciones:** se aceptan hasta 30 días después de la compra, **contados el día 30 incluido**.
5. **Años bisiestos:** el cierre anual necesita saber si un año es bisiesto (regla gregoriana completa).
6. **Informes:** se guardan solo dentro de la carpeta `informes/`; nunca se sobrescribe un informe que ya existe.
7. **Clientes:** el cliente se identifica por su correo; no puede haber dos ventas registradas con el mismo número de pedido.
8. **Contraseñas** de cajeros: nunca se guardan en claro ni con un hash rápido sin sal.
