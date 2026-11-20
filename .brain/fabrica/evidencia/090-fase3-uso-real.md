# Spec 090, fase 3: prueba de uso real (2026-11-20)

**Quién:** la misma IA que construyó el tramo (Claude #41), no una distinta: la spec pide otra IA, esto **no** la sustituye. Navegador integrado, sobre una carpeta de prueba (README y una prueba), nunca un proyecto de verdad. Carpeta y registro de prueba borrados al terminar.

## Lo comprobado con clics
- Añadir la carpeta en Proyectos (pidió confirmación): sale en la lista.
- «Instalar de verdad» **sin simular antes**: rechazado con el aviso, la carpeta no cambió.
- Simular instalación (nivel completo) y luego instalar de verdad: hecho; creó 161 archivos con avisos finales (sin git, hook de secretos pendiente).
- Tareas > correr pruebas: salida en vivo, botón **Parar** aparece, y al pulsarlo la tarea queda «Se paró».
- Tareas > cerrar tarea: escribió la línea en `.brain/decisions.log` **de la carpeta de prueba** (no en cerebro-vivo).
- `web_actividad.log` registró instalar (rechazada y hecha), pruebas, parar y cerrar.

## Hallazgo
- La simulación de instalar anunció **53 archivos** y la real creó **161**: el actualizador añade el resto justo después de instalar y la simulación no lo cuenta. No peligroso, pero la simulación subestima. Pendiente de corregir o de avisar en el texto.

## No probado
- Actualizar de verdad desde la web (solo por pruebas automáticas); el auditor desde la web; modo claro/móvil; ejecución en un proyecto con git; que **Parar** mate también los procesos hijos de las pruebas (solo se mata el proceso directo).
- Prueba por una IA distinta y auditor externo (la spec los pide para cerrar la fase 3).
