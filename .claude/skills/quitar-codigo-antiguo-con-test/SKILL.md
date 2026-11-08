---
name: quitar-codigo-antiguo-con-test
description: Use when removing an old function, window or feature.
---

# Quitar codigo antiguo con test

## Cómo (pasos)
1. Buscar todas las referencias (`Grep`) antes de borrar: funciones, `window.x = x`, tests y textos.
2. Borrar solo lo que nadie llama; anotar lo que queda sin uso para una limpieza futura.
3. Cambiar el test que exigía su existencia por uno que exija su ausencia (`assertNotIn`).
4. Pasar la suite completa y pedir a Darwin que pruebe los botones afectados.

## Error que evita (caso real)
- Las ventanas antiguas del panel de dev quedaron como respaldo hasta que Darwin lo dijo.

## Dónde está en el repo
- `static/js/app.js`, `tests/test_admin_page.py`

## Fuente
- #68, punto 000b, spec 028

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-10-31, spec 079)
