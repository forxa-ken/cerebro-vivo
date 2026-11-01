# Spec 002 · Resultados del modo ligero (2026-11-01)

- **Estado:** informe (medición parcial)

Tokens nuevos por chat, solo lado CON con el arnés nuevo. Referencias de la spec 001: CON 1.1.0 y SIN.

| Ejecución | Versión | Tokens nuevos | Logró | Línea del registro |
|---|---|---|---|---|
| T1 | 1.2.0 | 30k | sí | la escribió la IA |
| T2 | 1.2.0 | 29k | sí | la escribió la IA |
| T3 | 1.2.0 | 35k | sí | la escribió la IA |
| T1 (a) | 1.2.1 | 31k | sí | **automática** |
| T1 (b) | 1.2.1 | 30k | sí | **automática** |
| T2 (b) | 1.2.1 | 29k | sí | no la escribió nadie (la IA no la puso y el guardián no actuó) |
| *Referencia T1* | 1.1.0 / SIN | 30k y 21k / 26k y 17k | | |
| *Referencia T2* | 1.1.0 / SIN | 24k y 19k / 16k y 16k | | |
| *Referencia T3* | 1.1.0 / SIN | 24k y 27k / 19k y ? | | |

## Lectura honesta
1. **Funciona, pero no ahorra.** El modo ligero escribe la línea solo (T1 a y b), y aun así el gasto sigue en 29-31k. La vuelta extra del cierre **no era** el coste principal. El criterio de la spec (CON ≤ +10 % frente a SIN en T1 y T2) **no se cumple**: seguimos en torno a +40-80 % frente a SIN en estas ejecuciones.
2. **Fallo nuevo (T2 b):** con la instrucción «no escribas la línea», en una ejecución no quedó registro (el guardián no actuó, probablemente por no correr las pruebas de la forma que detecta). Hay que cubrir ese caso antes de repartir el cambio.
3. **Dónde está probablemente el coste (hipótesis, sin medir aún):** lo que el arnés pide leer al arrancar (`CLAUDE.md` largo, constitución, pendientes, copiar el resumen a Darwin) añade mensajes y tokens nuevos antes de empezar la tarea. T1 con arnés: 6 mensajes de IA; sin arnés: 4-5.
4. Pocas ejecuciones por caso; T2 (a) y T3 con 1.2.1 no se han lanzado.

## Siguiente paso propuesto (nueva spec)
Medir de verdad dónde se van los tokens extra (comparar, mensaje a mensaje, un chat CON y uno SIN) y recortar el ritual de arranque en tareas pequeñas: no leer constitución ni pendientes si el resumen del arranque no marca nada, y no copiar el resumen a Darwin salvo que haya novedades.

## Aviso añadido después (2026-11-01)
Las ejecuciones 1.2.x se hicieron cada una en una carpeta nueva (caché fría), mientras las referencias SIN se hicieron en la misma carpeta (caché caliente en las repeticiones). La comparación de tokens nuevos de esta tabla **no es justa**; ver el aviso de `001-resultados.md` y la spec 003.
