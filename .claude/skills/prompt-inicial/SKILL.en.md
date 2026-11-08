---
name: prompt-inicial
description: Use when Darwin wants to start a project or task with a complete prompt, or types /prompt-inicial.
---

# Initial prompt (optional template)

It only serves to write an errand. To see the state there is `/resumen`; to see a list, `/pendiente`.

## How (steps)
1. Ask the type: new project, fix a bug, add a feature, review or research; and the mode: quick (goal, how I will know it is right, what I do NOT want) or complete.
2. Fields, all optional (empty ones are omitted): goal and for whom; how I will know it is right; what I do NOT want; existing material; how to work (SDD or quick, auto or step by step); deadlines; costs (AI or zero cost); language and tone; what he must test; open questions.
3. Warn without blocking: the goal or the "done" criterion is missing; a bug without an example; a new project without limits; if the request is very big, suggest splitting it into chats or specs.
4. Assemble the prompt only with what was filled in, show it and wait for his approval before acting. If there are no open questions, add "ask me before inventing".
5. If he asks for the Gemini/Codex version, write the blank template as `.md` (`.brain/biblioteca/PLANTILLA_PROMPT_INICIAL.md`).

## Error it prevents (real case)
- Starting to program with a half-written errand: without a "done" criterion or limits, the AI invents and the work has to be redone.

## Where it lives in the repo
- Spec 084 and D-075; separated from `/resumen` and `/pendiente` in spec 006.

## Source
- D-075, spec 084 (item 81)

## Used
- Times: 1 · Last: 2026-11-01 (created on 2026-11-01)
