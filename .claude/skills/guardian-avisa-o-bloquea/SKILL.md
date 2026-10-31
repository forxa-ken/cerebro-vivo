---
name: guardian-avisa-o-bloquea
description: Use when creating an automatic check (guardian) for the Cerebro Vivo method.
---

# Guardian avisa o bloquea

## Cómo (pasos)
1. Por defecto, solo avisa: una línea en el resumen de arranque y detalle bajo `--ver`.
2. Bloquea solo lo irreversible (un secreto subido a GitHub no se puede «des-subir»).
3. Si el guardián falla, calla: nunca debe tumbar el trabajo.
4. Ajustes en `guardianes.json`; lo existente que incumple se anota como excepción con motivo.
5. Añadir test y una fila en `herramientas.md`.

## Error que evita (caso real)
- Las reglas que dependen de la disciplina de la IA se olvidan en silencio.

## Dónde está en el repo
- `.brain/guardianes/`, `guardianes.json`

## Fuente
- D-039, D-044, D-046, carta principio 8

## Usada
- Veces: 0 · Última: — (creada el 2026-10-31, spec 079)
