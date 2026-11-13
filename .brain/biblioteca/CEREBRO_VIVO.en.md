# The "Cerebro Vivo" method

> A working method for building a software project with an AI (Claude, Gemini or another) **without losing context between chats and while spending few tokens**. It was born in LoboHook (2026) and is written to be copied to other projects.
> Sources consulted: Lee, Yoonho et al., *Meta-Harness* (arXiv:2603.28052, Stanford, 2026); Databricks, *Omnigent* (2026); Nygard, Fowler, Microsoft, Red Hat and AWS on architecture decision records (ADR); GitHub (Microsoft), *Spec Kit* (`github/spec-kit`, August 2025) and *Spec-Driven Development*, origin of the "constitution" (`constitution.md`); Delimarsky, Den, GitHub Blog, 2 Sep 2025; Cusumano, Michael A., *Japan's Software Factories* (1991) and Greenfield and Short, *Software Factories* (2004), on the "software factory". Full list with links in the README. The implementation is our own, centered on collaborative work between AI agents and persistence of context between chats.
> To use it: copy this file into the new project and tell the AI: *"Apply the Cerebro Vivo method from `CEREBRO_VIVO.md`: create the structure and work by its rules."*

> Note: file, folder and command names stay in Spanish on purpose (`pendientes.md`, `guardianes/`, `/actualizar`, `traspaso-in`). Changing them would break existing projects.

---

## 1. The idea in one sentence
The AI **does not remember** what happened in earlier chats. So the project's memory lives in **files**, ordered so that the AI reads little at the start and looks up detail only when it needs it. *The truth is in the code and in these files, not in the conversation.*

## 2. The five principles
1. **Index first, detail after.** At the start a short index is read; detail is opened only if needed.
2. **Each thing in its place.** Rules, pending tasks, finished tasks, decisions and specifications go in different files.
3. **Closing is part of working.** A task is not finished until the memory is updated (log, pending list, index).
4. **What is done leaves the view.** Finished work is archived with an index; the pending list stays short.
5. **The "why" is kept.** A decision without its reason gets argued (and paid for) again every time.

## 3. File structure

```
CLAUDE.md                  ← short index for Claude (≤ 5 KB)
GEMINI.md                  ← same index for another AI (if more than one is used)
.brain/
  README.md                ← map of this folder
  constitution.md          ← non-negotiable rules
  pendientes.md            ← ONLY what is missing (≤ ~8 KB)
  decisions.log            ← one line per finished task: what was done
  decisions/
    indice.md              ← table of important decisions
    D-001-name.md          ← one card per decision, with its why (≤ 15 lines)
  specs/
    _template.md
    001-name.md            ← specification approved before programming
  architecture/
    area.md                ← card per technical area (read only the one that applies)
  archive/
    hechos.md              ← detail of finished and tested tasks
    hechos-indice.md       ← one row per finished task (THIS one is consulted)
    historial-antiguo.md + indice.md   ← for very long old records
  guardianes/              ← the method's automatic checks (section 9)
  biblioteca/              ← material reusable across projects
```

| File | Answers | Read at startup? |
| :--- | :--- | :---: |
| `CLAUDE.md` | How do we work here and where is everything? | Yes |
| `constitution.md` | Which rules cannot be broken? | Yes |
| `pendientes.md` | What is missing? | Yes |
| `architecture/<area>.md` | How does this part work? | Only the task's area |
| `decisions/indice.md` | Was this already decided and why? | If something decided is about to change |
| `specs/` | What was approved to be built? | Only the task's one |
| `decisions.log` | What was done and when? | No (only appended at the end) |
| `archive/hechos-indice.md` | Was X done? When? | Only when consulted |

**Startup reading:** `CLAUDE.md` + `constitution.md` + `pendientes.md` + one `architecture/` card. In LoboHook that is about 35 KB (~10,000 tokens) versus ~150,000 if everything had to be read.

