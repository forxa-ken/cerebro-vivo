# Pendientes

Lista viva de **lo que falta**. Una línea por punto. **Numeración fija** (los huecos son puntos ya terminados: están en `archive/hechos-indice.md`).

**Regla de cierre:** cuando Darwin prueba una tarea y confirma, en esa misma respuesta se pasa su detalle a `archive/hechos.md`, se añade su fila a `archive/hechos-indice.md` y se quita de aquí. Si la prueba falla, vuelve a «Falta programar» con una nota de qué falló.

## Falta programar (IA)
- **19:** [spec 035 APROBADA el 2026-11-10; Fases 1, 2 y 3 HECHAS el 2026-11-10 (plantillas en `biblioteca/PLANTILLAS_FABRICA` y `CARTA_EJECUTORA`, guardián `fabrica.py`, arnés 1.32.0, sin subir); skills y regla R9 en arnés 1.33.0; prueba mínima R13 HECHA el 2026-11-10 (informe en `archive/informe-r13-traductorvoz-2026-11-10.md`) y prueba de Codex con ventana llena cerrada (hechos 19-B; el tope de 200k es riesgo aceptado: lo cubre el diseño de encargos pequeños, no una medición en vivo); medidor de gasto de Codex HECHO el 2026-11-10 (arnés 1.34.0, `medir.py --fabrica`); falta solo el coste de la directora por tarea, que va en el punto 31] diseñar (spec aparte) cómo colaboran varias IA con responsabilidades distintas en un proyecto (caso Guild Control Forever: Claude con `.brain/`, Gemini solo traducciones con `AGENTS.md`). A decidir: qué lee/escribe cada IA, cómo no pisarse, `indices_ajenos` en `guardianes.json`. Detalle en `archive/pendientes-detalle-2026-11-08.md`.
  - **Prueba de ventana llena de Codex: CERRADA el 2026-11-10 por decisión de Darwin** (detalle en `archive/hechos.md`, punto 19-B). Relevo probado; aviso automático en vivo NO probado (riesgo conocido y barato: tope 200k por tanda, encargos pequeños, guardián al terminar cada tanda; vigilante en vivo solo si algún día un desbordamiento duele).
  - Sub-pendiente (2026-11-10): coste de la directora (Claude) por tarea en el medidor de la fábrica; se une al punto 31. El gasto de Codex ya lo suma `medir.py --fabrica` (1.34.0, probado con las 11 sesiones de R13: encargo 007 = 229k, igual que la anotación a mano).

- **22:** automatizaciones en la nube (Jenkins o GitHub; hoy todo corre en local). Antes: explicarle a Darwin cada opción en llano y que elija. Sin empezar.

- **23:** aprender a montar un agente que verifique las pruebas y errores de la IA principal (revisor independiente; idea somera de Darwin; sale de `F:\Arquitectura de desarrollo`, REC-003/004/005). Explicárselo en llano y hacerlo paso a paso con él. Sin empezar.

- **32:** ampliar `librerias.py` y el guardián `eventos_chat.py` a npm, cargo y go (OSV.dev los cubre; hoy solo avisa). Spec antes; es/en.

- **29:** idea del punto 24 (OpenAI): guardián que detecte memoria desactualizada. Informe 028: hacerlo dentro de la fusión de higiene de memoria, no como guardián nuevo. Spec antes; es/en.

- **30:** idea del punto 24 (OpenAI): que los avisos de los guardianes digan cómo arreglar el problema, no solo qué falló; revisar los de `textos.py` en es/en. Sin empezar.

- **31:** idea del punto 24 (The Harness Effect): cortar un guardián que falla repetidamente y que `medir.py` dé tokens por tarea terminada. Spec antes; es/en.

- **25:** distancia con un proyecto externo. HECHO el 2026-11-10 (arnés 1.34.1, 1.34.2 y 1.35.0): un autor externo, Stanford (Meta-Harness) y Databricks (Omnigent) como «Fuentes» en README, manual y página; «Fast-Track» pasó a «Cambio pequeño» / «Small change». Investigado en Internet: constitución, decisión y registro de decisiones son términos estándar del sector (Spec Kit, ADR), no de un autor externo; pendiente no existe en un proyecto externo; meta-arnés es ya un término público. Fuentes ampliadas (1.35.2) con ADR (Nygard, Fowler, Microsoft, Red Hat, AWS) y Spec Kit, para cubrir decisión y constitución sin renombrar. Queda por decidir con Darwin: (a) si aun así cambia pendiente → por-hacer, constitución → estatutos, decisión → elección, meta-arnés → Red cerebral (riesgo: confusión con «red neuronal»; afecta nombres de archivo; hacerlo en dos tandas y con spec); (b) qué otros autores base añadir a «Fuentes» (Darwin da la lista).

- **36:** mejora (idea de ODD, informe `archive/informe-odd-gentle-shell-2026-11-09.md`): usar el «resume test» (¿se puede retomar el trabajo solo con la petición y los cambios del código?) como segundo criterio, junto al contador de 15 ediciones del cierre por bloque y a la regla de «más de 2 archivos» de `spec-antes-de-programar`. Pequeño y reversible. Hacerlo después de ver los resultados del punto 35 (`medir.py --ritual`). Spec antes; es/en. Sin empezar.

- **37:** experimento VMware CERRADO (rondas 1-5, informes en `.brain/archive/informe-*vmware*`). Conclusión: las reglas de seguridad son lo que decide (skill `seguridad-en-sistemas-reales`, arnés 1.30.0); ODD + reglas para tareas puntuales, Cerebro Vivo + reglas para proyectos largos. Falta: (a) repetir la prueba de seguridad contra `vcsim`/`pyvmomi` (necesita el sí de Darwin para instalar Go); (b) arreglar `test_soporte_mac` (fin de línea de Windows); (c) revisar la regla «vcsim» de `AGENTS.md` del aprobador.

- **39:** TraductorVoz: investigar cómo separar mejor a los hablantes (hallazgo de la prueba R13, 2026-11-10). Hoy se corta solo por silencio y hay una huella por frase: dos voces seguidas caen en una frase y salen con un solo hablante. Ideas a investigar: cortar la frase cuando cambia la voz (ventanas de 1-2 s con huella), diarización neural con licencia libre, ajustar el umbral. Evidencia y audios en `F:\Proyectos\TraductorVoz-notas\evidencia-hablantes-aleman.md`. Sin empezar; entra en el informe final de R13.

## Esperando tu prueba (Darwin)
- **35:** cierre por bloque (spec 033, arnés 1.29.0): el guardián ya no pide la línea de registro hasta 15 archivos editados sin cerrar. Prueba: trabaja en un chat de cerebro-vivo con varias tareas pequeñas y comprueba que no salta el aviso en cada una; al final del bloque, pídele a la IA que cierre. Si falla, dime qué aviso salió. Medir con `python .brain/guardianes/medir.py --ritual` en 2 semanas.
## Acciones tuyas
