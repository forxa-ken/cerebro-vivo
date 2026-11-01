# Método «Cerebro Vivo»

> Método de trabajo para construir un proyecto de software con una IA (Claude, Gemini u otra) **sin que se pierda el contexto entre chats y gastando pocos tokens**. Nació en LoboHook (2026) y está escrito para copiarlo a otros proyectos.
> Para usarlo: copia este archivo al proyecto nuevo y dile a la IA: *«Aplica el método Cerebro Vivo de `CEREBRO_VIVO.md`: crea la estructura y trabaja con sus reglas.»*

---

## 1. La idea en una frase
La IA **no recuerda** lo que pasó en chats anteriores. Así que la memoria del proyecto vive en **archivos**, ordenados para que la IA lea poco al empezar y solo busque el detalle cuando lo necesite. *La verdad está en el código y en estos archivos, no en la conversación.*

## 2. Los cinco principios
1. **Índice primero, detalle después.** Al empezar se lee un índice corto; el detalle solo se abre si hace falta.
2. **Cada cosa en su sitio.** Reglas, tareas pendientes, tareas hechas, decisiones y especificaciones van en archivos distintos.
3. **Cerrar es parte de trabajar.** Una tarea no está terminada hasta que se actualiza la memoria (registro, pendientes, índice).
4. **Lo hecho sale de la vista.** Lo terminado se archiva con un índice; lo pendiente queda siempre corto.
5. **El «porqué» se guarda.** Una decisión sin su razón se vuelve a discutir (y a gastar) cada vez.

## 3. Estructura de archivos

```
CLAUDE.md                  ← índice corto para Claude (≤ 5 KB)
GEMINI.md                  ← mismo índice para otra IA (si se usa más de una)
.brain/
  README.md                ← mapa de esta carpeta
  constitution.md          ← reglas innegociables
  pendientes.md            ← SOLO lo que falta (≤ ~8 KB)
  decisions.log            ← una línea por tarea terminada: qué se hizo
  decisions/
    indice.md              ← tabla de decisiones importantes
    D-001-nombre.md        ← una ficha por decisión, con su porqué (≤ 15 líneas)
  specs/
    _template.md
    001-nombre.md          ← especificación aprobada antes de programar
  architecture/
    area.md                ← ficha por área técnica (leer solo la que toque)
  archive/
    hechos.md              ← detalle de tareas terminadas y probadas
    hechos-indice.md       ← una fila por tarea hecha (se consulta ESTE)
    historial-antiguo.md + indice.md   ← para registros viejos muy largos
  guardianes/              ← comprobaciones automáticas del método (sección 10)
  biblioteca/              ← material reutilizable entre proyectos
```

| Archivo | Responde a | ¿Se lee al empezar? |
| :--- | :--- | :---: |
| `CLAUDE.md` | ¿Cómo se trabaja aquí y dónde está cada cosa? | Sí |
| `constitution.md` | ¿Qué reglas no se pueden romper? | Sí |
| `pendientes.md` | ¿Qué falta? | Sí |
| `architecture/<área>.md` | ¿Cómo funciona esta parte? | Solo el área de la tarea |
| `decisions/indice.md` | ¿Ya se decidió esto antes y por qué? | Si se va a cambiar algo decidido |
| `specs/` | ¿Qué se aprobó construir? | Solo la de la tarea |
| `decisions.log` | ¿Qué se hizo y cuándo? | No (solo se añade al final) |
| `archive/hechos-indice.md` | ¿Se hizo X? ¿Cuándo? | Solo si se consulta |

**Lectura de arranque:** `CLAUDE.md` + `constitution.md` + `pendientes.md` + una ficha de `architecture/`. En LoboHook son unos 35 KB (~10.000 tokens) frente a ~150.000 si hubiera que leer todo.

