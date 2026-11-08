---
name: leccion
description: Use when Darwin types /leccion, or the hitos guardian blocks closing a task because a problem was solved or a delicate file changed.
---

# /leccion — apuntar la lección en el momento

La lección se apunta cuando ocurre el hito, no al final ni «si nos acordamos». El guardián `hitos.py` (hook Stop) no deja cerrar la tarea hasta que hay una lección nueva o un «sin lección».

## Cómo (pasos)
1. Decidir el tema (`video`, `metodo`…; el que ya exista en `.brain/lecciones/indice.md` si encaja).
2. Con lección: `python .brain/guardianes/lecciones.py --tema TEMA "problema | causa | regla"`. Una frase por parte; la regla debe poder aplicarse la próxima vez sin releer el chat. Si ya estaba escrita, lo dice y no la duplica.
3. Sin lección (cambio cosmético, error sin nada que aprender): `python .brain/guardianes/lecciones.py ninguna "motivo"`. El motivo es obligatorio.
4. Contar a Darwin en una línea qué se apuntó. Antes de repetir un trabajo de un tema, leer `.brain/lecciones/TEMA.md`.

## Error que evita (caso real)
- En Modelo 2 cada vídeo resolvía problemas y la lección se perdía porque dependía de acordarse (spec 026).

## Dónde está en el repo
- `.brain/guardianes/lecciones.py`, `hitos.py`, `.brain/lecciones/`, spec 026.

## Fuente
- Spec 026

## Usada
- Veces: 0 · Última: — (creada el 2026-11-07)
