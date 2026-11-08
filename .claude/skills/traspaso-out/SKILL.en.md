---
name: traspaso-out
description: Use when Darwin types traspaso-out (salgo or entro) or says he is switching AI (Claude, Gemini, Codex).
---

# Handoff-out: from one AI to another

Gemini and Codex do not run hooks: there is no summary on opening and no notice on closing. This skill replaces them by hand, with two modes (`/traspaso-out salgo`, in Codex `$traspaso-out salgo`). To move to a new chat with the same AI, use `traspaso-in`.

## How (steps)
**salgo** (I leave this AI):
1. Look at the real state: `git status --short`, `git log --oneline -5` and the result of the latest tests. Do not rely on the chat's memory alone.
2. Write **two** files (they overwrite) with the templates of `biblioteca/PLANTILLA_TRASPASO.md` (spec 026): `.brain/traspaso.md` **short** (~1500 characters) and `.brain/traspaso-completo.md` with the full history, filling in **AI writing it**, **AI continuing** (if Darwin said which) and **time**. Put the uncommitted files that git reported under "Not pushed" and in section 4. If a milestone is left without a lesson, note it first with `/leccion`.
3. If a task was finished, close it first (line in `decisions.log`).
4. **Save and push the memory (spec 022):** if `.brain/guardianes/guardar_traspaso.py` exists, run it. It commits only the memory (handoff, archived handoffs, log, pending list and specs) and pushes it to GitHub. This is the only push without Darwin's express order. If it does not exist, tell him the handoff stays unsaved in Git.
5. Tell Darwin what the guardian reports: what did not make it into the commit and, if it was not pushed, why. If it lists other unpushed commits, ask him, and only with his yes rerun it with `--subir-todo`. A Git failure does not stop the handoff.
6. Tell him in one sentence that he can now open the other AI and type `traspaso-out entro`. Start nothing else.

**entro** (I arrive from another AI, new chat):
1. If `.brain/guardianes/arranque.py` exists: run it with `--manual`; it shows the state and the handoff and archives it by itself.
2. If it does not exist (medium-level project): read `.brain/traspaso.md`, tell it and then **move** (do not delete) the file to `.brain/archive/traspasos/YYYY-MM-DD-HHMMSS.md`.
3. (The full history stays in `.brain/archive/traspasos/*-completo.md`; `/memoria-traspaso` brings it.) Tell Darwin in 4-5 plain bullets: what the other AI left, what is missing, what is uncommitted, what NOT to do. Close with a single question: where to go next. Start nothing on your own.

## Error it prevents (real case)
- Switching AI in the middle of a task and the new one not knowing what was done or what was discarded: it repeats or overwrites work.

## Where it lives in the repo
- `.claude/skills/traspaso-out`, `biblioteca/PLANTILLA_TRASPASO.md`, `guardianes/arranque.py`, `guardianes/guardar_traspaso.py`, specs 010, 011 and 022.

## Source
- Specs 010, 011 and 022, spec 078

## Used
- Times: 0 · Last: — (renamed from cambio-de-ia on 2026-11-03)
