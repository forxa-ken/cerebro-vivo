---
name: resumen
description: Use when Darwin types /resumen or asks where the project stands.
---

# Resumen del estado

## Cómo (pasos)
1. Solo leer, no escribir nada. Leer `.brain/pendientes.md` y la última línea de `.brain/decisions.log`; si existe `.brain/traspaso.md`, mirar su sección 3.
2. Contar en 4-5 viñetas llanas, sin jerga: versión o estado, qué falta (con sus números), qué está sin subir o sin commitear, qué debe probar Darwin.
3. Terminar con una sola pregunta: por dónde seguir. No empezar nada.

## Error que evita (caso real)
- Mezclar el resumen con empezar a trabajar o con escribir un traspaso: gasta tokens y hace lo que Darwin no pidió.

## Dónde está en el repo
- `.claude/skills/resumen`, spec 006.

## Fuente
- Spec 006

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-11-01)
