# Spec 001 · Resultados de la parte A (2026-11-01)
n- **Estado:** informe (medición hecha)

12 ejecuciones (3 tareas × 2 lados × 2 repeticiones), mismo modelo (Sonnet 5.5) y esfuerzo (medio). Detalle por ejecución en `bench/resultados.md`.

## ¿Lo logró? (prueba oculta)
| Tarea | CON arnés | SIN arnés |
|---|---|---|
| T1 añadir opción | 2/2 | 2/2 |
| T2 arreglar fallo | 2/2 | 2/2 |
| T3 retomar trabajo a medias | **2/2** | **0/2** |

## ¿Cuánto costó? (medias por chat, tokens nuevos)
| Tarea | CON | SIN | Diferencia |
|---|---|---|---|
| T1 | 25,3k | 21,6k | +17 % |
| T2 | 21,7k | 16,1k | +35 % |
| T3 | 25,6k | 18,0k | +43 % |
| Arranque (todas) | 71,7k | 70,1k | +2 % |

## Lectura honesta
1. **Ahorro de tokens: NO demostrado, de momento lo contrario.** En tareas pequeñas el arnés gasta entre un 17 % y un 43 % más de tokens nuevos (cierre, registro, lectura de memoria). El arranque cuesta casi lo mismo.
2. **Efectividad: sí se ve en T3.** Con el traspaso, el lado CON acertó el formato acordado las 2 veces. El lado SIN lo inventó las 2 veces (avisó de que era una suposición), así que habría que repetir trabajo: ese coste de rehacer **no está** en la tabla de tokens. T3 es el caso más favorable al arnés y está diseñado por nosotros: es una prueba de que la memoria funciona, no un promedio de la vida real.
3. **El ahorro real está donde esta prueba no llega:** chats largos (LoboHook llega a 400k+ de contexto), muchas sesiones seguidas y trabajo repartido entre chats. Para eso sirve el medidor B en proyectos reales durante semanas.
4. Muestra pequeña (2 por caso): tendencia, no estadística.

## Fallos del propio método vistos en la prueba
- En T3 el lado CON escribió la línea del registro **antes** de tener las pruebas en verde (contra la regla «implementada no es hecha»).
- En T2 el lado CON dio 13 mensajes de IA en una ejecución frente a 3 sin arnés: el ritual del arnés puede dispararse en tareas triviales.
- Las sesiones de la prueba recibieron un aviso de «sesiones enlazadas» de la app; afecta igual a los dos lados.

## Mejoras propuestas al arnés (candidatas, a decidir con Darwin)
1. **Modo ligero para tareas pequeñas:** saltar el cierre completo y el registro cuando la tarea es de 1 archivo y sin decisión (la dirección del ahorro).
2. Que `cerrar.py` exija pruebas en verde antes de escribir la línea.
3. Reducir lo que se lee al arrancar cuando no hay traspaso ni pendientes relevantes.
4. Ampliar el banco con una tarea larga multi-chat (donde se espera que el arnés gane en tokens) antes de dar por cerrada la medición.

## Aviso añadido después (2026-11-01): la caché distorsiona la tabla de tokens
Al mirar mensaje a mensaje (spec 003) se vio que «tokens nuevos» depende de si la caché de Claude estaba caliente. El primer mensaje de cada chat gastó ~26k nuevos en las carpetas CON y ~15k en SIN, pero en la primera ejecución de cada carpeta la caché estaba fría para los dos lados (T1 r1: CON 30k, SIN 26k) y en las siguientes caliente (SIN 16-19k, CON 19-27k). Las carpetas «v1.2» se montaron una por ejecución, así que **todas fueron en frío** y no son comparables con las del SIN. Lo que sí aguanta: el logro de las tareas (T3 2/2 contra 0/2). Lo que **no** aguanta con esa precisión: los porcentajes de sobrecoste. La spec 003 los vuelve a medir con un coste ponderado por precio y separando frío/caliente.