## 4. Los dos carriles de trabajo
| Carril | Cuándo | Pasos |
| :--- | :--- | :--- |
| **SDD** (especificar primero) | Toca más de 2 archivos, o un área sensible (dinero, permisos, licencias, base de datos, despliegue) | 1) Crear spec desde `_template.md`. 2) **Esperar aprobación del dueño.** 3) Programar. 4) Tests. 5) Cerrar. |
| **Fast-Track** | Todo lo demás | 1) Aplicar el cambio. 2) Tests en verde. 3) Cerrar. |

Una spec es corta: objetivo, qué entra y qué no, archivos que se tocan, cómo se prueba, riesgos. Su valor es que **el dueño aprueba antes de gastar tokens programando algo equivocado**.

## 5. Ciclo de vida de una tarea (y de un punto de `pendientes.md`)

```
Idea ──► [spec aprobada] ──► Falta programar ──► Implementada
                                                     │  tests en verde
                                                     ▼
                                       Esperando prueba del dueño
                                          │                 │
                                  prueba OK          prueba falla
                                          ▼                 ▼
                                   archive/hechos   vuelve a «Falta programar»
                                   + índice            con nota de qué falló
```

- **Implementada ≠ terminada.** Hasta que el dueño la prueba, la tarea sigue en `pendientes.md`, en la sección «Esperando tu prueba», con **una sola línea**.
- **Probada = terminada.** En la misma respuesta en que el dueño confirma, la IA transfiere: detalle a `hechos.md`, fila a `hechos-indice.md`, y borra el punto de `pendientes.md`. No se espera a que el archivo «se llene».
- **La numeración es fija.** El punto 16 sigue siendo el 16 en el archivo; los huecos son tareas hechas. Así los índices nunca se rompen.

## 6. Cierre de tarea (checklist obligatorio)
1. Tests en verde (comando fijo del proyecto).
2. Una línea en `decisions.log` (fecha, quién, qué, carril).
3. Si hubo una decisión importante: ficha `D-NNN` + fila en `decisions/indice.md`. Una decisión que cambia **no se borra**: se marca «reemplazada por D-NNN».
4. Actualizar `pendientes.md` (y transferir a `hechos` si el dueño ya probó).
5. Si cambió una funcionalidad, actualizar el mapa de funcionalidades.
6. Resumen al dueño en lenguaje llano: qué quedó, qué falta probar, qué no se verificó.

**Modo ligero (v1.2.0):** si la tarea fue pequeña (hasta 2 archivos, ninguno sensible, sin tocar `.brain/`) y las pruebas salieron en verde, el guardián `cierre.py` escribe solo la línea del registro (`Claude (auto)`) y los pasos 3-5 no hacen falta. Se apaga con `modo_ligero_activo` en `guardianes.json`. Motivo: en la medición de la spec 001 el cierre completo costaba entre un 17 % y un 43 % más de tokens en tareas pequeñas.

## 7. Reglas de conducta de la IA
- **Alcance estricto:** tocar solo lo que pide la tarea; nada de refactors no pedidos.
- **Tests siempre en verde;** si no hay fallo comprobado, no se reescribe código que funciona.
- **Consultar antes de cambiar lo ya decidido** (`decisions/indice.md`).
- **Lo irreversible se pregunta:** subir a internet, borrar, gastar dinero, tocar datos reales.
- **Hablar al nivel del dueño** (aquí: lenguaje llano, sin jerga, porque no es programador).
- **Avisar cuando el chat se alarga** y recomendar abrir uno nuevo (`Proyecto #N`). Un chat largo cuesta más que cualquier archivo, porque cada mensaje arrastra todo el historial.
- **No inventar:** si algo no se pudo probar, decirlo; no marcarlo como hecho.

## 8. Cómo arrancar en un proyecto nuevo
Pega esto en el primer chat:

> Aplica el método Cerebro Vivo (`CEREBRO_VIVO.md`). Crea `CLAUDE.md`, `.brain/` con `constitution.md`, `pendientes.md`, `decisions.log`, `decisions/`, `specs/`, `architecture/` y `archive/`. Mis reglas innegociables son: [escríbelas]. Comando de pruebas: [comando]. Responde en [idioma] y explica sin jerga. Trabaja con dos carriles (SDD/Fast-Track) y cierra cada tarea con el checklist.

