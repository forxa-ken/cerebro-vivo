---
name: guardar-respuesta
description: Use when Darwin types /guardar-respuesta, says "guarda esta respuesta" or "apunta esto", or an answer or comparison in the chat is worth keeping even though no error produced it.
---

# /guardar-respuesta — so a good answer is not lost with the chat

Lessons are only born from a solved problem. A useful explanation or comparison (why something was chosen, what separates two options) was lost when the chat closed. This skill files it in `.brain/respuestas/` with its source (spec 045).

## How (steps)
1. Decide what to save: the answer **summarized** (8 KB cap), without detours, understandable without rereading the chat. If Darwin said "save this one", save that one; do not invent another.
2. A short title and the source (chat and number, document or link it comes from).
3. Run: `python .brain/guardianes/respuestas.py --titulo "TITLE" --fuente "SOURCE" "text"`. With long text or accents: pass it through standard input with `-` (`... --fuente "SOURCE" -`) or write the file with Write and run `--indice`. Do not use a Python heredoc for the text.
4. Tell Darwin in one line what was saved and where. Before asking something again, look at `.brain/respuestas/indice.md`.

## Error it prevents (real case)
- A useful comparison from a chat stayed only in that chat: lessons did not pick it up because it did not come from a failure (idea of pending item 45).

## Where it lives in the repo
- `.brain/guardianes/respuestas.py`, `.brain/respuestas/`, spec 045 of the pending list (idea from the "LLM Wiki" gist).

## Source
- Pending item 45 (idea from the "LLM Wiki" gist, Karpathy, 2026-11-12)

## Used
- Real use: `python .brain/guardianes/medir.py --skills` (not recorded here) (created 2026-11-13)
