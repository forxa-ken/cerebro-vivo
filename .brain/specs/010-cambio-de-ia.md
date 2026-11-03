# Spec 010: `/cambio-de-ia` — pasar el trabajo entre Claude, Gemini y Codex

- **Estado:** hecha y probada por las pruebas del repo (1.8.0); falta la prueba de Darwin con Gemini y Codex
- **Fecha:** 2026-11-03

## 1. Objetivo
Darwin trabaja un mismo proyecto con Gemini y Codex (y Claude Code). Gemini y Codex no corren ganchos: no hay resumen al abrir ni aviso al cerrar, así que nadie le enseña a la IA que entra lo que dejó la que sale. Una skill `cambio-de-ia` hace las dos mitades a mano con una frase: al salir, escribe el traspaso; al entrar, lo lee, lo cuenta y lo archiva.

## 2. En alcance
- [x] Skill `cambio-de-ia` en `.claude/skills/` y `.agents/skills/` (en Codex, `$cambio-de-ia`). Dos modos:
  - **Salir:** escribe `.brain/traspaso.md` con la plantilla actual más tres campos nuevos: IA que lo escribe, IA que sigue (si se sabe) y hora. Completa con lo que ve en git (archivos sin commitear, últimos commits) y el resultado de las últimas pruebas, no solo con lo que recuerda.
  - **Entrar:** lee `.brain/traspaso.md`, lo cuenta a Darwin en 4-5 viñetas, lo archiva en `.brain/archive/traspasos/` (mover, no borrar) y sigue con lo que Darwin pida.
- [x] `PLANTILLA_TRASPASO.md` con los campos nuevos (compatible con el arranque actual de Claude Code, que sigue mostrándolo solo).
- [x] Regla corta en los archivos de entrada que genera el instalador (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`), también en nivel medio: «si existe `.brain/traspaso.md`, léelo primero; al cambiar de IA usa `cambio-de-ia`».
- [x] El instalador y el actualizador reparten la skill (también a `.agents/skills/` si hay `AGENTS.md`).
- [x] **Manual:** `MANUAL_DE_USO.md` recoge todos los comandos, incluidos los de esta spec: sección «Cambiar de IA» con las frases para salir y entrar, cómo se invoca en Claude (`/`), Codex (`$`) y Gemini (pedirle que lea `GEMINI.md` y la skill si no la reconoce), y una tabla única de comandos del método (instalar, actualizar y sus opciones, migrar objetivo, comprobar, cerrar, medir, pruebas). Los de actualizar y migrar ya están en la sección 7.
- [x] `VERSION` 1.8.0, `CAMBIOS.md`, `python generar_manifiesto.py`, pruebas del repo al día.

## 3. Fuera de alcance
- No automatizar el cambio: sin ganchos en Gemini/Codex, alguien dice la frase al irse y al llegar. Se dice claro en el manual.
- No tocar el arranque de Claude Code salvo si hace falta para leer los campos nuevos.
- No arreglar aquí que el actualizador copie guardianes y pruebas a proyectos de nivel medio (pendiente aparte).
- No arreglar los 4 fallos de pruebas de `F:\Pegatinas`.
- No actualizar proyectos (LoboHook, Pegatinas) ni subir a GitHub sin orden de Darwin.

## 4. Plan
1. Plantilla de traspaso con los campos nuevos y prueba de que el arranque la sigue leyendo.
2. Skill `cambio-de-ia` (Claude y Codex, mismo texto, adaptado a `$`).
3. Regla en las plantillas de los archivos de entrada del instalador; instalador y actualizador reparten la skill.
4. Manual, versión, cambios, manifiesto.

## 5. Verificación
- `python -m unittest discover tests` en verde (con pruebas nuevas: la skill existe en ambas carpetas y el manifiesto la reparte; el instalador en nivel medio escribe la regla en los tres archivos de entrada; la plantilla nueva sigue siendo leída por `arranque.py`).
- Lo que no se pueda probar sin Gemini o Codex reales se dice como no probado.
- **Prueba de Darwin:** en un proyecto con Codex y Gemini, escribir «cambio de IA, salgo» en una, abrir la otra, escribir «cambio de IA, entro» y comprobar que cuenta lo que dejó la primera.

## 6. Cierre
- [x] Spec aprobada por Darwin antes de programar
- [x] Línea añadida a `.brain/decisions.log`
