# Spec 090: web de ejecución del cerebro (visor, proyectos, acciones y aprobaciones)

- **Estado:** **fase 1 construida (v1.61.0), con revisión aparte y prueba de uso real; spec aprobada por Darwin el 2026-11-20 (ver 12.4); fase 2 construida (v1.63.0), falta su revisión aparte.** Las 3 preguntas de la sección 8 quedan respondidas con las recomendaciones.
- **Fecha:** 2026-11-18
- **Se apoya en:** `buscar.py`, `medir.py`, `actualizar_arnes.py`, `hermanos.py`, `revisar_contenido.py`, `guardar_traspaso.py`, spec 035 (fábrica) y la regla de «mover, no borrar».
- **Origen:** Darwin pidió (2026-11-18) una web para manejar el cerebro con interfaz, local y de un solo usuario. Funciones elegidas: ver y buscar, editar y aprobar, grafo de relaciones, medir uso y gestionar proyectos.

## 1. Objetivo
Una web que se abre **en el PC de Darwin** y le deja mirar y gobernar el cerebro (`.brain/`) y sus proyectos **sin usar la terminal**, sin instalar nada extra y sin que ningún dato salga de su máquina.

## 2. Qué NO es (límites)
- **No es un servidor público** ni de varias personas. Escucha solo en `127.0.0.1`. Usuarios, roles y cuentas quedan para otra spec, solo si Darwin lo pide.
- **(Cambia en la sección 12: la web también EJECUTA, solo con acciones de una lista cerrada.)**
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
- [x] Spec aprobada por Darwin (2026-11-20; ver 12.4)
- [x] Fase 1 construida y probada (v1.61.0; revisión aparte y prueba de uso real en `.brain/fabrica/evidencia/090-fase1-*.md`)
- [x] Fase 2 construida y probada con pruebas automáticas (v1.63.0, 2026-11-20). Revisión aparte hecha (apto con reparos; corregido lo grave). **Falta:** prueba de uso real por otra IA; permisos por ruta (13.5); no se ha probado en un proyecto que no sea el repo del arnés ni con clics en el navegador
- [x] Fase 3 **cerrada por Darwin el 2026-11-25** (v1.65.3): actualizar e instalar de verdad, tareas del método con parar; tres auditorías externas (Codex) corregidas; prueba de uso real por otro chat (`.brain/fabrica/evidencia/090-fase3-uso-real-2.md`, verde). Cerrada sin prueba por una IA de otra familia y con los límites conocidos (instante entre revalidar el guardián y reanudar; tareas y simulaciones no ligadas a la instancia)
- [ ] Línea añadida a `.brain/decisions.log`

## 11. Resultados de la fase 1 (2026-11-18)
- **Revisión aparte** (subagente solo lectura): sin hallazgos graves. Dos arreglos hechos: el buscador ya no muestra archivos que salgan de `.brain/` por un enlace simbólico, y con archivos grandes el Inicio enseña el final en vez de quedar vacío. Sin arreglar por baja gravedad: tiempo de espera de conexión y varios «medir» a la vez.
- **Prueba de uso real** (otra IA, en el navegador integrado): Inicio, Decisiones, Lecciones, Specs, búsqueda y Medir uso funcionan; sin clave da 403, ruta fuera da 404, POST da 405; sin scroll horizontal en móvil. Feo: los `.md` salen como texto crudo y las tablas de Medir uso se parten en pantalla estrecha. **No probado:** abrir un resultado de búsqueda, modo claro, Biblioteca y Respuestas a fondo, y la prueba de enlace simbólico en Windows (se salta sin permiso).

## 12. Cambio de alcance: web de ejecución (Darwin, 2026-11-18)
Darwin probó la fase 1 y dijo que es «más una página de búsqueda tipo Obsidian que una de ejecución». **Se queda el visor con buscador** y se añade lo que hace falta para **ejecutar**. Vocabulario de Darwin: **info** = la página pública de GitHub; **ejecución** = esta web local.

