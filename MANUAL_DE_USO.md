# Manual de uso de Cerebro Vivo (para Darwin)

Guía práctica, sin jerga. Para el porqué de cada cosa está `.brain/biblioteca/CEREBRO_VIVO.md`; este manual responde a «¿qué hago yo y cuándo?». Versión del arnés al escribirlo: 1.3.1.

## 1. Qué es, en una frase
Un conjunto de carpetas, avisos automáticos y costumbres para que la IA **recuerde lo acordado entre chats** y no te haga repetirlo. La memoria vive en la carpeta `.brain/` de cada proyecto.

## 2. Qué sabemos y qué no (medido el 2026-11-01)
- **Demostrado:** al retomar un trabajo en un chat nuevo, con el arnés se respetó lo acordado 5 de 5 veces; sin él, 0 de 5.
- **Demostrado:** en tareas pequeñas gasta de un 7 % a un 16 % **más**. No ahorra ahí.
- **Demostrado (un solo proyecto, ~80 fichas):** tener índice no mejoró el acierto y salió ~19 % más caro; con el índice roto tampoco falló nadie.
- **Sin medir:** que ahorre a la larga en un proyecto real. Es una idea razonable, no un hecho.
- Úsalo donde hay **muchos chats seguidos** sobre lo mismo. En una tarea suelta no compensa.

## 3. Empezar un proyecto nuevo
1. Doble clic en `instalar_kit.bat` (abre una ventana), o en terminal:
```bash
python .brain/biblioteca/kit-arranque/instalar.py RUTA_DEL_PROYECTO --nombre MiProyecto --dueno Darwin --nivel completo
```
2. Abre un chat en la carpeta del proyecto. El arranque mostrará solo un resumen del estado.
3. Para el primer encargo, usa `/prompt-inicial` en el chat (se explica en la sección 3 bis).

## 3 bis. Empezar bien un chat: `/prompt-inicial` y las demás plantillas
Un encargo completo evita idas y vueltas. **`/prompt-inicial`** te ayuda a escribirlo: escribe `/prompt-inicial` en el chat. Viene incluida al instalar el arnés (carpeta `.claude/skills/prompt-inicial`), no hay que instalar nada más y no gasta IA extra.

Te pide **objetivo, cómo sabré que está bien, qué NO quiero, material, cómo trabajar** (spec con aprobación o rápido, paso a paso), **plazos, costes, idioma y qué debo probar yo**. Te avisa de lo que falta y espera tu visto bueno antes de actuar. Solo sirve para escribir encargos. Para saber cómo va el proyecto escribe **`/resumen`** (cuenta el estado en pocas viñetas, sin escribir nada); para ver una lista escribe **`/pendiente`** (te deja elegir: falta programar, esperando tu prueba, acciones tuyas o specs abiertas, o escribe `/pendiente programar`).

**Para Gemini o Codex:** pídele a Claude «la versión para Gemini/Codex» y deja la plantilla en blanco en `.brain/biblioteca/PLANTILLA_PROMPT_INICIAL.md`.

**Panel `/plantilla`:** formulario con botones para escribir el encargo e insertarlo en el chat. Es un plugin de Claude Code (`plantilla-prompt/`) que se instala una vez por equipo, no con el actualizador; cómo, en `plantilla-prompt/README.md`.

**Otras plantillas que usa el método (ya vienen con el arnés):**
| Plantilla | Para qué | Dónde |
|---|---|---|
| Traspaso | Pasar de un chat a otro sin perder nada | `.brain/biblioteca/PLANTILLA_TRASPASO.md` |
| Nota de chat auxiliar | Dejar lo que hizo un chat que recibió un encargo de otro | `.brain/biblioteca/PLANTILLA_NOTA_CHAT.md` |
| Spec | Plan corto que apruebas antes de programar | `.brain/specs/_template.md` |
| Ficha de decisión | Por qué se decidió algo (`D-NNN`) | `.brain/decisions/_template.md` (la crea el kit en cada proyecto) |
| Registro de pruebas | Qué te toca probar y cómo | `.brain/pruebas/_plantilla.md` |

