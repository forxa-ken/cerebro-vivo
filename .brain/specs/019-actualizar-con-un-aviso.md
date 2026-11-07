# Spec 019: aviso de versión nueva y /actualizar

- **Estado:** implementada (arnés 1.17.0)
- **Fecha:** 2026-11-04

## 1. Objetivo
Que actualizar un proyecto sea: ver el aviso al abrir el chat, escribir `/actualizar` y listo. Antes había que lanzar comandos largos, recordar `--simular`, y los pasos de después (fichas de skills, claves de configuración) se olvidaban y dejaban pruebas rojas (un proyecto 9 versiones atrasado).

## 2. En alcance
- [x] El arranque avisa en una línea si el repo del arnés (`arnes_repo`, carpeta local) tiene una versión mayor que la instalada. Sin red; se apaga con `aviso_arnes_activo`.
- [x] El actualizador ya no solo propone: añade a `guardianes.json` las claves que faltan (sin cambiar las que ya hay), anota `arnes_repo` si falta, y añade a `.brain/experiencia/indice.md` las filas de las skills nuevas.
- [x] Skill `actualizar` (simular, contar en llano, pedir el sí, aplicar, informar).
- [x] Dos pruebas del kit que daban rojo en proyectos con guardianes propios o sin manifiesto: solo corren en el repo del arnés.

## 3. Fuera de alcance
- No actualiza solo sin el sí de Darwin. No toca datos del proyecto. No baja el arnés por internet en el aviso (con dirección git `/actualizar` sí clona, como siempre).

## 4. Verificación
- `python -m unittest discover tests` en verde. Probado de verdad en un proyecto real con 9 versiones de retraso y sin `arnes_repo`.

## 5. Cierre
- [x] Aprobada por Darwin ("necesito que arreglemos esto…", 2026-11-04) · [x] Línea en `decisions.log`
