---
name: mover-no-borrar
description: Use when pruning, archiving or replacing information in the brain.
---

# Move, do not delete

## How (steps)
1. Move to `.brain/archive/` (or a subfolder) instead of deleting.
2. Leave an index so the whole file need not be opened.
3. A decision that changes is not deleted: it is marked `reemplazada por D-NNN` (replaced by D-NNN).
4. Pruning of closed specs is done by guardian 6 (`poda_activa`).

## Error it prevents (real case)
- Deleting history makes it impossible to understand why something was decided; opening it whole spends tokens.

## Where it lives in the repo
- `.brain/archive/`, `.brain/guardianes/poda.py`

## Source
- spec 048, D-007, D-043

## Used
- Real use: `python .brain/guardianes/medir.py --skills` (not logged here) (created on 2026-10-31, spec 079)