## 3 ter. Proyecto que ya tenía su CLAUDE.md: `/adopta`, `/acorta`, `/trocea`
**Desde la 1.18.0 basta con `/adopta`: hace los pasos 1 a 3 seguidos y te pide el sí en cada tabla.** Los comandos sueltos (`/acorta`, `/trocea`) siguen sirviendo por separado. Para un proyecto empezado antes del método (con un CLAUDE.md gordo). Se instala el kit (no pisa nada: el original se guarda entero en `.brain/archive/adoptado/`), se reinicia Claude Code en esa carpeta y, en un chat nuevo, **en este orden**:

| Paso | Escribe | Qué hace | Tú |
|---|---|---|---|
| 1 | `/adopta` | Copia lo que había en el CLAUDE.md viejo a su sitio en `.brain/` (reglas, decisiones, objetivo; lo que no encaja va a `referencias.md`). No resume nada. | Apruebas la tabla del reparto |
| 2 | `/acorta` | Cambia las secciones gordas del CLAUDE.md, GEMINI.md y AGENTS.md por un enlace, hasta el tope de 5 KB. | Apruebas la tabla antes de escribir |
| 3 | `/trocea` | Divide los archivos de `.brain/` que pasen de 8 KB (típicamente `referencias.md`) en archivos **por tema con nombre** (`loot.md`, `roster.md`) en `.brain/architecture/`, con un índice. La copia íntegra queda en `.brain/archive/troceado/`. | Apruebas la tabla de cortes |
| 4 | `revisa los índices` | Comprueba referencias rotas, deriva y repetidos con doble pasada (skill `revisar-indices-de-ia`). | Apruebas lo que sobrevive |

Nada se borra: todo se copia o se mueve a archivo. El arranque avisa solo cuando un índice pasa del 80 % de su tope (4 KB) o un archivo de `.brain/` pasa del 80 % de su tope (6,5 KB). Lo nuevo (1.14.1 a 1.16.1) está probado con pruebas y en un proyecto real (Guild Control Forever: CLAUDE.md de 52 KB a 3,3 KB). Si un proyecto tiene un AGENTS.md ajeno al método, no lo añadas a `indices_entrada` y las pruebas no lo exigirán.

## 4. Un día normal de trabajo
- **Al abrir un chat:** la IA te resume en 4-5 viñetas dónde se quedó. Si no lo hace, pídeselo.
- **Mientras trabajas:** tareas pequeñas (hasta 2 archivos) van por el carril rápido. Cambios grandes o delicados (pagos, base de datos, licencias) piden una **spec** primero: un papel corto con objetivo, qué entra, qué no y cómo se prueba. Tú la apruebas antes de que se programe.
- **Al terminar una tarea:** la IA anota una línea en `.brain/decisions.log`. Si se le olvida, un aviso automático se lo recuerda. A mano:
```bash
python .brain/guardianes/cerrar.py --chat "Proyecto #N" "qué se hizo"
```
- **Cuando pruebas algo y funciona:** díselo en el chat; la IA lo pasa de `pendientes.md` a `hechos`.
- **Lo irreversible se pregunta:** subir a GitHub, borrar, gastar. No lo hace sin tu orden.

## 5. Cambiar de chat sin perder nada
- Un chat largo cuesta más y se vuelve torpe. Cuando te lo avise, o cuando lleves mucho rato, pide «prepara el traspaso y el chat nuevo».
- La IA escribe `.brain/traspaso.md` (qué pediste, qué se decidió, qué falta, qué NO hacer). El chat nuevo lo muestra solo al arrancar.
- Si un chat auxiliar recibe un encargo de otro, deja su nota en `.brain/notas-chats/`.

