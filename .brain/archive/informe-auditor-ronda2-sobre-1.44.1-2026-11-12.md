# Segunda auditoría del auditor (sobre 1.44.1, commit 0d87c4f) — 2026-11-12

**Ejecutores:** interno Sonnet 5.5 medio (~94k tokens, 130 s) + externo Codex `gpt-6-sol` medio (~33k tokens). Misma tarea para ambos.

| | Sonnet | Codex |
| :-- | :-- | :-- |
| Veredicto | apto con reparos | devuelto |
| Hallazgos antiguos | 12 enumerados: todos corregidos o decididos | 14: casi todos corregidos; 2 «parcial» |

## Coinciden
- `auditor_ignorar_extensiones=[""]` apaga el aviso (`endswith("")`). Sonnet además: `"md"` sin punto casa con `.cmd`.
- Un modelo que parece opción (`-s`, `--help`) entra en el comando de Codex.
- El aviso puede repetirse en cada respuesta con ediciones (la spec ya lo admite).

## Solo Sonnet
- `RecursionError` con JSON anidado 100000 veces (traceback en `main`); `auditor_modelo` sin sanear; `sensible` casa por subcadena (`auth` en `author/`); `externo "  "` da uso y `externo ""` es estado.

## Solo Codex
- `editados=[]` con `hubo_ediciones=True` deja pasar todos los cambios de git (es lo previsto para ediciones por terminal, spec 003).
- `/auditor estado` con el archivo roto muestra los valores por defecto sin avisar.

## Corregido en 1.44.2
Extensiones vacías/sin punto, opciones como valor, RecursionError, estado con archivo roto, `auditor_modelo` saneado (4 pruebas nuevas, 499 en total).
## No corregido (decidido)
Repetición del aviso sin apagado de la spec 038; `editados=[]` por terminal; subcadena en `sensible`; `externo " "`. **No probado:** que la IA obedezca el aviso; Codex real con `-m -s`; el hook `Stop` completo con transcript real.