**Plantillas mínimas**
- `pendientes.md`: encabezado con la regla de cierre + secciones *Falta programar*, *Esperando tu prueba*, *Acciones tuyas*, *Más adelante*.
- `hechos-indice.md`: tabla `Nº | Qué | Fecha | Ref.`.
- Ficha `D-NNN`: *Fecha · Estado · Decisión · Por qué · Consecuencias · Relacionado* (≤ 15 líneas).
- Spec: *Objetivo · Alcance (entra / no entra) · Archivos · Cómo se prueba · Riesgos · Aprobación del dueño*.

**Con el repo del arnés (`cerebro-vivo`, spec 087):** el método vive en su propio repositorio y cada proyecto se instala y se actualiza desde él.

| Comando | Para qué |
| :--- | :--- |
| `python .brain/biblioteca/kit-arranque/instalar.py RUTA --nombre N --dueno D --nivel completo` | Instala el método en un proyecto nuevo (guardianes, skills, kits, manual, pruebas) y anota de dónde se actualiza (`arnes_repo` en `guardianes.json`) |
| `python .brain/guardianes/actualizar_arnes.py --simular` | En un proyecto: enseña qué archivos del arnés cambiarían, sin escribir nada |
| `python .brain/guardianes/actualizar_arnes.py` | Actualiza: guarda copia en `.brain/copias_arnes/`, copia lo nuevo, **no pisa lo que modificaste a mano** (lo lista), nunca toca pendientes, specs, decisiones, registro ni `guardianes.json` (las claves nuevas solo las propone) y corre las pruebas del método |
| `… actualizar_arnes.py --forzar RUTA` | Pisa un archivo que sí quieres reemplazar aunque lo hayas modificado (con copia de seguridad) |
| `… actualizar_arnes.py --forzar-todo` | Primera vez en un proyecto antiguo (sin registro previo): pisa **todo** lo que difiere, siempre con copia en `.brain/copias_arnes/`. Úsalo solo tras ver la lista con `--simular` |
| `… actualizar_arnes.py --repo CARPETA_O_URL_GIT` | Indica el repo del arnés si el proyecto no lo tiene anotado |
| `python actualizar.py RUTA_PROYECTO [--simular]` | Lo mismo, lanzado desde el repo del arnés apuntando a un proyecto |
| `python generar_manifiesto.py [--ver]` | Solo en el repo del arnés: regenera `manifiesto.json` (lista de archivos con su huella) tras una mejora, con `VERSION` subida y `CAMBIOS.md` anotado; `--ver` dice si está al día |

---

## 9. Guardianes: que el método se cumpla solo
El punto débil del método es que depende de la disciplina de la IA. Los guardianes (carpeta `.brain/guardianes/`, solo librería estándar de Python, ajustes en `guardianes.json`) lo convierten en comprobaciones automáticas:

