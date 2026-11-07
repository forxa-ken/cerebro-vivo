# Contexto de cerebro-vivo para otra cuenta de IA

> Escrito el 2026-11-06 desde el chat «cerebro-vivo #15». Para pegar como primer mensaje (o adjuntar) en una cuenta que **no tiene acceso al proyecto**. Resume lo esencial; el detalle vive en los archivos que se nombran. Lo no probado va marcado como no probado.
> No contiene claves ni datos personales.

## 1. Qué es
**cerebro-vivo** es el repositorio del **meta-arnés «Cerebro Vivo»**: un método para trabajar con una IA (Claude, Gemini, Codex) **sin perder el contexto entre chats y gastando pocos tokens**, más las herramientas que lo hacen cumplir. Es el origen único: cada proyecto de Darwin (el dueño, no técnico) trae las mejoras desde aquí.

- Ubicación local: `F:\Proyectos Antigravity\cerebro-vivo` (Windows 11, Python, sin dependencias externas).
- GitHub: `forxa-ken/cerebro-vivo`. Lo subido se ve con `git log origin/main`. No se sube nada sin orden expresa de Darwin, salvo el commit de memoria de `traspaso-out salgo`.
- Versión actual del arnés: la del archivo `VERSION`.

## 2. La idea del método
La IA no recuerda entre chats, así que la memoria del proyecto vive en **archivos** ordenados: se lee un índice corto al empezar y solo se abre el detalle cuando hace falta. Principios: índice primero y detalle después; cada cosa en su sitio; cerrar una tarea incluye actualizar la memoria; «implementada» no es «terminada» (terminada = Darwin la probó); lo hecho sale de la vista; el porqué de cada decisión se guarda; lo que una máquina puede vigilar no se deja a la disciplina; alcance estricto; lo irreversible se pregunta; lo no probado se dice como no probado.

## 3. Estructura del repo
- `CLAUDE.md`: índice corto de entrada (es un índice, no un manual).
- `.brain/constitution.md`: reglas innegociables. `.brain/pendientes.md`: solo lo que falta. `.brain/decisions.log`: una línea por tarea terminada. `.brain/decisions/`: fichas D-NNN. `.brain/specs/`: especificaciones aprobadas antes de programar. `.brain/archive/`: hechos y traspasos archivados.
- `.brain/guardianes/`: comprobaciones automáticas (arranque, cierre, cerrar, poda, medir, secretos, librerías, pruebas, longitud, índices, notas de chats, archivos gordos, actualizar_arnes).
- `.brain/biblioteca/`: manual `CEREBRO_VIVO.md`, carta maestra `CARTA_META_ARNES.md`, plantillas de traspaso y nota de chat, kit de arranque y kit de traducción.
- `.claude/skills/`: skills genéricas (`/adopta`, `/acorta`, `/trocea`, `/actualizar`, `/traspaso-in`, `/traspaso-out`, `/resumen`, `/pendiente`, `/prompt-inicial` y otras).
- Raíz: `VERSION`, `CAMBIOS.md` (una línea por versión), `manifiesto.json` (huella de cada archivo repartido), `actualizar.py`, `generar_manifiesto.py`, `generar_zip_mac.py`, `instalar_kit.bat` y `.command`, `MANUAL_DE_USO.md`, `README.md`, `tests/`, `plantilla-prompt/`.

## 4. Reglas que hay que respetar (constitución resumida)
1. Responder en **español**, tono técnico, conciso y llano con Darwin.
2. **Alcance estricto:** solo lo que atañe al cambio pedido.
3. **Pruebas en verde** tras cada cambio: `python -m unittest discover tests` (hoy: 246 pruebas, OK, 5 saltadas).
4. Al cerrar cada tarea, una línea en el registro: `python .brain/guardianes/cerrar.py --chat "cerebro-vivo #N" "qué se hizo"`.
5. Pendientes solo con lo que falta; numeración fija.
6. Secretos fuera del repo. 7. Llamadas externas con tiempo máximo y plan B local.
8. **No subir a GitHub sin orden de Darwin.** Lo irreversible (borrar, gastar, subir) se pregunta antes.

## 5. Cómo se cambia el arnés (receta obligatoria)
Tras tocar cualquier archivo que se reparte: subir `VERSION` → anotar en `CAMBIOS.md` → `python generar_manifiesto.py` → `python generar_zip_mac.py` (deja `../cerebro-vivo-para-mac/cerebro-vivo-mac-VERSION.zip` y mueve el anterior a `anteriores/`; un amigo prueba con Mac con ese ZIP) → pruebas. Una prueba falla si se olvida el manifiesto.

