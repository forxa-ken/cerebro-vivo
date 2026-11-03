---
name: cambio-de-ia
description: Use when Darwin says he is switching AI (Claude, Gemini, Codex) or types /cambio-de-ia, either leaving or arriving.
---

# Cambio de IA

Gemini y Codex no corren ganchos: no hay resumen al abrir ni aviso al cerrar. Esta skill los sustituye a mano, con dos modos.

## Cómo (pasos)
**Salgo** (Darwin dice «cambio de IA, salgo» o similar):
1. Mirar el estado real: `git status --short`, `git log --oneline -5` y el resultado de las últimas pruebas. No fiarse solo de la memoria del chat.
2. Escribir `.brain/traspaso.md` (sobrescribe) con la plantilla de `biblioteca/PLANTILLA_TRASPASO.md`, rellenando arriba **IA que lo escribe**, **IA que sigue** (si Darwin la dijo) y **hora**. Añadir en la sección 4 los archivos sin commitear que salieron de git.
3. Si hubo tarea terminada, cerrarla antes (línea en `decisions.log`).
4. Decirle a Darwin en una frase que ya puede abrir la otra IA y escribir «cambio de IA, entro». No empezar nada más.

**Entro** (Darwin dice «cambio de IA, entro» o abre un chat nuevo en otra IA):
1. Si existe `.brain/guardianes/arranque.py`: ejecutarlo con `--manual`; muestra el estado y el traspaso y lo archiva solo.
2. Si no existe (proyecto en nivel medio): leer `.brain/traspaso.md`, contarlo y luego **mover** (no borrar) el archivo a `.brain/archive/traspasos/AAAA-MM-DD-HHMMSS.md`.
3. Contar a Darwin en 4-5 viñetas llanas: qué dejó la otra IA, qué falta, qué está sin commitear, qué NO hacer. Cerrar con una sola pregunta: por dónde seguir. No empezar nada por cuenta propia.

## Error que evita (caso real)
- Cambiar de IA a mitad de tarea y que la nueva no sepa qué se hizo ni qué estaba descartado: repite o pisa trabajo.

## Dónde está en el repo
- `.claude/skills/cambio-de-ia`, `biblioteca/PLANTILLA_TRASPASO.md`, `guardianes/arranque.py`, spec 010.

## Fuente
- Spec 010, spec 078

## Usada
- Veces: 0 · Última: — (creada el 2026-11-03)
