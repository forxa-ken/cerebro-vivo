# CLAVE de la ronda 2 (NO enseñar a los auditores; el proyecto vive en `proyecto/`, esta clave queda fuera)

Proyecto `caja` v2: 3 módulos, 9 pruebas en verde, y un `REQUISITOS.md` que el código incumple en varios sitios. Fallos **sutiles**: ninguno salta a la vista leyendo una sola línea; exigen cruzar código con requisito o razonar sobre ejecución.

| # | Tipo | Dónde | Fallo | Requisito |
| :-: | :-- | :-- | :-- | :-: |
| 1 | calidad (concurrencia) | `ventas.nuevo_folio` | leer-sumar-escribir sin cerrojo (`threading` importado y sin usar): dos hilos pueden repetir folio | 1 |
| 2 | calidad (regla de negocio) | `ventas.total_venta` | el tope del 30 % se aplica a cada descuento, no al total: [0.25, 0.25] da 50 % | 2 |
| 3 | calidad (regla de negocio) | `ventas.redondear` | redondea mitad-par (`ROUND_HALF_EVEN`), la spec pide mitad hacia arriba (p. ej. 0.125) | 3 |
| 4 | calidad (límite) | `fechas.devolucion_valida` | `<` en vez de `<=`: el día 30 se rechaza; además acepta una compra con fecha futura | 4 |
| 5 | calidad (solo ciertas entradas) | `fechas.es_bisiesto` | falta la regla del 400: 2000 sale «no bisiesto» | 5 |
| 6 | seguridad | `archivos.guardar_informe` | `startswith(CARPETA)` deja pasar `informes_otro/x` (prefijo hermano) | 6 |
| 7 | seguridad (comprobar-y-usar) | `archivos.guardar_informe` | `exists` y luego `open("w")`: carrera (y sigue enlaces simbólicos); debía ser `open("x")` | 6 |
| 8 | seguridad | `archivos.hash_clave` | MD5 sin sal | 8 |
| 9 | consumo | `ventas.pedidos_unicos` | `p not in lista` es O(n²); con un `set` sería O(n) | 7 |
| 10 | calidad (errores tragados) | `archivos.leer_config` | `except Exception: pass` oculta permisos, codificación, etc. | — |
| 11 | calidad (pruebas) | `tests/` | ninguna prueba cubre el día 30, el 2000, el tope total, el 0.125, hilos ni `../` y prefijo hermano; la de devolución elige fechas lejanas | — |

**No plantado pero real (no cuenta como acierto ni como falso positivo):** no hay nada que identifique al cliente por correo ni que rechace pedidos repetidos al registrar (req. 7 sin implementar; `pedidos_unicos` solo filtra una lista); `leer_config` no valida valores; `Decimal(x)` en `redondear` acepta flotantes; `CARPETA` depende del directorio de trabajo.

## Cómo puntuar
- **Acierto** = el hallazgo nombra el fallo y lo ubica (archivo/función). Puntuar aparte si lo **reprodujo con una ejecución** (2, 3, 4, 5, 6 y 1 se reproducen fácil).
- **Falso positivo** = hallazgo que no es fallo real. Anotar cuántos.
- Anotar además: gravedad que le dio a cada uno, si cruzó con `REQUISITOS.md` y gasto de tokens/tiempo.