## 6. Cómo llega a los proyectos
- Instalar en un proyecto nuevo o empezado antes: ventana `instalar_kit.bat` (o `python .brain/biblioteca/kit-arranque/instalar.py RUTA --nombre ... --nivel completo`). Si el proyecto ya tiene `CLAUDE.md`/`AGENTS.md`, el instalador **fusiona** (añade el bloque de memoria sin quitar nada; original en `.brain/archive/adoptado/`) y anota en `pendientes.md` «escribe `/adopta`». Niveles: ligero, medio, completo.
- Actualizar un proyecto que ya lo tiene: `/actualizar` dentro del proyecto, o `python actualizar.py RUTA --simular` y luego sin `--simular`. No pisa lo modificado a mano ni toca pendientes, specs, decisiones, registro ni configuración (solo añade claves de config que faltan).
- Proyectos conocidos que usan el arnés: **LoboHook** (donde nació; actualizado a 1.18.2), **Guild Control Forever** (addon de WoW Classic; en 1.16.1; su `AGENTS.md` lo usa Gemini solo para traducciones y NO se renombra ni se edita), **Guild Control** (addon de WoW Retail, `F:\World of Warcraft\_retail_\Interface\AddOns\GuildControl`; kit instalado el 2026-11-04 en 1.18.0, `/adopta` probado por Darwin), Modelo 2, Pegatinas (no tocar sin orden).

## 7. Qué está demostrado (medición del 2026-11-01)
- Al retomar un trabajo en un chat nuevo, con el arnés se respetó lo acordado 5 de 5 veces; sin él, 0 de 5.
- En tareas pequeñas gasta de un 7 % a un 16 % más que no usarlo; no ahorra ahí.
- Hipótesis aún sin medir: en un proyecto real y largo ahorra a la larga (se mide con `medir.py`). Los índices de decisiones no mejoraron el acierto a ~80 fichas (spec 004).

## 8. Historia reciente (versiones del 2026-11-04)
- 1.12.0 `/traspaso-in salgo` abre el chat nuevo solo. 1.13.0 el instalador fusiona `CLAUDE.md` y `settings.json` existentes; skill `adoptar-indice-existente`; `generar_zip_mac.py`. 1.14.0 revisión de los índices de IA con doble pasada (`revisar_indices.py`). 1.15.0 `/acorta`. 1.16.0 guardián `archivos_gordos.py` (tope 8 KB) y skill `/trocea`. 1.16.1 las pruebas miran solo `indices_entrada`.
- **1.17.0** (spec 019): el arranque avisa de versión nueva del arnés y existe `/actualizar`.
- **1.18.0** (spec 020): `/adopta` encadena adoptar, acortar y trocear pidiendo el sí en cada tabla.
- **1.18.1:** el aviso de arranque de índices pasados de tope dice «escribe /adopta».
- **1.18.2:** `/traspaso-in` sin palabra equivale a `salgo` y abre el chat nuevo.

## 9. Pendientes (estado real)
**Falta programar (IA):**
- **4:** (opcional) medir el arnés en un proyecto real durante semanas.
- **14:** el actualizador copia guardianes a proyectos de nivel medio sin `guardianes.json` y los deja rotos (caso Pegatinas); decidir si se salta o avisa.
- **19:** diseñar (spec aparte, sin programar) cómo colaboran varias IA en un proyecto cuando sus responsabilidades son distintas (caso Guild Control Forever: Claude con `.brain/`, Gemini solo traducciones con `AGENTS.md`).
- **20:** `traspaso-in salgo` cuando el chat nació de otra sesión: la app puede rechazar `start_session`; el aviso de chat largo se repetía en cada mensaje. Parcialmente atendido por 1.18.2, no resuelto del todo.

**Esperando la prueba de Darwin:** 13 (`traspaso-in`/`traspaso-out`; Gemini sin probar), 16 (aviso de chat largo que abre el chat nuevo), 17 (soporte Mac, solo probado en Windows).

**Otros abiertos:** actualizar Guild Control Forever a la versión actual y revisar los secretos de su historial (`secretos.py --historial`); repetir la suite completa de LoboHook (5 rojas de 1094 tras actualizar; una ya corregida; la skill vieja `traspaso-entre-chats` ya se eliminó); el encadenado completo de `/adopta` y el aviso de versión nueva en arranque real siguen sin verse de punta a punta.

## 10. Cómo trabajar con Darwin
- Habla en lenguaje llano; no técnico. Explícale con ejemplos, no con jerga.
- Al abrir un chat, copiarle el resumen de arranque en 4-5 viñetas. Avisar cuando el chat se alargue y abrir yo el chat nuevo (`start_session` + `detach_session`) en vez de pedirle que lo abra.
- Escribir archivos con Write o Edit; en scripts de shell las barras invertidas se rompen.
- Nunca empezar trabajo nuevo al arrancar: contar el estado y preguntar por dónde seguir.

## 11. Qué NO hacer
No subir a GitHub ni cambiar la visibilidad del repo sin orden. No renombrar el `AGENTS.md` de Guild Control Forever. No actualizar otros proyectos (Pegatinas, etc.) ni borrar chats o carpetas Bench sin orden. No meter nada de LoboHook ni de otro proyecto en este repo (lo vigila `tests/test_arnes_repo.py`).

## 12. Qué no tiene la otra cuenta y cómo suplirlo
No ve el código. Si necesita detalle, que Darwin le pase estos archivos: `CLAUDE.md`, `.brain/constitution.md`, `.brain/pendientes.md`, `MANUAL_DE_USO.md`, `.brain/biblioteca/CEREBRO_VIVO.md` y `CAMBIOS.md`. Esta cuenta no puede ejecutar nada aquí: cualquier cambio lo hace el chat de este proyecto.
