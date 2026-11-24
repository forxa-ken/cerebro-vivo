# Spec 090, fase 3: prueba de uso real, segunda vuelta (2026-11-25, v1.65.3)

**Quién:** Claude (chat #43), otro chat distinto del que construyó el tramo (#41/#42), pero **mismo modelo**: no es una IA de otra familia. Navegador integrado, sobre una carpeta de prueba nueva (git, README y una prueba) en el scratchpad; nunca un proyecto de verdad. Carpeta y entrada del registro borradas al terminar. Web arrancada con `web.py --no-abrir --puerto 8765`.

## Lo comprobado con clics (todo verde)
- Añadir carpeta en Proyectos: sale en la lista; ficha con Resumen, Pendientes, Actualizar, Instalar y Tareas.
- «Instalar de verdad» sin simular: rechazado («Primero simula… hace menos de 10 minutos»); la carpeta no cambió.
- Simular instalar (completo): anuncia 53 archivos **y avisa de «hasta 175» más que copia el actualizador justo después** (el hallazgo de la vuelta anterior, que decía 53 contra 161 reales, queda resuelto en el texto). Instalar de verdad: 165 archivos en disco, hook `pre-commit` puesto, `.gitignore` ampliado.
- Tareas > pruebas del proyecto: salida en vivo; **Parar** aparece, al pulsarlo la tarea queda «Se paró», y no queda ningún `python.exe` hijo vivo (solo la web).
- Tareas > cerrar tarea: la línea se escribió en `.brain/decisions.log` **de la carpeta de prueba**, no en el de cerebro-vivo.
- Tareas > estado del auditor: salida correcta.
- **Actualizar de verdad (no probado en la vuelta anterior):** con un guardián borrado y otro editado a mano, la simulación listó «nuevo: poda.py» y «modificado a mano, NO pisado: longitud.py»; la acción real restauró poda.py y dejó longitud.py idéntico (md5 igual).
- `web_actividad.log` registró registrar, instalar (rechazada y hecha), simular, pruebas, parar, cerrar, auditor y actualizar.
- Contra la web con curl: sin clave, clave mala y `Host` ajeno dan 403.

## Hallazgos menores
- El navegador integrado suprime los `confirm()` (devuelve «no»): para probar hubo que sustituir `window.confirm` por JavaScript. El texto de las confirmaciones sí se leyó (claro y con la ruta). No es fallo de la web.
- En la pestaña Tareas, antes de pulsar nada, se ve el texto «Pulsa «Simular» para ver qué haría…», que ahí no aplica (cosmético).

## No probado
- Origen ajeno en una petición que sí exista: mi prueba con curl dio 405 (ruta que no admite POST), así que no demuestra nada; lo cubren las pruebas automáticas.
- Modo claro, móvil; proyectos grandes; Parar con hijos de verdad más profundos (las pruebas de la copia eran las del propio arnés).
- Una IA de otra familia (la spec la pide); auditor desde la web con `--externo`; los límites ya conocidos (instante entre revalidar y reanudar; ligar tareas a la instancia).
- Dos confirmaciones del mismo clic de «Instalar de verdad» aparecieron (la del rechazo y la de la acción hecha): comportamiento normal, pero no revisado a fondo.
