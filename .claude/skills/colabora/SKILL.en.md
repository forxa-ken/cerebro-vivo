---
name: colabora
description: Use when Darwin types /colabora (si, no or estado) or asks to turn on or off the collaborative mode of the project (several AIs with different roles).
---

# /colabora — collaborative mode, yes or no

Turns on, turns off or shows the `modo_colaborativo` setting in `.brain/guardianes/guardianes.json` (spec 042). It is off by default: with a single AI (Claude with `CLAUDE.md`, Codex with `AGENTS.md` or Gemini with `GEMINI.md`) there is nothing to share out and everything works as usual. When on, it **is remembered between chats**: the startup says "COLLABORATIVE MODE ON" and every AI reads `.brain/colaboracion.md` first.

## How (steps)
1. Read the word after the command: `si` (on), `no` (off) or `estado` (just look). With no word, `estado`.
2. Run `python .brain/guardianes/colabora.py WORD`.
3. Tell Darwin in one line how it stands, with the text the script prints.
   - With `si`: it creates `.brain/colaboracion.md` from the template `biblioteca/IAS_COLABORATIVAS.md` if it does not exist and adds **a single line** pointing to it in the indexes that exist (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`), except those in `indices_ajenos` (those are not touched: a warning is shown).
   - With `no`: it removes those lines. `colaboracion.md` is kept.
4. With `si`, help Darwin **adapt the role matrix** in `.brain/colaboracion.md` (which AI does what and which files are its own), asking what you do not know; do not invent roles.
5. It opens no new chat (unlike `/fabrica`, there is no director).

## Mistake it prevents (real case)
- Two AIs in the same project without written roles: one edited the other's files and the rules were repeated, sometimes differently, in three indexes.

## Where it lives in the repo
- `.claude/skills/colabora`, `.brain/guardianes/colabora.py`, `arranque.py`, `guardianes.json` (`modo_colaborativo`, `indices_ajenos`), `biblioteca/IAS_COLABORATIVAS.md`, spec 042.

## Source
- Spec 042 (Darwin's request, 2026-11-12)

## Used
- Real use: `python .brain/guardianes/medir.py --skills` (not recorded here) (created 2026-11-12)
