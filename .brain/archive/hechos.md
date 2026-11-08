# Hechos (tareas terminadas y probadas)

> Aquí va el detalle de cada tarea **ya probada por Darwin**. `pendientes.md` solo guarda lo que falta.
> **No abrir completo:** consultar `hechos-indice.md` y leer solo la entrada necesaria (buscar `## <Nº>`).
> La **numeración es fija**: el número que tenía el punto en `pendientes.md` no cambia al moverlo aquí.

## 21 · Nada suelto ni viejo: traspaso-out salgo con remoto (spec 022, 1.20.0)
**Fecha:** 2026-11-08 · **Ref:** archive/hechos.md
Probado por Darwin el 2026-11-08 con Modelo #61 en un proyecto con GitHub: traspaso-out salgo hizo commit solo de la memoria (439b298, 7 archivos de .brain, verificado en GitHub), lo subio y listo el codigo suelto (prueba_suelta.py y otros) sin meterlo. Sin valorar: si el aviso de /actualizar ayuda o estorba. Hallazgo aparte: hitos.py no reconocia lecciones.py con PowerShell (arreglado en 1.28.7).

## 28 · Guardián con memoria del chat revisa el .venv (specs 027, 029 y 030, 1.28.5)
**Fecha:** 2026-11-08 · **Ref:** archive/hechos.md
Probado por Darwin el 2026-11-09 (confirmado tras las pruebas de Modelo #59 y #60 en F:/Modelo 2): con django==3.2 en el .venv el git push se detiene; con humanize==4.16.0 pasa callado. Arreglos: 1.28.4 (ve el .venv), 1.28.5 (olvida lo no instalado; 2>&1 no es una libreria). Sin comprobar: .venv en otra ruta; bloqueo con npm/cargo/go (punto 32). Commit vacio 9222812 en el GitHub de Modelo 2.

## 0 · Proyecto creado con el kit de arranque
**Fecha:** 2026-10-31
Estructura de Cerebro Vivo instalada con `instalar.py`.

## 1 · Repo subido a GitHub privado
**Fecha:** 2026-11-01
Subido a `forxa-ken/cerebro-vivo` (arnés 1.4.1, `e1b483b`) por orden de Darwin. Retirado de pendientes en cerebro-vivo #6.

## 9 · Índice central `.brain/INDICE.md` (DESCARTADO)
**Fecha:** 2026-11-01
Idea de Darwin (versión híbrida). Descartada por Darwin en cerebro-vivo #6: el ahorro de tokens nunca se demostró y añadía un archivo más que leer al arrancar. Los tres archivos de IA siguen como hasta ahora.

## 10 · Skills /resumen, /pendiente y /prompt-inicial separadas (spec 006)
**Fecha:** 2026-11-01
Arnés 1.4.2. Probado por Darwin en un chat nuevo.

## 2 · Retirar el repo viejo `cerebro-vivo-plugins` (decisión tomada)
**Fecha:** 2026-11-01
Darwin pidió retirar el punto de pendientes. El repo viejo NO se ha borrado ni tocado: borrarlo es irreversible y requiere su orden expresa sobre el repo.

## 6 · objetivo.md en el instalador (spec 007, arnés 1.5.0)
**Fecha:** 2026-11-01
Probado por Darwin en `F:\prueba` con Codex: existe `.brain/architecture/objetivo.md` y el chat nuevo lo leyó y dijo que el objetivo aún está por definir (correcto en un proyecto recién creado). La parte `.agents/skills/` (punto 7) sigue abierta.

## 12 · Migrar el objetivo a proyectos ya instalados (spec 008, arnés 1.6.0)
**Fecha:** 2026-11-01
Probado por Darwin: `--migrar-objetivo` creó el objetivo en un proyecto ya instalado (lo usó con Gemini). No se comprobó después la pregunta del objetivo en un chat nuevo de Codex.

## 7 · Skills para Codex en .agents/skills (spec 007, arnés 1.5.0)
**Fecha:** 2026-11-02
Probado por Darwin: con `AGENTS.md` en el proyecto, el actualizador copia las skills a `.agents/skills/` y Codex las usa.

## 11 · Panel /plantilla recuperado (spec 009, arnés 1.7.0)
**Fecha:** 2026-11-02
Probado por Darwin: el plugin `plantilla-prompt` se instala desde este repo y el panel `/plantilla` funciona.

## 3 · Primera adopción real en LoboHook
**Fecha:** 2026-11-07
Darwin confirma que `/actualizar` funciona en LoboHook. Su registro (chat #86) dice que ya estaba en 1.18.2, sin nada que traer, y que `CEREBRO_VIVO.md` figura modificado a mano y no se pisó. No hizo falta `--forzar-todo`. La skill vieja `traspaso-entre-chats` se eliminó de LoboHook el mismo día, con orden de Darwin.

## 18 · `/traspaso-in` abre el chat nuevo solo (arnés 1.12.0 y 1.18.2)
**Fecha:** 2026-11-07
Probado por Darwin en LoboHook. Su confirmación no detalla si miró en el sidebar el mismo nivel del chat nuevo ni si su resumen coincidía con lo hablado.

## 14 · Actualizador fiable (spec 021, arnés 1.19.0; con hooks desde 1.27.1)
**Fecha:** 2026-11-08
Darwin confirma «14 ok» tras probarlo en un proyecto real. Su confirmación no detalla en cuál, ni si lo retirado fue a `.brain/copias_arnes/`, ni qué decidió sobre `modo_auto.py`, `uso_tokens.py` y `test_modo_auto.py` de LoboHook. Además hay prueba automática de punta a punta (`tests/test_esperando_prueba.py`, 1.28.2).

## 26 · `/version` (spec 023, arnés 1.21.0)
**Fecha:** 2026-11-08
Darwin confirma «26 ok». Su confirmación no detalla si probó en Modelo 2 ni qué versión le dijo. Además hay prueba automática de los datos que lee y del aviso de versión nueva (`tests/test_arnes_esperando_prueba.py`, 1.28.3).

## 13 · `traspaso-in` y `traspaso-out` en Codex y Gemini (specs 010 y 011, arnés 1.9.0)
**Fecha:** 2026-11-08
Probado por Darwin en `F:\Modelo` (arnés 1.28.3) con capturas. Codex: `$traspaso-in salgo` escribió traspaso corto y completo; `$traspaso-in entro` en chat nuevo contó 5 viñetas y una pregunta; `$traspaso-out salgo` hizo commit local de solo `.brain/` (`b62ef7a`, 20 archivos), no subió por no haber remoto y avisó de 180 archivos sueltos. Gemini: `traspaso-out entro` contó 4 viñetas y una pregunta. Observaciones: el primer `entro` falló porque Darwin abrió el chat nuevo mientras `salgo` seguía escribiendo (5 min); hay que esperar el aviso de «Traspaso preparado». Sin la palabra, `$traspaso-in` se toma como `salgo`. La suite en el entorno restringido de Codex da errores de permisos y `git push`, no del arnés. La subida a GitHub de `salgo` no se probó (el proyecto no tiene remoto).
