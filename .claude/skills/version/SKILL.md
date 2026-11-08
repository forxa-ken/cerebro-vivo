---
name: version
description: Use when Darwin types /version or asks which version of the arnés (Cerebro Vivo) this project has.
---

# /version — qué versión del arnés tiene este proyecto

Solo lee; no escribe ni actualiza nada.

## Cómo (pasos)
1. Versión instalada: campo `version` de `.brain/arnes_instalado.json`. Si el archivo no existe, decir que el proyecto es anterior al registro de versiones (antes de la 1.0.0) o que no tiene el arnés.
2. Versión disponible: `arnes_repo` de `.brain/guardianes/guardianes.json` y el archivo `VERSION` de esa carpeta. Si falta `arnes_repo`, es una dirección web o la carpeta no existe, decir que no se puede comparar y por qué.
3. Contar a Darwin en 2-3 viñetas llanas:
   - Versión instalada y versión disponible.
   - Si hay una más nueva: los títulos de las versiones nuevas en `CAMBIOS.md` del repo del arnés, en una línea cada uno.
   - Cómo actualizar: `/actualizar`. Si la versión instalada es anterior a la 1.17.0, ese comando aún no existe en el proyecto; la primera vez se actualiza a mano, en la terminal y dentro del proyecto, con `python .brain/guardianes/actualizar_arnes.py --simular` y luego sin `--simular`. También vale, desde cerebro-vivo, `python actualizar.py "RUTA_DEL_PROYECTO" --simular` y luego sin `--simular`.
4. No actualizar sin que Darwin lo pida.

## Error que evita (caso real)
- En Modelo 2 (arnés 1.12.0) `/actualizar` no existía y no había forma rápida de saber qué versión tenía el proyecto.

## Dónde está en el repo
- `.claude/skills/version`, `.brain/arnes_instalado.json`, `actualizar_arnes.py` (`version_disponible`), spec 023.

## Fuente
- Spec 023 (petición de Darwin, 2026-11-07)

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-11-07)
