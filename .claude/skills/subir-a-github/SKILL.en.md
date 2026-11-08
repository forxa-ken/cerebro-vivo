---
name: subir-a-github
description: Use when Darwin orders to push or upload the project to GitHub, or says "sube".
---

# Push to GitHub

Only on Darwin's order, except for the memory commit of `traspaso-out salgo`, which carries its own exception.

## How (steps)
1. Check for secrets: `python .brain/guardianes/secretos.py`. If it finds anything, stop and tell Darwin.
2. Put the handoffs (`.brain/archive/traspasos/` and `.brain/traspaso.md`) and `.brain/decisions.log` in one commit, without asking, so the context reaches another computer.
3. Look at whatever else is still uncommitted (`git status --short`), ask Darwin what to do with it and run the tests, which must be green.
4. Show the commits that will go up (`git log --oneline @{u}..HEAD`) and push with `git push`. Never force. If GitHub rejects it, say so and ask before merging.
5. A line in `.brain/decisions.log` with what was pushed, with its local commit.

## Error it prevents (real case)
- Opening the project on another computer without the latest handoffs: they were left uncommitted and part of the context was lost.

## Where it lives in the repo
- `.claude/skills/subir-a-github`, `guardianes/secretos.py`, `guardianes/guardar_traspaso.py`, spec 022.

## Source
- Spec 022

## Used
- Times: 0 · Last: — (created on 2026-11-07, spec 022)
