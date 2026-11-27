# Spec 095: sugeridor de lecciones y skills al cerrar (idea tomada de Hermes Agent)

- **Estado:** **aprobada por Darwin el 2026-11-27; fase 1 (lecciones) implementada en v1.67.0**, sin probar en chats reales. Darwin aprobó sin contestar aparte a la sección 9: se tomaron sus tres respuestas recomendadas (solo lecciones en la fase 1, solo en cerebro-vivo, solo avisar). Quedan para la fase 2 la cola `propuestas.md`, sus avisos de tamaño y de skills largas o repetidas.
- **Fecha:** 2026-11-27
- **Se apoya en:** spec 026 (lecciones y guardián de hitos), spec 033 y 041 (cierre por bloque y prueba de retomar), spec 090 sección 4 (bandeja de propuestas).
- **Origen:** comparación con Hermes Agent (Nous Research, código abierto, MIT). Datos contrastados el 2026-11-27 con su documentación oficial (memoria, skills, sesiones). **No se pudo leer su código de revisión** (`agent/background_review.py`, error 503): el prompt y los valores por defecto de frecuencia no están confirmados.

### Lo contrastado con la documentación de Hermes (2026-11-27)
- La revisión corre **después de cada turno**, con el mismo modelo del chat por defecto, y la documentación admite que puede gastar «una parte importante» de los tokens. Aquí no se gasta una llamada extra: revisa la IA del chat.
- Memoria acotada: 2.200 y 1.375 caracteres; al pasarse da error y el agente consolida. No poda sola. Misma filosofía que los topes de 8 KB.
- Aprobación humana opcional (`write_approval`), **apagada por defecto**: escribe sola. Cerebro la deja siempre encendida.
- Señales para crear skills: flujo no trivial, error resuelto y corrección del usuario. Coinciden con las de esta spec.
- Tiene un avisador que marca skills demasiado largas; no vi prevención de duplicados al crearlas.
- Búsqueda en sesiones pasadas: SQLite con texto, **sin IA** (el README dice «con resumen por LLM» y la documentación lo contradice). Alimenta el pendiente 66.
- Fallo visto en sus issues: un parche de skill en cola no se aplica si la cita se parte en dos líneas. Lección para `propuestas.md`: guardar la propuesta entera, no una cita.

## 1. Cerebro Vivo frente a Hermes Agent

| Tema | Hermes Agent | Cerebro Vivo | Quién va por delante |
|---|---|---|---|
| Dónde vive la memoria | Archivos Markdown | `.brain/` en Markdown, con Git | Empate; Cerebro tiene historial y topes de tamaño |
| Quién decide qué se guarda | El agente, solo, cada pocos turnos | La IA y Darwin, al cerrar la tarea (`cerrar.py`, `/leccion`) | **Hermes** en automatismo; **Cerebro** en control |
| Cuándo se acuerda de guardar | Revisión interna tras cada turno (frecuencia exacta sin confirmar) | Hitos mecánicos (error resuelto, archivo delicado, cambio grande) más prueba de retomar | **Hermes** cubre más casos; Cerebro es más fiable en los que cubre |
| Skills | Las crea solo al resolver algo difícil | Las escribe Darwin o la IA a mano, con prueba de paridad es/en | **Cerebro** en calidad; **Hermes** en cantidad |
| Basura en la memoria | Riesgo real: se llena sola | Topes de 8 KB, «solo lo que falta», mover no borrar | **Cerebro** |
| Buscar en el pasado | Búsqueda de texto en sesiones previas | `buscar.py` sobre `.brain/`; traspasos archivados aparte | **Hermes** (ver pendiente 65) |
| Aprobación humana | Opcional y apagada por defecto | Constitución y sí de Darwin para lo irreversible | **Cerebro** |

Lectura en llano: Cerebro Vivo es más ordenado y seguro; Hermes se acuerda de más cosas sin que nadie se lo pida. Lo que a Cerebro le falta no es otra memoria: es **acordarse de lo que no fue un error**.

## 2. Problema
El guardián de hitos (spec 026) solo salta ante tres señales: un error que se resolvió, un archivo marcado como delicado y una modificación grande. Se escapan lecciones que no dejan huella mecánica:
- Darwin corrige a la IA («no, así no», «te dije que…») y la IA acepta la corrección, pero nadie la apunta.
- Se toma una decisión de diseño sin que falle nada.
- Se repite el mismo procedimiento a mano y nunca llega a ser una skill.

