# Spec 096: refinar las skills del arnés, revisando su utilidad y su uso

- **Estado:** **aprobada por Darwin el 2026-11-27** (pedida el mismo día: «programa un refinamiento de nuestras skills, revisar utilidad y uso»). Sin contestar aparte a la sección 8: se toman sus tres respuestas recomendadas (medir todos los proyectos, fábrica solo en tamaño, archivar solo del repo). La aprobación cubre la fase 1 (medir) y la fase 2 (informe); **no quitar, fusionar ni reescribir ninguna skill hasta que Darwin vea el informe y diga cuáles.**
- **Avance (2026-11-27, v1.68.0):** fase 1 hecha (`medir.py --skills --todos` y `--proyectos`, con lecturas de `SKILL.md`, proyectos y tamaño; sin repetidos ni experimentos). Fase 2 hecha: informe en `archive/notas-chats/2026-11-27-informe-skills-clasificacion.md`. Medido en 25 carpetas: **33 de 44 skills se usan** (contra 15 de 44 al medir solo este repo, lo que confirma que el 0 de un solo proyecto engañaba). Falta la fase 3, que espera las tres decisiones de Darwin del informe (sección 6).
- **Fecha:** 2026-11-27
- **Se apoya en:** spec 079 (skills y su medición), spec 095 (nuevas skills solo por propuesta aprobada), regla «mover, no borrar», spec 090 sección 15 (revisión de la fábrica, pendiente 62).
- **Medición de partida** (`medir.py --skills`, solo los chats de cerebro-vivo, 2026-11-27): 15 de 44 skills usadas. Cuatro concentran casi todo: `traspaso-in` (96 veces, 55 chats), `subir-a-github` (23), `pendiente` (12) y `traspaso-out` (7). 29 skills salen con 0.

## 1. Problema
- **Pocas skills hacen casi todo el trabajo** y 29 de 44 no aparecen en los registros. Cada skill cuesta: su descripción entra en el contexto de cada chat y mantenerla (es y `.en.md`, paridad, manifiesto) es trabajo.
- **El 0 no siempre significa «inútil».** `medir.py` solo cuenta llamadas a la herramienta Skill y comandos `/skill` escritos. Una skill que la IA aplica leyendo el archivo, o que los hooks sustituyen (`cerrar-una-tarea` sale con 0 y el cierre se usa en cada chat), queda infravalorada. Y solo se mide este repo: skills pensadas para otros proyectos (`seguridad-en-sistemas-reales`, `hermanos`, las de fábrica) no tienen aquí dónde usarse.
- **Tamaño desigual:** `directora-de-fabrica` pesa 15 KB y `revisor-de-spec` 7,6 KB; la mayoría pesa 1 a 3 KB. Las pesadas gastan contexto cuando se cargan.
- **Solapes posibles** a revisar: `adopta` y `adoptar-indice-existente`; `revisor-independiente`, `revisor-de-spec` y `revisor-de-consumo`; `resumen` y `pendiente`; `fabrica` y `directora-de-fabrica`.
- **Descripciones:** la descripción decide cuándo se dispara la skill. Una descripción vaga hace que no se use o que se use sin venir a cuento.

## 2. Fases
1. **Medir mejor (solo lectura).**
   - `medir.py --skills --proyecto RUTA` en cada proyecto que usa el arnés (LoboHook, ProMaps, yu-gi-wow, Prominimap y los demás) y sumar los resultados.
   - Cuenta aparte de «la IA leyó `SKILL.md`» (lectura directa del archivo), para no infravalorar las que se aplican sin la herramienta Skill.
   - Resultado: una tabla con, por skill, usos en total, proyectos que la usan, última vez y tamaño en bytes.
