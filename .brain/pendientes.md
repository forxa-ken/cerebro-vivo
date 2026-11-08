# Pendientes

Lista viva de **lo que falta**. Una línea por punto. **Numeración fija** (los huecos son puntos ya terminados: están en `archive/hechos-indice.md`).

**Regla de cierre:** cuando Darwin prueba una tarea y confirma, en esa misma respuesta se pasa su detalle a `archive/hechos.md`, se añade su fila a `archive/hechos-indice.md` y se quita de aquí. Si la prueba falla, vuelve a «Falta programar» con una nota de qué falló.

## Falta programar (IA)
- **4:** (opcional) medir el arnés en un proyecto real con `medir.py` durante semanas; GuildControl/GuildControlForever no sirven (no son independientes). Decide los recortes del informe 028.

- **19:** diseñar (spec aparte) cómo colaboran varias IA con responsabilidades distintas en un proyecto (caso Guild Control Forever: Claude con `.brain/`, Gemini solo traducciones con `AGENTS.md`). A decidir: qué lee/escribe cada IA, cómo no pisarse, `indices_ajenos` en `guardianes.json`. Detalle en `archive/pendientes-detalle-2026-11-08.md`.

- **22:** automatizaciones en la nube (Jenkins o GitHub; hoy todo corre en local). Antes: explicarle a Darwin cada opción en llano y que elija. Sin empezar.

- **23:** aprender a montar un agente que verifique las pruebas y errores de la IA principal (revisor independiente; idea somera de Darwin; sale de `F:\Arquitectura de desarrollo`, REC-003/004/005). Explicárselo en llano y hacerlo paso a paso con él. Sin empezar.

- **32:** ampliar `librerias.py` y el guardián `eventos_chat.py` a npm, cargo y go (OSV.dev los cubre; hoy solo avisa). Spec antes; es/en.

- **29:** idea del punto 24 (OpenAI): guardián que detecte memoria desactualizada. Informe 028: hacerlo dentro de la fusión de higiene de memoria, no como guardián nuevo. Spec antes; es/en.

- **30:** idea del punto 24 (OpenAI): que los avisos de los guardianes digan cómo arreglar el problema, no solo qué falló; revisar los de `textos.py` en es/en. Sin empezar.

- **31:** idea del punto 24 (The Harness Effect): cortar un guardián que falla repetidamente y que `medir.py` dé tokens por tarea terminada. Spec antes; es/en.


## Esperando tu prueba (Darwin)
- **28:** guardián con memoria del chat (spec 027, arnés 1.27.0). Prueba: `/actualizar` y reinicia Claude Code; instala una librería sin problemas y haz `git push` (debe pasar callado); con una de fallo conocido debe detenerse.
- **20:** chat nuevo solo (arnés 1.23.0 a 1.26.2; junta los antiguos 16 y 27). Pasos: en un proyecto de prueba pon `longitud_aviso_tokens` en 20000 y habla hasta el aviso; Claude debe abrir el chat nuevo al mismo nivel, decirte su nombre y no repetir el aviso en cada mensaje. Si falla, dime qué frase dijo la IA.
- **13:** `traspaso-in`/`traspaso-out` (specs 010 y 011, arnés 1.9.0). Prueba en Codex (`$traspaso-in salgo`, chat nuevo, `$traspaso-in entro`) y en Gemini (`traspaso-out entro`, sin probar). Debe contarte lo último hablado. Pasos exactos en `archive/pendientes-detalle-2026-11-08.md`.
- **17:** soporte para Mac (spec 013, arnés 1.11.0; solo probado en Windows). Prueba en un Mac: `python3 -m unittest discover tests`, doble clic en `instalar_kit.command` y abrir Claude Code en el proyecto de prueba.
- **14:** actualizador fiable (spec 021, arnés 1.19.0; con hooks desde 1.27.1). Solo ensayado en copias. Prueba: en un proyecto real `/actualizar` (o `python actualizar.py RUTA --simular` y luego sin él); lo retirado debe ir a `.brain/copias_arnes/`. En LoboHook decide si sobran `modo_auto.py`, `uso_tokens.py` y `test_modo_auto.py`.
- **21:** nada suelto ni viejo (spec 022, arnés 1.20.0). Prueba: `/traspaso-out salgo` en un proyecto con remoto debe hacer commit de la memoria, subirlo y listar el código suelto sin meterlo; y con `/actualizar` mira si el aviso ayuda o estorba.
- **26:** `/version` (spec 023, arnés 1.21.0). Prueba: en Modelo 2 (actualizado; reinicia Claude Code) escribe `/version`; debe decir 1.21.0, si hay otra más nueva y cómo actualizar.
## Acciones tuyas
