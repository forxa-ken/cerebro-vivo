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
- La skill `directora-de-fabrica` (es/en) ya no pide permiso a Darwin en cada lanzamiento de Codex: la directora lanza sola y solo para si salta un tope, van dos fallos seguidos o pasa algo imprevisto. Un solo fallo tampoco se pregunta (se anota con `--fallo` y se relanza); solo el segundo seguido. Las puertas (a) y (c) siguen siendo de Darwin. Solo cambia la skill.

## 1.38.0 (2026-11-11)
- La fábrica deja elegir la IA obrera: la carta (plantilla es/en) trae la línea «Ejecutora por defecto» (Codex, Claude o «la que decida la directora»), y la skill `directora-de-fabrica` (es/en) explica cómo lanzar Claude como obrera (subagente Sonnet en su worktree) además de Codex. Sin cambios de código; `fabrica.py` ya contaba gasto y fallos por papel.

## 1.38.1 (2026-11-11)
- El revisor de la fábrica es, por defecto, un subagente de solo lectura (Sonnet) que recibe solo el encargo, el requisito y el diff; su informe se guarda en `.brain/fabrica/evidencia/`. Un chat propio visible solo si Darwin lo pide. Cambian las skills `directora-de-fabrica` y `revisor-independiente` (es/en); sin cambios de código.

## 1.39.0 (2026-11-11)
- Skill nueva `revisor-de-consumo` (es/en): subagente de solo lectura que, al terminar un módulo o la misión de una fábrica, busca gasto de recursos de más (CPU, memoria, disco, red, batería) y mide cuando puede. La directora decide: lo que incumple el presupuesto de la spec vuelve a la ejecutora como encargo de arreglo; lo demás va a propuestas y se pregunta a Darwin.
- La plantilla de la spec y la skill `directora-de-fabrica` piden ahora un **presupuesto de recursos** en la spec («sin presupuesto» si no importa). Sin cambios de código.

## 1.39.1 (2026-11-11)
- `/fabrica si` abre el chat de la directora con Opus y esfuerzo medio, y lo llama «directora #N» (la cuenta N se lleva en `.brain/fabrica/directora_n.txt`). Comprueba después con `get_session` que quedó así y lo corrige si el chat que lo abrió no era Opus. Solo cambia la skill `fabrica` (es/en).

## 1.40.0 (2026-11-12)
- `medir.py --fabrica` enseña ahora también el gasto de la directora (Claude): sus chats del proyecto con tokens nuevos + salida (sin caché), además del gasto de Codex por encargo. Probado con TraductorVoz (1 chat de directora, 241k; Codex 18 sesiones, 994k). No cuenta los subagentes de Claude (obrera o revisor), que no tienen registro propio. Con prueba y textos es/en.

## 1.40.1 (2026-11-12)
- Punto 30: 18 avisos de los guardianes (fábrica, base de datos, traspaso e índices) dicen ahora **cómo arreglarlo**, no solo qué falló (por ejemplo, «vuelve a congelarla con `fabrica.py congelar SPEC`» o «para y pregunta a Darwin antes de relanzar»). Solo se añaden frases al final; el texto anterior no cambia. En español e inglés.

## 1.40.2 (2026-11-12)
- Punto 37 (b): `test_soporte_mac` ya no falla en los proyectos. Comprobaba que `instalar_kit.command` tuviera fin de línea Unix, pero en un proyecto Git de Windows lo baja con CRLF. Ahora solo se comprueba en el repo del arnés (donde existe `manifiesto.json` y `.gitattributes` lo fija en LF) y fuera se salta. Probado simulando un proyecto con el archivo en CRLF.

## 1.41.0 (2026-11-12)
- Punto 36 (spec 041): la **prueba de retomar** pasa a ser segundo criterio del cierre por bloque. Antes del tope de 15 ediciones, si otra IA no podria seguir solo con la peticion y el `git diff` (hay una decision, una causa o un paso pendiente solo en la conversacion), se cierra ya. Regla en la skill `cerrar-una-tarea` (es/en) y una frase en el aviso del guardian de cierre (es/en). El guardian no juzga: el contador de 15 sigue de red de seguridad. Se mide con `medir.py --ritual`.

