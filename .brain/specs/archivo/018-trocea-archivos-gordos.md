# Spec 018: /trocea — dividir los archivos de memoria gordos

- **Estado:** implementada (arnés 1.16.0)
- **Fecha:** 2026-11-04

## 1. Objetivo
Tras `/adopta` y `/acorta`, el texto del índice viejo queda en `referencias.md` (47 KB en Guild Control Forever) y la IA lo abre entero. Poner tope a los archivos de lectura de `.brain/` y una skill que los divida por tema.

## 2. En alcance
- [x] Guardián `archivos_gordos.py` (solo lectura), tope `tope_archivo_memoria_bytes` = 8 KB, aviso al 80 % en el arranque.
- [x] Skill `trocea` (tabla a Darwin, copia íntegra en `archive/troceado/`, índice en `architecture/`). Prueba `test_archivos_gordos.py`.

## 3. Fuera de alcance
- No toca índices de IA, pendientes, registro, specs ni archive. No resume ni borra.

## 4. Verificación
- `python -m unittest discover tests` en verde. `/trocea` sobre el `referencias.md` real de GCF: sin probar.

## 5. Cierre
- [x] Aprobada por Darwin ("si", 2026-11-04) · [x] Línea en `decisions.log`
