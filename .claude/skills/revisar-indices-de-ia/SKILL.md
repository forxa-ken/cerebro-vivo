---
name: revisar-indices-de-ia
description: Use when Darwin says "revisa los índices", the arranque warns that an AI index (CLAUDE.md, GEMINI.md, AGENTS.md) is near its cap, has broken references or is overdue for review.
---

# Revisar los índices de IA (doble pasada)

Limpia `CLAUDE.md`, `GEMINI.md` y `AGENTS.md` sin perder información y sin falsos positivos. El guardián solo propone; esta skill verifica con **dos pasadas**; Darwin aprueba; lo retirado se **mueve**, nunca se borra.

## Cómo (pasos)
1. Informe: `python .brain/guardianes/revisar_indices.py --json`. Cinco tipos de hallazgo: referencia rota, deriva entre índices, sección pesada, fecha vieja, duplicado en `.brain/`. Cada uno trae una `clave` estable.
2. **Pasada 1, buscar.** Verificar cada hallazgo contra el proyecto real: ¿el archivo existe con otro nombre o ruta (`posible_nuevo_sitio`)? ¿se crea al ejecutar? ¿se cita como ejemplo o como historia? ¿otro documento vigente lo menciona? ¿la fecha es histórica a propósito? Resultado: *confirmado*, *descartado* (con motivo) o *dudoso*.
3. **Pasada 2, refutar.** Sobre lo confirmado y lo dudoso, una lectura independiente intenta demostrar que el hallazgo es falso. Preferible con un subagente al que se pasa **solo el hallazgo y la ruta del proyecto**, sin el razonamiento de la pasada 1 (si no hay subagentes, releer desde cero antes de mirar la conclusión anterior). Solo sobreviven los que no se pueden refutar. Si las dos pasadas no coinciden, pasa a *dudoso*, nunca a seguro.
4. Anotar los descartados para que no vuelvan: `python .brain/guardianes/revisar_indices.py --descartar CLAVE --motivo "por qué"`.
5. **Enseñar a Darwin**, en lenguaje llano y antes de escribir nada: tabla «sección → qué proponemos» con tres grupos: *seguros* (sobreviven a las dos pasadas), *dudosos* («no tocar sin que lo mires tú») y una línea con cuántos se descartaron y por qué. Esperar su visto bueno.
6. Aplicar solo lo aprobado: la referencia viva que es documentación → su ficha (`.brain/architecture/`, `referencias.md`); lo desfasado → `.brain/archive/indices/AAAA-MM-DD-NOMBRE.md` con una línea en `.brain/archive/indices/indice.md`; lo corregible, corregido. Dejar los tres índices sincronizados.
7. Cerrar: `python .brain/guardianes/revisar_indices.py --marcar-revision`, volver a lanzar el informe (debe quedar limpio o solo con lo dudoso aceptado), pruebas en verde y línea en `decisions.log`.

## Error que evita (caso real)
- Borrar de un índice una "ruta rota" que era un ejemplo, un archivo que se crea al ejecutar o un histórico a propósito; o dejar crecer un `CLAUDE.md` hasta 49 KB (diez veces su tope) con secciones de arquitectura que nadie revisa contra el código.

## Dónde está en el repo
- `.brain/guardianes/revisar_indices.py`, `.brain/guardianes/revision_indices.json` (descartes y fecha de última revisión), spec 016

## Fuente
- spec 016

## Usada
- Veces: 0 · Última: — (creada el 2026-11-04, spec 016)
