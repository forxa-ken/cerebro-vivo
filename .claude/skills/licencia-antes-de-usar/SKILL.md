---
name: licencia-antes-de-usar
description: Use when adopting a free service, voice, font, model or library in something commercial.
---

# Licencia antes de usar

## Cómo (pasos)
1. Mirar la licencia y si permite uso comercial antes de publicar.
2. Preferir licencias abiertas claras (Apache 2.0, MIT, BSD).
3. Anotar la licencia y los créditos en `herramientas.md` y en el código.
4. Si hay duda, sustituir antes de lanzar y dejar la decisión en una ficha D-NNN.

## Error que evita (caso real)
- `edge-tts` es gratis pero no garantiza licencia comercial: hubo que cambiarlo por Kokoro-82M (Apache 2.0).

## Dónde está en el repo
- `.brain/biblioteca/herramientas.md`

## Fuente
- D-037, D-041, carta §16

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-10-31, spec 079)
