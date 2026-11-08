---
name: actualizar
description: Use when Darwin types /actualizar or the arranque says there is a new arnés version available for this project.
---

# /actualizar — bring the new harness version into this project

Does the whole process without Darwin typing commands. The updater keeps a backup, does not overwrite what was edited by hand and does not touch data (pending list, specs, decisions, log).

## How (steps)
1. Simulate: `python .brain/guardianes/actualizar_arnes.py --simular`. Tell Darwin in 3-4 plain bullets: from which version to which, what is new (read the harness repo's `CAMBIOS.md`, only the new versions), how many files change, what is retired and whether any file was edited by hand. If it says "Nothing is copied" (light or medium level), tell Darwin and stop.
2. Ask for his yes. If there are hand-edited files (`!`), say which ones and that they will NOT be overwritten unless he asks; retired files that were not modified go to the backup.
3. With the yes: `python .brain/guardianes/actualizar_arnes.py`. It adds only the missing settings keys, records `arnes_repo` and completes the skill cards in `.brain/experiencia/indice.md`. If the updater that ran was older than 1.19.0, run it again so it applies the retired files.
4. If the method's tests come out red, do NOT go on: say which ones and the backup path (`.brain/copias_arnes/`). A failure of a test that already failed before (the project's own guardians) is explained, not hidden.
5. Restart Claude Code if `.claude/settings.json` changed. Close with the log line.

## Error it prevents (real case)
- Updating by hand with long commands (one project ended up 9 versions behind) and forgetting the steps afterwards: the skill cards and the new keys, which left tests red.

## Where it lives in the repo
- `.brain/guardianes/actualizar_arnes.py` (`version_disponible`, `completar_configuracion`, `completar_fichas_skills`), specs 019 and 021

## Source
- spec 019 (Darwin's request, 2026-11-04)

## Used
- Times: 0 · Last: — (created on 2026-11-04)
