---
name: diapositivas
description: Use when Darwin types /diapositivas (with or without a topic or a document name) or asks to explain something as slides or a presentation.
---

# /diapositivas — presentations for humans, with one command

Turns a topic or a document into slides that open in the browser, with nothing to install (spec 045). Darwin does not write Markdown or commands.

## How (steps)
1. Read what comes after the command:
   - **Nothing:** topic `resumen` (state of the project).
   - **`resumen`, `version`, `traspaso`, `auditoria`:** `version` = the latest entry of `CAMBIOS.md`; `traspaso` = `.brain/traspaso.md` (or the latest archived one); `auditoria` = the latest auditor report.
   - **`doc NAME`** (or a name that looks like a file): document mode, see step 4.
   - **Free text:** the topic Darwin asks for.
2. Read **only** the files of the topic; nothing that does not come from them. Write `.brain/diapositivas/YYYY-MM-DD-topic.md` with the template `biblioteca/PLANTILLA_DIAPOSITIVAS.en.md` (or `.md` if the project is in Spanish). A `---` line separates each slide. Rules: **at most 12 slides and 6 bullets per slide**, short plain sentences (the plain-language explaining skill), what is not tested as "untested", and on the last slide the files everything comes from.
3. Run `python .brain/guardianes/diapositivas.py .brain/diapositivas/YYYY-MM-DD-topic.md`. It opens in the browser by itself. Tell Darwin in one line where it is and how to move (arrow keys, `o` to see all, Ctrl+P for PDF). Start nothing else.
4. **Document mode** (`doc NAME`): find it with `python .brain/guardianes/diapositivas.py --buscar NAME`. If one file comes out, go on. If several (exit 3), **ask Darwin which one**, never pick. If none (exit 2), say so and do not invent. Then:
   - The 12-slide cap **does not apply**. The first slide is an **index** with all the sections (`##`) of the document.
   - **Every section of the original gets at least one slide**, with its title text copied as is as `## title`.
   - Past 20 slides the script splits it by itself into linked parts.
   - The last slide says which document was presented and which sections were heavily condensed, with their path.
   - Before calling it done, check: `python .brain/guardianes/diapositivas.py --comprobar ORIGINAL.md SLIDES.md`. If a section is missing, add it and repeat.
5. **Diagrams (spec 046, phase 1):** if a slide is clearer with a drawing, write a ```` ```mermaid ```` block with `flowchart LR` (or `TD`: boxes and arrows, e.g. the life cycle of a task) or `sequenceDiagram` (who talks to whom, in order). At most 15 boxes, or 7 participants and 24 messages. The drawing **comes from the files you read**, it is not invented. If the script warns that a diagram could not be drawn, fix it or leave it as text; the other types (classes, states, pie, etc.) do not exist yet.
6. The `.html` files can be rebuilt and are not pushed to Git (the script leaves a local `.gitignore`). The `.md` files are.

## Error it avoids (real case)
- Squeezing a long document into a few slides without saying so and silently dropping whole sections. The index, the "one slide per section" rule and `--comprobar` make it visible. The check looks that every section appears, not that the summary is faithful: Darwin reviews that.

## Where it is in the repo
- `.brain/guardianes/diapositivas.py`, `.brain/biblioteca/PLANTILLA_DIAPOSITIVAS.md`, `tests/test_diapositivas.py`, spec 045.

## Source
- Spec 045 (idea from Karpathy's "LLM Wiki" gist, Darwin's request, 2026-11-12)

## Used
- Real use: `python .brain/guardianes/medir.py --skills` (not noted here) (created on 2026-11-12)
