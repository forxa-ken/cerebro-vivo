# Spec 037: detectar memoria desactualizada dentro de la higiene de `.brain/` (punto 29)

- **Estado:** borrador (2026-11-11), a aprobar por Darwin antes de programar
- **Origen:** idea del punto 24 (OpenAI, «jardinero de documentación») y informe 028: no es un guardián nuevo, sino la sexta pieza de la higiene de memoria, que hoy está repartida en `poda.py`, `archivos_gordos.py`, `revisar_indices.py`, `indices.py` y las skills `trocea`/`acorta`.

## 1. Decisión pendiente de Darwin
- **A (recomendada, pequeña):** añadir la detección a `revisar_indices.py` (que ya revisa enlaces rotos y fechas viejas), sin fusionar nada todavía.
- **B (grande):** primero fusionar las cinco piezas en un solo guardián de higiene y luego añadir la detección. Es la propuesta del informe 028; toca muchos archivos y los proyectos que ya usan el arnés.

## 2. En alcance (opción A)
- [ ] Detectar en `.brain/` (solo lectura, solo avisa): rutas de archivos citadas que ya no existen, puntos de `pendientes.md` que citan specs/fichas inexistentes, fichas de decisión cuyos archivos cambiaron después (hoy ya lo avisa el arranque) y documentos sin tocar hace más de N días que otros documentos contradicen o dejaron atrás.
- [ ] Una línea en el resumen de arranque solo si hay hallazgos (con todo al día, cuesta 0 tokens).
- [ ] Detalle con `revisar_indices.py --ver`; textos es/en en `textos.py`.
- [ ] Pruebas con una carpeta `.brain/` de ejemplo.

## 3. Fuera de alcance
- Corregir nada solo: la IA propone, Darwin decide (regla «mover, no borrar»).
- La fusión de las cinco piezas (opción B), que sería otra spec.

## 4. Archivos
`revisar_indices.py`, `textos.py`, `guardianes.json`, `tests/`, `VERSION`, `CAMBIOS.md`, `manifiesto.json`.

## 5. Verificación
`python -m unittest discover tests` en verde; pasada real sobre este mismo repo para ver cuántos falsos avisos da (no probada hasta hacerla).
