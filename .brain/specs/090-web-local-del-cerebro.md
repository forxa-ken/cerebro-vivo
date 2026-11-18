# Spec 090: web local del cerebro (ver, buscar, aprobar, medir y gestionar proyectos)

- **Estado:** **fase 1 construida (v1.61.0), con revisión aparte y prueba de uso real; fases 2 y 3 en borrador.** Darwin aceptó empezar solo por la fase 1 (2026-11-18); las 3 preguntas de la sección 8 siguen abiertas para las fases 2 y 3.
- **Fecha:** 2026-11-18
- **Se apoya en:** `buscar.py`, `medir.py`, `actualizar_arnes.py`, `hermanos.py`, `revisar_contenido.py`, `guardar_traspaso.py`, spec 035 (fábrica) y la regla de «mover, no borrar».
- **Origen:** Darwin pidió (2026-11-18) una web para manejar el cerebro con interfaz, local y de un solo usuario. Funciones elegidas: ver y buscar, editar y aprobar, grafo de relaciones, medir uso y gestionar proyectos.

## 1. Objetivo
Una web que se abre **en el PC de Darwin** y le deja mirar y gobernar el cerebro (`.brain/`) y sus proyectos **sin usar la terminal**, sin instalar nada extra y sin que ningún dato salga de su máquina.

## 2. Qué NO es (límites)
- **No es un servidor público** ni de varias personas. Escucha solo en `127.0.0.1`. Usuarios, roles y cuentas quedan para otra spec, solo si Darwin lo pide.
- **No sustituye a los guardianes:** todo lo que cambia el cerebro pasa por los mismos scripts y reglas de siempre (el registro, «mover no borrar», el manifiesto).
- **No sube a GitHub ni a la página** nunca desde la web.

## 3. Pantallas (de menor a mayor riesgo)
1. **Inicio:** estado real (lo mismo que el arranque): pendientes, commits sin subir, última línea del registro, avisos.
2. **Ver y buscar:** pendientes, registro, decisiones, lecciones, specs, biblioteca. Buscador sobre `buscar.py`. **Solo lectura.**
3. **Grafo de relaciones:** mapa de cómo se enlazan decisiones, specs, lecciones y pendientes (se construye leyendo las referencias que ya existen: «spec 088», «D-051», enlaces). Pulsar un nodo abre el documento.
4. **Medir uso:** muestra lo que ya calculan `medir.py` (skills, guardianes, fábrica): usos, gasto, tiempos. **Solo lectura**; no escribe en ningún sitio.
5. **Proyectos:** lista de proyectos que usan el arnés (rutas que Darwin añade), con su versión del arnés, si van atrasados y si tienen avisos. Botón de **simular actualización** (`--simular`). La actualización real exige confirmación explícita en pantalla.
6. **Editar y aprobar:** ver el siguiente apartado.

## 3 bis. Ideas para las fases 2 y 3 (estudio previo, 2026-11-18)
- **Grafo por comunidades:** agrupar los nodos por tema (lecciones de heredocs, de fábrica…), no un montón plano; pulsar un grupo lo abre.
- **Bandeja de propuestas:** las propuestas llegan agrupadas por tarea (por ejemplo «13 páginas de una investigación»), con **aprobar todas**, aprobar una a una o **editar antes de aprobar**. Debe poder apagarse para las que ya se aprueban solas.
- **Pantalla de salud:** páginas huérfanas, enlaces rotos, páginas demasiado largas, contradicciones posibles y propuestas sin resolver. Ya existe la lógica en `revisar_contenido.py`; la web solo la muestra.
- **Decisiones:** vista aparte con la ficha y los archivos que dependen de ella.
- **Lo que sí se aprende de la fase 1:** el índice como puerta de entrada y la búsqueda por palabras son lo que más sirve; el buscador semántico con vectores no hace falta a este tamaño.

## 4. Editar y aprobar (la parte delicada)
- La web **no edita archivos directamente**. Cada cambio se guarda primero como **propuesta** (qué archivo, texto actual, texto nuevo, quién lo propone: Darwin o una IA).
- Darwin ve la diferencia y pulsa **aprobar** o **rechazar**. Solo al aprobar se escribe el archivo.
- Antes de escribir: copia en `.brain/archive/` (mover, no borrar), y línea en `decisions.log`.
- **Solo se puede tocar** `.brain/` del propio proyecto elegido (pendientes, decisiones, lecciones, notas). **Nunca** código, guardianes, `manifiesto.json`, `VERSION` ni configuración: esos cambios siguen por la vía normal.
- Rutas validadas (sin `..`, sin salir de `.brain/`), tamaño máximo por archivo, y los pendientes respetan su tope de bytes.

