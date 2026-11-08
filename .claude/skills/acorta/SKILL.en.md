---
name: acorta
description: Use when Darwin types /acorta, says "sí, acorta", or an AI index (CLAUDE.md, GEMINI.md, AGENTS.md) is over its size cap after adopting or reviewing.
---

# /acorta — bring the indexes down to the cap

Brings `CLAUDE.md`, `GEMINI.md` and `AGENTS.md` down to the `tope_claude_md_bytes` cap (5 KB in `guardianes.json`) by replacing heavy blocks with a link. Nothing is lost: the text is already in `.brain/` or is copied there first.

## How (steps)
1. Measure: `python .brain/guardianes/revisar_indices.py --json`. See each index's size and its heavy sections.
2. For each heavy section, check that its text is **already** in `.brain/` (e.g. `referencias.md` after `/adopta`, or `.brain/archive/adoptado/`). If it is not, copy it as is to `.brain/referencias.md` (or `.brain/architecture/`) **before** touching the index.
3. **Show Darwin**, in plain language and before writing: a table "section (KB) → link where it ends up" and the size each index will have. Wait for his yes.
4. With the yes: replace each section with one line holding its link. Keep the three indexes in sync. Whatever does not fit is left alone and reported.
5. Measure again. If it is still over the cap, say so and propose what else to move; do not force it.
6. Tests green and a line in `decisions.log`.

## Error it prevents (real case)
- Leaving a 49-52 KB `CLAUDE.md` after adopting (ten times the cap) because nobody shortened it; or shortening it by deleting text that was not copied elsewhere.

## Where it lives in the repo
- `.brain/guardianes/revisar_indices.py`, spec 017

## Source
- spec 017 (Darwin's request, 2026-11-04)

## Used
- Real use: `python .brain/guardianes/medir.py --skills` (not logged here) (created on 2026-11-04)
