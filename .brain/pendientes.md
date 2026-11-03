# Pendientes

Lista viva de **lo que falta**. Una línea por punto. **Numeración fija** (los huecos son puntos ya terminados: están en `archive/hechos-indice.md`).

**Regla de cierre:** cuando Darwin prueba una tarea y confirma, en esa misma respuesta se pasa su detalle a `archive/hechos.md`, se añade su fila a `archive/hechos-indice.md` y se quita de aquí. Si la prueba falla, vuelve a «Falta programar» con una nota de qué falló.

Estado al 2026-11-01 (cerebro-vivo #7): arnés 1.7.0 subido a GitHub; specs 006 a 009 probadas; nada esperando tu prueba.

## Falta programar (IA)
- **3:** primera adopción real: actualizar LoboHook con `--simular` y luego `--forzar-todo` (con orden de Darwin).

- **4:** (opcional, sin urgencia) medir el arnés en un proyecto real con `medir.py` durante semanas para comprobar la hipótesis de que ahorra a la larga; los proyectos gemelos GuildControl/GuildControlForever NO sirven como comparación (Darwin adapta los cambios de uno a otro, así que no son independientes); solo si Darwin quiere una cifra más firme, spec 004 con una tarea larga repartida en 3-4 chats.


- **14:** el actualizador copia guardianes y pruebas del arnés a proyectos instalados en nivel medio (que no tienen `guardianes.json`) y los deja rotos (caso `F:\Pegatinas`); decidir si se salta o avisa. Spec aparte.

## Esperando tu prueba (Darwin)
- **13:** `/cambio-de-ia` (spec 010, arnés 1.8.0, sin subir). Qué es: pasar el trabajo entre Claude, Gemini y Codex. Pasos: actualiza un proyecto con Gemini y Codex (`python actualizar.py RUTA`), abre un chat nuevo en Codex y escribe `$cambio-de-ia`, di «salgo»; abre Gemini, pídele que lea `GEMINI.md` y la skill y di «entro». Si va bien: te cuenta lo que dejó la primera. Lo de Gemini sin probar.
## Acciones tuyas
