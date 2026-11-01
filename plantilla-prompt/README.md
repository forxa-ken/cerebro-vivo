# plantilla-prompt

Panel de Claude Code con una plantilla opcional para el prompt inicial de un proyecto. Se abre con `/plantilla`. Versión 0.3.0 (arnés 1.7.0).

**Qué hace:** tipo de tarea, tres campos (o diez en modo completo), avisos de lo que falta, insertar el encargo en el chat, mejorarlo con IA (Haiku), guardar la plantilla en blanco como `.md` para Gemini/Codex y sugerencias según el proyecto. Los botones de estado lanzan las skills del arnés: «Ver los pendientes» pone `/pendiente` en el chat y «Resumen del estado» pone `/resumen`.

## Cómo instalarlo y actualizarlo
No es un archivo de proyecto: se instala en Claude Code, una vez por equipo, y `actualizar_arnes.py` no lo toca.

1. Desde Claude Code: `/plugin marketplace add RUTA_DE_ESTE_REPO` y luego `/plugin install plantilla-prompt@cerebro-vivo`.
2. Alternativa: copiar esta carpeta a `~/.claude/dev-mods/<sesión>/plantilla-prompt/` o arrancar con `--plugin-dir RUTA_DE_ESTE_REPO/plantilla-prompt`.
3. Para actualizar: traer los cambios del repo (`git pull` o copiar de nuevo) y repetir el paso con el que lo instalaste.

Lógica pura y probada en `hooks/logica.ts` (`claude plugin test`).
