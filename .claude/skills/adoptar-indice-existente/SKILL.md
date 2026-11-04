---
name: adoptar-indice-existente
description: Use when pending item says to adapt what the project already had (CLAUDE.md, GEMINI.md or AGENTS.md) to the .brain memory, or Darwin says "adopta el índice existente".
---

# Adoptar el índice que el proyecto ya tenía

El instalador del kit no pisa nada: añadió un bloque de memoria al final del índice (entre `<!-- cerebro-vivo:inicio -->` y `<!-- cerebro-vivo:fin -->`) y guardó una copia íntegra del original en `.brain/archive/adoptado/NOMBRE.original.md`. Esta skill reparte ese contenido en su sitio **sin perder nada**.

## Cómo (pasos)
1. Leer la copia en `.brain/archive/adoptado/` (el original, no el índice ya fusionado). Si hay varias (CLAUDE, GEMINI, AGENTS), leer todas y unir lo repetido.
2. Clasificar cada bloque del original y proponer dónde va:
   - objetivo, descripción, público → `.brain/architecture/objetivo.md`
   - reglas, prohibiciones, estilo → `.brain/constitution.md`
   - decisiones con su porqué → `.brain/decisions/` (y una línea en `decisions/indice.md`)
   - mapa de archivos, comandos, entorno → `.brain/referencias.md`
   - tareas abiertas → `.brain/pendientes.md` (solo lo que falta)
3. **Enseñar a Darwin el reparto** (tabla corta: «esto → aquí») en lenguaje llano y esperar su visto bueno. No escribir nada antes.
4. Con el visto bueno: copiar cada bloque a su archivo **tal cual**, sin resumir ni reescribir lo que no encaje; lo dudoso va a `referencias.md`. Nunca descartar.
5. Solo si Darwin lo aprueba aparte (atajo `/acorta`): acortar el índice original a un índice (lo que ya está repartido se sustituye por el enlace al archivo donde quedó). La copia de `.brain/archive/adoptado/` se queda siempre (mover, no borrar).
6. Quitar la tarea de `.brain/pendientes.md` y cerrar con la línea en `decisions.log`.

## Reglas
- Contradicciones entre el original y el método: no resolverlas; listarlas a Darwin.
- Si falta la copia en `adoptado/`, usar `NOMBRE.antes-de-cerebro-vivo` (copia de seguridad del instalador).

## Error que evita (caso real)
- Instalar el kit sobre un proyecto con su propio `CLAUDE.md` y perder (o ignorar) lo que ya estaba escrito ahí: reglas, decisiones y mapa del proyecto.

## Dónde está en el repo
- `.brain/biblioteca/kit-arranque/instalar.py` (`fusionar_indice`, `fusionar_ajustes`), spec 015

## Fuente
- spec 015

## Usada
- Veces: 0 · Última: — (creada el 2026-11-04, spec 015)
