---
name: sincronizar
description: Use when Darwin types /sincronizar or says "sincroniza", "baja lo de GitHub" or "ponme al día" (typically on arriving at another computer).
---

# /sincronizar — bring this computer up to date with GitHub and ready to work

It only pulls; it never pushes, merges or overwrites anything.

## How (steps)
1. Run `python .brain/guardianes/sincronizar.py` (with `--simular` if Darwin wants to see first what it would do). It does `git fetch` + `git pull --ff-only` and then shows the startup summary (state, handover, harness version).
2. Tell Darwin in 3-4 plain bullets: whether there was anything new and how much, what is uncommitted or unpushed, and what the handover says (what awaits his answer and the next step).
3. If the script exits with an error (diverged branch, clash with local changes, no internet), say so plainly and do **not** fix it on your own: no `merge`, `rebase`, `stash`, `reset` or `push` without Darwin's order.
4. If it says there is a newer harness version, offer `/actualizar`; do not launch it by yourself.
5. First time on a computer without the project: there is nothing to sync; run `git clone https://github.com/forxa-ken/cerebro-vivo.git`, enter the folder and say `/sincronizar` (or `traspaso-in entro`).
6. One single question at the end: where to continue. Do not start anything.

## Error it prevents (real case)
- Darwin switched computers mid-work and had no single command to catch up: he had to remember `git pull`, check the state and read the handover separately.

## Where it lives in the repo
- `.claude/skills/sincronizar`, `.brain/guardianes/sincronizar.py`, `textos.py` (`sync_*` keys), spec 093, `tests/test_sincronizar.py`.

## Source
- Spec 093 (Darwin's request, 2026-11-20)

## Used
- Real use: `python .brain/guardianes/medir.py --skills` (not recorded here) (created 2026-11-20)
