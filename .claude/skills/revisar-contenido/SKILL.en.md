---
name: revisar-contenido
description: Use when Darwin says "revisa el contenido" or "revisa la memoria", or the arranque warns of findings in the content of .brain/ (orphan pages, outdated statements, possible contradictions).
---

# Review the content of `.brain/` (search and refute with another AI)

Memory rots without anyone noticing: a page nobody links, a sentence that is no longer true, two documents that contradict each other. The guardian proposes; this skill verifies; **an independent pass tries to refute**; Darwin decides. Nothing is fixed on its own.

## How (steps)
1. Report: `python .brain/guardianes/revisar_contenido.py --json`. Three types: `huerfana` (nobody links it), `desfasada` (a path that does not exist, a «current version» different from `VERSION`, a false count) and `contradiccion` (the same limit with different values). Each finding carries a stable `clave`.
2. **Pass 1, search (you).** Read each finding against the real project: is the page historical on purpose, or linked by an index under another name? Is the path created when the method is used? Do the two limits talk about different things? Result: *confirmed*, *dismissed* (with a reason) or *doubtful*. Also look by hand for what the script cannot see: «pending» in one document and «done» in another, or a sentence that no longer holds.
3. **Pass 2, refute (another AI, not you).** Whoever finds a finding tends to agree with themselves, so **do not refute yourself**. Launch a fresh subagent (same model, without your context) and give it **only the two sentences and the project path**, with the question «do they contradict each other, or is it no longer true, really? Try to prove it is NOT» (lean on the `revisor-independiente` skill). Only those it cannot refute survive. If you disagree, the finding becomes *doubtful*, never certain.
4. **Optional, only for the doubtful ones:** if the project has another AI configured (Gemini, Codex; see `colaboracion.md`), ask it for a second opinion in the same way.
5. Note the dismissed ones so they do not come back: `python .brain/guardianes/revisar_contenido.py --descartar CLAVE --motivo "why"`.
6. **Show Darwin**, in plain language and before touching anything: *certain* (survive the refutation), *doubtful* («do not touch unless you look at it yourself») and how many were dismissed and why. Wait for his approval.
7. Apply only what is approved: link the orphan page from its index, fix the sentence, or **move** the old content to `.brain/archive/` (never delete; see the `mover-no-borrar` skill).
8. Close: `python .brain/guardianes/revisar_contenido.py --marcar-revision`, run the report again, tests green and a line in `decisions.log`.

## Mistake it avoids (real case)
- Calling two limits a contradiction when they were about different files, or deleting an «orphan» page that was historical on purpose; and having the AI that proposes a finding also be the one that confirms it.

## Where it is in the repo
- `.brain/guardianes/revisar_contenido.py`, `.brain/guardianes/revision_contenido.json` (dismissals and the date of the last review), spec 048

## Source
- spec 048 (pending item 44, idea from Karpathy's «LLM Wiki» gist)

## Used
- Real use: `python .brain/guardianes/medir.py --skills` (not noted here) (created on 2026-11-13, spec 048)