## 1.42.0 (2026-11-12)
- Spec 042 (punto 19): **modo colaborativo** y Gemini como obrera. Comando `/colabora si|no|estado` (`colabora.py` + skill es/en): enciende `modo_colaborativo`, crea `.brain/colaboracion.md` desde la plantilla `biblioteca/IAS_COLABORATIVAS.md` (es/en) y pone UNA linea que remite a el en `CLAUDE.md`, `AGENTS.md` y `GEMINI.md`; el arranque lo recuerda entre chats. Ajuste nuevo `indices_ajenos` en `guardianes.json` (R12 de la spec 035): el instalador y el actualizador no tocan esos indices. La skill `directora-de-fabrica` y la carta de la ejecutora admiten a **Gemini** (`gemini -p ... --approval-mode auto_edit`, solo texto, traducciones y documentacion); **no probado con Gemini**: falta que Darwin inicie sesion y corra un encargo minimo. 13 pruebas nuevas.

## 1.43.0 (2026-11-12)
- Spec 043 (punto 19): **proyectos hermanos**. Guardian `hermanos.py` (solo lectura, no hace `fetch`): con `proyectos_hermanos` en `guardianes.json` (`{nombre, ruta, rama, archivo_portar}`; vacio por defecto) compara los commits del hermano con el archivo de portar de este proyecto (secciones `Ultimo portado`, `Pendiente`, `Hecho`, es/en) y el arranque avisa «N commits de X sin portar»; si el hermano no es accesible, calla. Plantillas `PLANTILLA_PORTAR` y `PLANTILLA_HALLAZGOS` (es/en), skill `hermanos` (es/en) e instalador con el guardian nuevo. **Arreglo de la 1.42.0:** la plantilla `IAS_COLABORATIVAS` (es/en) no estaba en la lista que se reparte, asi que `/colabora si` no la encontraba en los proyectos; ahora se reparte. 11 pruebas nuevas con dos repositorios de juguete; **sin probar contra proyectos reales** (falta la prueba a mano de la spec, solo lectura).

## 1.44.0 (2026-11-12)
- Spec 044 (punto 23): **auditor**. Skill `/auditor` (es/en) y guardian `auditor.py`: dice quien audita en cada modo (`general`, `cierre`, `spec`) y da el comando de Codex en solo lectura (en Windows con `windows.sandbox="unelevated"`, sin lo cual Codex no puede ejecutar `python`). Reparto decidido tras dos rondas de fallos plantados: el interno (Sonnet 5.5 medio) siempre; la IA externa (Codex) en revision general y cierre de spec, y en cierres rutinarios solo con `auditor_externo` en `siempre`; en `no` no se llama a ninguna IA externa. `cierre.py` **solo avisa** tras cambios de codigo o configuracion si `auditor_cierre` esta encendido (no avisa si solo se tocaron documentos). Ajustes nuevos en `guardianes.json`: `auditor_cierre`, `auditor_externo`, `auditor_modelo`, `auditor_modelo_externo`, `auditor_esfuerzo`, `auditor_ignorar_extensiones`, `revision_sensibles`. Plantilla `PLANTILLA_INFORME_REVISION` (es/en), linea informativa en el arranque si el externo no esta en el valor por defecto, prueba `test_auditor.py`.

## 1.44.1 (2026-11-12)
- Correcciones del auditor (spec 044) halladas por el propio auditor (Sonnet + Codex, informe en `.brain/archive/informe-auditor-sobre-044-2026-11-12.md`): `/auditor cierre|externo` ya no borra el resto de `guardianes.json` si está roto o tiene BOM (no escribe y avisa; BOM se lee); el aviso de cierre no se apaga con el cierre por bloques ni salta si la respuesta no editó nada; un ajuste con tipo raro ya no tumba el cierre; `auditor_cierre` es verdadero por defecto en todos los sitios y acepta «false»/«no»/«0»; los valores que entran en el comando de Codex se validan; `revision_sensibles` ahora se lee (`quien cierre ARCHIVO…` sugiere el externo); README/LICENSE no cuentan como código; el arranque normaliza `auditor_externo`. Pruebas nuevas (40 en `test_auditor`). Documentado en la spec 044 que `.brain/*` y `.claude/*` quedan fuera del aviso.

## 1.44.2 (2026-11-12)
- Segunda auditoría (Sonnet + Codex) sobre la 1.44.1: confirman corregidos los hallazgos anteriores y hallan fallos menores, ya arreglados: una lista de extensiones vacía (`[""]`) o sin punto (`"md"`) apagaba el aviso de cierre; un modelo o esfuerzo que parece una opción (`-s`) entraba en el comando de Codex; un JSON anidado enorme daba traceback; `/auditor estado` con el archivo roto no avisaba de que mostraba valores por defecto; `auditor_modelo` sin sanear. **Sin cambiar (decidido):** el aviso puede repetirse en cada respuesta con ediciones (no pasa por el apagado de la spec 038) y, con ediciones hechas por terminal, cuenta todos los cambios de git; `sensible` casa por subcadena.

