---
name: trocea
description: Use when Darwin types /trocea, or the arranque warns that a .brain/ file (referencias.md, architecture/…) is over its size cap.
---

# /trocea — dividir un archivo de memoria gordo por temas

Divide un archivo de `.brain/` que pasa de `tope_archivo_memoria_bytes` (8 KB) en archivos pequeños **con nombre de tema** y un índice. Nada se pierde ni se resume: se corta por los títulos que ya tiene.

## Cómo (pasos)
1. Listar los gordos: `python .brain/guardianes/archivos_gordos.py`.
2. Para cada uno, leerlo y proponer los cortes por sus títulos (`##`): un archivo por tema en `.brain/architecture/` con nombre claro (`loot.md`, `roster.md`), nunca `parte-2.md`. Lo transversal (comandos, entorno, mapa de archivos) se queda en `referencias.md`. Un tema aún gordo se divide en subtemas con nombre (`loot-reparto.md`).
3. **Enseñar a Darwin**, en llano y antes de escribir: tabla «sección (KB) → archivo nuevo» y el tamaño que quedará. Esperar su sí.
4. Con el sí: guardar la copia íntegra del original en `.brain/archive/troceado/AAAA-MM-DD-NOMBRE.md`; copiar cada sección **tal cual** a su archivo; crear/actualizar `.brain/architecture/indice.md` (una línea por archivo) y dejar en el original solo lo transversal y una línea que apunta al índice. Enlazar el índice desde el CLAUDE.md.
5. Comprobar que no se perdió texto: el contenido de los trozos juntos coincide con la copia (mismas líneas). Volver a lanzar `archivos_gordos.py`: nada sobre el tope, o decir qué sigue grande.
6. Pruebas en verde y línea en `decisions.log`.

## Error que evita (caso real)
- Tras adoptar un proyecto antiguo, `referencias.md` quedó con 47 KB: acortar el CLAUDE.md solo movió el problema y la IA seguía abriendo un archivo enorme para tocar un módulo.

## Dónde está en el repo
- `.brain/guardianes/archivos_gordos.py`, spec 018

## Fuente
- spec 018 (petición de Darwin, 2026-11-04)

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-11-04)
