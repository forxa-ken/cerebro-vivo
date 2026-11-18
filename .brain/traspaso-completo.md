# Traspaso completo del chat #35 al #36 (2026-11-18)

- **IA que lo escribe:** Claude
- **IA que sigue:** Claude
- **Hora:** 2026-11-18

## 1. Lo último que pidió Darwin (palabras literales)
- «hacer que la fabrica ponga varios ejecutores a la vez, en este caso codex y deepseek trabajando al tiempo con encargos distintos» y «me dices que piensas».

## 2. Decisiones
- Tomadas: subir y aplicar la 1.60.14 y luego la 1.60.15 (Codex siempre en esfuerzo alto; DeepSeek como tercera ejecutora). Darwin dijo «sí» a ambas subidas.
- Abiertas: ¿redactar la spec 089 del paralelo? Mi propuesta: máx. 2 a la vez (Codex y DeepSeek), solo si no comparten archivos permitidos, contador de fallos y gasto por encargo en fabrica.py, fusión a main de una en una con pruebas, revisión aparte por encargo, probar antes en una fábrica de prueba.

## 3. Estado de cada punto en curso
- 1.60.14 y 1.60.15: subidas (69a6603, 8dc32c8) y aplicadas en empresa-virtual-sim y Prominimap (en Prominimap `tests/test_cerebro_indices.py` no se pisó: modificado a mano).
- Pruebas de tiempos y calidad guardadas en `.brain/respuestas/`: tres tareas con Sonnet 5.5, Codex (high y xhigh), DeepSeek V4.1 Flash Free (opencode-cli.exe de la app de escritorio, `opencode/deepseek-v4.1-flash-free`). Tiempos: tres en raya 8 s / 25 s / 134-153 s; Conecta 4 20 s / 36 s / 81-138 s; inventario 27 s / 17 s / 118 s. Revisión a ciegas del inventario: Codex 9 robustez, DeepSeek 6, Sonnet 5.
- DeepSeek dentro de una fábrica real: aún no probado. La directora #15 de Prominimap (spec 031, encargo 019) decía que no podía lanzarla por tener la skill vieja en memoria; le mandé el aviso y el comando. Falta ver cómo le fue.
- Internet: DeepSeek V4 cerca de los mejores en SWE-bench (~79-81 %), peor en pruebas duras; 4-8 veces más barato; la versión gratuita de OpenCode es «por tiempo limitado»; no entrena con datos según terceros, sin confirmar en la página oficial.

## 4. Sin subir a GitHub
- Nada pendiente de subir.

## 5. Qué debe probar Darwin
- Que la directora de Prominimap lance DeepSeek en un encargo sencillo y revise alcance, pruebas y revisión aparte.

## 6. NO hacer (descartado)
- No tocar vmware-automatizacion ni arreglar nada dentro de empresa-virtual-sim. No tocar encargos en marcha de Prominimap. Gemini no es ejecutora. DeepSeek con `--auto` no tiene caja de seguridad: solo en el worktree del encargo.

## 7. Lecciones apuntadas en este chat
- Ninguna nueva. Recordar: el `claude` de línea de comandos no tiene sesión; `codex exec` ya no admite `--full-auto` (usar `-s workspace-write`); un chat abierto antes de actualizar el arnés conserva la skill vieja.