## 1.44.3 (2026-11-12)
- El aviso del auditor de cierre ahora pasa por el apagado de avisos repetidos (spec 038): si sale 3 veces seguidas en el mismo chat sin cambiar nada, se avisa de que se apaga y no se repite en ese chat (`evaluar(..., auditor_aparte=lista)`; `main` lo trata como informativo). Probado con el hook `Stop` real en un repo temporal: avisa 3 veces y calla.

## 1.44.4 (2026-11-12)
- Corrección de raíz: 4 pruebas del método (3 de `test_auditor.py`, 1 de `test_colabora.py`) comprobaban las ediciones en inglés y `generar_manifiesto.py`, que solo existen en el repo del arnés, y fallaban en los proyectos que las recibían (visto al actualizar LoboHook a la 1.44.3). Se mudan a `tests/test_arnes_reparto.py`, que no se reparte, con una prueba que vigila que siga sin repartirse. El actualizador quita de los proyectos lo que ya no llega. No cambia nada de lo que hace el arnés.
- Nuevo en la plantilla de constitución de los proyectos (es y en): regla 12, «un parche se llama parche» (pedido por Darwin).

## 1.44.5 (2026-11-12)
- La directora de fábrica lanza a Codex con `-m gpt-6-luna -c model_reasoning_effort=max` y tope de 1800 s (antes: el modelo y esfuerzo del `config.toml` de Codex, 900 s). Pedido por Darwin; en la skill `directora-de-fabrica`, es y en. Sin probar en un encargo real con esfuerzo máximo.

## 1.44.6 (2026-11-12)
- El chat nuevo de la directora de fábrica se separa solo del chat que lo abrió: paso 0 en la skill `directora-de-fabrica` y frase añadida al encargo con que `/fabrica si` abre ese chat (es y en). Antes solo lo separaba el chat de fuera, y si la app lo rechazaba quedaba colgado. Sin probar con una directora real.

## 1.44.7 (2026-11-12)
- Limpieza de fuentes por orden de Darwin: quitada una fuente externa de las Fuentes (README es/en, cabecera de CEREBRO_VIVO es/en y pie de la página pública) y de los registros, notas y cambios; el historial de git se reescribió sin esas menciones. Solo texto.

## 1.45.0 (2026-11-12)
- Nuevo `/diapositivas` (spec 045, punto 49): convierte un tema (`resumen`, `version`, `traspaso`, `auditoria`) o un documento entero (`doc NOMBRE`) en una presentación `.html` autocontenida que se abre en el navegador, sin instalar nada y sin conexión; flechas, `o` para ver todas, Ctrl+P para PDF. Script `diapositivas.py` (también `--buscar NOMBRE` y `--comprobar ORIGINAL DIAPOSITIVAS`), skill es/en, plantilla es/en y textos es/en. En modo documento: índice, una diapositiva por sección y partes enlazadas pasadas 20. El HTML del `.md` se escapa, solo hay enlaces http(s) o relativos y una política impide cargar nada de internet. Los `.html` no se suben a Git. Sin probar con Darwin en un trabajo real.

