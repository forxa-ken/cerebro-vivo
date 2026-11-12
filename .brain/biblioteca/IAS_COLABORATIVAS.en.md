# Collaboration between AIs (template; spec 042)

This file lives at `.brain/colaboracion.md` only in projects that turn on `/colabora si`. With a single AI it is not used. **Each rule is written once, here**: the indexes (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`) only carry one line pointing to this file.

## 1. Roles (fill in the table; do not invent: ask the owner)

| AI | Entry file | Does | Files it may write | Files it never touches |
| :--- | :--- | :--- | :--- | :--- |
| Claude | `CLAUDE.md` | (e.g. owner of `.brain/` and the code) | (to fill in) | (to fill in) |
| Codex | `AGENTS.md` | (e.g. only what its assignment says) | those of the assignment, in its worktree | `.brain/`, except its note |
| Gemini | `GEMINI.md` | (e.g. texts, translations, documentation) | those of the assignment, in its worktree | `.brain/`, except its note; security and money |

Remove the rows of the AIs that do not take part.

## 2. Do not step on each other
- Two AIs that write **never share a working folder**: each in its own worktree and branch.
- What one edits, the other sees only after the commit.
- Nobody writes to `.brain/decisions.log` except whoever closes the block (the owner of `.brain/`).
- If you doubt which file is yours, stop and ask the owner; do not fill the gap with an assumption.

## 3. Notes between AIs
When you finish or stop, leave a note in `.brain/notas-chats/` (template `PLANTILLA_NOTA_CHAT.md`): what you did, what you touched, what you could not test. The startup shows it to the next AI.

## 4. What is found is shared
Before researching something, look at `.brain/hallazgos-compartidos.md` (if it exists) and at the sister projects'. After researching something useful for several, write it down there.
