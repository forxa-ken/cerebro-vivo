# Cambios del arnés

Una línea por versión. Subir `VERSION`, anotar aquí y lanzar `python generar_manifiesto.py` antes de dar por buena una mejora.

## 1.0.0 (2026-10-31)
- Primer repositorio propio del meta-arnés (spec 087 de LoboHook). Trae todo lo hecho hasta hoy: guardianes (incluido el **modo auto**, `cerrar.py --indices/--hecho`, `indices.py`, `notas_abiertas.py`), manual `CEREBRO_VIVO.md` y carta, plantillas, kit de arranque y de traducción, skills genéricas (con `/prompt-inicial`), pruebas del método y el plugin `plantilla-prompt` 0.2.0 (`/plantilla`).
- Nuevo: `actualizar_arnes.py` (en cada proyecto) y `actualizar.py` (en este repo) para traer las mejoras sin pisar lo modificado a mano.

## 1.1.0 (2026-11-01)
- Nuevo guardián `medir.py` (spec 001): mide por chat tokens nuevos, salida, arranque, mensajes tuyos y correcciones; `--comparar RUTA_CON RUTA_SIN` enseña las medias de dos proyectos y la diferencia en %. Solo lectura. Con su prueba `test_medir.py`.
- (1.1.0, antes de repartir) `medir.py` ignora los avisos automáticos pegados delante del mensaje y admite `--tarea TEXTO` para comparar solo un tipo de tarea.

## 1.2.0 (2026-11-01)
- **Modo ligero** (spec 002): en una tarea pequeña (hasta 2 archivos, ninguno sensible, sin tocar `.brain/`) y con las pruebas en verde, `cierre.py` escribe él mismo la línea del registro («Claude (auto)») y no obliga a la IA a dar otra vuelta. Ajustes `modo_ligero_activo` y `modo_ligero` en `guardianes.json` (las claves nuevas se proponen, no se pisan).
- El aviso de cierre normal recuerda que la línea se escribe solo con las pruebas en verde.
- El resumen de arranque omite las líneas «sin novedad».
- Prueba nueva `test_modo_ligero.py`.
- (1.2.0) El `CLAUDE.md` que instala el kit para Claude dice ahora que en tareas pequeñas NO se escriba la línea del registro (la pone el hook `Stop`); sin esto la IA la escribía antes y el modo ligero no ahorraba (medición de la spec 002).

## 1.3.0 (2026-11-01)
- `medir.py` (spec 003): columna **Coste** ponderado por precio (entrada ×1, escritura de caché ×1,25, lectura ×0,1, salida ×5), `--desglose ID` (coste mensaje a mensaje con las herramientas usadas) y `--comparar` que solo compara chats con la misma caché (fría con fría, caliente con caliente). Los pesos son ajustables (`PESOS`).

## 1.3.1 (2026-11-01)
- Recortes del arranque (spec 003): el `CLAUDE.md` del kit ya no manda leer constitución y pendientes en tareas pequeñas; el aviso del arranque pide una línea si no hay nada que requiera acción. `cierre.py` también cierra solo cuando la IA editó con la terminal (usa lo que git ve cambiado) y no repite la misma línea automática.

## 1.4.0 (2026-11-01)
- Se quitan, por decisión de Darwin, herramientas poco útiles (spec 005): el medidor `uso_tokens.py` (lo hace `medir.py`, que ahora lleva dentro lo que necesitaba), el **modo auto** (`modo_auto.py`, su aviso automático `PreToolUse`, sus ajustes y su prueba) y el **plugin `/plantilla`** (`plantilla-prompt/` y el catálogo `.claude-plugin/`; queda `/prompt-inicial`). El instalador deja de crearlos. Los proyectos que ya los tengan no los pierden: el actualizador no borra nada.

## 1.4.1 (2026-11-01)
- `CEREBRO_VIVO.md`: encargo con autoevaluación (§4) y dos preguntas de revisión en el cierre (§6, paso 7), tomados de la guía maestra. Sin cambios de código.

## 1.4.2 (2026-11-01)
- Spec 006: `/prompt-inicial` vuelve a ser solo la plantilla para escribir un encargo; nuevas skills `/resumen` (cuenta el estado, solo lectura) y `/pendiente` (menú de listas: programar, prueba, acciones, specs). Solo Claude Code hasta el pendiente 7 (`.agents/skills/`).

## 1.5.0 (2026-11-01)
- Spec 007: el instalador crea `.brain/architecture/objetivo.md` (los índices lo enlazan primero y la constitución manda escribir ahí todo objetivo) y, si el proyecto usa Codex (`AGENTS.md`), instalador y actualizador copian las skills también a `.agents/skills/`.

## 1.5.1 (2026-11-01)
- `/pendiente`: en «Esperando tu prueba» y «Acciones tuyas» describe cada punto completo (qué es, qué tienes que hacer paso a paso y qué debe pasar si va bien).

## 1.6.0 (2026-11-01)
- Spec 008: `actualizar_arnes.py --migrar-objetivo` (con `--simular`) crea `objetivo.md`, lo enlaza en los índices de entrada y añade la regla a la constitución en proyectos ya instalados. Solo añade, guarda copia y es idempotente.