## 1.46.0 (2026-11-12)
- Diagramas en `/diapositivas` (spec 046, fase 1): un bloque ```` ```mermaid ```` con `flowchart` (LR, RL, TB, TD, BT; cajas, rombos, flechas con etiqueta, punteadas y gruesas) o `sequenceDiagram` (participantes, mensajes, notas, autonumber) se dibuja como SVG dentro del `.html`, sin internet ni librerías (`diagramas.py`, nuevo). Si no se puede dibujar (tipo no soportado, línea rota o demasiado grande) queda como texto y el script avisa en es/en. Skill, plantilla y manual al día; `test_diagramas.py`. Sin probar por Darwin; clases, estados, tarta, ER y Gantt quedan para fases posteriores.

## 1.46.1 (2026-11-13)
- `diagramas.py`: los dibujos anchos (secuencia) ya no se agrandan hasta un texto mucho mayor que el de las cajas; el SVG lleva un `max-width` de 1,2 veces su ancho.

## 1.46.2 (2026-11-13)
- `/diapositivas`: subviñetas. Una línea de lista con más sangría (2 espacios) cuelga de la anterior, hasta 3 niveles; antes se aplanaban. Con 3 pruebas nuevas, plantilla es/en y skill es/en al día.


## 1.46.3 (2026-11-13)
- `fabrica.py alcance` con un archivo de encargo que no existe: avisa en llano (es/en) y apunta a la plantilla, en vez de soltar un error técnico. Sin probar por Darwin.


## 1.46.4 (2026-11-13)
- `hitos.py`: un error solo cuenta como «resuelto» si vuelve a funcionar el mismo comando o script que falló (antes bastaba cualquier comando de consola). Recorta el aviso de hito sin lección, que era el 62 % de los avisos del guardián. Con 2 pruebas nuevas. Sin probar por Darwin.


## 1.46.5 (2026-11-13)
- `hitos.py`: el aviso de hito sin lección ya no cuenta como fallo la palabra «error» suelta, que salía al leer o buscar código. Solo mira marcas precisas (`Traceback`, `Exit code`, `FAILED`, `...Error:`) y solo en consola; en `Read`, `Grep` o `Edit` cuenta únicamente si la herramienta falla de verdad. Con 3 pruebas nuevas. Sin probar por Darwin.


## 1.46.6 (2026-11-13)
- Gemini deja de ser ejecutora de la fábrica (spec 042, parte B), por orden de Darwin: Google cerró el comando `gemini` para cuentas personales y no se quiere pagar. La skill `directora-de-fabrica` (es/en) lo dice y la carta de la ejecutora queda en «Claude o Codex». `/colabora` y `indices_ajenos` se mantienen (probados por Darwin); el índice `GEMINI.md` sigue siendo opcional.

## 1.47.0 (2026-11-13)
- Pendiente 48: cada línea nueva de `decisions.log` lleva un **tipo fijo** en el segundo campo (`AAAA-MM-DD | tipo | quién (chat) | qué | carril`), para filtrarla con `grep "| arnes |" .brain/decisions.log`. `cerrar.py` acepta `--tipo` (arnes, leccion, decision, spec, pendiente, memoria, otro; por defecto «otro»); la línea automática de `cierre.py` usa `auto` y la de `eventos_chat.py` usa `guardian`. Las líneas antiguas no se tocan y los guardianes que leen el registro (arranque, cierre) no cambian. Documentado en `CEREBRO_VIVO` y en la skill `cerrar-una-tarea` (es/en). Pruebas nuevas del formato.

## 1.48.0 (2026-11-13)
- Pendiente 47: **efecto en cadena al cerrar** (`cierre.py`). Cuando el chat cierra una tarea, avisa de documentos que el cambio puede haber dejado viejos: por ejemplo, tocó una spec y no `pendientes.md`, tocó una decisión y no su índice, tocó la constitución y no `CLAUDE.md`, o tocó un guardián y no el manual. Solo avisa (no bloquea) y, si se repite sin atenderse, se apaga en ese chat (spec 038). Las reglas van en `cadenas` de `guardianes.json` (`si`, `salvo`, `avisar` es/en; cada proyecto añade las suyas) y se apaga todo con `cadenas_activas: false`. Textos es/en y 6 pruebas nuevas.

## 1.49.0 (2026-11-13)
- Pendiente 45: **respuestas guardadas**. Nuevo guardián `respuestas.py` y skill `/guardar-respuesta` (es/en): archiva en `.brain/respuestas/AAAA-MM-DD-titulo.md` una respuesta o comparación útil de un chat con su fuente, aunque no venga de un fallo (las lecciones solo nacen de un problema resuelto). Genera `indice.md` (la más nueva primero), no pisa una respuesta con el mismo título y fecha, exige título y fuente, tope de 8 KB y admite el texto por la entrada estándar (`-`) para no usar heredocs. Entra en el kit (`instalar.py`), en el índice de experiencia y en el manual. Textos es/en y 6 pruebas nuevas.

## 1.50.0 (2026-11-13)
- Pendiente 44 (spec 048): **revisión del contenido de `.brain/`**. Nuevo guardián `revisar_contenido.py` y skill `/revisar-contenido` (es/en). Solo lectura y sin bloquear: avisa de páginas de `.brain/` que nadie enlaza, de frases que ya no son ciertas en `architecture/` y `biblioteca/` (ruta que no existe, «versión actual» distinta de `VERSION`, «hay N skills» falso) y de topes contradictorios de un mismo archivo entre documentos. El arranque da **una línea** (solo si hay hallazgos y han pasado `revision_contenido_dias`, 30 por defecto; se apaga con `revision_contenido_activa`). La skill hace *buscar y refutar* con **otra IA** (un subagente nuevo sin el contexto de la primera; segundo juez opcional de otra IA para lo dudoso). Lo descartado queda en `revision_contenido.json`. Textos es/en, 18 pruebas nuevas. **Sin probar por Darwin.**

## 1.50.1 (2026-11-13)
- `revisar_contenido.py` (spec 048): tras la primera pasada real, la otra IA que refutó los hallazgos vio que el guardián no leía `decisions.log` ni `CAMBIOS.md` ni reconocía «informe NNN», y marcaba como huérfanas páginas que sí estaban citadas. Ahora cuenta ambos archivos y «informe NNN» como menciones. Una prueba nueva (19 en total).

## 1.51.0 (2026-11-14)
- Pendiente 46 (spec 049): **búsqueda local en la memoria**. Nuevo guardián `buscar.py` y skill `/buscar-en-la-memoria` (es/en). Pregunta a `.brain/` (lecciones, decisiones, specs, respuestas, registro) con unas palabras y devuelve los mejores archivos con título y las líneas donde salen. Sin índice (recorre la memoria en cada consulta, unos 470 KB tardan milisegundos), sin tildes ni mayúsculas, sin palabras vacías, más peso al título y a los encabezados y tope para que un archivo largo no gane solo por repetir. `--solo`, `--max`, `--archivo` (incluye `archive/`), `--json`. Solo lectura. Umbral para pasar a un índice: 5 MB o más de 1 segundo. Textos es/en, pruebas nuevas. **Sin probar por Darwin.**

## 1.52.0 (2026-11-14)
- Spec 050, **fase 1** (modo automático de la fábrica): ajuste `fabrica_automatica` (apagado por defecto, solo vale con `modo_fabrica`), orden `fabrica.py automatico si|no|estado` (`estado` dice si falta la carta sellada, el criterio de «esperado» en `.brain/fabrica/esperado.md` o una rama de trabajo distinta de `main`), `modo no` y `modo normal` lo apagan también, aviso «Modo fábrica AUTOMÁTICO» en el arranque, skill `/fabrica` ampliada (es/en) y textos es/en. Solo el interruptor: todavía no hay revisor de spec, ni prueba de uso real, ni bloqueos (fases 2 a 5). 6 pruebas nuevas. **Sin probar por Darwin.**

## 1.53.0 (2026-11-14)
- Spec 050, **fase 2** (revisor de spec): skill `revisor-de-spec` (es/en) y, en `fabrica.py`, `sellar-negocio` (huella de `.brain/fabrica/negocio.md`, que `verificar` vigila), `veredicto` (valida el veredicto de la otra IA: línea APROBADA/RECHAZADA, secciones (a) negocio no cubierto, (b) requisito inventado, (c) hueco, (d) contradicción; **todo hallazgo cita una frase real** del negocio, la spec o specs anteriores, y un rechazo sin cita no cuenta; marca los huecos `[GRANDE]` que suben a Darwin) y `vueltas` (tope de 3 rechazos, luego parar y preguntar). Manual y textos es/en. Tras la auditoría de cierre se endureció: las cuatro secciones son obligatorias, no se valida sin negocio sellado e íntegro, las citas mínimo 12 caracteres, todas deben existir y al menos una salir de la fuente de su sección, listas numeradas y encabezados `####` o en negrita no se cuelan, un archivo que no es UTF-8 no rompe el guardián, el contador de vueltas aguanta un JSON roto y un `[GRANDE]` sube aunque su cita no valga. 17 pruebas nuevas. Prueba con revisores reales (Sonnet, otro chat; **no** se probó con Codex): la spec 049 buena y tres copias dañadas a propósito (requisito inventado, parte del negocio omitida, contradicción), 2 vueltas cada una = 8 veredictos. Las 2 buenas salieron APROBADA y las 6 dañadas RECHAZADA con cita válida en la sección esperada; el guardián dio por válidos los 8. Un revisor añadió un hallazgo (b) discutible en la copia «omitida». Muestra pequeña: no demuestra fiabilidad. **Sin probar por Darwin.**
- (1.53.0) Receta corta para instalar con Gemini: `.brain/biblioteca/GUIA_GEMINI.md` y `GUIA_GEMINI.en.md`, enlazada desde `GUIA_INSTALACION.md`. Avisa de que con `--ias gemini` solo no se copian las skills (`.agents/skills/` pide `AGENTS.md`). Probado el instalador en carpeta de prueba; **sin probar dentro de Antigravity real.**
- (1.53.0) Receta corta para instalar con Codex: `.brain/biblioteca/GUIA_CODEX.md` y `GUIA_CODEX.en.md`, enlazada desde `GUIA_INSTALACION.md`. Probado el instalador con `--ias codex` en carpeta de prueba (crea `AGENTS.md` y `.agents/skills/`); **sin probar dentro de Codex real.**

