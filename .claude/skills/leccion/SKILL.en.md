---
name: leccion
description: Use when Darwin types /leccion, or the hitos guardian blocks closing a task because a problem was solved or a delicate file changed.
---

# /leccion — note the lesson on the spot

The lesson is noted when the milestone happens, not at the end or "if we remember". The `hitos.py` guardian (Stop hook) does not let the task close until there is a new lesson or a "no lesson".

## How (steps)
1. Decide the topic (`video`, `metodo`…; one that already exists in `.brain/lecciones/indice.md` if it fits).
2. With a lesson: `python .brain/guardianes/lecciones.py --tema TOPIC "problem | cause | rule"`. One sentence per part; the rule must be applicable next time without rereading the chat. If it was already written, it says so and does not duplicate it.
3. Without a lesson (cosmetic change, error with nothing to learn): `python .brain/guardianes/lecciones.py ninguna "reason"`. The reason is mandatory.
4. Tell Darwin in one line what was noted. Before repeating work on a topic, read `.brain/lecciones/TOPIC.md`.

## Error it prevents (real case)
- In Modelo 2 each video solved problems and the lesson was lost because it depended on remembering (spec 026).

## Where it lives in the repo
- `.brain/guardianes/lecciones.py`, `hitos.py`, `.brain/lecciones/`, spec 026.

## Source
- Spec 026

## Used
- Times: 0 · Last: — (created on 2026-11-07)
