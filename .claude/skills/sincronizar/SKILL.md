---
name: sincronizar
description: Use when Darwin types /sincronizar or says "sincroniza", "baja lo de GitHub" or "ponme al día" (typically on arriving at another computer).
---

# /sincronizar — dejar este ordenador al día con GitHub y listo para trabajar

Solo baja; nunca sube, mezcla ni pisa nada.

## Cómo (pasos)
1. Ejecutar `python .brain/guardianes/sincronizar.py` (con `--simular` si Darwin quiere ver antes qué haría). Hace `git fetch` + `git pull --ff-only` y luego muestra el resumen de arranque (estado, traspaso, versión del arnés).
2. Contar a Darwin en 3-4 viñetas llanas: si había cosas nuevas y cuántas, qué hay sin commitear o sin subir, y lo que diga el traspaso (qué espera su respuesta y el siguiente paso).
3. Si el script sale con error (rama separada, choque con cambios locales, sin internet), decirlo en llano y **no** arreglarlo por cuenta propia: nada de `merge`, `rebase`, `stash`, `reset` ni `push` sin orden de Darwin.
4. Si dice que hay versión nueva del arnés, ofrecer `/actualizar`; no lanzarlo solo.
5. Primera vez en un ordenador sin el proyecto: no existe nada que sincronizar; hace falta `git clone https://github.com/forxa-ken/cerebro-vivo.git`, entrar en la carpeta y decir `/sincronizar` (o `traspaso-in entro`).
6. Una sola pregunta al final: por dónde seguir. No empezar nada.

## Error que evita (caso real)
- Darwin cambió de ordenador a mitad del trabajo y no tenía un comando único para ponerse al día: había que recordar `git pull`, mirar el estado y leer el traspaso por separado.

## Dónde está en el repo
- `.claude/skills/sincronizar`, `.brain/guardianes/sincronizar.py`, `textos.py` (claves `sync_*`), spec 093, `tests/test_sincronizar.py`.

## Fuente
- Spec 093 (petición de Darwin, 2026-11-20)

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-11-20)
