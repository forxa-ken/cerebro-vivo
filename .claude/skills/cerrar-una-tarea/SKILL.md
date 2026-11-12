---
name: cerrar-una-tarea
description: Use when finishing any task in the project.
---

# Cerrar una tarea

**Se cierra por bloque** (spec 033): un tema completo con pruebas en verde, no cada cambio pequeño. El guardián no pide la línea hasta 15 archivos editados sin cerrar (`cierre_bloque_max_ediciones`). **Siempre** se cierra antes de abrir un chat nuevo, escribir un traspaso o cambiar de IA.

**Prueba de retomar** (spec 041): antes del tope de 15, si otra IA que solo viera la petición y el `git diff` no podría retomar el trabajo (hay una decisión, una causa descubierta, un paso pendiente o algo que Darwin debe probar que solo está en la conversación), se cierra ya con su línea en `decisions.log`.

## Cómo (pasos)
1. Tests en verde: `venv\Scripts\python.exe -m unittest discover tests`.
2. Línea en `.brain/decisions.log` (o `cerrar.py`). Primero la línea y luego el commit; si la línea llega después, entra en el siguiente commit.
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
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-10-31, spec 079)
