# Prueba de tiempos: Sonnet, Codex y DeepSeek

- **Fuente:** chat cerebro-vivo #35, prueba con Darwin
- **Fecha:** 2026-11-18

Misma tarea a cuatro IAs, una sola ejecución de cada una, lanzadas en paralelo. Un comprobador propio verificó cada resultado. Archivos en el scratchpad de la sesión (temporal).

**Encargo pequeño** (`tictactoe.py`, tres en raya con minimax; el comprobador prueba que la máquina nunca pierde):
- Sonnet 5.5 (subagente): ~8 s, OK.
- DeepSeek V4.1 Flash Free (opencode): 25 s, OK.
- Codex high: 134 s, OK.
- Codex xhigh: 153 s, OK.

**Encargo grande** (Conecta 4 con alfa-beta y `test_conecta4.py`, tope de 30k tokens escrito en el encargo):
- Sonnet 5.5: ~20 s; el subagente informó 63.680 tokens, que incluyen la carga fija de contexto, no comparable. OK.
- DeepSeek V4.1 Flash Free: 36 s; ~20.000 tokens nuevos (12.745 entrada, 3.622 salida, 3.625 razonamiento) más ~49.000 de caché. OK.
- Codex high: 81 s; 18.101 tokens. OK.
- Codex xhigh: 138 s; 13.142 tokens. OK.

**Cómo se lanzó cada uno:**
- Codex: `codex exec --skip-git-repo-check -s workspace-write -m gpt-6.1-sol -c model_reasoning_effort=xhigh|high -` (esta versión, 0.167.0, ya no admite `--full-auto`).
- DeepSeek: `%LOCALAPPDATA%\Programs\ai.opencode.desktop\resources\opencode-cli.exe run -m opencode/deepseek-v4.1-flash-free --auto --archived --format json "<encargo>"` (opencode v2.3.0; `--format json` da los tokens).
- Sonnet: subagente de Claude Code, porque el `claude` de línea de comandos no tenía sesión iniciada.

**Límites de la prueba:**
- Una sola ejecución de cada uno; las diferencias entre Codex high y xhigh no son concluyentes.
- Los tiempos de Codex y DeepSeek incluyen el arranque del programa y los de Sonnet no, así que no son del todo comparables.
- El tope de 30k tokens no se hizo cumplir por la fuerza; solo se comprobó después.
- En Codex, más esfuerzo tardó más y gastó menos tokens en el grande.
