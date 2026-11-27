# Anexo a la spec 095: cómo nacen las skills en el trabajo real (caso ProMaps)

- **Fecha:** 2026-11-27. **Estado:** idea para la **fase 2** de la spec 095; no se construye hasta tener los datos del pendiente 65 (tres chats con el sugeridor).
- **Fuente:** las skills `leer-wowhead-forever` y `volcar-del-navegador` de ProMaps (revisadas por el chat #46) y lo que contó Darwin sobre por qué nacieron.

## Cómo nació `leer-wowhead-forever` (según Darwin)
1. **Necesidad:** llenar la base de datos con datos fiables y completos, con una sola fuente (Wowhead).
2. **Primero reglas** sueltas en la constitución. **No funcionó:** la IA se saltaba pasos y no hacía todo lo pedido.
3. **Después skill:** Darwin detalló el procedimiento paso a paso, donde la IA lo sigue en orden.
4. **Crecimiento por acumulación:** cada fallo del trabajo (captcha 405, comentarios sin leer, dudosas dadas por revisadas) añadió un párrafo a la skill. Hoy pesa 6,8 KB más un `referencia.md`.

`volcar-del-navegador` nació de un error resuelto («Failed to fetch» a localhost desde Wowhead); su ficha cita la lección de `extraccion.md` (chat #153) como fuente.

## Lo que enseña para el detector
- Una **regla que la IA incumple** (Darwin tiene que repetirla o reclamarla) es la señal más fuerte de que falta una skill: pasa de «regla en la constitución» a «procedimiento con pasos».
- Otra señal: una **lección apuntada que describe un procedimiento que funciona** («lo que funciona es…», pasos) y se ha citado en 2 o más chats. Candidata a **promover de lección a skill**.
- Una **regla** no es un **procedimiento**: lo que sea de «siempre/nunca» va a la constitución; lo que tenga pasos en orden, a una skill. El detector debe distinguirlos.
- Las skills **crecen**: el aviso de «skill demasiado larga» (spec 095, sección 4) hace falta de verdad. Conviene sugerir troceo (`referencia.md` aparte) antes de que se llenen.

## Cómo sería barato (sin IA, sin llamadas)
- Contar en el registro del chat cuántas veces Darwin repite o corrige el mismo tema (ya lo hace el sugeridor con las correcciones) y cruzarlo con el tema de una lección existente.
- Al cerrar un **hito** (módulo, encargo de fábrica o tarea grande con pruebas en verde), una sola pregunta a la IA del chat: «¿hay aquí un procedimiento reutilizable?». La respuesta va entera a `propuestas.md` y la aprueba Darwin. Nada entra solo.

## Sin confirmar
- Si en ProMaps la lección precedió a cada skill o se escribieron a la vez: se dedujo de la ficha, no del historial de Git.

## Experimento en ProMaps (encargo enviado el 2026-11-27 al chat Mappro #156)
- **Qué se prueba:** que una skill larga con tres listas solapadas, rehecha como «espina» corta con puertas enlazadas a `referencia.md` más dos frenos de código, deja de perder pasos. Los pasos que se saltaba, según Darwin: leer los comentarios de la ficha y mirar el mapa (coordenadas).
- **Los dos frenos:** (a) `revisar_zona.py` pone en el informe, por cada misión dudosa, las líneas del mapa (`M`) y los comentarios (`C`); (b) `zonas.py` no deja cerrar sin una nota por dudosa en `pendientes-misiones.md` con lo que dijeron el mapa y los comentarios.
- **Cómo se mide:** en la siguiente zona de ProMaps, contar las dudosas sin nota de mapa o comentarios (antes del cambio y después) y si Darwin tuvo que reclamar esos pasos. Resultado en una nota del chat de ProMaps (`.brain/notas-chats/` de ese proyecto).
- **Qué decide:** si funciona, cerebro-vivo escribe una spec de plantilla general de skills largas (espina + módulos + índice). Esa plantilla también resolvería el troceo de `directora-de-fabrica`, `revisor-de-spec` y `fabrica`. Si no funciona, se descarta o se cambia el enfoque.
- **Estado:** enviado, en cola (el chat estaba trabajando). Sin respuesta todavía.
