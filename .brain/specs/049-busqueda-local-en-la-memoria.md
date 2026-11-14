# Spec 049: búsqueda local sobre `.brain/` (pendiente 46)

- **Estado:** aprobada por Darwin y programada el 2026-11-14 en el arnés 1.51.0 (594 pruebas en verde); sin probar por Darwin
- **Fecha:** 2026-11-14
- **Origen:** idea del gist «LLM Wiki» de Karpathy (búsqueda sobre la memoria). El pendiente decía «dejar para cuando la memoria crezca más». Hoy `.brain/` (sin `archive/`) son ~125 archivos y ~470 KB: aún se puede leer entera en un instante, así que **la primera versión no necesita índice ni base de datos**.
- **Es del arnés:** vale para cualquier proyecto con `.brain/`. Nada de lo que se reparte nombra proyectos concretos.

## 1. Objetivo
Que la IA (y Darwin) encuentre en segundos qué dice la memoria sobre un tema —lecciones, decisiones, specs, respuestas guardadas— **sin leer carpetas enteras** y sin gastar tokens en abrir archivos que no tienen nada que ver.

## 2. Decisión de diseño (a confirmar)
- **Un solo script, `buscar.py`**, solo lectura y librería estándar. Recorre `.brain/**/*.md` y `decisions.log` en cada consulta (470 KB tardan milisegundos); **sin índice que se quede viejo**.
- Busca por palabras sueltas, **sin distinguir mayúsculas ni tildes** («leccion» encuentra «lección»), y puntúa: más peso si la palabra está en el título o en un encabezado, y más si salen varias palabras de la consulta en el mismo archivo.
- Devuelve los **N mejores archivos** (10 por defecto) con ruta, título y 1 a 2 líneas con la palabra (`ruta:línea`), para que la IA abra solo lo que toca.
- `archive/` queda fuera por defecto (es historia); `--archivo` lo incluye. `--solo lecciones|decisiones|specs|respuestas` limita la carpeta.
- Salida legible y `--json`. Textos en `textos.py` es/en.
- **Skill `buscar-en-la-memoria`** (es/en): antes de volver a investigar, preguntar a la memoria con `buscar.py`; si no aparece nada, entonces investigar. Complementa el índice de respuestas (spec 045) y las lecciones.
- **Crecer después, no ahora:** si la memoria pasa de ~5 MB o la búsqueda tarda más de 1 segundo, se añade un índice invertido en caché. Queda anotado como umbral, no se construye.

## 3. En alcance
- [ ] `buscar.py` con consulta, `--max`, `--solo`, `--archivo`, `--json`.
- [ ] Normalización sin tildes y puntuación (título, encabezados, varias palabras).
- [ ] Textos es/en en `textos.py`; skill `buscar-en-la-memoria` y su `.en.md`; fila en `experiencia/indice.md`.
- [ ] Una línea en `CEREBRO_VIVO.md` y `.en.md` (y el kit de instalación: `GUARDIANES` en `instalar.py`).
- [ ] Pruebas con una carpeta `.brain/` de juguete (sin tildes, título pesa más, `archive` excluido, `--solo`, consulta vacía, sin resultados).
- [ ] `VERSION`, `CAMBIOS.md`, `manifiesto.json`.

## 4. Fuera de alcance
- Índice, base de datos, embeddings o IA dentro del script.
- Buscar en el código del proyecto (para eso están `grep` y el editor).
- Modificar nada: solo lee.
- Aviso automático en el arranque: no hace falta; es una herramienta que se usa a demanda.

## 5. Riesgos
- Puntuación simple: puede subir un archivo poco útil. Mitigación: enseña las líneas encontradas para juzgar de un vistazo y el máximo es corto.
- Que la IA no la use y siga leyendo carpetas enteras. Mitigación: la skill y una línea en el manual; se mide con `medir.py --skills` si hace falta.
- Crecimiento de la memoria: umbral explícito (5 MB o 1 s) para pasar a índice.

## 6. Archivos
`buscar.py` (nuevo), `textos.py`, `instalar.py` (`GUARDIANES`), skill `buscar-en-la-memoria` (es/en), `experiencia/indice.md`, `CEREBRO_VIVO.md` y `.en.md`, `tests/test_buscar.py`, `VERSION`, `CAMBIOS.md`, `manifiesto.json`.

## 7. Verificación
`python -m unittest discover tests` en verde; pasada real con 3 o 4 preguntas sobre este repo («tope de bytes», «heredoc», «hermanos») para ver que lo primero que sale es lo esperado. **No probado hasta hacerla.**
