---
name: guardar-respuesta
description: Use when Darwin types /guardar-respuesta, says "guarda esta respuesta" or "apunta esto", or an answer or comparison in the chat is worth keeping even though no error produced it.
---

# /guardar-respuesta — que una buena respuesta no se pierda con el chat

Las lecciones solo nacen de un problema resuelto. Una explicación o comparación útil (por qué se eligió algo, qué diferencia hay entre dos opciones) se perdía al cerrar el chat. Esta skill la archiva en `.brain/respuestas/` con su fuente (spec 045).

## Cómo (pasos)
1. Decidir qué se guarda: la respuesta **resumida** (tope 8 KB), sin rodeos, que se entienda sin releer el chat. Si Darwin dijo «guarda esta», guardar esa; no inventar otra.
2. Un título corto y la fuente (chat y número, documento o enlace de donde sale).
3. Lanzar: `python .brain/guardianes/respuestas.py --titulo "TÍTULO" --fuente "FUENTE" "texto"`. Con texto largo o con tildes: pasarlo por la entrada estándar con `-` (`... --fuente "FUENTE" -`) o escribir el archivo con Write y lanzar `--indice`. No usar un heredoc de Python para el texto.
4. Contar a Darwin en una línea qué se guardó y dónde. Antes de volver a preguntar algo, mirar `.brain/respuestas/indice.md`.

## Error que evita (caso real)
- Una comparación útil de un chat quedaba solo en ese chat: las lecciones no la recogían porque no venía de un fallo (idea del pendiente 45).

## Dónde está en el repo
- `.brain/guardianes/respuestas.py`, `.brain/respuestas/`, spec 045 del pendiente (idea del gist «LLM Wiki»).

## Fuente
- Pendiente 45 (idea del gist «LLM Wiki», Karpathy, 2026-11-12)

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-11-13)
