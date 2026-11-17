# Spec 088: camino corto de la fábrica (cambios pequeños sin ceremonia)

- **Estado:** **aprobada por Darwin el 2026-11-17.** El comportamiento ya está en el arnés desde la 1.60.10 y la 1.60.11 (órdenes de Darwin del 2026-11-16) y **no se ha probado en un encargo real**; esta spec deja escrito el porqué y cómo se mide.
- **Fecha:** 2026-11-17
- **Se apoya en:** spec 035 (fábrica con directora, revisor y tres puertas), spec 050 (modo automático y prueba de uso real), skills `directora-de-fabrica`, `revisor-de-spec`, `revisor-independiente` y `prueba-de-uso-real`.
- **Origen:** la directora de `empresa-virtual-sim` tardó demasiado en un cambio pequeño de un panel (un botón, un texto) porque pasaba por todo el camino: revisión de spec de hasta 3 vueltas, un encargo por requisito, Codex con esfuerzo máximo y revisión aparte. Darwin pidió un camino más corto para eso, sin quitar nada a lo delicado.

## 1. Objetivo
Que un cambio **pequeño y no delicado** pase por la fábrica en poco tiempo y con poco gasto, **sin perder las defensas que más valen**: la spec aprobada antes de programar (puerta (a)), el alcance de archivos, las pruebas de la directora, la lectura del diff y la prueba de uso real. Lo delicado y todo lo dudoso sigue por el **camino completo**, sin cambios.

## 2. Cuándo se usa (las dos condiciones a la vez)
- **Pequeño:** cabe en **un solo encargo** y toca **como máximo 3 archivos** de interfaz, texto o estilo.
- **No delicado:** no toca pagos, permisos, datos de usuarios, servidores reales, seguridad, red o servidor, accesos, ni subir a GitHub o a la página.
- **Ante la duda, o si hace falta más de un encargo: camino completo.**

## 3. En qué se diferencia del camino completo
| Paso | Camino completo | Camino corto |
|---|---|---|
| Spec | Completa | Corta |
| Aviso de tiempo | — | Antes de empezar, la directora dice a Darwin cuánto tardará (mirando encargos parecidos en `estado/`). Si calcula **más de 30 minutos**, espera su decisión. |
| Revisión de la spec | Hasta 3 vueltas | **Una sola vuelta**. Si el revisor la rechaza, se pasa al camino completo desde ese paso y se dice a Darwin en una frase. |
| Encargos | Uno por requisito | **Uno solo** |
| Esfuerzo de Codex | Máximo (Luna «Muy alto», decisión de Darwin del 2026-11-12) | **Alto** (más rápido, sigue haciéndolo bien) |
| Revisión aparte del encargo | En cada encargo | **No**. Se cierra con el alcance, las pruebas de la directora y la lectura del diff. El informe lo dice. |
| Prueba de uso real | Sí | **Sí**, aunque sea breve |
| Informe final | Normal | Dice que fue camino corto y por qué |

## 4. Qué NO cambia (no se negocia)
- Darwin aprueba la spec antes de programar (puerta (a)) y recibe el informe final (puerta (c)).
- El guardián de alcance, los topes de gasto y los frenos de la spec 050.
- La prueba de uso real hecha por una IA distinta de la que construyó.
- El camino completo, con esfuerzo máximo, para todo lo que no cumpla las condiciones de la sección 2.
- Nunca se salta un guardián ni una prueba.

## 5. Riesgos y límites honestos
- **Sin revisión aparte hay menos ojos.** Es el cambio de mayor riesgo. Se acepta porque el cambio es pequeño y de interfaz; si un defecto que la revisión aparte habría visto llega a Darwin, el camino se aprieta (ver sección 7).
- **Nada lo hace cumplir por código.** «Pequeño» y «delicado» los juzga la directora leyendo la skill; ningún guardián cuenta archivos ni detecta lo delicado. Si el juicio falla, el cambio delicado se cuela por el camino corto. Posible fase futura: que `fabrica.py` compruebe el número de archivos y palabras delicadas del encargo.
- **Esfuerzo alto de Codex:** la tabla de arriba se basa en una impresión de rapidez, no en una medición. Hay que medirlo.
- **Sin probar en un encargo real.** Solo hay pruebas automáticas de partes sueltas (por ejemplo, que `medir.py` encuentre los chats de la directora).

## 6. Plan de verificación
1. **Estreno real:** un encargo pequeño en `empresa-virtual-sim` (el panel con el arreglo del «Enter que se pierde»), por el camino corto.
2. **Medir** con `python .brain/guardianes/medir.py --fabrica`: tiempo y gasto del encargo, y comparar con un encargo pequeño parecido por el camino completo.
3. **Comparar el aviso con la realidad:** ¿el tiempo que dijo la directora era razonable?
4. **Mirar el resultado:** ¿llegó a Darwin algo roto o con extras no pedidos?
5. Anotar el resultado en esta spec (sección 8) y decidir si se confirma, se aprieta o se retira.

## 7. Criterio para confirmar, apretar o retirar
- **Confirmar** si, en al menos 3 encargos pequeños reales, el camino corto ahorra tiempo o gasto de forma clara y nada llegó roto a Darwin.
- **Apretar** (reducir el máximo de 3 archivos, o exigir revisión aparte en algún tipo de cambio) si algo defectuoso se coló que la revisión aparte habría visto.
- **Retirar** si el ahorro es pequeño o si hay un solo fallo grave: todo vuelve al camino completo.

## 8. Resultados de las pruebas reales
- (vacío; aún sin estrenar)

## 9. Decisiones de Darwin ya tomadas
- 2026-11-16: no hacer revisión aparte en encargos pequeños (1.60.10).
- 2026-11-16: camino corto con aviso de tiempo, una vuelta de revisión de spec, un encargo, Codex con esfuerzo alto, sin revisión aparte y con prueba de uso real breve (1.60.11).
- 2026-11-17: la limpieza de la fábrica va antes que esta spec; el modo automático nace encendido con la fábrica (1.60.12).

## 10. Cierre
- [x] Spec aprobada por Darwin (2026-11-17)
- [ ] Estreno real hecho y medido (sección 6)
- [ ] Resultado anotado en la sección 8 y decisión tomada (sección 7)
- [ ] Línea añadida a `.brain/decisions.log`
