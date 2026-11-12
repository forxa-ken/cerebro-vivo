# Pendientes

Lista viva de **lo que falta**. Una línea por punto. **Numeración fija** (los huecos son puntos ya terminados: están en `archive/hechos-indice.md`).

**Regla de cierre:** cuando Darwin prueba una tarea y confirma, en esa misma respuesta se pasa su detalle a `archive/hechos.md`, se añade su fila a `archive/hechos-indice.md` y se quita de aquí. Si la prueba falla, vuelve a «Falta programar» con una nota de qué falló.

## Falta programar (IA)



- **37:** experimento VMware CERRADO (rondas 1-5, informes en `.brain/archive/informe-*vmware*`). Conclusión: las reglas de seguridad son lo que decide (skill `seguridad-en-sistemas-reales`, arnés 1.30.0); ODD + reglas para tareas puntuales, Cerebro Vivo + reglas para proyectos largos. Falta: (a) repetir la prueba de seguridad contra `vcsim`/`pyvmomi` (necesita el sí de Darwin para instalar Go); (b) HECHO el 2026-11-12 (arnés 1.40.2: `test_soporte_mac` se salta fuera del repo del arnés, donde Git de Windows convierte el fin de línea); (c) revisar la regla «vcsim» de `AGENTS.md` del aprobador.

## Esperando tu prueba (Darwin)
- **30:** avisos de los guardianes con el cómo arreglarlo (arnés 1.40.1). 18 avisos de la fábrica, base de datos, traspaso e índices añaden una frase final con la solución. Prueba: provoca uno, por ejemplo `python .brain/guardianes/fabrica.py alcance` sin foto previa, y comprueba que el aviso dice qué comando lanzar.
- **29:** memoria desactualizada (spec 037, arnés 1.36.0, sin subir): `revisar_indices.py` avisa de rutas, specs y fichas citadas en `pendientes.md` y `constitution.md` que ya no existen. Prueba: `python .brain/guardianes/revisar_indices.py` y mirar si los avisos son reales. Comprobado 2026-11-12: da «Sin hallazgos»; la constitución ya cita `metodo-scripts-y-heredocs.md`, que existe.
- **31:** guardián que se repite y tokens por tarea (spec 038, arnés 1.36.0, sin subir): `cierre.py` apaga en el chat un aviso informativo que sale 3 veces seguidas; `medir.py` muestra «Por tarea terminada». Prueba: `python .brain/guardianes/medir.py --ultimos 3` y ver en un chat largo que el aviso de hito no se repite sin fin.

- **35:** cierre por bloque (spec 033, arnés 1.29.0): el guardián ya no pide la línea de registro hasta 15 archivos editados sin cerrar. Prueba: trabaja en un chat de cerebro-vivo con varias tareas pequeñas y comprueba que no salta el aviso en cada una; al final del bloque, pídele a la IA que cierre. Si falla, dime qué aviso salió. Medir con `python .brain/guardianes/medir.py --ritual` en 2 semanas.
- **36:** prueba de retomar en el cierre (spec 041, arnés 1.41.0, sin subir): regla nueva en la skill `cerrar-una-tarea` y una frase en el aviso del guardián. Prueba: en un chat de trabajo, comprueba que la IA cierra antes de 15 ediciones cuando hay una decisión que solo está en la conversación. Medir con `python .brain/guardianes/medir.py --ritual` en 2 semanas, junto al 35.
- **42:** modo colaborativo y Gemini como obrera (spec 042, arnés 1.42.0, sin subir). Prueba: (1) en un proyecto de prueba, `/colabora si` y comprueba que crea `.brain/colaboracion.md`, pone una línea en cada índice y el arranque dice «MODO COLABORATIVO ACTIVADO»; `/colabora no` la quita. (2) Escribe `gemini` en una terminal e inicia sesión con tu cuenta de Google; luego dime y corremos un encargo mínimo (una traducción) para probar la viñeta de Gemini, que sigue **sin probar**. (3) `indices_ajenos` en `guardianes.json`: ponlo con `["AGENTS.md"]` y comprueba que reinstalar o actualizar no lo toca.
- **43:** proyectos hermanos (spec 043, arnés 1.43.0, sin subir). Prueba: en un proyecto con hermano, pon `proyectos_hermanos` en su `guardianes.json` (nombre, ruta, rama, archivo_portar), crea el archivo de portar con la plantilla `PLANTILLA_PORTAR.md` (skill `hermanos`) y lanza `python .brain/guardianes/hermanos.py`: los commits que salen deben ser reales (solo lectura, **sin probar con proyectos reales**).
- **23:** auditor (spec 044, arnés 1.44.0, sin subir). Programado y con 23 pruebas en verde; **sin probar en un trabajo real con la IA**. Prueba: (1) `python .brain/guardianes/auditor.py estado` y `quien spec`; (2) en un proyecto, cambia un `.py` y comprueba que al cerrar sale el aviso «lanza el auditor»; con solo un `.md` no debe salir; (3) pide `/auditor general` sobre una carpeta pequeña y mira que lance a Sonnet y a Codex y junte un informe con coincidencias y discrepancias. `/auditor externo no` debe dejar solo al interno.
## Acciones tuyas
