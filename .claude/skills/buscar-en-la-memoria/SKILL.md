---
name: buscar-en-la-memoria
description: Use when you are about to investigate, decide or explain something the project may already have written down (a lesson, decision, spec or saved answer), or Darwin asks "¿ya lo teníamos apuntado?" or "busca en la memoria".
---

# Buscar en la memoria antes de investigar

La memoria del proyecto (`.brain/`) guarda lecciones, decisiones, specs y respuestas. Leer carpetas enteras gasta tokens; esta skill pregunta primero y abre solo lo que toca (spec 049).

## Cómo (pasos)
1. Antes de investigar o de volver a preguntar algo, lanzar: `python .brain/guardianes/buscar.py PALABRAS` (sin tildes da igual; 2 a 4 palabras clave, sin «de», «la»…).
2. Leer la lista: cada archivo trae su título y 1 o 2 líneas con la palabra (`ruta:línea`). **Abrir solo los 1 o 2 primeros** que encajen, y solo la parte que toca.
3. Afinar si hace falta: `--solo lecciones` (o `decisions`, `specs`, `respuestas`), `--max 5`, `--archivo` para buscar también en la historia (`archive/`, fuera por defecto).
4. Si no sale nada útil, entonces investigar. Si lo encontrado ya estaba, usarlo y decirle a Darwin de dónde sale.
5. Si lo que se descubre es útil para otra vez: `/guardar-respuesta` o `/leccion`.

## Error que evita (caso real)
- Volver a investigar algo que una lección o una respuesta guardada ya resolvía, o abrir carpetas enteras de `.brain/` para encontrar una sola frase.

## Dónde está en el repo
- `.brain/guardianes/buscar.py`, spec 049 (pendiente 46, idea del gist «LLM Wiki»)

## Fuente
- spec 049

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-11-14, spec 049)
