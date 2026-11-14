---
name: prueba-de-uso-real
description: Use when a factory in automatic mode (spec 050) has an assignment built and it must be tested in real use, with saved evidence, before it can be called delivered; or when you must test a product that another AI built.
---

# Real-use test

Programmed is not finished. This skill says **how to really test** what another AI built and what evidence to leave. **You** do it, and you did not build it (another model, or at least another chat with these instructions). If you built it, stop: tell the director so a different AI tests it.

## What you receive
- The **"expected" criterion** (`.brain/fabrica/esperado.md`), written **before** building. It is your yardstick: you test what was asked, not something easier.
- The assignment and the product (the working branch). Not the conversation of whoever built it.

## How (steps)
First, by product:
- **Command-line tools and guardians:** really run them with **good** and **bad** cases; compare the output with the criterion and check that the bad is **rejected** (exit code and message).
- **Documents, skills and generated pages:** generate and open them (the page, in the built-in browser); check that they load, that there are no external requests or console errors, and that the requested path works.
- **Applications with a screen:** open the application and walk through a user's path with browser or computer control, if available.
- **What an AI cannot judge** ("looks good", "is understandable"): mark it **not tested**. It goes to "Waiting for your test (Darwin)". Never declare it done.

## Where the evidence goes
1. Save commands, outputs and screenshots in `.brain/fabrica/evidencia/` (for example `REQ-1/output-good.txt`).
2. Write `.brain/fabrica/evidencia/REQ-1.md` with the `PLANTILLAS_FABRICA` template (section 10): who built, who tested, the criterion tested **quoted in «…» exactly as in `esperado.md`**, good and bad cases run, evidence files, result (green / red / not tested) and the **Not tested** list, which is never left empty without an explanation.
3. Check: `python .brain/guardianes/fabrica.py entregar REQ-1`. It exits 0 only if the evidence is complete: a different AI tested, the quoted criterion exists, the files exist and are not empty, and the result is green. With red, or not tested, it exits 1.

## Against the trick test
- A test **without saved evidence counts as not done.**
- If you cannot quote the criterion, you are testing something else: stop and ask.
- A green result with an empty "Not tested" list and no explanation is suspicious: justify why nothing is left.

## Error it prevents
- The AI approves itself, or accepts something because the code tests passed although nobody used it for real.

## Where it is in the repo
- `.claude/skills/prueba-de-uso-real`, `.brain/guardianes/fabrica.py` (`entregar`), `PLANTILLAS_FABRICA` (section 10), spec 050 (phase 4).

## Source
- Spec 050 (Darwin's request, 2026-11-14)

## Used
- Real use: `python .brain/guardianes/medir.py --skills` (not noted here) (created 2026-11-14)
