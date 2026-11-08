---
name: guardian-avisa-o-bloquea
description: Use when creating an automatic check (guardian) for the Cerebro Vivo method.
---

# A guardian warns or blocks

## How (steps)
1. By default it only warns: one line in the startup summary and detail under `--ver`.
2. It blocks only what is irreversible (a secret pushed to GitHub cannot be "un-pushed").
3. If the guardian fails, it stays silent: it must never bring the work down.
4. Settings in `guardianes.json`; anything existing that breaks the rule is noted as an exception with a reason.
5. Add a test and a row in `herramientas.md`.

## Error it prevents (real case)
- Rules that depend on the AI's discipline are silently forgotten.

## Where it lives in the repo
- `.brain/guardianes/`, `guardianes.json`

## Source
- D-039, D-044, D-046, letter principle 8

## Used
- Real use: `python .brain/guardianes/medir.py --skills` (not logged here) (created on 2026-10-31, spec 079)
