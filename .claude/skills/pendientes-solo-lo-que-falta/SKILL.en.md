---
name: pendientes-solo-lo-que-falta
description: Use when Darwin confirms he tested a task or when pendientes.md changes.
---

# The pending list holds only what is missing

## How (steps)
1. `pendientes.md` keeps only what is missing, one line per item, fixed numbering. An item does not say whether it is pushed or not: the startup summary reports that, and a note would go stale.
2. When Darwin confirms the test, IN THAT REPLY: detail to `archive/hechos.md`, a row in `archive/hechos-indice.md`, remove it from pending.
3. 8 KB cap watched by the guardian.
4. If the test fails, it goes back to "To program" with a note.

## Error it prevents (real case)
- `pendientes.md` reached 20 KB (~6,000 tokens at every startup).

## Where it lives in the repo
- `.brain/pendientes.md`, `.brain/archive/`

## Source
- D-038

## Used
- Times: 0 · Last: — (created on 2026-10-31, spec 079)
