# Spec 022: que no se quede nada suelto ni viejo

- **Estado:** implementada (falta la prueba de Darwin)
- **Fecha:** 2026-11-07
- **Versión prevista:** arnés 1.20.0

## 1. Objetivo
Que Darwin vea lo que está sin commitear y que los documentos no digan cosas falsas con el tiempo. Hoy, comprobado en el chat #18:
- `ignorar_cambios` excluye `.brain/*` y `.claude/*`, y el arranque no avisa de lo suelto allí. Había 11 archivos sin commitear y el resumen no decía nada. Una skill cambiada y sin commitear tampoco se avisaría.
- `arranque.py` archiva cada traspaso en `.brain/archive/traspasos/`, y Git los ve como archivos nuevos que nadie recoge (6 ahora).
- Git sigue `secretos_estado.json`, y cada revisión del historial le cambia la fecha. Los demás archivos de estado están ignorados.
- `poda.py` mueve specs sin hacer commit, y nada recuerda después que quedó a medias.
- `poda.py` solo archiva specs cuyo estado empieza por «implementada», «reemplazada» o «descartada». Las 006 a 009 dicen «hecha y probada» y no se archivan nunca.
- Datos escritos a mano que envejecen:
  - El «sin subir» de los puntos de `pendientes.md`.
  - La versión en `CONTEXTO_PARA_OTRA_CUENTA.md`.
  - La línea «Estado al…» de la plantilla del kit y de la carta.
  - El ZIP de Mac en `CLAUDE.md`, que manda regenerarlo aunque está en pausa.
  - «Sin commitear» en el estado de la spec 005.

## 2. En alcance
- [x] **Aviso de lo suelto.** La línea «Sin commitear» del arranque mira todo el proyecto, con una clave nueva `no_avisar_commit`.
  - `ignorar_cambios` no cambia, porque `cierre.py` lo usa para otra cosa.
  - La lista de `no_avisar_commit` (en `guardianes.json` y en `ajustes_neutros.json`) es: lo que ya ignoraba salvo `.brain/*` y `.claude/*`, más `.brain/decisions.log`, `.brain/traspaso.md`, `.brain/archive/traspasos/*` y `.brain/guardianes/*_estado.json`.
  - Si un proyecto no tiene la clave, el arranque usa esa misma lista por defecto.
  - La línea da el total y hasta 5 rutas: «Sin commitear: 8 archivos (a, b, c, d, e…)».
  - En un archivo movido cuenta la ruta de destino, no el texto «a -> b».
- [x] **`secretos_estado.json` fuera de Git.** Añadirlo a `.gitignore` y a la lista de `instalar.py`, y quitarlo del seguimiento con `git rm --cached` en este repo. El archivo se queda en el disco.
- [x] **Traspasos dentro de Git (decisión de Darwin, 2026-11-07).** Tienen que llegar a otro ordenador, así que no se ignoran. No disparan el aviso, porque saldría uno en cada chat; los recoge la skill `subir-a-github`.
- [x] **Poda.** `es_terminada` acepta también «hecha», manteniendo el filtro de «falta», «pendiente» y «sin probar». Una spec citada en `pendientes.md` sigue sin archivarse. Por eso, a partir de ahora, también se archivarán solas las que ya estén cerradas (las 005 a 009, salvo que algo las cite).
- [x] **Línea del registro.** La skill `cerrar-una-tarea` dice el orden: primero la línea del registro y luego el commit. Si la línea llega después, entra en el siguiente commit. Por eso `decisions.log` no dispara el aviso.
- [x] **Un solo sitio para cada dato.**
  - Skill `pendientes-solo-lo-que-falta`: en un punto no se escribe si está subido o no; eso lo cuenta el arranque. Quitar el «sin subir» del punto 14.
  - Quitar «Estado al…» de `kit-arranque/plantillas/pendientes.md` y de `CARTA_META_ARNES.md`.
  - `CONTEXTO_PARA_OTRA_CUENTA.md`: la versión y lo subido se remiten a `VERSION` y a `git log origin/main`.
  - `CLAUDE.md`: el ZIP de Mac está en pausa y solo se regenera si Darwin lo pide.
  - Spec 005: quitar «sin commitear» de su estado.
- [x] **Lista para subir a GitHub.** Skill corta `subir-a-github`, para cuando Darwin da la orden:
  1. Revisar secretos.
  2. Meter en un commit, sin preguntar, los traspasos (`.brain/archive/traspasos/` y `.brain/traspaso.md`) y `decisions.log`, para que el contexto llegue a otro ordenador.
  3. Mirar lo demás que siga sin commitear, preguntar qué hacer con ello y lanzar las pruebas, que deben estar en verde.
  4. Subir.
  5. Línea en el registro, con su commit local.
