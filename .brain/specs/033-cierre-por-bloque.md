# Spec 033: cierre por bloque de trabajo, no por tarea pequeña

- **Estado:** pedida por Darwin el 2026-11-08 (propuesta 1 del informe 032) y programada en 1.29.0
- **Origen:** informe 032: cerebro-vivo cierra 7,3 veces por chat (Modelo 2: 2,4; LoboHook: 1,1). Cada aviso del guardián obliga a una llamada extra que relee todo el contexto. Los avisos de registro cuestan el 2,1-2,5 % del coste.
- **Aclaración de Darwin:** Claude Code compacta el contexto a unos 950.000 tokens; un chat de 200-300k está muy lejos. Pero un chat que se cierra, se cae o se abandona pierde lo no anotado: el cierre por bloque no elimina el cierre, lo agrupa.

## 1. En alcance
- [x] `cierre.py`: nueva función `ediciones_sin_cerrar` (cuenta, en todo el chat, los archivos del proyecto no ignorados editados con Edit/Write desde la última vez que se tocó el registro o se lanzó `cerrar.py`).
- [x] `evaluar`: con `cierre_por_bloque` activo (por defecto sí) y menos de `cierre_bloque_max_ediciones` (15) ediciones sin cerrar, **no** pide la línea de registro todavía. Al llegar a 15, la pide como siempre. El aviso del tope de `pendientes.md` no cambia.
- [x] `guardianes.json`: claves `cierre_por_bloque` y `cierre_bloque_max_ediciones`. Con `cierre_por_bloque: false` el guardián vuelve a pedir la línea en cada respuesta.
- [x] Sin dato del chat (no se puede leer) el comportamiento es el de antes.
- [x] El cierre ligero automático (spec 002: tarea pequeña, pruebas en verde, sin llamada extra de la IA) no cambia.
- [x] Skill `cerrar-una-tarea` (es/en) y `CLAUDE.md`: se cierra al acabar un bloque (un tema completo con pruebas en verde), y **siempre** antes de abrir un chat nuevo, escribir un traspaso o pasar a otra IA (`traspaso-in/out` ya lo exigen).
- [x] Pruebas en `tests/test_cerebro_indices.py` (5 de `evaluar` y 1 de `ediciones_sin_cerrar`).

## 2. Fuera de alcance
- Cambiar los textos de aviso (la regla ya está en la skill).
- Que el guardián cierre solo al llegar a un número de turnos o minutos; solo cuentan ediciones.
- Ediciones hechas con la terminal (no con Edit/Write): no suman al contador; el chat solo de terminal pide la línea como antes (spec 031).

## 3. Riesgo asumido
Si el chat muere con un bloque abierto (hasta 14 archivos editados sin línea), esa línea se pierde; el código y los commits no. Se acepta frente al ahorro; el tope de 15 se puede bajar en `guardianes.json`.

## 4. Archivos
`cierre.py`, `guardianes.json`, `textos.py` (sin cambios), `cerrar-una-tarea/SKILL.md` y `.en.md`, `CLAUDE.md`, `tests/test_cerebro_indices.py`, `VERSION`, `CAMBIOS.md`, `manifiesto.json`.

## 5. Verificación
- `python -m unittest discover tests` en verde.
- Medir en 2 semanas con `medir.py --ritual`: cierres por chat de cerebro-vivo por debajo de ~3 y coste de avisos de registro por debajo de 1 %.
