# Cerebro Vivo user manual (for Darwin)

A practical guide, no jargon. For the why of each thing see `.brain/biblioteca/CEREBRO_VIVO.en.md`; this manual answers "what do I do and when?". Harness version when written: 1.3.1. (Spanish original: [`MANUAL_DE_USO.md`](MANUAL_DE_USO.md).)

## 1. What it is, in one sentence
A set of folders, automatic notices and habits so that the AI **remembers what was agreed between chats** and does not make you repeat it. The memory lives in each project's `.brain/` folder.

## 2. What we know and what we do not (measured on 2026-11-01)
- **Proven:** when resuming work in a new chat, with the harness what had been agreed was respected 5 out of 5 times; without it, 0 out of 5.
- **Proven:** on small tasks it spends 7 % to 16 % **more**. It does not save there.
- **Proven (a single project, ~80 cards):** having an index did not improve accuracy and came out ~19 % more expensive; with a broken index nobody failed either.
- **Not measured:** that it saves in the long run in a real project. It is a reasonable idea, not a fact.
- Use it where there are **many chats in a row** about the same thing. For a one-off task it does not pay off.

## 3. Starting a new project
1. Double-click `instalar_kit.bat` (a window opens), or in a terminal:
```bash
python .brain/biblioteca/kit-arranque/instalar.py PROJECT_PATH --nombre MyProject --dueno Darwin --nivel completo
```
2. Open a chat in the project folder. Startup will show only a summary of the state.
3. For the first errand, use `/prompt-inicial` in the chat (explained in section 3 bis).

## 3 bis. Starting a chat well: `/prompt-inicial` and the other templates
A complete errand avoids back-and-forth. **`/prompt-inicial`** helps you write it: type `/prompt-inicial` in the chat. It comes included when installing the harness (folder `.claude/skills/prompt-inicial`), nothing else needs installing and it spends no extra AI.

It asks you for **goal, how I will know it is right, what I do NOT want, material, how to work** (spec with approval or quick, step by step), **deadlines, costs, language and what I must test**. It warns you about what is missing and waits for your approval before acting. It only serves to write errands. To know how the project is going type **`/resumen`** (tells the state in a few bullets, writing nothing); to see a list type **`/pendiente`** (lets you choose: to program, waiting for your test, your actions or open specs, or type `/pendiente programar`).

**For Gemini or Codex:** ask Claude for "the Gemini/Codex version" and leave the blank template in `.brain/biblioteca/PLANTILLA_PROMPT_INICIAL.md`.

**`/plantilla` panel:** a form with buttons to write the errand and insert it into the chat. It is a Claude Code plugin (`plantilla-prompt/`) installed once per team, not with the updater; how, in `plantilla-prompt/README.md`.

**Other templates the method uses (they already come with the harness):**
| Template | What for | Where |
|---|---|---|
| Handoff | Moving from one chat to another without losing anything | `.brain/biblioteca/PLANTILLA_TRASPASO.md` |
| Helper-chat note | Leaving what a chat did that received an errand from another | `.brain/biblioteca/PLANTILLA_NOTA_CHAT.md` |
| Spec | A short plan you approve before programming | `.brain/specs/_template.md` |
| Decision card | Why something was decided (`D-NNN`) | `.brain/decisions/_template.md` (created by the kit in each project) |
| Test record | What you have to test and how | `.brain/pruebas/_plantilla.md` |

## 3 ter. A project that already had its CLAUDE.md: `/adopta`, `/acorta`, `/trocea`
**Since 1.18.0 `/adopta` is enough: it does steps 1 to 3 in a row and asks for your yes on each table.** The separate commands (`/acorta`, `/trocea`) still work on their own. For a project started before the method (with a fat CLAUDE.md). The kit is installed (it overwrites nothing: the original is kept whole in `.brain/archive/adoptado/`), Claude Code is restarted in that folder and, in a new chat, **in this order**:

| Step | Type | What it does | You |
|---|---|---|---|
| 1 | `/adopta` | Copies what was in the old CLAUDE.md into its place in `.brain/` (rules, decisions, goal; what does not fit goes to `referencias.md`). It summarizes nothing. | You approve the distribution table |
| 2 | `/acorta` | Replaces the fat sections of CLAUDE.md, GEMINI.md and AGENTS.md with a link, down to the 5 KB cap. | You approve the table before writing |
| 3 | `/trocea` | Splits the `.brain/` files over 8 KB (typically `referencias.md`) into files **by named topic** (`loot.md`, `roster.md`) in `.brain/architecture/`, with an index. The full copy stays in `.brain/archive/troceado/`. | You approve the table of cuts |
| 4 | `revisa los índices` | Checks broken references, drift and repeats with a double pass (skill `revisar-indices-de-ia`). | You approve what survives |