- [x] **Git automático en `traspaso-out salgo` (orden de Darwin, 2026-11-07).** Guardián nuevo `guardar_traspaso.py`, para que Claude, Codex y Gemini hagan lo mismo. La skill lo llama después de escribir el traspaso.
  - Mete en un commit la memoria: `.brain/traspaso.md`, `.brain/archive/traspasos/`, `decisions.log`, `pendientes.md` y `.brain/specs/`.
  - No mete el resto (código a medias o trabajo de otros chats). Lo lista en la sección 4 del traspaso y lo dice a Darwin, que decide.
  - Pasa la revisión de secretos antes del commit. Si encuentra algo, no hace commit y lo dice.
  - Si Git falla o no hay remoto, lo dice claro y el traspaso sigue adelante.
  - **Sube a GitHub después del commit (decisión de Darwin, 2026-11-07).** Añade una excepción a la regla 9 de la constitución y de su plantilla: `traspaso-out salgo` sube su commit de memoria sin más orden.
  - Git sube todos los commits pendientes, no solo el último. Si hay otros commits sin subir, no sube: los lista y pregunta a Darwin, porque pueden llevar código sin probar. Mientras tanto, el commit de memoria queda hecho en local.
  - Sube solo a la rama actual con su remoto y nunca fuerza. Si GitHub rechaza la subida (por ejemplo, porque otro ordenador subió antes), lo dice claro y no mezcla nada por su cuenta.
  - Se documenta en `MANUAL_DE_USO.md`, en `CEREBRO_VIVO.md` y en la skill `traspaso-out`.
- [x] **Lo suelto de hoy.** Commit aparte, antes de programar, con el movimiento de las specs 018-020 y su índice, y los traspasos archivados.

## 3. Fuera de alcance
- Hacer commits automáticos al abrir o cerrar un chat. Commitear sigue siendo decisión de Darwin; el arranque solo avisa. Las únicas excepciones son `traspaso-out salgo` y el paso 2 de `subir-a-github`, que solo ocurren cuando Darwin los pide.
- Git automático en `traspaso-in`: se usa en cada chat largo y llenaría el historial. Para cambiar de ordenador con la misma IA, Darwin dice «sube» o usa `traspaso-out`.
- Sincronizar la memoria automática de Claude (`C:\Users\darwi\.claude\projects\…\memory\`), que vive fuera del repositorio y no viaja con Git.
- Un guardián que detecte textos viejos en cualquier documento. Saldría caro y daría falsos avisos.
- Archivar las specs 010 a 013 y 015: siguen citadas o esperando prueba.
- Reescribir el estado de las specs antiguas, salvo la 005.
- Los restos de LoboHook en `_template.md` y en `cerrar-una-tarea` (`venv\Scripts`): son del grupo C.
- Actualizar proyectos reales y regenerar el ZIP de Mac.
- Subir a GitHub sin la orden de Darwin.

## 4. Plan de implementación
1. Commit aparte de lo suelto de hoy (specs 018-020, su índice y los traspasos archivados).
2. `arranque.py`: clave `no_avisar_commit`, total de archivos y ruta de destino en los movidos. Añadir la clave a `guardianes.json` y `ajustes_neutros.json`.
3. `poda.py`: aceptar «hecha» en `es_terminada`.
4. `.gitignore`, `instalar.py` y `git rm --cached` de `secretos_estado.json`.
5. Textos: `cerrar-una-tarea`, `pendientes-solo-lo-que-falta`, plantilla, carta, `CONTEXTO_PARA_OTRA_CUENTA.md`, `CLAUDE.md`, spec 005 y punto 14.
6. Skill `subir-a-github` con su ficha en el índice de skills.
7. Guardián `guardar_traspaso.py` y paso nuevo en `traspaso-out salgo`.
7b. `MANUAL_DE_USO.md` y `CEREBRO_VIVO.md`: el aviso, la skill nueva y el Git automático.
8. `VERSION` 1.20.0, `CAMBIOS.md` y `python generar_manifiesto.py`. Sin ZIP de Mac.

## 5. Plan de verificación
- Pruebas: `python -m unittest discover tests` (todo en verde).
- Pruebas nuevas, en un repositorio Git temporal:
  - Un archivo suelto en `.brain/specs/` o `.claude/skills/` sale en el aviso.
  - `decisions.log`, un traspaso archivado y `secretos_estado.json` no salen.
  - Un archivo movido sale con su ruta de destino.
  - Un proyecto sin la clave `no_avisar_commit` funciona con la lista por defecto.
  - El total es correcto con más de 5 archivos.
- Pruebas nuevas de `poda.py`: «hecha y probada» se archiva; «hecha, falta probar» no; una spec citada en pendientes no.
- Prueba nueva: `instalar.py` deja las líneas nuevas en `.gitignore`, y la plantilla ya no lleva «Estado al».
- Comprobar que `secretos.py` funciona sin `secretos_estado.json` en un clon limpio.
- Pruebas nuevas de `guardar_traspaso.py`, en un repositorio Git temporal: el commit lleva la memoria y no el código suelto; con un secreto no hace commit; sin remoto o con Git fallando, avisa y no rompe el traspaso; con otros commits pendientes no sube y los lista; con un remoto local de prueba sube solo la rama actual y sin forzar. Ninguna prueba toca GitHub.
- **Sigue en Git:** tras los cambios, `git check-ignore` no marca `.brain/archive/traspasos/` ni `.brain/traspaso.md`.
- **Lo que debe probar Darwin:** abrir un chat con algo sin commitear en `.brain/` y ver que el resumen lo dice. Después, en un proyecto real con `/actualizar`, ver si el aviso le resulta útil o le estorba. En LoboHook saldrá trabajo de otros chats, y eso es correcto.

## 6. Cierre
- [x] Spec aprobada por Darwin antes de programar.
- [x] Darwin decide: `traspaso-out salgo` hace commit y también sube a GitHub.
- [x] Línea añadida a `.brain/decisions.log`.