## 3. Qué hace (propuesta)
Al cerrar el bloque (mismo momento en que hoy actúa `cierre.py`), un paso nuevo, **el sugeridor**, hace dos cosas:
1. Detecta **señales baratas en el registro del chat**, sin llamar a ninguna IA externa (constitución, regla 8): mensajes de Darwin con marcas de corrección («no», «mal», «otra vez», «te dije», «en vez de»), decisiones («mejor», «descartado», «vamos con») y la misma orden repetida 3 veces o más.
2. Si hay señales, **devuelve un aviso a la IA que está trabajando**, con las frases concretas y esta pregunta: «¿alguna de estas es una lección, una decisión o un procedimiento repetido que aún no está apuntado?». Es la propia IA del chat quien hace la revisión que en Hermes hace el agente; no se gasta una llamada extra.

La IA responde de una de tres formas: `lecciones.py --tema …` (apunta), propone una skill en la bandeja, o `lecciones.py ninguna "motivo"` (ya existe). Todo lo propuesto **queda como propuesta; no entra solo en la memoria**: lo aprueba Darwin.

## 4. En alcance
- [ ] `sugeridor.py` en `.brain/guardianes/`: lee el registro del chat y devuelve señales (solo lectura, solo librería estándar, si falla calla).
- [ ] Llamada desde `cierre.py`, con la misma pauta que `hitos.py`: avisa una vez por respuesta y se corta solo si se repite (spec 038).
- [ ] Antes de avisar, comprobar con `buscar.py` que no hay ya una lección sobre lo mismo (no repetir).
- [ ] Máximo 3 señales por aviso y un tope de avisos por chat, ajustables en `guardianes.json` (`sugeridor_activo`, `sugeridor_max`).
- [ ] Propuestas de skill en `.brain/propuestas.md`, que funciona como **cola de aprobación**: una por bloque, con fecha, porqué, chat de origen y el texto completo propuesto (no una cita suelta). Estados: pendiente, aprobada, descartada. Nada pasa a la memoria sin aprobar. La bandeja web de la spec 090 la leerá cuando exista.
- [ ] Aviso de tamaño: si `propuestas.md` o la carpeta de lecciones pasa su tope (8 KB por archivo), el sugeridor avisa de trocear o podar antes de añadir más, en vez de seguir creciendo (idea del límite con error de Hermes).
- [ ] Aviso de skill propuesta demasiado larga (tope por definir en la fase 2) y comprobación de que no repite el nombre ni el tema de una skill existente.
- [ ] Textos del aviso en `textos.py` es/en; documento en `biblioteca/` con su edición `.en.md`; skill `cerrar-una-tarea` con una línea nueva (es y `.en.md`).
- [ ] Pruebas en `tests/`: con un registro de ejemplo salta; sin señales calla; con lección ya apuntada no repite; si falla no rompe el cierre.
- [ ] `VERSION`, `CAMBIOS.md`, `manifiesto.json`.

## 5. Fuera de alcance
- Escribir lecciones o skills **sin** aprobación. Es justo el riesgo que Hermes asume y Cerebro no.
- Llamar a un modelo externo para juzgar la conversación (coste, tiempo máximo y plan B; no hace falta).
- Reentrenar ni «mejorar» nada fuera de la memoria.
- Buscar en los traspasos archivados (es el pendiente 66; basta ampliar `buscar.py`, sin IA).
- Tocar el tope de 15 ediciones ni la prueba de retomar.

## 6. Riesgos
- **Falsos avisos:** las marcas de corrección son palabras sueltas y pueden saltar sin motivo. Mitigación: máximo 3 por aviso, tope por chat y corte automático si se repiten. Hay que medirlo antes de dejarlo activo en los proyectos.
- **Cansancio de avisos:** si molesta, la gente lo apaga. Por eso `sugeridor_activo` y empezar solo en cerebro-vivo.
- Sigue siendo una regla para la IA, no un candado: puede contestar «ninguna» sin pensar. Se acepta, igual que en la spec 041.

## 7. Plan de verificación
- `python -m unittest discover tests` en verde.
- Prueba de uso real: tres chats de cerebro-vivo con el sugeridor activo; contar cuántas señales eran útiles y cuántas ruido (`medir.py`). Si menos de la mitad sirve, ajustar o descartar.

## 8. Cierre
- [ ] Spec aprobada por Darwin antes de programar
- [ ] Probada en tres chats reales
- [ ] Línea añadida a `.brain/decisions.log`

## 9. Preguntas para Darwin
1. ¿Aprobar solo la parte de **lecciones** (fase 1) y dejar las **skills propuestas** para una fase 2? Recomendado: sí, porque lo segundo exige ver el mismo procedimiento en varios chats.
2. ¿El sugeridor empieza **solo en cerebro-vivo** y pasa a los proyectos tras medirlo? Recomendado: sí.
3. ¿El aviso puede bloquear el cierre como el de hitos, o solo avisar? Recomendado: solo avisar al principio.