Nothing is deleted: everything is copied or moved to the archive. Startup warns by itself when an index passes 80 % of its cap (4 KB) or a `.brain/` file passes 80 % of its cap (6.5 KB). The new parts (1.14.1 to 1.16.1) are tested with tests and in a real project (Guild Control Forever: CLAUDE.md from 52 KB to 3.3 KB). If a project has an AGENTS.md foreign to the method, do not add it to `indices_entrada` and the tests will not require it.

## 4. A normal working day
- **When opening a chat:** the AI summarizes in 4-5 bullets where it left off. If it does not, ask for it.
- **While you work:** small tasks (up to 2 files) go by the quick lane. Big or delicate changes (payments, database, licenses) ask for a **spec** first: a short paper with goal, what is in, what is out and how it is tested. You approve it before it is programmed.
- **When finishing a task:** the AI notes a line in `.brain/decisions.log`. If it forgets, an automatic notice reminds it. By hand:
```bash
python .brain/guardianes/cerrar.py --chat "Project #N" "what was done"
```
- **When you test something and it works:** tell it in the chat; the AI moves it from `pendientes.md` to `hechos`.
- **Anything irreversible is asked:** pushing to GitHub, deleting, spending. It does not do it without your order.

## 5. Switching chats without losing anything
- A long chat costs more and gets clumsy. When it warns you, or when you have been at it a long time, ask "prepare the handoff and the new chat".
- The AI writes `.brain/traspaso.md` (what you asked, what was decided, what is missing, what NOT to do). The new chat shows it by itself on startup.
- If a helper chat receives an errand from another, it leaves its note in `.brain/notas-chats/`.

### Same AI, new chat: `traspaso-in`
| Moment | What you type | What the AI does |
|---|---|---|
| Before closing a long chat | `/traspaso-in salgo` (in Codex, `$traspaso-in salgo`) | Looks at git and the tests and writes `.brain/traspaso.md` with what you last asked |
| In the new chat | `/traspaso-in entro` (in Codex, `$traspaso-in entro`) | Reads it, tells it in 4-5 bullets, archives it and asks where to go next |

Claude Code shows the handoff by itself on opening; in Codex and Gemini you have to type `entro`. If you do not type `salgo` first, the new chat has nothing to read.

### Switching AI (Claude, Gemini, Codex): `traspaso-out`
Gemini and Codex do not run hooks (no summary on opening and no notice on closing), so the switch is done with one sentence on each side. Only one AI at a time works on the project.

| Moment | What you type | What the AI does |
|---|---|---|
| When leaving an AI | `/traspaso-out salgo` (in Codex, `$traspaso-out salgo`) | Looks at git and the tests and writes `.brain/traspaso.md` with who writes it, who continues and the time. Then commits the memory and pushes it to GitHub |
| When arriving at the other (new chat) | `/traspaso-out entro` (in Codex, `$traspaso-out entro`) | Reads the handoff, tells it in 4-5 bullets, archives it and asks where to go next |
| Only see the state, without switching | `/resumen` (in Codex, `$resumen`) | Tells the state without writing anything |
| See lists of what is missing | `/pendiente` (in Codex, `$pendiente`) | Menu: program, test, your actions, specs |

If Gemini does not recognize the skill, ask it: "read `GEMINI.md`, `.brain/traspaso.md` and `.brain/pendientes.md` and tell me the state". Without hooks there is no way to make it automatic: the sentence is mandatory.

**Automatic Git on leaving:** `traspaso-out salgo` launches `guardar_traspaso.py`, which saves and pushes the memory so the context reaches the other AI or another computer.
- **Goes into the commit:** the handoff, the archived handoffs, the log, the pending list and the specs.
- **Does not go in:** loose code. It lists it for you and you decide.
- **It stops if:** it finds a secret (no commit) or there are other unpushed commits that are not memory (it makes the commit locally and asks before pushing).
- **Never** forces the push or merges anything. If Git fails, it tells you and the handoff goes ahead.

`traspaso-in` does no Git. To switch computers with the same AI, say "sube" (push; skill `subir-a-github`) or use `traspaso-out`. What has not been pushed does not reach the other computer. Claude's automatic memory does not travel either, because it lives outside the repository.

