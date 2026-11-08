---
name: adoptar-indice-existente
description: Use when pending item says to adapt what the project already had (CLAUDE.md, GEMINI.md or AGENTS.md) to the .brain memory, or Darwin says "adopta el índice existente".
---

# Adopt the index the project already had

The kit installer overwrites nothing: it added a memory block at the end of the index (between `<!-- cerebro-vivo:inicio -->` and `<!-- cerebro-vivo:fin -->`) and kept a full copy of the original in `.brain/archive/adoptado/NAME.original.md`. This skill distributes that content into its place **without losing anything**.

## How (steps)
1. Read the copy in `.brain/archive/adoptado/` (the original, not the already merged index). If there are several (CLAUDE, GEMINI, AGENTS), read all of them and join what is repeated.
2. Classify each block of the original and propose where it goes:
   - goal, description, audience → `.brain/architecture/objetivo.md`
   - rules, prohibitions, style → `.brain/constitution.md`
   - decisions with their why → `.brain/decisions/` (and a line in `decisions/indice.md`)
   - file map, commands, environment → `.brain/referencias.md`
   - open tasks → `.brain/pendientes.md` (only what is missing)
3. **Show Darwin the distribution** (short table: "this → here") in plain language and wait for his approval. Write nothing before.
4. With the approval: copy each block to its file **as is**, without summarizing or rewriting what does not fit; anything doubtful goes to `referencias.md`. Never discard.
5. Only if Darwin approves it separately (shortcut `/acorta`): shorten the original index to an index (what is already distributed is replaced by a link to the file where it ended up). The copy in `.brain/archive/adoptado/` always stays (move, do not delete).
6. Remove the task from `.brain/pendientes.md` and close with the line in `decisions.log`.

## Rules
- Contradictions between the original and the method: do not resolve them; list them to Darwin.
- If the copy in `adoptado/` is missing, use `NAME.antes-de-cerebro-vivo` (the installer's backup).

## Error it prevents (real case)
- Installing the kit over a project with its own `CLAUDE.md` and losing (or ignoring) what was already written there: the project's rules, decisions and map.

## Where it lives in the repo
- `.brain/biblioteca/kit-arranque/instalar.py` (`fusionar_indice`, `fusionar_ajustes`), spec 015

## Source
- spec 015

## Used
- Real use: `python .brain/guardianes/medir.py --skills` (not logged here) (created on 2026-11-04, spec 015)
