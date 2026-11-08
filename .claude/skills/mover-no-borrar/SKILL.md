---
name: mover-no-borrar
description: Use when pruning, archiving or replacing information in the brain.
---

# Mover no borrar

## Cómo (pasos)
1. Mover a `.brain/archive/` (o a una subcarpeta) en vez de borrar.
2. Dejar un índice para no abrir el archivo completo.
3. Una decisión que cambia no se borra: se marca `reemplazada por D-NNN`.
4. La poda de specs cerradas la hace el guardián 6 (`poda_activa`).

## Error que evita (caso real)
- Borrar historia impide entender por qué algo se decidió; abrirla entera gasta tokens.

## Dónde está en el repo
- `.brain/archive/`, `.brain/guardianes/poda.py`

## Fuente
- spec 048, D-007, D-043

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-10-31, spec 079)