## 6. Where everything is
| What you are looking for | Where |
|---|---|
| What is left to do | `.brain/pendientes.md` |
| What was already done and you tested | `.brain/archive/hechos-indice.md` (the detail, in `hechos.md`) |
| What was done and when | `.brain/decisions.log` |
| Why something was decided | `.brain/decisions/indice.md` and its `D-NNN` cards |
| Rules that are not touched | `.brain/constitution.md` |
| Approved plans | `.brain/specs/` |
| The full method | `.brain/biblioteca/CEREBRO_VIVO.en.md` |

**The indexes (`decisions/indice.md`, `archive/hechos-indice.md`) are on demand:** startup does not read them; they are opened only when a card has to be looked up. In the test (spec 004, ~80 cards) they did not improve accuracy and cost somewhat more, so they are kept but not loaded every time. The entry files (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`) are kept short and with links to the brain.

**Gemini and Codex:** `/prompt-inicial` and Claude Code's hooks (the automatic summary on opening and the notice on closing) do not work there; the project adapts to the method written in `GEMINI.md` / `AGENTS.md`. In Codex the skills are invoked with `$prompt-inicial` and must be in `.agents/skills/` (Codex does not read `.claude/skills/`). Always open a new chat: an already open chat does not reload the entry file.

## 7. Bringing improvements to a project that already uses it
**The easy way (1.17.0):** when opening a chat shows "Harness: there is a new version", type **`/actualizar`**. It tells you what it brings, asks for your yes and does everything (backup, new keys, skill cards). What follows is the manual way, in case a project has no `arnes_repo` recorded: the first time update it from here with `python actualizar.py PATH` and it is recorded by itself.

First **simulate** (writes nothing), then update:
```bash
python .brain/guardianes/actualizar_arnes.py --simular
python .brain/guardianes/actualizar_arnes.py
```
It saves a copy first, does not overwrite what you changed by hand and never touches your pending list, specs, decisions or log. An old project with no previous record uses `--forzar-todo`, **only** after seeing the list with `--simular`.

**From cerebro-vivo, onto another project** (does the same; useful if the project does not have `actualizar_arnes.py` yet):
```bash
python actualizar.py "PROJECT_PATH" --simular
python actualizar.py "PROJECT_PATH"
```

**Updater options** (both ways accept them, unless noted):
| Option | What it does |
|---|---|
| `--simular` | Shows what would change; writes nothing. Always use it first |
| `--forzar PATH` | Overwrites that file even if you edited it by hand (with a copy) |
| `--forzar-todo` | Overwrites **all** hand-edited ones (with a copy). Commit first and look at the list with `--simular` |
| `--migrar-objetivo` | Only inside the project. For projects installed before 1.6.0: creates `.brain/architecture/objetivo.md`, links it in `CLAUDE.md`/`GEMINI.md`/`AGENTS.md` and adds the rule to the constitution. It only adds; it can be repeated. Try first with `--simular` |
| `--dueno NAME` | Records the owner if the project has none |
| `--repo PATH` | Harness repo to use (otherwise the one in `arnes_repo` in `guardianes.json`) |
| `--sin-pruebas` | Does not run the method's tests at the end |

Backups stay in `.brain/copias_arnes/`. If the project uses Codex (`AGENTS.md`), the updater also copies the skills to `.agents/skills/`. **Language:** a project with `"idioma": "en"` in `guardianes.json` receives the English editions (`X.en.md`) of skills, manual and templates in the place of `X.md`; to switch language, change that setting and update.

## 8. Measuring whether it is helping you
```bash
python .brain/guardianes/medir.py
```
It shows per chat the cost, your messages and how many times you had to correct the AI. Ideas for a real project: note the average **before** putting the harness in, put it in, and compare 3-4 weeks later. Other options: `--comparar WITH_FOLDER WITHOUT_FOLDER`, `--tarea TEXT` (only one kind of task), `--desglose ID` (one chat message by message). Read-only; it changes nothing.

## 9. Notices and guardians you will see
- **Startup** (when opening a chat): real state of pending items, unpushed commits, what is still uncommitted (also in `.brain/` and `.claude/`, except what is generated by itself), last log line.
- **Close** (at the end of a reply): warns if the log line is missing. Only once.
- **Light mode:** on small tasks with green tests, the log line is written by itself.
- **Secrets:** `python .brain/guardianes/secretos.py` looks for keys or personal data; `--historial` also reviews what is already stored in git. Run it before pushing anything online.

## 10. Rules for you
- Do not push anything to GitHub without running `secretos.py` and without deciding it yourself. Say "sube" and the `subir-a-github` skill reviews it. The only push without your order is the memory of `traspaso-out salgo`.
- If a result "seems too good", ask it to test it and to say so as untested if it could not.
- After changing any file **in this repo**: raise `VERSION`, note `CAMBIOS.md`, `python generar_manifiesto.py` and `python -m unittest discover tests`.

## 11. When something does not work
| Symptom | What to do |
|---|---|
| The summary does not appear when opening the chat | Ask the AI to run `python .brain/guardianes/arranque.py` |
| It asks to read too much | New chat with a handoff; long chats are what costs the most |
| A notice repeats or annoys | Tell it; the caps are in `.brain/guardianes/guardianes.json` |
| Doubts about whether something broke on updating | `python -m unittest discover tests`; the copies are in `.brain/copias_arnes/` |

## 12. All the commands in one table
`PATH` is the project folder. Those in `.brain/guardianes/` are launched inside the project; `actualizar.py` and `instalar.py`, from cerebro-vivo.

| What for | Command |
|---|---|
| Install in a new project (window) | double-click `instalar_kit.bat` |
| Install in a new project (terminal) | `python .brain/biblioteca/kit-arranque/instalar.py PATH --nombre Name --dueno Darwin --nivel completo` (levels: `ligero`, `medio`, `completo`; `--traduccion` adds es/en/pt; `--idioma English` for the English editions) |
| Check an already installed project | `python .brain/biblioteca/kit-arranque/instalar.py PATH --comprobar` |
| See what an update would bring | `python actualizar.py PATH --simular` (or, inside the project, `python .brain/guardianes/actualizar_arnes.py --simular`) |
| See the project's harness version | `/version` (also says whether there is a newer one) |
| Note a lesson on the spot (the milestone guardian requires it) | `/leccion` |
| See the previous chat's full history | `/memoria-traspaso` (or `/memoria-traspaso 2` for an older one) |
| Have the AI open the new chat by itself when the chat gets long (or only warn) | `/chat-nuevo si`, `/chat-nuevo no`, `/chat-nuevo estado` |
| Update a project (the easy way) | type `/actualizar` when the notice appears at startup |
| `/actualizar` or `/version` do not exist (project older than 1.17.0 or 1.21.0) | the first time, by hand: `python .brain/guardianes/actualizar_arnes.py --simular` inside the project, or `python actualizar.py PATH --simular` from cerebro-vivo; then the same without `--simular` |
| Update a project (by hand) | `python actualizar.py PATH` (or `python .brain/guardianes/actualizar_arnes.py`) |
| Overwrite hand-edited files | `--forzar FILE_PATH` (one) or `--forzar-todo` (all; commit first) |
| Migrate the goal into an old project | `python .brain/guardianes/actualizar_arnes.py --migrar-objetivo --simular` and then without `--simular` |
| Other updater options | `--dueno NAME`, `--repo PATH`, `--sin-pruebas` |
| Startup summary by hand (Gemini, Codex) | `python .brain/guardianes/arranque.py --manual` |
| Close a task (line in the log) | `python .brain/guardianes/cerrar.py --chat "Project #N" "what was done"` (`--carril`, `--simular`) |
| Add decision cards missing a row to the index | `python .brain/guardianes/cerrar.py --indices` |
| Move a tested item to done | `python .brain/guardianes/cerrar.py --hecho N` (`--conservar` if something is still pending) |
| Measure chats (tokens, cost) | `python .brain/guardianes/medir.py` (`--ultimos N`, `--desglose ID`, `--tarea TEXT`, `--comparar PATH_WITH PATH_WITHOUT`) |
| Tests | `python -m unittest discover tests` |
| Regenerate the harness manifest (in cerebro-vivo, after changing something) | `python generar_manifiesto.py` |
| Distribute the old CLAUDE.md into the memory | `/adopta` (skill `adoptar-indice-existente`) |
| Bring the AI indexes down to the 5 KB cap | `/acorta` |
| Split a fat `.brain/` file by topics | `/trocea` (see which: `python .brain/guardianes/archivos_gordos.py`) |
| Review the AI indexes (double pass) | "revisa los índices" (`python .brain/guardianes/revisar_indices.py` for the report) |
| Skills in Claude | `/resumen`, `/pendiente`, `/prompt-inicial`, `/traspaso-in`, `/traspaso-out`, `/adopta`, `/acorta`, `/trocea`, `/subir-a-github`, `/version`, `/chat-nuevo`, `/leccion`, `/memoria-traspaso` |
| Skills in Codex | `$resumen`, `$pendiente`, `$prompt-inicial`, `$traspaso-in`, `$traspaso-out`, `$adopta`, `$acorta`, `$trocea`, `$subir-a-github`, `$version` (they need `.agents/skills/`) |
