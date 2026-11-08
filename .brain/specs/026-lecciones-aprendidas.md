# Spec 026: lecciones apuntadas en el momento y traspaso corto

- **Estado:** implementada (1.24.0; falta la prueba de Darwin en Modelo 2)
- **Fecha:** 2026-11-07

## 1. Objetivo
En Modelo 2, cada vídeo trae problemas que se resuelven, pero la lección se pierde si nadie la apunta (existe `.brain/lecciones_video.md`, pero depende de acordarse). Regla de Darwin: **no se deja al humano ni a la IA**. Dos partes que se complementan:
- **A.** La lección se apunta en el momento en que ocurre el hito, forzado por un guardián; el traspaso solo verifica.
- **B.** El traspaso que carga el chat nuevo es corto (lo último tratado); el historial completo queda archivado y se consulta con una skill.

## 2. Parte A: lecciones en el momento
1. **Carpeta `.brain/lecciones/`**: un archivo por tema (`video.md`…) con líneas problema → causa → regla, más `indice.md`. `lecciones_video.md` de Modelo 2 pasa a `lecciones/video.md` sin perder nada.
2. **Guardián de hitos** (`hitos.py`, lo llama `cierre.py` en el hook Stop con el registro del chat): detecta señales desde la última lección:
   - un error de herramienta que después se resolvió (mismo comando fallido y luego correcto);
   - cambios en archivos que el proyecto marca como delicados (`lecciones_vigiladas` en `guardianes.json`: tema → patrones; en Modelo 2, el lanzador del vídeo y las fichas);
   - una modificación grande (`hitos_max_archivos`, por defecto 5).
3. **Con un hito sin resolver, devuelve exit 2**: no deja dar la tarea por cerrada hasta que haya una lección nueva o un «sin lección: motivo». Una sola vez por hito (estado por chat, como el aviso de longitud).
4. **`/leccion`** (skill y `lecciones.py --tema T "problema | causa | regla"`) escribe la lección en el sitio y formato correctos, actualiza el índice y evita duplicados. `/leccion ninguna "motivo"` cierra un hito sin lección.
5. **Al hacer el traspaso, solo se verifica:** `cierre.py` no deja pasar si queda un hito sin resolver. Sin hitos pendientes, pasa.
6. El resumen de arranque lista los temas con lecciones y cuántas reglas tienen. Los archivos de lecciones entran en el tope de tamaño (`/trocea`).

## 3. Parte B: traspaso corto
1. **`.brain/traspaso.md` (corto, ~1500 caracteres):** lo último que pidió Darwin, lo que espera su respuesta, el siguiente paso, lo que NO hay que hacer y si queda algo sin subir. Es lo único que carga el chat nuevo.
2. **Historial completo:** se escribe aparte en `.brain/archive/traspasos/AAAA-MM-DD-HHMMSS-completo.md` (plantilla actual), siempre disponible.
3. **Skill `/memoria-traspaso`:** trae y resume en llano el historial completo del chat anterior; con un número, uno más antiguo.
4. `PLANTILLA_TRASPASO.md` pasa a tener las dos plantillas; el arranque muestra solo el corto y la ruta del completo. «NO hacer» y «sin subir» nunca salen del corto.

## 4. Fuera de alcance
- Detectar sin señal alguna un problema que se resolvió sin dejar rastro, y redactar la lección sin la IA: la IA redacta, el guardián solo obliga a parar.
- Fase 3 de la spec 024.

## 5. Plan
1. `lecciones.py` y `hitos.py` con pruebas (error resuelto, archivo vigilado, modificación grande, «sin lección», sin duplicados, una vez por hito).
2. Enganche en `cierre.py` y `arranque.py`; ajustes `lecciones_activas`, `lecciones_vigiladas`, `hitos_max_archivos`.
3. Traspaso corto/completo en plantilla, `traspaso-in`/`traspaso-out`, `guardar_traspaso.py` y `arranque.py`; skills `/leccion` y `/memoria-traspaso`; regla en la plantilla de los índices; textos es/en.
4. Versión 1.24.0, `CAMBIOS.md`, manifiesto; mover `lecciones_video.md` de Modelo 2 al actualizar.

## 6. Verificación
- `python -m unittest discover tests` en verde.
- Darwin: en Modelo 2, provocar un error que se resuelva y ver que pide la lección; en el traspaso, ver que carga solo lo corto y que `/memoria-traspaso` trae el resto.

## 7. Cierre
- [x] Spec aprobada por Darwin antes de programar
- [x] Línea añadida a `.brain/decisions.log`
