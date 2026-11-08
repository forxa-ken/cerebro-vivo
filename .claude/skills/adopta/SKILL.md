---
name: adopta
description: Use when Darwin types /adopta (atajo de adoptar-indice-existente) to split the project's existing CLAUDE.md, GEMINI.md or AGENTS.md into the .brain memory.
---

# /adopta — adoptar, acortar y trocear de una vez

Un solo comando para un proyecto que ya tenía su CLAUDE.md. Encadena tres pasos y **pide el sí de Darwin en cada tabla** (nunca escribe sin él).

## Cómo (pasos)
1. **Repartir:** leer la skill `adoptar-indice-existente` y seguir sus pasos hasta el reparto aprobado (el texto viejo copiado a `.brain/`; copia íntegra en `.brain/archive/adoptado/`).
2. **Acortar:** leer la skill `acorta` y seguirla (tabla «sección → enlace», el sí de Darwin, tope de 5 KB). Si los índices ya caben, saltar este paso y decirlo.
3. **Trocear:** lanzar `python .brain/guardianes/archivos_gordos.py`. Si algún archivo de `.brain/` pasa del tope, leer la skill `trocea` y seguirla (tabla de cortes, el sí de Darwin). Si no hay ninguno, saltar y decirlo.
4. **Cerrar:** lanzar `python .brain/guardianes/revisar_indices.py`, contar el resultado en 3-4 viñetas llanas (tamaños antes y después, nada perdido), quitar la tarea de `.brain/pendientes.md`, pruebas en verde y línea en el registro. Proponer «revisa los índices» como siguiente paso, sin lanzarlo.
5. Si Darwin dice «no» a un paso, parar ahí y dejar anotado en `pendientes.md` qué falta (`/acorta` o `/trocea`).

## Error que evita (caso real)
- Tener que acordarse de tres comandos en orden (y de escribirlos bien) para dejar un proyecto antiguo en regla.

## Dónde está en el repo
- `.claude/skills/adopta`, `adoptar-indice-existente`, `acorta`, `trocea`; spec 020

## Fuente
- Petición de Darwin (2026-11-04), specs 015, 017 y 018

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-11-04)
