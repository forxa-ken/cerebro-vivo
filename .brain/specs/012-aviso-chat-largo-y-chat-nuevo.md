# Spec 012: aviso de chat largo y chat nuevo al mismo nivel

- **Estado:** hecha y probada por las pruebas del repo (1.10.0); falta la prueba de Darwin
- **Nota al programar:** ya existía el guardián `longitud.py` (spec 056, mide tokens reales, avisa por tramos y ya pedía escribir el traspaso). No se creó `chat_largo.py` ni se mide en KB: solo se amplió su aviso. Se descartan los puntos de guardián nuevo, `chat_largo_kb` y escritura del traspaso por el guardián (lo escribe la IA, como antes).
- **Fecha:** 2026-11-03

## 1. Objetivo
Hoy el aviso de «chat largo» depende de que la IA se acuerde. Se quiere que sea automático: al llegar a un límite fijado, el traspaso queda escrito, Darwin recibe un aviso claro y el chat nuevo se abre **al mismo nivel** que el anterior (no colgado de él en el sidebar).

## 2. En alcance
- [ ] Guardián `chat_largo.py` en el gancho `Stop` de Claude Code: lee `transcript_path` (llega por stdin al gancho), mide el tamaño y, al pasar el límite, avisa **una sola vez por chat**. Se registra el aviso para no repetirlo.
- [ ] Límite configurable en `guardianes.json` (clave `chat_largo_kb`, con un valor por defecto prudente a decidir con Darwin tras medir un chat real).
- [ ] Al saltar el aviso, el guardián escribe `.brain/traspaso.md` con la misma plantilla de `traspaso-in salgo` (git, últimas pruebas, lo último que pidió Darwin) y dice: «Chat largo: he dejado el traspaso. Ábrelo en un chat nuevo o dime "abre el chat nuevo"».
- [ ] Regla para la IA de Claude Code: al ver ese aviso, o cuando Darwin diga «abre el chat nuevo», abre el chat con `start_session` (encargo = leer el traspaso) y **enseguida** lo separa con `detach_session` para que quede al nivel principal. Después avisa a Darwin con el nombre del chat nuevo.
- [ ] Manual y `CAMBIOS.md` al día, `VERSION` subida, manifiesto regenerado, prueba nueva del guardián (por debajo del límite no avisa; por encima avisa una vez; no repite).

## 3. Fuera de alcance
- Codex y Gemini: no tienen ganchos ni herramienta para abrir chats; siguen con `traspaso-in salgo` a mano. El manual lo dice.
- Un hook no puede abrir sesiones por sí mismo: la apertura la hace la IA al leer el aviso o tras la orden de Darwin.
- No tocar el resumen automático propio de Claude Code.
- No actualizar proyectos ni subir a GitHub sin orden de Darwin.

## 4. Riesgos
- `detach_session` no se puede deshacer, y solo vale para chats abiertos por la propia IA; si falla, el chat queda anidado y se avisa a Darwin sin más daño.
- Medir en KB es una aproximación del tamaño de contexto, no un contador exacto de tokens.
- El gancho en Windows: probar la salida con la consola (skill `probar-guardian-en-windows`).

## 5. Plan
1. Medir el tamaño de un chat real para fijar el límite por defecto.
2. Guardián + registro de «ya avisado» + escritura del traspaso.
3. Regla en `CLAUDE.md` (apertura con `start_session` + `detach_session`).
4. Pruebas, manual, versión, manifiesto.

## 6. Verificación
- `python -m unittest discover tests` en verde.
- **Prueba de Darwin:** bajar el límite a un valor pequeño en un proyecto de prueba, seguir hablando hasta que salte el aviso, decir «abre el chat nuevo» y comprobar que el chat nuevo aparece al mismo nivel y cuenta lo último que se habló.

## 7. Cierre
- [x] Spec aprobada por Darwin antes de programar
- [ ] Línea añadida a `.brain/decisions.log`
