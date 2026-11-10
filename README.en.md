# cerebro-vivo

[Léelo en español](README.md)

The **"Cerebro Vivo" meta-harness**: a method for working with an AI without losing context between chats and while spending few tokens, plus the tools that make it stick. One single repository, and each project decides when to pull in the improvements.

**Day-to-day user manual: [`MANUAL_DE_USO.en.md`](MANUAL_DE_USO.en.md).**

Note: file, folder and command names stay in Spanish on purpose (`pendientes.md`, `guardianes/`, `/actualizar`, `traspaso-in`); changing them would break existing projects. The content (guardian notices, skills, manual, templates) is available in English: a project with `"idioma": "en"` in `.brain/guardianes/guardianes.json` receives the English editions (`X.en.md`) in the place of `X.md`.

## Sources
- Lee, Yoonho; Nair, Roshen; Zhang, Qizheng; Lee, Kangwook; Khattab, Omar; Finn, Chelsea. *Meta-Harness: End-to-End Optimization of Model Harnesses*. arXiv:2603.28052, March 2026 (https://arxiv.org/abs/2603.28052): Stanford paper on the term "meta-harness".
- Databricks. *Introducing Omnigent: a meta-harness to combine, control and share your agents*, June 2026 (https://www.databricks.com/blog/introducing-omnigent-meta-harness-combine-control-and-share-your-agents): orchestration layer over AI agents.
- Nygard, Michael. *Documenting Architecture Decisions*, November 2011 (https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions): origin of architecture decision records (ADR), the basis of `decisions.log` and `decisions/`.
- Fowler, Martin. *Architecture Decision Record* (https://www.martinfowler.com/bliki/ArchitectureDecisionRecord.html): the decision log as a set of ADRs.
- Microsoft. *Maintain an architecture decision record (ADR)*, Azure Well-Architected Framework (https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record).
- Red Hat. *Why you should be using architecture decision records to document your project* (https://www.redhat.com/en/blog/architecture-decision-records).
- InfoQ. *AWS Publishes Guide to Architecture Decision Records*, June 2022 (https://www.infoq.com/news/2022/06/aws-adr-guide/): AWS guide to ADRs.
- GitHub (Microsoft). *Spec Kit*, repository `github/spec-kit`, August 2025, MIT license (https://github.com/github/spec-kit): spec-driven development; origin of the "constitution" (`constitution.md`) as project rules, as in this method. Its README says to create it once per project.
- GitHub. *Spec-Driven Development* (`spec-driven.md`) (https://github.com/github/spec-kit/blob/main/spec-driven.md): defines the constitution as a set of immutable principles, with a dated amendment process.
- Delimarsky, Den. *Spec-driven development with AI: get started with a new open source toolkit*, GitHub Blog, 2 September 2025 (https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/): Spec Kit announcement (does not mention the constitution).

The implementation is our own, centered on collaborative work between AI agents and persistence of context between chats.

## What it contains
- **Guardians** (`.brain/guardianes/`): startup, close, cerrar, pruning, meter, secrets, libraries, tests, length, analysis, database, indexes, chat notes, lessons and milestones.
- **Manual and letter** (`.brain/biblioteca/CEREBRO_VIVO.md` / `CEREBRO_VIVO.en.md`, `CARTA_META_ARNES.md`), handoff and chat-note templates.
- **`/plantilla` plugin** (`plantilla-prompt/`, a Claude Code panel; installed separately, the updater does not distribute it).
- **Kits**: the starter kit (sets the method up in a new project) and the es/en/pt translation kit.
- Generic **skills** in `.claude/skills/` (including `/prompt-inicial`, `/resumen` and `/pendiente`) and their **tests** in `tests/`.

## What is proven and what is not (measurement of 2026-11-01, specs 001-003)
- **Proven:** when resuming work in a new chat, with the harness what had been agreed was respected 5 out of 5 times; without it, 0 out of 5 (it invented the format). On loose, small tasks both work the same.
- **Cost:** on small tasks the harness spends 7 % to 16 % more than not using it (cache equalized, sonnet 5.5). It does not save on those tasks.
- **Hypothesis (not measured yet):** in a real, long project, the harness saves in the long run because it avoids repeating explanations and redoing work because of mistakes; without a method, those repetitions cost more. It is checked with `python .brain/guardianes/medir.py` in real projects over weeks.
- **Indexes (spec 004, a single real project):** with ~80 cards, having an index did not improve accuracy (30/30 in all three cases) and came out ~19 % more expensive than not having one; an index with false rows did not make anything fail either. It is not shown that the index saves at that size.
- Detail: `.brain/specs/001-resultados.md`, `002-resultados.md`, `003-resultados.md`, `004-resultados.md`.

## Start a new project
```bash
python .brain/biblioteca/kit-arranque/instalar.py PROJECT_PATH --nombre My --dueno Ana --nivel completo --idioma English
```
(or double-click `instalar_kit.bat`). It records in the project where it is updated from (`arnes_repo` in `.brain/guardianes/guardianes.json`). With `--idioma English` the notices, skills, manual and templates are installed in English.

## Bring the improvements to a project that already uses it
From the project itself:
```bash
python .brain/guardianes/actualizar_arnes.py --simular
python .brain/guardianes/actualizar_arnes.py
```
Or from this repo:
```bash
python actualizar.py PROJECT_PATH --simular
python actualizar.py PROJECT_PATH
```
`--simular` only shows what would change. When updating, a copy is first saved in `.brain/copias_arnes/` and what the project edited by hand is **not overwritten** (it is listed; `--forzar PATH` overwrites it). What the harness retired leaves the project into that copy, unless it was modified. Pending list, specs, decisions and log are never touched; in `guardianes.json` only missing keys are added, without changing the existing ones. A light or medium level project receives nothing. At the end it runs the project's method tests.

## To improve the harness
Change it here, raise `VERSION`, note it in `CAMBIOS.md` (kept in Spanish), run `python generar_manifiesto.py` and the tests (`python -m unittest discover tests`).