### Misma IA, chat nuevo: `traspaso-in`
| Momento | Qué escribes | Qué hace la IA |
|---|---|---|
| Antes de cerrar un chat largo | `/traspaso-in salgo` (en Codex, `$traspaso-in salgo`) | Mira git y las pruebas y escribe `.brain/traspaso.md` con lo último que pediste |
| En el chat nuevo | `/traspaso-in entro` (en Codex, `$traspaso-in entro`) | Lo lee, te lo cuenta en 4-5 viñetas, lo archiva y pregunta por dónde seguir |

Claude Code muestra el traspaso solo al abrir; en Codex y Gemini hay que escribir `entro`. Si no escribes `salgo` antes, el chat nuevo no tiene nada que leer.

### Cambiar de IA (Claude, Gemini, Codex): `traspaso-out`
Gemini y Codex no corren ganchos (ni resumen al abrir ni aviso al cerrar), así que el cambio se hace con una frase en cada lado. Solo una IA a la vez trabaja en el proyecto.

| Momento | Qué escribes | Qué hace la IA |
|---|---|---|
| Al irte de una IA | `/traspaso-out salgo` (en Codex, `$traspaso-out salgo`) | Mira git y las pruebas y escribe `.brain/traspaso.md` con quién lo escribe, quién sigue y la hora |
| Al llegar a la otra (chat nuevo) | `/traspaso-out entro` (en Codex, `$traspaso-out entro`) | Lee el traspaso, te lo cuenta en 4-5 viñetas, lo archiva y te pregunta por dónde seguir |
| Solo ver el estado, sin cambiar | `/resumen` (en Codex, `$resumen`) | Cuenta el estado sin escribir nada |
| Ver listas de lo que falta | `/pendiente` (en Codex, `$pendiente`) | Menú: programar, prueba, acciones tuyas, specs |

Si Gemini no reconoce la skill, pídele: «lee `GEMINI.md`, `.brain/traspaso.md` y `.brain/pendientes.md` y cuéntame el estado». Sin ganchos no hay forma de hacerlo automático: la frase es obligatoria.

## 6. Dónde está cada cosa
| Qué buscas | Dónde |
|---|---|
| Lo que falta por hacer | `.brain/pendientes.md` |
| Lo que ya se hizo y probaste | `.brain/archive/hechos-indice.md` (el detalle, en `hechos.md`) |
| Qué se hizo y cuándo | `.brain/decisions.log` |
| Por qué se decidió algo | `.brain/decisions/indice.md` y sus fichas `D-NNN` |
| Reglas que no se tocan | `.brain/constitution.md` |
| Planes aprobados | `.brain/specs/` |
| El método completo | `.brain/biblioteca/CEREBRO_VIVO.md` |

