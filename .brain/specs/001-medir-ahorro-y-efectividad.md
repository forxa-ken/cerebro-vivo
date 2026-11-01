# Spec 001: Demostrar que el arnés ahorra tokens y mejora el trabajo

- **Estado:** aprobada (Darwin, 2026-11-01); parte B y parte A ejecutadas; resultados en `001-resultados.md`
- **Fecha:** 2026-11-01

## 1. Objetivo
Probar con números, no con impresiones, dos cosas: (1) el arnés gasta menos tokens por tarea; (2) el trabajo sale más efectivo (menos repeticiones, menos vueltas). Darwin eligió **A + B**: un medidor reutilizable en cualquier proyecto (B) y una prueba de carpetas gemelas con 3 tareas pequeñas para calibrar y refinar (A).

## 2. En alcance
**Parte B — medidor (`.brain/guardianes/medir.py`, solo lectura, librería estándar)**
- [ ] Lee los registros de Claude Code de cualquier proyecto (reutiliza la lógica de `uso_tokens.py`; no se toca el de LoboHook).
- [ ] Por chat saca: tokens nuevos, salida, coste de arranque, mensajes, **mensajes del usuario** (proxy de «turnos hasta cerrar») y **correcciones** (mensajes del usuario que empiezan con «no», «otra vez», «te dije», «repite»… lista editable).
- [x] `--comparar RUTA_CON RUTA_SIN` compara las medias de dos proyectos (carpetas gemelas) y da la diferencia en % (sustituye a la idea de etiquetas, más simple).
- [ ] Salida en lenguaje llano, una tabla corta.
- [ ] Entra en `manifiesto.json` (sube `VERSION`, `CAMBIOS.md`) y tiene pruebas.

**Parte A — carpetas gemelas (calibración)**
- [ ] 3 tareas pequeñas, repetibles y con un criterio objetivo de «hecha» (una prueba que pasa o falla). Propuesta:
  1. Añadir una opción nueva a un script pequeño ya existente (cambio de 1 archivo + prueba).
  2. Arreglar un fallo sembrado a propósito (la prueba falla al inicio).
  3. Retomar trabajo tras un «chat cortado»: continuar una tarea a medias usando solo lo que quedó anotado (mide el valor de la memoria entre chats).
- [ ] Un proyecto de juguete en `bench/` (fuera del manifiesto), copiado a dos carpetas gemelas: **CON** (arnés instalado con `instalar.py`) y **SIN** (mismo código, sin `.brain/`, solo un `CLAUDE.md` mínimo).
- [ ] Mismo prompt, mismo modelo, mismo esfuerzo en ambas; cada ejecución en un chat nuevo; se repite 2 veces por tarea/lado para ver el ruido (12 ejecuciones en total).
- [ ] Se compara con `medir.py`: tokens nuevos, salida, turnos, correcciones y si la prueba final pasa.
- [ ] Con lo que salga se anotan mejoras concretas del arnés (p. ej. arranque demasiado grande) como pendientes.

## 3. Fuera de alcance
- No tocar `F:\Proyectos Antigravity\LoboHook` (solo se leen sus registros como ejemplo); no adoptar el arnés allí.
- No subir nada a GitHub sin orden de Darwin. No borrar nada.
- No cambiar el arnés mientras dura la prueba A (se refina después, y se vuelve a medir).

## 4. Plan de implementación
1. Escribir `medir.py` + pruebas (parte B), probarlo contra los registros reales de LoboHook (solo lectura).
2. Crear `bench/` con el proyecto de juguete, las 3 tareas y sus pruebas de «hecha».
3. Montar las carpetas gemelas CON/SIN.
4. Ejecutar las 12 pruebas (chats nuevos separados) y medir.
5. Informe corto a Darwin en `.brain/specs/001-resultados.md`: tabla CON vs SIN, qué se ahorra, qué falla, qué se refina.

## 5. Plan de verificación
- `python -m unittest discover tests` en verde.
- `medir.py` sobre LoboHook da totales iguales a los de `uso_tokens.py` (control cruzado).
- Cada tarea tiene prueba automática de «hecha»; no se cuenta como lograda sin ella.

## 6. Límites honestos (se dicen de antemano)
- 2 repeticiones por caso es muestra pequeña: servirá para **calibrar y ver tendencia**, no para una prueba estadística definitiva. Para eso hace falta el medidor B en proyectos reales durante semanas.
- LoboHook no tiene chats «sin arnés» (los registros empiezan el 25-oct, con el arnés ya puesto), así que no hay comparación histórica posible; por eso la prueba A.
- Las ejecuciones gastan uso real (estimación: unos 100-300k tokens nuevos por ejecución con arnés; ~12 ejecuciones). Darwin debe aprobar ese gasto.
- «Correcciones» se detecta por palabras; es un indicador aproximado.

## 7. Cierre
- [x] Spec aprobada por Darwin antes de programar
- [ ] Línea añadida a `.brain/decisions.log`

## 8. Cómo quedó preparada la parte A (2026-11-01)
- `bench/` (en el repo, fuera del manifiesto): proyecto de juguete `base/`, las 3 tareas (`tareas.md`), `montar.py`, `verificar.py` y las pruebas ocultas de «hecha» en `hechas/`.
- Las carpetas gemelas se crean **fuera del repo**, en `F:\Proyectos Antigravity\bench-cerebro\con_arnes` y `sin_arnes` (dentro del repo, el `CLAUDE.md` de cerebro-vivo contaminaría el lado SIN; «con» a secas no sirve como nombre en Windows). Lo que hubiera se mueve a `_historial/`, no se borra.
- Cada lado mezcla sus 6 chats (3 tareas × 2); el título del chat empieza por `[T1]`, `[T2]`, `[T3]` para separarlos.
- T3: CON recibe un traspaso con el formato acordado (céntimos enteros, minúsculas, orden); SIN solo tiene el código a medias. La prueba oculta exige ese formato.
- Comprobado: el punto de partida falla las 3 pruebas ocultas y una solución de referencia las pasa las 3.
