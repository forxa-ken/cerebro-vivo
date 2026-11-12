---
name: auditor
description: Use when Darwin types /auditor (general, cierre, externo or estado), asks for an audit of quality, resource use and security, or the closing warns "lanza el auditor".
---

# /auditor — quien intenta romper el trabajo antes de darlo por bueno

El auditor funciona en **cualquier proyecto**, sin fábrica. Busca fallos de **calidad** (¿cumple lo que pide la spec?), **consumo** (CPU, memoria, disco, red) y **seguridad**, y **solo avisa**: no cambia código ni bloquea el cierre (spec 044). No sustituye al revisor de la fábrica, que comprueba cada encargo; en la fábrica el auditor entra en el **cierre de la spec**.

## Cómo (pasos)
1. **Elegir el modo** con la palabra detrás del comando: `general` (revisa el proyecto o la carpeta indicada), `cierre` (lo cambiado en la tarea actual) o `spec` (cierre de spec de la fábrica: la spec, los encargos, el veredicto de la directora y la integración). Sin palabra, `estado`.
2. **Ver quién audita:** `python .brain/guardianes/auditor.py quien MODO`. Siempre el **interno** (subagente de solo lectura, Sonnet 5.5 en medio, distinto del que escribió). El **externo** (Codex) entra en `general` y `spec`, y en `cierre` solo si `auditor_externo` es `siempre`; con `no` no se llama a ninguna IA externa. En `cierre` pásale los archivos cambiados (`quien cierre ARCHIVO…`): si tocan algo sensible (`revision_sensibles`) responde `externo?` = se sugiere el externo; decídelo con Darwin.
3. **Lanzar al interno** como subagente de solo lectura con instrucción adversa: «demuestra que falla», cruza el código con la spec, **ejecuta** pruebas y comprobaciones (no solo lee) y da cada hallazgo con archivo y línea. Para los criterios, reutiliza `revisor-independiente` (calidad), `revisor-de-consumo` (consumo) y `seguridad-en-sistemas-reales` (seguridad); no los copies.
4. **Lanzar al externo** si toca: `python .brain/guardianes/auditor.py codex` da el comando (`codex exec` en solo lectura; en Windows lleva `windows.sandbox="unelevated"` o Codex no puede ejecutar `python`). Pásale la misma tarea por la entrada estándar. Si Codex no está instalado o falla, **dilo claro** y sigue con el interno.
5. **Informe único** con `biblioteca/PLANTILLA_INFORME_REVISION.md`: veredicto, hallazgos por bloque (calidad, consumo, seguridad), lo no comprobado y, si hubo dos auditores, en qué **coinciden** y en qué **discrepan**.
6. **Contar a Darwin en llano** lo importante y dejar que decida: el informe es suyo. Lo que se corrija, se corrige después, en otra tarea.
7. **Ajustes:** `/auditor cierre si|no|estado` (el aviso tras cambios de código o configuración; encendido por defecto, no avisa si solo se tocó memoria o documentos) y `/auditor externo general-y-spec|siempre|no|estado` con `python .brain/guardianes/auditor.py cierre|externo PALABRA`. Modelos y esfuerzo: `auditor_modelo`, `auditor_modelo_externo`, `auditor_esfuerzo` en `guardianes.json`.

## Error que evita (caso real)
- Prueba de fallos plantados (2026-11-12, spec 044): un código de juguete con 11 fallos sutiles pasaba sus 9 pruebas en verde. Los tres auditores hallaron 10 o 11; solo Codex reprodujo la carrera de los folios y solo Sonnet y Opus vieron los errores tragados. Ninguno solo cubre todo: por eso en lo delicado van dos.

## Dónde está en el repo
- `.claude/skills/auditor`, `.brain/guardianes/auditor.py` (ajustes y comando de Codex), `cierre.py` (aviso), `biblioteca/PLANTILLA_INFORME_REVISION.md`, spec 044 y los informes de las dos rondas en `.brain/archive/`.

## Fuente
- Spec 044 (petición de Darwin, 2026-11-12)

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-11-12)
