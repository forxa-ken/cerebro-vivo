# Resultados de la prueba (spec 001, parte A)

| Ejecución | Lado | Logró (prueba oculta) | Pruebas propias | Notas |
|---|---|---|---|---|
| T1 r1 | CON | sí | pasan | 6 mensajes IA; escribió línea en decisions.log |
| T1 r1 | SIN | sí | pasan | 4 mensajes IA |
| T1 r2 | CON | sí | pasan | 6 mensajes IA; línea en decisions.log |
| T1 r2 | SIN | sí | pasan | 5 mensajes IA |
| T2 r1 | CON | sí | pasan | 13 mensajes IA, 24k nuevos |
| T2 r1 | SIN | sí | pasan | 3 mensajes IA, 16k nuevos |
| T2 r2 | CON | sí | pasan | 4 mensajes IA, 19k nuevos |
| T2 r2 | SIN | sí | pasan | 3 mensajes IA, 16k nuevos |
| T3 r1 | CON | **sí** | pasan | 10 mensajes IA, 24k nuevos; usó el traspaso. Escribió la línea del registro antes de tener las pruebas en verde (flojera del arnés) |
| T3 r1 | SIN | **no** | pasan | 4 mensajes IA, 19k nuevos; inventó el formato (`gastos`/`por_categoria`/`total`), avisó de que no había formato acordado |

Tokens nuevos (T1): CON 30k y 21k; SIN 26k y 17k. El arnés cuesta ~4k más por tarea pequeña (+15-24 %). Arranque casi igual (71k vs 70k). 2 datos por lado: tendencia, no prueba.
