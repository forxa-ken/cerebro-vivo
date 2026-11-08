---
name: implementada-no-es-hecha
description: Use when about to call a task finished or done.
---

# Implementada no es hecha

## Cómo (pasos)
1. «Implementada» = programada y con tests; «hecha» = Darwin la probó.
2. Hasta la prueba queda en «Esperando tu prueba» con los pasos concretos.
3. Decir en el mensaje qué prueba falta y en qué consiste.
4. No subir a GitHub antes de su confirmación, salvo orden expresa.

## Error que evita (caso real)
- Se dieron tareas por hechas sin que el dueño las probara y luego fallaron (p. ej. el idioma del manual en #68).

## Dónde está en el repo
- `.brain/pendientes.md`

## Fuente
- D-038, carta §16

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-10-31, spec 079)
