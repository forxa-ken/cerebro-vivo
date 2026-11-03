# Spec 011: comandos fijos `traspaso-in` y `traspaso-out`

- **Estado:** hecha y probada por las pruebas del repo (1.9.0); falta la prueba de Darwin
- **Fecha:** 2026-11-03

## 1. Objetivo
Darwin confunde dos casos distintos y el nombre actual no ayuda: pasar de un chat a otro **con la misma IA** (chat largo, chat nuevo) y pasar el trabajo **entre IAs** (Claude, Gemini, Codex). Dos comandos fijos y descriptivos, el mismo nombre en las tres IAs:
- **`traspaso-in`** — dentro de la misma IA: de un chat al chat nuevo.
- **`traspaso-out`** — fuera de la IA: de una IA a otra.

Se invocan `/traspaso-in` y `/traspaso-out` en Claude y `$traspaso-in` y `$traspaso-out` en Codex.

## 2. En alcance
- [x] Skill `traspaso-in`: sustituye a `traspaso-entre-chats`. Dos modos, con la palabra detrás del comando: **`salgo`** (cierra el chat: escribe `.brain/traspaso.md` mirando git y las últimas pruebas, con lo último que Darwin pidió en palabras literales) y **`entro`** (en el chat nuevo: lo lee, lo cuenta en 4-5 viñetas, lo archiva moviéndolo y pregunta por dónde seguir). Si el chat nuevo es de Claude Code, el arranque ya lo muestra solo; `entro` cubre Codex y Gemini.
- [x] Skill `traspaso-out`: sustituye a `cambio-de-ia` (mismo contenido, otro nombre), con los mismos dos modos `salgo` y `entro`, y los campos IA que lo escribe, IA que sigue y hora.
- [x] La regla de los archivos de entrada (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`) y la plantilla de traspaso nombran los dos comandos.
- [x] Manual: sección «Cambiar de chat sin perder nada» y tabla de comandos con los dos nombres; se quita `cambio-de-ia` del manual.
- [x] Se retiran `cambio-de-ia` y `traspaso-entre-chats` del repo (con la prueba que lo vigila); `VERSION` 1.9.0, `CAMBIOS.md`, manifiesto, índice de skills, pruebas del repo al día.

## 3. Fuera de alcance
- No automatizar: Codex y Gemini no corren ganchos, la palabra la dices tú. El manual lo dice claro.
- No tocar el arranque de Claude Code.
- No arreglar aquí el archivado del traspaso por las pruebas ni el pendiente 14.
- No actualizar proyectos ni subir a GitHub sin orden de Darwin.

## 4. Plan
1. Crear `traspaso-in` y `traspaso-out` desde las skills actuales; quitar las dos viejas.
2. Reglas, plantilla y manual con los nombres nuevos.
3. Prueba nueva (existen ambas, no existen las viejas, la regla las nombra); versión, cambios, manifiesto.

## 5. Verificación
- `python -m unittest discover tests` en verde.
- Los proyectos que ya tienen las skills viejas **las conservan** tras actualizar (el actualizador solo añade y actualiza, no borra); se avisa en `CAMBIOS.md` y se borran a mano si se quiere.
- **Prueba de Darwin:** en Codex, `$traspaso-in salgo` en un chat y `$traspaso-in entro` en el chat nuevo: debe contar lo último que hablaron. Y `traspaso-out` entre Codex y Gemini.

## 6. Cierre
- [x] Spec aprobada por Darwin antes de programar
- [x] Línea añadida a `.brain/decisions.log`
