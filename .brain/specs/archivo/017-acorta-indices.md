# Spec 017: /acorta — bajar los índices de IA al tope

- **Estado:** implementada (arnés 1.15.0)
- **Fecha:** 2026-11-04

## 1. Objetivo
Dar un atajo `/acorta` que lleve `CLAUDE.md`, `GEMINI.md` y `AGENTS.md` al tope (`tope_claude_md_bytes`, 5 KB) sustituyendo secciones pesadas por un enlace, sin perder texto. Es el paso 5 de `adoptar-indice-existente` con nombre propio.

## 2. En alcance
- [x] Skill `acorta` (solo instrucciones; reutiliza `revisar_indices.py`, sin código nuevo).
- [x] Ficha en `.brain/experiencia/indice.md`; `adopta` y `adoptar-indice-existente` apuntan a `/acorta`.

## 3. Fuera de alcance
- No cambiar el guardián ni el tope. No borrar nada: todo se mueve a `.brain/`.

## 4. Plan
1. Medir con `revisar_indices.py`. 2. Comprobar que cada sección pesada ya está copiada en `.brain/` (o copiarla antes). 3. Tabla «sección → enlace» a Darwin y esperar su sí. 4. Sustituir por el enlace, sincronizar los tres índices, comprobar tope.

## 5. Verificación
- `python -m unittest discover tests` en verde. Probar en Guild Control Forever (52 KB): sin probar.

## 6. Cierre
- [x] Aprobada por Darwin ("ok", 2026-11-04) · [x] Línea en `decisions.log`