## 1.54.0 (2026-11-14)
- Spec 050, **fase 3** (criterio de «esperado» y rama de trabajo): en `fabrica.py`, orden `arrancar` que, con el modo automático activo, **bloquea** (código 1) si falta `.brain/fabrica/esperado.md`, si sus campos obligatorios («Cómo se sabe que salió bien» y «Casos malos», o sus equivalentes en inglés) están vacíos, siguen en plantilla (`<…>`) o son demasiado cortos, o si se está en `main`/`master`/cabeza suelta; `foto` (el arranque de cada encargo) la llama sola. Fuera del modo automático no cambia nada. Sección 9 nueva en `PLANTILLAS_FABRICA` (es/en) con la plantilla del criterio; `automatico estado` ahora avisa de un criterio a medias. 11 pruebas nuevas, suite en verde. **Sin probar por Darwin ni en un proyecto real.**

## 1.55.0 (2026-11-14)
- Spec 050, **fase 4** (prueba de uso real): skill `prueba-de-uso-real` (es/en) con cómo probar cada tipo de producto, dónde queda la evidencia y qué se marca «no probado»; y, en `fabrica.py`, orden `entregar REQ` que, con el modo automático activo, **bloquea** (código 1) dar un requisito por entregado si falta `.brain/fabrica/evidencia/REQ.md`, si falta algún campo o sigue en plantilla, si «Probó» es igual que «Construyó», si «Criterio probado» no cita entre «…» una frase literal de `esperado.md`, si un archivo de evidencia no existe, está vacío o queda fuera de `.brain/fabrica/evidencia/`, o si el resultado no es «verde» (rojo vuelve a la ejecutora; no probado pasa a Darwin). Sección 10 nueva en `PLANTILLAS_FABRICA` (es/en). Fuera del modo automático no cambia nada. 13 pruebas nuevas, suite en verde. **Límite conocido:** el guardián no puede saber si de verdad se ejecutó lo que la evidencia dice, ni si «Probó» es de verdad otra IA (compara los nombres escritos); eso lo cubre el revisor y la prueba de Darwin. **Sin probar por Darwin ni en un proyecto real.**

