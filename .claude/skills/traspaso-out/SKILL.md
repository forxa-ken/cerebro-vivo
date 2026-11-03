---
name: traspaso-out
description: Use when Darwin types traspaso-out (salgo or entro) or says he is switching AI (Claude, Gemini, Codex).
---

# Traspaso-out: de una IA a otra

Gemini y Codex no corren ganchos: no hay resumen al abrir ni aviso al cerrar. Esta skill los sustituye a mano, con dos modos (`/traspaso-out salgo`, en Codex `$traspaso-out salgo`). Para pasar a un chat nuevo con la misma IA, usar `traspaso-in`.

## Cómo (pasos)
**salgo** (dejo esta IA):
1. Mirar el estado real: `git status --short`, `git log --oneline -5` y el resultado de las últimas pruebas. No fiarse solo de la memoria del chat.
2. Escribir `.brain/traspaso.md` (sobrescribe) con la plantilla de `biblioteca/PLANTILLA_TRASPASO.md`, rellenando **IA que lo escribe**, **IA que sigue** (si Darwin la dijo) y **hora**. Añadir en la sección 4 los archivos sin commitear que salieron de git.
3. Si hubo tarea terminada, cerrarla antes (línea en `decisions.log`).
4. Decirle a Darwin en una frase que ya puede abrir la otra IA y escribir `traspaso-out entro`. No empezar nada más.

**entro** (llego desde otra IA, chat nuevo):
1. Si existe `.brain/guardianes/arranque.py`: ejecutarlo con `--manual`; muestra el estado y el traspaso y lo archiva solo.
2. Si no existe (proyecto en nivel medio): leer `.brain/traspaso.md`, contarlo y luego **mover** (no borrar) el archivo a `.brain/archive/traspasos/AAAA-MM-DD-HHMMSS.md`.
3. Contar a Darwin en 4-5 viñetas llanas: qué dejó la otra IA, qué falta, qué está sin commitear, qué NO hacer. Cerrar con una sola pregunta: por dónde seguir. No empezar nada por cuenta propia.

## Error que evita (caso real)
- Cambiar de IA a mitad de tarea y que la nueva no sepa qué se hizo ni qué estaba descartado: repite o pisa trabajo.

## Dónde está en el repo
- `.claude/skills/traspaso-out`, `biblioteca/PLANTILLA_TRASPASO.md`, `guardianes/arranque.py`, specs 010 y 011.

## Fuente
- Specs 010 y 011, spec 078

## Usada
- Veces: 0 · Última: — (renombrada de cambio-de-ia el 2026-11-03)
