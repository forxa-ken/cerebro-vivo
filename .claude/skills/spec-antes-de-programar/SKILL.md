---
name: spec-antes-de-programar
description: Use when a change touches quotas, payments, licenses, deployment, the database, real servers or security rules, or cannot be resumed from the request plus the git diff.
---

# Spec antes de programar

## Cómo (pasos)
0. **¿Hace falta spec?** Sí si el cambio toca cuotas, pagos, licencias, despliegue, base de datos, servidores reales o reglas de seguridad. En lo demás, **prueba de retomar**: si otra IA puede continuar solo con el encargo y el `git diff`, es tarea pequeña y va directa por Fast-Track, con las reglas de seguridad, el registro y la lección de siempre. El número de archivos ya no decide.
1. Crear `.brain/specs/NNN-nombre.md` desde `_template.md`: objetivo, alcance, fuera de alcance, plan, verificación. **Cada regla se escribe una sola vez** (decirla de dos maneras provoca rechazos del aprobador).
2. Esperar la aprobación de Darwin antes de programar.
3. Lo demás va por Fast-Track: cambio directo, tests en verde y línea en `decisions.log`.
4. Al cerrar: ficha D-NNN si hubo decisión importante.

## Error que evita (caso real)
- Programar sin plan en cambios grandes genera código desordenado y trabajo repetido.

## Dónde está en el repo
- `.brain/specs/`, `.brain/specs/_template.md`

## Fuente
- D-001

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-10-31, spec 079)
