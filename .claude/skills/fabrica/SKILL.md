---
name: fabrica
description: Use when Darwin types /fabrica (si, no or estado) or asks to turn on or off the factory mode of the project (the AI as director who does not code).
---

# /fabrica — modo fábrica, sí o no

Activa, desactiva o muestra el ajuste `modo_fabrica` de `.brain/guardianes/guardianes.json`. Por defecto está apagado (modo normal). Encendido, **se recuerda entre chats**: el arranque de cada chat nuevo dice «MODO FÁBRICA ACTIVADO» y la IA actúa como directora (skill `directora-de-fabrica`) sin que Darwin lo repita.

## Cómo (pasos)
1. Leer la palabra detrás del comando: `si` (activar), `no` (desactivar) o `estado` (solo mirar). Sin palabra, `estado`.
2. Ejecutar `python .brain/guardianes/fabrica.py modo PALABRA`.
3. Decir a Darwin en una línea cómo queda, con el texto que imprime el script. Con `si`, cargar la skill `directora-de-fabrica` y seguirla; con `no`, trabajar como un chat normal. La carta la escribe Darwin, no la IA.

## Error que evita (caso real)
- El proyecto tenía `.brain/fabrica/` pero cada chat nuevo trabajaba como un chat normal: nadie le decía que era una fábrica y había que repetirlo en todos los chats.

## Dónde está en el repo
- `.claude/skills/fabrica`, `.brain/guardianes/fabrica.py` (`modo`), `arranque.py`, `guardianes.json` (`modo_fabrica`), spec 040.

## Fuente
- Spec 040 (petición de Darwin, 2026-11-11)

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-11-11)
