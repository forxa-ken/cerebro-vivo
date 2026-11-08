---
name: revisar-indices-de-ia
description: Use when Darwin says "revisa los índices", the arranque warns that an AI index (CLAUDE.md, GEMINI.md, AGENTS.md) is near its cap, has broken references or is overdue for review.
---

# Review the AI indexes (double pass)

Cleans `CLAUDE.md`, `GEMINI.md` and `AGENTS.md` without losing information and without false positives. The guardian only proposes; this skill verifies with **two passes**; Darwin approves; what is retired is **moved**, never deleted.

## How (steps)
1. Report: `python .brain/guardianes/revisar_indices.py --json`. Five kinds of finding: broken reference, drift between indexes, heavy section, old date, duplicate in `.brain/`. Each carries a stable `clave` (key).
2. **Pass 1, search.** Verify each finding against the real project: does the file exist under another name or path (`posible_nuevo_sitio`)? Is it created when running? Is it cited as an example or as history? Does another current document mention it? Is the date historical on purpose? Result: *confirmed*, *discarded* (with a reason) or *doubtful*.
3. **Pass 2, refute.** On what is confirmed and doubtful, an independent reading tries to prove the finding false. Preferably with a subagent that is given **only the finding and the project path**, without pass 1's reasoning (if there are no subagents, reread from scratch before looking at the earlier conclusion). Only those that cannot be refuted survive. If the two passes disagree, it becomes *doubtful*, never certain.
4. Note the discarded ones so they do not come back: `python .brain/guardianes/revisar_indices.py --descartar KEY --motivo "why"`.
5. **Show Darwin**, in plain language and before writing anything: a table "section → what we propose" with three groups: *certain* (survive both passes), *doubtful* ("do not touch unless you look at it yourself") and one line with how many were discarded and why. Wait for his approval.
6. Apply only what is approved: the live reference that is documentation → its card (`.brain/architecture/`, `referencias.md`); the outdated → `.brain/archive/indices/YYYY-MM-DD-NAME.md` with a line in `.brain/archive/indices/indice.md`; what can be fixed, fixed. Keep the three indexes in sync.
7. Close: `python .brain/guardianes/revisar_indices.py --marcar-revision`, run the report again (it must be clean or hold only the accepted doubtful ones), tests green and a line in `decisions.log`.

## Error it prevents (real case)
- Deleting from an index a "broken path" that was an example, a file created when running, or a deliberate historical one; or letting a `CLAUDE.md` grow to 49 KB (ten times its cap) with architecture sections nobody checks against the code.

## Where it lives in the repo
- `.brain/guardianes/revisar_indices.py`, `.brain/guardianes/revision_indices.json` (discards and date of last review), spec 016

## Source
- spec 016

## Used
- Times: 0 · Last: — (created on 2026-11-04, spec 016)
