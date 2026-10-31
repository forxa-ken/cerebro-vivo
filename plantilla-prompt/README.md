# plantilla-prompt

Panel de Claude con una plantilla opcional para el prompt inicial de un proyecto. Se abre con `/plantilla`.

Copia versionada del mod. El mod que carga Claude vive en `~/.claude/dev-mods/<sesión>/plantilla-prompt/`; para usarlo en otra sesión, copiar esta carpeta ahí (o `--plugin-dir`). Lógica pura y probada en `hooks/logica.ts` (`claude plugin test`).
