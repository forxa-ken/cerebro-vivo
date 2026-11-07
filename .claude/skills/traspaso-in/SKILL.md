---
name: traspaso-in
description: Use when Darwin types traspaso-in (salgo or entro), a chat gets long, or he asks to open a new chat with the same AI.
---

# Traspaso-in: de un chat al chat nuevo, con la misma IA

El chat nuevo no ve el anterior; solo sabe lo que hay en archivos. Dos modos, con la palabra detrás del comando (`/traspaso-in salgo`, en Codex `$traspaso-in salgo`). **Sin palabra, es `salgo`** (si el chat es el viejo y Darwin pide pasar a uno nuevo, escribir el traspaso Y abrir el chat nuevo; nunca quedarse solo en el resumen). `entro` solo si Darwin lo escribe o el chat acaba de nacer de un traspaso.

## Cómo (pasos)
**salgo** (cierra este chat):
1. Mirar el estado real: `git status --short`, `git log --oneline -5` y el resultado de las últimas pruebas. No fiarse solo de la memoria.
2. Escribir `.brain/traspaso.md` (sobrescribe) con la plantilla de `biblioteca/PLANTILLA_TRASPASO.md`: lo último que pidió Darwin en sus palabras literales, decisiones, estado de cada punto, lo no subido, lo descartado. En «IA que lo escribe» y «IA que sigue» poner la misma IA.
3. Si hubo tarea terminada, cerrarla antes (línea en `decisions.log`). No empezar nada más.
4. **Abrir el chat nuevo tú mismo** si tienes la herramienta `start_session` (Claude Code de escritorio): cárgala con ToolSearch (`select:mcp__ccd_session__start_session`, sola en su mensaje), ábrelo con contexto `fresh`, `initiation: "user_asked"` y de encargo «leer `.brain/traspaso.md`, ejecutar `traspaso-in entro` y contarlo en 4-5 viñetas»; **enseguida** sepáralo con `detach_session` (id que devuelve `start_session`) para que quede al mismo nivel y no colgado de este. Dile a Darwin cómo se llama el chat nuevo. Si `detach_session` falla, dilo claro: el chat queda anidado, sin más daño.
5. Sin esa herramienta (Codex, Gemini): decir a Darwin que abra el chat nuevo y escriba `traspaso-in entro`.

**entro** (chat nuevo):
1. Si existe `.brain/guardianes/arranque.py`: ejecutarlo con `--manual` (muestra el estado y el traspaso y lo archiva solo). Si no existe: leer `.brain/traspaso.md` y **mover** (no borrar) el archivo a `.brain/archive/traspasos/AAAA-MM-DD-HHMMSS.md`.
2. Contar a Darwin en 4-5 viñetas llanas: lo último que pidió, qué falta, qué está sin commitear, qué NO hacer. Una sola pregunta al final: por dónde seguir. No empezar nada.
3. Si no hay traspaso, decirlo claro; no inventarlo.

Hacerlo pronto: la IA solo puede resumir lo que aún tiene en contexto. Claude Code muestra el traspaso solo al abrir; Codex y Gemini necesitan `entro`.

## Error que evita (caso real)
- Al abrir un chat nuevo se perdía el último tramo hablado.

## Dónde está en el repo
- `.brain/traspaso.md`, `biblioteca/PLANTILLA_TRASPASO.md`, `guardianes/arranque.py`, `longitud.py`, specs 078 y 011.

## Fuente
- D-051, D-069, specs 078 y 011

## Usada
- Veces: 0 · Última: — (renombrada de traspaso-entre-chats el 2026-11-03)
