---
name: hermanos
description: Use when the project has sibling projects (same origin, different variant), the arranque says "N commits de X sin portar", or Darwin asks to set up or adopt a "portar" file.
---

# Sibling projects — what is left to port, computed automatically

A "sibling" project shares its origin with this one (another variant or edition). What is done in one and missing in the other is computed with git instead of depending on anyone's memory (spec 043). **Read-only**: the guardian does not `fetch` or change anything; if the sibling is not accessible, it stays silent.

## How (steps)
1. **Set up a sibling** (Darwin asks; he gives the path): in `.brain/guardianes/guardianes.json`, `proyectos_hermanos`: `[{"nombre": "...", "ruta": "C:/path/to/sibling", "rama": "main", "archivo_portar": ".brain/portar-NAME.md"}]`. Several siblings are allowed.
2. **Create the port file** from `.brain/biblioteca/PLANTILLA_PORTAR.en.md` (sections `## Last ported`, `## Pending`, `## Done`). Put in "Last ported" a sibling commit that is already up to date.
3. **Adopt a port file that already existed in another format:** keep it, add the three headings and move each commit already ported or discarded into "Done" with its hash (7 characters or more). Do not invent hashes: take them from the sibling's `git log`.
4. **Read the notice:** the startup says "N commits from X not yet ported". See the list with `python .brain/guardianes/hermanos.py`. Port (or decide "not applicable") and write the hash in "Done" with what changes, what to adapt and what not to port. The guardian does no `cherry-pick`: a person or the project's AI decides.
5. **Shared findings:** before investigating, look at the sibling's `.brain/hallazgos-compartidos.md`; after investigating something useful to several, note it in your own (template `PLANTILLA_HALLAZGOS.en.md`).

## Mistake it prevents (real case)
- Two variants of one project: the "port" file had said "Pending: (nothing)" for weeks while the other kept moving, and what was discovered got researched twice.

## Where it lives in the repo
- `.claude/skills/hermanos`, `.brain/guardianes/hermanos.py`, `arranque.py`, `guardianes.json` (`proyectos_hermanos`), `biblioteca/PLANTILLA_PORTAR.md`, `PLANTILLA_HALLAZGOS.md`, spec 043.

## Source
- Spec 043 (Darwin's request, 2026-11-12)

## Used
- Real use: `python .brain/guardianes/medir.py --skills` (not recorded here) (created 2026-11-12)
