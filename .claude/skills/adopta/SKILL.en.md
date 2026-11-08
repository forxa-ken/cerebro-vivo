---
name: adopta
description: Use when Darwin types /adopta (atajo de adoptar-indice-existente) to split the project's existing CLAUDE.md, GEMINI.md or AGENTS.md into the .brain memory.
---

# /adopta — adopt, shorten and split in one go

One command for a project that already had its CLAUDE.md. It chains three steps and **asks for Darwin's yes on each table** (it never writes without it).

## How (steps)
1. **Distribute:** read the `adoptar-indice-existente` skill and follow its steps up to the approved distribution (the old text copied into `.brain/`; full copy in `.brain/archive/adoptado/`).
2. **Shorten:** read the `acorta` skill and follow it ("section → link" table, Darwin's yes, 5 KB cap). If the indexes already fit, skip this step and say so.
3. **Split:** run `python .brain/guardianes/archivos_gordos.py`. If any `.brain/` file is over the cap, read the `trocea` skill and follow it (table of cuts, Darwin's yes). If none is, skip and say so.
4. **Close:** run `python .brain/guardianes/revisar_indices.py`, tell the result in 3-4 plain bullets (sizes before and after, nothing lost), remove the task from `.brain/pendientes.md`, tests green and a log line. Propose "review the indexes" as the next step, without running it.
5. If Darwin says "no" to a step, stop there and note in `pendientes.md` what is missing (`/acorta` or `/trocea`).

## Error it prevents (real case)
- Having to remember three commands in order (and type them right) to bring an old project into line.

## Where it lives in the repo
- `.claude/skills/adopta`, `adoptar-indice-existente`, `acorta`, `trocea`; spec 020

## Source
- Darwin's request (2026-11-04), specs 015, 017 and 018

## Used
- Times: 0 · Last: — (created on 2026-11-04)