**Los índices (`decisions/indice.md`, `archive/hechos-indice.md`) son a demanda:** el arranque no los lee; solo se abren cuando hace falta buscar una ficha. En la prueba (spec 004, ~80 fichas) no mejoraron el acierto y costaron algo más, así que se mantienen pero sin cargarlos siempre. Los archivos de entrada (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`) se mantienen cortos y con enlaces al cerebro.

**Gemini y Codex:** `/prompt-inicial` y los ganchos de Claude Code (el resumen automático al abrir y el aviso al cerrar) no funcionan allí; el proyecto se adapta al método escrito en `GEMINI.md` / `AGENTS.md`. En Codex las skills se invocan con `$prompt-inicial` y deben estar en `.agents/skills/` (Codex no lee `.claude/skills/`). Abre siempre un chat nuevo: un chat ya abierto no recarga el archivo de entrada.

## 7. Traer mejoras a un proyecto que ya lo usa
**Lo fácil (1.17.0):** cuando al abrir un chat sale «Arnés: hay una versión nueva», escribe **`/actualizar`**. Te cuenta qué trae, te pide el sí y lo hace todo (copia de seguridad, claves nuevas, fichas de skills). Lo de abajo es la forma manual, por si algún proyecto no tiene `arnes_repo` anotado: la primera vez actualízalo desde aquí con `python actualizar.py RUTA` y se anota solo.

Primero **simular** (no escribe nada), luego actualizar:
```bash
python .brain/guardianes/actualizar_arnes.py --simular
python .brain/guardianes/actualizar_arnes.py
```
Guarda una copia antes, no pisa lo que cambiaste a mano y nunca toca tus pendientes, specs, decisiones ni registro. Un proyecto antiguo sin registro previo usa `--forzar-todo`, **solo** después de ver la lista con `--simular`.

**Desde cerebro-vivo, sobre otro proyecto** (hace lo mismo; útil si el proyecto aún no tiene `actualizar_arnes.py`):
```bash
python actualizar.py "RUTA_DEL_PROYECTO" --simular
python actualizar.py "RUTA_DEL_PROYECTO"
```

**Opciones del actualizador** (las dos formas las aceptan, salvo que se indique):
| Opción | Qué hace |
|---|---|
| `--simular` | Muestra qué cambiaría; no escribe nada. Úsala siempre primero |
| `--forzar RUTA` | Pisa ese archivo aunque lo hayas modificado a mano (con copia) |
| `--forzar-todo` | Pisa **todos** los modificados a mano (con copia). Haz commit antes y mira la lista con `--simular` |
| `--migrar-objetivo` | Solo dentro del proyecto. Para proyectos instalados antes de la 1.6.0: crea `.brain/architecture/objetivo.md`, lo enlaza en `CLAUDE.md`/`GEMINI.md`/`AGENTS.md` y añade la regla a la constitución. Solo añade; se puede repetir. Probar antes con `--simular` |
| `--dueno NOMBRE` | Registra el dueño si el proyecto no lo tiene |
| `--repo RUTA` | Repo del arnés a usar (si no, el de `arnes_repo` en `guardianes.json`) |
| `--sin-pruebas` | No corre las pruebas del método al terminar |

Las copias de seguridad quedan en `.brain/copias_arnes/`. Si el proyecto usa Codex (`AGENTS.md`), el actualizador también copia las skills a `.agents/skills/`.

## 8. Medir si te está ayudando
```bash
python .brain/guardianes/medir.py
```
Enseña por chat el coste, los mensajes tuyos y cuántas veces tuviste que corregir a la IA. Ideas para un proyecto real: apuntar la media **antes** de poner el arnés, ponerlo, y comparar 3-4 semanas después. Otras opciones: `--comparar CARPETA_CON CARPETA_SIN`, `--tarea TEXTO` (solo un tipo de tarea), `--desglose ID` (un chat mensaje a mensaje). Solo lee; no cambia nada.

## 9. Avisos y guardianes que verás
- **Arranque** (al abrir un chat): estado real de pendientes, commits sin subir, última línea del registro.
- **Cierre** (al acabar una respuesta): avisa si falta la línea del registro. Una sola vez.
- **Modo ligero:** en tareas pequeñas con pruebas en verde, la línea del registro se escribe sola.
- **Secretos:** `python .brain/guardianes/secretos.py` busca claves o datos personales; `--historial` revisa también lo ya guardado en git. Pásalo antes de subir nada a internet.

## 10. Reglas para ti
- No subas nada a GitHub sin pasar por `secretos.py` y sin decidirlo tú.
- Si un resultado «parece demasiado bueno», pide que lo pruebe y lo diga como no probado si no pudo.
- Tras cambiar cualquier archivo **de este repo**: subir `VERSION`, anotar `CAMBIOS.md`, `python generar_manifiesto.py` y `python -m unittest discover tests`.

## 11. Cuando algo no va
| Síntoma | Qué hacer |
|---|---|
| No sale el resumen al abrir el chat | Pídele a la IA que ejecute `python .brain/guardianes/arranque.py` |
| Te pide leer demasiado | Chat nuevo con traspaso; los chats largos son lo que más cuesta |
| Un aviso se repite o molesta | Díselo; los topes están en `.brain/guardianes/guardianes.json` |
| Dudas de si algo se rompió al actualizar | `python -m unittest discover tests` y las copias están en `.brain/copias_arnes/` |

## 12. Todos los comandos en una tabla
`RUTA` es la carpeta del proyecto. Los de `.brain/guardianes/` se lanzan dentro del proyecto; `actualizar.py` e `instalar.py`, desde cerebro-vivo.

| Para qué | Comando |
|---|---|
| Instalar en un proyecto nuevo (ventana) | doble clic en `instalar_kit.bat` |
| Instalar en un proyecto nuevo (terminal) | `python .brain/biblioteca/kit-arranque/instalar.py RUTA --nombre Nombre --dueno Darwin --nivel completo` (niveles: `ligero`, `medio`, `completo`; `--traduccion` añade es/en/pt) |
| Comprobar un proyecto ya instalado | `python .brain/biblioteca/kit-arranque/instalar.py RUTA --comprobar` |
| Ver qué traería una actualización | `python actualizar.py RUTA --simular` (o, dentro del proyecto, `python .brain/guardianes/actualizar_arnes.py --simular`) |
| Actualizar un proyecto (lo fácil) | escribe `/actualizar` cuando salga el aviso en el arranque |
| Actualizar un proyecto (a mano) | `python actualizar.py RUTA` (o `python .brain/guardianes/actualizar_arnes.py`) |
| Pisar archivos modificados a mano | `--forzar RUTA_ARCHIVO` (uno) o `--forzar-todo` (todos; commit antes) |
| Migrar el objetivo a un proyecto antiguo | `python .brain/guardianes/actualizar_arnes.py --migrar-objetivo --simular` y luego sin `--simular` |
| Otras opciones del actualizador | `--dueno NOMBRE`, `--repo RUTA`, `--sin-pruebas` |
| Resumen de arranque a mano (Gemini, Codex) | `python .brain/guardianes/arranque.py --manual` |
| Cerrar una tarea (línea en el registro) | `python .brain/guardianes/cerrar.py --chat "Proyecto #N" "qué se hizo"` (`--carril`, `--simular`) |
| Añadir fichas de decisiones sin fila al índice | `python .brain/guardianes/cerrar.py --indices` |
| Pasar un punto probado a hechos | `python .brain/guardianes/cerrar.py --hecho N` (`--conservar` si algo sigue pendiente) |
| Medir chats (tokens, coste) | `python .brain/guardianes/medir.py` (`--ultimos N`, `--desglose ID`, `--tarea TEXTO`, `--comparar RUTA_CON RUTA_SIN`) |
| Pruebas | `python -m unittest discover tests` |
| Regenerar el manifiesto del arnés (en cerebro-vivo, tras cambiar algo) | `python generar_manifiesto.py` |
| Repartir el CLAUDE.md viejo en la memoria | `/adopta` (skill `adoptar-indice-existente`) |
| Bajar los índices de IA al tope de 5 KB | `/acorta` |
| Dividir un archivo de `.brain/` gordo por temas | `/trocea` (ver cuáles: `python .brain/guardianes/archivos_gordos.py`) |
| Revisar los índices de IA (doble pasada) | «revisa los índices» (`python .brain/guardianes/revisar_indices.py` para el informe) |
| Skills en Claude | `/resumen`, `/pendiente`, `/prompt-inicial`, `/traspaso-in`, `/traspaso-out`, `/adopta`, `/acorta`, `/trocea` |
| Skills en Codex | `$resumen`, `$pendiente`, `$prompt-inicial`, `$traspaso-in`, `$traspaso-out`, `$adopta`, `$acorta`, `$trocea` (necesitan `.agents/skills/`) |