### 12.1 Qué se añade
1. **Proyectos:** lista de proyectos registrados (nombre, ruta, versión del arnés, atraso, avisos). **Añadir un proyecto** eligiendo su carpeta; se guarda en un archivo de la propia web (`.brain/web_proyectos.json`, no se reparte), nunca fuera de lo que Darwin añade.
2. **Instalador sencillo:** desde la web, instalar el arnés en un proyecto nuevo o adoptar uno existente, envolviendo `kit-arranque/instalar.py` (ya existente); primero **simula** y enseña qué crearía, y solo con confirmación lo hace.
3. **Actualizar proyectos:** botón «simular» y botón «actualizar» por proyecto (o todos), sobre `actualizar_arnes.py`; la real pide confirmación y enseña el resultado.
4. **Tareas del método:** botones para correr pruebas, generar el manifiesto, cerrar tarea (`cerrar.py`), lanzar el auditor y escribir el traspaso.
5. **Fábrica y chats:** ver el estado de la fábrica de cada proyecto (`estado/`, gasto, frenos, encargos) y lanzar los comandos de `fabrica.py`. **Límite honesto:** abrir o seguir chats de Claude Code es cosa de la app de escritorio; la web solo puede mostrar el estado y dar el enlace o el comando; no se promete abrir chats desde aquí hasta comprobarlo.
6. **Aprobar cambios:** la bandeja de propuestas de la sección 4, ahora con aprobar todas, una a una o editar.

### 12.2 Cómo se ejecuta sin abrir una puerta peligrosa (no se negocia)
- **Lista cerrada de acciones:** cada botón corresponde a un comando fijo con argumentos validados; **nunca** una línea de texto que llegue a un shell. Un proyecto solo puede ser uno de los registrados.
- Las acciones usan **POST** con la clave del arranque, el nombre de servidor comprobado y un **token por acción**; un GET nunca ejecuta nada.
- **Lo que cambia algo pide confirmación en pantalla**, con lo que va a hacer escrito en llano; lo que solo mira (simular, medir) no.
- **Nunca desde la web:** subir a GitHub o a la página, `push`, borrar proyectos o historial, tocar secretos o configuración personal, forzar nada. Esas siguen siendo orden de Darwin.
- Cada ejecución queda **registrada** (qué, dónde, cuándo, resultado) en el archivo de actividad de la web, y las acciones largas corren en segundo plano con su salida visible y un botón de parar.
- Una acción por proyecto a la vez; un proyecto con una acción en marcha rechaza la siguiente.
- Antes de **actualizar de verdad**, se enseña la simulación; y el arnés ya no pisa lo modificado a mano.

### 12.3 Fases nuevas (sustituyen a las de la sección 6)
1. **Fase 1 (hecha, v1.61.0):** visor y buscador, solo lectura.
2. **Fase 2:** proyectos (registro, añadir, ver versión y atraso) y **simulaciones** (instalar y actualizar en simulado). Sigue sin cambiar nada.
3. **Fase 3:** acciones que cambian cosas: instalador real, actualizar real, tareas del método. Con la sección 12.2 completa, revisión aparte, auditor externo y prueba de uso real **sobre una copia de un proyecto**, no sobre uno de verdad.
4. **Fase 4:** aprobar cambios (bandeja de propuestas).
5. **Fase 5:** fábrica y chats (solo ver estado al principio), más una **ventana de informes de la fábrica**: cuando la fábrica entrega el informe de lo que hizo, se ve ahí, organizado (por encargo, qué se hizo, qué se revisó, gasto y resultado), sin abrir archivos. Solo lectura. (Añadido por Darwin, 2026-11-20.)
6. **Después:** grafo y pantalla de salud (sección 3 bis).

### 12.4 Respuestas de Darwin (2026-11-18)
- **Proyectos:** se podrán registrar **todos los proyectos actuales**; cada uno con **perfil propio**, presentado **como pestañas** (pendientes, versión, simulaciones, permisos y colaboradores de ese proyecto en su pestaña). Para la prueba de uso real de la fase 3 se sigue usando una copia de uno.
- **Orden de fases (APROBADO por Darwin, 2026-11-20):** proyectos y simulaciones primero; lo que cambia cosas después.
- **Fábrica y chats (APROBADO por Darwin, 2026-11-20):** en la primera versión solo ver estado; lanzar comandos y abrir chats desde la web, más adelante y solo si la app lo permite.
- **Ventana de informes de la fábrica (pedido de Darwin, 2026-11-20):** el informe que entrega la fábrica se ve organizado en una ventana propia de la web (fase 5).
- **Spec aprobada por Darwin el 2026-11-20** («de resto lo apruebo»), con las recomendaciones de la sección 8: web primero solo en cerebro-vivo viendo todos los proyectos; las IAs también pueden proponer cambios; fase 1 ya aprobada.

