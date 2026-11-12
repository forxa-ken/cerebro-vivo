# Pendientes

Lista viva de **lo que falta**. Una línea por punto. **Numeración fija** (los huecos son puntos ya terminados: están en `archive/hechos-indice.md`).

**Regla de cierre:** cuando Darwin prueba una tarea y confirma, en esa misma respuesta se pasa su detalle a `archive/hechos.md`, se añade su fila a `archive/hechos-indice.md` y se quita de aquí. Si la prueba falla, vuelve a «Falta programar» con una nota de qué falló.

## Falta programar (IA)
- **19:** [spec 035 APROBADA el 2026-11-10; Fases 1, 2 y 3 HECHAS el 2026-11-10 (plantillas en `biblioteca/PLANTILLAS_FABRICA` y `CARTA_EJECUTORA`, guardián `fabrica.py`, arnés 1.32.0, sin subir); skills y regla R9 en arnés 1.33.0; prueba mínima R13 HECHA el 2026-11-10 (informe en `archive/informe-r13-traductorvoz-2026-11-10.md`) y prueba de Codex con ventana llena cerrada (hechos 19-B; el tope de 200k es riesgo aceptado: lo cubre el diseño de encargos pequeños, no una medición en vivo); medidor de gasto de Codex HECHO el 2026-11-10 (arnés 1.34.0, `medir.py --fabrica`); coste de la directora en `medir.py --fabrica` HECHO el 2026-11-12 (arnés 1.40.0); el coste por tarea terminada sigue en el punto 31] diseñar (spec aparte) cómo colaboran varias IA con responsabilidades distintas en un proyecto (caso Guild Control Forever: Claude con `.brain/`, Gemini solo traducciones con `AGENTS.md`). A decidir: qué lee/escribe cada IA, cómo no pisarse, `indices_ajenos` en `guardianes.json`. Detalle en `archive/pendientes-detalle-2026-11-08.md`.
  - **Prueba de ventana llena de Codex: CERRADA el 2026-11-10 por decisión de Darwin** (detalle en `archive/hechos.md`, punto 19-B). Relevo probado; aviso automático en vivo NO probado (riesgo conocido y barato: tope 200k por tanda, encargos pequeños, guardián al terminar cada tanda; vigilante en vivo solo si algún día un desbordamiento duele).

- **23:** aprender a montar un agente que verifique las pruebas y errores de la IA principal (revisor independiente; idea somera de Darwin; sale de `F:\Arquitectura de desarrollo`, REC-003/004/005). Explicárselo en llano y hacerlo paso a paso con él. Sin empezar.


- **37:** experimento VMware CERRADO (rondas 1-5, informes en `.brain/archive/informe-*vmware*`). Conclusión: las reglas de seguridad son lo que decide (skill `seguridad-en-sistemas-reales`, arnés 1.30.0); ODD + reglas para tareas puntuales, Cerebro Vivo + reglas para proyectos largos. Falta: (a) repetir la prueba de seguridad contra `vcsim`/`pyvmomi` (necesita el sí de Darwin para instalar Go); (b) HECHO el 2026-11-12 (arnés 1.40.2: `test_soporte_mac` se salta fuera del repo del arnés, donde Git de Windows convierte el fin de línea); (c) revisar la regla «vcsim» de `AGENTS.md` del aprobador.

## Esperando tu prueba (Darwin)
- **30:** avisos de los guardianes con el cómo arreglarlo (arnés 1.40.1). 18 avisos de la fábrica, base de datos, traspaso e índices añaden una frase final con la solución. Prueba: provoca uno, por ejemplo `python .brain/guardianes/fabrica.py alcance` sin foto previa, y comprueba que el aviso dice qué comando lanzar.
- **29:** memoria desactualizada (spec 037, arnés 1.36.0, sin subir): `revisar_indices.py` avisa de rutas, specs y fichas citadas en `pendientes.md` y `constitution.md` que ya no existen. Prueba: `python .brain/guardianes/revisar_indices.py` y mirar si los avisos son reales. Comprobado 2026-11-12: da «Sin hallazgos»; la constitución ya cita `metodo-scripts-y-heredocs.md`, que existe.
- **31:** guardián que se repite y tokens por tarea (spec 038, arnés 1.36.0, sin subir): `cierre.py` apaga en el chat un aviso informativo que sale 3 veces seguidas; `medir.py` muestra «Por tarea terminada». Prueba: `python .brain/guardianes/medir.py --ultimos 3` y ver en un chat largo que el aviso de hito no se repite sin fin.

- **35:** cierre por bloque (spec 033, arnés 1.29.0): el guardián ya no pide la línea de registro hasta 15 archivos editados sin cerrar. Prueba: trabaja en un chat de cerebro-vivo con varias tareas pequeñas y comprueba que no salta el aviso en cada una; al final del bloque, pídele a la IA que cierre. Si falla, dime qué aviso salió. Medir con `python .brain/guardianes/medir.py --ritual` en 2 semanas.
- **36:** prueba de retomar en el cierre (spec 041, arnés 1.41.0, sin subir): regla nueva en la skill `cerrar-una-tarea` y una frase en el aviso del guardián. Prueba: en un chat de trabajo, comprueba que la IA cierra antes de 15 ediciones cuando hay una decisión que solo está en la conversación. Medir con `python .brain/guardianes/medir.py --ritual` en 2 semanas, junto al 35.
## Acciones tuyas
