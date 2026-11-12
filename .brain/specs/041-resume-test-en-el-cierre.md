# Spec 041: «prueba de retomar» como segundo criterio del cierre por bloque (punto 36)

- **Estado:** aprobada por Darwin el 2026-11-12 y programada en 1.41.0
- **Fecha:** 2026-11-12
- **Origen:** idea de ODD (informe `archive/informe-odd-gentle-shell-2026-11-09.md`, propuesta 1): el tamaño no clasifica; clasifica el «resume test» (¿se puede retomar el trabajo solo con la petición y el `git diff`?). Hoy el cierre por bloque (spec 033) usa solo un contador: 15 archivos editados sin cerrar. Un contador no ve lo importante: una decisión o una causa descubierta puede existir solo en la conversación aunque se hayan editado 3 archivos.
- **Ya existente:** `spec-antes-de-programar` ya usa la prueba de retomar en su paso 0 (decide si hace falta spec). Este punto solo añade el uso en el cierre.
- **Nota de orden:** el punto 36 pedía esperar los resultados del 35 (`medir.py --ritual`, 2 semanas). Darwin dijo «go» el 2026-11-12 sabiéndolo; se hace ahora y se mide después con el mismo comando.

## 1. Objetivo
Que el cierre no dependa solo de contar archivos: antes de dejar un bloque sin línea de registro, la IA se hace la prueba de retomar, y si falla cierra ya, aunque lleve menos de 15 ediciones.

## 2. En alcance
- [ ] Skill `cerrar-una-tarea` (es y `.en.md`): una regla nueva, una sola vez escrita: «Antes del tope de 15, si alguien que solo viera la petición y el `git diff` no podría retomar el trabajo (porque hay una decisión, una causa descubierta, un paso pendiente o algo que Darwin debe probar que solo está en la conversación), se cierra ya, con una línea en `decisions.log`.»
- [ ] `CLAUDE.md` de cerebro-vivo: una línea que remita a esa regla (no repetirla).
- [ ] Texto del aviso del guardián `cierre.py` (en `textos.py`, es/en): el aviso de «sin línea de registro» menciona la prueba de retomar para que la IA la aplique al recibirlo. No cambia cuándo salta (sigue en 15 ediciones o al cerrar el chat).
- [ ] Prueba en `tests/` de que la skill y los textos es/en tienen la regla (la prueba de paridad ya existe y la vigila).
- [ ] `VERSION`, `CAMBIOS.md`, `manifiesto.json`.

## 3. Fuera de alcance
- Hacer que el guardián juzgue por sí mismo si se puede retomar: no es mecánico. Una aproximación automática (por ejemplo, cerrar al editar `specs/` o `pendientes.md`) queda para después, solo si `medir.py --ritual` muestra que la regla escrita no basta.
- Tocar el tope de 15 ni `cierre_por_bloque` en `guardianes.json`.
- La regla de «más de 2 archivos» de `spec-antes-de-programar`: ya usa la prueba de retomar.

## 4. Riesgos
- Es una regla para la IA, no un candado: puede olvidarse. Se acepta; el contador de 15 sigue de red de seguridad.
- Pueden aumentar un poco los cierres (más llamadas); se mide con `medir.py --ritual` a las 2 semanas.

## 5. Archivos
`.claude/skills/cerrar-una-tarea/SKILL.md` y `.en.md`, `CLAUDE.md`, `textos.py`, `tests/`, `VERSION`, `CAMBIOS.md`, `manifiesto.json`.

## 6. Verificación
`python -m unittest discover tests` en verde; leer el aviso nuevo provocándolo; en 2 semanas, `python .brain/guardianes/medir.py --ritual` para ver si los cierres por chat suben o bajan.
