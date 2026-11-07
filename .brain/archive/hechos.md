# Hechos (tareas terminadas y probadas)

> Aquí va el detalle de cada tarea **ya probada por Darwin**. `pendientes.md` solo guarda lo que falta.
> **No abrir completo:** consultar `hechos-indice.md` y leer solo la entrada necesaria (buscar `## <Nº>`).
> La **numeración es fija**: el número que tenía el punto en `pendientes.md` no cambia al moverlo aquí.

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
