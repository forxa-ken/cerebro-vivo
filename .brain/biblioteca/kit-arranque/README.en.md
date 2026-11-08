# Cerebro Vivo starter kit (spec 054, D-049)

Sets up the memory and the guardians in a new project with one command. The guardians are copied from this very project (a single source of truth) with the neutral settings of `ajustes_neutros.json`; the templates are in `plantillas/`. It never overwrites a file that already exists.

```
python .brain/biblioteca/kit-arranque/instalar.py C:\path\new-project --nombre My --dueno Ana --idioma English --pruebas "pytest" --ias claude,codex --nivel completo
python .brain/biblioteca/kit-arranque/instalar.py C:\path\new-project --comprobar
```

Levels: `ligero` (index + pending + log), `medio` (+ constitution, decisions, facts, specs), `completo` (+ guardians, Claude Code hooks, index tests, library, test memory, secrets hook). After installing: restart Claude Code in the project and run `--comprobar`.

**With a window (spec 055):** double-click `instalar_kit.bat` (project root). It asks for the folder, project name, your name, language, test command, AI and level; it shows a summary to confirm, installs, runs `git init` if missing and checks the guardians. It remembers your name, language and test command for next time (`preferencias.json`, ignored by Git).
