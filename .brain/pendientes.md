# Pendientes

Lista viva de **lo que falta**. Una línea por punto. **Numeración fija** (los huecos son puntos ya terminados: están en `archive/hechos-indice.md`).

**Regla de cierre:** cuando Darwin prueba una tarea y confirma, en esa misma respuesta se pasa su detalle a `archive/hechos.md`, se añade su fila a `archive/hechos-indice.md` y se quita de aquí. Si la prueba falla, vuelve a «Falta programar» con una nota de qué falló.

Estado al 2026-11-01 (cerebro-vivo #6): arnés 1.4.1 subido a GitHub; spec 006 hecha y probada (1.4.2).

## Falta programar (IA)
- **2:** decidir cuándo retirar el repo viejo `cerebro-vivo-plugins` (no se borra nada hasta que Darwin lo diga).
- **3:** primera adopción real: actualizar LoboHook con `--simular` y luego `--forzar-todo` (con orden de Darwin).

- **4:** (opcional, sin urgencia) medir el arnés en un proyecto real con `medir.py` durante semanas para comprobar la hipótesis de que ahorra a la larga; los proyectos gemelos GuildControl/GuildControlForever NO sirven como comparación (Darwin adapta los cambios de uno a otro, así que no son independientes); solo si Darwin quiere una cifra más firme, spec 004 con una tarea larga repartida en 3-4 chats.

- **6:** (hueco real visto en el proyecto Modelo, 2026-11-01) el objetivo del proyecto vivía solo en el chat de Gemini y Codex no lo sabía. Que `instalar.py` cree `architecture/objetivo.md` desde una plantilla, que los índices de entrada (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`) lo enlacen como lo primero a leer y que la constitución diga que todo objetivo dado por Darwin se escribe ahí en la misma respuesta. Con su prueba; subir `VERSION`.
- **7:** que el instalador deje también las skills en `.agents/skills/` (Codex las lee de ahí y las invoca con `$`, no `/`); hoy hubo que adaptarlas a mano en Modelo (spec 005 de Modelo, 15 skills, `$prompt-inicial` ya funciona).


## Esperando tu prueba (Darwin)

## Acciones tuyas
