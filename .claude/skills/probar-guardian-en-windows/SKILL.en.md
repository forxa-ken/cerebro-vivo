---
name: probar-guardian-en-windows
description: Use when testing a guardian, hook or script that prints to the Windows console.
---

# Test a guardian on Windows

## How (steps)
1. Test it in the real Windows console, not just in theory.
2. Force UTF-8 on the output of the harness scripts (a "⚠" brought down the token meter).
3. Before testing, leave the ground clean and check that the test case CAN fail.
4. Test in a new chat when it depends on a startup hook.

## Error it prevents (real case)
- The token meter crashed when printing "⚠"; a guardian test proved nothing because the log was already modified.

## Where it lives in the repo
- `.brain/guardianes/*.py`

## Source
- letter §16 (#39)

## Used
- Real use: `python .brain/guardianes/medir.py --skills` (not logged here) (created on 2026-10-31, spec 079)
