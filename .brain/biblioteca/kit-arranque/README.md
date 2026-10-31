# Kit de arranque de Cerebro Vivo (spec 054, D-049)

Monta la memoria y los guardianes en un proyecto nuevo con un comando. Los guardianes se copian de este mismo proyecto (una sola fuente de verdad) con los ajustes neutros de `ajustes_neutros.json`; las plantillas están en `plantillas/`. Nunca pisa un archivo que ya existe.

```
python .brain/biblioteca/kit-arranque/instalar.py C:\ruta\proyecto-nuevo --nombre Mi --dueno Ana --idioma español --pruebas "pytest" --ias claude,codex --nivel completo
python .brain/biblioteca/kit-arranque/instalar.py C:\ruta\proyecto-nuevo --comprobar
```

Niveles: `ligero` (índice + pendientes + registro), `medio` (+ constitución, decisiones, hechos, specs), `completo` (+ guardianes, hooks de Claude Code, tests de índices, biblioteca, memoria de pruebas, hook de secretos). Tras instalar: reiniciar Claude Code en el proyecto y ejecutar `--comprobar`.

**Con ventana (spec 055):** doble clic en `instalar_kit.bat` (raíz del proyecto). Pide carpeta, nombre, tu nombre, idioma, comando de pruebas, IA y nivel; enseña un resumen para confirmar, instala, hace `git init` si falta y comprueba los guardianes. Recuerda tu nombre, idioma y comando de pruebas para la próxima vez (`preferencias.json`, ignorado por Git).
