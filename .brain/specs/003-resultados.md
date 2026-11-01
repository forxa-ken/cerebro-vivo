# Spec 003 · Resultados parciales (2026-11-01)

- **Estado:** informe final (spec 003 ejecutada)

## Qué se hizo
`medir.py` 1.3.0: coste ponderado, `--desglose`, y comparación solo con la misma caché. Se releyeron las 18 ejecuciones ya hechas.

## La caché estaba mal igualada (confirmado)
Primer mensaje de cada chat: la caché fría lee ~45,5k del prefijo y escribe ~24-26k; la caliente lee ~55k y escribe ~14,5-17k. Las 6 ejecuciones «v1.2» y «v1.2.1» fueron todas en frío. Por eso no valen para comparar con el SIN caliente.

## Con caché igualada (lado CON 1.1.0 frente a SIN, 2 repeticiones; coste ponderado medio)
| Caché | CON | SIN | Diferencia |
|---|---|---|---|
| Fría (1 chat por lado) | 90k | 66k | +35 % |
| Caliente (5 por lado) | 103k | 53k | +92 % |

## De dónde sale la diferencia (desglose mensaje a mensaje)
1. **Casi todo es el número de mensajes de la IA.** Cada mensaje después del primero cuesta ~9-10k equivalentes (releer ~72-78k de contexto en caché). CON usó de media 8 mensajes y SIN 3,8.
2. **El arnés en sí pesa poco:** su arranque añade solo ~2-3k tokens al primer mensaje (16,6-17,1k frente a 14,5-14,8k escritos en caliente) y ~1 mensaje para leer constitución y pendientes.
3. **Gran parte de la diferencia es ruido del modelo, no del arnés.** En la ejecución CON de 13 mensajes (T2) la IA tardó 11 mensajes en editar una prueba con trucos de terminal (espacios, saltos de línea) y reintentos; el arnés no tuvo parte. Con 2 repeticiones por caso no se puede separar el ruido del efecto.
4. **La salida también pesa** (peso 5): CON escribe de media el doble (resúmenes más largos, líneas de registro).

## Lectura honesta
- El sobrecoste del arnés en tareas pequeñas es real pero **menor y más ruidoso** de lo que decían los informes 001/002. Su parte fija estimada: ~2-3k de arranque + ~1 mensaje (~9k) + algo más de salida; el resto de la brecha observada (+92 %) no se puede atribuir con estos datos.
- El criterio de éxito de la spec (≤ +15 % en T1/T2) **no se cumple**, y con 2 repeticiones no se podrá afirmar nada fino.

## Siguiente (pasos 3-5, necesitan sesiones de prueba y tu OK)
- Recortar lo claramente fijo: pedir leer constitución y pendientes solo si el resumen marca algo; mensaje de cierre más corto.
- Banco justo (carpeta reutilizada, calentamiento) y **más repeticiones (5 por caso en lugar de 2)** para separar el ruido.

## Re-medición con el arnés 1.3.1 (caché fría en los dos lados, 5 chats por lado, carpeta nueva por ejecución)
### T1 (añadir opción)
| | CON 1.3.1 | SIN | Diferencia |
|---|---|---|---|
| Logradas (prueba oculta) | 5/5 | 5/5 | |
| Coste ponderado medio | 84k | 79k | **+7 %** |
| Tokens nuevos | 30,1k | 27,7k | +9 % |
| Mensajes de la IA | 5,6 | 5,2 | +8 % |
| Salida | 1,6k | 1,9k | −14 % |

Costes por chat: CON 98k 89k 78k 80k 77k; SIN 86k 77k 77k 86k 68k. Se solapan: la diferencia (+7 %) está dentro del ruido y cumple el criterio de la spec (≤ +15 %). Antes de los recortes, T1 daba +17 % (y esa cifra estaba además mal igualada en caché). Faltan T2 y T3.

### T2 (arreglar un fallo)
| | CON 1.3.1 | SIN | Diferencia |
|---|---|---|---|
| Logradas (prueba oculta) | 5/5 | 5/5 | |
| Coste ponderado medio | 81k | 70k | **+16 %** |
| Tokens nuevos | 30,8k | 27,3k | +13 % |
| Mensajes de la IA | 5,0 | 4,4 | +14 % |
| Salida | 1,7k | 1,3k | +27 % |

Costes por chat: CON 80k 69k 81k 83k 92k; SIN 67k 84k 56k 67k 75k (se solapan). +16 % queda en el borde del criterio (≤ 15 %). El cierre automático escribió su línea en las 5 ejecuciones (incluido el hueco de la spec 002: antes una ejecución se quedó sin registro). Antes de los recortes T2 daba +35 % (mal igualado en caché).

### T3 (retomar un trabajo a medias)
| | CON 1.3.1 | SIN | Diferencia |
|---|---|---|---|
| **Logradas (prueba oculta)** | **5/5** | **0/5** | |
| Coste ponderado medio | 118k | 74k | +59 % |
| Tokens nuevos | 33,7k | 28,5k | +18 % |
| Mensajes de la IA | 8,2 | 4,4 | +86 % |
| Salida | 3,2k | 1,9k | +73 % |

Costes por chat: CON 127k 103k 137k 128k 96k; SIN 80k 79k 71k 71k 70k (no se solapan).

## Conclusión de la spec 003 (2026-11-01)
| Tarea | Logro CON / SIN | Coste CON frente a SIN |
|---|---|---|
| T1 | 5/5 · 5/5 | +7 % |
| T2 | 5/5 · 5/5 | +16 % |
| T3 | **5/5 · 0/5** | +59 % por chat |

1. **Efectividad: demostrada en el caso donde importa la memoria.** Sin arnés, 0 de 5 chats acertaron el formato acordado (los 5 inventaron uno y lo avisaron); con arnés, 5 de 5. En tareas autocontenidas (T1, T2) no hay diferencia: las dos formas funcionan.
2. **Ahorro de tokens: NO demostrado.** En tareas pequeñas el arnés cuesta de +7 % a +16 % (tras los recortes; antes se creía +17 % a +43 %, con mala igualación de caché). En T3 cuesta +59 % por chat, pero **la comparación está sesgada a favor de SIN**: sus 5 chats no cumplieron lo pedido, y en la vida real habría que gastar otro intercambio (explicar el formato, rehacer), un coste que no se midió. Hipótesis sin medir: con esa corrección SIN costaría tanto como CON o más.
3. **Criterio de la spec (≤ +15 % en T1/T2 y T3 sigue logrando):** T1 se cumple (+7 %), T2 queda en el borde (+16 %), T3 se cumple en logro.
4. **Dónde sí debería ahorrar y esta prueba no mide:** chats largos (contexto que crece), muchas sesiones seguidas y trabajo repartido entre chats. Para eso hace falta una tarea larga repartida en 3-4 chats (propuesta para una spec 004) o medir con `medir.py` en proyectos reales durante semanas.
5. Límite: tareas de juguete, 5 repeticiones por caso, un solo modelo (Sonnet 5.5, esfuerzo medio).
