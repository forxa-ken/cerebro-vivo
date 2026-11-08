---
name: spec-antes-de-programar
description: Use when a change touches more than 2 files or quotas, payments, licenses, deployment or the database.
---

# Spec before programming

## How (steps)
1. Create `.brain/specs/NNN-name.md` from `_template.md`: goal, scope, out of scope, plan, verification.
2. Wait for Darwin's approval before programming.
3. Everything else goes by Fast-Track: direct change, tests green and a line in `decisions.log`.
4. On closing: a D-NNN card if there was an important decision.

## Error it prevents (real case)
- Programming without a plan in big changes produces messy code and repeated work.

## Where it lives in the repo
- `.brain/specs/`, `.brain/specs/_template.md`

## Source
- D-001

## Used
- Real use: `python .brain/guardianes/medir.py --skills` (not logged here) (created on 2026-10-31, spec 079)
