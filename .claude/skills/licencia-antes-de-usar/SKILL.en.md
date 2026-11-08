---
name: licencia-antes-de-usar
description: Use when adopting a free service, voice, font, model or library in something commercial.
---

# License before use

## How (steps)
1. Check the license and whether it allows commercial use before publishing.
2. Prefer clear open licenses (Apache 2.0, MIT, BSD).
3. Note the license and credits in `herramientas.md` and in the code.
4. If in doubt, replace it before launch and leave the decision in a D-NNN card.

## Error it prevents (real case)
- `edge-tts` is free but does not guarantee a commercial license: it had to be swapped for Kokoro-82M (Apache 2.0).

## Where it lives in the repo
- `.brain/biblioteca/herramientas.md`

## Source
- D-037, D-041, letter §16

## Used
- Real use: `python .brain/guardianes/medir.py --skills` (not logged here) (created on 2026-10-31, spec 079)