### 12.5 Riesgos honestos
- Es la parte más delicada del arnés hasta ahora: una página local que ejecuta comandos sobre varios proyectos. De ahí la lista cerrada, las confirmaciones y la prueba sobre una copia.
- Instalar y actualizar ya existen y están probados por separado; lo nuevo es que ahora se disparan desde una página, y eso hay que probarlo entero.
- **Riesgo aceptado de las tareas (auditoría externa, 2026-11-20):** correr las pruebas, el auditor o «cerrar» de un proyecto registrado **ejecuta código de ese proyecto con los permisos y el entorno de quien lanzó la web**. «Nunca subir ni tocar secretos» es una regla de lo que hace la web por sí misma, no una garantía técnica sobre ese código: un proyecto malicioso podría leer secretos o hacer `push`. Por eso solo se registran proyectos propios o de confianza y la pantalla de confirmación lo dice. Aislarlo de verdad (usuario o contenedor sin permisos) queda para la fase de internet.
- **Cerrado tras la auditoría externa (v1.65.1):** el guardián debe colgar de `<proyecto>/.brain/guardianes` sin enlaces que salgan del proyecto (se comprueba al validar y otra vez justo antes de lanzar); los procesos hijos de una tarea mueren con ella (Job Object en Windows, grupo de procesos en el resto), también al acabar el padre, al parar y al pasar el límite; las simulaciones ocupan la carpeta como cualquier otra acción; el `Origin` de un POST debe ser exactamente esta web (esquema, host y puerto; sin cabecera sigue exigiéndose clave y token). Hueco conocido: un hijo creado en los microsegundos antes de entrar en el grupo en Windows (cerrado en v1.65.2: el proceso nace suspendido).
- **Tercera auditoría (v1.65.3, apto con reparos):** una tarea invalida las simulaciones de su carpeta; sin poder anotar el inicio no se ejecuta nada; el guardián se revalida con el proceso ya creado y parado. **Límites conocidos, no cerrados:** (a) entre esa última comprobación y la reanudación hay un instante en que alguien con acceso simultáneo al proyecto podría cambiar el guardián por un enlace; cerrarlo del todo exigiría ejecutar desde una copia verificada, y se acepta porque exige modificar el proyecto a la vez que se lanza la tarea; (b) tareas y simulaciones no están ligadas a la instancia o raíz del arnés, lo que solo importa con varias webs a la vez en un mismo proceso.

## 13. Local primero, preparado para internet, con roles como en Git (Darwin, 2026-11-18)
**Decisión de Darwin:** todo se hace **primero en local** y se deja **listo para internet**. Subirlo a internet **no** entra en esta spec: sería una spec aparte con revisión de seguridad.

### 13.1 Roles (como en Git)
| Rol | Qué puede |
|---|---|
| **Solo lectura** | Ver y buscar. Nada más. |
| **Colaborador** | Lo anterior, más **proponer cambios** (desde la web o desde su IA por MCP). |
| **Dueño** | Todo: aprobar o rechazar propuestas, **ejecutar acciones** (instalar, actualizar, tareas, fábrica), añadir proyectos y gestionar usuarios y roles. |
- **Local hoy:** un solo usuario, que es **dueño** automáticamente. Los roles ya existen en el diseño y se comprueban, pero no hay pantalla de inicio de sesión.
- **Roles por proyecto** (un «Brain» por proyecto): una persona puede ser dueña de uno y solo lectura de otro.
- **Las IAs conectadas** (sección 14) llevan su propio rol: una IA es un usuario más, con una clave propia que puede ser solo lectura o colaboradora. **Ninguna IA es dueña.**

### 13.2 Reglas de diseño para que quede listo (valen desde la fase 2)
1. **Capa de reglas aparte de la pantalla:** buscar, proponer, aprobar y ejecutar viven en una capa que expone una API; la web es solo un cliente. La misma capa servirá al MCP y a internet.
2. **Cada acción lleva «quién» y «sobre qué proyecto»,** y la capa comprueba el permiso antes de hacerla. Una acción sin permiso se rechaza y se registra.
3. **Almacenamiento detrás de una pieza intercambiable:** hoy archivos de `.brain/`; mañana, si hace falta, una base de datos, sin tocar las reglas ni la pantalla.
4. **Un Brain por proyecto,** con sus usuarios y roles propios.
5. **Registro de actividad con autor** (ya previsto en 12.2).
6. **Secretos fuera del repo** y claves de las IAs guardadas con huella, nunca en claro.
7. **Las acciones que ejecutan comandos** son de la capa local y solo del dueño; en una versión de internet serían un **agente local** que el dueño instala, nunca ejecución directa del servidor en tu PC.

