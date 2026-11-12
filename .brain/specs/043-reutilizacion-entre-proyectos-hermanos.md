# Spec 043: reutilización entre proyectos hermanos (genérica, va en el arnés)

- **Estado:** aprobada por Darwin el 2026-11-12; programada el 2026-11-12 en el arnés 1.43.0 (pruebas con repos de juguete en verde; la prueba real a mano sigue pendiente de Darwin)
- **Fecha:** 2026-11-12
- **Origen:** Darwin tiene proyectos que comparten trabajo (el caso que lo motivó: dos versiones de un mismo addon, una para cada edición del juego). Hoy lo que se hace en uno y falta en el otro se anota a mano en un archivo de «portar» de cada proyecto (commit, qué cambia, qué adaptar, qué no portar). Funciona, pero depende de que alguien se acuerde: uno de esos archivos lleva semanas sin tocarse y dice «Pendiente: (nada)». Además solo cubre commits, no lo descubierto.
- **Es del arnés, no de esos dos proyectos:** cualquier proyecto de Darwin con uno o más «hermanos» (mismo origen, distinta variante) puede activarlo. **Nada de lo que se reparte nombra proyectos concretos**; los ejemplos de esta spec no pasan a los archivos del kit (lo vigila `tests/test_arnes_repo.py`).
- **Relación:** se apoya en la spec 042 (`.brain/colaboracion.md`) pero no depende de que esté programada.

## 1. Objetivo
Que ningún proyecto hermano investigue dos veces lo mismo, y que lo pendiente de portar se calcule solo en vez de depender de la memoria de nadie.

## 2. En alcance
- [ ] **Ajuste `proyectos_hermanos`** en `guardianes.json`: lista de `{nombre, ruta, rama, archivo_portar}`. Vacía por defecto (el guardián calla). Cada proyecto pone los suyos; el arnés no trae ninguno.
- [ ] **Guardián `hermanos.py`** (es/en), de solo lectura: para cada hermano configurado, compara con git sus commits con lo que **el archivo de portar de este proyecto** da por portado o «no aplica», y lista los que faltan. No hace `fetch` ni cambia nada; si el hermano no está accesible, calla.
- [ ] **Formato estándar del archivo de portar** (plantilla `biblioteca/PLANTILLA_PORTAR.md`, es/en): «Último portado», «Pendiente», «Hecho», y por entrada: commit, qué cambia, adaptar, no portar. El guardián lee ese formato; un proyecto con otro formato lo ajusta o lo adopta con el procedimiento de la skill.
- [ ] **Aviso al arrancar** (`arranque.py`): una línea «N commits de NOMBRE sin portar» con el cómo arreglarlo. Sin hermanos configurados, no dice nada.
- [ ] **Hallazgos compartidos:** plantilla `biblioteca/PLANTILLA_HALLAZGOS.md` (es/en) para `.brain/hallazgos-compartidos.md`, entradas de formato fijo (qué se descubrió, cómo se comprobó, fecha, proyecto de origen). Regla única, escrita en la plantilla de `colaboracion.md` (spec 042): antes de investigar, mirar el de los hermanos; tras investigar algo útil para varios, anotarlo.
- [ ] **Skill `hermanos`** (es/en): configurar un hermano, adoptar un archivo de portar existente, leer el aviso.
- [ ] Pruebas con dos repositorios de juguete creados en una carpeta temporal.

## 3. Fuera de alcance
- Hacer `git fetch` o `cherry-pick` automáticamente: lo decide una persona o la IA del proyecto con aviso.
- Tocar el código de ningún proyecto.
- Guardar el contenido de los hallazgos en el arnés: pertenece a cada proyecto.
- Dar por sentado que son solo dos: se admiten varios hermanos.

## 4. Riesgos
- Comparar commits entre repositorios distintos puede dar falsos pendientes (cambios solo de una variante). El guardián solo avisa; «no aplica» en el archivo de portar los descarta.
- Leer la carpeta de otro proyecto: solo lectura y solo si Darwin pone la ruta en `guardianes.json`.
- Un archivo de portar con formato propio no se entiende; por eso la skill trae el paso de adoptarlo.

## 5. Archivos
`hermanos.py` (nuevo), `arranque.py`, `guardianes.json`, `textos.py`, skill `hermanos` (es/en), `PLANTILLA_PORTAR` y `PLANTILLA_HALLAZGOS` (es/en), `tests/`, `VERSION`, `CAMBIOS.md`, `manifiesto.json`.

## 6. Verificación
`python -m unittest discover tests` en verde; prueba real a mano con los dos proyectos del addon (solo lectura) para ver que los pendientes que salen son reales. **No probado hasta hacerla.**
