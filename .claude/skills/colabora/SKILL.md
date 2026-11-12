---
name: colabora
description: Use when Darwin types /colabora (si, no or estado) or asks to turn on or off the collaborative mode of the project (several AIs with different roles).
---

# /colabora — modo colaborativo, sí o no

Activa, desactiva o muestra el ajuste `modo_colaborativo` de `.brain/guardianes/guardianes.json` (spec 042). Por defecto está apagado: con una sola IA (Claude con `CLAUDE.md`, Codex con `AGENTS.md` o Gemini con `GEMINI.md`) no hay nada que repartir y todo sigue como siempre. Encendido, **se recuerda entre chats**: el arranque dice «MODO COLABORATIVO ACTIVADO» y cada IA lee primero `.brain/colaboracion.md`.

## Cómo (pasos)
1. Leer la palabra detrás del comando: `si`, `no` o `estado`. Sin palabra, `estado`.
2. Ejecutar `python .brain/guardianes/colabora.py PALABRA`.
3. Decir a Darwin en una línea cómo queda, con el texto que imprime el script.
   - Con `si`: crea `.brain/colaboracion.md` desde la plantilla `biblioteca/IAS_COLABORATIVAS.md` si no existe y añade **una sola línea** que remite a él en los índices que existan (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`), salvo los de `indices_ajenos` (esos no se tocan: se avisa).
   - Con `no`: quita esas líneas. `colaboracion.md` se conserva.
4. Con `si`, ayudar a Darwin a **adaptar la matriz de papeles** de `.brain/colaboracion.md` (qué IA hace qué y qué archivos son suyos), preguntando lo que no sepas; no inventar papeles.
5. No abre ningún chat nuevo (a diferencia de `/fabrica`, no hay directora).

## Error que evita (caso real)
- Dos IA en el mismo proyecto sin papeles escritos: una editaba lo de la otra y las reglas se repetían, a veces distintas, en tres índices.

## Dónde está en el repo
- `.claude/skills/colabora`, `.brain/guardianes/colabora.py`, `arranque.py`, `guardianes.json` (`modo_colaborativo`, `indices_ajenos`), `biblioteca/IAS_COLABORATIVAS.md`, spec 042.

## Fuente
- Spec 042 (petición de Darwin, 2026-11-12)

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-11-12)
