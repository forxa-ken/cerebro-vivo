---
name: buscar-en-la-memoria
description: Use when you are about to investigate, decide or explain something the project may already have written down (a lesson, decision, spec or saved answer), or Darwin asks "¿ya lo teníamos apuntado?" or "busca en la memoria".
---

# Search the memory before investigating

The project memory (`.brain/`) holds lessons, decisions, specs and answers. Reading whole folders burns tokens; this skill asks first and opens only what matters (spec 049).

## How (steps)
1. Before investigating or asking something again, run: `python .brain/guardianes/buscar.py WORDS` (accents do not matter; 2 to 4 keywords, no filler words).
2. Read the list: each file shows its title and 1 or 2 lines with the word (`path:line`). **Open only the first 1 or 2** that fit, and only the part that matters.
3. Refine if needed: `--solo lecciones` (or `decisions`, `specs`, `respuestas`), `--max 5`, `--archivo` to also search the history (`archive/`, left out by default).
4. If nothing useful comes up, then investigate. If it was already there, use it and tell Darwin where it comes from.
5. If what you find out is useful next time: `/guardar-respuesta` or `/leccion`.

## Mistake it avoids (real case)
- Investigating again something a lesson or a saved answer already solved, or opening whole `.brain/` folders to find a single sentence.

## Where it is in the repo
- `.brain/guardianes/buscar.py`, spec 049 (pending item 46, idea from the «LLM Wiki» gist)

## Source
- spec 049

## Used
- Real use: `python .brain/guardianes/medir.py --skills` (not noted here) (created on 2026-11-14, spec 049)
