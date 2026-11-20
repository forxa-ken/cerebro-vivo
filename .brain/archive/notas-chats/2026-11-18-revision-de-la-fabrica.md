# Revisión de la fábrica — informe para Darwin (2026-11-18)

Pendiente 62 / spec 090 sección 15. **Solo lectura y análisis: no se ha cambiado nada** (ni fábrica, ni specs, ni GitHub, ni Prominimap). Datos leídos de `empresa-virtual-sim` (36 encargos, la única fábrica con registro completo), del informe de la prueba de TraductorVoz y de `medir.py --fabrica`.

## 1. Respuesta corta

Tienes razón en parte, y los números dicen **dónde**:

- **Construir no es lo caro.** Los encargos tardan de 3 a 51 minutos (mediana 17). Lo caro y lo lento es lo que se pone **alrededor**: spec formal, revisión de la spec, revisión aparte, revisión de consumo, informe, autorizaciones de tope.
- **En un cambio pequeño la ceremonia cuesta 3 veces el trabajo.** El arreglo del «Enter que se pierde» (spec 004, encargo 029) fueron ~6 líneas de código. Gasto anotado: **≈179.500 tokens**; la ejecutora solo gastó 34.487 (19 %). El otro 81 % fue revisar la spec (~65.570) y la revisión aparte (79.441), y eso **sin contar** a la directora ni la prueba de uso real.
- **En un encargo grande la ceremonia sí compensa**: las specs 003 y 005 fueron rechazadas dos veces cada una con fallos reales (spec 005: «Comprobar mi reto» sin criterio definido, `New-VM` que crea la máquina encendida y en PowerCLI real nace apagada, etc.) antes de gastar un solo encargo.

**Decisión de fondo que propongo:** la fábrica pasa a ser **solo para encargos grandes**. Lo pequeño lo hace una sola IA, directamente, con pruebas. Umbral en la sección 5.

## 2. Qué se midió (y con qué fiabilidad)

| Dato | Valor | Fiabilidad |
|---|---|---|
| Encargos con gasto anotado | 36 (empresa-virtual-sim) | medido |
| Gasto de ejecutoras + revisoras + Codex | **9.169.919 tokens** (ejecutoras 6.981.772 · revisoras 1.841.164 · Codex 346.983) | **suelo**: 9 encargos tienen cifras redondas (30.000, 45.000, 150.000…), es decir, estimadas |
| Gasto de las directoras (`medir.py --fabrica`) | 9 chats, **2.845.575 tokens** | medido, sin caché; mezcla proyectos; **no está en los topes** |
| Líneas de código añadidas | 26.543 en 36 encargos → **345 tokens por línea** | medido (git) |
| Tiempo de cada encargo (foto → fusión) | 34 encargos: suma 592 min (≈10 h), mediana 17 min | medido; la misión 2 (11–36) duró ≈45 h de reloj, solo el 15 % fue construir |
| Revisiones aparte | 31 informes | solo 15 tienen tokens anotados → 1,84 M es un suelo |
| Revisión de la spec (Codex/Claude) | ~65.000–115.000 tokens por pasada | casi nunca anotado |
| Ampliaciones de tope que tuviste que autorizar | **7** en 36 encargos (5 de ellas por cambios de 3–6 min) | medido |
| Papel generado en `.brain/fabrica/` | 2,4 MB frente a 0,8 MB de código y 0,8 MB de pruebas | medido |
| Tiempo y esfuerzo tuyo (leer, aprobar, esperar) | — | **no medido** |
| Si lees los informes y evidencias | — | **no medido** (pregunta para ti, sección 7) |
| Comparación «misma tarea sin fábrica» | — | **no medido**: nunca se hizo el mismo encargo dos veces (ver sección 4) |

Reparto del gasto: ejecutoras Sonnet 76 %, revisoras 20 %, **Codex solo 3,8 %**. DeepSeek: ningún encargo medido. La premisa «Codex barato como ejecutora» casi no pesa en el gasto real; lo que pesa es Claude en todos los papeles.

## 3. Lo que muestran los datos, pieza por pieza

### Cuánto cuesta según el tamaño del encargo
| Tamaño (líneas añadidas) | Encargos | Tokens medios | Tokens por línea |
|---|---|---|---|
| Pequeño, ≤150 | 8 (019–024, 029, 033) | 50.786 | **989** |
| Medio, 151–700 | 14 | 309.422 | 681 |
| Grande, >700 | 14 | 316.552 | 224 |

