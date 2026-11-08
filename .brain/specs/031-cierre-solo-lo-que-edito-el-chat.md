# Spec 031: el aviso de cierre solo cuenta lo que el chat editó

- **Estado:** aprobada por Darwin el 2026-11-08 y programada en 1.28.6
- **Fecha:** 2026-11-08
- **Versión prevista:** arnés 1.28.6
- **Origen:** punto 33 de pendientes. En Modelo 2, tras `/actualizar`, un chat auxiliar solo editó `guardianes.json` (carpeta `.brain/`, ignorada por el guardián) y `cierre.py` le pidió una línea de registro por `tests/test_eventos_chat.py`, que había traído el actualizador, no el chat. Salió dos veces.

## 1. Causa
`cierre.py` mira `git status` entero. Si el chat editó cualquier cosa (aunque sea un archivo ignorado) y hay cambios sin commitear de otro origen (el actualizador, otro chat), los atribuye al chat y pide la línea.

## 2. En alcance
- [x] En `evaluar` (y `main`): si se sabe qué archivos editó el chat con Edit/Write (ya lo da `detalle_respuesta`), solo cuentan los cambios de git que estén en esa lista. Si ninguno de los archivos editados es del proyecto (todos ignorados), no se pide línea.
- [x] Si el chat no hizo ninguna edición con Edit/Write (trabajó con la terminal), se mantiene el comportamiento de hoy (vale lo que git ve cambiado), para no dejar de avisar de lo escrito con scripts.
- [x] Pruebas: chat que solo edita un archivo de `.brain/` con un cambio ajeno en git → sin aviso; chat que edita un archivo del proyecto → avisa; chat solo de terminal con cambios en git → avisa como antes.

## 3. Fuera de alcance
- Un chat que mezcla ediciones con Edit y escritura con la terminal: lo escrito con la terminal puede no avisarse. Se acepta y se documenta.
- Cambiar los textos de aviso.

## 4. Archivos
`cierre.py`, `tests/test_cerebro_indices.py` (donde ya se prueba `evaluar`), `VERSION`, `CAMBIOS.md`, `manifiesto.json`.

## 5. Verificación
- `python -m unittest discover tests` en verde.
- Darwin: tras `/actualizar` en un proyecto, un chat que solo toque `.brain/` no pide línea de registro por los archivos que trajo el actualizador.

## 6. Cierre
- [x] Spec aprobada por Darwin antes de programar
- [x] Línea en `decisions.log`
- [x] Punto 33 de pendientes pasa a «Esperando tu prueba»
