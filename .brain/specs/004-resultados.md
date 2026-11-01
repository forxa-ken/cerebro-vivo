# Resultados de la spec 004: ¿ayudan los índices? (2026-11-01)

- **Estado:** medida y cerrada (2026-11-01)

Datos: copia del `.brain` de LoboHook (78 fichas, índices de 14,7 KB y 9 KB, hechos de 26 KB). 30 chats de un mensaje, solo lectura, mismo modelo (sonnet 5.5): 3 lados × 5 preguntas × 2 repeticiones. Lado a = con índice, b = sin índice, c = índice con 5 filas falsas. Coste con `medir.py` (tokens equivalentes de entrada).

## Acierto
| Lado | Aciertos | Notas |
| :--- | :--- | :--- |
| a (con índice) | 10/10 | La pregunta sin respuesta salió «no consta» las 2 veces |
| b (sin índice) | 10/10 | Una respuesta dijo «8 acciones por flujo» (la ficha no dice «por flujo»): acierta la cifra, matiza mal |
| c (índice con filas falsas) | 10/10 | Los chats encontraron la ficha correcta aunque el enlace del índice estaba cruzado |

Nadie inventó la respuesta de Bizum.

## Coste (media por chat, 10 chats por lado)
| Lado | Coste | Nuevos | Chats con caché fría |
| :--- | :--- | :--- | :--- |
| a | 57k | 28k | 2 |
| b | 48k | 22k | 2 |
| c | 65k | 32k | 3 |

Con índice (a) salió un **19 % más caro** que sin índice (b); con el índice roto (c), un **36 % más caro**. El número de mensajes por chat fue casi igual (2,9 / 2,8 / 3,3).

## Qué se puede decir
- **A este tamaño el índice no ayudó a acertar** (todos acertaron) **y costó más**. No se demuestra que ahorre.
- **El índice roto no hizo fallar a nadie**: la IA buscó por su cuenta (nombres de ficha, búsqueda de texto). Es una señal buena para la robustez, pero cuesta más.
- Las fichas de LoboHook tienen nombres que describen su contenido (`D-062-creditos-de-ia-y-recargas.md`). El lado b **conservaba esa lista de nombres**, que actúa como un índice gratuito. Esto probablemente explica que b no sufriera.

## Limitaciones (dichas de antemano y nuevas)
- Un solo proyecto (LoboHook) y ~80 fichas: con cientos de fichas o nombres poco claros el resultado podría cambiar.
- 2 repeticiones por caso: tendencia, no estadística. Hubo 3 chats fríos en c frente a 2 en a y b.
- 4 chats de la pregunta 4 se cortaron y se reintentaron por mensaje, lo que puede alterar su coste.
- No se midió la pregunta que necesita juntar varias fichas (se cambió la 4 por ser ambigua: D-054 aún dice «30 IA al mes» y D-062 pasó a créditos, ambas como vigentes; eso sí es un dato viejo real en LoboHook).

## Siguiente paso posible (sin hacer)
Repetir sin nombres descriptivos en las fichas (solo `D-062.md`) o con cientos de fichas, que es donde un índice debería ganar. Y revisar si el arranque debe pedir leer los índices o dejarlos a demanda.
