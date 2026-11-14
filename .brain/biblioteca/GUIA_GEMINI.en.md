# Short recipe: install Cerebro Vivo in a project that uses Gemini (Antigravity)

For anyone working with **Antigravity/Gemini**. The general guide (all AIs) is `GUIA_INSTALACION.md`; this covers only what changes with Gemini. The installer was tested with `--ias gemini` in a scratch folder; **not tested inside a real Antigravity**.

## 1. Install
From the harness repo (change the paths and the name):
```powershell
python "HARNESS_REPO_PATH\.brain\biblioteca\kit-arranque\instalar.py" "PROJECT_PATH" --nombre NAME --dueno OWNER --idioma english --pruebas "python -m unittest discover tests" --ias gemini --nivel completo
```
Or with the window: double-click `instalar_kit.bat` and tick only Gemini under "AI that will be used".

It creates `GEMINI.md` (the index Gemini reads), `.brain/` (memory, constitution, pending list), the guardians and the tests. It also leaves `.claude/` with the Claude Code hooks: harmless, Gemini does not use it.

**Skills for Gemini:** Antigravity's project-level skills live in `.agents/skills/`, and the installer only copies them **if the project has `AGENTS.md`**. With `--ias gemini` alone they are not created. If you want the skills, install with `--ias gemini,codex` (they are called with `$name`, not `/`).

## 2. Check
```powershell
python "PROJECT_PATH\.brain\biblioteca\kit-arranque\instalar.py" "PROJECT_PATH" --comprobar
```
Everything should show ✅. The "Claude Code hooks" line is normal and does not affect Gemini.

## 3. How it is used (what differs from Claude)
- **Gemini runs no hooks:** no startup summary and no closing notice. When you open a chat, ask it: "read `GEMINI.md`, `.brain/traspaso.md` and `.brain/pendientes.md` and tell me the state". Or run `python .brain/guardianes/arranque.py --manual` yourself.
- **When a task ends:** have it write the log line with `python .brain/guardianes/cerrar.py --chat "name #N" "what was done"`.
- **Switching chat or AI:** type `salgo` in the chat you leave and `entro` in the new one; only one AI works on the project at a time.
- **Do not work in Gemini:** `/prompt-inicial` and the automatic notices.
- **Old global plugin** (`%USERPROFILE%\.gemini\config\plugins\cerebro-vivo`): outdated, do not use it.

## 4. Update later
```powershell
python .brain/guardianes/actualizar_arnes.py --simular
python .brain/guardianes/actualizar_arnes.py
```
It does not overwrite what you changed by hand.