## 1.7.0 (2026-11-01)
- Se recupera el panel `/plantilla` (spec 009): `plantilla-prompt/` 0.3.0 y el catálogo `.claude-plugin/`, tal como estaban antes de la 1.4.0. Sus botones «Retomar: N» pasan a un solo «Ver los pendientes (N)» que pone `/pendiente` en el chat, y «Resumen del estado» pone `/resumen`. Es un plugin de Claude Code: se instala una vez por equipo (ver su README y la guía de instalación) y `actualizar_arnes.py` no lo reparte. Prueba nueva `test_plugin_plantilla.py`.

## 1.8.0 (2026-11-03)
- Spec 010: nueva skill `cambio-de-ia` (en Codex, `$cambio-de-ia`) para pasar el trabajo entre Claude, Gemini y Codex: al salir escribe `.brain/traspaso.md` mirando git y las pruebas; al entrar lo lee, lo cuenta y lo archiva. La plantilla de traspaso lleva ahora IA que lo escribe, IA que sigue y hora. Los archivos de entrada (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`) de nivel medio y completo llevan la regla de leer el traspaso y usar la skill.

## 1.8.1 (2026-11-03)
- La prueba `test_cambio_de_ia.py` ya no falla en los proyectos: comprueba el manifiesto solo si existe (solo está en el repo del arnés).

## 1.9.0 (2026-11-03)
- Spec 011: comandos fijos y descriptivos. **`traspaso-in`** (de un chat al chat nuevo con la misma IA) sustituye a `traspaso-entre-chats`; **`traspaso-out`** (de una IA a otra) sustituye a `cambio-de-ia`. Los dos llevan los modos `salgo` y `entro` (`/traspaso-in salgo`; en Codex, `$traspaso-in salgo`). La regla de los archivos de entrada, la plantilla de traspaso y el manual usan los nombres nuevos.
- Los proyectos que ya tenían `cambio-de-ia` o `traspaso-entre-chats` las conservan al actualizar (el actualizador no borra): se pueden borrar a mano de `.claude/skills/` y `.agents/skills/`.

## 1.9.1 (2026-11-03)
- Arreglo: `test_arranque_imprime_json_visible_y_de_contexto` (en `test_cerebro_indices.py`) ejecutaba el `arranque.py` real y archivaba el `.brain/traspaso.md` del proyecto cada vez que se corrían las pruebas. Ahora lleva `CEREBRO_NO_ARCHIVAR_TRASPASO=1`.

## 1.9.2 (2026-11-03)
- Arreglo: `test_manual_no_espera_stdin` se colgaba (60 s y error) cuando había un `.brain/traspaso.md` largo, porque no leía la salida y la tubería se llenaba. Ahora la salida va a un archivo.

## 1.10.0 (2026-11-03)
- Spec 012: el aviso de chat largo (`longitud.py`, que ya existía) ahora también le pide a la IA abrir ella el chat nuevo con `start_session` y separarlo enseguida con `detach_session`, para que quede al mismo nivel y no colgado del anterior; le dice a Darwin el nombre del chat nuevo. Sin la herramienta (Codex, Gemini) queda la frase de traspaso a mano. Sin guardián nuevo ni ajustes nuevos.

## 1.11.0 (2026-11-03)
- Soporte para Mac (spec 013), **sin probar en un Mac real**: nuevo `instalar_kit.command` (doble clic; avisa si falta Python o tkinter); el instalador escribe `python3` en los ganchos cuando la máquina no tiene `python` (en Windows no cambia nada); `instalar_gui.py` avisa con claridad si falta tkinter; la pista de `librerias.py` y la conversión de fin de línea del actualizador tienen en cuenta Mac. Manual y guía de instalación con la sección de Mac. Prueba nueva `test_soporte_mac.py` (simula Mac; no sustituye a probarlo allí).

## 1.12.0 (2026-11-04)
- `/traspaso-in salgo` ahora abre el chat nuevo él mismo en Claude Code de escritorio: escribe el traspaso, lo abre con `start_session` (encargo: leer el traspaso y `traspaso-in entro`) y lo separa enseguida con `detach_session` para que quede al mismo nivel; dice a Darwin el nombre. Sin esa herramienta (Codex, Gemini) sigue a mano. Prueba nueva en `test_traspaso_in_out.py`.

## 1.13.0 (2026-11-04)
- El instalador (spec 015) ya no deja el kit a medias en un proyecto que tiene su propio `CLAUDE.md`/`GEMINI.md`/`AGENTS.md` o `.claude/settings.json`: **añade lo suyo sin quitar nada**. Al índice le agrega al final un bloque marcado (`cerebro-vivo:inicio/fin`) y guarda copia íntegra del original en `.brain/archive/adoptado/`; a los ajustes les fusiona los hooks que falten y une `permissions.deny`; si el JSON está roto no lo toca y avisa. Copia `.antes-de-cerebro-vivo` de lo modificado, idempotente, `--simular` no escribe. Avisa si ya había un hook propio en el mismo evento.
- Skill nueva `adoptar-indice-existente`: la IA reparte lo que el proyecto ya tenía en `objetivo`, `constitution`, `decisions`, `referencias` y `pendientes` con el visto bueno del dueño y sin descartar nada. Probado solo en Windows.
- Herramienta nueva `generar_zip_mac.py`: genera el ZIP de prueba para Mac con la versión actual (el anterior pasa a `anteriores/`). Se lanza tras cada cambio del arnés. ZIP 1.13.0 hecho; en Mac sigue sin probarse.

## 1.14.0 (2026-11-04)
- Revisión de los índices de IA (spec 016): guardián `revisar_indices.py` (solo lectura) que informa de referencias rotas, deriva entre CLAUDE/GEMINI/AGENTS, secciones pesadas, fechas viejas y párrafos ya presentes en `.brain/`; ignora el bloque que añade el instalador y lo que el método crea al usarse. Lo descartado se anota en `revision_indices.json` y no se repite. El arranque avisa en una línea si un índice pasa el 80 % del tope, tiene referencias rotas o lleva más de 60 días sin revisarse (`revision_indices_activa` lo apaga).
- Skill nueva `revisar-indices-de-ia`: **doble pasada** contra falsos positivos (buscar y refutar, la segunda sin el razonamiento de la primera), tabla a Darwin antes de escribir y, con su visto bueno, lo retirado se mueve a `.brain/archive/indices/`, no se borra. Probado solo en Windows.

## 1.14.1 (2026-11-04)
- Skill nueva `adopta`: atajo `/adopta` de `adoptar-indice-existente`, para no tener que escribir la frase entera.

## 1.15.0 (2026-11-04)
- Skill nueva `acorta` (spec 017): atajo `/acorta` que baja CLAUDE/GEMINI/AGENTS al tope sustituyendo secciones pesadas por enlaces, con tabla y visto bueno de Darwin antes de escribir. Sin código nuevo; usa `revisar_indices.py`. Sin probar en un proyecto real.

## 1.16.0 (2026-11-04)
- Guardián nuevo `archivos_gordos.py` (spec 018): tope de 8 KB (`tope_archivo_memoria_bytes`) para los archivos de lectura de `.brain/`; el arranque avisa al 80 %. Skill nueva `trocea` (`/trocea`): divide por temas con nombre, copia íntegra en `archive/troceado/`, índice en `architecture/`. Las claves nuevas de `guardianes.json` se proponen a los proyectos existentes; sin ellas el guardián usa 8 KB. Sin probar en un proyecto real.

- (1.16.0) Manual: sección 3 ter de `MANUAL_DE_USO.md` y 9 quinquies de `CEREBRO_VIVO.md` con `/adopta`, `/acorta`, `/trocea`, `archivos_gordos.py` y el orden de uso.

## 1.16.1 (2026-11-04)
- Prueba `test_arranque.py`: los índices que comprueba son los de `indices_entrada` de `guardianes.json` (antes siempre CLAUDE/GEMINI/AGENTS). Así un `AGENTS.md` ajeno al método (p. ej. el de Antigravity en Guild Control Forever, solo para traducciones y que no se edita) ya no da 2 pruebas rojas.
- Manual: `/adopta`, `/acorta` y `/trocea` probados con éxito en un proyecto real (Guild Control Forever: CLAUDE.md 52 KB a 3,3 KB, referencias.md 47 KB a 13 archivos por tema, 0 líneas perdidas).

## 1.17.0 (2026-11-04)
- Actualizar con un aviso (spec 019): el arranque avisa cuando el repo del arnés (`arnes_repo`) tiene una versión mayor que la instalada (`aviso_arnes_activo` lo apaga); nueva skill `/actualizar` (simula, cuenta en llano, pide el sí, aplica). El actualizador ahora AÑADE a `guardianes.json` las claves que faltan (sin cambiar las existentes), anota `arnes_repo` si falta y completa las fichas de skills de `.brain/experiencia/indice.md`. Dos pruebas de `test_kit_arranque.py` solo corren en el repo del arnés.

## 1.18.0 (2026-11-04)
- `/adopta` encadena adoptar, acortar y trocear (spec 020), pidiendo el sí de Darwin en cada tabla; el instalador anota en `pendientes.md` y en su aviso final «escribe /adopta». Sin probar el encadenado completo en un proyecto real.

## 1.18.1 (2026-11-04)
- El aviso de arranque de índices de IA pasados de tope dice «escribe /adopta» (antes solo «revisa los índices»); lo notó Darwin al instalar el kit en Guild Control.

## 1.18.2 (2026-11-04)
- `/traspaso-in` sin palabra equivale a `salgo` y abre el chat nuevo (en LoboHook #79 Darwin lo escribió solo, la IA dio el resumen y no abrió el chat).

## 1.19.0 (2026-11-07)
- **Actualizador fiable (spec 021).** Lo retirado del arnés (lista `retirados` del manifiesto, que `generar_manifiesto.py` mantiene solo) sale de los proyectos a la copia de seguridad, con su fila del índice de skills; lo modificado a mano se lista y no se toca.
- Cada archivo se escribe de forma atómica: un corte deja el viejo o el nuevo entero, y al relanzar se completa.
- El registro anota `sin_aplicar` con lo que se quedó viejo, y el informe dice «aplicada salvo N archivos».
- Antes de escribir se comprueba la huella de cada archivo contra el manifiesto, también en el kit.
- El kit anota `nivel` en `.brain/arnes_instalado.json`; un proyecto de nivel ligero o medio no recibe nada y se le dice cómo subir a completo (punto 14).
- `--simular` anuncia todo lo que hará: retirados, filas y fichas del índice, y lo que queda sin aplicar.
- `README.md` y el manual ya no dicen que las claves nuevas «solo se proponen».

## 1.19.1 (2026-11-07)
- `traspaso-in entro` empieza separándose del chat anterior si sigue colgado de él (`get_session` y `detach_session` con `self`). Cubre el chat abierto desde una tarjeta, que el chat viejo no separaba (punto 20). El aviso de `longitud.py` manda ya ejecutar `traspaso-in entro` en el encargo del chat nuevo.

## 1.20.0 (2026-11-07)
- **Nada suelto ni viejo (spec 022).** La línea «Sin commitear» del arranque mira también `.brain/` y `.claude/`, salvo lo que se genera solo (clave nueva `no_avisar_commit`), y da el total de archivos.
- **`traspaso-out salgo` guarda y sube la memoria** con el guardián nuevo `guardar_traspaso.py`: commit de traspaso, traspasos archivados, registro, pendientes y specs, y subida a GitHub. El código suelto no entra. Se para con un secreto o con otros commits sin subir que no son de memoria (`--subir-todo` con el sí del dueño). Nunca fuerza ni mezcla. La regla 9 de la constitución y su plantilla recogen esta excepción.
- Skill nueva `subir-a-github`: lo que se repasa cuando el dueño ordena subir.
- `poda.py` archiva también las specs «hecha», salvo si falta algo o siguen citadas en pendientes.
- `secretos_estado.json` sale de Git. Los traspasos archivados siguen dentro.
- Fuera los datos a mano que envejecen: «Estado al…» en la plantilla y la carta. La skill de pendientes pide no escribir si un punto está subido.

## 1.20.1 (2026-11-07)

## 1.20.2 (2026-11-07)

## 1.21.0 (2026-11-07)
- Skill nueva `/version` (spec 023): dice qué versión del arnés tiene el proyecto, si hay una más nueva y cómo actualizar. Si el proyecto es anterior a la 1.17.0 y `/actualizar` no existe, da los comandos para actualizar a mano la primera vez. Solo lee.

## 1.22.0 (2026-11-07)
- Avisos en inglés (spec 024, fase 2): ajuste nuevo `"idioma": "es" | "en"` en `guardianes.json` (si falta, español: los proyectos que ya existen no cambian). Guardián nuevo `textos.py` con unos 250 mensajes en los dos idiomas; lo usan los 17 guardianes (arranque, cierre, traspaso, actualizador, secretos, librerías, base de datos, poda, medir…). Quedan en español la ayuda de `--help` y lo que se escribe dentro de los archivos de memoria (fase 3). El kit de arranque guarda el idioma elegido («English» → `en`). Prueba nueva `test_textos.py` (ninguna clave falta ni se repite en ningún idioma, y todos los guardianes usan `textos.py`). Los nombres de archivos y comandos siguen en español.

## 1.23.0 (2026-11-07)
- Chat nuevo solo, como regla común (spec 025): al pasar el aviso de chat largo, la IA escribe el traspaso y abre ella misma el chat nuevo (`start_session` + `detach_session`); el aviso le prohíbe decir que la app lo rechaza sin haberlo intentado y solo deja la frase para pegar si la llamada falla. Ajuste nuevo `chat_nuevo_auto` en `guardianes.json` (por defecto sí; el actualizador lo añade). Comando nuevo `/chat-nuevo si|no|estado` (`longitud.py --chat-nuevo`). La skill `traspaso-in` y la plantilla del índice dicen lo mismo.

## 1.23.1 (2026-11-07)
- El índice de cada IA (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`, que salen de la misma plantilla) lleva ahora la frase de permiso fijo: el dueño autoriza abrir el chat nuevo de forma automática, para que el filtro del modo auto no deniegue `start_session` (spec 025). Solo llega a proyectos que se instalen desde ahora; en uno ya instalado hay que añadir la frase a mano, porque el actualizador no toca los índices.

