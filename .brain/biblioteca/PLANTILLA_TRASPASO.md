# Plantillas de traspaso (specs 078 y 026)

La IA escribe **dos** archivos (sobrescribiéndolos) **antes** de proponer o crear un chat nuevo (skill `traspaso-in`) o al cambiar de IA (skill `traspaso-out`). No van a GitHub (salvo el commit de memoria de `traspaso-out salgo`).

- **`.brain/traspaso.md` (corto):** es lo único que carga solo el chat nuevo. Máximo ~1500 caracteres (el guardián avisa pasado `traspaso_corto_max`). «NO hacer» y «sin subir» nunca salen de aquí.
- **`.brain/traspaso-completo.md` (completo):** el historial entero. No se carga solo; el arranque solo avisa de que existe. Al entrar se archiva en `.brain/archive/traspasos/AAAA-MM-DD-HHMMSS-completo.md` y la skill `/memoria-traspaso` lo trae. Máximo ~6000 caracteres.

## Plantilla corta (`traspaso.md`)
```markdown
# Traspaso del chat #N al #N+1 (AAAA-MM-DD)

- **IA que lo escribe:** Claude | Gemini | Codex
- **IA que sigue:** (si se sabe)

## Lo último que pidió Darwin
- «…» (palabras literales)

## Espera su respuesta
- …

## Siguiente paso
- …

## NO hacer
- …

## Sin subir a GitHub
- Archivos y commits locales (o «nada»)

Detalle completo: `/memoria-traspaso`
```

## Plantilla completa (`traspaso-completo.md`)
```markdown
# Traspaso completo del chat #N al #N+1 (AAAA-MM-DD)

- **IA que lo escribe:** Claude | Gemini | Codex
- **IA que sigue:** (si se sabe)
- **Hora:** AAAA-MM-DD HH:MM

## 1. Lo último que pidió Darwin (palabras literales)
- «…»

## 2. Decisiones
- Tomadas: …
- Abiertas (esperan respuesta de Darwin): …

## 3. Estado de cada punto en curso
- Punto X: hecho / a medias (qué falta) / sin probar

## 4. Sin subir a GitHub
- Archivos y commits locales

## 5. Qué debe probar Darwin
- Pasos concretos

## 6. NO hacer (descartado)
- …

## 7. Lecciones apuntadas en este chat
- Tema y regla de cada una (o «ninguna»)
```
