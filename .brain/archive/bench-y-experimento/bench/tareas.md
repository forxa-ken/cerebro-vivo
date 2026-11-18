# Las 3 tareas de la prueba (spec 001, parte A)

El texto de cada una es **idéntico** en los dos lados (CON y SIN arnés). Se pega tal cual en un chat nuevo.

**T1 — Añadir una opción**
> [T1] En este proyecto, añade la opción `--min IMPORTE` a la línea de comandos de `gastos.py`: solo cuenta los gastos con importe mayor o igual a ese valor. Añade su prueba.

**T2 — Arreglar un fallo**
> [T2] El resumen de `datos/ejemplo.csv` sale con categorías duplicadas (Comida y comida, Transporte con espacio delante). Arréglalo y añade una prueba.

**T3 — Retomar un trabajo a medias**
> [T3] Termina lo que quedó a medias en este proyecto (la exportación a JSON).

En CON el chat anterior dejó un traspaso con el formato acordado; en SIN solo queda el código a medias (así es la vida real sin arnés).
Cada ejecución: chat nuevo, mismo modelo y esfuerzo, y la carpeta se rehace con `python bench/montar.py LADO TAREA`.
Después de cada una: `python bench/verificar.py LADO TAREA` (pasa/falla). Al final: `python .brain/guardianes/medir.py --comparar CON SIN`.
