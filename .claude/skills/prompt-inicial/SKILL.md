---
name: prompt-inicial
description: Use when Darwin wants to start a project or task with a complete prompt, or types /prompt-inicial.
---

# Prompt inicial (plantilla opcional)

Solo sirve para escribir un encargo. Para ver el estado está `/resumen`; para ver una lista, `/pendiente`.

## Cómo (pasos)
1. Preguntar el tipo: proyecto nuevo, arreglar un fallo, añadir una función, revisión o investigar; y el modo: rápido (objetivo, cómo sabré que está bien, qué NO quiero) o completo.
2. Campos, todos opcionales (lo vacío se omite): objetivo y para quién; cómo sabré que está bien; qué NO quiero; material que existe; cómo trabajar (SDD o rápido, auto o paso a paso); plazos; costes (IA o coste cero); idioma y tono; qué debe probar él; dudas abiertas.
3. Avisar sin bloquear: falta el objetivo o el criterio de «hecho»; un fallo sin ejemplo; un proyecto nuevo sin límites; si lo pedido es muy grande, sugerir dividirlo en chats o specs.
4. Armar el prompt solo con lo rellenado, enseñarlo y esperar su visto bueno antes de actuar. Si no hay dudas abiertas, añadir «pregúntame antes de inventar».
5. Si pide la versión para Gemini/Codex, escribir la plantilla en blanco como `.md` (`.brain/biblioteca/PLANTILLA_PROMPT_INICIAL.md`).

## Error que evita (caso real)
- Empezar a programar con un encargo a medias: sin criterio de «hecho» ni límites, la IA inventa y hay que rehacer.

## Dónde está en el repo
- Spec 084 y D-075; separada de `/resumen` y `/pendiente` en la spec 006.

## Fuente
- D-075, spec 084 (punto 81)

## Usada
- Veces: 1 · Última: 2026-11-01 (creada el 2026-11-01)
