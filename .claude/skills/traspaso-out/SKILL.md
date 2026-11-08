---
name: traspaso-out
description: Use when Darwin types traspaso-out (salgo or entro) or says he is switching AI (Claude, Gemini, Codex).
---

# Traspaso-out: de una IA a otra

Gemini y Codex no corren ganchos: no hay resumen al abrir ni aviso al cerrar. Esta skill los sustituye a mano, con dos modos (`/traspaso-out salgo`, en Codex `$traspaso-out salgo`). Para pasar a un chat nuevo con la misma IA, usar `traspaso-in`.

## Cómo (pasos)
**salgo** (dejo esta IA):
1. Mirar el estado real: `git status --short`, `git log --oneline -5` y el resultado de las últimas pruebas. No fiarse solo de la memoria del chat.
2. Escribir **dos** archivos (sobrescriben) con las plantillas de `biblioteca/PLANTILLA_TRASPASO.md` (spec 026): `.brain/traspaso.md` **corto** (~1500 caracteres) y `.brain/traspaso-completo.md` con el historial entero, rellenando **IA que lo escribe**, **IA que sigue** (si Darwin la dijo) y **hora**. Poner en «Sin subir» y en la sección 4 los archivos sin commitear que salieron de git. Si queda un hito sin lección, apuntarla antes con `/leccion`.
3. Si hubo tarea terminada, cerrarla antes (línea en `decisions.log`).
4. **Guardar y subir la memoria (spec 022):** si existe `.brain/guardianes/guardar_traspaso.py`, ejecutarlo. Hace commit solo de la memoria (traspaso, traspasos archivados, registro, pendientes y specs) y lo sube a GitHub. Esta es la única subida sin orden expresa de Darwin. Si no existe, decirle que el traspaso queda sin guardar en Git.
5. Contarle a Darwin lo que diga el guardián: lo que no entró en el commit y, si no se subió, por qué. Si lista otros commits sin subir, preguntarle, y solo con su sí relanzarlo con `--subir-todo`. Un fallo de Git no para el traspaso.
6. Decirle en una frase que ya puede abrir la otra IA y escribir `traspaso-out entro`. No empezar nada más.

**entro** (llego desde otra IA, chat nuevo):
1. Si existe `.brain/guardianes/arranque.py`: ejecutarlo con `--manual`; muestra el estado y el traspaso y lo archiva solo.
2. Si no existe (proyecto en nivel medio): leer `.brain/traspaso.md`, contarlo y luego **mover** (no borrar) el archivo a `.brain/archive/traspasos/AAAA-MM-DD-HHMMSS.md`.
3. (El historial completo queda en `.brain/archive/traspasos/*-completo.md`; `/memoria-traspaso` lo trae.) Contar a Darwin en 4-5 viñetas llanas: qué dejó la otra IA, qué falta, qué está sin commitear, qué NO hacer. Cerrar con una sola pregunta: por dónde seguir. No empezar nada por cuenta propia.

## Error que evita (caso real)
- Cambiar de IA a mitad de tarea y que la nueva no sepa qué se hizo ni qué estaba descartado: repite o pisa trabajo.

## Dónde está en el repo
- `.claude/skills/traspaso-out`, `biblioteca/PLANTILLA_TRASPASO.md`, `guardianes/arranque.py`, `guardianes/guardar_traspaso.py`, specs 010, 011 y 022.

## Fuente
- Specs 010, 011 y 022, spec 078

## Usada
- Veces: 0 · Última: — (renombrada de cambio-de-ia el 2026-11-03)