## 4. The two work lanes
| Lane | When | Steps |
| :--- | :--- | :--- |
| **SDD** (specify first) | Touches more than 2 files, or a sensitive area (money, permissions, licenses, database, deployment) | 1) Create a spec from `_template.md`. 2) **Wait for the owner's approval.** 3) Program. 4) Tests. 5) Close. |
| **Small change** | Everything else | 1) Apply the change. 2) Tests green. 3) Close. |

A spec is short: goal, what is in and what is out, files touched, how it is tested, risks. Its value is that **the owner approves before tokens are spent programming the wrong thing**.

**Errand with self-evaluation (v1.4.1):** in a big errand, the spec or the message ends with verifiable success criteria ("1) … 2) … 3) …") and this order: *"Before handing me the result, review it yourself against those criteria, fix what fails and tell me which ones you meet and which you do not. If you cannot check one, say so instead of calling it good."*

## 5. Life cycle of a task (and of an item in `pendientes.md`)

```
Idea ──► [approved spec] ──► To program ──► Implemented
                                                │  tests green
                                                ▼
                                    Waiting for the owner's test
                                       │                 │
                                  test OK           test fails
                                       ▼                 ▼
                                archive/hechos     back to "To program"
                                + index            with a note of what failed
```

- **Implemented ≠ finished.** Until the owner tests it, the task stays in `pendientes.md`, in the "Waiting for your test" section, with **a single line**.
- **Tested = finished.** In the same reply in which the owner confirms, the AI moves it: detail to `hechos.md`, row to `hechos-indice.md`, and deletes the item from `pendientes.md`. It does not wait for the file to "fill up".
- **Numbering is fixed.** Item 16 stays 16 in the file; the gaps are finished tasks. That way the indexes never break.

