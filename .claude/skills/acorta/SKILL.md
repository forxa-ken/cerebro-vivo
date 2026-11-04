---
name: acorta
description: Use when Darwin types /acorta, says "sí, acorta", or an AI index (CLAUDE.md, GEMINI.md, AGENTS.md) is over its size cap after adopting or reviewing.
---

# /acorta — bajar los índices al tope

Lleva `CLAUDE.md`, `GEMINI.md` y `AGENTS.md` al tope de `tope_claude_md_bytes` (5 KB en `guardianes.json`) cambiando bloques pesados por un enlace. Nada se pierde: el texto ya está o se copia antes en `.brain/`.

## Cómo (pasos)
1. Medir: `python .brain/guardianes/revisar_indices.py --json`. Ver el tamaño de cada índice y sus secciones pesadas.
2. Para cada sección pesada, comprobar que su texto **ya está** en `.brain/` (p. ej. `referencias.md` tras `/adopta`, o `.brain/archive/adoptado/`). Si no está, copiarlo tal cual a `.brain/referencias.md` (o `.brain/architecture/`) **antes** de tocar el índice.
3. **Enseñar a Darwin**, en llano y antes de escribir: tabla «sección (KB) → enlace donde queda» y el tamaño que tendrá cada índice. Esperar su sí.
4. Con el sí: sustituir cada sección por una línea con su enlace. Dejar los tres índices sincronizados. Lo que no encaje se deja y se avisa.
5. Volver a medir. Si sigue sobre el tope, decirlo y proponer qué más mover; no forzar.
6. Pruebas en verde y línea en `decisions.log`.

## Error que evita (caso real)
- Dejar un `CLAUDE.md` de 49-52 KB tras adoptar (diez veces el tope) porque nadie lo acortó; o acortarlo borrando texto que no estaba copiado en otro sitio.

## Dónde está en el repo
- `.brain/guardianes/revisar_indices.py`, spec 017

## Fuente
- spec 017 (petición de Darwin, 2026-11-04)

## Usada
- Veces: 0 · Última: — (creada el 2026-11-04)
