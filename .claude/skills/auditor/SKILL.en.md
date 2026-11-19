---
name: auditor
description: Use when Darwin types /auditor (general, cierre, externo or estado), asks for an audit of quality, resource use and security, or the closing warns "lanza el auditor".
---

# /auditor — the one who tries to break the work before it is called good

The auditor works in **any project**, no factory needed. It looks for flaws in **quality** (does it meet the spec?), **consumption** (CPU, memory, disk, network) and **security**, and it **only warns**: it does not change code or block the closing (spec 044). It does not replace the factory's reviewer, who checks each assignment; in a factory the auditor joins at the **spec closing**.

## How (steps)
1. **Pick the mode** with the word after the command: `general` (reviews the project or the given folder), `cierre` (what changed in the current task) or `spec` (factory spec closing: the spec, the assignments, the director's verdict and the final integration). With no word, `estado`.
2. **See who audits:** `python .brain/guardianes/auditor.py quien MODE`. By default the **external** one (Codex) audits in `general`, `cierre` and `spec`. The **internal** one (read-only subagent, Sonnet 5.5 at medium, different from whoever wrote the work) is **optional**: it joins with `auditor_interno` set to `siempre`, or just this once with `quien MODE --interno`, and always when the external one does not run (`auditor_externo` is `no`, or `general-y-spec` in a routine closing). In `cierre` pass the changed files (`quien cierre FILE…`): if they touch something sensitive (`revision_sensibles`) it answers `externo?` = the external one is suggested; decide it with Darwin.
3. **Launch the internal one** as a read-only subagent with an adversarial instruction: "prove it fails", cross-check the code against the spec, **run** tests and checks (do not just read) and give every finding with file and line. For the criteria, reuse `revisor-independiente` (quality), `revisor-de-consumo` (consumption) and `seguridad-en-sistemas-reales` (security); do not copy them.
4. **Launch the external one** if it applies: `python .brain/guardianes/auditor.py codex` prints the command (`codex exec` read-only; on Windows it carries `windows.sandbox="unelevated"` or Codex cannot run `python`). Give it the same task on standard input. If Codex is not installed or fails, **say so clearly** and carry on with the internal one.
5. **One report** with `biblioteca/PLANTILLA_INFORME_REVISION.en.md`: verdict, findings per block (quality, consumption, security), what was not checked and, if there were two auditors, where they **agree** and where they **disagree**.
6. **Tell Darwin in plain words** what matters and let him decide: the report is his. Whatever gets fixed is fixed afterwards, in another task.
7. **Settings:** `/auditor cierre si|no|estado` (the closing warning; on by default). **Since 1.61.4 (spec 092) it only warns when a spec or a factory assignment is declared finished**, not on every response with uncommitted changes: when a spec with code is finished, run `python .brain/guardianes/auditor.py terminada NNN` (in factory mode a green `fabrica.py cerrar-encargo` marks it by itself); the warning stays until, once the auditor has run, you run `python .brain/guardianes/auditor.py auditada`. If only documents or memory were touched, `terminada` marks nothing and `/auditor externo general-y-spec|siempre|no|estado` and `/auditor interno opcional|siempre|estado`, with `python .brain/guardianes/auditor.py cierre|externo|interno WORD`. Models and effort: `auditor_modelo`, `auditor_modelo_externo`, `auditor_esfuerzo` in `guardianes.json`.

## Error it prevents (real case)
- Planted-flaws test (2026-11-12, spec 044): toy code with 11 subtle flaws passed its 9 tests in green. The three auditors found 10 or 11; only Codex reproduced the folio race and only Sonnet and Opus saw the swallowed errors. None covers everything alone: that is why two go on delicate work.

## Where it lives in the repo
- `.claude/skills/auditor`, `.brain/guardianes/auditor.py` (settings and the Codex command), `cierre.py` (warning), `biblioteca/PLANTILLA_INFORME_REVISION.md`, spec 044 and the reports of the two rounds in `.brain/archive/`.

## Source
- Spec 044 (Darwin's request, 2026-11-12)

## Used
- Real use: `python .brain/guardianes/medir.py --skills` (not noted here) (created 2026-11-12)
