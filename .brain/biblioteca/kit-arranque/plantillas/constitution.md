# Constitución de {{NOMBRE}} (reglas innegociables)

> Si una tarea exige saltarse alguna de estas reglas, **detenerse y pedir autorización explícita a {{DUENO}}**. Fuente única de reglas para todas las IA del proyecto.

1. **Idioma y tono:** responder en **{{IDIOMA}}**, tono técnico y conciso.
2. **Alcance estricto:** trabajar solo sobre lo que atañe al cambio solicitado; prohibido refactorizar o reescribir lo ajeno.
3. **Pruebas siempre en verde:** `{{PRUEBAS}}` tras cada cambio. Con todo en verde y sin un fallo comprobado, no se altera el código existente sin orden directa.
4. **Memoria viva:** al cerrar cada tarea, una línea en `decisions.log` (`python .brain/guardianes/cerrar.py --chat "{{NOMBRE}} #N" "qué se hizo"`) y, si hubo una decisión importante, su ficha `D-NNN` con el porqué.
5. **Pendientes solo con lo que falta:** «implementada» no es «terminada»; sigue en `pendientes.md` hasta que {{DUENO}} la prueba. En cuanto confirma, en esa misma respuesta: detalle a `archive/hechos.md`, fila en `archive/hechos-indice.md` y punto fuera de `pendientes.md`. La numeración es fija.
6. **Memoria de pruebas:** una campaña de pruebas con hallazgos abre su `P-NNN` en `.brain/pruebas/`; al arreglar un hallazgo se marca `- [x]`.
7. **Secretos:** claves y tokens viven en variables de entorno o en archivos ignorados por Git, nunca en el repositorio.
8. **Toda llamada externa** lleva tiempo máximo y un plan B local.
9. **Subir a GitHub** solo con orden expresa de {{DUENO}}. Única excepción: `traspaso-out salgo` sube sin más orden su commit de memoria, y pregunta antes si hay otros commits pendientes.
10. **El objetivo se escribe:** todo objetivo o cambio de objetivo que {{DUENO}} dé en un chat se anota en `.brain/architecture/objetivo.md` en esa misma respuesta; lo que solo está en el chat se pierde.
