# Spec 016: revisión periódica de los índices de IA (CLAUDE.md, GEMINI.md, AGENTS.md)

- **Estado:** implementada en 1.14.0 y probada con las pruebas del repo y sobre una copia de Guild Control Forever (Windows); la doble pasada con IA y el reparto real quedan por probar en el proyecto
- **Fecha:** 2026-11-04
- **Relacionada:** spec 015 (adopción del índice existente); la 014 sigue reservada al aviso de versión.

## 1. Objetivo
Los índices de IA crecen y se quedan viejos (rutas que ya no existen, secciones con datos de hace meses, el mismo texto repetido y distinto en tres archivos). Hoy solo hay un tope de tamaño que avisa tarde. Se quiere una revisión **repetible** que detecte lo que sobra o está desfasado, proponga qué mover y, con el visto bueno de Darwin, lo deje limpio **sin perder información**.

## 2. Reparto del trabajo
El guardián no entiende textos; la IA sí, pero no debe actuar sola. Tres piezas:
1. **Guardián `revisar_indices.py` (mecánico, solo lectura).** Produce un informe corto. Detecta:
   - **Referencias rotas:** rutas, archivos y comandos citados en el índice que ya no existen en el proyecto.
   - **Deriva entre índices:** secciones que están en uno y no en otro, o con texto distinto (CLAUDE vs GEMINI vs AGENTS).
   - **Secciones pesadas:** las que pasan de un tamaño y su peso sobre el total.
   - **Fechas viejas:** secciones con fecha explícita de más de N días (por defecto 90).
   - **Contenido que ya vive en otro sitio:** párrafos casi idénticos a `.brain/constitution.md`, `objetivo.md` o fichas de `architecture/`.
2. **Skill `revisar-indices-de-ia` (criterio, con Darwin).** La IA lee el informe, comprueba cada punto contra el código real y clasifica cada sección: *vigente*, *desfasada* (con la diferencia concreta) o *dudosa*. Enseña la tabla en lenguaje llano y espera el visto bueno **antes de escribir**.
   **Doble pasada contra falsos positivos** (la skill nunca enseña un hallazgo que no haya pasado las dos):
   - *Pasada 1 — buscar:* se recorre el informe del guardián y cada hallazgo se verifica contra el proyecto real (¿el archivo existe con otro nombre o en otra ruta? ¿se crea al ejecutar? ¿se cita como ejemplo o como histórico? ¿lo menciona otro documento vigente?). Resultado: *confirmado*, *descartado* (con el motivo) o *dudoso*.
   - *Pasada 2 — refutar:* sobre lo *confirmado* y lo *dudoso*, otra lectura independiente hace de abogado del diablo: intenta demostrar que el hallazgo es falso. Idealmente la hace un subagente que recibe solo el hallazgo y el proyecto, sin el razonamiento de la pasada 1 (si la herramienta no lo permite, una segunda lectura desde cero antes de mirar la conclusión anterior). Solo sobreviven los que no se pueden refutar.
   - *Qué se enseña a Darwin:* los que sobreviven, más una línea con cuántos se descartaron y por qué; los *dudosos* que no se resuelven van en una lista aparte «no tocar sin que lo mires tú». Si las dos pasadas no coinciden, se trata como dudoso, nunca como seguro.
   - El guardián sirve también de segunda red: cada vez que descartan un hallazgo, se anota en `.brain/guardianes/revision_indices.json` (referencia + motivo) para no volver a proponerlo en la siguiente revisión.
3. **Aplicar lo aprobado.** Lo vigente que es referencia se mueve a su ficha (`architecture/`, `referencias.md`); lo desfasado se **mueve a `.brain/archive/indices/AAAA-MM-DD-NOMBRE.md`** con una línea en su índice; lo corregible se corrige. Los índices de las tres IA se dejan sincronizados. Nunca se borra (regla *mover, no borrar*).

## 3. Cuándo se lanza
- A mano: `python .brain/guardianes/revisar_indices.py` (informe) y la orden «revisa los índices».
- Aviso en el resumen de arranque cuando algún índice pasa el 80 % del tope, tiene referencias rotas, o hace más de 60 días de la última revisión (una línea, apagable en `guardianes.json`).
- Nunca actúa solo: el guardián avisa, la skill propone, Darwin aprueba.

## 4. En alcance
- [x] `revisar_indices.py` con sus 5 detecciones, solo librería estándar, ajustes en `guardianes.json` (`revision_indices_activa`, `revision_indices_dias`, `revision_indices_seccion_bytes`).
- [x] Skill nueva `revisar-indices-de-ia` con la **doble pasada** (buscar y refutar) y la lista de descartes (+ fila en `experiencia/indice.md`).
- [x] El guardián lee `revision_indices.json` y no repite lo ya descartado (con prueba).
- [x] Alta del guardián en el kit (`GUARDIANES` de `instalar.py`) y aviso en `arranque.py`.
- [x] Pruebas: referencias rotas detectadas; deriva entre índices; sección vieja por fecha; informe vacío si todo está sano; nada se escribe fuera del informe; el aviso de arranque se apaga con el ajuste.
- [x] Versión 1.14.0, `CAMBIOS.md`, manifiesto, manual, **ZIP de Mac regenerado** (`generar_zip_mac.py`).

## 5. Fuera de alcance
- Que la IA reescriba o resuma el contenido sin aprobación.
- Revisar otros documentos (README, manuales del proyecto): solo los índices de entrada de la IA.
- Juzgar si una decisión de arquitectura es buena; solo si el texto sigue coincidiendo con el código.
- Subir a GitHub o actualizar otros proyectos sin orden de Darwin.

## 6. Riesgos
- **Falsos positivos:** una ruta citada como ejemplo o que se crea al ejecutar parecerá rota. Por eso el informe solo propone y la IA lo pasa por la doble pasada (buscar y refutar) antes de enseñarlo. Coste: la segunda pasada gasta más tokens; solo se hace sobre lo confirmado o dudoso, no sobre lo ya descartado.
- **La doble pasada no es infalible:** dos lecturas de la misma IA pueden equivocarse igual. Por eso nada se aplica sin el visto bueno de Darwin y todo lo movido queda recuperable en el archivo.
- **Pérdida de información:** se evita moviendo siempre al archivo con índice, y comprobando en una prueba que lo movido se puede recuperar.
- **Probado solo en Windows**, y la prueba real será sobre el `CLAUDE.md` de Guild Control Forever (copia) tras la adopción de la spec 015.

## 7. Plan
1. Guardián con el informe y sus pruebas.
2. Skill y alta en el kit; aviso de arranque.
3. Probar en la copia de Guild Control Forever: informe, tabla de clasificación, mover lo aprobado.
4. Versión, manifiesto, ZIP de Mac, manual; pruebas completas.

## 8. Cierre
- [x] Spec aprobada por Darwin antes de programar
- [x] Pruebas en verde y probada en la copia de Guild Control Forever
- [x] ZIP de Mac regenerado
- [x] Línea añadida a `.brain/decisions.log`