Los pequeños salen caros **por línea** porque la ceremonia es fija. Ojo: los encargos 019 a 025 (cambios de 3 a 6 minutos cada uno, 28.000–69.000 tokens) fueron **sin revisión aparte y funcionaron**: Darwin probó el profesor con Google real tras el 025 y dijo que funciona. Es decir, el atajo ya se usó de hecho y no rompió nada.

### Revisión aparte por encargo
- 31 revisiones; **en unas 11 hubo corrección** (devuelto o reparos aplicados; cuenta aproximada por los commits «vuelta»), 20 no cambiaron nada (solo «menores»).
- **En la segunda mitad (encargos 026–036): 1 corrección de 11** (la 034: un reto imposible de resolver con los comandos de la lección; hallazgo real y bueno). Coste anotado de esas 11: ≈1,04 M tokens.
- Varias devoluciones tempranas (007, 008) fueron por «las pruebas no detectan mutaciones», valioso pero pedante para código de práctica local.
- En el 029 la revisión dio 0 hallazgos útiles (el único comentario era un archivo del propio arnés).
- Ruido típico: «menor, nombre/estilo», escenarios que el propio revisor llama «poco realistas».

### Revisión de la spec
- Spec 003: rechazada 2 veces, aprobada a la 3.ª. Spec 005: igual. Hallazgos reales y concretos (huecos «GRANDE»).
- Spec 004 (6 líneas): rechazada; fue **útil** (la causa real era el botón deshabilitado, no lo que suponía la spec), pero costó ~65.000 tokens y cambió el camino de «corto» a «completo».
- Con Codex como revisor falló de formas conocidas (caja sin leer archivos, 5 intentos en la fase 6: lo más lento del experimento, y ~115.000 tokens no anotados).
- En el experimento VMware (fase 6) un cambio de 1 función costó: ejecutora 72.113 + probador 90.644 + Codex ≈115.000 (spec) ≈ 278.000 tokens en 12 min.

### Revisión de consumo
- 2 pasadas (spec 001/003 y spec 005): **ambas «dentro del presupuesto», 0 hallazgos**. Medía milisegundos de un simulador local. Valor medido: ninguno hasta hoy.

### Prueba de uso real
- Evidencias de 0,6–4 KB por encargo o spec. Es la única comprobación que ve algo que las pruebas no ven (en el 029 se simuló un comando lento en el navegador). Barata y útil.

### Carta y topes
- Los topes **nunca pararon nada peligroso**: el mayor encargo gastó 661.948 (tope 800.000). Sí generaron **7 autorizaciones tuyas** de «un encargo más», algunas por cambios de minutos. Es fricción sin protección demostrada.

### Directora en chat aparte
- 9 chats, 2,8 M tokens (≈31 % encima del gasto de ejecución). Para un encargo pequeño es un chat entero para algo que el chat actual ya sabe hacer.

### Modo automático
- Funciona: los encargos 030–033 se hicieron seguidos de madrugada en 66 min de construcción sin preguntarte. Es lo mejor de la fábrica **para misiones largas**.

### Camino corto (spec 088)
- «Estreno real» pendiente en su propia spec, pero la sección 8 está vacía y el único caso (029) **empezó corto y acabó completo** porque la spec fue rechazada. Nunca se ha medido un camino corto de punta a punta. Además sigue exigiendo spec, revisión de spec y prueba de uso real: para 6 líneas sigue siendo mucho.

### Papeleo
- 2,4 MB de informes, revisiones, evidencias y contratos frente a 1,6 MB de producto (código+pruebas). **No medido si alguien lo lee.** Los informes por spec (003/004/005, más `informe.md`) repiten lo que ya dicen las revisiones y las notas del chat.

### Ejecutoras
- Sonnet como subagente: 76 % del gasto, funciona. Codex en esfuerzo alto: probado, barato (34–143 k), pero el Python de su caja no corre pruebas, así que las corre la directora (coste extra). DeepSeek: sin ningún encargo medido; los avisos de la skill (sin caja de seguridad, `--auto`) lo hacen apto solo para cosas inocuas, siempre con revisión.

### Spec 089 (paralelo)
- Con encargos de mediana 17 min y los huecos reales de reloj (el 85 % no es construir: esperas, spec, tu prueba), el paralelo ahorraría como mucho unos minutos por misión; añade riesgo de solapes y un tercer sitio donde esperar. **No aprobada y recomiendo seguir en pausa** (o descartar).

## 4. Comparación con trabajar sin fábrica (límites honestos)

