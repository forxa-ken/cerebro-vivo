---
name: cerrar-una-tarea
description: Use when finishing any task in the project.
---

# Close a task

## How (steps)
1. Tests green: `venv\Scripts\python.exe -m unittest discover tests`.
2. A line in `.brain/decisions.log` (or `cerrar.py`). The line first and then the commit; if the line arrives later, it goes into the next commit.
3. A D-NNN card if there was an important decision; `FUNCIONALIDADES.md` if a feature changes.
   - After creating the card: `venv\Scripts\python.exe .brain\guardianes\cerrar.py --indices` adds its row to the index (do not write it by hand).
   - If Darwin tested an item: `cerrar.py --hecho No. --titulo "..." --detalle "..." --ref "..." [--conservar] [--simular]` moves it from pending to done with its row (spec 083).
4. If the method changes: the meta-harness letter and the three mirror indexes.
5. Tell Darwin what he must test; do not push to GitHub without his confirmation.

## Error it prevents (real case)
- Without a log, Antigravity and later chats lose the context.

## Where it lives in the repo
- `CLAUDE.md` §1, `.brain/guardianes/cerrar.py`

## Source
- D-040, CLAUDE.md

## Used
- Times: 0 · Last: — (created on 2026-10-31, spec 079)
