---
name: pendiente
description: Use when Darwin types /pendiente or asks to see a list of what is missing (to program, to test, his own actions, open specs).
---

# See a pending list

## How (steps)
1. If Darwin typed the name (`/pendiente programar`, `prueba`, `acciones`, `spec`), go straight to that list. If not, ask with a menu of four options: To program, Waiting for your test, Your actions, Open specs.
2. Read only that part: the section of `.brain/pendientes.md`, or the "Estado" header of each spec in `.brain/specs/` that is not done.
3. "To program" and "Open specs": each item on one plain line with its number.
4. "Waiting for your test" and "Your actions" (what Darwin has to do): for each item, a full description with **what it is** (what was done or what is asked and why), **what you have to do** (concrete steps, in order, with the command or the screen) and **what should happen if it goes well** (and what to report if not). If the item cites a spec, read only its verification section to complete the steps.
5. Write nothing and start none of them.

## Error it prevents (real case)
- Opening every file to show a single list: it spends tokens.

## Where it lives in the repo
- `.claude/skills/pendiente`, spec 006.

## Source
- Spec 006

## Used
- Times: 0 · Last: — (created on 2026-11-01)