### 13.5 Permisos que reparte el dueño (Darwin, 2026-11-18)
«Un colaborador solo podrá hacer lo que el dueño deje»: los roles de 13.1 son solo el punto de partida; el dueño **recorta o amplía** lo que puede cada colaborador (persona o IA), por carpeta, archivo y acción.
- **Empieza sin nada:** un colaborador nuevo no puede hacer nada hasta que el dueño le dé permisos (negar por defecto). Solo lectura puede traer ya el permiso de ver.
- **Reglas por usuario y proyecto**, guardadas en un archivo de la web (`.brain/web_permisos.json`, no se reparte ni se sube). Cada regla: **ruta** (archivo o carpeta, con comodines, por ejemplo `.brain/lecciones/**`), **permiso** y, opcional, **caducidad**.
- **Permisos por ruta:** `ver` · `proponer` (el cambio espera al dueño) · `editar` (se aplica sin esperar, solo si el dueño lo concede). Un permiso no incluye al otro: se dan por separado.
- **Permisos por acción** (lista cerrada de 12.2): cada acción (simular, actualizar, correr pruebas, cerrar tarea…) se concede o no, por proyecto.
- **Gana la regla más específica;** si empatan, gana la que niega. Todo lo que no está permitido está denegado.
- **Intocable aunque el dueño quiera delegarlo:** guardianes, `manifiesto.json`, `VERSION`, ajustes, secretos y el propio archivo de permisos. Solo el dueño y solo por la vía normal. Subir a GitHub sigue siendo orden de Darwin, para todos.
- **Plantillas rápidas** para no escribir reglas a mano (por ejemplo «solo lecciones y notas»), que el dueño puede ajustar.
- **Cada petición se comprueba en la capa de reglas** (13.2), nunca solo en la pantalla: ocultar un botón no cuenta como permiso. Los intentos denegados se registran con quién, qué y dónde.
- **Se prueba con una matriz** (usuario × ruta × permiso), incluidos los intentos de salirse con `..`, enlaces y nombres parecidos, y que una IA no pueda subirse el rol.
- **Pregunta 13.4-1 queda resuelta por este sistema:** aprobar es del dueño salvo que **él** lo conceda por ruta.

### 13.3 Qué NO viene en local y queda para la spec de internet
HTTPS y dominio, cuentas con contraseña y recuperación, invitaciones, base de datos real, copias de seguridad, límites de uso, privacidad de los datos de otros y mantenimiento del servidor.

### 13.4 Respuestas de Darwin (2026-11-18)
1. **Aprobar** es del dueño, salvo que él lo conceda por ruta (13.5).
2. **No hay cuarto rol «curador»:** Darwin no recuerda haberlo pedido (probable error de palabra por «colaborador»). Los roles son tres: dueño, colaborador y solo lectura.

## 14. IAs conectadas por MCP (pendiente de fase)
Servidor MCP local sobre la capa de reglas (sección 13.2), con herramientas de buscar, leer, ver pendientes y **proponer cambio**; cada IA con su clave y su rol. Las propuestas llegan a la bandeja de la fase 4. Va **después de la fase 4**. Límite: una IA sin ganchos propios (como los de Claude Code) no recibe los avisos automáticos; solo las herramientas.

## 15. Revisión exhaustiva de la fábrica (orden de Darwin, 2026-11-18)
**Motivo (palabras de Darwin):** la fábrica «no me convence, parece que en vez de agilizar el trabajo lo hace más tedioso y caro». Es una revisión **antes** de seguir ampliándola (la spec 089 sigue sin aprobar); no se hace dentro de la web.
- **Alcance:** specs 035, 040, 050, 088 y 089, la skill `fabrica`, `directora-de-fabrica`, los revisores, `fabrica.py` y los kits.
- **Medir con datos reales, no con impresiones:** por cada encargo ya hecho (`medir.py --fabrica`): tiempo de principio a fin, gasto por IA, número de vueltas de revisión, pasos que tuvo que hacer Darwin y cuántos hallazgos de los revisores eran reales frente a ruido.
- **Comparar con trabajar sin fábrica:** el mismo tipo de encargo hecho directamente por una sola IA; ¿cuánto tiempo y gasto se ahorra o se pierde?
- **Buscar:** pasos que no aportan, revisiones duplicadas, papeleo que nadie lee, ejecutoras que cuestan más de lo que valen, y encargos pequeños que no deberían pasar por la fábrica.
- **Resultado esperado:** informe en llano con números y una decisión por cada pieza: **quitar, simplificar, o dejar solo para encargos grandes**; un umbral claro de «esto no necesita fábrica». Sin tocar nada hasta que Darwin elija.
- **Mientras tanto:** no ampliar la fábrica (spec 089 en pausa) y no usarla para encargos pequeños.
- **Lo hace:** un chat propio, con independencia de la web (fase 5 «fábrica y chats» queda condicionada a su resultado).

### Orden final de fases
1 visor (hecha) · 2 proyectos y simulaciones, con la capa de reglas y los roles ya dentro · 3 acciones que cambian cosas · 4 aprobar cambios · 5 fábrica y chats · 6 IAs por MCP · después grafo y pantalla de salud.