2. **Clasificar y proponer (sin tocar nada).** Cada skill en una de cuatro cajas, con una frase de motivo:
   - **Núcleo:** se usa a menudo; solo afinar.
   - **A demanda:** casi nunca, pero cuando toca es necesaria (por ejemplo seguridad, fábrica); se queda, con descripción precisa.
   - **Fusionar o acortar:** solapes y skills pesadas.
   - **Candidata a archivar:** sin uso en ningún proyecto y sin hook que la apoye. Se propone a Darwin con el porqué; se mueve a `archive/skills/`, **nunca se borra**.
   La propuesta va como informe en `.brain/archive/notas-chats/` y su resumen a Darwin en llano.
3. **Refinar lo aprobado, de una en una.** Para cada skill que Darwin apruebe tocar:
   - Reescribir la descripción (cuándo sí y cuándo no) y comprobar con 3 frases de ejemplo que se dispararía bien.
   - Trocear las pesadas: el cuerpo corto y el detalle en un archivo aparte que se lee solo si hace falta.
   - Fusionar o archivar según lo decidido, con su edición `.en.md`, y actualizar `README` de skills y referencias (`CLAUDE.md`, biblioteca).
4. **Volver a medir** tras 4 semanas de uso y comparar: skills usadas, tamaño total cargado en contexto y número de skills.

## 3. En alcance
- [ ] Fase 1: `medir.py --skills` suma varios proyectos y cuenta la lectura directa de `SKILL.md`; columna de tamaño. Pruebas en `tests/test_medir.py`.
- [ ] Informe de clasificación (fase 2) y su resumen en llano para Darwin.
- [ ] Refinado de las skills aprobadas (fase 3), con es/en y la prueba de paridad en verde.
- [ ] `VERSION`, `CAMBIOS.md`, `manifiesto.json` en cada entrega.

## 4. Fuera de alcance
- Borrar skills: solo se archivan, y solo con el sí de Darwin.
- Crear skills nuevas: eso va por la spec 095 (propuesta aprobada).
- Cambiar los guardianes ni los hooks.
- Decidir por una sola cifra: con pocos chats, un 0 es una tendencia, no una sentencia (lo avisa el propio `medir.py`).
- La revisión de la fábrica (pendiente 62) sigue su propio camino; aquí solo se mira el tamaño y el solape de sus skills.

## 5. Riesgos
- **Quitar una skill que en realidad se usa** sin la herramienta Skill. Mitigación: fase 1 cuenta la lectura directa y todo pasa por Darwin.
- **Romper referencias** (otras skills, `CLAUDE.md`, guardianes y textos que nombran una skill). Mitigación: buscar con `buscar.py` cada nombre antes de fusionar o archivar, y la prueba de paridad y la de manifiesto en verde.
- **Proyectos con el arnés viejo:** una skill archivada aquí sigue en los proyectos hasta que actualicen; `actualizar_arnes.py` no borra lo que ya tienen. Hay que ver cómo avisarles (por definir en la fase 3).

## 6. Plan de verificación
- `python -m unittest discover tests` en verde en cada fase.
- Fase 3: por cada skill tocada, tres frases de prueba que deben dispararla y una que no.
- Fase 4: nueva medición comparada con la de partida (sección inicial).

## 7. Cierre
- [ ] Spec aprobada por Darwin antes de programar
- [ ] Informe de clasificación visto por Darwin
- [ ] Línea añadida a `.brain/decisions.log` en cada fase

## 8. Preguntas para Darwin
1. ¿Mido también los otros proyectos (LoboHook, ProMaps, yu-gi-wow, Prominimap)? Recomendado: sí; solo leo sus registros, no toco nada.
2. ¿Las skills de fábrica (`fabrica`, `directora-de-fabrica`, `revisor-*`, `prueba-de-uso-real`) entran ahora o esperan al resultado del pendiente 62? Recomendado: entran solo para medir tamaño; las decisiones esperan al 62.
3. ¿Una skill archivada se retira también de los proyectos al actualizar, o solo del repo? Recomendado: solo del repo; en los proyectos se avisa y la quita quien quiera.
