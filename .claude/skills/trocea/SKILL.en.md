---
name: trocea
description: Use when Darwin types /trocea, or the arranque warns that a .brain/ file (referencias.md, architecture/…) is over its size cap.
---

# /trocea — split a fat memory file by topics

Splits a `.brain/` file that goes over `tope_archivo_memoria_bytes` (8 KB) into small files **named after their topic** plus an index. Nothing is lost or summarized: it is cut along the headings it already has.

## How (steps)
1. List the fat ones: `python .brain/guardianes/archivos_gordos.py`.
2. For each one, read it and propose cuts along its headings (`##`): one file per topic in `.brain/architecture/` with a clear name (`loot.md`, `roster.md`), never `part-2.md`. Cross-cutting material (commands, environment, file map) stays in `referencias.md`. A topic that is still fat is divided into named subtopics (`loot-reparto.md`).
3. **Show Darwin**, in plain language and before writing: a table "section (KB) → new file" and the size that will remain. Wait for his yes.
4. With the yes: save the full copy of the original in `.brain/archive/troceado/YYYY-MM-DD-NAME.md`; copy each section **as is** to its file; create/update `.brain/architecture/indice.md` (one line per file) and leave in the original only the cross-cutting material and a line pointing to the index. Link the index from CLAUDE.md.
5. Check that no text was lost: the content of the pieces together matches the copy (same lines). Run `archivos_gordos.py` again: nothing over the cap, or say what is still big.
6. Tests green and a line in `decisions.log`.

## Error it prevents (real case)
- After adopting an old project, `referencias.md` ended up at 47 KB: shortening CLAUDE.md only moved the problem and the AI kept opening a huge file to touch one module.

## Where it lives in the repo
- `.brain/guardianes/archivos_gordos.py`, spec 018

## Source
- spec 018 (Darwin's request, 2026-11-04)

## Used
- Times: 0 · Last: — (created on 2026-11-04)
