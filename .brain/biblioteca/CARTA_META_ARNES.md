# Carta del Meta-Arnés «Cerebro Vivo»

> **Qué es este documento:** la carta maestra con la que Darwin arma el *arnés de trabajo con IA* de **todos** sus proyectos. Un «arnés» es el conjunto de archivos, reglas y vigilantes automáticos que rodean a la IA para que trabaje con continuidad, poco gasto y bajo control del dueño. «Meta-arnés» = el arnés que sirve para **crear el arnés de cada proyecto nuevo**.
> **Estado:** documento vivo, versión 0.22 (2026-11-01), extraído de LoboHook (#1 a #72). Se completa a medida que se aprende. Cada hecho aquí fue vivido o comprobado en LoboHook; lo no comprobado va marcado **(sin verificar)**.
> **Relación con otros archivos:** `CEREBRO_VIVO.md` es el manual operativo (el «cómo»); esta carta es el mapa completo y el «por qué» (principios, piezas, kit de arranque, lecciones, huecos). Si se contradicen, manda la carta y se corrige el manual.

---

## 0. Cómo leer esta carta
| Si quieres… | Ve a |
| :--- | :--- |
| Entender la idea | §1 y §2 |
| Montar un proyecto nuevo hoy | §14 (kit de arranque) y §15 (qué nivel elegir) |
| Saber qué vigila automáticamente | §9 |
| Evitar errores ya cometidos | §16 |
| Ver qué falta por resolver del método | §18 y §19 |

---

## 1. Propósito y promesa
**Problema:** la IA no recuerda entre chats, el contexto cuesta dinero en cada mensaje, y el dueño no técnico no puede auditar el código.
**Promesa del arnés:**
1. Retomar un proyecto tras días, o con otra IA, **sin repetir explicaciones**.
2. **Leer poco** al empezar y buscar el detalle solo cuando hace falta.
3. Que el dueño **vea el estado real** (qué existe, qué se probó, qué falta) sin leer código.
4. Que **nada irreversible** (subir, borrar, gastar, tocar datos reales) ocurra sin su orden.
5. Que el método **se cumpla solo** donde se pueda, y no dependa de la buena memoria de la IA.

## 2. Principios (las leyes del arnés)
1. **La verdad está en los archivos y el código, no en la conversación.** Lo que solo se dijo en el chat, se perdió.
2. **Índice primero, detalle después.** Se lee un índice corto; el detalle se abre solo si toca.
3. **Cada cosa en su sitio:** reglas, estado, historia, decisiones, especificaciones y conocimiento técnico van en archivos distintos.
4. **Cerrar es parte de trabajar.** Tarea sin memoria actualizada = tarea sin terminar.
5. **«Implementada» no es «terminada».** Terminada = el dueño la probó y confirmó.
6. **Lo hecho sale de la vista;** lo pendiente se mantiene corto.
7. **El porqué se guarda.** Una decisión sin su razón se vuelve a discutir y a pagar.
8. **Lo que se puede vigilar con una máquina, no se deja a la disciplina.** Primero regla escrita, luego guardián automático.
9. **Alcance estricto.** La IA toca solo lo que pide la tarea.
10. **Lo irreversible se pregunta.** Sin excepciones por «comodidad».
11. **Honestidad ante todo:** lo no probado se dice como no probado; un fallo se reporta con su salida.
12. **Hablar al nivel del dueño.** Lenguaje llano, sin jerga; el detalle técnico vive en los archivos.
13. **Medir antes de afirmar.** Los ahorros se estiman o se miden; no se prometen.
14. **Cero dependencias cuando se pueda** (también en el propio arnés: solo Python estándar).

## 3. Anatomía: las 7 capas
| Capa | Qué contiene | Dónde (LoboHook) |
| :--- | :--- | :--- |
| 0. **Dueño** | Decide, aprueba specs, prueba, ordena subir | Darwin |
| 1. **Índices de entrada** | Qué leer y dónde está cada cosa | `CLAUDE.md`, `GEMINI.md`, `AGENTS.md` (GPT Codex), `.brain/README.md` |
| 2. **Reglas** | Lo innegociable | `.brain/constitution.md` |
| 3. **Estado** | Qué falta / qué se hizo / qué se decidió | `pendientes.md`, `decisions.log`, `archive/hechos*.md`, `decisions/` |
| 4. **Conocimiento** | Cómo funciona cada área y qué se aprobó construir | `architecture/`, `specs/`, `FUNCIONALIDADES.md`, guías y manuales |
| 5. **Guardianes** | Vigilantes automáticos | `.brain/guardianes/`, `tests/test_cerebro_indices.py`, hook `Stop` |
| 6. **Biblioteca** | Material reutilizable entre proyectos | `.brain/biblioteca/` (esta carta, el manual, directorio de herramientas) |
| (fuera del repo) | **Memoria personal del asistente**: preferencias del dueño y correcciones recibidas | `~/.claude/projects/<proyecto>/memory/` |

## 4. Estructura de archivos y topes
```
CLAUDE.md / GEMINI.md / AGENTS.md   índice de entrada por IA (≤ 5 KB cada uno, vigilado por test; mismo contenido; AGENTS.md lo lee GPT Codex)
FUNCIONALIDADES.md           mapa de lo que hace el producto (fiel al código)
.brain/
  README.md                  mapa de la carpeta
  referencias.md             mapa de documentos y hoja de ruta (se abre solo si toca; fuera de los índices para no gastar tokens)
  constitution.md            reglas innegociables
  pendientes.md              SOLO lo que falta (tope 8 KB)
  decisions.log              una línea por tarea cerrada (solo se añade al final)
  decisions/indice.md + D-NNN-*.md   decisiones con su porqué (≤ 15 líneas c/u)
  specs/_template.md + NNN-*.md      especificaciones aprobadas antes de programar
  architecture/<área>.md     una ficha por área técnica
  archive/                   hechos.md + hechos-indice.md + historial antiguo + índice
  guardianes/                cierre.py · arranque.py · cerrar.py · poda.py · medir.py · analisis.py · analisis_base.json · guardianes.json
  biblioteca/                CARTA_META_ARNES.md · CEREBRO_VIVO.md · herramientas.md
.claude/settings.json        hook Stop que activa el guardián de cierre
tests/test_cerebro_indices.py   test de coherencia de los índices
```
**Escala real en LoboHook:** unas 50 specs vivas (+30 ya cerradas en `specs/archivo/`), 72 fichas de decisión, 992 tests, `decisions.log` de ~54 KB, unos 72 chats de trabajo en 5 días (a 2026-11-01).

## 5. Lectura de arranque y presupuesto de tokens
- **Se lee siempre:** índice de entrada + `constitution.md` + `pendientes.md` + **una** ficha de `architecture/` (la del área).
- **Se consulta solo si toca:** `decisions/indice.md` (antes de cambiar algo ya decidido), `archive/hechos-indice.md` (¿ya se hizo X?), la spec de la tarea.
- **Nunca se abre completo:** `decisions.log`, `archive/hechos.md`, historial antiguo.
- Estimación: ~10.000 tokens de lectura propia frente a ~150.000 si hubiera que leerlo todo.
- **Medición real (guardián 3, 25 chats):** el arranque cuesta ~69.000 tokens en *todos* los chats. Son sobre todo instrucciones y herramientas de la propia aplicación, que ningún método reduce. Lo que sí controla el arnés: la lectura propia (~10k) y, sobre todo, **la longitud del chat** (contexto máximo observado 93k–473k; la mediana de los largos pasa de 250k).

## 6. Los dos carriles (cómo se decide el trabajo)
| Carril | Cuándo | Pasos |
| :--- | :--- | :--- |
| **SDD** | Toca > 2 archivos, o un área sensible (dinero, pagos, licencias, permisos, base de datos, despliegue, datos de usuarios) | Spec desde la plantilla → **aprobación del dueño** → programar → tests → cierre |
| **Fast-Track** | Todo lo demás | Cambio → tests → cierre |

Una spec es corta: objetivo, qué entra y qué no, archivos, cómo se prueba, riesgos, aprobación. Su valor: que el dueño frene un error **antes** de gastar tokens.
Regla de desempate: si dudas entre carriles, es SDD.

## 7. Ciclo de vida de una tarea
```
Idea → [spec aprobada] → Falta programar → Implementada (tests verdes)
     → Esperando prueba del dueño → prueba OK → archive/hechos + índice
                                  → prueba falla → vuelve a «Falta programar» con nota
```
- La numeración de los puntos de `pendientes.md` es **fija** (los huecos son tareas hechas): así los índices no se rompen.
- Al confirmar el dueño que probó: **en esa misma respuesta** se transfiere el detalle a `hechos.md`, se añade su fila a `hechos-indice.md` y se quita de pendientes.

## 8. Checklist de cierre (obligatorio, cada tarea)
1. Tests en verde (comando fijo del proyecto).
2. Línea en `decisions.log` (fecha · quién/chat · qué · carril).
3. Decisión importante → ficha `D-NNN` + fila en el índice. Una decisión que cambia no se borra: «reemplazada por D-NNN».
4. `pendientes.md` al día (y transferencia a `hechos` si el dueño ya probó).
5. Mapa de funcionalidades actualizado si cambió algo visible.
6. Fila nueva en `herramientas.md` si se usó una herramienta nueva.
7. Si salió una preferencia o corrección del dueño: memoria personal del asistente (§12).
8. Resumen al dueño en lenguaje llano: qué quedó, qué debe probar, **qué no se verificó**.

## 9. Guardianes (que el método se cumpla solo)
Solo Python estándar; ajustes en `guardianes.json`; nada del proyecto de origen dentro de los scripts.
| # | Guardián | Qué hace | Cuándo |
| :-: | :--- | :--- | :--- |
| 1 | **Aviso de cierre** (`cierre.py`) | Si hay archivos del proyecto cambiados, la IA los editó en esta respuesta y falta la línea en `decisions.log` (o `pendientes.md` pasó su tope), la IA recibe el aviso y corrige. Avisa **una vez** por respuesta; si falla, calla. Ignora `.brain/`, `.claude/`, grabaciones, copias, base de datos. | Hook `Stop` de Claude Code |
| 2 | **Test de índices** | Ficha ↔ fila de decisiones, enlaces vivos, hechos ↔ índice de hechos, nada a la vez pendiente y hecho, topes de tamaño (pendientes y los tres índices de entrada) | Suite de tests (cualquier IA) |
| 4 | **Arranque** (`arranque.py`) | Resume el estado real al abrir el chat: puntos y tamaño de pendientes, commits sin subir, cambios sin commitear, última línea del registro | Hook `SessionStart` |
| 5 | **Fichas frescas** | Una ficha puede declarar `Archivos:` y `Revisada:`; si un archivo citado cambia en Git después, sale «a revisar» | En el resumen de arranque y en tests |
| 6 | **Poda de memoria** (`poda.py`, spec 048) | Mueve (nunca borra) a `archivo/` las specs ya terminadas (implementadas, sin nada pendiente de prueba y no citadas en pendientes) y las fichas «reemplazada por D-NNN» a secas; reescribe los enlaces, deja un índice de una línea por spec y lo anota en el registro. No actúa si hay cambios sin guardar o si quedarían enlaces rotos (en ese caso deshace). Avisa si `decisions.log` o `hechos.md` pasan de 60 KB (no recorta). Se apaga con `poda_activa` | Dentro de `arranque.py` (`SessionStart`); a mano `poda.py --ver` / `--aplicar` |
| 7 | **Análisis de código** (`analisis.py`, spec 049, D-044) | Lee el código con `ast` y avisa de: consultas SQL armadas con texto, funciones/archivos que crecen respecto a `analisis_base.json` (trinquete: no obliga a refactorizar) y reglas del proyecto declaradas en `guardianes.json` (timeout en llamadas de red, `audit_event` en rutas de escritura sensibles, nadie edita la tabla de auditoría). Lo ya incumplido se anota como excepción con motivo. Solo avisa. Se apaga con `analisis_activo` | Dentro de `arranque.py` (`SessionStart`); a mano `analisis.py --ver` / `--renovar-base` |
| 8 | **Base de datos** (`base_datos.py`, spec 050, D-045) | Defensa dentro de `users.db`: copia consistente en `copias_bd/` solo antes de cambiar tablas (rotación de 5, restauración solo con orden), salud al arrancar (`integrity_check`, `foreign_key_check`, triggers de auditoría) y foto del esquema (`esquema_base.json`, renovar con `--renovar-esquema --ficha D-NNN`). Solo avisa; motor genérico. |
| 9 | **Secretos** (`secretos.py`, spec 051, D-046) | Busca tokens y claves con formato real (Discord, Gemini, GitHub, `sk-`, llaves privadas, webhooks) y vigila que los archivos secretos sigan ignorados. Un hook `pre-commit` (`--instalar-hook`) **bloquea** el commit con un secreto de alta confianza; lo dudoso solo avisa. El historial se revisa a mano (`--historial`) y el arranque avisa a los 30 días. Genérico (kit de arranque). |
| 10 | **Librerías** (`librerias.py`, spec 052, D-047) | Cada semana (a mano) consulta OSV.dev (vulnerabilidades conocidas) y PyPI (versión mayor más nueva) para las librerías de `requirements.txt` y guarda el resultado; el arranque solo lo lee (sin red) y añade una línea. Solo avisa, nunca actualiza; si falla la red calla. Genérico (kit de arranque). |
| 11 | **Pruebas** (`pruebas.py`, spec 053, D-048) | Memoria indexada de campañas de pruebas con hallazgos (`.brain/pruebas/`, casillas `- [ ]`/`- [x]`). El arranque imprime una línea **solo si queda algo abierto** (0 tokens si todo está cerrado) y avisa si índice y archivos no coinciden. Genérico (kit de arranque). |
| 12 | **Longitud de chat** (`longitud.py`, spec 056, D-051) | El hook de cierre (`Stop`) mide el contexto real del chat y, al pasar 200k tokens (y cada 100k más), avisa **una vez por tramo** para abrir un chat nuevo, con la frase de traspaso lista. Solo avisa; solo en Claude Code (en Gemini y Codex sigue manual). Genérico (kit de arranque). |
| 13 | **Notas en chat abierto** (`notas_abiertas.py`, spec 081, D-072) | Al enviar el dueño un mensaje, imprime las notas nuevas de chats auxiliares que ese chat aún no recibió; sin notas, calla; no mueve nada | Hook `UserPromptSubmit` (Claude Code) |
| – | **Cierre rápido** (`cerrar.py`) | Añade la línea del registro con su formato; en un cambio de una línea basta con ella | A mano |
| 3 | **Medidor de tokens** (`medir.py`) | Por chat: coste ponderado, tokens nuevos, salida, arranque y correcciones; compara dos proyectos | A mano |

**Qué no hacen:** no leen mensajes, no envían datos fuera, no bloquean commits, no sustituyen el juicio.
**Cobertura por IA:** Claude Code → todos. Otras IA sin hooks (Gemini/Antigravity, GPT Codex) → solo 2 y la disciplina del manual. GPT Codex (probado el 2026-10-28, #41): con `AGENTS.md` actualizado y en un chat nuevo sí hizo el inicio solo (la primera vez, en el chat equivocado, no se pudo afirmar); ejecuta `arranque.py` bien cuando se lo indica el texto; **no** tiene aviso al terminar (el cierre con `cerrar.py` es manual y lo vigila el test); no abrió la constitución al no ser una orden escrita, por eso `AGENTS.md` la manda leer explícitamente. Mientras tanto, cualquier IA puede ejecutar `arranque.py` y `cerrar.py` a mano.
**Candidatos futuros (sin construir):** aviso al superar el umbral de longitud del chat; aviso si `decisions.log` o `hechos.md` pasan cierto tamaño; verificar que `FUNCIONALIDADES.md` no queda atrás respecto a cambios de interfaz.

## 10. Varias IA, varios chats, sesiones auxiliares
- **Un solo cerebro** (`.brain/`) para todas las IA. Los índices `CLAUDE.md`, `GEMINI.md` y `AGENTS.md` (GPT Codex) son espejo: si se cambia uno, se cambian los demás.
- **Chats numerados** (`Proyecto #N`) y **cortos**: la IA avisa sola cuando el chat se alarga y recomienda abrir uno nuevo. Un chat largo cuesta más que cualquier archivo, porque cada mensaje arrastra todo el historial.
- **Traspaso entre chats (spec 078):** antes de proponer o crear un chat nuevo, la IA escribe `.brain/traspaso.md` (plantilla `biblioteca/PLANTILLA_TRASPASO.md`: palabras literales del dueño, decisiones, estado de cada punto, lo no subido, lo descartado); `arranque.py` lo muestra en el chat nuevo y lo archiva en `archive/traspasos/`. Además, el chat nuevo arranca con una frase corta de contexto y lee el índice.
- **Notas de chats auxiliares (spec 080):** un chat que sale de otro (bifurcado o auxiliar) deja al terminar una nota corta en `.brain/notas-chats/` (plantilla `biblioteca/PLANTILLA_NOTA_CHAT.md`); `arranque.py` la muestra en el siguiente chat y la archiva en `archive/notas-chats/`. Sirve para cualquier IA; depende de que el auxiliar cumpla la regla.
- **Aviso en el chat abierto (spec 081, D-072):** hook `UserPromptSubmit` (`notas_abiertas.py`, guardián 13): al escribir el dueño, Claude recibe las notas nuevas una vez por chat. Claude Code (`.claude/settings.json`) y Codex (`.codex/hooks.json`, mismo script; según su documentación, **sin comprobar en vivo**: Codex pide confiar en el hook la primera vez). Gemini/Antigravity (spec 082, D-073): `.agents/hooks.json` con `PreInvocation`; el script responde `injectSteps` solo en la primera llamada (**formato según Gemini, sin comprobar en vivo**; la app de escritorio puede no pintarlo).
- **Sesiones auxiliares** (una sesión lanza otra para un trabajo concreto): el encargo debe ser autosuficiente; los hallazgos grandes se dejan en una carpeta de notas compartida, no en mensajes largos; el informe va primero con lo hecho.
- **Archivos que la IA no debe tocar** (grabaciones, copias de migración): se dejan sin commitear a propósito y se listan en `pendientes.md` y en `ignorar_cambios` de los guardianes.

## 11. Reglas de conducta de la IA (portables)
- Responder siempre en el idioma del dueño; tono directo; explicar sin jerga.
- **Alcance estricto:** nada de refactors no pedidos; si los tests están en verde y no hay fallo comprobado, no se reescribe.
- **Consultar lo decidido** antes de cambiarlo.
- **Git:** commits solo cuando se pide; **nunca subir a internet sin orden expresa**; no tocar archivos ajenos al cambio; no usar atajos que salten verificaciones.
- **Irreversible = preguntar:** subir, borrar, gastar, enviar mensajes, tocar datos reales.
- **No inventar:** si algo no se pudo probar, decirlo; no marcarlo como hecho.
- **Probar en la plataforma real.** Un guardián o script se da por bueno solo después de ejecutarlo donde el dueño lo usará (ver §16, caso del medidor).

## 12. Qué va en el repo y qué en la memoria personal del asistente
| Va en el **repo** (`.brain/`) | Va en la **memoria personal** (fuera del repo) |
| :--- | :--- |
| Lo que cualquier IA necesita saber del proyecto | Quién es el dueño y cómo prefiere que se le hable |
| Reglas, estado, decisiones, specs | Correcciones y preferencias de trabajo que valen entre proyectos |
| Hechos verificables en el código | Cosas que no se deducen del código ni de git |
Ejemplos vigentes: «Darwin no es programador: lenguaje llano» y «avisar de sesión larga». Regla: no duplicar en memoria lo que ya está en el repo; si una memoria resulta falsa, se borra.

## 13. Biblioteca y herramientas
- `herramientas.md`: una fila por herramienta usada (para qué, licencia/coste, estado ✅🔁⚠️📝, dónde verla). Se añade una fila **al usar algo nuevo**; antes de buscar algo, se mira ahí.
- Reglas aprendidas que valen siempre: **cero dependencias cuando se pueda · mirar la licencia comercial antes de publicar · toda llamada externa con tiempo máximo y plan B local · nada de secretos en el repositorio · el coste cero por defecto en IA creativa.**
- Si algo usado exige crédito (p. ej. Kokoro, datos CC BY), queda anotado en la fila y en pendientes como condición de publicación.

## 14. Kit de arranque (proyecto nuevo, en orden)
**Atajo (spec 054, D-049):** `python .brain/biblioteca/kit-arranque/instalar.py DESTINO --nombre … --dueno … --idioma … --pruebas "…" --ias claude,gemini,codex --nivel ligero|medio|completo` hace lo de abajo por ti y `--comprobar` prueba los guardianes. Con ventana: doble clic en `instalar_kit.bat` (spec 055). Detalle en `.brain/biblioteca/kit-arranque/README.md`. Los pasos siguientes explican lo que hace por dentro.

1. Crear la carpeta del proyecto y abrir el primer chat con la IA.
2. Copiar `CEREBRO_VIVO.md` y esta carta a `.brain/biblioteca/` del proyecto nuevo.
3. Pegar: *«Aplica el método Cerebro Vivo (`CEREBRO_VIVO.md` y `CARTA_META_ARNES.md`). Crea la estructura de la §4. Mis reglas innegociables son: […]. Comando de pruebas: […]. Idioma: […]. Explica sin jerga.»*
4. La IA crea: `CLAUDE.md` (+`GEMINI.md` y/o `AGENTS.md` según las IA que se usen), `.brain/` con constitución, pendientes (con su regla de cierre), `decisions.log`, índice de decisiones, plantilla de spec, `archive/` con `hechos` e índice, `architecture/` vacía.
5. **Instalar guardianes:** copiar `.brain/guardianes/` y `tests/test_cerebro_indices.py`; editar `guardianes.json` (ruta del registro, topes, patrones a ignorar); añadir el hook `Stop` en `.claude/settings.json`; reiniciar Claude Code; **probar los guardianes instalados** (§9) antes de confiar.
6. Escribir la primera spec solo cuando haya una tarea que toque > 2 archivos o área sensible.
7. Anotar el proyecto en la lista de §20.

**Idiomas del producto (opcional, spec 057, D-052):** `instalar.py DESTINO --traduccion` (o la casilla de la ventana) copia `biblioteca/kit-traduccion/` a `static/i18n/` y el test de paridad a `tests/`; añadir un idioma = una línea y un bloque de textos.

**Qué personalizar siempre:** reglas innegociables, comando de pruebas, idioma, idiomas del producto, topes, patrones ignorados, nombre de los chats.
**Qué no cambiar:** los 14 principios, el ciclo de vida de la tarea, el checklist de cierre.

## 15. Niveles de adopción
| Nivel | Qué lleva | Cuándo |
| :--- | :--- | :--- |
| **Ligero** | `CLAUDE.md` + `pendientes.md` + `decisions.log` | Proyecto pequeño o de pocos días |
| **Medio** | + constitución, decisiones con porqué, specs para lo sensible, archivo de hechos | Semanas; varios chats |
| **Completo** | + guardianes, biblioteca, multi-IA, memoria personal | Meses; dinero/permisos/datos de usuarios; dueño no técnico |
No usarlo: prototipo de un día, un solo chat que termina hoy, experimentos sin consecuencias.

## 16. Lecciones aprendidas (casos reales)
| Caso | Qué pasó | Regla que salió |
| :--- | :--- | :--- |
| `pendientes.md` a 20 KB (~6.000 tokens por arranque) | Faltaba la regla de pasar lo probado a «hechos» | Pendientes solo con lo que falta + tope de 8 KB + guardián (D-038, D-039) |
| Chats de 300–470k de contexto | Cada mensaje arrastraba todo el historial | Avisar y abrir chat nuevo; medir con el guardián 3 |
| Voz `edge-tts` | Gratis, pero sin licencia comercial garantizada | Mirar la licencia antes de publicar; se sustituyó por Kokoro (D-037) |
| Push a GitHub bloqueado por permisos | La IA no puede dar por hecho que subir funciona | Subir solo con orden expresa; dejar anotado qué queda sin subir |
| **Medidor de tokens roto en la consola de Windows** (hallado en la primera prueba real, chat #39) | Funcionaba en teoría; al ejecutarlo en la consola de Windows se caía al imprimir «⚠» | Probar guardianes en la plataforma real; los scripts del arnés fuerzan UTF-8 en su salida |
| «Implementada» dada por «hecha» | El dueño no la había probado | Sección «Esperando tu prueba» y transferencia solo tras su confirmación |
| **El aviso de cierre callaba por un registro viejo sin commitear** (hallado en la prueba en vivo, #39) | Comparaba contra el estado de Git: si `decisions.log` ya estaba modificado, daba la tarea por registrada | El guardián lee el chat y comprueba si la IA tocó el registro *en esa respuesta*; y cada tarea acaba en un commit |
| **Prueba de guardián que no probaba nada** (#39) | La primera prueba en vivo era inválida: el registro ya estaba modificado | Antes de probar un guardián, dejar el terreno limpio y comprobar que el caso de prueba *puede* fallar |
| Lo aprendido estaba repartido en carta, decisiones y herramientas (2026-10-31, #68) | La IA volvía a descubrir técnicas ya resueltas | Skills de experiencia (`.claude/skills/`), activadas por su descripción, con índice en `.brain/experiencia/` (D-070) |
| Reglas que dependían de la disciplina | Se olvidaban en silencio | Principio 8: guardianes |
| Fichas con números de línea | Se desfasaban | Referencias por número de punto fijo, no por línea |

## 17. Evidencia: qué se ha medido y qué no
- **Medido (25 chats, 25–28 oct 2026):** arranque ~69k tokens en todos; contexto máximo 93k–473k; total ~6,1 M tokens nuevos, ~549 M leídos de caché, ~2,5 M de salida.
- **Estimado, no medido:** el ahorro frente a un proyecto sin método (~90 % menos de lectura de arranque, por tamaño de archivos). No existe el chat «sin método» para compararlo.
- **Comprobado a mano:** el aviso de cierre devuelve aviso en los casos esperados (cambio sin registro → avisa; con registro, solo `.brain/`, grabaciones o sin ediciones de la IA → calla; pendientes sobre el tope → avisa). La suite de índices pasa (tests en `tests/test_cerebro_indices.py`; la suite completa de LoboHook, 992 a 2026-11-01).
- **Comprobado en vivo (2026-10-28, #39):** el hook `Stop` de Claude Code saltó solo al terminar una respuesta que editó un archivo sin registrar, con el texto bien codificado, aunque `decisions.log` tuviera cambios de una tarea anterior. Requiere reabrir Claude Code para cargar el hook.
- **Medido (65 chats, 31 oct 2026, #70):** el método añade ~8-10k tokens al arrancar (69k→77k frente a 66-69k en proyectos sin método); cerrar tareas (registro, fichas, índices) es como máximo el 14 % de los mensajes y el 11 % de los tokens nuevos; coste medio por chat ~190k tokens nuevos frente a ~850k-1.200k en dos proyectos sin método (no es comparación limpia: otro tipo de trabajo). Lo que más pesa es la longitud del chat.
- **Sin verificar aún:** el comportamiento del hook en otro sistema operativo o en otra IA con hooks propios.

## 18. Hoja de ruta del arnés
1. ✅ Prueba en vivo del hook (cerrada en #39).
2. ✅ Fichas con archivos y revisión (spec 047, falta prueba en vivo); falta añadir `Archivos:` a las fichas existentes cuando se toquen.
3. ✅ Aviso de tamaño de `decisions.log`/`hechos.md` (guardián 6, spec 048). ✅ Aviso de longitud de chat (guardián 12, spec 056).
4. Cobertura equivalente al hook para Gemini/Antigravity (hoy solo el test). GPT Codex: ✅ `AGENTS.md` creado y probado (#41): no lo lee solo, arranque y cierre son manuales. ✅ Gemini/Antigravity probado (#41): recibe `GEMINI.md` por el sistema; con las instrucciones de inicio escritas en `GEMINI.md`, en un **chat nuevo** leyó la constitución y los pendientes, ejecutó `arranque.py --manual` y mostró el resumen correcto **sin que se lo pidieran** (un chat ya abierto no recarga `GEMINI.md`). El cierre sigue siendo manual (`cerrar.py`). Sin `--manual` el arranque se quedaba esperando el teclado: arreglado y con test. Codex repetido en **chat nuevo** (#41): leyó la constitución y ejecutó `arranque.py --manual` sin que se lo pidieran, con el resumen correcto (no abrió `pendientes.md`, pero el resumen ya lo cubre).
5. ✅ Kit de arranque (spec 054, D-049): `kit-arranque/instalar.py` con niveles y `--comprobar`; probado por el dueño (en uso en otro proyecto, 2026-11-01). ✅ Kit de traducción opcional (spec 057, D-052): `--traduccion`, idiomas ampliables; probado por el dueño (2026-11-01, #72): selector y recuerdo del idioma en el navegador, el test de paridad falla con claves faltantes y con un JSON roto y pasa con todo en su sitio.
6. ✅ Guardián 7 de análisis AST (spec 049): probado por el dueño. ✅ Guardián 8 de defensa en la base de datos (spec 050, D-045): probado por el dueño.
   ✅ Guardián 9 de secretos (spec 051, D-046): hook pre-commit que bloquea; probado por el dueño.
   ✅ Guardián 10 de librerías (spec 052, D-047): chequeo semanal a mano; probado por el dueño.
   ✅ Guardián 11 de memoria de pruebas (spec 053, D-048): probado por el dueño (2026-11-01, el arranque avisa de pruebas pendientes).
   ✅ Guardián 12 de longitud de chat (spec 056, D-051): probado por el dueño (2026-11-01, avisa).
7. ✅ Política de poda (spec 048): mover, no borrar; la ejecuta el guardián 6. `poda_activa` encendida por orden del dueño (D-043): corre sola al abrir cada chat. Falta verla mover una spec real.

8. ✅ **Resuelto en la spec 078 (probado por el dueño, 2026-11-01, #72):** `traspaso.md` + lectura en el arranque. Detectado por Darwin el 2026-10-29 (#51): al pedir «crea un chat nuevo», el chat nuevo **pierde el último tramo de la conversación** (lo hablado justo antes: decisiones, dudas, estado a medias). El traspaso solo lleva lo que la IA escribe en el encargo y lo registrado en `.brain/`. Revisar al terminar el trabajo actual: guardar un resumen del último tramo (carpeta compartida de traspaso o `.brain/`) y que el chat nuevo lo lea al arrancar; y definir qué debe llevar siempre el encargo (decisiones abiertas, texto literal del dueño, estado de cada punto).

## 19. Huecos conocidos (honestidad)
- Depende de que la IA lea los índices; el guardián solo detecta olvidos al *cerrar*, no malas lecturas al empezar.
- Coste fijo de mantenimiento: 3–4 escrituras por tarea; desproporcionado en cambios de una línea.
- Una ficha falsa se propaga: las fichas se verifican contra el código cuando deciden algo.
- La aprobación de specs frena el trabajo si el dueño no está.
- El ahorro real frente a «sin método» no es medible con precisión (no hay la misma tarea hecha con y sin método); solo hay comparación aproximada (§17).
- Los guardianes asumen Claude Code, Git y Windows/Python; en otro entorno hay que adaptarlos **(sin verificar fuera de Windows)**.

## 20. Proyectos que usan el arnés
| Proyecto | Nivel | Desde | Notas |
| :--- | :--- | :--- | :--- |
| LoboHook | Completo | 2026-10 (#1) | Origen del método; guardianes desde #38 |
| Otro proyecto de Darwin | Kit de arranque | 2026-11 | En uso (probado por el dueño, 2026-11-01) |
| *(añadir aquí cada proyecto nuevo)* | | | |

## 21. Registro de versiones de la carta
| Versión | Fecha | Cambio |
| :--- | :--- | :--- |
| 0.1 | 2026-10-28 | Primera carta completa (LoboHook #39): principios, 7 capas, kit de arranque, lecciones, huecos |
| 0.2 | 2026-10-28 | Hook comprobado en vivo; 2 lecciones nuevas; añadidos §22 (seguridad), §23 (plantillas), §24 (glosario) y §25 (cómo se mantiene la carta) |
| 0.3 | 2026-10-28 | Guardianes 4 y 5 y cierre rápido (spec 047, D-040) en §9 y §18 |
| 0.4 | 2026-10-28 | Incluido GPT Codex (`AGENTS.md`) en índices, cobertura por IA y hoja de ruta (§3, §4, §9, §10, §14, §18) |
| 0.5 | 2026-10-28 | Guardián 6: poda de memoria (spec 048), mover sin borrar |
| 0.6 | 2026-10-28 | GPT Codex probado en vivo: hallazgos en §9 y §18 |
| 0.7 | 2026-10-28 | Gemini/Antigravity probado en vivo; `arranque.py --manual`; GEMINI.md con pasos de inicio y cierre; arranque solo confirmado en chat nuevo |
| 0.8 | 2026-10-28 | Codex confirmado en chat nuevo: arranca solo |
| 0.9 | 2026-10-28 | Carta al día con la realidad (cifras, poda encendida); índices de entrada con tope de 5 KB vigilado en los tres (D-043); `referencias.md`; tabla de versiones ordenada |
| 0.10 | 2026-10-28 | Guardián 7: análisis AST (spec 049, D-044) en §4, §9 y §18 |
| 0.11 | 2026-10-28 | Guardián 8: defensa en la base de datos (spec 050, D-045) en §9 y §18 |
| 0.12 | 2026-10-28 | Guardián 9: secretos (spec 051, D-046) en §9 y §18 |
| 0.13 | 2026-10-28 | Guardián 10: vigilancia de librerías (spec 052, D-047) en §9 y §18 |
| 0.14 | 2026-10-28 | Guardián 11: memoria de pruebas (spec 053, D-048) en §9 y §18 |
| 0.15 | 2026-10-28 | Kit de arranque (spec 054, D-049): `instalar.py` en §14 y §18 punto 5 |
| 0.16 | 2026-10-28 | Ventana del instalador del kit (spec 055, D-050) en §14 |
| 0.17 | 2026-10-28 | Guardián 12: aviso de longitud de chat (spec 056, D-051) en §9 y §18 |
| 0.18 | 2026-10-28 | Kit de traducción es/en/pt opcional (spec 057, D-052) en §14 y §18 punto 5 |
| 0.19 | 2026-10-31 | Traspaso entre chats (spec 078, D-069): `traspaso.md`, plantilla y lectura en el arranque en §10 y §18 punto 8 |
| 0.20 | 2026-10-31 | Sistema de experiencia (spec 079, D-070): 28 skills reales en `.claude/skills/` + índice `experiencia/indice.md`; lección en §16 |
| 0.21 | 2026-10-31 | Notas de chats auxiliares (spec 080, D-071) en §10; consumo medido en 65 chats (punto 51) en §17 |
| 0.22 | 2026-11-01 | Puesta al día de cifras (v. de cabecera, 992 tests, fichas, chats), §14 «probar los guardianes», §17 suite, §20 segundo proyecto; probados por el dueño: traspaso (078), kit de arranque, guardianes 11 y 12 (#72) |
| 0.23 | 2026-11-01 | Guardián 13 (spec 081, D-072): el chat principal ya abierto recibe las notas de los auxiliares al escribir el dueño (hook `UserPromptSubmit`); §9 y §10 |
| 0.24 | 2026-11-01 | Aviso de notas para Codex (`.codex/hooks.json`) y Gemini/Antigravity (spec 082, D-073); §10 |

## 22. Seguridad y límites (portables)
- **Secretos:** claves, tokens y contraseñas viven en variables de entorno o en archivos ignorados por Git, nunca en el repositorio. Antes de cada subida, escanear en busca de secretos (D-020 en LoboHook).
- **Datos reales:** pruebas con base de datos temporal; los tests nunca tocan los datos reales.
- **Lo que la IA no hace sola:** subir a internet, borrar datos, gastar dinero, enviar mensajes en nombre del dueño, cambiar permisos o configuración de seguridad.
- **Llamadas externas:** tiempo máximo estricto y plan B local; el programa no debe caerse porque un servicio externo falle.
- **Acciones críticas** (roles, licencias, pagos, cuotas, despliegues, borrados): registro de auditoría inmutable.
- **Antes de tocar algo en vivo:** instantánea y vuelta atrás garantizada.
- **Los guardianes** no leen el contenido de los mensajes ni envían nada fuera del equipo.

## 23. Plantillas listas para copiar
**`pendientes.md`**
```
# Pendientes
Lista viva de lo que falta. Una línea por punto. Numeración fija (los huecos son puntos ya hechos).
Regla de cierre: al confirmar el dueño que probó una tarea, en esa misma respuesta pasa a archive/hechos.md + fila en hechos-indice.md y se quita de aquí. Si falla, vuelve a «Falta programar» con nota.
## Falta programar (IA)
## Esperando tu prueba (dueño)
## Acciones tuyas
## Más adelante
```
**Fila de `decisions.log`:** `AAAA-MM-DD | quién (Proyecto #N) | qué se hizo, en una frase | SDD o Fast-Track`
**Ficha `D-NNN-nombre.md`:** Estado · Fecha · Decidió · Área → *Por qué* → *Decisión* → *Consecuencias* → *Relacionado* (≤ 15 líneas).
**`hechos-indice.md`:** tabla `Nº | Qué | Fecha | Ref.` (lo más reciente arriba). **`hechos.md`:** `## Nº · título` + `Fecha · Ref` + 2–4 líneas de qué se probó y qué límites quedaron.
**Spec:** objetivo · en alcance · fuera de alcance · plan · plan de verificación · cierre (aprobada por el dueño antes de programar).
**Frase de traspaso a un chat nuevo:** *«Venimos de Proyecto #N. Qué se hizo: … Qué queda sin subir: … Qué debe probar el dueño: … Lee el índice y responde; no empieces nada por tu cuenta.»*
**Hook `.claude/settings.json`:** evento `Stop` que ejecuta `cierre.py` con el Python del entorno virtual del proyecto (tiempo máximo 20 s).

## 24. Glosario en lenguaje llano
| Término | Qué significa |
| :--- | :--- |
| Arnés | Todo lo que rodea a la IA para que trabaje con orden: archivos, reglas y vigilantes |
| Meta-arnés | El arnés que sirve para crear el arnés de cada proyecto (esta carta) |
| Contexto | Todo lo que la IA «tiene delante» en un chat; cuanto más largo, más cuesta cada mensaje |
| Token | La unidad en que se mide ese texto (aprox. ¾ de palabra) |
| Spec | Ficha corta de lo que se va a construir, aprobada antes de programar |
| Hook | Aviso automático que Claude Code lanza en un momento fijo (aquí, al terminar cada respuesta) |
| Guardián | Comprobación automática de que el método se cumple |
| Commit | Foto guardada de los cambios en el equipo; no es subirlos a internet |
| Push | Subir esos commits a GitHub; solo con orden del dueño |
| Fast-Track / SDD | Los dos carriles de trabajo (§6) |

## 25. Cómo se mantiene esta carta
- Se actualiza cuando **algo del método cambia, falla o se aprende**, no por calendario.
- Cada cambio: subir la versión (§21), corregir §16 si hubo lección y §17–§19 si cambió lo comprobado o lo pendiente.
- Lo comprobado y lo supuesto se distinguen siempre; nada pasa a «comprobado» sin haberlo ejecutado.
- Al empezar un proyecto nuevo (§20) se copia la versión vigente; las mejoras vuelven aquí.
- Si esta carta y `CEREBRO_VIVO.md` se contradicen, manda la carta y se corrige el manual.

