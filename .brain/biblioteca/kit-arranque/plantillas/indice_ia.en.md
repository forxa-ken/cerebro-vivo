# {{NOMBRE}} — Entry index for {{IA}}

This file (`{{ARCHIVO}}`) is the index that **{{IA}}** reads. Same operating content as the project's other entry indexes ({{OTROS}}): if one changes, the others change too. It is an index, not a manual.

---

## Persistent memory (Brain `.brain/`)
{{BLOQUE_IA}}
{{MAPA}}
* **Lessons:** when a milestone is solved (error resolved, delicate file, big change) note the lesson on the spot with `/leccion`; the `hitos.py` guardian does not let the task close without it. Read `.brain/lecciones/` before repeating that work.
* **Short chats:** when the session gets long, write the handoff and open the new chat yourself (`{{NOMBRE}} #N`), unless `/chat-nuevo no` turned it off. **{{DUENO}} gives permanent authorization to open that new chat automatically** (tools `start_session` and `detach_session`), without asking permission each time. Speak to them in plain language.

## Essential rules
* Reply language: **{{IDIOMA}}**, technical and concise tone.
* **Strict scope:** touch only what concerns the requested change; no unrequested refactors.
* **Test command after every change:** `{{PRUEBAS}}`
* Anything irreversible (pushing, deleting, spending, touching real data) is asked first. What is untested is stated as untested.

## Methodology (two lanes)
1. **SDD** — more than 2 files or sensitive areas (payments, permissions, user data, deployment): spec in `.brain/specs/NNN-name.md` from `_template.md` and **wait for {{DUENO}}'s approval** before coding.
2. **Fast-Track** — everything else: apply, tests green and one line in `.brain/decisions.log`.