## 5. Cómo se construye
- **Cero dependencias** (skill `cero-dependencias`): servidor con la librería estándar de Python (`http.server`), una sola página con HTML, CSS y JavaScript propios, sin descargar nada de internet. Se arranca con `python .brain/guardianes/web.py` y abre el navegador.
- Solo escucha en `127.0.0.1`, puerto configurable; con una clave aleatoria por arranque en la dirección para que otra página abierta en el navegador no pueda mandarle órdenes.
- Es **un guardián/herramienta más** del arnés: llega a los proyectos por `actualizar_arnes.py`, en español e inglés (textos en `textos.py`, prueba de paridad), con su entrada en el manifiesto.
- Pregunta abierta de reparto: ¿va en cada proyecto (ve su propio cerebro) o solo en cerebro-vivo (ve todos)? Ver pregunta 1 de la sección 8.

## 6. Fases
1. **Fase 1, solo lectura:** inicio, ver y buscar, medir uso. Sin ningún riesgo de escribir.
2. **Fase 2:** grafo y proyectos (con `--simular`).
3. **Fase 3:** editar y aprobar, y la actualización real de proyectos. Con revisión aparte y prueba de uso real, por ser lo que escribe.

Cada fase se entrega y se prueba antes de empezar la siguiente.

## 7. Cómo se prueba
- Pruebas automáticas: rutas fuera de `.brain/` rechazadas, propuesta que no escribe hasta aprobar, copia antes de escribir, solo escucha en 127.0.0.1, la clave por arranque, paridad es/en.
- Prueba de uso real con una IA distinta de la que construyó: abrir la web, buscar, aprobar un cambio de prueba en una copia del proyecto y comprobar registro y copia de archivo.
- Lo no probado se dice como no probado.

## 8. Preguntas para Darwin (antes de aprobar)
1. ¿La web va **en cada proyecto** (cada uno ve su cerebro, y llega por `actualizar_arnes.py`) o **solo aquí** (en cerebro-vivo, viendo todos los proyectos)? Recomendado: aquí primero, y se reparte después si te sirve.
2. ¿«Editar y aprobar» incluye **cambios que propone una IA** desde la terminal (la web solo los aprueba), o solo lo que tú escribes en la web? Recomendado: ambos, con la misma bandeja de propuestas.
3. ¿Aprobada la **fase 1 sola** para empezar (solo lectura)? Recomendado: sí.

## 9. Riesgos honestos
- Una web que escribe archivos es la parte más expuesta: por eso va en la fase 3, con propuestas y no con edición directa.
- Una página local sin clave podría recibir órdenes de otra pestaña del navegador; de ahí la clave por arranque.
- El grafo depende de que las referencias estén escritas con un formato constante; lo que no siga el formato no aparecerá.

## 10. Cierre
- [ ] Spec aprobada por Darwin (respuestas a la sección 8)
- [x] Fase 1 construida y probada (v1.61.0; revisión aparte y prueba de uso real en `.brain/fabrica/evidencia/090-fase1-*.md`)
- [ ] Fase 2
- [ ] Fase 3
- [ ] Línea añadida a `.brain/decisions.log`

## 11. Resultados de la fase 1 (2026-11-18)
- **Revisión aparte** (subagente solo lectura): sin hallazgos graves. Dos arreglos hechos: el buscador ya no muestra archivos que salgan de `.brain/` por un enlace simbólico, y con archivos grandes el Inicio enseña el final en vez de quedar vacío. Sin arreglar por baja gravedad: tiempo de espera de conexión y varios «medir» a la vez.
- **Prueba de uso real** (otra IA, en el navegador integrado): Inicio, Decisiones, Lecciones, Specs, búsqueda y Medir uso funcionan; sin clave da 403, ruta fuera da 404, POST da 405; sin scroll horizontal en móvil. Feo: los `.md` salen como texto crudo y las tablas de Medir uso se parten en pantalla estrecha. **No probado:** abrir un resultado de búsqueda, modo claro, Biblioteca y Respuestas a fondo, y la prueba de enlace simbólico en Windows (se salta sin permiso).
