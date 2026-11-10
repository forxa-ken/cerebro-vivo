# Spec del addon de prueba (fábrica, spec 035 · R13)

- **Estado:** borrador consolidado con las respuestas de Darwin; falta su «sí» final para congelarla.
- **Fecha:** 2026-11-09
- **Cliente:** WoW Forever (interfaz 16001, API moderna tipo Mainline; carpeta `_forever_/Interface/AddOns`). Según fuentes de fans, sin confirmación oficial; se comprueba en el juego.

## Requisitos (R*) con su prueba de aceptación
- **R1** Cada línea del chat muestra el nombre del jugador con el **color de su clase**. *Prueba:* en el juego, jugadores de clases distintas salen con su color.
- **R2** El **nivel solo se muestra si se consulta**: sin consulta no se muestra nada (ni `[?]`). *Prueba:* un desconocido sale solo con nombre coloreado.
- **R3** Al hacer **Shift+clic** en un nombre aparece la información (`[nivel] Nombre <Hermandad>`) **debajo de esa línea**. Solo si el juego lo permite; si no es posible, no se añade. *Prueba:* en el juego; requisito más arriesgado, se comprueba primero.
- **R4** La **hermandad** se muestra solo cuando el juego permite consultarla. Si no, no aparece.
- **R5** Funciona en **todos los canales**.
- **R6** **Botón** en la **esquina superior izquierda** del chat, casi transparente pero visible, al estilo del botón de copiar de Prat (no pude verlo: no encontré su aspecto exacto; se ajusta en el juego). Abre una ventana con las **últimas 200 líneas** del chat, **todo el texto seleccionado** y un **letrero que dice «Ctrl+C»**.
- **R7** *(eliminado por Darwin: no hay comportamiento especial al hacer clic en una línea.)*
- **R8** **Icono en el minimapa** con forma de **pergamino**, de **tamaño proporcional** a los demás iconos del minimapa y **bien ubicado dentro del borde del minimapa**. Al hacer clic **abre la configuración**.
- **R9** **Ventana de configuración** con: idioma (Español / English), valor de N (por defecto 200), activar/desactivar color de clase, activar/desactivar hermandad.
- **R10** Textos en **inglés y español**; el idioma se elige en la configuración (por defecto, el del cliente).

## Fuera de alcance
- Nada que escriba en el portapapeles del sistema, nada que consulte a todos los jugadores automáticamente, nada fuera de estos requisitos.

## Huecos abiertos
- Ninguno de Darwin pendiente. Lo no verificable aquí (aspecto del botón de Prat, comportamiento de la consulta de nivel en WoW Forever) se prueba en el juego.

## Verificación
- Por programa: archivos `.toc`/Lua bien formados, sin errores de sintaxis, textos en es/en completos.
- Por Darwin en el juego: R1 a R9 (puerta final).