No hay un solo caso en el que la misma tarea se haya hecho de las dos maneras, así que **no se puede dar una cifra de ahorro o pérdida real**. Lo que sí hay:

- **Cerca de un «sin fábrica»:** los encargos 019–025 (sin spec revisada ni revisión aparte): 28–69 k tokens, 3–6 min, cero fallos comunicados. Y la fase 1 de la web (spec 090, v1.61.0, 691 líneas) hecha en **un solo chat** con una revisión aparte y una prueba de uso real: la revisión halló 1 fallo real (fuga por enlace simbólico) y 5 menores, 142 líneas de pruebas. Gasto no medido.
- **Estimación (no medida):** el 029 hecho por una sola IA habría costado del orden de la ejecutora (≈35–60 k) en vez de 179 k+, es decir **3 a 5 veces menos**, con el riesgo de no tener la revisión que dio 0 hallazgos. Lo único que la fábrica aportó ahí y una IA sola podría saltarse es la causa real del fallo; se mitiga con la regla «encuentra la causa antes de cambiar nada».
- **Lo que una sola IA no hace igual en grande:** la revisión de spec con negocio sellado, los topes que protegen un gasto grande, el alcance de archivos, y el «Frankenstein» (specs 003/005 rechazadas con motivos reales) son defensas **que sí valen** cuando hay muchos encargos y mucho que romper.

Propuesta para medirlo de verdad (sin coste para ti): en el próximo cambio pequeño, hacerlo directo y apuntar tiempo y tokens; en el próximo grande, la fábrica de siempre. Dos datos, dos tamaños.

## 5. Umbral: «esto no necesita fábrica»

**Ninguna fábrica (una sola IA, el chat normal, con pruebas y lectura del diff)** si se cumplen **las cuatro**:
1. Toca **3 archivos o menos** y añade **unas 150 líneas o menos** (todos los pequeños medidos: 3–6 min).
2. **Nada delicado:** pagos, permisos, datos de usuarios, servidores reales, seguridad, red, accesos, subir a GitHub.
3. **Se conoce la causa** o es un cambio de texto, estilo o valor (si hay que investigar o diseñar, no es pequeño).
4. Cabe en un solo encargo y no depende de otros pendientes.

Lo que se hace en ese caso: la IA dice en una frase qué va a tocar y cuánto tardará, lo hace, corre las pruebas completas, te enseña un resumen del diff y tú pruebas lo visible. **Sin spec formal, sin revisor de spec, sin revisión aparte, sin informe, sin autorizar tope.**

**Camino corto (de 150 a ~700 líneas o 4–6 archivos, sin lo delicado):** spec corta, una sola revisión de spec, un encargo, revisión aparte solo si hay lógica nueva, prueba de uso real breve.

**Fábrica completa:** más de ~700 líneas, o más de un encargo, o algo delicado, o una spec con huecos de negocio.

## 6. Decisión por pieza (recomendación)

| Pieza | Decisión | Por qué (dato) |
|---|---|---|
| Spec 035: carta, tres puertas, spec congelada, alcance de archivos | **Dejar, solo para grandes** | La puerta (a) fue lo que más valió; el alcance es un programa gratis |
| Spec 035: topes de misión (encargos y tokens) | **Simplificar** | 7 autorizaciones tuyas, 0 paradas útiles. Dejar un tope por encargo y que el de misión **avise** en vez de pedirte permiso |
| Spec 040: `/fabrica si/no` y directora en chat aparte | **Simplificar** | Chat propio y 2,8 M tokens: reservarlo a misiones grandes; en pequeño actúa el chat actual |
| Spec 050: modo automático | **Dejar (grandes)** | 30–33 funcionaron de madrugada, sin preguntarte |
| Revisor de spec (skill y guardián `veredicto`/`vueltas`) | **Dejar solo para grandes; 2 vueltas máximo** | Rechazos reales en 003 y 005; en 004 costó 65 k por 6 líneas |
| Revisión aparte por encargo | **Dejar solo para grandes o con lógica nueva; quitar en ≤150 líneas** | 20 de 31 sin cambios; 1 de 11 en la segunda mitad |
| Revisión de consumo | **Quitar** (volver si la spec trae un presupuesto de recursos real) | 2 de 2 sin hallazgos |
| Prueba de uso real | **Dejar, más ligera** | La única que ve lo que no ven las pruebas; evidencia de 1–4 KB |
| Informes finales de 6 secciones y evidencia por requisito | **Simplificar** | Repiten revisiones y notas; 2,4 MB; lectura tuya no medida. En pequeño, una línea |
| Camino corto (spec 088) | **Reemplazar por el umbral de arriba** | Nunca medido de punta a punta; el único caso acabó completo |
| Ejecutoras: Claude/Codex alto | **Dejar** | Codex 3,8 % del gasto; Sonnet funciona |
| Ejecutora DeepSeek | **Dejar solo para encargos inocuos con revisión; no ampliar** | Sin ningún encargo medido |
| Spec 089 (paralelo) | **Seguir en pausa o descartar** | Ahorro pequeño, riesgo de solapes, nada medido |
| Foto/alcance como paso manual | **Simplificar** | Dos fallos conocidos (carpeta equivocada, `R-1`); que lo haga solo `arrancar` |
| Kits y plantillas de la fábrica | **Sin cambios por ahora** | Solo `PLANTILLAS_FABRICA` y `CARTA_EJECUTORA` la mencionan; no se hallaron problemas de gasto aquí |

