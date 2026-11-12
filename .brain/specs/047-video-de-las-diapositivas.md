# Spec 047: vídeo de las diapositivas (`/video`), reutilizando la técnica del Estudio de video de LoboHook

- **Estado:** borrador, **esperando la aprobación de Darwin** (no se programa nada hasta entonces).
- **Fecha:** 2026-11-12
- **Origen:** Darwin pidió reutilizar el constructor de vídeos de LoboHook para hacer vídeos del arnés. Se revisó en solo lectura: `static/js/studio.js` (3.688 líneas) graba un lienzo de 1920×1080 a 60 imágenes por segundo con `canvas.captureStream` + `MediaRecorder` a `.webm` (VP9 y Opus, 16 Mbps), con sonido de Web Audio y 21 MP3 de locución hechos con Kokoro-82M (Apache 2.0).

## 1. Qué se reutiliza y qué no
- **Se reutiliza la técnica, no el archivo.** Este repo no puede contener nada de LoboHook (lo vigila `tests/test_arnes_repo.py`) y `studio.js` es 100 % del producto (Discord, construir servidores con IA). Se escribe código nuevo y propio, corto, con la misma idea probada: lienzo → `captureStream` → `MediaRecorder` → descarga `.webm`.
- **No se copia la grabación de pantalla** (`getDisplayMedia`, que pide permiso y comparte la ventana). Aquí el visor **dibuja él mismo cada diapositiva en el lienzo**, así que no pide permisos y el resultado es limpio y repetible.
- **Ahorro real:** sabemos que la técnica funciona en el navegador, en Full HD y sin librerías, y el flujo de la locución con Kokoro ya está resuelto. No ahorra el dibujo de las diapositivas en lienzo ni el guion, que hay que escribir.

## 2. Objetivo
Que Darwin escriba `/video [tema o documento]` y obtenga un **`.webm` descargable** con las diapositivas de `/diapositivas` pasando solas (con transiciones suaves y la duración de cada una), sin instalar nada y sin salir del método (Python estándar y navegador, es/en).

## 3. Fases (cada una se aprueba y se prueba aparte)
1. **Vídeo mudo (esta fase):** `diapositivas.py --video` añade al visor un botón «Grabar vídeo». Las diapositivas se dibujan en un lienzo 1920×1080 con transición de fundido; cada una dura según su cantidad de texto (mínimo 4 s); se graba y se descarga `AAAA-MM-DD-tema.webm`. Incluye los diagramas de la spec 046 si ya existen, como imagen SVG pintada en el lienzo.
2. **Música y efectos sintetizados** con Web Audio (sin archivos): fondo suave y un «pop» al cambiar de diapositiva, con la opción de silencio.
3. **Locución (opcional):** MP3 por diapositiva generados **fuera del arnés** con Kokoro (licencia Apache 2.0, local y gratis) y un archivo de guion; el visor los reproduce y ajusta la duración de cada diapositiva a su audio. El arnés **no instala ni depende** de Kokoro: solo lee MP3 si existen. Créditos a Kokoro si se publica.
4. **Animaciones en las diapositivas** (flechas que se dibujan, pasos que se encienden), solo si Darwin las pide después de ver la fase 1.

## 4. En alcance (fase 1)
- [ ] Código del dibujante de lienzo y del grabador, en un archivo propio (`diapositivas_video.py` o JS dentro del HTML generado), corto y sin dependencias; el HTML sigue sin pedir nada a internet.
- [ ] Botón «Grabar vídeo» y barra de avance; al terminar, vista previa y descarga. Si el navegador no soporta `MediaRecorder` con `webm`, mensaje claro (es/en en `textos.py`) y no se rompe el visor.
- [ ] Skill `/video` (es y `.en.md`): prepara las diapositivas como `/diapositivas`, avisa de que Darwin pulse el botón y de dónde quedó el `.webm`. Una línea en el manual (es y en), versión nueva, `CAMBIOS.md`, manifiesto, página pública revisada (no se sube sin orden).
- [ ] Pruebas: el HTML generado incluye el grabador y no tiene peticiones externas; la duración por diapositiva se calcula por el texto; salida en UTF-8 en consola de Windows; paridad es/en en verde.
- [ ] Ejemplo real: un vídeo corto del arnés (portada, ciclo de una tarea, qué vigila) para que Darwin lo vea.

## 5. Fuera de alcance
- Copiar o importar código, audios o vídeos de LoboHook.
- Grabación de pantalla, cursor, zoom de cámara y edición en el navegador.
- Convertir a MP4 (necesitaría ffmpeg; queda como mejora opcional solo si ya está instalado).
- Instalar o ejecutar Kokoro desde el arnés.
- Cambiar el resto del arnés o del visor.

## 6. Riesgos
- **El vídeo se genera en el navegador:** depende de que soporte `MediaRecorder` (Chrome, Edge y Firefox sí; Safari menos). Mitigación: detección y mensaje claro. **Sin probar en Mac.**
- **Pesa mucho:** 16 Mbps son unos 2 MB por segundo. Mitigación: 8 Mbps por defecto; vídeos cortos.
- **Duraciones mal calculadas:** una diapositiva con mucho texto pasa muy rápido. Mitigación: regla por palabras (unas 2,5 palabras por segundo) con mínimo 4 s, y tecla para pausar al grabar.
- **Voces:** solo con licencia comercial clara (Kokoro, Apache 2.0). Nunca edge-tts (uso comercial no garantizado, lo ya aprendido en LoboHook).

## 7. Verificación
- `python -m unittest discover tests` en verde.
- Grabar el ejemplo en Chrome y verlo con sonido y sin él. **Sin probar por Darwin hasta que lo haga.**

## 8. Cierre
- [ ] Spec aprobada por Darwin antes de programar
- [ ] Línea añadida a `.brain/decisions.log` al cerrar cada fase
