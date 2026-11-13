---
name: revisar-contenido
description: Use when Darwin says "revisa el contenido" or "revisa la memoria", or the arranque warns of findings in the content of .brain/ (orphan pages, outdated statements, possible contradictions).
---

# Revisar el contenido de `.brain/` (buscar y refutar con otra IA)

La memoria se pudre sin que nadie lo note: una página que nadie enlaza, una frase que ya no es cierta, dos documentos que se contradicen. El guardián propone; esta skill verifica; **otra pasada independiente intenta refutar**; Darwin decide. Nada se corrige solo.

## Cómo (pasos)
1. Informe: `python .brain/guardianes/revisar_contenido.py --json`. Tres tipos: `huerfana` (nadie la enlaza), `desfasada` (ruta que no existe, «versión actual» distinta de `VERSION`, cifra falsa) y `contradiccion` (el mismo tope con valores distintos). Cada hallazgo trae una `clave` estable.
2. **Pasada 1, buscar (tú).** Lee cada hallazgo contra el proyecto real: ¿la página es histórica a propósito o la enlaza un índice con otro nombre? ¿la ruta se crea al usar el método? ¿los dos topes hablan de cosas distintas? Resultado: *confirmado*, *descartado* (con motivo) o *dudoso*. Además, busca a mano lo que el script no ve: «pendiente» en un documento y «hecho» en otro, o una frase que ya no se cumple.
3. **Pasada 2, refutar (otra IA, no tú).** Quien encuentra un hallazgo tiende a darse la razón, así que **no te refutes a ti mismo**. Lanza un subagente nuevo (mismo modelo, sin tu contexto) y pásale **solo las dos frases y la ruta del proyecto**, con la pregunta «¿se contradicen o ya no es cierto, de verdad? Intenta demostrar que NO» (apóyate en la skill `revisor-independiente`). Solo sobreviven los que no puede refutar. Si no coincidís, el hallazgo pasa a *dudoso*, nunca a seguro.
4. **Opcional, solo para lo dudoso:** si el proyecto tiene otra IA configurada (Gemini, Codex; ver `colaboracion.md`), pídele un segundo juicio del mismo modo.
5. Anota los descartados para que no vuelvan: `python .brain/guardianes/revisar_contenido.py --descartar CLAVE --motivo "por qué"`.
6. **Enseña a Darwin**, en lenguaje llano y antes de tocar nada: *seguros* (sobreviven a la refutación), *dudosos* («no tocar sin que lo mires tú») y cuántos se descartaron y por qué. Espera su visto bueno.
7. Aplica solo lo aprobado: enlazar la página huérfana desde su índice, corregir la frase, o **mover** lo viejo a `.brain/archive/` (nunca borrar; ver la skill `mover-no-borrar`).
8. Cierra: `python .brain/guardianes/revisar_contenido.py --marcar-revision`, vuelve a lanzar el informe, pruebas en verde y línea en `decisions.log`.

## Error que evita (caso real)
- Dar por contradicción dos topes que hablaban de archivos distintos, o borrar una página «huérfana» que era histórica a propósito; y que la IA que propone el hallazgo sea también la que lo confirma.

## Dónde está en el repo
- `.brain/guardianes/revisar_contenido.py`, `.brain/guardianes/revision_contenido.json` (descartes y fecha de la última revisión), spec 048

## Fuente
- spec 048 (pendiente 44, idea del gist «LLM Wiki» de Karpathy)

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-11-13, spec 048)