| Guardián | Archivo | Qué hace | Cuándo actúa |
| :--- | :--- | :--- | :--- |
| **1. Aviso de cierre** | `cierre.py` | Si se tocaron archivos del proyecto y falta la línea en `decisions.log`, o `pendientes.md` pasó su tope, la IA recibe el aviso y lo corrige. Avisa **una sola vez** por respuesta. | Al terminar cada respuesta (hook `Stop` de Claude Code, en `.claude/settings.json`) |
| **2. Test de índices** | `tests/test_cerebro_indices.py` | Cada ficha `D-NNN` tiene fila y viceversa; enlaces que existen; índice de hechos = hechos; ningún punto a la vez pendiente y hecho; topes de tamaño. | En la suite normal de tests (sirve para cualquier IA) |
| **4. Arranque** | `arranque.py` | Al abrir un chat inyecta el estado real: puntos de pendientes y su tamaño, commits sin subir, cambios sin commitear, última línea del registro y fichas de decisión a revisar. | Hook `SessionStart` de Claude Code |
| **5. Fichas frescas** | `arranque.py` + `decisions/_template.md` | Una ficha puede declarar `Archivos:` y `Revisada:`; si un archivo citado cambió en Git después, sale «a revisar». | En el resumen de arranque |
| **Cierre rápido** | `cerrar.py` | Añade la línea del registro con su formato: `python .brain/guardianes/cerrar.py "qué se hizo" --chat "Proyecto #N"`. En un cambio de una línea basta con esta línea. | A mano o por la IA |
| **Modo auto** | `modo_auto.py` (hook `PreToolUse`) | La IA avanza sola dentro de la spec aprobada y el guardián **bloquea** lo que se sale de los límites (archivos fuera de la spec, base de datos real, `git push`, chat que no es nuevo, 2 fallos sin arreglar, 200k de contexto). Comandos: `activar NNN [NNN…]` (specs aprobadas, chat nuevo) · `desactivar` (vuelve a modo normal) · `estado` · `fallo CLAVE` · `resuelto CLAVE` (un fallo arreglado al momento no cuenta) · `otro-sitio ARCHIVO «qué fallaba» «qué cambio»` (corrección fuera de la spec, queda en el registro) · `continuar` (solo Darwin levanta una parada) · `hecha` (pasa a la siguiente spec de la cola) · `base-prueba crear\|restaurar` (copia fija de la base). Todos como `python .brain/guardianes/modo_auto.py COMANDO`. Spec 086, D-077. | Hook automático + comandos a mano |
| **Prompt inicial** | `/prompt-inicial` (skill en `.claude/skills/prompt-inicial`) y panel `/plantilla` (plugin `plantilla-prompt`) | Ayudan a empezar un chat con un encargo completo: objetivo, cómo sabré que está bien, qué NO quiero, material, cómo trabajar (SDD o rápido, auto o paso a paso), plazos, costes, idioma y qué debe probar el dueño; avisa de lo que falta y espera el visto bueno antes de actuar. En un proyecto ya empezado ofrece retomar el traspaso, un pendiente, una spec o el estado. `/prompt-inicial` funciona en el chat sin gastar IA extra; `/plantilla` es el panel visual, con un botón **Mejorar con IA** (reescribe el prompt armado con Haiku, gasta un poco de tu uso de Claude; te enseña la propuesta y tú eliges «Usar» o «Descartar», nunca se envía sola): se instala una vez desde la app (+ → Agregar plugins → Agregar desde un repositorio → `forxa-ken/cerebro-vivo` → `plantilla-prompt`, pasos en `.brain/mods/README.md`) y `arranque.py` avisa si falta. Para Gemini/Codex, pedirle a Claude «la versión para Gemini/Codex» y escribe la plantilla en blanco en `.brain/biblioteca/PLANTILLA_PROMPT_INICIAL.md`. Specs 084 y 085, D-075 y D-076. | A mano (Darwin) |
| **3. Medidor de tokens** | `uso_tokens.py` | Lee los registros de chat de Claude Code y muestra por chat: tokens nuevos, caché, salida, **arranque** y contexto máximo (marca los chats largos). | A mano: `python .brain/guardianes/uso_tokens.py` |

**Cómo se llevan a otro proyecto:** copiar `.brain/guardianes/` y `tests/test_cerebro_indices.py`, editar `guardianes.json` (topes y patrones a ignorar), añadir los hooks `Stop` (cierre) y `SessionStart` (arranque) en `.claude/settings.json`. Los scripts no contienen nada del proyecto de origen. Las IA que no usan hooks de Claude Code (p. ej. Gemini) quedan cubiertas por el guardián 2.

**Qué no hacen:** no leen los mensajes, no envían datos a ningún sitio, no bloquean commits y no sustituyen el juicio de la IA; solo detectan olvidos.

## 10. Opinión objetiva (con lo vivido en LoboHook)

