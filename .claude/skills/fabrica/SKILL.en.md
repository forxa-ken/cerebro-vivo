---
name: fabrica
description: Use when Darwin types /fabrica (si, no or estado) or asks to turn on or off the factory mode of the project (the AI as director who does not code).
---

# /fabrica — factory mode, yes or no

Turns on, turns off or shows the `modo_fabrica` setting in `.brain/guardianes/guardianes.json`. It is off by default (normal mode). When on, it **is remembered between chats**: the startup of every new chat says "FACTORY MODE ON" and the AI acts as director (skill `directora-de-fabrica`) without Darwin repeating it.

## How (steps)
1. Read the word after the command: `si` (turn on), `no` (turn off) or `estado` (just look). With no word, `estado`.
2. Run `python .brain/guardianes/fabrica.py modo WORD`.
3. Tell Darwin in one line how it stands, using the text the script prints. With `si`, load the skill `directora-de-fabrica` and follow it; with `no`, work like a normal chat. The charter is written by Darwin, not the AI.

## Error it prevents (real case)
- The project had `.brain/fabrica/` but every new chat worked like a normal chat: nobody told it that it was a factory and it had to be repeated in every chat.

## Where it lives in the repo
- `.claude/skills/fabrica`, `.brain/guardianes/fabrica.py` (`modo`), `arranque.py`, `guardianes.json` (`modo_fabrica`), spec 040.

## Source
- Spec 040 (Darwin's request, 2026-11-11)

## Used
- Real use: `python .brain/guardianes/medir.py --skills` (not logged here) (created on 2026-11-11)
