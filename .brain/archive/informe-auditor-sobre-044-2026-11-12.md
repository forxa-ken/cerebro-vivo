# Informe del auditor sobre sí mismo (spec 044, 1.44.0) — revisión general, 2026-11-12

Primera prueba real del auditor (no código de juguete). **Modo:** general. **Ejecutores:** interno Sonnet 5.5 medio + externo Codex `gpt-6-sol` medio (`windows.sandbox="unelevated"`, solo lectura), con la misma tarea (`quien general` = interno + externo). **Estado: hallazgos NO corregidos; es lo que sigue.**

| | Sonnet 5.5 (interno) | Codex (externo) |
| :-- | :-- | :-- |
| Veredicto | apto con reparos | **devuelto** |
| Hallazgos | 8 de calidad, 2 de seguridad, 0 de consumo | 5 de calidad, 1 de consumo, 1 de seguridad |
| Ejecutó comprobaciones | sí (copia temporal, `python -B`) | sí (6 pruebas de `test_auditor` no pudieron correr: su sandbox no deja `tempfile`) |
| Gasto | ~92.8k tokens, 124 s | ~39.6k tokens |

## Coinciden (los dos lo vieron)
1. **`auditor_cierre` por defecto distinto:** `cierre.py:221` usa `False` si falta la clave y `auditor.py` (estado) usa `True`; la spec dice «verdadero por defecto». Lo consagra `test_no_avisa_si_el_ajuste_no_existe`. Gravedad media/baja.
2. **Comando de Codex sin escapar** (`auditor.py` `main`/`comando_codex`): valores de `guardianes.json` entran tal cual en la línea impresa. Riesgo bajo (solo lo ejecuta la IA; requiere escribir en el repo).
3. **Pruebas que no cubren** la función `main` (comandos `quien`, `codex`, `estado`) ni entradas raras.

## Solo Sonnet
- **[alta] Pérdida de configuración:** si `guardianes.json` tiene BOM (Bloc de notas) o JSON roto, `_cfg` devuelve `{}` y `/auditor cierre no` o `externo X` **sobrescribe el archivo con solo esa clave**. Reproducido. Arreglo: no escribir si falla la lectura, avisar; leer con `utf-8-sig`.
- **[media] Tipos equivocados rompen el cierre:** `auditor_ignorar_extensiones` en `None`/número da `TypeError` dentro de `cierre.evaluar` (solo se captura `ImportError`). Un guardián que solo avisa no debe tumbar el cierre: envolver en `except Exception`. Raíz del JSON que no es objeto (`[1,2]`) da `AttributeError`.
- **[media] Sordo en este repo:** `ignorar_cambios` incluye `.brain/*` y `.claude/*`, así que el aviso no salta para el código de los guardianes, hooks y skills. Decidir si es intencionado y escribirlo en la spec.
- **[baja]** `"false"` como texto cuenta como encendido; `/auditor cierre FALSE` da error de uso; `arranque.py` no normaliza el valor como `valor_externo`.
- Nota: dice que `gpt-6-sol` «no está verificado»; sí se ha ejecutado con ese nombre en las rondas 1 y 2 y en esta.

## Solo Codex
- **[media] El cierre por bloques lo apaga:** con `sin_cerrar` menor de 15, `del_proyecto` se vacía antes de mirar el aviso del auditor; una tarea de código con pocas ediciones se cierra sin auditor. Reproducido (con 15 sí avisa). Las pruebas pasan siempre `sin_cerrar=None`.
- **[media] No mira `hubo_ediciones`:** puede pedir auditar cambios de una tarea anterior aunque esta respuesta no editó nada.
- **[media] `revision_sensibles` existe solo como lista:** ningún código la lee ni sugiere `auditor_externo="siempre"` (punto «En alcance» sin hacer).
- **[baja]** `README`/`LICENSE` (sin extensión ignorada) cuentan como código.

## Lectura
- Los dos conjuntos casi no se solapan: Sonnet halló los fallos de robustez y datos; Codex los de lógica de integración con el cierre y lo prometido en la spec. **Juntos dieron 14 hallazgos distintos; ninguno solo cubría la mitad** (refuerza la regla de dos auditores en lo delicado). Sonnet y Codex no coincidieron en el veredicto.
- El auditor funcionó de punta a punta como se diseñó: `quien`, comando de Codex con el arreglo de Windows, informe con la plantilla y coincidencias/discrepancias.
- Orden sugerido para corregir: (1) pérdida de configuración (BOM/JSON roto) con prueba; (2) tipos + `except Exception` en el aviso; (3) cierre por bloques y `hubo_ediciones`; (4) leer `revision_sensibles` o quitarla de la spec; (5) unificar el valor por defecto de `auditor_cierre`; (6) decidir lo de `.brain/*` y `.claude/*`.
