/* Datos de las fichas, tarjetas y diapositivas en cada idioma. JSON estricto: lo lee comprobar_idiomas.py. */
window.DATOS = {
 "es": {
  "FILES": [
   {
    "p": "CLAUDE.md",
    "d": 0,
    "q": "¿Cómo se trabaja aquí y dónde está cada cosa?",
    "r": "Siempre, al empezar",
    "w": "Se cuida a mano, hasta 5 KB",
    "n": "GEMINI.md y AGENTS.md cumplen el mismo papel para otras IA."
   },
   {
    "p": ".brain/",
    "d": 0,
    "g": 1,
    "q": "Toda la memoria del proyecto",
    "r": "Por partes, nunca entera",
    "w": "La IA y los guardianes",
    "n": "Es el corazón del método."
   },
   {
    "p": "constitution.md",
    "d": 1,
    "q": "¿Qué reglas no se pueden romper?",
    "r": "Al empezar",
    "w": "Solo cambia con tu autorización",
    "n": "Hay 10 reglas en este repositorio."
   },
   {
    "p": "pendientes.md",
    "d": 1,
    "q": "¿Qué falta?",
    "r": "Al empezar",
    "w": "La IA, al abrir y cerrar puntos",
    "n": "Tope de 8 KB. Solo lo que falta, con numeración fija."
   },
   {
    "p": "decisions.log",
    "d": 1,
    "q": "¿Qué se hizo y cuándo?",
    "r": "No se lee al empezar: se añade al final",
    "w": "cerrar.py, o cierre.py en modo ligero",
    "n": "Una línea por tarea terminada."
   },
   {
    "p": "decisions/",
    "d": 1,
    "q": "¿Ya se decidió esto y por qué?",
    "r": "Si se va a cambiar algo decidido",
    "w": "La IA, una ficha D-NNN por decisión",
    "n": "Una decisión que cambia no se borra: se marca como reemplazada."
   },
   {
    "p": "specs/",
    "d": 1,
    "q": "¿Qué se aprobó construir?",
    "r": "Solo la de la tarea en curso",
    "w": "La IA; la apruebas tú",
    "n": "Objetivo, qué entra y qué no, archivos, pruebas y riesgos."
   },
   {
    "p": "architecture/",
    "d": 1,
    "q": "¿Cómo funciona esta parte del proyecto?",
    "r": "Solo la ficha del área que toca",
    "w": "La IA, también con /trocea",
    "n": "Un archivo por tema, con nombre claro."
   },
   {
    "p": "traspaso.md",
    "d": 1,
    "q": "¿Dónde se quedó el chat anterior?",
    "r": "Al abrir el chat siguiente",
    "w": "traspaso-in o traspaso-out",
    "n": "Tras leerlo se mueve a archive/traspasos/. Solo existe entre un chat y otro."
   },
   {
    "p": "traspaso-completo.md",
    "d": 1,
    "q": "¿Qué pasó en el chat anterior, con todo detalle?",
    "r": "Solo si lo pides con /memoria-traspaso",
    "w": "traspaso-in o traspaso-out",
    "n": "El traspaso corto (~1.500 caracteres) se lee solo; este guarda el historial entero y nunca se carga solo."
   },
   {
    "p": "notas-chats/",
    "d": 1,
    "q": "¿Qué hizo un chat auxiliar?",
    "r": "Cuando hay una nota nueva; se avisa solo",
    "w": "El chat que recibió el encargo",
    "n": "Solo aparece cuando hace falta."
   },
   {
    "p": "colaboracion.md",
    "d": 1,
    "q": "¿Qué IA hace qué en este proyecto?",
    "r": "Cuando el modo colaborativo está encendido; los índices la apuntan",
    "w": "colabora.py, desde la plantilla IAS_COLABORATIVAS",
    "n": "Solo existe si has usado /colabora si. Al apagarlo se conserva."
   },
   {
    "p": "archive/",
    "d": 1,
    "q": "¿Se hizo esto? ¿Cuándo?",
    "r": "Solo al consultar; primero hechos-indice.md",
    "w": "La IA y la poda",
    "n": "Lo terminado y probado. Mover, no borrar."
   },
   {
    "p": "pruebas/",
    "d": 1,
    "q": "¿Qué hallazgos dejó una campaña de pruebas?",
    "r": "Cuando toca",
    "w": "La IA, una ficha P-NNN",
    "n": "Cada hallazgo arreglado se marca."
   },
   {
    "p": "lecciones/",
    "d": 1,
    "q": "¿Qué error ya resuelto no debo repetir?",
    "r": "Antes de repetir un trabajo parecido; el arranque cuenta cuántas hay",
    "w": "lecciones.py, lanzada por la IA con /leccion",
    "n": "Un archivo por tema, con «problema | causa | regla»."
   },
   {
    "p": "respuestas/",
    "d": 1,
    "q": "¿Ya guardamos esta respuesta o comparación?",
    "r": "Cuando se busca algo ya resuelto; también con /buscar-en-la-memoria",
    "w": "respuestas.py, lanzado por la IA con /guardar-respuesta",
    "n": "Una respuesta por archivo, con su fuente, y un índice con la más nueva primero."
   },
   {
    "p": "referencias.md",
    "d": 1,
    "q": "¿Qué documentos y hoja de ruta tiene el proyecto?",
    "r": "Solo si toca",
    "w": "La IA",
    "n": "Evita que los índices de entrada engorden."
   },
   {
    "p": "experiencia/",
    "d": 1,
    "q": "¿Qué skills hay y cuándo se usa cada una?",
    "r": "A demanda",
    "w": "Al añadir o quitar una skill",
    "n": "Lista maestra de skills."
   },
   {
    "p": "biblioteca/",
    "d": 1,
    "q": "¿Dónde está el manual y lo reutilizable?",
    "r": "Cuando hace falta",
    "w": "Viene con el arnés",
    "n": "Método, carta maestra, plantillas y kits."
   },
   {
    "p": "guardianes/",
    "d": 1,
    "q": "¿Qué se comprueba automáticamente?",
    "r": "Los ejecuta el sistema, no se leen",
    "w": "Viene con el arnés",
    "n": "Python con la librería estándar. Los ajustes están en guardianes.json."
   },
   {
    "p": ".claude/",
    "d": 0,
    "g": 1,
    "q": "La conexión con Claude Code",
    "r": "Lo usa la herramienta",
    "w": "El instalador",
    "n": "Otras IA no tienen estos ganchos."
   },
   {
    "p": "settings.json",
    "d": 1,
    "q": "¿Qué se lanza en cada momento?",
    "r": "Lo usa Claude Code",
    "w": "El instalador",
    "n": "Declara 4 hooks: abrir sesión, enviar mensaje, antes de cada orden y acabar respuesta."
   },
   {
    "p": "skills/",
    "d": 1,
    "q": "¿Cómo debe actuar la IA en cada situación?",
    "r": "Solo la skill que toca",
    "w": "Viene con el arnés",
    "n": "32 skills en este repositorio."
   },
   {
    "p": "tests/",
    "d": 0,
    "q": "¿Sigue funcionando el método?",
    "r": "Se lanza: python -m unittest discover tests",
    "w": "El arnés",
    "n": "Último pase: 409 pruebas, con 6 saltadas."
   },
   {
    "p": "VERSION y manifiesto.json",
    "d": 0,
    "q": "¿Qué versión es y qué archivos se reparten?",
    "r": "Lo usa el actualizador",
    "w": "generar_manifiesto.py",
    "n": "Solo existen así en el repositorio origen. Una prueba falla si se olvida regenerarlo."
   }
  ],
  "MOM": [
   {
    "t": "Abrir chat",
    "h": "SessionStart",
    "what": "Se lanza arranque.py.",
    "items": [
     "Te resume pendientes, commits sin subir, lo que sigue sin commitear y la última línea del registro.",
     "Muestra el traspaso anterior y lo archiva.",
     "Mueve a archivo la memoria vieja, sin borrarla. Lo pospone si hay cambios sin guardar en esos archivos.",
     "Avisa de secretos, librerías, archivos o índices demasiado grandes y versiones nuevas del arnés."
    ]
   },
   {
    "t": "Enviar mensaje",
    "h": "UserPromptSubmit",
    "what": "Se lanza notas_abiertas.py.",
    "items": [
     "Avisa si otro chat auxiliar dejó una nota nueva."
    ]
   },
   {
    "t": "Acabar respuesta",
    "h": "Stop",
    "what": "Se lanza cierre.py.",
    "items": [
     "Avisa si falta la línea en el registro.",
     "En tareas pequeñas con pruebas en verde, escribe esa línea solo.",
     "Avisa si el chat se alarga: a los 200.000 tokens, y repite cada 100.000."
    ]
   },
   {
    "t": "Hacer commit",
    "h": "Hook pre-commit de Git",
    "what": "Se lanza secretos.py sobre lo que se va a guardar.",
    "items": [
     "Bloquea el commit si encuentra una clave o token de alta confianza. Se aplica con cualquier IA, porque es de Git."
    ]
   },
   {
    "t": "Traspaso de IA",
    "h": "traspaso-out salgo",
    "what": "La skill lanza guardar_traspaso.py.",
    "items": [
     "Hace commit solo de la memoria y lo sube a GitHub.",
     "Se para si hay un secreto. Pregunta antes si hay otros commits sin subir."
    ]
   }
  ],
  "G": [
   {
    "n": "Arranque",
    "f": "arranque.py",
    "w": "Resume el estado real y lanza otras comprobaciones.",
    "c": "Al abrir",
    "e": "Avisa",
    "k": "auto",
    "ek": "warn",
    "d": "Es lo primero que corre al abrir un chat (aviso SessionStart). Lee el estado real —pendientes, commits sin subir, cambios sin commitear, última línea del registro— y lo imprime, para que la IA no dependa de acordarse. Además lanza la poda, avisa de archivos gordos, secretos, librerías, memoria desactualizada y versión nueva del arnés, y muestra el traspaso del chat anterior, que después archiva. Recuerda entre chats los interruptores que estén encendidos: modo fábrica, modo colaborativo y un auditor externo con ajuste no habitual. Si hay proyectos hermanos, dice «N commits de X sin portar». Si todo está en orden, imprime una sola línea."
   },
   {
    "n": "Notas abiertas",
    "f": "notas_abiertas.py",
    "w": "Avisa de notas nuevas de chats auxiliares.",
    "c": "Al enviar",
    "e": "Avisa",
    "k": "auto",
    "ek": "warn",
    "d": "Aviso UserPromptSubmit: cuando envías un mensaje, mira si hay notas nuevas de chats auxiliares en .brain/notas-chats/ que este chat aún no ha recibido y las imprime una vez. No mueve ni borra nada. Sin notas nuevas no imprime nada y no gasta tokens."
   },
   {
    "n": "Aviso de cierre",
    "f": "cierre.py",
    "w": "Recuerda la línea del registro y el tope de pendientes.",
    "c": "Al acabar",
    "e": "Avisa",
    "k": "auto",
    "ek": "warn",
    "d": "Aviso Stop (fin de cada respuesta). Si se tocaron archivos del proyecto y falta la línea en decisions.log, o pendientes.md pasó su tope de 8 KB, devuelve un aviso que la IA lee y corrige; avisa una sola vez por respuesta. Cierra por bloque de trabajo: avisa tras 15 ediciones sin cerrar, o antes si la tarea no pasa la prueba de retomar (otra IA no podría seguir solo con la petición y el git diff). En tareas pequeñas (hasta 2 archivos, ninguno sensible) escribe él mismo la línea. Desde la 1.44 también avisa «lanza el auditor» cuando hubo cambios de código o configuración (no si solo se tocaron documentos o la memoria). Los avisos que solo informan (chat largo, hito sin lección, auditor) se apagan en ese chat si salen 3 veces seguidas sin cambiar nada; el aviso de la línea del registro nunca se apaga. Desde la 1.48 también avisa del efecto en cadena: si se tocó un documento y no el que depende de él, lo recuerda; solo avisa y se apaga en ese chat si se repite."
   },
   {
    "n": "Hitos y lecciones",
    "f": "hitos.py",
    "w": "Obliga a apuntar la lección cuando se resuelve un error o se toca un archivo delicado.",
    "c": "Al acabar",
    "e": "Bloquea",
    "k": "auto",
    "ek": "block",
    "d": "Corre dentro del aviso de cierre. Busca tres señales: un error que se resolvió, cambios en archivos que el proyecto marca como delicados, o una modificación grande (5 o más archivos propios). Si hay alguna, bloquea el cierre hasta que se apunte la lección con /leccion o se diga «ninguna» con su motivo."
   },
   {
    "n": "Longitud",
    "f": "longitud.py",
    "w": "Avisa de que el chat se ha alargado.",
    "c": "Al acabar",
    "e": "Avisa",
    "k": "auto",
    "ek": "warn",
    "d": "Mide el contexto real del último mensaje de la IA (entrada + caché). Al pasar 200.000 tokens avisa de que conviene abrir un chat nuevo y deja lista la frase de traspaso; repite cada 100.000 más. Un chat largo cuesta más en cada mensaje, así que cortarlo a tiempo ahorra."
   },
   {
    "n": "Secretos",
    "f": "secretos.py",
    "w": "Busca claves y tokens. También puede revisar el historial.",
    "c": "Al abrir y en cada commit",
    "e": "Bloquea",
    "k": "auto",
    "ek": "block",
    "d": "Busca claves y tokens con patrones de alta confianza (formato real de token) y de baja (asignaciones sospechosas), y archivos secretos que deben estar ignorados por Git. Al abrir revisa el proyecto; en cada commit (hook pre-commit) revisa lo preparado y bloquea el commit si hay un secreto."
   },
   {
    "n": "Poda",
    "f": "poda.py",
    "w": "Mueve a archivo la memoria vieja. Nunca borra.",
    "c": "Al abrir",
    "e": "Actúa",
    "k": "auto",
    "ek": "act",
    "d": "Mueve a archivo/ las specs ya terminadas y las fichas de decisión «reemplazada», reescribe los enlaces de los .md que las citan y mantiene un índice de una línea por spec. Nunca borra y, ante la duda, no mueve. A mano: poda.py --ver enseña qué haría sin tocar nada."
   },
   {
    "n": "Git del traspaso",
    "f": "guardar_traspaso.py",
    "w": "Hace commit de la memoria y lo sube.",
    "c": "En traspaso-out salgo",
    "e": "Actúa",
    "k": "auto",
    "ek": "act",
    "d": "Lo llama traspaso-out salgo. Hace commit solo de la memoria (traspaso, registro, pendientes, specs) y la sube. El código suelto no entra: lo lista para que decidas. Nunca fuerza la subida; si hay otros commits sin subir que no son de memoria, no sube y los lista. Es la única excepción a «subir a GitHub solo con tu orden»."
   },
   {
    "n": "Librerías",
    "f": "librerias.py",
    "w": "Vigila versiones. Al abrir solo lee el último resultado; la consulta por internet se lanza aparte.",
    "c": "Al abrir / a mano",
    "e": "Avisa",
    "k": "auto",
    "ek": "warn",
    "d": "Lee la lista de librerías del proyecto y la compara con OSV.dev, una base pública de vulnerabilidades conocidas. Entiende cuatro mundos: Python (requirements.txt), JavaScript con npm (package-lock.json), Rust con cargo (Cargo.lock) y Go (go.mod). Esos archivos fijan la versión exacta de cada librería, así que el aviso es preciso: «lodash 4.17.15 tiene 5 vulnerabilidades, corregidas en 4.17.21». Solo para Python mira además si hay una versión mayor nueva en PyPI. Si el proyecto no tiene ninguno de esos archivos, calla. Guarda el resultado y el arranque solo lo lee, sin red. Si falla internet, conserva el resultado anterior y no bloquea nada. Solo avisa: nunca actualiza ni instala nada. Probado de verdad contra OSV.dev con un proyecto de juguete: detectó las tres librerías vulnerables (npm, cargo y Go)."
   },
   {
    "n": "Memoria del chat",
    "f": "eventos_chat.py",
    "w": "Recuerda qué librerías se instalan en el chat y, en el git push, detiene la subida si alguna tiene un fallo conocido.",
    "c": "Antes de cada orden",
    "e": "Bloquea",
    "k": "auto",
    "ek": "block",
    "d": "Aviso PreToolUse (antes de cada orden de terminal o edición). Recuerda, por chat, qué librerías se instalaron (con pip, npm, cargo o go) y, al ver un git push, las revisa con OSV.dev: limpio → deja pasar; vulnerabilidad conocida → detiene el push y lo explica; sin red → no bloquea y lo recuerda. No depende de la IA ni de ti."
   },
   {
    "n": "Memoria de pruebas",
    "f": "pruebas.py",
    "w": "Sigue las campañas de pruebas y sus hallazgos.",
    "c": "Al abrir",
    "e": "Avisa",
    "k": "auto",
    "ek": "warn",
    "d": "Cuenta los hallazgos abiertos (casillas - [ ]) de las campañas de .brain/pruebas/ y comprueba que el índice coincide con los archivos. Solo imprime una línea si hay algo abierto o incoherente: con todo cerrado cuesta 0 tokens."
   },
   {
    "n": "Revisión de índices",
    "f": "revisar_indices.py",
    "w": "Busca referencias rotas y deriva en CLAUDE.md, GEMINI.md y AGENTS.md.",
    "c": "Al abrir / a mano",
    "e": "Avisa",
    "k": "auto",
    "ek": "warn",
    "d": "Revisa CLAUDE.md, GEMINI.md y AGENTS.md y saca un informe de lo que parece sobrar o estar desfasado: referencias rotas, deriva entre índices, secciones largas y cercanía al tope. Desde la 1.36 también detecta memoria desactualizada en pendientes.md y constitution.md (rutas, specs y fichas que ya no existen). No modifica nada. Avisa a los 60 días de la última revisión o cuando un índice llega al 80 % de su tope; los descartes que le dices se recuerdan."
   },
   {
    "n": "Archivos gordos",
    "f": "archivos_gordos.py",
    "w": "Avisa cuando un archivo de memoria se acerca a su tope de 8 KB.",
    "c": "Al abrir / a mano",
    "e": "Avisa",
    "k": "auto",
    "ek": "warn",
    "d": "Los índices de IA y pendientes.md tienen su tope; los demás archivos de lectura de .brain/ (referencias, constitución, architecture/, decisions/…) tienen un tope de 8 KB. Avisa al 80 % y propone /trocea. Solo lectura."
   },
   {
    "n": "Cierre rápido",
    "f": "cerrar.py",
    "w": "Añade la línea del registro con su formato correcto.",
    "c": "A mano o por la IA",
    "e": "Actúa",
    "k": "mano",
    "ek": "act",
    "d": "Añade la línea de la tarea a decisions.log con el formato correcto: python .brain/guardianes/cerrar.py --chat «Proyecto #N» «qué se hizo». Con --carril elige Cambio pequeño (por defecto) o SDD. Es el cierre de una línea: no obliga a tocar pendientes ni fichas salvo que corresponda. Desde la 1.47 acepta --tipo (arnes, leccion, decision, spec, pendiente, memoria, otro) para etiquetar la línea del registro."
   },
   {
    "n": "Medidor",
    "f": "medir.py",
    "w": "Muestra por chat el coste y las correcciones. Solo lee.",
    "c": "A mano",
    "e": "Solo lee",
    "k": "mano",
    "ek": "ok",
    "d": "Solo lectura. Lee los registros de Claude Code y, por chat, saca coste ponderado, tokens nuevos, salida, arranque, mensajes tuyos y correcciones, y los tokens por tarea terminada. --comparar enfrenta dos proyectos, --desglose ID da el coste mensaje a mensaje, --ritual separa cuánto del coste es ritual del arnés y cuánto es trabajo (y mide la prueba de retomar). Con --fabrica suma el gasto de la directora (sus chats, sin caché) y el de las sesiones de Codex por encargo de la fábrica; no cuenta los subagentes de Claude, que no tienen registro propio."
   },
   {
    "n": "Fábrica de IA",
    "f": "fabrica.py",
    "w": "Sella la spec y la carta, comprueba el alcance de cada encargo, vigila el gasto y recuerda el modo fábrica.",
    "c": "A mano (lo lanza la directora)",
    "e": "Avisa",
    "k": "mano",
    "ek": "warn",
    "d": "Sin IA, solo comprobaciones. Lo usa la directora entre un paso y otro; no es un hook ni vigila en vivo. Congela la spec aprobada y sella la carta, saca una foto de la carpeta de trabajo antes de que trabaje la ejecutora, comprueba que el encargo tiene su requisito y que solo se tocaron los archivos permitidos, anota el gasto de cada papel y lo compara con los topes de la carta. Con «fabrica.py modo si|no|estado» (o /fabrica) enciende el modo fábrica, que se recuerda entre chats. Si algo incumple, sale con error para parar y avisarte."
   },
   {
    "n": "Auditor",
    "f": "auditor.py",
    "w": "Dice quién audita (interno y/o IA externa), da el comando de Codex y guarda los ajustes. No lanza ninguna IA.",
    "k": "mano",
    "ek": "ok",
    "d": "Spec 044 (1.44). Busca fallos de calidad, consumo y seguridad y solo avisa: nunca cambia código ni bloquea el cierre. Este guardián no audita: guarda los ajustes en guardianes.json (auditor_cierre, auditor_externo, modelos y esfuerzo) y responde a «quien general|cierre|spec» con quién debe auditar (siempre el interno; la IA externa Codex en revisión general y cierre de spec, y en cierres rutinarios solo con auditor_externo en «siempre»; con «no», nunca). «codex» imprime el comando de Codex en solo lectura (en Windows con windows.sandbox=\"unelevated\", o Codex no puede ejecutar python). Si guardianes.json está roto no lo pisa, y los valores que entran en el comando se validan. Lo lanza la IA con la skill /auditor; cierre.py solo recuerda hacerlo.",
    "c": "A mano",
    "e": "Solo lee"
   },
   {
    "n": "Modo colaborativo",
    "f": "colabora.py",
    "w": "Enciende o apaga el trabajo de varias IA con papeles distintos en un proyecto.",
    "k": "mano",
    "ek": "ok",
    "d": "Spec 042 (1.42). «colabora.py si» enciende modo_colaborativo, crea .brain/colaboracion.md desde la plantilla IAS_COLABORATIVAS (quién hace qué: Claude, Codex, Gemini) y pone una sola línea que remite a ese archivo en CLAUDE.md, AGENTS.md y GEMINI.md (salvo los que figuren en indices_ajenos). «no» lo apaga y quita esas líneas, pero conserva colaboracion.md. «estado» solo muestra cómo está. El arranque lo recuerda entre chats. No abre ningún chat.",
    "c": "A mano",
    "e": "Solo lee"
   },
   {
    "n": "Proyectos hermanos",
    "f": "hermanos.py",
    "w": "Dice cuántos commits de un proyecto hermano faltan por portar a este.",
    "k": "auto",
    "ek": "warn",
    "d": "Spec 043 (1.43). Solo lectura. Con proyectos_hermanos en guardianes.json (nombre, ruta, rama y archivo_portar) compara los commits del hermano con el archivo de portar de este proyecto (secciones «Último portado», «Pendiente» y «Hecho») y el arranque avisa «N commits de X sin portar». No hace fetch ni cambia nada; si el hermano no es accesible, calla (solo el comando manual lo dice). Sin hermanos configurados, no dice nada.",
    "c": "Al abrir / a mano",
    "e": "Avisa"
   },
   {
    "n": "Actualizador",
    "f": "actualizar_arnes.py",
    "w": "Trae las mejoras al proyecto, con copia de seguridad.",
    "c": "A mano o con /actualizar",
    "e": "Actúa",
    "k": "mano",
    "ek": "act",
    "d": "Trae a un proyecto las mejoras del arnés (guardianes, skills, manual, kits, pruebas del método) comparando las huellas del manifiesto. --simular enseña qué cambiaría sin tocar nada; guarda copia; no pisa lo modificado a mano ni toca datos ni configuración."
   },
   {
    "n": "Análisis de código",
    "f": "analisis.py",
    "w": "Revisa el código con reglas como funciones demasiado largas.",
    "c": "Apagado aquí",
    "e": "Apagado",
    "k": "off",
    "ek": "off",
    "d": "Lee la estructura del código Python y avisa de tres cosas: SQL inseguro (consultas armadas con texto), funciones o archivos que crecen respecto a su base guardada, y reglas propias del proyecto. Apagado aquí; se activa en proyectos con código."
   },
   {
    "n": "Base de datos",
    "f": "base_datos.py",
    "w": "Defiende una base de datos SQLite con copias y reglas.",
    "c": "Apagado aquí",
    "e": "Apagado",
    "k": "off",
    "ek": "off",
    "d": "Copia consistente de SQLite antes de cambiar tablas (con rotación), revisión de salud en solo lectura y restauración solo con orden expresa. Apagado aquí; se activa en proyectos con base de datos."
   },
   {
    "n": "Lecciones",
    "f": "lecciones.py",
    "w": "Guarda cada lección aprendida y rehace su índice.",
    "c": "Al resolver un hito",
    "e": "Actúa",
    "k": "mano",
    "ek": "act",
    "d": "Guarda cada lección en .brain/lecciones/<tema>.md con la forma «problema | causa | regla» y rehace el índice. La lanza la IA con /leccion cuando el guardián de hitos lo pide; el arranque resume cuántas hay. Es lo que hace que un error ya resuelto no se repita."
   },
   {
    "n": "Índices del cierre",
    "f": "indices.py",
    "w": "Evita trabajo repetido al cerrar una tarea.",
    "c": "Dentro del cierre rápido",
    "e": "Actúa",
    "k": "mano",
    "ek": "act",
    "d": "Lo usa cerrar.py: añade a decisions/indice.md las filas de las fichas D-NNN que faltan (nunca borra ni cambia filas) y mueve un punto terminado de pendientes.md a archive/hechos.md con su fila en el índice. Devuelve los textos y quien lo llama decide si escribe: así existe la vista previa."
   },
   {
    "n": "Diapositivas",
    "f": "diapositivas.py",
    "w": "Convierte un tema o un documento en una presentación .html.",
    "c": "A mano (/diapositivas)",
    "e": "Solo lee",
    "k": "mano",
    "ek": "ok",
    "d": "Genera un .html autocontenido (sin internet ni librerías) a partir de un tema (resumen, version, traspaso, auditoria) o de un documento entero. El texto del .md se escapa, solo hay enlaces http(s) o relativos y una política impide cargar nada de fuera. Con --buscar NOMBRE localiza el documento y con --comprobar compara el original con las diapositivas. Los .html no se suben a Git."
   },
   {
    "n": "Diagramas",
    "f": "diagramas.py",
    "w": "Dibuja los bloques mermaid de las diapositivas como imagen.",
    "c": "Lo usa diapositivas.py",
    "e": "Solo lee",
    "k": "mano",
    "ek": "ok",
    "d": "Entiende flowchart (cajas, rombos, flechas con etiqueta, punteadas y gruesas) y sequenceDiagram, y los dibuja como SVG dentro del .html, sin internet. Si el tipo no se soporta o el dibujo es demasiado grande, deja el texto y el script avisa en español e inglés."
   },
   {
    "n": "Respuestas guardadas",
    "f": "respuestas.py",
    "w": "Archiva una respuesta útil de un chat con su fuente.",
    "c": "A mano o por la IA (/guardar-respuesta)",
    "e": "Actúa",
    "k": "mano",
    "ek": "act",
    "d": "Guarda la respuesta en .brain/respuestas/AAAA-MM-DD-titulo.md y genera indice.md (la más nueva primero). No pisa una con el mismo título y fecha, exige título y fuente, tiene un tope de 8 KB y admite el texto por la entrada estándar para no usar heredocs."
   },
   {
    "n": "Revisión de contenido",
    "f": "revisar_contenido.py",
    "w": "Avisa de páginas huérfanas, frases ya falsas y topes contradictorios en .brain/.",
    "c": "Al abrir (una línea) / a mano",
    "e": "Avisa",
    "k": "auto",
    "ek": "warn",
    "d": "Solo lectura, nunca bloquea. El arranque da una línea si hay hallazgos y han pasado revision_contenido_dias (30 por defecto; se apaga con revision_contenido_activa). La skill /revisar-contenido hace «buscar y refutar» con otra IA nueva, sin el contexto de la primera, y lo descartado queda en revision_contenido.json."
   },
   {
    "n": "Búsqueda en la memoria",
    "f": "buscar.py",
    "w": "Responde con los mejores archivos de .brain/ para unas palabras.",
    "c": "A mano (/buscar-en-la-memoria)",
    "e": "Solo lee",
    "k": "mano",
    "ek": "ok",
    "d": "Recorre lecciones, decisiones, specs, respuestas y registro en cada consulta, sin índice: unos 470 KB tardan milisegundos. Ignora tildes, mayúsculas y palabras vacías, da más peso al título y a los encabezados y limita lo que suma un archivo largo por repetirse. Con --archivo incluye archive/. Umbral para pasar a un índice: 5 MB o más de 1 segundo."
   },
   {
    "n": "Textos en dos idiomas",
    "f": "textos.py",
    "w": "Guarda los mensajes de todos los guardianes en español e inglés.",
    "c": "Siempre (lo usan los demás)",
    "e": "Solo lee",
    "k": "auto",
    "ek": "ok",
    "d": "El idioma sale del ajuste «idioma» de guardianes.json (si falta, español, así los proyectos antiguos no cambian). Los nombres de archivos y comandos siguen en español en los dos idiomas. Una prueba avisa si a un idioma le falta una clave."
   }
  ],
  "SK": [
   [
    "Tus comandos",
    [
     "resumen",
     "pendiente",
     "prompt-inicial",
     "actualizar",
     "version",
     "subir-a-github"
    ]
   ],
   [
    "Cambiar de chat o de IA",
    [
     "traspaso-in",
     "traspaso-out",
     "chat-nuevo",
     "memoria-traspaso"
    ]
   ],
   [
    "Adoptar y ordenar proyectos antiguos",
    [
     "adopta",
     "adoptar-indice-existente",
     "acorta",
     "trocea",
     "revisar-indices-de-ia"
    ]
   ],
   [
    "Cerrar bien el trabajo",
    [
     "cerrar-una-tarea",
     "implementada-no-es-hecha",
     "pendientes-solo-lo-que-falta",
     "mover-no-borrar",
     "spec-antes-de-programar",
     "leccion"
    ]
   ],
   [
    "Evitar errores técnicos",
    [
     "secretos-fuera-del-repo",
     "vigilar-librerias",
     "licencia-antes-de-usar",
     "cero-dependencias",
     "quitar-codigo-antiguo-con-test"
    ]
   ],
   [
    "Construir guardianes y hablar claro",
    [
     "guardian-avisa-o-bloquea",
     "probar-guardian-en-windows",
     "explicar-a-darwin-en-llano"
    ]
   ],
   [
    "Sistemas reales",
    [
     "seguridad-en-sistemas-reales"
    ]
   ],
   [
    "La fábrica de IA",
    [
     "directora-de-fabrica",
     "revisor-independiente",
     "fabrica",
     "revisor-de-consumo"
    ]
   ],
   [
    "Auditar y trabajar en equipo",
    [
     "auditor",
     "colabora",
     "hermanos"
    ]
   ],
   [
    "Memoria y presentaciones",
    [
     "diapositivas",
     "guardar-respuesta",
     "revisar-contenido",
     "buscar-en-la-memoria"
    ]
   ]
  ],
  "GL": [
   [
    "Actualizador",
    "Programa que lleva las mejoras del arnés a un proyecto, sin pisar lo tuyo."
   ],
   [
    "Aprobador",
    "Agente aparte que lee una spec y dice APROBADA o RECHAZADA con una regla fija; en el experimento VMware hacía de Darwin."
   ],
   [
    "Archivo",
    "Carpeta donde va lo terminado o viejo. Se mueve allí, no se borra."
   ],
   [
    "Arnés",
    "Todo lo que rodea a la IA para que trabaje bien: método, guardianes, skills y pruebas."
   ],
   [
    "Arranque",
    "Resumen automático del estado del proyecto al abrir un chat."
   ],
   [
    "Auditor",
    "IA que intenta demostrar que un trabajo falla (calidad, consumo, seguridad) y entrega un informe. Solo avisa: no cambia nada ni bloquea. Hay uno interno (Sonnet) y, si toca, uno externo (Codex)."
   ],
   [
    "Bloquear",
    "Impedir una acción, como un commit con una clave. Es más fuerte que avisar."
   ],
   [
    "Cambio pequeño",
    "Carril corto, para tareas pequeñas."
   ],
   [
    "Carril",
    "Camino de un encargo: con spec o rápido."
   ],
   [
    "Carta",
    "Reglas del juego de una misión de la fábrica, firmadas por Darwin: qué se puede tocar, qué está prohibido y cuánto se puede gastar."
   ],
   [
    "CI/CD",
    "Automatización que lanza pruebas y despliegues en cada subida. Aún no la tenemos."
   ],
   [
    "Commit",
    "Foto de los cambios guardada en el historial de Git. Solo es local hasta que se sube."
   ],
   [
    "Constitución",
    "Reglas del proyecto que no se saltan sin permiso."
   ],
   [
    "Decisión (D-NNN)",
    "Ficha corta que guarda qué se decidió y por qué."
   ],
   [
    "Directora",
    "Diseño: agente principal de un proyecto (Opus) que convierte tu objetivo en una spec y reparte encargos. No programa."
   ],
   [
    "Ejecutora",
    "IA que hace un encargo pequeño dentro de los archivos permitidos (Claude, Codex o Gemini)."
   ],
   [
    "Encargo",
    "Tarea pequeña de la fábrica: requisito que cumple, archivos permitidos y prueba que la da por buena."
   ],
   [
    "Fallos plantados",
    "Prueba del auditor: se esconden fallos conocidos en un código de juguete y se cuenta cuántos encuentra cada auditor."
   ],
   [
    "Fábrica de IA",
    "Diseño (spec 035), ya construido (1.31 a 1.44): trabajar con varias IA con papeles distintos, límites vigilados por programas y tres puertas de aprobación tuyas. Se enciende con /fabrica si."
   ],
   [
    "Git",
    "Sistema que guarda el historial de cambios de un proyecto."
   ],
   [
    "Guardián",
    "Script que comprueba solo que el método se cumple."
   ],
   [
    "Hook (gancho)",
    "Orden que se lanza sola cuando pasa algo, como abrir un chat."
   ],
   [
    "Manifiesto",
    "Lista de los archivos del arnés con su huella, para saber si cambiaron."
   ],
   [
    "Meta-arnés",
    "Arnés que sirve para muchos proyectos, repartido desde un solo origen."
   ],
   [
    "Modo colaborativo",
    "Interruptor (/colabora) para que varias IA trabajen en el mismo proyecto con papeles distintos, según .brain/colaboracion.md."
   ],
   [
    "Modo ligero",
    "Cierre abreviado para tareas pequeñas con pruebas en verde."
   ],
   [
    "Nivel",
    "Cuánto del método se instala en un proyecto: ligero, medio o completo."
   ],
   [
    "Nota de chat",
    "Lo que deja un chat auxiliar para quien le hizo el encargo."
   ],
   [
    "ODD",
    "Método ligero de comparación: las tareas pequeñas van directas y las grandes llevan un documento de tareas; sin guardianes."
   ],
   [
    "Pendientes",
    "Lista de lo que falta. Solo eso."
   ],
   [
    "Poda",
    "Limpieza que mueve memoria vieja al archivo."
   ],
   [
    "Pre-commit",
    "Hook de Git que se lanza justo antes de guardar un commit."
   ],
   [
    "Proyectos hermanos",
    "Proyectos que salen del mismo origen con otra variante. El arnés avisa de los commits del hermano que faltan por portar."
   ],
   [
    "Prueba (test)",
    "Comprobación automática de que algo sigue funcionando."
   ],
   [
    "Prueba de retomar",
    "Pregunta que decide si hace falta spec: ¿otra IA puede continuar solo con el encargo y el git diff? Si sí, vía rápida."
   ],
   [
    "Push",
    "Enviar los commits a GitHub."
   ],
   [
    "Registro",
    "El archivo decisions.log: una línea por tarea terminada."
   ],
   [
    "Reglas de seguridad",
    "Seis reglas para proyectos que actúan sobre sistemas reales (skill seguridad-en-sistemas-reales): todo por el motor, fallar hacia lo seguro, no depender del laboratorio y más."
   ],
   [
    "Revisor independiente",
    "Otra IA, en otro chat, que no hizo el trabajo y lo revisa con ojos nuevos: nadie aprueba su propio trabajo."
   ],
   [
    "Secreto",
    "Clave o token que nunca debe entrar en el repositorio."
   ],
   [
    "Skill",
    "Ficha de instrucciones para una situación concreta."
   ],
   [
    "Spec",
    "Plan corto que apruebas antes de programar."
   ],
   [
    "Subagente",
    "IA que lanza otra IA para una tarea acotada y recibe solo su informe. Se usa de revisor y de auditor interno, siempre de solo lectura."
   ],
   [
    "Token",
    "Unidad con la que se mide y se cobra lo que la IA lee y escribe."
   ],
   [
    "Traspaso",
    "Archivo que pasa el contexto de un chat o de una IA a otra."
   ],
   [
    "vcsim",
    "Simulador de VMware (necesita Go) que se usaría para probar contra algo más real que el laboratorio en memoria. Aún no instalado."
   ],
   [
    "Versión",
    "Número del arnés. Sube con cada cambio repartido."
   ],
   [
    "Índice de entrada",
    "Archivo corto que lee la IA primero: CLAUDE.md, GEMINI.md o AGENTS.md."
   ]
  ],
  "T": [
   {
    "c": "Cada día",
    "t": "Saber cómo va el proyecto",
    "w": "En el chat",
    "x": "/resumen",
    "d": "Cuenta el estado en pocas viñetas, sin escribir nada."
   },
   {
    "c": "Cada día",
    "t": "Ver lo que falta",
    "w": "En el chat",
    "x": "/pendiente",
    "d": "Te deja elegir entre programar, tu prueba, tus acciones o specs. También vale /pendiente programar."
   },
   {
    "c": "Cada día",
    "t": "Empezar un encargo bien explicado",
    "w": "En el chat",
    "x": "/prompt-inicial",
    "d": "Te ayuda a escribir el objetivo, los límites y qué debes probar."
   },
   {
    "c": "Cada día",
    "t": "Confirmar que probaste algo",
    "w": "En el chat",
    "x": "Probé el punto N y funciona",
    "d": "La IA lo pasa de pendientes a hechos en esa misma respuesta."
   },
   {
    "c": "Cada día",
    "t": "Cerrar una tarea a mano",
    "w": "En la terminal",
    "x": "python .brain/guardianes/cerrar.py --chat \"Proyecto #N\" \"qué se hizo\"",
    "d": "Normalmente lo hace la IA."
   },
   {
    "c": "Chats e IA",
    "t": "Pasar a un chat nuevo con la misma IA",
    "w": "En el chat",
    "x": "/traspaso-in salgo",
    "d": "Escribe el traspaso y abre el chat nuevo. En Codex, $traspaso-in salgo."
   },
   {
    "c": "Chats e IA",
    "t": "Entrar en el chat nuevo",
    "w": "En el chat nuevo",
    "x": "/traspaso-in entro",
    "d": "Cuenta lo anterior en 4-5 viñetas. Claude lo muestra solo al abrir."
   },
   {
    "c": "Chats e IA",
    "t": "Irte de esta IA a otra",
    "w": "En el chat",
    "x": "/traspaso-out salgo",
    "d": "Escribe el traspaso, hace commit de la memoria y lo sube a GitHub."
   },
   {
    "c": "Chats e IA",
    "t": "Llegar a la otra IA",
    "w": "En la otra IA",
    "x": "/traspaso-out entro",
    "d": "Si Gemini no reconoce la skill, pídele que lea GEMINI.md, .brain/traspaso.md y .brain/pendientes.md."
   },
   {
    "c": "GitHub",
    "t": "Subir a GitHub",
    "w": "En el chat",
    "x": "sube",
    "d": "La skill repasa secretos y pruebas antes de subir."
   },
   {
    "c": "GitHub",
    "t": "Buscar claves antes de publicar",
    "w": "En la terminal",
    "x": "python .brain/guardianes/secretos.py",
    "d": "Añade --historial para revisar también lo ya guardado en Git."
   },
   {
    "c": "Proyectos",
    "t": "Instalar en un proyecto nuevo",
    "w": "En la terminal, desde cerebro-vivo",
    "x": "python .brain/biblioteca/kit-arranque/instalar.py RUTA --nombre Nombre --dueno Darwin --nivel completo",
    "d": "También hay doble clic en instalar_kit.bat. Niveles: ligero, medio y completo."
   },
   {
    "c": "Proyectos",
    "t": "Comprobar un proyecto instalado",
    "w": "En la terminal, desde cerebro-vivo",
    "x": "python .brain/biblioteca/kit-arranque/instalar.py RUTA --comprobar",
    "d": "Dice qué piezas están y cuáles faltan."
   },
   {
    "c": "Proyectos",
    "t": "Adoptar un proyecto con un CLAUDE.md antiguo",
    "w": "En el chat",
    "x": "/adopta",
    "d": "Encadena los pasos de reparto, acortar y trocear, y te pide el sí en cada tabla."
   },
   {
    "c": "Proyectos",
    "t": "Actualizar un proyecto (lo fácil)",
    "w": "En el chat del proyecto",
    "x": "/actualizar",
    "d": "Te cuenta qué trae, te pide el sí y lo hace todo."
   },
   {
    "c": "Proyectos",
    "t": "Ver la versión del arnés de un proyecto",
    "w": "En el chat del proyecto",
    "x": "/version",
    "d": "Dice la versión instalada, si hay una más nueva y cómo actualizar. No cambia nada. Llega con la 1.21.0."
   },
   {
    "c": "Proyectos",
    "t": "Si /actualizar no existe (1): ver qué hará",
    "w": "En la terminal, dentro del proyecto",
    "x": "python .brain/guardianes/actualizar_arnes.py --simular",
    "d": "Pasa en proyectos anteriores a la 1.17.0. No escribe nada. Luego, el paso 2."
   },
   {
    "c": "Proyectos",
    "t": "Si /actualizar no existe (2): aplicarlo",
    "w": "En la terminal, dentro del proyecto",
    "x": "python .brain/guardianes/actualizar_arnes.py",
    "d": "Guarda copia en .brain/copias_arnes/, no pisa lo modificado y pasa las pruebas. Después ya tendrás /actualizar y /version."
   },
   {
    "c": "Proyectos",
    "t": "Ver qué traería una actualización",
    "w": "En la terminal, desde cerebro-vivo",
    "x": "python actualizar.py RUTA --simular",
    "d": "No escribe nada. Conviene hacerlo siempre primero."
   },
   {
    "c": "Proyectos",
    "t": "Actualizar un proyecto (a mano)",
    "w": "En la terminal, desde cerebro-vivo",
    "x": "python actualizar.py RUTA",
    "d": "Guarda copia en .brain/copias_arnes/ y no pisa lo modificado."
   },
   {
    "c": "Mantenimiento",
    "t": "Revisar los índices de IA",
    "w": "En el chat",
    "x": "revisa los índices",
    "d": "Hace doble pasada y mueve lo retirado con tu visto bueno."
   },
   {
    "c": "Mantenimiento",
    "t": "Acortar un índice demasiado grande",
    "w": "En el chat",
    "x": "/acorta",
    "d": "Baja CLAUDE.md, GEMINI.md y AGENTS.md al tope de 5 KB."
   },
   {
    "c": "Mantenimiento",
    "t": "Dividir un archivo de memoria gordo",
    "w": "En el chat",
    "x": "/trocea",
    "d": "Lo divide por temas con nombre y guarda la copia íntegra."
   },
   {
    "c": "Mantenimiento",
    "t": "Lanzar las pruebas",
    "w": "En la terminal",
    "x": "python -m unittest discover tests",
    "d": "Tras cualquier cambio."
   },
   {
    "c": "Mantenimiento",
    "t": "Medir chats",
    "w": "En la terminal",
    "x": "python .brain/guardianes/medir.py",
    "d": "Muestra coste y correcciones. Solo lee."
   },
   {
    "c": "Mantenimiento",
    "t": "Repartir un cambio del arnés",
    "w": "En la terminal, en cerebro-vivo",
    "x": "python generar_manifiesto.py",
    "d": "Antes sube VERSION y anota CAMBIOS.md. Después lanza las pruebas."
   },
   {
    "c": "Si algo falla",
    "t": "No sale el resumen al abrir",
    "w": "En la terminal, o pídeselo a la IA",
    "x": "python .brain/guardianes/arranque.py --manual",
    "d": "Sirve también en Gemini y Codex."
   },
   {
    "c": "Si algo falla",
    "t": "Un aviso se repite o molesta",
    "w": "En el chat",
    "x": "Este aviso me molesta, revisa guardianes.json",
    "d": "Los topes están en .brain/guardianes/guardianes.json."
   },
   {
    "c": "Mantenimiento",
    "t": "Saber cuánto cuesta cada chat",
    "w": "En la terminal",
    "x": "python .brain/guardianes/medir.py",
    "d": "Tabla por chat: coste ponderado, tokens nuevos, salida y arranque. Solo lee, no cambia nada."
   },
   {
    "c": "Mantenimiento",
    "t": "Saber cuánto del coste es ritual del arnés",
    "w": "En la terminal",
    "x": "python .brain/guardianes/medir.py --ritual",
    "d": "Separa el coste en trabajo, memoria, chat nuevo, avisos del guardián y mantenimiento del arnés."
   },
   {
    "c": "Fábrica de IA",
    "t": "Dirigir una fábrica de IA",
    "w": "En el chat",
    "x": "/directora-de-fabrica",
    "d": "La IA actúa de directora: escribe la spec y los encargos y te pide el visto bueno en cada puerta. Otras IA ejecutan."
   },
   {
    "c": "Fábrica de IA",
    "t": "Revisar un trabajo con ojos nuevos",
    "w": "En un chat aparte",
    "x": "/revisor-independiente",
    "d": "Otra IA, que no hizo el trabajo, lo revisa contra el encargo. Nadie aprueba su propio trabajo."
   },
   {
    "c": "Fábrica de IA",
    "t": "Comprobar el gasto y los topes de la fábrica",
    "w": "En la terminal, en el proyecto",
    "x": "python .brain/guardianes/fabrica.py topes --encargo N",
    "d": "Compara el gasto anotado con los topes de la carta. Sale con error si alguno se pasa."
   },
   {
    "c": "Fábrica de IA",
    "t": "Medir el gasto de Codex por encargo",
    "w": "En la terminal",
    "x": "python .brain/guardianes/medir.py --fabrica --proyecto RUTA",
    "d": "Suma los tokens gastados por cada sesión de Codex, agrupados por carpeta de encargo. Solo lee."
   },
   {
    "c": "Fábrica de IA",
    "t": "Encender el modo fábrica",
    "w": "En el chat",
    "x": "/fabrica si",
    "d": "La IA pasa a ser directora: no programa, escribe la spec y reparte encargos. Abre sola un chat nuevo con Opus en esfuerzo medio. Se recuerda entre chats."
   },
   {
    "c": "Fábrica de IA",
    "t": "Apagar el modo fábrica / ver cómo está",
    "w": "En el chat",
    "x": "/fabrica no",
    "d": "Vuelve al modo normal. Con /fabrica estado solo te dice cómo está."
   },
   {
    "c": "Fábrica de IA",
    "t": "Revisar el consumo de un módulo",
    "w": "En el chat",
    "x": "/revisor-de-consumo",
    "d": "Un subagente de solo lectura busca gasto de CPU, memoria, disco o red de más al terminar un módulo de la fábrica."
   },
   {
    "c": "Varias IA",
    "t": "Encender el trabajo de varias IA en un proyecto",
    "w": "En el chat",
    "x": "/colabora si",
    "d": "Crea .brain/colaboracion.md (quién hace qué: Claude, Codex, Gemini) y una línea que lo apunta en los índices de cada IA. Se recuerda entre chats."
   },
   {
    "c": "Varias IA",
    "t": "Apagarlo / ver cómo está",
    "w": "En el chat",
    "x": "/colabora no",
    "d": "Lo apaga y quita las líneas; colaboracion.md se conserva. Con /colabora estado solo lo muestra."
   },
   {
    "c": "Varias IA",
    "t": "Saber qué falta por portar de un proyecto hermano",
    "w": "En la terminal",
    "x": "python .brain/guardianes/hermanos.py",
    "d": "Solo lectura: lista los commits del hermano que aún no están en tu archivo de portar. El arranque ya lo avisa solo."
   },
   {
    "c": "Varias IA",
    "t": "Preparar o adoptar el archivo de portar",
    "w": "En el chat",
    "x": "/hermanos",
    "d": "Te guía para configurar proyectos_hermanos y crear el archivo de portar desde la plantilla."
   },
   {
    "c": "Auditar",
    "t": "Auditar todo el proyecto (o una carpeta)",
    "w": "En el chat",
    "x": "/auditor general",
    "d": "Dos auditores independientes —uno interno y Codex— buscan fallos de calidad, consumo y seguridad y entregan un informe único. Solo avisa; no cambia nada."
   },
   {
    "c": "Auditar",
    "t": "Auditar lo cambiado en esta tarea",
    "w": "En el chat",
    "x": "/auditor cierre",
    "d": "Lo mismo, pero solo sobre lo que cambió. Lo usa la IA cuando el cierre dice «lanza el auditor»."
   },
   {
    "c": "Auditar",
    "t": "Encender o apagar el aviso de cierre",
    "w": "En el chat",
    "x": "/auditor cierre no",
    "d": "Con «si» vuelve a avisar tras cambios de código o configuración. Con «estado» solo lo muestra."
   },
   {
    "c": "Auditar",
    "t": "Elegir cuándo entra la IA externa (Codex)",
    "w": "En el chat",
    "x": "/auditor externo general-y-spec",
    "d": "Valores: general-y-spec (por defecto), siempre (también en cierres rutinarios, más gasto) y no (nunca se llama a una IA externa)."
   },
   {
    "c": "Auditar",
    "t": "Ver quién audita y el comando de Codex",
    "w": "En la terminal",
    "x": "python .brain/guardianes/auditor.py quien general",
    "d": "Dice «interno + externo» o solo «interno». Con «codex» en lugar de «quien…» imprime el comando exacto de Codex en solo lectura."
   },
   {
    "c": "Cada día",
    "t": "Explicar un tema o documento como presentación",
    "w": "En el chat",
    "x": "/diapositivas",
    "d": "Crea un .html que se abre en el navegador, sin conexión. También vale /diapositivas doc NOMBRE."
   },
   {
    "c": "Cada día",
    "t": "Guardar una respuesta útil del chat",
    "w": "En el chat",
    "x": "/guardar-respuesta",
    "d": "La archiva en .brain/respuestas/ con su fuente, para no tener que volver a pedirla."
   },
   {
    "c": "Cada día",
    "t": "Preguntar a la memoria si ya estaba apuntado",
    "w": "En el chat",
    "x": "/buscar-en-la-memoria",
    "d": "Devuelve los mejores archivos de .brain/ para unas palabras, con las líneas donde salen."
   },
   {
    "c": "Mantenimiento",
    "t": "Revisar que la memoria no diga cosas falsas",
    "w": "En el chat",
    "x": "/revisar-contenido",
    "d": "Busca páginas huérfanas, frases que ya no son ciertas y topes contradictorios; otra IA refuta cada hallazgo."
   }
  ]
 },
 "en": {
  "FILES": [
   {
    "p": "CLAUDE.md",
    "d": 0,
    "q": "How do we work here and where is everything?",
    "r": "Always, at the start",
    "w": "Kept by hand, up to 5 KB",
    "n": "GEMINI.md and AGENTS.md play the same role for other AIs."
   },
   {
    "p": ".brain/",
    "d": 0,
    "g": 1,
    "q": "The whole memory of the project",
    "r": "In parts, never all at once",
    "w": "The AI and the guardians",
    "n": "It is the heart of the method."
   },
   {
    "p": "constitution.md",
    "d": 1,
    "q": "Which rules can never be broken?",
    "r": "At the start",
    "w": "Only changes with your permission",
    "n": "There are 10 rules in this repository."
   },
   {
    "p": "pendientes.md",
    "d": 1,
    "q": "What is missing? (the to-do list)",
    "r": "At the start",
    "w": "The AI, when opening and closing items",
    "n": "Capped at 8 KB. Only what is missing, with fixed numbering."
   },
   {
    "p": "decisions.log",
    "d": 1,
    "q": "What was done and when?",
    "r": "Not read at the start: lines are added at the end",
    "w": "cerrar.py, or cierre.py in light mode",
    "n": "One line per finished task."
   },
   {
    "p": "decisions/",
    "d": 1,
    "q": "Was this already decided, and why?",
    "r": "When something already decided is about to change",
    "w": "The AI, one D-NNN record per decision",
    "n": "A decision that changes is not deleted: it is marked as replaced."
   },
   {
    "p": "specs/",
    "d": 1,
    "q": "What was approved to be built?",
    "r": "Only the one for the current task",
    "w": "The AI; you approve it",
    "n": "Goal, what is in and out, files, tests and risks."
   },
   {
    "p": "architecture/",
    "d": 1,
    "q": "How does this part of the project work?",
    "r": "Only the record for the area being touched",
    "w": "The AI, also with /trocea",
    "n": "One file per topic, with a clear name."
   },
   {
    "p": "traspaso.md",
    "d": 1,
    "q": "Where did the previous chat leave off? (the handover)",
    "r": "When the next chat opens",
    "w": "traspaso-in or traspaso-out",
    "n": "After reading it, it is moved to archive/traspasos/. It only exists between one chat and the next."
   },
   {
    "p": "traspaso-completo.md",
    "d": 1,
    "q": "What happened in the previous chat, in full detail?",
    "r": "Only if you ask with /memoria-traspaso",
    "w": "traspaso-in or traspaso-out",
    "n": "The short handover (~1,500 characters) is read automatically; this one keeps the whole history and is never loaded on its own."
   },
   {
    "p": "notas-chats/",
    "d": 1,
    "q": "What did a helper chat do?",
    "r": "When there is a new note; you are told automatically",
    "w": "The chat that received the request",
    "n": "It only appears when needed."
   },
   {
    "p": "colaboracion.md",
    "d": 1,
    "q": "Which AI does what in this project?",
    "r": "When collaborative mode is on; the indexes point to it",
    "w": "colabora.py, from the IAS_COLABORATIVAS template",
    "n": "It only exists if you have used /colabora si. Turning it off keeps it."
   },
   {
    "p": "archive/",
    "d": 1,
    "q": "Was this done? When?",
    "r": "Only when looking something up; hechos-indice.md first",
    "w": "The AI and the pruning",
    "n": "Finished and tested work. Move, never delete."
   },
   {
    "p": "pruebas/",
    "d": 1,
    "q": "What findings did a test campaign leave?",
    "r": "When it applies",
    "w": "The AI, one P-NNN record",
    "n": "Each fixed finding is marked."
   },
   {
    "p": "lecciones/",
    "d": 1,
    "q": "Which already-solved mistake must I not repeat?",
    "r": "Before repeating similar work; the start-up counts how many there are",
    "w": "lecciones.py, launched by the AI with /leccion",
    "n": "One file per topic, as \"problem | cause | rule\"."
   },
   {
    "p": "respuestas/",
    "d": 1,
    "q": "Did we already save this answer or comparison?",
    "r": "When looking for something already solved; also with /buscar-en-la-memoria",
    "w": "respuestas.py, launched by the AI with /guardar-respuesta",
    "n": "One answer per file, with its source, and an index with the newest first."
   },
   {
    "p": "referencias.md",
    "d": 1,
    "q": "Which documents and roadmap does the project have?",
    "r": "Only when it applies",
    "w": "The AI",
    "n": "Keeps the entry indexes from growing."
   },
   {
    "p": "experiencia/",
    "d": 1,
    "q": "Which skills exist and when is each one used?",
    "r": "On demand",
    "w": "When a skill is added or removed",
    "n": "Master list of skills."
   },
   {
    "p": "biblioteca/",
    "d": 1,
    "q": "Where are the manual and the reusable pieces?",
    "r": "When needed",
    "w": "Comes with the harness",
    "n": "Method, master letter, templates and kits."
   },
   {
    "p": "guardianes/",
    "d": 1,
    "q": "What is checked automatically?",
    "r": "Run by the system, not read",
    "w": "Comes with the harness",
    "n": "Python with the standard library only. Settings live in guardianes.json."
   },
   {
    "p": ".claude/",
    "d": 0,
    "g": 1,
    "q": "The connection with Claude Code",
    "r": "Used by the tool",
    "w": "The installer",
    "n": "Other AIs do not have these hooks."
   },
   {
    "p": "settings.json",
    "d": 1,
    "q": "What runs at each moment?",
    "r": "Used by Claude Code",
    "w": "The installer",
    "n": "Declares 4 hooks: session start, message sent, before each command and answer finished."
   },
   {
    "p": "skills/",
    "d": 1,
    "q": "How should the AI act in each situation?",
    "r": "Only the skill that applies",
    "w": "Comes with the harness",
    "n": "32 skills in this repository."
   },
   {
    "p": "tests/",
    "d": 0,
    "q": "Does the method still work?",
    "r": "Run with: python -m unittest discover tests",
    "w": "The harness",
    "n": "Last run: 409 tests, 6 skipped."
   },
   {
    "p": "VERSION and manifiesto.json",
    "d": 0,
    "q": "Which version is this and which files are shared?",
    "r": "Used by the updater",
    "w": "generar_manifiesto.py",
    "n": "They only exist like this in the source repository. A test fails if you forget to regenerate it."
   }
  ],
  "MOM": [
   {
    "t": "Open a chat",
    "h": "SessionStart",
    "what": "arranque.py runs.",
    "items": [
     "Summarises to-dos, unpushed commits, what is still uncommitted and the last log line.",
     "Shows the previous handover and archives it.",
     "Moves old memory to the archive, without deleting it. It waits if those files have unsaved changes.",
     "Warns about secrets, libraries, files or indexes that are too big, and new harness versions."
    ]
   },
   {
    "t": "Send a message",
    "h": "UserPromptSubmit",
    "what": "notas_abiertas.py runs.",
    "items": [
     "Warns if another helper chat left a new note."
    ]
   },
   {
    "t": "Finish an answer",
    "h": "Stop",
    "what": "cierre.py runs.",
    "items": [
     "Warns if the log line is missing.",
     "For small tasks with green tests, writes that line itself.",
     "Warns when the chat gets long: at 200,000 tokens, and again every 100,000."
    ]
   },
   {
    "t": "Make a commit",
    "h": "Git pre-commit hook",
    "what": "secretos.py runs on what is about to be saved.",
    "items": [
     "Blocks the commit if it finds a high-confidence key or token. It works with any AI, because it belongs to Git."
    ]
   },
   {
    "t": "AI handover",
    "h": "traspaso-out salgo",
    "what": "The skill runs guardar_traspaso.py.",
    "items": [
     "Commits only the memory and pushes it to GitHub.",
     "Stops if there is a secret. Asks first if there are other unpushed commits."
    ]
   }
  ],
  "G": [
   {
    "n": "Start-up",
    "f": "arranque.py",
    "w": "Summarises the real state and runs other checks.",
    "c": "On open",
    "e": "Warns",
    "k": "auto",
    "ek": "warn",
    "d": "It is the first thing that runs when a chat opens (SessionStart hook). It reads the real state —pending items, unpushed commits, uncommitted changes, last log line— and prints it, so the AI does not depend on remembering. It also runs the pruning, warns about big files, secrets, libraries, outdated memory and a new harness version, and shows the previous chat's handover, which it then archives. It reminds you, across chats, of any switch that is on: factory mode, collaborative mode and an external auditor with a non-default setting. If there are sibling projects, it says \"N commits from X not ported\". If everything is fine it prints a single line."
   },
   {
    "n": "Open notes",
    "f": "notas_abiertas.py",
    "w": "Warns about new notes from helper chats.",
    "c": "On send",
    "e": "Warns",
    "k": "auto",
    "ek": "warn",
    "d": "UserPromptSubmit hook: when you send a message, it checks whether there are new notes from helper chats in .brain/notas-chats/ that this chat has not received yet and prints them once. It moves and deletes nothing. With no new notes it prints nothing and spends no tokens."
   },
   {
    "n": "Closing reminder",
    "f": "cierre.py",
    "w": "Reminds you of the log line and the to-do cap.",
    "c": "On finish",
    "e": "Warns",
    "k": "auto",
    "ek": "warn",
    "d": "Stop hook (end of every reply). If project files were touched and the line in decisions.log is missing, or pendientes.md went over its 8 KB cap, it returns a warning that the AI reads and fixes; it warns once per reply. It closes by block of work: it warns after 15 edits without closing, or earlier if the task fails the resume test (another AI could not continue from the request and the git diff alone). In small tasks (up to 2 files, none sensitive) it writes the line itself. Since 1.44 it also warns \"launch the auditor\" when code or configuration changed (not if only documents or memory were touched). Warnings that only inform (long chat, milestone without a lesson, auditor) switch themselves off in that chat if they appear 3 times in a row with nothing changing; the log-line warning never switches off. Since 1.48 it also warns about the chain effect: if one document was touched but not the one that depends on it, it reminds you; it only warns and switches itself off in that chat if repeated."
   },
   {
    "n": "Milestones and lessons",
    "f": "hitos.py",
    "w": "Forces the lesson to be written down when an error is solved or a delicate file is changed.",
    "c": "On finish",
    "e": "Blocks",
    "k": "auto",
    "ek": "block",
    "d": "It runs inside the closing notice. It looks for three signals: an error that got solved, changes to files the project marks as delicate, or a large change (5 or more own files). If there is any, it blocks closing until the lesson is written with /leccion or \"none\" is stated with a reason."
   },
   {
    "n": "Length",
    "f": "longitud.py",
    "w": "Warns that the chat has grown long.",
    "c": "On finish",
    "e": "Warns",
    "k": "auto",
    "ek": "warn",
    "d": "It measures the real context of the AI's last message (input + cache). Past 200,000 tokens it warns that a new chat is advisable and leaves the handover phrase ready; it repeats every further 100,000. A long chat costs more with every message, so cutting it in time saves money."
   },
   {
    "n": "Secrets",
    "f": "secretos.py",
    "w": "Looks for keys and tokens. It can also scan the history.",
    "c": "On open and on every commit",
    "e": "Blocks",
    "k": "auto",
    "ek": "block",
    "d": "It looks for keys and tokens with high-confidence patterns (real token format) and low-confidence ones (suspicious assignments), and for secret files that must be ignored by Git. On opening it checks the project; on every commit (pre-commit hook) it checks what is staged and blocks the commit if there is a secret."
   },
   {
    "n": "Pruning",
    "f": "poda.py",
    "w": "Moves old memory to the archive. Never deletes.",
    "c": "On open",
    "e": "Acts",
    "k": "auto",
    "ek": "act",
    "d": "It moves finished specs and \"replaced\" decision cards to archivo/, rewrites the links in the .md files that cite them and keeps a one-line index per spec. It never deletes and, when in doubt, does not move. By hand: poda.py --ver shows what it would do without touching anything."
   },
   {
    "n": "Handover Git",
    "f": "guardar_traspaso.py",
    "w": "Commits the memory and pushes it.",
    "c": "On traspaso-out salgo",
    "e": "Acts",
    "k": "auto",
    "ek": "act",
    "d": "Called by traspaso-out salgo. It commits only the memory (handover, log, pending items, specs) and pushes it. Loose code stays out: it lists it for you to decide. It never forces the push; if there are other unpushed commits that are not memory, it does not push and lists them. It is the only exception to \"push to GitHub only on your order\"."
   },
   {
    "n": "Libraries",
    "f": "librerias.py",
    "w": "Watches versions. On open it only reads the last result; the online check runs separately.",
    "c": "On open / by hand",
    "e": "Warns",
    "k": "auto",
    "ek": "warn",
    "d": "It reads the project's list of libraries and compares it with OSV.dev, a public database of known vulnerabilities. It understands four ecosystems: Python (requirements.txt), JavaScript with npm (package-lock.json), Rust with cargo (Cargo.lock) and Go (go.mod). Those files pin the exact version of each library, so the warning is precise: «lodash 4.17.15 has 5 vulnerabilities, fixed in 4.17.21». For Python only, it also checks PyPI for a new major version. If the project has none of those files, it stays silent. It saves the result and the start-up only reads it, with no network. If the internet fails, it keeps the previous result and blocks nothing. It only warns: it never updates or installs anything. Tested for real against OSV.dev with a toy project: it detected all three vulnerable libraries (npm, cargo and Go)."
   },
   {
    "n": "Chat memory",
    "f": "eventos_chat.py",
    "w": "Remembers which libraries are installed in the chat and, on git push, stops the upload if one has a known flaw.",
    "c": "Before every command",
    "e": "Blocks",
    "k": "auto",
    "ek": "block",
    "d": "PreToolUse hook (before every terminal command or edit). It remembers, per chat, which libraries were installed (with pip, npm, cargo or go) and, on seeing a git push, checks them with OSV.dev: clean → lets it through; known vulnerability → stops the push and explains; no network → does not block and reminds you. It depends neither on the AI nor on you."
   },
   {
    "n": "Test memory",
    "f": "pruebas.py",
    "w": "Tracks test campaigns and their findings.",
    "c": "On open",
    "e": "Warns",
    "k": "auto",
    "ek": "warn",
    "d": "It counts the open findings (- [ ] boxes) of the test campaigns in .brain/pruebas/ and checks that the index matches the files. It only prints a line if something is open or inconsistent: with everything closed it costs 0 tokens."
   },
   {
    "n": "Index review",
    "f": "revisar_indices.py",
    "w": "Looks for broken references and drift in CLAUDE.md, GEMINI.md and AGENTS.md.",
    "c": "On open / by hand",
    "e": "Warns",
    "k": "auto",
    "ek": "warn",
    "d": "It reviews CLAUDE.md, GEMINI.md and AGENTS.md and produces a report of what seems superfluous or out of date: broken references, drift between indexes, long sections and closeness to the cap. Since 1.36 it also detects outdated memory in pendientes.md and constitution.md (paths, specs and cards that no longer exist). It changes nothing. It warns 60 days after the last review or when an index reaches 80 % of its cap; the dismissals you give are remembered."
   },
   {
    "n": "Large files",
    "f": "archivos_gordos.py",
    "w": "Warns when a memory file nears its 8 KB cap.",
    "c": "On open / by hand",
    "e": "Warns",
    "k": "auto",
    "ek": "warn",
    "d": "AI indexes and pendientes.md have their own cap; the other reading files of .brain/ (references, constitution, architecture/, decisions/…) have an 8 KB cap. It warns at 80 % and suggests /trocea. Read only."
   },
   {
    "n": "Quick close",
    "f": "cerrar.py",
    "w": "Adds the log line in the right format.",
    "c": "By hand or by the AI",
    "e": "Acts",
    "k": "mano",
    "ek": "act",
    "d": "It adds the task line to decisions.log in the right format: python .brain/guardianes/cerrar.py --chat \"Project #N\" \"what was done\". With --carril you pick Small change (default) or SDD. It is the one-line close: it does not force you to touch pending items or cards unless needed. Since 1.47 it accepts --tipo (arnes, leccion, decision, spec, pendiente, memoria, otro) to label the log line."
   },
   {
    "n": "Meter",
    "f": "medir.py",
    "w": "Shows cost and corrections per chat. Read only.",
    "c": "By hand",
    "e": "Read only",
    "k": "mano",
    "ek": "ok",
    "d": "Read-only. It reads the Claude Code logs and, per chat, gives weighted cost, new tokens, output, startup, your messages and corrections, and tokens per finished task. --comparar compares two projects, --desglose ID gives the cost message by message, --ritual separates how much of the cost is harness ritual and how much is work (and measures the resume test). With --fabrica it adds up the director's spending (her chats, without cache) and that of the Codex sessions per factory assignment; it does not count Claude subagents, which have no log of their own."
   },
   {
    "n": "AI factory",
    "f": "fabrica.py",
    "w": "Seals the spec and charter, checks each assignment's scope, watches spending and remembers factory mode.",
    "c": "By hand (the director runs it)",
    "e": "Warns",
    "k": "mano",
    "ek": "warn",
    "d": "No AI, only checks. The director uses it between steps; it is not a hook and does not watch live. It freezes the approved spec and seals the charter, takes a snapshot of the working folder before the executor works, checks that the assignment has its requirement and that only allowed files were touched, records each role's spending and compares it with the charter's caps. With \"fabrica.py modo si|no|estado\" (or /fabrica) it turns factory mode on, which is remembered across chats. If something is breached, it exits with an error to stop and warn you."
   },
   {
    "n": "Auditor",
    "f": "auditor.py",
    "w": "Says who audits (internal and/or external AI), gives the Codex command and stores the settings. It launches no AI.",
    "k": "mano",
    "ek": "ok",
    "d": "Spec 044 (1.44). It looks for quality, resource-use and security flaws and only warns: it never changes code or blocks closing. This guardian does not audit: it stores the settings in guardianes.json (auditor_cierre, auditor_externo, models and effort) and answers \"quien general|cierre|spec\" with who must audit (always the internal one; the external AI Codex in general review and spec closing, and in routine closings only with auditor_externo on \"siempre\"; with \"no\", never). \"codex\" prints the Codex command in read-only mode (on Windows with windows.sandbox=\"unelevated\", or Codex cannot run python). If guardianes.json is broken it does not overwrite it, and the values that go into the command are validated. The AI launches it with the /auditor skill; cierre.py only reminds it to.",
    "c": "By hand",
    "e": "Read only"
   },
   {
    "n": "Collaborative mode",
    "f": "colabora.py",
    "w": "Turns on or off several AIs working with different roles in one project.",
    "k": "mano",
    "ek": "ok",
    "d": "Spec 042 (1.42). \"colabora.py si\" turns on modo_colaborativo, creates .brain/colaboracion.md from the IAS_COLABORATIVAS template (who does what: Claude, Codex, Gemini) and puts a single line pointing to that file in CLAUDE.md, AGENTS.md and GEMINI.md (except those listed in indices_ajenos). \"no\" turns it off and removes those lines but keeps colaboracion.md. \"estado\" just shows how it is. The startup reminds you across chats. It opens no chat.",
    "c": "By hand",
    "e": "Read only"
   },
   {
    "n": "Sibling projects",
    "f": "hermanos.py",
    "w": "Says how many commits of a sibling project are still to be ported to this one.",
    "k": "auto",
    "ek": "warn",
    "d": "Spec 043 (1.43). Read-only. With proyectos_hermanos in guardianes.json (nombre, ruta, rama and archivo_portar) it compares the sibling's commits with this project's port file (sections \"Last ported\", \"Pending\" and \"Done\") and the startup warns \"N commits from X not ported\". It does no fetch and changes nothing; if the sibling is not reachable it stays silent (only the manual command says so). With no siblings configured, it says nothing.",
    "c": "On open / by hand",
    "e": "Warns"
   },
   {
    "n": "Updater",
    "f": "actualizar_arnes.py",
    "w": "Brings the improvements into the project, with a backup.",
    "c": "By hand or with /actualizar",
    "e": "Acts",
    "k": "mano",
    "ek": "act",
    "d": "It brings the harness improvements (guardians, skills, manual, kits, method tests) to a project by comparing the manifest fingerprints. --simular shows what would change without touching anything; it keeps a backup; it does not overwrite what you edited by hand nor touch data or configuration."
   },
   {
    "n": "Code analysis",
    "f": "analisis.py",
    "w": "Reviews the code with rules such as functions that are too long.",
    "c": "Off here",
    "e": "Off",
    "k": "off",
    "ek": "off",
    "d": "It reads the structure of the Python code and warns about three things: unsafe SQL (queries built from text), functions or files that grow relative to their saved baseline, and the project's own rules. Off here; turn it on in projects with code."
   },
   {
    "n": "Database",
    "f": "base_datos.py",
    "w": "Protects a SQLite database with backups and rules.",
    "c": "Off here",
    "e": "Off",
    "k": "off",
    "ek": "off",
    "d": "Consistent SQLite backup before changing tables (with rotation), read-only health check and restore only on explicit order. Off here; turn it on in projects with a database."
   },
   {
    "n": "Lessons",
    "f": "lecciones.py",
    "w": "Stores each lesson learned and rebuilds its index.",
    "c": "When a milestone is solved",
    "e": "Acts",
    "k": "mano",
    "ek": "act",
    "d": "It stores each lesson in .brain/lecciones/<topic>.md in the form \"problem | cause | rule\" and rebuilds the index. The AI launches it with /leccion when the milestones guardian asks; the start-up summarises how many there are. It is what stops an already-solved mistake from happening again."
   },
   {
    "n": "Closing indexes",
    "f": "indices.py",
    "w": "Avoids repeated work when closing a task.",
    "c": "Inside the quick close",
    "e": "Acts",
    "k": "mano",
    "ek": "act",
    "d": "Used by cerrar.py: it adds to decisions/indice.md the rows of the D-NNN cards that are missing (it never deletes or changes rows) and moves a finished item from pendientes.md to archive/hechos.md with its row in the index. It returns the texts and the caller decides whether to write: that is how the preview exists."
   },
   {
    "n": "Slides",
    "f": "diapositivas.py",
    "w": "Turns a topic or a document into a .html presentation.",
    "c": "By hand (/diapositivas)",
    "e": "Read only",
    "k": "mano",
    "ek": "ok",
    "d": "Builds a self-contained .html (no internet, no libraries) from a topic (resumen, version, traspaso, auditoria) or a whole document. The .md text is escaped, only http(s) or relative links are allowed and a policy stops anything from loading from outside. --buscar NAME finds the document and --comprobar compares the original with the slides. .html files are not pushed to Git."
   },
   {
    "n": "Diagrams",
    "f": "diagramas.py",
    "w": "Draws the slides' mermaid blocks as an image.",
    "c": "Used by diapositivas.py",
    "e": "Read only",
    "k": "mano",
    "ek": "ok",
    "d": "Understands flowchart (boxes, diamonds, labelled, dashed and thick arrows) and sequenceDiagram, and draws them as SVG inside the .html, with no internet. If the type is not supported or the drawing is too big, it leaves the text and the script warns in Spanish and English."
   },
   {
    "n": "Saved answers",
    "f": "respuestas.py",
    "w": "Files a useful answer from a chat with its source.",
    "c": "By hand or by the AI (/guardar-respuesta)",
    "e": "Acts",
    "k": "mano",
    "ek": "act",
    "d": "Saves the answer in .brain/respuestas/YYYY-MM-DD-title.md and builds indice.md (newest first). It does not overwrite one with the same title and date, requires a title and a source, has an 8 KB cap and accepts the text on standard input so heredocs are not needed."
   },
   {
    "n": "Content review",
    "f": "revisar_contenido.py",
    "w": "Warns about orphan pages, sentences that are no longer true and contradictory caps in .brain/.",
    "c": "On open (one line) / by hand",
    "e": "Warns",
    "k": "auto",
    "ek": "warn",
    "d": "Read only, never blocks. Start-up gives one line if there are findings and revision_contenido_dias have passed (30 by default; switched off with revision_contenido_activa). The /revisar-contenido skill does \"search and refute\" with a fresh AI that does not have the first one's context, and what is discarded is kept in revision_contenido.json."
   },
   {
    "n": "Memory search",
    "f": "buscar.py",
    "w": "Answers with the best files in .brain/ for a few words.",
    "c": "By hand (/buscar-en-la-memoria)",
    "e": "Read only",
    "k": "mano",
    "ek": "ok",
    "d": "Sweeps lessons, decisions, specs, answers and log on every query, with no index: about 470 KB takes milliseconds. It ignores accents, case and filler words, gives more weight to the title and headings and limits what a long file earns by repeating itself. --archivo includes archive/. Threshold for moving to an index: 5 MB or more than 1 second."
   },
   {
    "n": "Two-language texts",
    "f": "textos.py",
    "w": "Holds every guardian's messages in Spanish and English.",
    "c": "Always (the others use it)",
    "e": "Read only",
    "k": "auto",
    "ek": "ok",
    "d": "The language comes from the \"idioma\" setting in guardianes.json (if missing, Spanish, so old projects do not change). File and command names stay in Spanish in both languages. A test warns if a language lacks a key."
   }
  ],
  "SK": [
   [
    "Your commands",
    [
     "resumen",
     "pendiente",
     "prompt-inicial",
     "actualizar",
     "version",
     "subir-a-github"
    ]
   ],
   [
    "Changing chat or AI",
    [
     "traspaso-in",
     "traspaso-out",
     "chat-nuevo",
     "memoria-traspaso"
    ]
   ],
   [
    "Adopting and tidying older projects",
    [
     "adopta",
     "adoptar-indice-existente",
     "acorta",
     "trocea",
     "revisar-indices-de-ia"
    ]
   ],
   [
    "Closing work properly",
    [
     "cerrar-una-tarea",
     "implementada-no-es-hecha",
     "pendientes-solo-lo-que-falta",
     "mover-no-borrar",
     "spec-antes-de-programar",
     "leccion"
    ]
   ],
   [
    "Avoiding technical mistakes",
    [
     "secretos-fuera-del-repo",
     "vigilar-librerias",
     "licencia-antes-de-usar",
     "cero-dependencias",
     "quitar-codigo-antiguo-con-test"
    ]
   ],
   [
    "Building guardians and speaking plainly",
    [
     "guardian-avisa-o-bloquea",
     "probar-guardian-en-windows",
     "explicar-a-darwin-en-llano"
    ]
   ],
   [
    "Real systems",
    [
     "seguridad-en-sistemas-reales"
    ]
   ],
   [
    "The AI factory",
    [
     "directora-de-fabrica",
     "revisor-independiente",
     "fabrica",
     "revisor-de-consumo"
    ]
   ],
   [
    "Audit and teamwork",
    [
     "auditor",
     "colabora",
     "hermanos"
    ]
   ],
   [
    "Memory and slides",
    [
     "diapositivas",
     "guardar-respuesta",
     "revisar-contenido",
     "buscar-en-la-memoria"
    ]
   ]
  ],
  "GL": [
   [
    "AI factory",
    "Design (spec 035), now built (1.31 to 1.44): working with several AIs with different roles, limits watched by programs and three approval gates of yours. Turned on with /fabrica si."
   ],
   [
    "Aprobador",
    "A separate agent that reads a spec and answers APPROVED or REJECTED under a fixed rule; in the VMware experiment it stood in for Darwin."
   ],
   [
    "Archive",
    "Folder where finished or old work goes. It is moved there, not deleted."
   ],
   [
    "Assignment",
    "Small factory task: the requirement it meets, allowed files and the test that accepts it."
   ],
   [
    "Auditor",
    "An AI that tries to prove that a piece of work fails (quality, resource use, security) and hands in a report. It only warns: it changes nothing and blocks nothing. There is an internal one (Sonnet) and, when needed, an external one (Codex)."
   ],
   [
    "Block",
    "To stop an action, such as a commit with a key. Stronger than warning."
   ],
   [
    "Charter",
    "The rules of the game for a factory mission, signed by Darwin: what can be touched, what is forbidden and how much can be spent."
   ],
   [
    "Chat note",
    "What a helper chat leaves for the chat that asked it for something."
   ],
   [
    "CI/CD",
    "Automation that runs tests and deployments on every push. We do not have it yet."
   ],
   [
    "Collaborative mode",
    "A switch (/colabora) for several AIs to work on the same project with different roles, as set in .brain/colaboracion.md."
   ],
   [
    "Commit",
    "A snapshot of changes saved in the Git history. It is only local until it is pushed."
   ],
   [
    "Constitution",
    "Project rules that are not broken without permission."
   ],
   [
    "Decision (D-NNN)",
    "Short record that keeps what was decided and why."
   ],
   [
    "Director",
    "Design: main agent of a project (Opus) that turns your goal into a spec and hands out assignments. Does not code."
   ],
   [
    "Entry index",
    "Short file the AI reads first: CLAUDE.md, GEMINI.md or AGENTS.md."
   ],
   [
    "Executor",
    "An AI that does a small assignment inside the allowed files (Claude, Codex or Gemini)."
   ],
   [
    "Git",
    "System that keeps the history of changes of a project."
   ],
   [
    "Guardian",
    "Script that checks on its own that the method is followed."
   ],
   [
    "Handover",
    "File that passes the context from one chat, or one AI, to another."
   ],
   [
    "Harness",
    "Everything around the AI so it works well: method, guardians, skills and tests."
   ],
   [
    "Hook",
    "A command that runs on its own when something happens, such as opening a chat."
   ],
   [
    "Independent reviewer",
    "Another AI, in another chat, that did not do the work and reviews it with fresh eyes: nobody approves their own work."
   ],
   [
    "Lane",
    "The path a request takes: with a spec, or fast."
   ],
   [
    "Level",
    "How much of the method is installed in a project: ligero (light), medio (medium) or completo (full)."
   ],
   [
    "Light mode",
    "Short closing for small tasks with green tests."
   ],
   [
    "Log",
    "The decisions.log file: one line per finished task."
   ],
   [
    "Manifest",
    "List of the harness files with their fingerprint, to know whether they changed."
   ],
   [
    "Meta-harness",
    "A harness that serves many projects, shared from a single source."
   ],
   [
    "ODD",
    "Lightweight comparison method: small tasks go straight through and large ones get a task document; no guardians."
   ],
   [
    "Planted flaws",
    "An auditor test: known flaws are hidden in toy code and each auditor is scored on how many it finds."
   ],
   [
    "Pre-commit",
    "Git hook that runs just before a commit is saved."
   ],
   [
    "Prueba de retomar",
    "Question that decides whether a spec is needed: can another AI continue from just the request and the git diff? If so, fast track."
   ],
   [
    "Pruning",
    "Clean-up that moves old memory to the archive."
   ],
   [
    "Push",
    "Sending commits to GitHub."
   ],
   [
    "Reglas de seguridad",
    "Six rules for projects that act on real systems (skill seguridad-en-sistemas-reales): everything through the engine, fail safe, do not depend on the lab and more."
   ],
   [
    "Secret",
    "A key or token that must never enter the repository."
   ],
   [
    "Sibling projects",
    "Projects that come from the same origin with a different variant. The harness warns about the sibling's commits still to be ported."
   ],
   [
    "Skill",
    "Instruction card for a specific situation."
   ],
   [
    "Small change",
    "The short lane, for small tasks."
   ],
   [
    "Spec",
    "Short plan you approve before coding."
   ],
   [
    "Start-up",
    "Automatic summary of the project state when a chat opens."
   ],
   [
    "Subagent",
    "An AI that launches another AI for a narrow task and receives only its report. Used as reviewer and as internal auditor, always read-only."
   ],
   [
    "Test",
    "Automatic check that something still works."
   ],
   [
    "To-dos",
    "List of what is missing (pendientes.md). Only that."
   ],
   [
    "Token",
    "Unit used to measure and charge what the AI reads and writes."
   ],
   [
    "Updater",
    "Program that brings harness improvements into a project without overwriting your work."
   ],
   [
    "vcsim",
    "VMware simulator (needs Go) that would be used to test against something more real than the in-memory lab. Not installed yet."
   ],
   [
    "Version",
    "The harness number. It goes up with every shared change."
   ]
  ],
  "T": [
   {
    "c": "Every day",
    "t": "See how the project is going",
    "w": "In the chat",
    "x": "/resumen",
    "d": "Tells the state in a few bullet points, without writing anything."
   },
   {
    "c": "Every day",
    "t": "See what is missing",
    "w": "In the chat",
    "x": "/pendiente",
    "d": "Lets you choose between coding, your tests, your actions or specs. /pendiente programar also works."
   },
   {
    "c": "Every day",
    "t": "Start a well-explained request",
    "w": "In the chat",
    "x": "/prompt-inicial",
    "d": "Helps you write the goal, the limits and what you must test."
   },
   {
    "c": "Every day",
    "t": "Confirm you tested something",
    "w": "In the chat",
    "x": "I tested item N and it works",
    "d": "The AI moves it from to-dos to done in that same answer."
   },
   {
    "c": "Every day",
    "t": "Close a task by hand",
    "w": "In the terminal",
    "x": "python .brain/guardianes/cerrar.py --chat \"Proyecto #N\" \"qué se hizo\"",
    "d": "Usually the AI does it. The last argument is what was done."
   },
   {
    "c": "Chats and AI",
    "t": "Move to a new chat with the same AI",
    "w": "In the chat",
    "x": "/traspaso-in salgo",
    "d": "Writes the handover and opens the new chat. In Codex, $traspaso-in salgo."
   },
   {
    "c": "Chats and AI",
    "t": "Enter the new chat",
    "w": "In the new chat",
    "x": "/traspaso-in entro",
    "d": "Tells what came before in 4-5 bullet points. Claude shows it automatically on open."
   },
   {
    "c": "Chats and AI",
    "t": "Leave this AI for another",
    "w": "In the chat",
    "x": "/traspaso-out salgo",
    "d": "Writes the handover, commits the memory and pushes it to GitHub."
   },
   {
    "c": "Chats and AI",
    "t": "Arrive at the other AI",
    "w": "In the other AI",
    "x": "/traspaso-out entro",
    "d": "If Gemini does not recognise the skill, ask it to read GEMINI.md, .brain/traspaso.md and .brain/pendientes.md."
   },
   {
    "c": "GitHub",
    "t": "Push to GitHub",
    "w": "In the chat",
    "x": "push it",
    "d": "The skill checks secrets and tests before pushing."
   },
   {
    "c": "GitHub",
    "t": "Look for keys before publishing",
    "w": "In the terminal",
    "x": "python .brain/guardianes/secretos.py",
    "d": "Add --historial to also scan what is already saved in Git."
   },
   {
    "c": "Projects",
    "t": "Install in a new project",
    "w": "In the terminal, from cerebro-vivo",
    "x": "python .brain/biblioteca/kit-arranque/instalar.py RUTA --nombre Nombre --dueno Darwin --nivel completo",
    "d": "You can also double-click instalar_kit.bat. Levels: ligero (light), medio (medium) and completo (full)."
   },
   {
    "c": "Projects",
    "t": "Check an installed project",
    "w": "In the terminal, from cerebro-vivo",
    "x": "python .brain/biblioteca/kit-arranque/instalar.py RUTA --comprobar",
    "d": "Says which pieces are there and which are missing."
   },
   {
    "c": "Projects",
    "t": "Adopt a project with an old CLAUDE.md",
    "w": "In the chat",
    "x": "/adopta",
    "d": "Chains the steps of splitting, shortening and cutting up, and asks for your yes at each table."
   },
   {
    "c": "Projects",
    "t": "Update a project (the easy way)",
    "w": "In the project's chat",
    "x": "/actualizar",
    "d": "Tells you what it brings, asks for your yes and does everything."
   },
   {
    "c": "Projects",
    "t": "See a project's harness version",
    "w": "In the project's chat",
    "x": "/version",
    "d": "Tells the installed version, whether there is a newer one and how to update. Changes nothing. Arrived in 1.21.0."
   },
   {
    "c": "Projects",
    "t": "If /actualizar does not exist (1): see what it will do",
    "w": "In the terminal, inside the project",
    "x": "python .brain/guardianes/actualizar_arnes.py --simular",
    "d": "Happens in projects older than 1.17.0. Writes nothing. Then step 2."
   },
   {
    "c": "Projects",
    "t": "If /actualizar does not exist (2): apply it",
    "w": "In the terminal, inside the project",
    "x": "python .brain/guardianes/actualizar_arnes.py",
    "d": "Keeps a copy in .brain/copias_arnes/, does not overwrite what was changed and runs the tests. Afterwards you will have /actualizar and /version."
   },
   {
    "c": "Projects",
    "t": "See what an update would bring",
    "w": "In the terminal, from cerebro-vivo",
    "x": "python actualizar.py RUTA --simular",
    "d": "Writes nothing. Always worth doing first."
   },
   {
    "c": "Projects",
    "t": "Update a project (by hand)",
    "w": "In the terminal, from cerebro-vivo",
    "x": "python actualizar.py RUTA",
    "d": "Keeps a copy in .brain/copias_arnes/ and does not overwrite what was changed."
   },
   {
    "c": "Maintenance",
    "t": "Review the AI indexes",
    "w": "In the chat",
    "x": "review the indexes",
    "d": "Does a double pass and moves what is retired with your approval."
   },
   {
    "c": "Maintenance",
    "t": "Shorten an index that is too big",
    "w": "In the chat",
    "x": "/acorta",
    "d": "Brings CLAUDE.md, GEMINI.md and AGENTS.md down to the 5 KB cap."
   },
   {
    "c": "Maintenance",
    "t": "Split a large memory file",
    "w": "In the chat",
    "x": "/trocea",
    "d": "Splits it by named topics and keeps the full copy."
   },
   {
    "c": "Maintenance",
    "t": "Run the tests",
    "w": "In the terminal",
    "x": "python -m unittest discover tests",
    "d": "After any change."
   },
   {
    "c": "Maintenance",
    "t": "Measure chats",
    "w": "In the terminal",
    "x": "python .brain/guardianes/medir.py",
    "d": "Shows cost and corrections. Read only."
   },
   {
    "c": "Maintenance",
    "t": "Share a harness change",
    "w": "In the terminal, in cerebro-vivo",
    "x": "python generar_manifiesto.py",
    "d": "First bump VERSION and note it in CAMBIOS.md. Then run the tests."
   },
   {
    "c": "If something fails",
    "t": "The summary does not show on open",
    "w": "In the terminal, or ask the AI",
    "x": "python .brain/guardianes/arranque.py --manual",
    "d": "Also works in Gemini and Codex."
   },
   {
    "c": "If something fails",
    "t": "A warning repeats or gets in the way",
    "w": "In the chat",
    "x": "This warning bothers me, check guardianes.json",
    "d": "The caps live in .brain/guardianes/guardianes.json."
   },
   {
    "c": "Maintenance",
    "t": "See what each chat costs",
    "w": "In the terminal",
    "x": "python .brain/guardianes/medir.py",
    "d": "Per-chat table: weighted cost, new tokens, output and start-up. Read only, changes nothing."
   },
   {
    "c": "Maintenance",
    "t": "See how much of the cost is harness ritual",
    "w": "In the terminal",
    "x": "python .brain/guardianes/medir.py --ritual",
    "d": "Splits the cost into work, memory, new chat, guardian notices and harness maintenance."
   },
   {
    "c": "AI factory",
    "t": "Direct an AI factory",
    "w": "In the chat",
    "x": "/directora-de-fabrica",
    "d": "The AI acts as director: writes the spec and the assignments and asks for your approval at each gate. Other AIs execute."
   },
   {
    "c": "AI factory",
    "t": "Review work with fresh eyes",
    "w": "In a separate chat",
    "x": "/revisor-independiente",
    "d": "Another AI, which did not do the work, reviews it against the assignment. Nobody approves their own work."
   },
   {
    "c": "AI factory",
    "t": "Check the factory's spend and limits",
    "w": "In the terminal, in the project",
    "x": "python .brain/guardianes/fabrica.py topes --encargo N",
    "d": "Compares the recorded spend with the charter's limits. Exits with an error if any is exceeded."
   },
   {
    "c": "AI factory",
    "t": "Measure Codex spend per assignment",
    "w": "In the terminal",
    "x": "python .brain/guardianes/medir.py --fabrica --proyecto RUTA",
    "d": "Adds up the tokens spent by each Codex session, grouped by assignment folder. Read only."
   },
   {
    "c": "AI factory",
    "t": "Turn factory mode on",
    "w": "In the chat",
    "x": "/fabrica si",
    "d": "The AI becomes the director: it does not code, it writes the spec and hands out assignments. It opens a new chat by itself with Opus at medium effort. Remembered across chats."
   },
   {
    "c": "AI factory",
    "t": "Turn factory mode off / see its state",
    "w": "In the chat",
    "x": "/fabrica no",
    "d": "Back to normal mode. /fabrica estado only tells you how it is."
   },
   {
    "c": "AI factory",
    "t": "Review a module's resource use",
    "w": "In the chat",
    "x": "/revisor-de-consumo",
    "d": "A read-only subagent looks for extra CPU, memory, disk or network use when a factory module is finished."
   },
   {
    "c": "Several AIs",
    "t": "Turn on several AIs working in a project",
    "w": "In the chat",
    "x": "/colabora si",
    "d": "Creates .brain/colaboracion.md (who does what: Claude, Codex, Gemini) and a line pointing to it in each AI's index. Remembered across chats."
   },
   {
    "c": "Several AIs",
    "t": "Turn it off / see its state",
    "w": "In the chat",
    "x": "/colabora no",
    "d": "Turns it off and removes the lines; colaboracion.md is kept. /colabora estado only shows it."
   },
   {
    "c": "Several AIs",
    "t": "See what is left to port from a sibling project",
    "w": "In the terminal",
    "x": "python .brain/guardianes/hermanos.py",
    "d": "Read-only: lists the sibling's commits not yet in your port file. The startup already warns you by itself."
   },
   {
    "c": "Several AIs",
    "t": "Set up or adopt the port file",
    "w": "In the chat",
    "x": "/hermanos",
    "d": "Guides you to configure proyectos_hermanos and create the port file from the template."
   },
   {
    "c": "Audit",
    "t": "Audit the whole project (or a folder)",
    "w": "In the chat",
    "x": "/auditor general",
    "d": "Two independent auditors —an internal one and Codex— look for quality, resource-use and security flaws and hand in a single report. It only warns; it changes nothing."
   },
   {
    "c": "Audit",
    "t": "Audit what changed in this task",
    "w": "In the chat",
    "x": "/auditor cierre",
    "d": "The same, but only on what changed. The AI uses it when the closing says \"launch the auditor\"."
   },
   {
    "c": "Audit",
    "t": "Turn the closing warning on or off",
    "w": "In the chat",
    "x": "/auditor cierre no",
    "d": "With \"si\" it warns again after code or configuration changes. \"estado\" only shows it."
   },
   {
    "c": "Audit",
    "t": "Choose when the external AI (Codex) joins",
    "w": "In the chat",
    "x": "/auditor externo general-y-spec",
    "d": "Values: general-y-spec (default), siempre (also in routine closings, more cost) and no (no external AI is ever called)."
   },
   {
    "c": "Audit",
    "t": "See who audits and the Codex command",
    "w": "In the terminal",
    "x": "python .brain/guardianes/auditor.py quien general",
    "d": "Says \"interno + externo\" or just \"interno\". With \"codex\" instead of \"quien…\" it prints the exact read-only Codex command."
   },
   {
    "c": "Every day",
    "t": "Explain a topic or document as a presentation",
    "w": "In the chat",
    "x": "/diapositivas",
    "d": "Creates a .html that opens in the browser, offline. /diapositivas doc NAME also works."
   },
   {
    "c": "Every day",
    "t": "Save a useful answer from the chat",
    "w": "In the chat",
    "x": "/guardar-respuesta",
    "d": "Files it in .brain/respuestas/ with its source, so you do not have to ask for it again."
   },
   {
    "c": "Every day",
    "t": "Ask the memory whether it was already written down",
    "w": "In the chat",
    "x": "/buscar-en-la-memoria",
    "d": "Returns the best files in .brain/ for a few words, with the lines where they appear."
   },
   {
    "c": "Maintenance",
    "t": "Check that the memory does not say false things",
    "w": "In the chat",
    "x": "/revisar-contenido",
    "d": "Looks for orphan pages, sentences that are no longer true and contradictory caps; another AI refutes each finding."
   }
  ]
 }
};
