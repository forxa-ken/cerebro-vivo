# Informe del experimento Cerebro Vivo contra ODD — Ronda 1 (2026-11-09)

Escrito por Claude (cerebro-vivo #33) para Darwin. **Muestra de 1 por lado: solo es una tendencia, no una prueba.** La ronda 1 queda archivada (etiquetas `ronda1-A` y `ronda1-B` en `vmware-automatizacion`). Se repite como ronda 2 porque los cuelgues de Codex contaminaron el resultado.

## 1. Qué se comparó
- Mismo encargo (`experimento/encargo.md`, 7 criterios de aceptación), misma base (cimientos, spec 001) y mismo aprobador (Codex, regla fija en `AGENTS.md`, esfuerzo medio).
- **Rama A:** módulo **Instantáneas** con Cerebro Vivo completo (spec antes de programar, guardianes, lecciones, cierre).
- **Rama B:** módulo **Clonado desde plantilla** con ODD (un `CLAUDE.md` con el flujo, documento `odd/tasks/`, sin memoria ni guardianes).
- Limitación de origen: cada método hizo un módulo distinto, así que parte de la diferencia puede ser del módulo y no del método.

## 2. Resultado de calidad (lo que se pudo comprobar)
| | A (Cerebro Vivo) | B (ODD) |
|---|---|---|
| Criterios del encargo cumplidos | 7 de 7, con prueba cada uno | 7 de 7, con prueba cada uno |
| Pruebas del módulo | 19 nuevas + 17 de cimientos, en verde (comprobado) | 25 nuevas + 17 de cimientos = 45, en verde (comprobado) |
| Código del módulo (líneas) | 20 (fachada) + cambios en motor/laboratorio; en total ~330 en `vmware_auto` | 97 + cambios en motor/laboratorio; en total ~391 en `vmware_auto` |
| Spec/documento previo | 483 palabras | 581 palabras |
| Documento de uso | `INSTANTANEAS.md` | `CLONADO.md` |
| Fallo suelto | 1 prueba del instalador de Mac, **ajena** (el archivo se guardó con fin de línea de Windows en esa carpeta; en la carpeta principal pasa) | ninguno |

## 3. Aprobador (Codex)
- **A:** 6 veredictos, 5 RECHAZADA y 1 APROBADA. Según A, 3 rechazos fueron de contenido (crear una instantánea sin visto bueno; fallos provocados como posible acción sin visto bueno; laboratorio en memoria frente a `vcsim`) y 2 fueron fallos técnicos (Codex no pudo leer archivos). Además 2 cuelgues de más de 15 minutos que A mató a mano.
- **B:** 2 veredictos, 1 RECHAZADA (el documento no aclaraba que el laboratorio en memoria es la primera versión del modo `vcsim`) y 1 APROBADA. Sin cuelgues.
- **El aprobador no es determinista:** un criterio rechazado en una ejecución lo dio por cumplido otra. Eso pesa tanto como cualquier diferencia de método.
- Ojo: «5 rechazos frente a 1» **no** se puede leer como «Cerebro Vivo comete más fallos». Dos de los de A son fallos de la herramienta, y la diferencia más grande es el criterio 5 sobre «crear», que dependía del módulo.

## 4. Coste medido (`medir.py`, mismo instrumento para las dos ramas)
| | A | B |
|---|---|---|
| Coste total del chat | ≈ 744k | ≈ 257k |
| Tokens nuevos | 140k | 61k |
| Salida | 28k | 19k |
| Arranque (lo que se carga al empezar) | 75k | 74k |
| Turnos de la IA | 41 | 10 |
| Mensajes tuyos / correcciones | 2 / 0 | 1 / 0 |

- A cuesta unas 2,9 veces más que B. Pero **en A entra la espera y los reintentos del aprobador** (cuelgues, mensajes míos para despertarla, 5 rechazos), que B no tuvo. No es una comparación limpia. Eso es justo lo que la ronda 2 corrige.
- El arranque es casi igual en las dos (≈ 75k): el arnés completo no cuesta más al abrir el chat; el sobrecoste viene del trabajo posterior.

## 5. Tiempo (incidencias en `vmware-automatizacion/experimento/incidencias.md`)
- Paradas de A que **no son del método**: ≈ 82 min esperando una respuesta de Codex que no llegaba, y ≈ 7 min más hasta que Darwin reinició Codex. Resta final ≈ 89 min (aproximada; sin confirmar si la primera parada también necesitó intervención).
- **Advertencia:** los relojes de las marcas de hora de los commits y de los chats no cuadran del todo entre sí (la rama B figura commiteada unos 2 minutos después de abrirse su chat, lo que no es creíble con ese trabajo). Por eso **no doy un tiempo total fiable**; en la ronda 2 se medirá con turnos y tokens.

- **Causa de los cuelgues (encontrada después, probada):** el aprobador lanzaba Codex sin cerrar la entrada estándar y Codex esperaba una entrada que nunca llegaba. Con la entrada cerrada contesta en 5-11 s. Fue un fallo del montaje del experimento, no del método ni de Codex. Reiniciar Codex solo funcionaba por casualidad. Corregido antes de la ronda 2.

## 6. Lo que dice cada rama que no quedó
- **A:** restaurar no modela el estado de disco ni la memoria; no hay límite de instantáneas por máquina; la línea de comandos no se probó como proceso real.
- **B:** el laboratorio no copia discos reales (solo cuenta GB); el todo-o-nada del clon es «por construcción» y con `vcsim` habrá que hacer una vuelta atrás real; una prueba de `--simular` por línea de comandos es débil.
- **Coste de tocar el módulo después:** las dos dicen «poco». B apunta un acoplamiento oculto (el motor conoce `clonado`); A mantiene las reglas solo en el motor.

## 7. Conclusión prudente
1. **Calidad: empate técnico** en lo comprobado (7 de 7 criterios con pruebas en las dos). La calidad fina (nombres, claridad, errores explicados) la valora Darwin al final; no la he juzgado.
2. **Coste:** B salió más barato, pero la medición favorece a B por los cuelgues y rechazos técnicos de A. No se puede decir cuánto del 2,9× es del método.
3. **Rigor:** Cerebro Vivo obligó a escribir spec, pasar el aprobador y dejar lecciones; ODD llegó a un resultado equivalente con menos pasos. Con una muestra, no se puede decir que el rigor extra se haya notado en el resultado.
4. **Lo aprendido del montaje (y la causa real de los cuelgues, ver sección 5):** el aprobador debe tener tope de tiempo y distinguir «error técnico» de «rechazo» (ya arreglado en la ronda 2), y el chat no debe terminar el turno «esperando» a una herramienta (regla añadida al encargo).

## 8. Qué se hace en la ronda 2
- Mismos módulos (decisión de Darwin), ramas nuevas `exp2-cerebro-instantaneas` y `exp2-odd-clonado` desde master, aprobador con tope de 3 min y reintento, `ERROR_TECNICO` aparte de los rechazos.
- Las dos ramas se miden con `medir.py` desde fuera (para B: `python .brain/guardianes/medir.py --proyecto RUTA_RAMA_B`), con el mismo instrumento.
