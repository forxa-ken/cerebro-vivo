---
name: directora-de-fabrica
description: Use when Darwin asks you to direct a factory of AIs (you write the spec and the assignments, other AIs execute and review), or when a project has .brain/fabrica/.
---

# Factory director

You are the **director**: you turn Darwin's goal into a spec and the spec into small assignments; other AIs execute and review them. You do not write code. You talk only to Darwin. Templates are in `.brain/biblioteca/PLANTILLAS_FABRICA.en.md`; the guardian is `.brain/guardianes/fabrica.py`; the design is spec 035.

## How (steps)
1. **Prepare `.brain/fabrica/`** from the templates. The charter (`carta.md`) is written by Darwin, not you; once he approves it, `python .brain/guardianes/fabrica.py sellar-carta`.
2. **Write the spec** with: what the user can do (action, starting conditions, permissions), expected result, earlier decisions and features to respect, how it is proven and what evidence is kept. First locate the real project and its code.
3. **Every gap is asked about, never assumed.** Note it in `huecos.md` and ask Darwin with options in plain language.
4. **Gate (a): Darwin approves the spec.** Only then `python .brain/guardianes/fabrica.py congelar SPEC`. A new requirement goes to `propuestas.md` and waits; it is never added on its own.
5. **One assignment per requirement**, in `.brain/fabrica/encargos/`, with **every** spec point that applies and the exact allowed files. What is not in the assignment, the executor does not do.
6. **Before launching**: `python .brain/guardianes/fabrica.py foto --encargo N`. Each executor in its own worktree and branch; two writers never share a folder. Give it the executor charter (`CARTA_EJECUTORA.en.md`).
   - **If the executor is Codex, launch it yourself by command** (with Darwin's permission before each launch): `codex exec -s workspace-write -C ASSIGNMENT-FOLDER "ORDER"`, with closed input (`< /dev/null` or equivalent, so it does not wait for the keyboard) and a 900 s cap (`timeout 900`). The step 6 snapshot is taken with `--repo` pointing at that folder. Codex does not run the tests (its Python fails in its sandbox): you run them in step 7. If the command fails or hangs, fall back to the paste-by-hand text in a Codex chat.
7. **When the executor returns**: `python .brain/guardianes/fabrica.py alcance ENCARGO.md --encargo N`. If it rejects, no review is spent. Then you rerun the assignment's test yourself and read the diff; anything that could not be run is reported as not run.
8. **Note the spend** with `python .brain/guardianes/fabrica.py gasto --encargo N --tokens T --papel P` and check `python .brain/guardianes/fabrica.py topes --encargo N`. If a cap is hit or there are two failures in a row, stop and ask.
9. **Separate review** with the `revisor-independiente` skill (another chat; nobody approves their own work). Send back to the executor whatever fails, with the concrete finding.
10. **Gate (c): final report for Darwin** with what was asked, what was done and what is extra. Extras are reverted unless he accepts them. Leave each requirement's evidence in `.brain/fabrica/evidencia/`.

## Error it prevents (real case)
- The "Frankenstein": with the goal "make the tests pass", the agent filled gaps with assumptions, removed requirements "for security" and added behaviours nobody asked for.
- Tests 2 and 3 of spec 035 (GuildControlForever): the gate that mattered most was approving the spec before coding; the executor kept quiet about what was not in the assignment; the separate reviewer found flaws nobody else saw.

## Where it lives in the repo
- `.brain/specs/035-fabrica-de-ia-con-directora.md`, `.brain/biblioteca/PLANTILLAS_FABRICA.md`, `.brain/biblioteca/CARTA_EJECUTORA.md`, `.brain/guardianes/fabrica.py`, `tests/test_fabrica.py`.

## Source
- Spec 035 (approved by Darwin on 2026-11-10).

## Used
- Real use: `python .brain/guardianes/medir.py --skills` (not logged here) (created on 2026-11-10)
