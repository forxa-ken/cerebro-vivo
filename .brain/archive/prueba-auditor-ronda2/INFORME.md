# Prueba de fallos plantados del auditor, ronda 2 (fallos sutiles) — 2026-11-12

**Montaje:** proyecto `caja` v2 con `REQUISITOS.md` y 11 fallos sutiles (clave en `CLAVE.md`). Misma instrucción para los tres, revisión general, solo lectura, esfuerzo medio.

| Auditor | Hallados (de 11) | Reprodujo ejecutando | Falsos positivos | Gasto |
| :-- | :-: | :-: | :-: | :-- |
| Claude Sonnet 5.5 (subagente) | 11 | 6 (bisiesto, tope, redondeo, día 30, ruta hermana, MD5); folios lo intentó y no salió | 0 | ~69k tokens, 34 s |
| Claude Opus 5.5 (subagente) | 11 | 6 (los mismos); folios no salió | 0 | ~72k tokens, 201 s |
| Codex `gpt-6-sol` (externo), 1.ª pasada | 9 (no señaló `leer_config`; las pruebas flojas solo en una frase final) | 0: `python` «Acceso denegado» en su sandbox | 0 | ~13k tokens |
| Codex `gpt-6-sol`, 2.ª pasada con `windows.sandbox=unelevated` | 10 (falta solo `leer_config`) | 7 (folios, tope, redondeo, día 30, bisiesto, ruta hermana —con `open` simulado—, MD5) | 0 | ~8k tokens |

**Lectura (sin sobreinterpretar):**
- Con fallos sutiles Sonnet y Opus siguen empatados al 11/11; Codex baja a 9/11 pero sin poder ejecutar nada. Aun así, **no hay evidencia de que Sonnet sea peor auditor que Opus** en este tipo de código. Una sola prueba de juguete: no mide el sesgo de familia.
- Los tres cruzaron código con requisitos. La condición de carrera de los folios no la reprodujo nadie (CPython la disimula): se halló por lectura.
- Extras reales no plantados: importe negativo con descuentos acumulados, req. 7 sin implementar, comparación de hash no constante.
- Codex sin ejecutar sigue siendo la limitación principal: arreglar su acceso a `python` antes de usarlo de auditor.

**Con el arreglo de `python`:** Codex sube de 9 a 10 de 11 y es el único que reprodujo la carrera de los folios (dos llamadas devolvieron el folio 1). Sigue sin ver `leer_config` (errores tragados). Su suite dio 1 error porque su entorno no tiene carpeta temporal escribible: es limitación del sandbox, no del proyecto. Con ejecución, Codex queda a la par de Sonnet y Opus, a menos de la mitad de gasto en tokens (cuentan distinto).
