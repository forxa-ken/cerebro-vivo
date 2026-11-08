---
name: memoria-traspaso
description: Use when Darwin types /memoria-traspaso, or you need the full detail of what the previous chat did and the short traspaso is not enough.
---

# /memoria-traspaso — traer el historial completo del chat anterior

El traspaso que carga el chat nuevo es corto. El detalle completo se guarda aparte y se consulta solo cuando hace falta.

## Cómo (pasos)
1. Buscar en `.brain/archive/traspasos/` los archivos `*-completo.md`. Con `/memoria-traspaso` sin número, el más reciente; con un número N, el N-ésimo más antiguo hacia atrás (1 = el último, 2 = el anterior…). Si hay un `.brain/traspaso-completo.md` aún sin archivar, es el más reciente.
2. Leerlo entero y contar a Darwin en llano (viñetas cortas): qué se hizo, decisiones, qué quedó a medias, qué se descartó.
3. Si no hay ninguno, decirlo claro; no inventarlo. No modificar ni mover nada.

## Error que evita (caso real)
- Cargar el traspaso entero en cada chat nuevo gasta contexto aunque casi nunca se necesite el detalle (spec 026).

## Dónde está en el repo
- `.brain/archive/traspasos/`, `biblioteca/PLANTILLA_TRASPASO.md`, `guardianes/arranque.py`, spec 026.

## Fuente
- Spec 026

## Usada
- Veces: 0 · Última: — (creada el 2026-11-07)
