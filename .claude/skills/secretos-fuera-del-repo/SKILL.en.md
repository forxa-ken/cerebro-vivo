---
name: secretos-fuera-del-repo
description: Use when adding a key, token, webhook URL or personal data file, or before any git push.
---

# Secrets outside the repo

## How (steps)
1. Keys live in `.env` / hosting variables, never in the code or in Git.
2. User data and webhooks go in `.gitignore`.
3. The pre-commit hook (`secretos.py --instalar-hook`) blocks a secret of real format; do not use `--no-verify` without a reason.
4. If a key leaks: change it first, clean the history afterwards (see `architecture/secretos.md`).

## Error it prevents (real case)
- The commits of spec 008 carried a real Discord webhook URL.

## Where it lives in the repo
- `.gitignore`, `.brain/guardianes/secretos.py`, `.brain/architecture/secretos.md`

## Source
- D-020, D-046

## Used
- Real use: `python .brain/guardianes/medir.py --skills` (not logged here) (created on 2026-10-31, spec 079)