## 1.56.0 (2026-11-14)
- Spec 050, **fase 5** (informe de entrega y frenos), en `fabrica.py`: `frenos --encargo N` (con el modo automático activo) para el encargo a los **3 fallos** (cuenta los `gasto --fallo` de ese encargo) o a los **30 minutos sin avance**, y deja `.brain/fabrica/estado/parada-N.md` con dónde quedó; solo Darwin reanuda (`frenos --reanudar`, que pone fallos y reloj a cero). `avance --encargo N` anota avance a mano; `gasto` sin fallo, `foto` y `entregar` lo anotan solos, y `foto` aplica los frenos al arrancar cada intento. La carta puede cambiar los topes (`auto_reintentos_max`, `auto_atasco_minutos`). `informe [ARCHIVO]` valida `.brain/fabrica/informe.md`: las seis secciones (pedido, hecho, extra, probado, no probado, decisiones por su cuenta), ninguna vacía sin explicación. Sección 11 nueva en `PLANTILLAS_FABRICA` (es/en). Fuera del modo automático los frenos no hacen nada. 17 pruebas nuevas, suite en verde. **Límite conocido:** el reloj de atasco solo se mueve cuando alguien lo marca (el guardián no vigila en segundo plano); lo comprueba al arrancar cada intento y cuando la directora lo ejecuta. **Sin probar por Darwin ni en un proyecto real.**

## 1.57.0 (2026-11-14)
- Arreglos de los hallazgos del experimento de la fase 6 (spec 050): el guardián `alcance` entiende `R-1` igual que `R1` (la plantilla decía `R-n`) y no cuenta como cambio de la ejecutora la spec congelada que la directora corrige y vuelve a congelar; las pruebas que leen las ediciones `.en.md` solo las exigen en el repo del arnés (un proyecto en español no las recibe, y fallaban 5 tras `actualizar`); la skill `revisor-de-spec` (es y en) explica cómo lanzar a Codex pegando el texto en la orden.