## 6. Task close (mandatory checklist)
1. Tests green (the project's fixed command).
2. One line in `decisions.log` (date, type, who, what, lane). The type is a fixed word (`arnes`, `leccion`, `decision`, `spec`, `pendiente`, `memoria`, `otro`) set with `cerrar.py --tipo` and used to filter: `grep "| arnes |" .brain/decisions.log`. Old lines do not carry it (spec 048).
   When closing, `cierre.py` also warns about the **knock-on effect** (spec 047): if the chat touched, for example, a spec but not `pendientes.md`, it says which document to check. Warning only; the rules live in `cadenas` of `guardianes.json` (`si`, `salvo`, `avisar` es/en) and are turned off with `cadenas_activas: false`.
3. If there was an important decision: `D-NNN` card + row in `decisions/indice.md`. A decision that changes **is not deleted**: it is marked "replaced by D-NNN".
4. Update `pendientes.md` (and move to `hechos` if the owner already tested).
5. If a feature changed, update the feature map.
6. Summary to the owner in plain language: what is left, what remains to test, what was not verified.
7. Before calling something done, two questions (v1.4.1): is there anything here that is not true or that I have not tested? Is there anything the owner would not say or understand that way?

**Light mode (v1.2.0):** if the task was small (up to 2 files, none sensitive, `.brain/` untouched) and the tests came out green, the `cierre.py` guardian writes the log line itself (`Claude (auto)`) and steps 3-5 are not needed. It is switched off with `modo_ligero_activo` in `guardianes.json`. Reason: in the spec 001 measurement, the full close cost between 17 % and 43 % more tokens on small tasks.

## 7. The AI's conduct rules
- **Strict scope:** touch only what the task asks; no unrequested refactors.
- **Tests always green;** if there is no verified failure, working code is not rewritten.
- **Consult before changing what was decided** (`decisions/indice.md`).
- **Anything irreversible is asked first:** publishing online, deleting, spending money, touching real data.
- **Speak at the owner's level** (here: plain language, no jargon, because they are not a programmer).
- **Warn when the chat gets long** and recommend opening a new one (`Project #N`). A long chat costs more than any file, because every message drags the whole history. In Claude Code desktop, the notice (`longitud.py`) also asks the AI to open the new chat and separate it from the previous one (`detach_session`) so it sits at the same level; in Codex and Gemini there is no such tool and `traspaso-in salgo` is used by hand.
- **Do not invent:** if something could not be tested, say so; do not mark it as done.

## 8. How to start in a new project
Paste this in the first chat:

> Apply the Cerebro Vivo method (`CEREBRO_VIVO.md`). Create `CLAUDE.md`, `.brain/` with `constitution.md`, `pendientes.md`, `decisions.log`, `decisions/`, `specs/`, `architecture/` and `archive/`. My non-negotiable rules are: [write them]. Test command: [command]. Reply in [language] and explain without jargon. Work with two lanes (SDD/Small change) and close every task with the checklist.

**Minimal templates**
- `pendientes.md`: header with the closing rule + sections *To program*, *Waiting for your test*, *Your actions*, *Later*.
- `hechos-indice.md`: table `No. | What | Date | Ref.`.
- `D-NNN` card: *Date · Status · Decision · Why · Consequences · Related* (≤ 15 lines).
- Spec: *Goal · Scope (in / out) · Files · How it is tested · Risks · Owner approval*.

**With the harness repo (`cerebro-vivo`, spec 087):** the method lives in its own repository and each project is installed and updated from it.

| Command | What for |
| :--- | :--- |
| `python .brain/biblioteca/kit-arranque/instalar.py PATH --nombre N --dueno D --nivel completo` | Installs the method in a new project (guardians, skills, kits, manual, tests) and records where it is updated from (`arnes_repo` in `guardianes.json`) |
| `python .brain/guardianes/actualizar_arnes.py --simular` | In a project: shows which harness files would change, writing nothing |
| `python .brain/guardianes/actualizar_arnes.py` | Updates: keeps a copy in `.brain/copias_arnes/`, copies what is new, moves to that copy what the harness retired, **does not overwrite what you edited by hand** (it lists it and the version is recorded with those files under `sin_aplicar`), never touches pending list, specs, decisions or log, adds to `guardianes.json` only the missing keys, copies nothing in a light or medium level project, and runs the method's tests |
| `… actualizar_arnes.py --forzar PATH` | Overwrites a file you do want replaced even though you edited it (with a backup) |
| `… actualizar_arnes.py --forzar-todo` | First time in an old project (no previous record): overwrites **everything** that differs, always with a copy in `.brain/copias_arnes/`. Use it only after seeing the list with `--simular` |
| `… actualizar_arnes.py --repo FOLDER_OR_GIT_URL` | Tells it the harness repo if the project has none recorded |
| `python actualizar.py PROJECT_PATH [--simular]` | The same, launched from the harness repo pointing at a project |
| `python generar_manifiesto.py [--ver]` | Only in the harness repo: regenerates `manifiesto.json` (list of files with their fingerprint) after an improvement, with `VERSION` raised and `CAMBIOS.md` noted; `--ver` says whether it is up to date |

**Language (spec 024):** the setting `"idioma": "es" | "en"` in `guardianes.json` chooses the language of the guardians' notices. A project with `"en"` also receives the English editions of the skills, of this manual and of the templates: in the harness repo they are the files `X.en.md` next to `X.md`, and the updater copies them into the place of `X.md`. File names, folders and commands do not change.

---

## 9. Guardians: the method enforces itself
The method's weak point is that it depends on the AI's discipline. The guardians (folder `.brain/guardianes/`, Python standard library only, settings in `guardianes.json`) turn it into automatic checks:

| Guardian | File | What it does | When it acts |
| :--- | :--- | :--- | :--- |
| **1. Close notice** | `cierre.py` | If project files were touched and the line in `decisions.log` is missing, or `pendientes.md` went over its cap, the AI gets the notice and fixes it. It warns **only once** per reply. | At the end of every reply (Claude Code `Stop` hook, in `.claude/settings.json`) |
| **2. Index test** | `tests/test_cerebro_indices.py` | Each `D-NNN` card has a row and vice versa; links that exist; done index = done; no item both pending and done; size caps. | In the normal test suite (works for any AI) |
| **4. Startup** | `arranque.py` | When a chat opens it injects the real state: pending items and their size, unpushed commits, uncommitted changes, last log line and decision cards to review. | Claude Code `SessionStart` hook |
| **5. Fresh cards** | `arranque.py` + `decisions/_template.md` | A card can declare `Archivos:` and `Revisada:`; if a cited file changed in Git afterwards, it shows "to review". | In the startup summary |
| **Quick close** | `cerrar.py` | Adds the log line with its format: `python .brain/guardianes/cerrar.py "what was done" --chat "Project #N"`. For a one-line change this line is enough. | By hand or by the AI |
| **Loose-ends notice** | `arranque.py` | The "Uncommitted" line looks at the whole project, also `.brain/` and `.claude/`, except what is generated by itself (key `no_avisar_commit`). It makes no commits: it only warns (spec 022). |
| **Handoff Git** | `guardar_traspaso.py` | Launched by `traspaso-out salgo`: commit of only the memory (handoff, archived handoffs, log, pending list and specs) and push to GitHub. It stops on a secret or if there are other unpushed commits that are not memory (`--subir-todo` with the owner's yes). It never forces or merges (spec 022). |
| **Version** | `/version` (skill) | Says which harness version the project has, whether a newer one exists and how to update, also if `/actualizar` does not exist yet (spec 023). Read-only. |
| **New chat by itself** | `/chat-nuevo si`, `no` or `estado` (skill) | When the long-chat notice passes, the AI writes the handoff and opens the new chat itself (by default, yes). `no` leaves it as a notice only, with the sentence to paste (spec 025). |
| **Factory mode** | `/fabrica si`, `no` or `estado` (skill) | Project switch, **remembered between chats**: with `si`, the startup of every chat says "FACTORY MODE ON" and the AI acts as director (does not code, writes spec and assignments). With `no`, normal mode; nothing in `.brain/fabrica/` is deleted. Off by default. |
| **Lessons on the spot** | `/leccion` (skill), `lecciones.py`, `hitos.py` | `hitos.py` (Stop hook) detects a resolved error, a change in delicate files (`lecciones_vigiladas`) or a big modification (`hitos_max_archivos`) and does not let the task close until the lesson is noted in `.brain/lecciones/TOPIC.md` or `lecciones.py ninguna "reason"` (spec 026). |
| **Saved answers** | `/guardar-respuesta` (skill), `respuestas.py` | Files in `.brain/respuestas/` a useful answer or comparison from a chat, with its source, even if no failure produced it (spec 045). There is an index; look at it before asking the same thing again. 8 KB cap per answer. |
| **Content of `.brain/`** | `/revisar-contenido` (skill), `revisar_contenido.py` | Warns, without blocking or changing anything, of `.brain/` pages nobody links, sentences that are no longer true (a path that does not exist, an outdated version or count) and contradictory limits between documents (spec 048). The startup says it in one line; the skill does search and **refute with another AI** (a subagent without your context) before showing it to you. Dismissed items do not come back. Turn it off with `revision_contenido_activa`. |
| **Short + full handoff** | `/memoria-traspaso` (skill) | `.brain/traspaso.md` is short (latest, what awaits, next step, DO NOT do, not pushed); the whole history goes to `.brain/traspaso-completo.md` and is archived with the same stamp (`*-completo.md`). `/memoria-traspaso` brings it when needed (spec 026). |
| **Push to GitHub** | `/subir-a-github` (skill) | List of what is reviewed when the owner orders a push: secrets, handoffs and log in one commit, everything else uncommitted, and tests. |
| **Slides** | `/diapositivas` (skill), `diapositivas.py` | Turns a topic (`resumen`, `version`, `traspaso`, `auditoria`) or a whole document (`doc NAME`) into an `.html` presentation that opens in the browser, with nothing to install; Ctrl+P saves it as PDF. In document mode there is an index and one slide per section, and `--comprobar` warns if one is missing (spec 045). A ```` ```mermaid ```` block (`flowchart` or `sequenceDiagram`) is drawn as an SVG without internet (spec 046, phase 1). |
| **Initial prompt** | `/prompt-inicial` (skill in `.claude/skills/prompt-inicial`) | Helps start a chat with a complete errand: goal, how I will know it is right, what I do NOT want, material, how to work, deadlines, costs, language and what the owner must test; warns about what is missing and waits for approval before acting. It only writes errands: the state comes from `/resumen` and the lists from `/pendiente` (new skills, Claude Code only until the installer covers `.agents/skills/`). | By hand (Darwin) |
| **3. Token meter** | `medir.py` | Reads Claude Code's chat logs and shows per chat the weighted cost, new tokens, output, startup and corrections; `--comparar` pits two projects against each other. Read-only. | By hand: `python .brain/guardianes/medir.py` |

**How they are carried to another project:** copy `.brain/guardianes/` and `tests/test_cerebro_indices.py`, edit `guardianes.json` (caps and patterns to ignore), add the `Stop` (close) and `SessionStart` (startup) hooks in `.claude/settings.json`. The scripts contain nothing from the source project. AIs that do not use Claude Code hooks (e.g. Gemini) are covered by guardian 2.

**What they do not do:** they do not read the messages, do not send data anywhere, do not block commits and do not replace the AI's judgment; they only detect oversights.

## 9 ter. Installing in a project that already has Claude (spec 015)
- The installer **does not overwrite**: to an existing `CLAUDE.md`/`GEMINI.md`/`AGENTS.md` it appends at the end a block between `<!-- cerebro-vivo:inicio -->` and `<!-- cerebro-vivo:fin -->`, and keeps the whole original in `.brain/archive/adoptado/`. Into `.claude/settings.json` it merges the missing hooks and permissions, and leaves `NAME.antes-de-cerebro-vivo` beside it.
- Afterwards, in the first chat: "adopta el índice existente" (adopt the existing index; skill `adoptar-indice-existente`): the AI distributes the old content into the memory and shows it to you before shortening anything. Restart Claude Code so the hooks count.

## 9 quater. Reviewing the AI indexes (spec 016)
- `python .brain/guardianes/revisar_indices.py` produces a report (read-only) on `CLAUDE.md`/`GEMINI.md`/`AGENTS.md`: broken references, drift between them, heavy sections, old dates and paragraphs already present in `.brain/`. Startup warns in one line when it is advisable.
- Say "revisa los índices" (review the indexes; skill `revisar-indices-de-ia`): the AI verifies each finding with a **double pass** (search and refute), shows you what survives and, with your approval, moves what is retired to `.brain/archive/indices/`. Nothing is deleted.

## 9 quinquies. Shorten and split (specs 017 and 018, harness 1.15.0 and 1.16.0)
- Shortcuts of the adoption: `/adopta` (= "adopt the existing index", 1.14.1), `/acorta` (brings CLAUDE/GEMINI/AGENTS down to the `tope_claude_md_bytes` cap of 5 KB by swapping heavy sections for links; first it checks that their text is already in `.brain/`) and `/trocea`. All of them show a table and wait for Darwin's yes before writing.
- `archivos_gordos.py` guardian (read-only): cap `tope_archivo_memoria_bytes` (8 KB) for the reading files of `.brain/` (references, constitution, architecture/, decisions/…). It does not look at archive, biblioteca, specs, pruebas, experiencia, pendientes or the handoff. Startup warns at 80 %. Settings: `archivos_gordos_activo`, `archivos_gordos_aviso_porcentaje`, `archivos_gordos_ignorar`.
- `eventos_chat.py` guardian (`PreToolUse` hook, with chat memory): remembers the libraries installed in the chat (`pip install`, `npm install`…) and, on `git push`, reviews the new ones by itself with `librerias.py` (OSV.dev). Clean: says nothing. Known vulnerability: stops the `git push` and explains it; to go on, the owner says so in the chat and the AI logs `python .brain/guardianes/eventos_chat.py permitir "reason"`. No network: does not block and reminds on the next `git push`. Python only; for npm, cargo or go it warns once. Settings: `eventos_chat_activo`, `eventos_chat_bloquear`, `eventos_chat_sin_red_bloquear`, `eventos_chat_comandos`.
- `/trocea` divides by named topics (never `part-2`), keeps the full copy in `.brain/archive/troceado/`, creates `architecture/indice.md` and checks that the pieces add up to the same as the original. Reason: after adopting an old project, `referencias.md` reached 47 KB and the AI opened it whole to touch one module.
- Recommended order in an old project: install, `/adopta`, `/acorta`, `/trocea`, "revisa los índices".

## 9 bis. Using the harness on Mac (spec 013, untested on a real Mac)
- The guardians are Python with the standard library and work the same. Python 3 is needed (`python3`).
- **Install the kit:** double-click `instalar_kit.command` (if it does not open, in Terminal once: `chmod +x instalar_kit.command`). If tkinter is missing (`brew install python-tk`) or Python is, it says so; the alternative is `python3 .brain/biblioteca/kit-arranque/instalar.py DESTINATION --nombre N --dueno D --idioma I`.
- **Claude Code hooks:** the installer writes `python3` if `python` does not exist on that machine; on Windows it stays `python`. A project already installed on Windows and opened on a Mac: change `python` to `python3` in `.claude/settings.json`.
- **Tests:** `python3 -m unittest discover tests`.

## 10. Objective opinion (from what was lived in LoboHook)

### What works well
- **It saves a lot at the start of every chat.** Estimate by file size (not a real token count): ~10,000 startup tokens versus ~150,000 without indexes, about 90 % less. It is the biggest advantage.
- **It removes the AI's "amnesia".** A task can be resumed after days or with another AI (Claude and Gemini shared the same `.brain/`) without repeating explanations.
- **Specs prevent thrown-away work.** Asking for approval before touching money, permissions or the database costs little and avoids redoing.
- **Decision cards stop repeated arguments** and allow reverting with judgment.
- **It makes the real state visible:** what is programmed, what is tested and what is missing. The owner does not need to read code.
- **It works with a non-technical owner**, because the mandatory communication is in plain language.

### What costs or fails
- **Fixed maintenance cost.** Each small task requires 3-4 file writes at close. For a one-line change that is disproportionate (that is why the small-change lane exists, but it still has to be logged).
- **It depends on the AI keeping the discipline.** Nothing technically forces it; if it forgets to close, the memory goes stale silently. Real test: `pendientes.md` grew to 20 KB (~6,000 tokens) because the rule to move what is done was missing. The method failed exactly where it had no rule.
- **Indexes can drift** (forgotten rows, line numbers that no longer match). That is why fixed item numbers are preferred over line numbers.
- **Memory grows without limit** (in LoboHook ~400 KB after some 45 specs). The index protects startup, but if the index itself gets fat, the saving is lost.
- **Spec approval slows things down** if the owner is unavailable; the work stands still.
- **A mistake in a stored fact spreads:** if a card says something false, the AI will believe it. Cards must be verified against the code when used to decide.
- **It is overkill for small projects** (a script, a one-page website, something that lasts a weekend).

### When to use it and when not
| Use it | Do not use it (or use only half) |
| :--- | :--- |
| A project of weeks or months | A one-day prototype |
| Several chats or several AIs | A single chat that ends today |
| Money, permissions or user data | Experiments with no consequences |
| A non-technical owner who needs to see the state | A programmer who already carries everything in their head |

**Light version** for small projects: just `CLAUDE.md` + `pendientes.md` + `decisions.log`.

### Improvements
1. ✅ **Automated close** with a hook (guardian 1, spec 046).
2. ✅ **Tokens really measured** (guardian 3). First reading in LoboHook (24 chats, 25-28 Oct 2026): startup costs ~69,000 tokens in **all** chats; maximum context runs around 150-470k; the median of long chats passes 250k. Honest conclusion: those ~69k are mostly the tool's system (instructions and tools), which no method can reduce; what the method controls is what is read **on top** of that (~10k instead of ~150k) and, above all, **the length of the chat**. What cannot be measured is the chat that would have existed without the method: the saving against that case remains an estimate.
3. ✅ **Test that validates the indexes** (guardian 2).
4. **Pending:** date each card and review it when the code changes.

### Verdict
A very good method for **medium and long projects with AI**: the continuity and the control over what is read make up for the maintenance. Its weak point was being sustained by discipline; the guardians cover it in part (oversights and drift), but the biggest real expense is long chats, and there only closing and opening a new one in time helps. For something small, use the light version.
