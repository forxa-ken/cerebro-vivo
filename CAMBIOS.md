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
