# Constitución de cerebro-vivo (reglas innegociables)

> Si una tarea exige saltarse alguna de estas reglas, **detenerse y pedir autorización explícita a Darwin**. Fuente única de reglas para todas las IA del proyecto.

1. **Idioma y tono:** responder en **español**, tono técnico y conciso.
2. **Alcance estricto:** trabajar solo sobre lo que atañe al cambio solicitado; prohibido refactorizar o reescribir lo ajeno.
3. **Pruebas siempre en verde:** `python -m unittest discover tests` tras cada cambio. Con todo en verde y sin un fallo comprobado, no se altera el código existente sin orden directa.
4. **Memoria viva:** al cerrar cada tarea, una línea en `decisions.log` (`python .brain/guardianes/cerrar.py --chat "cerebro-vivo #N" "qué se hizo"`) y, si hubo una decisión importante, su ficha `D-NNN` con el porqué.
5. **Pendientes solo con lo que falta:** «implementada» no es «terminada»; sigue en `pendientes.md` hasta que Darwin la prueba. En cuanto confirma, en esa misma respuesta: detalle a `archive/hechos.md`, fila en `archive/hechos-indice.md` y punto fuera de `pendientes.md`. La numeración es fija.
6. **Memoria de pruebas:** una campaña de pruebas con hallazgos abre su `P-NNN` en `.brain/pruebas/`; al arreglar un hallazgo se marca `- [x]`.
7. **Secretos:** claves y tokens viven en variables de entorno o en archivos ignorados por Git, nunca en el repositorio.
8. **Toda llamada externa** lleva tiempo máximo y un plan B local.
9. **Subir a GitHub** solo con orden expresa de Darwin. Única excepción: `traspaso-out salgo` sube sin más orden su commit de memoria, y pregunta antes si hay otros commits pendientes (spec 022).
10. **Editar código sin trucos de terminal:** los bloques de código (más de 3 líneas) se escriben con las herramientas Edit o Write, nunca con un script Python en heredoc, donde `\n` y las comillas se estropean; si aun así se edita con script, comprobar la sintaxis (`python -c "import ast; ast.parse(open('ARCHIVO', encoding='utf-8').read())"`) antes de seguir. Falló 3 veces (lección en `.brain/lecciones/metodo-heredocs-saltos-de-linea.md`).
11. **Un parche se llama parche:** si lo que se entrega arregla el síntoma y no la causa (por ejemplo, saltar una prueba en vez de quitarla de donde no pinta), decirlo con esa palabra, «es un parche», y qué falta para arreglarlo de raíz. Nunca presentarlo como arreglo. Pedido por Darwin el 2026-11-12.
