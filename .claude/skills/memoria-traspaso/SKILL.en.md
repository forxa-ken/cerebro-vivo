---
name: memoria-traspaso
description: Use when Darwin types /memoria-traspaso, or you need the full detail of what the previous chat did and the short traspaso is not enough.
---

# /memoria-traspaso — bring back the full history of the previous chat

The handoff the new chat loads is short. The full detail is kept apart and consulted only when needed.

## How (steps)
1. Look in `.brain/archive/traspasos/` for the `*-completo.md` files. With `/memoria-traspaso` and no number, the most recent; with a number N, the N-th counting backwards (1 = the last, 2 = the one before…). If there is a `.brain/traspaso-completo.md` not yet archived, it is the most recent.
2. Read it whole and tell Darwin in plain language (short bullets): what was done, decisions, what was left half done, what was discarded.
3. If there is none, say so clearly; do not invent it. Modify or move nothing.

## Error it prevents (real case)
- Loading the whole handoff in every new chat spends context even though the detail is almost never needed (spec 026).

## Where it lives in the repo
- `.brain/archive/traspasos/`, `biblioteca/PLANTILLA_TRASPASO.md`, `guardianes/arranque.py`, spec 026.

## Source
- Spec 026

## Used
- Times: 0 · Last: — (created on 2026-11-07)
