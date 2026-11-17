---
name: fabrica
description: Use when Darwin types /fabrica (si, no or estado) or asks to turn on or off the factory mode of the project (the AI as director who does not code).
---

# /fabrica — modo fábrica, sí o no

Activa, desactiva o muestra el ajuste `modo_fabrica` de `.brain/guardianes/guardianes.json`. Por defecto está apagado (modo normal). Encendido, **se recuerda entre chats**: el arranque de cada chat nuevo dice «MODO FÁBRICA ACTIVADO» y la IA actúa como directora (skill `directora-de-fabrica`) sin que Darwin lo repita.

## Cómo (pasos)
1. Leer la palabra detrás del comando: `si` (activar), `no` (desactivar) o `estado` (solo mirar). Sin palabra, `estado`.
2. Ejecutar `python .brain/guardianes/fabrica.py modo PALABRA`.
3. Decir a Darwin en una línea cómo queda, con el texto que imprime el script. Con `no`, trabajar como un chat normal. La carta la escribe Darwin, no la IA.
4. **Con `si`, el chat de la directora se abre solo** (una directora por proyecto, en chat limpio; este chat no se convierte en la directora). Solo si el modo estaba apagado antes: si ya estaba activo, no abrir otro. Pasos, sin pedir permiso (Darwin lo autorizó de forma permanente):
   - **Preguntar antes a Darwin lo de rigor**, con una sola llamada a `AskUserQuestion` (cárgala con ToolSearch si hace falta), tres preguntas cerradas y en lenguaje llano: (1) **modelo de la directora**: Sonnet 5.5 (recomendado, gasta menos), Opus 5.5 (más potente, gasta más) u otro que escriba él; (2) **ejecutora por defecto**: Codex, Claude o «la que decida la directora»; (3) **modo automático**: encendido (por defecto) o apagado. Aplicar lo que responda: el modelo va al `start_session` de abajo; si apaga el automático, `python .brain/guardianes/fabrica.py automatico no`; el modelo y la ejecutora se anotan en el traspaso («elegido por Darwin») y el modelo en la segunda línea de `.brain/fabrica/directora_n.txt`. La directora los pasa al borrador de la carta; **la carta la sella Darwin**, no la IA. Si el modo ya estaba activo, no preguntar.
   - Escribir `.brain/traspaso.md` corto (plantilla `biblioteca/PLANTILLA_TRASPASO.md`) con lo que Darwin quiere de la fábrica, qué encargos o ideas hay, y «NO hacer: programar». Es la directora quien lo leerá.
   - Cargar `start_session` con ToolSearch (`select:mcp__ccd_session__start_session`, sola en su mensaje) y abrir el chat con contexto `fresh`, `initiation: "user_asked"`, `model` el que eligió Darwin (por defecto `"claude-sonnet-5-5"`: Sonnet 5.5, por gasto, orden de Darwin 2026-11-17; Opus `"claude-opus-5-5"` si lo elige él o lo dice la carta), `effort: "medium"`, `title: "directora #N"` y `name: "directora-N"`, donde N es el número de directoras que ha tenido el proyecto (lleva la cuenta en `.brain/fabrica/directora_n.txt`: léelo, suma 1 y guárdalo; si no existe, N = 1), y de encargo «eres la directora de fábrica: separarte del chat que te abrió (`get_session` con `self`; si no está `detached`, `detach_session` con `self`), leer `.brain/traspaso.md`, cargar la skill `directora-de-fabrica` y contarle a Darwin en 4-5 viñetas por dónde empezar. No programes».
   - **Enseguida** `detach_session` con el id que devuelve, para que no cuelgue de este chat. Comprobar con `get_session` (`session_id` el que devuelve) que quedó en Sonnet con esfuerzo medio: la app ignora un modelo mayor que el del chat que lo abre, y si este chat no es Opus puede heredar el suyo. Si no coincide, corregirlo con `set_session_model` y `set_session_effort`, o decírselo a Darwin. Decir a Darwin cómo se llama el chat nuevo. Anotar el modelo usado en `.brain/fabrica/directora_n.txt` (segunda línea) para cruzar el gasto con `medir.py --fabrica`.
   - Sin esas herramientas (Codex) o si la app rechaza la llamada tras intentarla: decirlo claro y dar la frase para abrirlo a mano. Nunca decir que se rechaza sin haberlo intentado.

## Modo automático (spec 050)
- `/fabrica automatico si|no|estado` → `python .brain/guardianes/fabrica.py automatico PALABRA`. Solo vale con el modo fábrica encendido; `fabrica.py arrancar` bloquea el arranque de un encargo si falta el criterio o se está en `main`; `estado` dice qué falta (carta sellada, criterio de «esperado» en `.brain/fabrica/esperado.md`, rama de trabajo que no sea `main`). Ajuste `fabrica_automatica`: **nace encendido junto con la fábrica** (`/fabrica si`, orden de Darwin 2026-11-17); solo si el modo estaba apagado, así repetir `/fabrica si` no lo reenciende si Darwin lo apagó con `automatico no`. `/fabrica no` o `modo normal` lo apagan también.
- Activarlo no abre ningún chat nuevo: lo único que cambia es el aviso del arranque. Las fases siguientes (revisor de spec, prueba de uso real) se activan con sus propias specs.

## Error que evita (caso real)
- El proyecto tenía `.brain/fabrica/` pero cada chat nuevo trabajaba como un chat normal: nadie le decía que era una fábrica y había que repetirlo en todos los chats.

## Dónde está en el repo
- `.claude/skills/fabrica`, `.brain/guardianes/fabrica.py` (`modo`), `arranque.py`, `guardianes.json` (`modo_fabrica`), spec 040.

## Fuente
- Spec 040 (petición de Darwin, 2026-11-11)

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-11-11)
