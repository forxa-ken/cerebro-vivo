# Short recipe: install Cerebro Vivo in a project that uses GPT Codex

For anyone working with **GPT Codex**. The general guide (all AIs) is `GUIA_INSTALACION.md`; this covers only what changes with Codex. The installer was tested with `--ias codex` in a scratch folder; **not tested inside a real Codex**.

## 1. Install
From the harness repo (change the paths and the name):
```powershell
python "HARNESS_REPO_PATH\.brain\biblioteca\kit-arranque\instalar.py" "PROJECT_PATH" --nombre NAME --dueno OWNER --idioma english --pruebas "python -m unittest discover tests" --ias codex --nivel completo
```
Or with the window: double-click `instalar_kit.bat` and tick only Codex under "AI that will be used".

It creates `AGENTS.md` (the index Codex reads), `.brain/` (memory, constitution, pending list), the guardians, the tests and the **skills in `.agents/skills/`** (copied automatically because `AGENTS.md` exists). It also leaves `.claude/` with the Claude Code hooks: harmless, Codex does not use it.

## 2. Check
```powershell
python "PROJECT_PATH\.brain\biblioteca\kit-arranque\instalar.py" "PROJECT_PATH" --comprobar
```
Everything should show ✅. The "Claude Code hooks" line is normal and does not affect Codex.

## 3. How it is used (what differs from Claude)
- **Skills are called with `$`, not `/`:** `$resumen`, `$pendiente`, `$traspaso-in`, `$traspaso-out`, `$adopta`, `$acorta`, `$trocea`, `$subir-a-github`, `$version`.
- **Codex runs no hooks:** no startup summary and no closing notice. When you open a chat, ask it: "read `AGENTS.md`, `.brain/traspaso.md` and `.brain/pendientes.md` and tell me the state". Or run `python .brain/guardianes/arranque.py --manual` yourself.
- **When a task ends:** have it write the log line with `python .brain/guardianes/cerrar.py --chat "name #N" "what was done"`.
- **Switching chat or AI:** `$traspaso-out salgo` in the chat you leave and `$traspaso-out entro` (or `$traspaso-in entro`) in the new one; only one AI works on the project at a time.
- **Do not work in Codex:** `/prompt-inicial` and the automatic notices.
- **Codex as an auditor from Claude:** if Claude is installed, `python .brain/guardianes/auditor.py codex` prints the read-only `codex exec` command (on Windows it carries the sandbox setting; without it Codex cannot run `python`).

## 4. Update later
```powershell
python .brain/guardianes/actualizar_arnes.py --simular
python .brain/guardianes/actualizar_arnes.py
```
It does not overwrite what you changed by hand and, since `AGENTS.md` exists, it also updates `.agents/skills/`.
