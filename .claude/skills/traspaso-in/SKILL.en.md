---
name: traspaso-in
description: Use when Darwin types traspaso-in (salgo or entro), a chat gets long, or he asks to open a new chat with the same AI.
---

# Handoff-in: from one chat to a new chat, with the same AI

The new chat does not see the previous one; it only knows what is in files. Two modes, with the word after the command (`/traspaso-in salgo`, in Codex `$traspaso-in salgo`). **With no word, it is `salgo`** (if this is the old chat and Darwin asks to move to a new one, write the handoff AND open the new chat; never stop at the summary). `entro` only if Darwin types it or the chat has just been born from a handoff.

## How (steps)
**salgo** (closes this chat):
1. Look at the real state: `git status --short`, `git log --oneline -5` and the result of the latest tests. Do not rely on memory alone.
2. Write **two** files (they overwrite; write them **only once**: if they already exist from this same chat and nothing has changed, do not rewrite them, update only what is new) with the templates of `biblioteca/PLANTILLA_TRASPASO.md` (spec 026): `.brain/traspaso.md` **short** (~1500 characters: what Darwin last asked in his literal words, what awaits his answer, next step, DO NOT do, not pushed) and `.brain/traspaso-completo.md` with the full history (decisions, state of each item, what was discarded, lessons of the chat). In "AI writing it" and "AI continuing" put the same AI. Before closing, check that `hitos.py` leaves no milestone without a lesson (`/leccion`).
3. If a task was finished, close it first (line in `decisions.log`). Start nothing else.
4. **Open the new chat yourself** if you have the `start_session` tool (Claude Code desktop): load it with ToolSearch (`select:mcp__ccd_session__start_session`, alone in its message), open it with context `fresh`, `initiation: "user_asked"` and the errand "read `.brain/traspaso.md`, run `traspaso-in entro` and tell it in 4-5 bullets"; **right away** separate it with `detach_session` (id returned by `start_session`) so it sits at the same level and not hanging from this one. Tell Darwin the new chat's name. **Never say the app refuses it without having made the call** (spec 025); if `user_asked` errors, try once with `own_initiative`. If `detach_session` fails, say so clearly: the chat stays nested, no further harm. If the app only lets you propose it (a card remains), there is no need to separate it from here: the new chat will do it when it enters.
5. Without that tool (Codex, Gemini): tell Darwin to open the new chat and type `traspaso-in entro`.

**entro** (new chat):
1. **Separate from the previous chat** if you have the session tools (Claude Code desktop): load them with ToolSearch (`select:mcp__ccd_session_mgmt__get_session,mcp__ccd_session_mgmt__detach_session`) and look at `get_session` with `self`. If it has a `parentSessionId` and `detached` is not `true`, call `detach_session` with `self`. **Always call it, even if you think the app will refuse** (a chat born from a card or a click: do not write it off as impossible without trying; in Guild Control Forever #18 this step was skipped and it stayed hanging from #17). If it fails, say so clearly: the chat stays nested, no further harm. Without those tools (Codex, Gemini), skip this step.
2. If `.brain/guardianes/arranque.py` exists: run it with `--manual` (it shows the state and the handoff and archives it by itself). If it does not exist: read `.brain/traspaso.md` and **move** (do not delete) the file to `.brain/archive/traspasos/YYYY-MM-DD-HHMMSS.md`.
3. Tell Darwin in 4-5 plain bullets: what he last asked, what is missing, what is uncommitted, what NOT to do. The full detail is not loaded: if needed, `/memoria-traspaso`. A single question at the end: where to go next. Start nothing.
4. If there is no handoff, say so clearly; do not invent one.

Do it early: the AI can only summarize what it still has in context. Claude Code shows the handoff by itself on opening; Codex and Gemini need `entro`.

## Error it prevents (real case)
- When opening a new chat the last stretch of conversation was lost.
- Chat #18 was opened from a card and stayed hanging from #17, because nobody separated it after the click.

## Where it lives in the repo
- `.brain/traspaso.md`, `biblioteca/PLANTILLA_TRASPASO.md`, `guardianes/arranque.py`, `longitud.py`, specs 078 and 011.

## Source
- D-051, D-069, specs 078 and 011

## Used
- Real use: `python .brain/guardianes/medir.py --skills` (not logged here) (renamed from traspaso-entre-chats on 2026-11-03)
