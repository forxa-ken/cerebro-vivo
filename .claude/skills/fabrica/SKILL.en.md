---
name: fabrica
description: Use when Darwin types /fabrica (si, no or estado) or asks to turn on or off the factory mode of the project (the AI as director who does not code).
---

# /fabrica — factory mode, yes or no

Turns on, turns off or shows the `modo_fabrica` setting in `.brain/guardianes/guardianes.json`. It is off by default (normal mode). When on, it **is remembered between chats**: the startup of every new chat says "FACTORY MODE ON" and the AI acts as director (skill `directora-de-fabrica`) without Darwin repeating it.

## How (steps)
1. Read the word after the command: `si` (turn on), `no` (turn off) or `estado` (just look). With no word, `estado`.
2. Run `python .brain/guardianes/fabrica.py modo WORD`.
3. Tell Darwin in one line how it stands, using the text the script prints. With `no`, work like a normal chat. The charter is written by Darwin, not the AI.
4. **With `si`, the director's chat opens by itself** (one director per project, in a clean chat; this chat does not become the director). Only if the mode was off before: if it was already on, do not open another. Steps, without asking permission (Darwin authorised it permanently):
   - Write a short `.brain/traspaso.md` (template `biblioteca/PLANTILLA_TRASPASO.en.md`) with what Darwin wants from the factory, which assignments or ideas exist, and "DO NOT: code". The director will read it.
   - Load `start_session` with ToolSearch (`select:mcp__ccd_session__start_session`, alone in its message) and open the chat with context `fresh`, `initiation: "user_asked"`, `model: "claude-opus-5-5"` (Opus; another only if the charter says so), `effort: "medium"`, `title: "directora #N"` and `name: "directora-N"`, where N is the number of directors the project has had (keep the count in `.brain/fabrica/directora_n.txt`: read it, add 1 and save it; if it does not exist, N = 1), and the task "you are the factory director: detach from the chat that opened you (`get_session` with `self`; if not `detached`, `detach_session` with `self`), read `.brain/traspaso.md`, load the skill `directora-de-fabrica` and tell Darwin in 4-5 bullets where to start. Do not code".
   - **Right away** `detach_session` with the id it returns, so it does not hang from this chat. Check with `get_session` (`session_id` the one it returns) that it ended up on Opus with medium effort: the app ignores a model higher than the opening chat's, so if this chat is not Opus it may inherit its own. If it does not match, fix it with `set_session_model` and `set_session_effort`, or tell Darwin. Tell Darwin the new chat's name.
   - Without those tools (Codex, Gemini) or if the app refuses after trying: say so clearly and give the sentence to open it by hand. Never say it is refused without having tried.

## Automatic mode (spec 050)
- `/fabrica automatico si|no|estado` → `python .brain/guardianes/fabrica.py automatico WORD`. It only works with factory mode on; `fabrica.py arrancar` blocks an assignment from starting if the criterion is missing or you are on `main`; `estado` says what is missing (sealed charter, "expected" criterion in `.brain/fabrica/esperado.md`, a working branch that is not `main`). Setting `fabrica_automatica` (off by default). `/fabrica no` or `modo normal` also turn it off.
- Turning it on opens no new chat: the only change is the startup notice. The later phases (spec reviewer, real-use test) are switched on by their own specs.

## Error it prevents (real case)
- The project had `.brain/fabrica/` but every new chat worked like a normal chat: nobody told it that it was a factory and it had to be repeated in every chat.

## Where it lives in the repo
- `.claude/skills/fabrica`, `.brain/guardianes/fabrica.py` (`modo`), `arranque.py`, `guardianes.json` (`modo_fabrica`), spec 040.

## Source
- Spec 040 (Darwin's request, 2026-11-11)

## Used
- Real use: `python .brain/guardianes/medir.py --skills` (not logged here) (created on 2026-11-11)