### Lo que funciona bien
- **Ahorra mucho al empezar cada chat.** Estimación por tamaño de archivos (no es un conteo real de tokens): ~10.000 tokens de arranque frente a ~150.000 sin índices, un ~90 % menos. Es la mayor ventaja.
- **Elimina la «amnesia» de la IA.** Se retoma una tarea tras días o con otra IA (Claude y Gemini compartieron el mismo `.brain/`) sin repetir explicaciones.
- **Las specs evitan trabajo tirado.** Pedir aprobación antes de tocar dinero, permisos o base de datos cuesta poco y evita rehacer.
- **Las fichas de decisión frenan discusiones repetidas** y permiten revertir con criterio.
- **Hace visible el estado real:** qué está programado, qué probado y qué falta. El dueño no necesita leer código.
- **Funciona con un dueño no técnico**, porque la comunicación obligatoria es en lenguaje llano.

### Lo que cuesta o falla
- **Coste de mantenimiento fijo.** Cada tarea pequeña exige 3-4 escrituras de archivos al cerrar. Para un cambio de una línea es desproporcionado (por eso existe Fast-Track, pero igual hay que registrar).
- **Depende de que la IA cumpla la disciplina.** No hay nada que obligue técnicamente; si se olvida de cerrar, la memoria se desactualiza en silencio. Prueba real: `pendientes.md` creció a 20 KB (~6.000 tokens) porque faltaba la regla de transferir lo hecho. El método falló justo donde no tenía regla.
- **Los índices pueden quedar desfasados** (filas olvidadas, números de línea que ya no coinciden). Por eso se prefieren números de punto fijos a números de línea.
- **La memoria crece sin límite** (en LoboHook ~400 KB tras unas 45 specs). El índice protege el arranque, pero si el índice mismo engorda, se pierde el ahorro.
- **La aprobación de specs ralentiza** si el dueño no está disponible; el trabajo queda parado.
- **Un fallo en un hecho guardado se propaga:** si una ficha dice algo falso, la IA lo creerá. Las fichas deben verificarse contra el código cuando se usan para decidir.
- **Es exagerado para proyectos pequeños** (un script, una web de una página, algo que dura un fin de semana).

### Cuándo usarlo y cuándo no
| Usarlo | No usarlo (o usar solo la mitad) |
| :--- | :--- |
| Proyecto de semanas o meses | Prototipo de un día |
| Varios chats o varias IA | Un solo chat que termina hoy |
| Dinero, permisos o datos de usuarios | Experimentos sin consecuencias |
| Dueño no técnico que necesita ver el estado | Programador que ya lleva todo en la cabeza |

**Versión ligera** para proyectos pequeños: solo `CLAUDE.md` + `pendientes.md` + `decisions.log`.

### Mejoras
1. ✅ **Cierre automatizado** con un hook (guardián 1, spec 046).
2. ✅ **Tokens medidos de verdad** (guardián 3). Primera lectura en LoboHook (24 chats, 25-28 oct 2026): el arranque cuesta ~69.000 tokens en **todos** los chats; el contexto máximo ronda 150-470k; la mediana de los chats largos pasa de 250k. Conclusión honesta: esos ~69k son sobre todo el sistema de la herramienta (instrucciones y herramientas), que ningún método puede reducir; lo que el método controla es lo que se lee **encima** de eso (~10k en vez de ~150k) y, sobre todo, **la longitud del chat**. Lo que no se puede medir es el chat que habría existido sin el método: el ahorro frente a ese caso sigue siendo una estimación.
3. ✅ **Test que valida los índices** (guardián 2).
4. **Pendiente:** fechar cada ficha y revisarla cuando el código cambie.

### Veredicto
Muy buen método para **proyectos medianos y largos con IA**: la continuidad y el control de lo que se lee compensan el mantenimiento. Su punto débil era sostenerse por disciplina; los guardianes lo cubren en parte (olvidos y desfases), pero el mayor gasto real son los chats largos, y ahí solo ayuda cerrar y abrir uno nuevo a tiempo. Para algo pequeño, usa la versión ligera.
