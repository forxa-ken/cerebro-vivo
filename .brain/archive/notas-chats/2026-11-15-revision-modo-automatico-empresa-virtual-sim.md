# Revisión del modo automático con empresa-virtual-sim (pendientes 57 y 58)

- **Quién / cuándo:** Claude (cerebro-vivo #29), 2026-11-15. Solo lectura sobre `empresa-virtual-sim`; nada tocado allí.
- **Fuentes:** `.brain/fabrica/` (gasto, carta, huecos, propuestas, evidencia), git del proyecto y los cuatro chats de la línea (transcripciones: mensajes de Darwin y preguntas de la directora).
- **Qué NO se miró:** el código del simulador ni si las explicaciones enseñan bien VMware (lo juzga Darwin); no se abrió GitHub.

## Resultado en cifras
- 10 encargos (001 a 010), todos fusionados en `fase1`; Darwin aceptó la rama y `main` = `fase1` (`a6df9a5`), **sin subir a GitHub** (origen en `46499e5`). 1 fallo anotado en todo el gasto.
- Gasto: 3.233.844 tokens (ejecutora 2.120.771, revisora 800.577, Codex 312.496). Tope de misión final 3.600.000 (partió de 1.000.000 por defecto).
- Darwin tuvo que decidir o empujar de más:
  - **Topes:** 7 preguntas por tope; el de misión se subió 5 veces (1,6 / 2,0 / 2,6 / 3,2 / 3,6 millones) y el de encargo una (400.000 a 800.000).
  - **«Sigue con…»:** al menos 8 mensajes de empuje («sigue con el 006», «con el 005», «con la revisión del 007», «con la fusión del 007», «con el 009»…) y 4 «cómo vas». La directora se quedaba esperando a Codex o a un subagente sin que nada la despertara.
  - **Una pregunta entre encargos** («¿Sigo con el 003?», a las 00:01), antes de que existiera la regla de la 1.59.0.

## Lo que funcionó
- La cadena spec → revisor de spec → carta → encargos → revisión por encargo → prueba de uso real fue completa y dejó evidencia. El revisor del encargo 007 halló que 12 de 32 roturas sobrevivían; se reforzaron las pruebas.
- La prueba de uso real de R-10 (57 comprobaciones) y el probador independiente señalaron los fallos de contenido de las explicaciones; eso originó el encargo 010 y Darwin lo confirmó leyendo.
- Las paradas por tope y por spec sí pararon (no hubo gasto sin permiso).

## Hallazgos para el arnés
1. **Topes mal calculados (pendiente 58).** La carta dice «tokens de Codex» pero `fabrica.py topes` suma todos los papeles; el gasto de la ejecutora Claude (subagentes) es el 65 % y es lo que dispara el tope. Los valores por defecto (1.000.000 por misión, 400.000 por encargo) no sirven para una misión real: la media fue ~320.000 por encargo. Hay que decidir qué cuenta, topes por papel o un tope sugerido según el número de encargos, y qué pasa cuando Darwin ya aprobó una ampliación.
2. **La directora se para esperando a un subagente o a Codex** y Darwin tiene que despertarla. La skill dice «lanza el siguiente de inmediato» pero no da cómo esperar (vigilante en segundo plano) ni qué hacer al volver. Falta decirlo explícito en `directora-de-fabrica`.
3. **Una spec con un hueco que el revisor de spec no vio:** el negocio decía «aprender de forma certera» y la spec v3 no pedía ninguna explicación; lo detectó Darwin probando («no veo ningún tipo de explicación»), no el revisor. Añadir al revisor de spec la pregunta «¿el objetivo del negocio tiene un requisito que lo cumpla?».
4. **El informe final no se actualiza con una spec nueva (v4):** `informe.md` sigue siendo el de la fase 1 (spec v3, 9 requisitos) y no menciona R-10 ni el encargo 010. (No se comprobó si lo guardó en otro sitio; en `.brain/fabrica/` no hay otro.)
5. **Tope de encargos a la vez que cambia el alcance:** 10 encargos era justo el 010; un undécimo habría vuelto a pedir permiso. Un cambio de spec aprobado por Darwin debería reabrir los topes de forma explícita en vez de uno a uno.
6. **Separación del chat nuevo (v1.59.3):** no se pudo comprobar en esta tanda (los chats #3 y #4 ya existían); queda para el próximo traspaso real.

## Siguiente
- Arreglar 1, 2, 3, 4 y 5 en el arnés (versión nueva) con las pruebas habituales; luego traer la 1.59.x al proyecto con `actualizar_arnes.py --simular` (la línea ya terminó).
