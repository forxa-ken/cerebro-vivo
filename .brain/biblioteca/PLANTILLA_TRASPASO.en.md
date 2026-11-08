# Handoff templates (specs 078 and 026)

The AI writes **two** files (overwriting them) **before** proposing or creating a new chat (skill `traspaso-in`) or when switching AI (skill `traspaso-out`). They do not go to GitHub (except the memory commit of `traspaso-out salgo`).

- **`.brain/traspaso.md` (short):** the only thing the new chat loads by itself. At most ~1500 characters (the guardian warns past `traspaso_corto_max`). "DO NOT do" and "not pushed" never leave this one.
- **`.brain/traspaso-completo.md` (full):** the whole history. It is not loaded by itself; startup only warns that it exists. On entry it is archived in `.brain/archive/traspasos/YYYY-MM-DD-HHMMSS-completo.md` and the `/memoria-traspaso` skill brings it back. At most ~6000 characters.

## Short template (`traspaso.md`)
```markdown
# Handoff from chat #N to #N+1 (YYYY-MM-DD)

- **AI writing it:** Claude | Gemini | Codex
- **AI continuing:** (if known)

## What Darwin last asked
- "…" (literal words)

## Awaiting his answer
- …

## Next step
- …

## DO NOT do
- …

## Not pushed to GitHub
- Local files and commits (or "nothing")

Full detail: `/memoria-traspaso`
```

## Full template (`traspaso-completo.md`)
```markdown
# Full handoff from chat #N to #N+1 (YYYY-MM-DD)

- **AI writing it:** Claude | Gemini | Codex
- **AI continuing:** (if known)
- **Time:** YYYY-MM-DD HH:MM

## 1. What Darwin last asked (literal words)
- "…"

## 2. Decisions
- Taken: …
- Open (awaiting Darwin's answer): …

## 3. State of each item in progress
- Item X: done / half done (what is missing) / untested

## 4. Not pushed to GitHub
- Local files and commits

## 5. What Darwin must test
- Concrete steps

## 6. DO NOT do (discarded)
- …

## 7. Lessons noted in this chat
- Topic and rule of each (or "none")
```
