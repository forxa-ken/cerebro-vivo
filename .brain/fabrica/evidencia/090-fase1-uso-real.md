# 090 fase 1: prueba de uso real (2026-11-18)

Probadora: no construyó la web. Navegador integrado (panel estrecho, ~386 px, luego 800 px) y curl. Servidor `web.py --no-abrir --puerto 8791`, parado al final (confirmado: sin respuesta).

## Resultados
1. Inicio: carga; muestra PENDIENTES completos (0 fallos) y «ÚLTIMA LÍNEA DEL REGISTRO» (la del 2026-11-18, spec 090), más «Archivos sin commitear: 14» y «Commits sin subir: 0». OK.
2. Decisiones: abre solo `decisions/indice.md` (es el único archivo; tabla vacía, correcto). Lecciones: lista 16 archivos, abrí `lecciones/arnes-heredocs.md`, OK. Specs: lista larga (incluye `archivo/`), abrí `specs/090-web-local-del-cerebro.md`, OK.
3. Búsqueda «heredoc»: devuelve resultados (lecciones, decisions.log, plantillas constitution es/en, specs). Abrir un resultado: no pude confirmarlo con claridad (mis clics por coordenadas fueron poco fiables); no probado a fondo.
4. Medir uso: las tres vistas funcionan (Uso de skills 13 de 43; Gasto de la fábrica; Coste del ritual 75 chats). Cada una respondió en pocos segundos, no hizo falta esperar 2 min. Error legible: no probado (no se provocó ningún error).
5. Sin clave: 403; clave errónea: 403; `/api/doc?r=../CLAUDE.md&k=CLAVE` (path-as-is): 404; POST a `/` y a `/api/doc`: 405. OK.
6. Móvil 375 px: scrollWidth = 375 en Inicio, Decisiones, Lecciones, Specs, Biblioteca, Respuestas, Medir uso y Uso de skills. Sin scroll horizontal. OK.

## Cosas feas o confusas
- Los .md se muestran como texto crudo (`# `, `**negrita**`, tablas con `|`), no renderizados. Legible pero feo.
- Al abrir un documento de una lista larga (Specs), el documento queda debajo de la lista; hay que desplazarse para verlo. No hay señal de que se abrió.
- Tablas de Medir uso (Uso de skills) se parten en dos líneas en panel estrecho (la columna «Última vez» baja de línea).
- El cuadro de búsqueda conserva «heredoc» al cambiar de pestaña; confunde un poco.
- No vi indicador de «cargando» en Medir uso (respuesta rápida, no se pudo valorar).
- Arrancar con salida redirigida a archivo no muestra la dirección hasta usar `python -u` (la salida va con búfer): detalle para quien lo lance en segundo plano.

## No probado
Error legible de Medir uso; espera de 2 minutos; Biblioteca y Respuestas más allá de que cargan sin scroll lateral; modo claro; apertura confirmada de un resultado de búsqueda; capturas no guardadas en esta carpeta (solo vistas en pantalla).
