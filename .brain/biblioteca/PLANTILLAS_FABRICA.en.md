# AI factory templates (spec 035, phase 1)

For a project where a **director** (Opus) turns Darwin's goal into a spec, **executors** do small assignments and an independent **reviewer** verifies. These are only templates: they are copied to the project's `.brain/fabrica/` when Darwin decides to set up a factory. They are enforced by the guardian `.brain/guardianes/fabrica.py` (phase 2); from the charter it reads the `key: number` lines.

## 1. Factory charter

File `.brain/fabrica/carta.md`. **Only Darwin writes it**; the director reads it and does not edit it (a guardian will enforce this).

```markdown
# Factory charter: <project>
- Goal: <one sentence, in Darwin's words>
- Forbidden: <what no AI may do: new dependencies, touching X, pushing to GitHub…>
- Cap per assignment: 2 windows of ~200,000 tokens or 400,000 spent; whichever comes first (stop and ask)
- Cap per mission: 10 assignments and 1,000,000 Codex tokens
- General brake: if the weekly Codex budget drops below 50 % free, stop and ask
- Failures: two in a row on one assignment = stop and tell Darwin
- tope_encargo_tokens: 400000
- tope_mision_encargos: 10
- tope_mision_tokens: 1000000
- libre_semanal_minimo: 50
- fallos_seguidos_max: 2
- Director: Opus, medium effort, one per project. Detailed reading of results: Sonnet, medium effort
```

## 2. Roles

File `.brain/fabrica/roles.md`: who does what and who owns each file. Someone else's file is read, not written. Nobody approves their own work.

```markdown
# Factory roles
| Role | Who | May write | May not |
|---|---|---|---|
| Director | Claude Opus (one chat per project) | spec, assignments, gaps, proposals, evidence | write code; edit the charter; talk to anyone but Darwin |
| Executor | Claude or Codex Luna | only the files its assignment lists, in its own worktree and branch; its note in `.brain/notas-chats/` | commit; touch the rest of `.brain/`; add or remove requirements |
| Reviewer | Claude in another chat | its report | change the code it reviews |
| Darwin | person | the charter; approves the three gates | — |
```

## 3. Darwin's three gates

1. **The spec**, before anything is launched. It must have: what the user can do (action, starting conditions, permissions), expected result, which earlier decisions and features must be respected, how it is proven and what evidence is kept.
2. **Each gap** in the spec: it is recorded and asked about; nobody fills it with an assumption.
3. **The final report**: what was asked, what was done and what is extra. Extras are reverted unless Darwin accepts them.

After the spec is approved its fingerprint is stored with `python .brain/guardianes/fabrica.py congelar SPEC`. A new requirement goes to proposals and waits for approval.

## 4. Assignment

File `.brain/fabrica/encargos/NNN-name.md`. Written by the director. **Without an approved requirement, the assignment is rejected.** It must list **every** spec point that applies: what is not listed, the executor does not do.

```markdown
# Assignment NNN: <name>
- Requirement it meets: <R-n of the approved spec> (mandatory)
- Spec points included: <complete list, not a summary>
- Allowed files: <exact paths; a folder ends with />
- Forbidden in this assignment: <dependencies, new accesses, other files>
- Test that accepts it: <concrete command or check>
- Evidence it must leave: <what is noted and where>
- Executor: <Claude / Codex Luna (effort)> · worktree and branch: <name>
```

## 5. Evidence

File `.brain/fabrica/evidencia/REQ-n.md`: one per closed requirement. A check that was not run is written as "not run", never left out.

```markdown
# Evidence for requirement R-n
- Assignment(s): NNN
- What was checked and how: …
- Result: <green / red / not run, with the reason>
- Files touched (by the scope guardian, or by hand if it does not exist yet): …
- Spend: <tokens per role>
- Extras that appeared: <none / list>
```

## 6. Gaps and proposals

Files `.brain/fabrica/huecos.md` and `.brain/fabrica/propuestas.md`. The director writes them from what the executor and the reviewer report.

```markdown
# Gap H-n (open / resolved by Darwin on YYYY-MM-DD)
- Where: <requirement or spec point>
- What is left to decide: …
- Options seen: …
- Darwin's answer: …

# Proposal P-n (waiting / approved / rejected)
- Who proposes it and why: …
- New requirement or change: …
```

## 7. Security without changing what was asked

No AI changes or removes a requirement "for security". If it sees a risk, it records it as a gap or proposal and asks Darwin.

## 8. Risk-based review

The reviewer checks that what was delivered answers the requirement, checks each finding against the real code and ranks them by severity. Trivial things are fixed and noted. Anything that affects a requirement or an earlier decision is escalated to Darwin.
