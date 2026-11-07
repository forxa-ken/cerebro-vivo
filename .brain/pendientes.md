# Pendientes

Lista viva de **lo que falta**. Una línea por punto. **Numeración fija** (los huecos son puntos ya terminados: están en `archive/hechos-indice.md`).

**Regla de cierre:** cuando Darwin prueba una tarea y confirma, en esa misma respuesta se pasa su detalle a `archive/hechos.md`, se añade su fila a `archive/hechos-indice.md` y se quita de aquí. Si la prueba falla, vuelve a «Falta programar» con una nota de qué falló.

Estado al 2026-11-01 (cerebro-vivo #7): arnés 1.7.0 subido a GitHub; specs 006 a 009 probadas; nada esperando tu prueba.

## Falta programar (IA)
- **4:** (opcional, sin urgencia) medir el arnés en un proyecto real con `medir.py` durante semanas para comprobar la hipótesis de que ahorra a la larga; los proyectos gemelos GuildControl/GuildControlForever NO sirven como comparación (Darwin adapta los cambios de uno a otro, así que no son independientes); solo si Darwin quiere una cifra más firme, spec 004 con una tarea larga repartida en 3-4 chats.


- **14:** el actualizador copia guardianes y pruebas del arnés a proyectos instalados en nivel medio (que no tienen `guardianes.json`) y los deja rotos (caso `F:\Pegatinas`); decidir si se salta o avisa. Spec aparte.
- **19:** diseñar (spec aparte, sin programar) cómo colaboran varias IA en un mismo proyecto cuando sus responsabilidades son distintas. Caso real: Guild Control Forever, donde Claude trabaja con la memoria `.brain/` y Gemini (Antigravity) solo hace traducciones con sus reglas en `AGENTS.md`, que no se edita. A decidir: qué archivos lee y escribe cada IA, cómo se avisan los cambios entre ellas sin que una pise a otra, si el instalador debe respetar archivos ajenos (idea: `indices_ajenos` en `guardianes.json`; hoy reinstalar con `--ias gemini/codex` añadiría el bloque de memoria a ese `AGENTS.md`) y cómo encajan `traspaso-out` y los roles por IA.

- **20:** arreglar `traspaso-in salgo` cuando el chat nació de OTRA sesión (caso real, chat #14): el aviso de chat largo y la skill mandan abrir el chat nuevo con `start_session`, pero la app lo rechaza mientras se trabaja sobre un mensaje de una sesión; la IA dijo «no puedo abrirlo» y solo funcionó cuando Darwin lo pidió con sus palabras («tu lo puedes abrir como que no?»). Además el aviso de >200k tokens se repitió en cada mensaje (unas 10 veces) y Darwin tuvo que insistir. A decidir en una spec: (a) la skill debe probar `start_session` con `user_asked` si el último mensaje es de Darwin y, si la app lo rechaza, decirlo claro y dar UNA frase para pegar en vez de repetir el aviso; (b) el aviso del arranque/cierre no debe repetirse en cada mensaje una vez dado (p. ej. recordar «ya avisado» hasta que el chat cambie); (b2) mientras se espera, `traspaso.md` debe escribirse una sola vez y actualizarse, no reescribirse; (c) comprobar que `detach_session` deja el chat nuevo al mismo nivel.

## Esperando tu prueba (Darwin)
- **13:** `traspaso-in` y `traspaso-out` (specs 010 y 011, arnés 1.9.0, sin subir). Qué es: pasar de un chat a otro con la misma IA (`traspaso-in`) y de una IA a otra (`traspaso-out`). Pasos: actualiza un proyecto (`python actualizar.py RUTA`); en Codex escribe `$traspaso-in salgo`, abre un chat nuevo y escribe `$traspaso-in entro`; luego `$traspaso-out salgo` en Codex y, en Gemini (pídele que lea `GEMINI.md` y la skill), `traspaso-out entro`. Si va bien: te cuenta lo último que hablaron. Gemini sin probar.
- **16:** aviso de chat largo que abre el chat nuevo al mismo nivel (spec 012, arnés 1.10.0, sin subir). Pasos: en un proyecto de prueba pon `longitud_aviso_tokens` bajo (p. ej. 20000) en `guardianes.json`, habla hasta que salte el aviso y comprueba que Claude abre el chat nuevo, lo deja al mismo nivel que el anterior y te dice su nombre.
- **17:** soporte para Mac (spec 013, arnés 1.11.0, sin subir). Solo probado en Windows. Pasos en un Mac: `python3 -m unittest discover tests`; doble clic en `instalar_kit.command` (si no abre, `chmod +x instalar_kit.command`) y crea un proyecto de prueba; abre Claude Code ahí y mira que el arranque muestra el resumen.
## Acciones tuyas
