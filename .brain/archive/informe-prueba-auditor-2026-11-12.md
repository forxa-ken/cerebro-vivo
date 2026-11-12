# Prueba de fallos plantados del auditor (spec 044), ronda 1 — 2026-11-12

**Montaje:** proyecto de juguete `caja` (2 módulos y 4 pruebas en verde) con 11 fallos plantados: 4 de calidad (promedio sin lista vacía, `paginar` pierde un elemento, prueba que no comprueba nada, prueba que fija el resultado erróneo), 3 de consumo (espera activa de 1 ms, log entero en memoria, caché sin límite) y 4 de seguridad (inyección SQL, inyección de comandos, token en el código, salida de la carpeta de informes). Clave guardada fuera del proyecto. Misma instrucción para los tres, modo revisión general, solo lectura, esfuerzo medio.

| Auditor | Fallos plantados hallados | Hallazgos totales | Ejecutó comprobaciones | Gasto |
| :--- | :--- | :--- | :--- | :--- |
| Claude Sonnet 5.5 (subagente) | 11 de 11 | 14 | poco (lectura, algo comprobado) | ~66k tokens, 26 s |
| Claude Opus 5.5 (subagente) | 11 de 11 | 16 | sí: reprodujo SQL, rutas, `paginar`, descuento e IVA | ~67k tokens, 45 s |
| Codex `gpt-6-sol` (externo) | 11 de 11 | 11 | **no**: `python` no estaba disponible en su sandbox | ~6k tokens, varios minutos |

**Lectura (sin sobreinterpretar):**
- La prueba **no distingue** entre los tres: los fallos eran demasiado evidentes y todos los hallaron. No sirve aún para decidir modelo ni para medir el sesgo de familia.
- Diferencias reales: Opus fue el único que reprodujo fallos en vez de solo leerlos; Codex no pudo ejecutar nada (hay que arreglar el acceso a `python` en su sandbox antes de usarlo como auditor) y puso el token y `promedio([])` como «baja»; Sonnet y Opus los pusieron más altos. Sonnet y Opus encontraron además extras no plantados (dinero con coma flotante, descuento sin validar, IVA sin validar).
- El gasto de Codex (6k) no es comparable a primera vista con el de los subagentes (66k): cuentan distinto.

**Siguiente ronda propuesta:** fallos sutiles (condición de carrera, comprobar-y-usar sobre un archivo, error solo con ciertas entradas, lógica de negocio con una regla de la spec incumplida) y una spec corta como «requisito» que el código incumple.
