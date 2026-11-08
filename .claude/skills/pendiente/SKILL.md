---
name: pendiente
description: Use when Darwin types /pendiente or asks to see a list of what is missing (to program, to test, his own actions, open specs).
---

# Ver un pendiente

## Cómo (pasos)
1. Si Darwin escribió el nombre (`/pendiente programar`, `prueba`, `acciones`, `spec`), ir directo a esa lista. Si no, preguntar con un menú de cuatro opciones: Falta programar, Esperando tu prueba, Acciones tuyas, Specs abiertas.
2. Leer solo esa parte: la sección de `.brain/pendientes.md`, o la cabecera «Estado» de cada spec en `.brain/specs/` que no esté hecha.
3. «Falta programar» y «Specs abiertas»: cada punto en una línea llana con su número.
4. «Esperando tu prueba» y «Acciones tuyas» (lo que le toca hacer a Darwin): por cada punto, descripción completa con **qué es** (qué se hizo o qué se pide y por qué), **qué tienes que hacer** (pasos concretos, en orden, con el comando o la pantalla) y **qué debe pasar si va bien** (y qué avisar si no). Si el punto cita una spec, leer solo su sección de verificación para completar los pasos.
5. No escribir nada ni empezar ninguno.

## Error que evita (caso real)
- Abrir todos los archivos para enseñar una sola lista: gasta tokens.

## Dónde está en el repo
- `.claude/skills/pendiente`, spec 006.

## Fuente
- Spec 006

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-11-01)