## 7. Preguntas, vacíos y lo que NO se midió

- Tu tiempo real de aprobar, leer y esperar; si lees los informes y las evidencias (ahora mismo son papel sin lector demostrado).
- Tokens de la directora por encargo, de las revisiones de spec y de varias revisiones aparte.
- Comparación real con una sola IA (propuesta en la sección 4).
- No se miró Prominimap, ni se tocó nada.
- Los datos salen de **una** fábrica grande (empresa-virtual-sim) más pruebas antiguas; el umbral de 150 líneas es una lectura de esos datos, no una ley.

## 8. Qué decisión tomar primero

**Aprobar el umbral de la sección 5** (≤150 líneas y ≤3 archivos, sin lo delicado y con causa conocida = sin fábrica). Es la decisión que más tiempo y gasto quita y de la que cuelgan casi todas las demás.

## 9. Anexo: antes y después de las versiones 1.61.1 a 1.61.3 (pedido por el chat #38)

**Medido, «antes»:** todo lo de arriba (36 encargos de empresa-virtual-sim, último el 036 del 17-nov 12:20).
**Medido, «después»:** **nada**. Ningún encargo de ninguna fábrica se ha hecho todavía con estas versiones (empresa-virtual-sim no tiene commits desde el 18-nov y `gasto.json` acaba en el 036). El efecto de los cambios es **no medido**; lo que sigue es lo que deberían cambiar, no lo que han cambiado.

| Queja de Darwin | Qué la ataca | Estado |
|---|---|---|
| **Más caro: cambios pequeños** (029: ≈179.500 tokens para ~6 líneas) | 1.61.1: hasta 150 líneas y 3 archivos, un subagente, sin spec, revisión ni informe | **Atendida en papel**; sin medir. Se verá con el primer cambio pequeño real |
| **Más caro: revisión de consumo** (2 pasadas, 0 hallazgos) | 1.61.2: solo bajo petición | **Atendida** (se deja de gastar; ahorro no medido porque nunca se anotó su coste) |
| **Más caro: la directora** (2,85 M tokens, sin medir por encargo) | 1.61.2: delega lo mecánico a Haiku; 1.61.3: se mide su gasto por encargo (no cuenta en topes) | **Medición atendida; ahorro por comprobar**. Haiku sin probar |
| **Más tedioso: pasos sueltos de la directora** (`foto`, `alcance`, `gasto`, `topes`…) | 1.61.3: `cerrar-encargo` en un comando | **Atendida en parte**: falta ver si de verdad le ahorra mensajes |
| **Más tedioso: 7 autorizaciones de tope tuyas** | Nada | **No atendida**: los topes de misión siguen pidiéndote permiso |
| **Más tedioso: papeleo** (2,4 MB, informes de 6 secciones) | Solo en la ruta A (sin informe); en B y C sigue igual | **No atendida** en encargos medios y grandes |
| **Revisión aparte** (20 de 31 sin cambios) | Solo en ruta A y en camino corto sin lógica nueva | **Atendida en parte**; en completo sigue en cada encargo |
| **Revisor de spec** (65 k por 6 líneas) | Solo indirecto: lo pequeño ya no lo usa | **Atendida solo para lo pequeño**; las 2 vueltas máximo no están aplicadas en las skills |

**Para medirlo bien:** repetir esta revisión cuando haya al menos 3 encargos pequeños (ruta A) y 1 misión grande hechos con 1.61.3; con `gasto_directora_entre` ya habrá cifra de la directora por encargo. Comparar con las medias de arriba: pequeños ≈51.000 tokens y 3-6 min; encargo medio ≈309.000; directora sin medir.