## 1.23.2 (2026-11-07)
- `traspaso-in entro`: el chat nuevo debe llamar siempre a `detach_session` con `self` aunque crea que la app lo rechazará (en Guild Control Forever #18, nacido de una tarjeta, se saltó el paso y quedó colgado del #17).

## 1.24.0 (2026-11-07)
- Lecciones apuntadas en el momento y traspaso corto (spec 026). Nuevo guardián `hitos.py` (lo llama `cierre.py`): si hay un error resuelto, cambios en archivos delicados (`lecciones_vigiladas`) o una modificación grande (`hitos_max_archivos`), no deja cerrar hasta apuntar la lección con `lecciones.py` (`/leccion`) o `lecciones.py ninguna "motivo"`. Las lecciones viven en `.brain/lecciones/TEMA.md` con índice; el arranque las lista. El traspaso que carga el chat nuevo es corto (`traspaso.md`, ~1500 caracteres); el historial entero va a `traspaso-completo.md`, se archiva con el mismo sello y se consulta con `/memoria-traspaso`. Plantillas, `traspaso-in`/`traspaso-out`, `guardar_traspaso.py` y textos es/en actualizados. Pruebas `test_lecciones.py` y `test_hitos.py`. Al actualizar, mover a mano `lecciones_video.md` a `.brain/lecciones/video.md` (no hay migración automática).

## 1.25.0 (2026-11-08)
- Edición inglesa de lo que lee la IA y la persona (spec 024, fase 3). Cada `X.md` puede tener su `X.en.md`: las 28 skills (`SKILL.en.md`), `CEREBRO_VIVO.en.md`, `PLANTILLA_TRASPASO.en.md`, `PLANTILLA_NOTA_CHAT.en.md` y las 9 plantillas del kit (`plantillas/*.en.md`, constitución, índice de IA, pendientes…). `actualizar_arnes.py` copia la edición inglesa en el sitio de `X.md` solo si el proyecto tiene `"idioma": "en"` en `guardianes.json` (en español no copia las `.en`; cambiar de idioma y actualizar basta); el manifiesto guarda la huella de las dos. El instalador, con `--idioma English`, monta constitución, índices de IA, pendientes y manual en inglés. Nombres de archivos, carpetas y comandos siguen en español. En este repo: `README.en.md` y `MANUAL_DE_USO.en.md`, enlazados desde los originales. Pruebas nuevas `test_ediciones_en.py` (se reparte) y `test_arnes_paridad_en.py` (esqueleto, marcadores y comandos iguales).

## 1.25.1 (2026-11-08)
- La prueba `test_todos_los_guardianes_usan_textos` solo revisa los guardianes que reparte el arnés (los de `manifiesto.json` o `arnes_instalado.json`); un guardián propio de un proyecto, como el modo auto de LoboHook, ya no la pone en rojo.

## 1.25.2 (2026-11-08)
- Edición inglesa de los dos README que reparte el arnés: `kit-arranque/README.en.md` y `kit-traduccion/README.en.md` (spec 024, fase 3). El instalador con `--idioma English --traduccion` copia el README inglés del kit de traducción. Prueba de paridad ampliada.

## 1.25.3 (2026-11-08)
- Plantilla de spec en inglés (`.brain/specs/_template.en.md`): un proyecto con `"idioma": "en"` la recibe en el sitio de `_template.md` (actualizador e instalador), así las specs nuevas salen en inglés. `test_cada_spec_declara_su_estado` acepta «Status». Prueba de paridad ampliada.

## 1.26.0 (2026-11-08)
- La ayuda de `--help` de `cerrar.py`, `medir.py` y `actualizar_arnes.py` sale en el idioma del proyecto (claves `ayuda_*` de `textos.py`, es/en).

## 1.26.1 (2026-11-08)
- Plantilla de pruebas en inglés (`.brain/pruebas/_plantilla.en.md`): un proyecto con `"idioma": "en"` la recibe en el sitio de `_plantilla.md`. Prueba de paridad ampliada. Con esto la edición inglesa del arnés queda completa (salvo `CAMBIOS.md`, las specs de este repo y la carta maestra, por decisión).

## 1.26.2 (2026-11-08)
- `traspaso-in salgo` (es/en): el traspaso se escribe una sola vez; si ya existe de este chat y nada cambió, no se reescribe (punto 20, b2). El resto del punto 20 ya estaba hecho: probar `start_session` y no decir «rechazada» sin llamarla (1.23.0 y 1.23.1), aviso de chat largo una vez por tramo de 100k (spec 056) y `detach_session` al entrar (1.23.2).

## 1.27.0 (2026-11-08)
- Guardián nuevo `eventos_chat.py` (spec 027, punto 28): hook `PreToolUse` con memoria del chat. Recuerda las instalaciones de librerías del chat y, antes de `git push`, revisa él solo las nuevas con `librerias.py` (que gana `consultar()`); limpio no molesta, vulnerabilidad conocida detiene el push (`permitir "motivo"` para seguir, queda en el registro), sin red no bloquea y lo recuerda en el siguiente push. Solo Python; de npm/cargo/go avisa una vez. Ajustes nuevos en `guardianes.json` (`eventos_chat_*`), textos es/en, instalador y prueba `test_eventos_chat.py`. Los proyectos ya instalados reciben el guardián con `/actualizar`, pero el hook en `.claude/settings.json` se añade volviendo a lanzar el instalador del kit.

## 1.27.1 (2026-11-08)
- Dos arreglos del informe de poda (spec 028, puntos 3.1 y 3.3). El actualizador (`actualizar_arnes.py`) ahora añade a `.claude/settings.json` del proyecto los hooks de guardianes que le faltan (`completar_hooks`; no quita ni cambia los que hay, respeta el `python`/`python3` del proyecto, guarda copia y avisa en el informe), así que un guardián nuevo como `eventos_chat.py` queda activo con `/actualizar` sin volver a lanzar el instalador (reiniciar Claude Code). Y el hook de `eventos_chat.py` solo vigila `Bash` y `PowerShell` (se quitan `Edit`, `Write` y `MultiEdit`: ahorra una ejecución por edición). Pruebas nuevas en `test_arnes_actualizar.py`.

## 1.28.0 (2026-11-08)
- `medir.py --skills` (informe 028, 3.2): uso real de cada skill, leído de los registros de los chats (llamadas a la herramienta Skill y comandos `/skill`; las no usadas salen con 0, con chats y última fecha). Sustituye al campo «Veces», que nadie actualizaba y marcaba 0 en todas: las 29 skills (es/en) ahora apuntan al comando en su sección «Usada». Solo mira los chats de la carpeta pedida (`--proyecto RUTA` para otro). Textos es/en y pruebas nuevas en `test_medir.py`.

## 1.28.1 (2026-11-08)
- Plantilla de constitución (es/en) con una regla nueva (informe 028, 3.5): los bloques de código se escriben con Edit/Write y no con scripts Python en heredoc, y tras editar con script se comprueba la sintaxis. Falló tres veces en cerebro-vivo. Solo la reciben los proyectos nuevos; los ya instalados tienen su propia constitución. Sin cambios de código.

## 1.28.2 (2026-11-08)
- Informe 028, 3.4: `tests/test_esperando_prueba.py` comprueba de punta a punta, con el arnés real instalado en una carpeta temporal, los puntos 14 (actualizador: repone lo borrado, respeta lo tocado, retira a `copias_arnes`), 21 (`traspaso-out salgo` sube la memoria y lista el código suelto) y 26 (`/version`: datos que lee y aviso de versión nueva). Solo pruebas; el código no cambia.

## 1.28.3 (2026-11-08)
- Arreglo de un fallo de 1.28.2: la prueba nueva dependia de `VERSION` y `CAMBIOS.md`, que solo existen en este repo, y se repartio a los proyectos donde fallaba. Se renombra a `tests/test_arnes_esperando_prueba.py` (las `test_arnes_*` no se reparten) y la vieja pasa a retirados: el actualizador la saca de los proyectos que ya la recibieron, con copia.

## 1.28.4 (2026-11-08)
- Spec 029, punto 28 reabierto: el guardián con memoria del chat (`eventos_chat.py`) no veía las librerías instaladas en el `.venv` del proyecto y dejaba pasar `git push` con una vulnerable (fallo hallado por Modelo #59). Ahora pregunta la versión, por este orden, al Python del `.venv`/`venv` del proyecto, a la versión fijada en el comando (`nombre==versión`) y al Python del hook; y si no la encuentra en ninguno **avisa una vez** en vez de callar (texto nuevo `eventos_chat_sin_version`, es/en). Pruebas con un `.venv` real.

## 1.28.5 (2026-11-08)
- Spec 030, hallazgos de Modelo #59 sobre el guardián con memoria del chat (`eventos_chat.py`): ya no recuerda para siempre una librería que no está instalada (desinstalada, o cuya orden se detuvo antes de ejecutarse): la olvida sola si hay `.venv` y no está ni en él ni en el Python del hook; y `2>&1`, `>fichero` y similares ya no se toman por una librería (de ahí el «(2)» del aviso). Prueba con `.venv` real.

## 1.28.6 (2026-11-08)
- Spec 031, punto 33: el aviso de cierre (`cierre.py`) ya no atribuye al chat los cambios sin commitear que trajo `/actualizar` u otro chat. Si el chat editó archivos con Edit/Write, solo cuentan esos; si trabajó solo con la terminal, todo sigue como antes. Límite: lo escrito con la terminal en un chat que también usó Edit puede no avisarse.

## 1.28.7 (2026-11-08)
- Arreglo de `hitos.py` (hallado por Modelo #61): reconocía que se había apuntado la lección (`lecciones.py`) solo si se lanzaba con Bash; con PowerShell, habitual en Windows, el aviso «hito sin lección» se repetía aunque ya estuviera apuntada. Ahora vale también PowerShell. Prueba nueva.

## 1.28.8 (2026-11-08)
- Arreglo de `actualizar_arnes.py` (hallado en LoboHook): al completar el hook de un guardián nuevo, si el proyecto usa el Python del venv entre comillas (`"$CLAUDE_PROJECT_DIR/venv/Scripts/python.exe"`), no lo reconocía y escribía `python` a secas, y el vigilante podía no arrancar. Ahora respeta ese intérprete; con `python`/`python3` todo igual. Prueba nueva.

## 1.29.0 (2026-11-08)
- **Cierre por bloque** (spec 033, propuesta 1 del informe 032): `cierre.py` ya no pide la línea de `decisions.log` en cada respuesta; la pide cuando el chat lleva 15 archivos del proyecto editados sin cerrar (`cierre_bloque_max_ediciones`) o al cerrar con traspaso. Ajustes nuevos `cierre_por_bloque` y `cierre_bloque_max_ediciones` en `guardianes.json` (`cierre_por_bloque: false` vuelve al aviso de cada respuesta). La skill `cerrar-una-tarea` (es/en) lo explica. Pruebas nuevas.
- `medir.py --ritual` (informe 032): coste de los rituales del arnés (memoria, chat nuevo, avisos) frente al trabajo, y avisos del guardián por tipo. Textos es/en y pruebas.
- Spec 034: análisis de fusión de skills (sin ejecutar; espera la aprobación de Darwin).

## 1.29.1 (2026-11-09)
- `arranque.py` guarda un registro de tiempos (`.brain/guardianes/arranque_estado.json`, ignorado por Git): cuánto tarda cada arranque (últimos 20) y, si pasa de 8 s, la pila de dónde está parado (`ultimo_lento`). Para averiguar por qué en Modelo 2 el hook se corta a los 20 s (28 cortes frente a 8 arranques correctos). No cambia lo que muestra el arranque. Prueba nueva en `test_arranque.py`.

## 1.29.2 (2026-11-09)
- `poda.py` y `revisar_indices.py` ya no recorren `vendor`, `outputs`, `dist`, `build`, `site-packages`, `.venv` ni `env` al revisar enlaces de los .md. En Modelo 2 había ~27.000 .md (código de terceros y resultados de pruebas) y el arranque tardaba hasta 36 s (el hook corta a los 20 s). Es la causa hallada con el registro de tiempos de 1.29.1. Prueba nueva en `test_poda.py`.

## 1.30.0 (2026-11-09)
- Nueva skill `seguridad-en-sistemas-reales` (es/en): seis reglas para proyectos que actúan sobre sistemas reales (todo cambio por el motor, fallar hacia lo seguro, no depender de detalles internos del laboratorio, prueba con servidor falso mínimo, entradas raras, lista de comprobación al cerrar). Sale del experimento VMware (rondas 3 y 4; informes en `.brain/archive/`): con estas reglas Cerebro Vivo y ODD quedaron igual de seguros; sin ellas, ambos ataron el motor al laboratorio. Muestra de 1 por casilla: tendencia.

## 1.30.1 (2026-11-09)
- Skill `spec-antes-de-programar` (es/en): ya no exige spec por «más de 2 archivos». Spec obligatoria si toca cuotas, pagos, licencias, despliegue, base de datos, servidores reales o reglas de seguridad; en lo demás, «prueba de retomar» (basta el encargo y el `git diff`) y va por Fast-Track. Cada regla de una spec se escribe una sola vez. Sale del experimento VMware (rondas 1-5): el sobrecoste de Cerebro Vivo venía de spec + aprobador + rechazos en tareas pequeñas; con reglas de seguridad ambos métodos quedaron empatados en coste (≈ 369k frente a ≈ 423k de media; 377k frente a 383k en la ronda 5). Muestra de 1 por casilla: tendencia.

## 1.31.0 (2026-11-10)
- Fábrica de IA, fase 1 (spec 035): plantillas `PLANTILLAS_FABRICA.md` (carta de la fábrica con los topes aprobados, roles, tres puertas de Darwin, encargo, evidencia, huecos y propuestas) y `CARTA_EJECUTORA.md` (reglas reducidas para la IA que ejecuta un encargo), ambas es/en. Solo plantillas: los guardianes (alcance, spec congelada, topes) son la fase 2 y aún no se reparten.

## 1.32.0 (2026-11-10)
- Fábrica de IA, fase 2 (spec 035): nuevo guardián `fabrica.py` (sin IA, es/en en `textos.py`): `congelar` (huella de la spec aprobada), `sellar-carta` (la carta solo la cambia Darwin), `verificar`, `foto` y `alcance` (el encargo debe cumplir un requisito de la spec congelada y la ejecutora solo puede tocar sus archivos permitidos; rechaza sin gastar revisión), `gasto` y `topes` (tope por encargo, por misión, freno semanal de Codex y parada tras dos fallos seguidos). La carta lleva ahora líneas `clave: número` que el guardián lee. Sustituye al prototipo `alcance.py` (archivado). Prueba nueva `test_fabrica.py`. Es una herramienta que se lanza a mano, no un hook; las skills de la fase 3 y la prueba R13 con ella siguen sin hacer.

## 1.33.0 (2026-11-10)
- Fábrica de IA, fase 3 (spec 035): skills nuevas `directora-de-fabrica` y `revisor-independiente` (es/en) y regla 7 en `seguridad-en-sistemas-reales` (R9: ninguna IA cambia un requisito «por seguridad»; lo registra como hueco o propuesta y pregunta). Falta la prueba mínima R13 con todo junto.

## 1.33.1 (2026-11-10)
- Fábrica de IA: se quita el «paso previo: ¿ya existe el producto?» de la skill `directora-de-fabrica` y de `PLANTILLAS_FABRICA` (es/en) y de la spec 035. Fue algo puntual del addon de WoW, no un paso general (aclaración de Darwin).

## 1.34.0 (2026-11-10)
- `medir.py --fabrica --proyecto RUTA` (spec 035, medidor de gasto): suma el gasto de las sesiones de Codex por carpeta de encargo leyendo `~/.codex/sessions` (tokens totales menos lo leído de caché, que es la cifra del tope de la fábrica; ignora las revisiones internas de Codex). Textos en es/en y prueba nueva en `test_medir.py`. Falta el coste de la directora por tarea (punto 31).


## 1.34.1 (2026-11-10)


## 1.34.2 (2026-11-10)
- Fuentes: se añaden el artículo de Stanford «Meta-Harness» (arXiv:2603.28052, marzo de 2026) y Omnigent de Databricks (junio de 2026) en los README (es/en) y en `CEREBRO_VIVO.md` (es/en). Solo texto.


## 1.35.0 (2026-11-10)
- El carril corto «Fast-Track» pasa a llamarse **«Cambio pequeño»** (en inglés **«Small change»**), para no coincidir con el «FTD, Fast-Track Development» de otro proyecto. Cambia en `CEREBRO_VIVO.md`, la carta, las plantillas de índice y la skill `spec-antes-de-programar` (es/en), y en los guardianes `cerrar.py`, `cierre.py` y `eventos_chat.py` (clave nueva `carril_corto` en `textos.py`). `cerrar.py --carril` sigue aceptando «Fast-Track» como alias. Las líneas viejas de `decisions.log` no se reescriben; nadie lee esa columna, así que conviven sin problema.


## 1.35.1 (2026-11-10)
- Arreglo de fondo del hook `pre-commit` del guardián de secretos (pendiente 38): buscaba `.brain/guardianes/secretos.py` con ruta relativa y fallaba en los worktrees (la página en `gh-pages`), donde ese script no existe. Ahora, si no lo halla en la carpeta actual, lo busca en el repo principal vía `git rev-parse --git-common-dir`; si no está en ningún sitio, bloquea con un mensaje claro. Prueba nueva con un worktree real. Un proyecto lo recibe al actualizar y ejecutar `python .brain/guardianes/secretos.py --instalar-hook`.


## 1.35.2 (2026-11-10)
- Fuentes: se añaden los registros de decisiones (Nygard 2011, Fowler, Microsoft, Red Hat y la guía de AWS) y el Spec Kit de GitHub (`constitution.md`) en los README (es/en) y en `CEREBRO_VIVO.md` (es/en). Solo texto.


## 1.35.3 (2026-11-10)
- Fuentes: la «constitución» se atribuye a GitHub (Microsoft), `github/spec-kit` (agosto de 2025, MIT); se añaden `spec-driven.md` y el anuncio de Delimarsky en el GitHub Blog (2-9-2025, no nombra la constitución). README (es/en) y `CEREBRO_VIVO.md` (es/en). Solo texto.


## 1.35.4 (2026-11-11)
- Punto 30: los avisos más comunes de los guardianes (análisis de código, base de datos, pruebas y secretos) dicen ahora cómo arreglar el problema, no solo qué falló. Textos es/en en `textos.py`.


## 1.35.5 (2026-11-11)


## 1.35.6 (2026-11-11)
- Fuentes: «fábrica» se cubre con bibliografía: Cusumano, *Japan's Software Factories* (Oxford University Press, 1991) y Greenfield y Short, *Software Factories* (Wiley, 2004). README (es/en), `CEREBRO_VIVO.md` (es/en) y pie de la página. Solo texto; sin renombrar nada.

## 1.36.0 (2026-11-11)
- Spec 036 (punto 32): `librerias.py` y `eventos_chat.py` vigilan también npm (`package-lock.json`), cargo (`Cargo.lock`) y go (`go.mod`) con OSV.dev; ya no avisan de que no pueden revisarlos. La versión mayor nueva sigue siendo solo de Python.
- Spec 038 (punto 31): `cierre.py` apaga en ese chat un aviso informativo (chat largo, hito sin lección) que sale 3 veces seguidas (`guardian_fallos_max`); el cierre nunca se apaga. `medir.py` da los tokens por tarea terminada (por chat y en `--comparar`).
- Spec 037 (punto 29): `revisar_indices.py` detecta memoria desactualizada en `.brain/pendientes.md` y `constitution.md` (rutas, specs y fichas que ya no existen); solo avisa, con descartes y línea en el arranque.

## Sin versión (2026-11-11)
- Spec 039: `.github/workflows/pruebas.yml` lanza las pruebas en GitHub Actions (Ubuntu y Windows) en cada subida a `main` y en cada pull request. Solo de este repo; no llega a los proyectos, no cambia `VERSION` ni el manifiesto.

## 1.36.1 (2026-11-11)
- Arreglo: el hook `pre-commit` de secretos se instalaba sin permiso de ejecución, así que en Linux y Mac git lo ignoraba y no bloqueaba los secretos. Lo encontró la primera ejecución en GitHub Actions (spec 039).

## 1.37.0 (2026-11-11)
- Nuevo `/fabrica si|no|estado` (spec 040): interruptor del modo fábrica, **recordado entre chats** (`modo_fabrica` en `guardianes.json`). Con `si`, el arranque de cada chat dice «MODO FÁBRICA ACTIVADO» y la IA actúa como directora; con `no`, modo normal. Apagado por defecto; los proyectos con `.brain/fabrica/` de antes no cambian. Nueva skill `fabrica` (es/en), `fabrica.py modo`, textos es/en y pruebas.

## 1.37.1 (2026-11-11)
- `/fabrica si` abre solo el chat de la directora: escribe el traspaso, abre un chat limpio con `start_session` (Opus, sin pedir permiso) y lo separa con `detach_session`. Antes solo escribía el traspaso y Darwin tenía que abrir el chat a mano. Solo cambia la skill (es/en); sin cambios de código.

## 1.37.2 (2026-11-11)
- Arreglo: `fabrica.py` ya no se rompe en consolas de Windows (cp1252) por el emoji de sus mensajes (lo halló la directora de TraductorVoz con `topes`). Con prueba.

## 1.37.3 (2026-11-11)
- La skill `directora-de-fabrica` (es/en) añade el paso de lanzar a la ejecutora Codex por comando (`codex exec -s workspace-write -C carpeta`, entrada cerrada, tope 900 s, foto con `--repo` de esa carpeta, pruebas corridas por la directora, permiso de Darwin en cada lanzamiento, y si falla, texto para pegar a mano). Solo cambia la skill; sin cambios de código.

## 1.37.4 (2026-11-11)
- La skill `directora-de-fabrica` (es/en) ya no pide permiso a Darwin en cada lanzamiento de Codex: la directora lanza sola y solo para si salta un tope, van dos fallos seguidos o pasa algo imprevisto. Las puertas (a) y (c) siguen siendo de Darwin. Solo cambia la skill.
