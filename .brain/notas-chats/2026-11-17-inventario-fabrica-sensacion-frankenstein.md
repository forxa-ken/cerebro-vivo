# Inventario: dónde está repartida la fábrica (solo lectura; nada tocado)

Chat cerebro-vivo #34, 2026-11-17. Pedido por Darwin tras la sensación de «parche sobre parche» del arnés.

## Dónde vive cada regla
| Pieza | Qué contiene | Tamaño |
|---|---|---|
| `.claude/skills/directora-de-fabrica/SKILL.md` (+ `.en`) | El flujo (13 pasos), caminos completo/corto, modo automático, esperas | 59 líneas, ~13 KB |
| Spec 035 | Diseño original de la fábrica, pruebas del 2026-11-09 | 77 líneas |
| Spec 042 | Colaboración + Gemini como obrera (**la parte Gemini, retirada el 2026-11-13**) | 63 líneas |
| Spec 050 | Modo automático: reparto de decisiones, frenos, prueba de uso real | 103 líneas |
| `PLANTILLAS_FABRICA.md`, `CARTA_EJECUTORA.md` | Plantillas | — |
| `fabrica.py` | El guardián (topes, alcance, foto, informe) | — |
| `CAMBIOS.md` | Historial 1.60.0 a 1.60.11 | — |

## Hallazgos
1. **El camino corto no está en ninguna spec.** Vive solo en la skill y en CAMBIOS (orden de Darwin 2026-11-16). Las specs 035 y 050 no lo mencionan. Es la regla más nueva y la que menos respaldo tiene escrito. Conviene una spec corta (o un apartado en la 035) antes de seguir.
2. **La skill mezcla tres cosas:** el flujo, el modo automático y ruido operativo (cómo esperar, vigilantes de 1800 s, qué decir al esperar). Las «esperas» ocupan casi un tercio y son operación, no flujo: candidato a pasar a una plantilla o a un apartado aparte.
3. **Números repetidos en varios sitios:** el tope de 350.000 tokens por encargo está en la skill, `fabrica.py`, `PLANTILLAS_FABRICA` (es/en), `tests/test_fabrica.py` y CAMBIOS. Si cambia, hay que tocarlo en 5 lugares. Fuente única debería ser `fabrica.py`; el resto, remitir.
4. **Gemini sigue apareciendo** en `.claude/skills/fabrica/SKILL.md` (línea 18, «Sin esas herramientas (Codex, Gemini)»). Es otro asunto (chat nuevo sin herramientas), no el de ejecutora, pero conviene confirmar si debe quedarse. La spec 042 ya marca la parte Gemini como retirada.
5. **La página pública:** no encontré «aún no está construida» en el repo; lo dicho antes sobre eso ya está corregido o vive solo en `_cv_pagina` (no lo verifiqué a fondo). Falta el capítulo 20 «Lo nuevo» con la 1.60.x.
6. **Modo automático: apagado por defecto.** `fabrica.py` solo lo activa con `automatico si`, y solo vale con el modo fábrica encendido. Eso resuelve la duda; falta dejarlo escrito en un sitio visible.
7. **Skill ya unificada en 1.60.11:** un solo flujo con marcas **[corto]**. Lo que queda no es duplicidad dentro de la skill, sino repartición entre skill, specs y CAMBIOS.

## Qué podaría (cuando Darwin lo ordene y tras estrenar el camino corto)
- A. Escribir el camino corto en la spec 035 (apartado) y marcar en la 042 la parte Gemini como retirada de forma visible al principio.
- B. Sacar de la skill la sección «Esperar sin quedarte parada» a una plantilla; dejar un enlace de una línea.
- C. Dejar el 350.000 solo en `fabrica.py`; la skill y plantillas dicen «el tope que dé `topes`».
- D. Revisar la línea Gemini de la skill `fabrica`.
- E. Escribir en un solo sitio «automático: apagado por defecto».
- F. Página: capítulo 20 y estado actual.

## Sin comprobar
No corrí pruebas ni cambié nada. No he leído a fondo las specs 035/042/050 más allá de títulos y líneas sueltas; los tamaños son de `wc`.
