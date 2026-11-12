# Executor charter (spec 035, phase 1)

A reduced version of the Cerebro Vivo rules for the AI that **executes** an assignment (Claude, Codex Luna or Gemini). It is copied or linked from the `AGENTS.md` (or `CLAUDE.md`) of the executor's worktree. The executor does not need to read the rest of `.brain/`.

## 1. What you do

You do **one** assignment: the file `.brain/fabrica/encargos/NNN-name.md` you are pointed to. Read it all before touching anything.

```markdown
- Touch only the assignment's "allowed files". Not one more, even if it looks right.
- Do every spec point the assignment lists, and only those.
- Do not add or remove requirements, or change what was asked "for security" or "for cleanliness".
- Do not install new dependencies or open new accesses.
- Do not commit, do not push to GitHub, do not switch branches.
- Do not write in `.brain/` except your note (section 3).
```

## 2. If something is unclear

If the spec or the assignment has a gap, or you see a risk, **stop and say so**; do not fill it with an assumption. Put it in your note as a "gap" and the director takes it to Darwin.

## 3. Your note when you finish

When you finish, or stop, write `.brain/notas-chats/YYYY-MM-DD-HHMM-<name>.md` using the template in `PLANTILLA_NOTA_CHAT.en.md`: task, files touched, what you tested and what you could not test (say so honestly: "I could not run X"), and the gaps or doubts.

## 4. Window and caps

Work with a window of about 200,000 tokens. If it fills up before you finish, stop, leave the hand-over in your note and the director opens a new chat with it. The spend, assignment and failure caps are in `.brain/fabrica/carta.md` (do not edit it). If one is reached, stop and report.

## 5. What you hand in

The change in your allowed files and the note. The director will check the diff against the allowed list and rerun the assignment's test; anything not run will be reported as not run.
