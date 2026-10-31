---
name: cerrar-una-tarea
description: Use when finishing any task in the project.
---

# Cerrar una tarea

## Cómo (pasos)
1. Tests en verde: `venv\Scripts\python.exe -m unittest discover tests`.
2. Línea en `.brain/decisions.log` (o `cerrar.py`).
3. Ficha D-NNN si hubo decisión importante; `FUNCIONALIDADES.md` si cambia una funcionalidad.
   - Tras crear la ficha: `venv\Scripts\python.exe .brain\guardianes\cerrar.py --indices` añade su fila al índice (no la escribas a mano).
   - Si Darwin probó un punto: `cerrar.py --hecho Nº --titulo "..." --detalle "..." --ref "..." [--conservar] [--simular]` lo pasa de pendientes a hechos con su fila (spec 083).
4. Si cambia el método: carta del meta-arnés y los tres índices espejo.
5. Decir a Darwin qué debe probar; no subir a GitHub sin su confirmación.

## Error que evita (caso real)
- Sin registro, Antigravity y los chats siguientes pierden el contexto.

## Dónde está en el repo
- `CLAUDE.md` §1, `.brain/guardianes/cerrar.py`

## Fuente
- D-040, CLAUDE.md

## Usada
- Veces: 0 · Última: — (creada el 2026-10-31, spec 079)
