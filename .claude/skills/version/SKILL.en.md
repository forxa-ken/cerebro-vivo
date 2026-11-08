---
name: version
description: Use when Darwin types /version or asks which version of the arnés (Cerebro Vivo) this project has.
---

# /version — which harness version this project has

Read-only; it writes and updates nothing.

## How (steps)
1. Installed version: the `version` field of `.brain/arnes_instalado.json`. If the file does not exist, say the project predates version tracking (before 1.0.0) or does not have the harness.
2. Available version: `arnes_repo` in `.brain/guardianes/guardianes.json` and the `VERSION` file in that folder. If `arnes_repo` is missing, is a web address or the folder does not exist, say it cannot be compared and why.
3. Tell Darwin in 2-3 plain bullets:
   - Installed version and available version.
   - If a newer one exists: the titles of the new versions in the harness repo's `CAMBIOS.md`, one line each.
   - How to update: `/actualizar`. If the installed version is older than 1.17.0, that command does not exist yet in the project; the first time it is updated by hand, in the terminal and inside the project, with `python .brain/guardianes/actualizar_arnes.py --simular` and then without `--simular`. From cerebro-vivo, `python actualizar.py "PROJECT_PATH" --simular` and then without `--simular` also works.
4. Do not update unless Darwin asks.

## Error it prevents (real case)
- In Modelo 2 (harness 1.12.0) `/actualizar` did not exist and there was no quick way to know which version the project had.

## Where it lives in the repo
- `.claude/skills/version`, `.brain/arnes_instalado.json`, `actualizar_arnes.py` (`version_disponible`), spec 023.

## Source
- Spec 023 (Darwin's request, 2026-11-07)

## Used
- Real use: `python .brain/guardianes/medir.py --skills` (not logged here) (created on 2026-11-07)
