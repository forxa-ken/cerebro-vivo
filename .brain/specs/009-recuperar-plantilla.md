# Spec 009: recuperar el panel /plantilla en el repo

- **Estado:** hecha y probada (1.7.0)
- **Fecha:** 2026-11-01

## 1. Objetivo
Darwin usa el panel `/plantilla` («Prompt inicial») en su Claude Code y quiere que esté en el repo, versionado y repartido, no solo en una copia suelta del repo viejo. Se retiró en la 1.4.0 (spec 005) y se recupera del historial de git (commit `e1e604e~1`).

## 2. En alcance
- [x] Recuperar `plantilla-prompt/` (plugin de Claude Code en TypeScript: `register.tsx`, `logica.ts`, su prueba, `hooks.json`, `plugin.json`, README) y `.claude-plugin/marketplace.json` desde `e1e604e~1`.
- [x] Adaptar el panel a lo nuevo: los botones «Retomar: N» y «Resumen del estado» pasan a lanzar `/pendiente` y `/resumen` (o se quitan); el resto (tipo de tarea, tres campos, avisos, insertar en el chat, guardar en la biblioteca, plantilla en blanco para Gemini/Codex) se queda.
- [x] Decidir y dejar escrito cómo llega a los proyectos: el plugin se instala en Claude Code (no es un archivo de proyecto), así que la guía de instalación explica cómo añadirlo desde este repo y cómo actualizarlo.
- [x] `VERSION` 1.7.0, `CAMBIOS.md`, manifiesto si el plugin se reparte, pruebas del repo al día (`test_arnes_repo` y la prueba del plugin).
- [x] Quitar de `GUIA_INSTALACION.md` el aviso de que el repo ya no reparte el panel.

## 3. Fuera de alcance
- No tocar `/prompt-inicial` (sigue siendo la skill de texto, para Gemini/Codex y para quien no use el panel).
- No añadir funciones nuevas al panel.
- No subir a GitHub sin orden de Darwin.

## 4. Plan
1. Recuperar los archivos del commit anterior a la 1.4.0 y comprobar que la prueba `logica.test.ts` pasa (si hay herramienta para correrla en este equipo).
2. Adaptar los botones de estado.
3. Guía, versión, cambios, manifiesto, pruebas.

## 5. Verificación
- `python -m unittest discover tests` en verde; la prueba TypeScript del plugin, si se puede ejecutar (si no, se dice como no probada).
- **Prueba de Darwin:** instalar/actualizar el plugin desde este repo, escribir `/plantilla` y comprobar el panel (botones nuevos, insertar en el chat, guardar plantilla en blanco).

## 6. Cierre
- [x] Spec aprobada por Darwin antes de programar
- [x] Línea en `.brain/decisions.log`
