---
name: vigilar-librerias
description: Use when adding, updating or auditing a Python library.
---

# Vigilar librerias

## Cómo (pasos)
1. Ejecutar `librerias.py` a mano cada 7 días (consulta OSV.dev y PyPI con timeout).
2. El arranque solo lee el resultado y avisa si tiene 10 días o más.
3. Solo avisa: nunca actualiza ni instala solo; falsos avisos van a la lista `ignorar` con motivo.
4. Detalle en `architecture/librerias.md`.

## Error que evita (caso real)
- `requirements.txt` no fija versiones y nadie miraba fallos de seguridad conocidos.

## Dónde está en el repo
- `.brain/guardianes/librerias.py`, `.brain/architecture/librerias.md`

## Fuente
- D-047

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-10-31, spec 079)
