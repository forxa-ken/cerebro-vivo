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
    "d": "Es lo primero que corre al abrir un chat (aviso SessionStart). Lee el estado real —pendientes, commits sin subir, cambios sin commitear, última línea del registro— y lo imprime, para que la IA no dependa de acordarse. Además lanza la poda, avisa de archivos gordos, secretos, librerías y versión nueva del arnés, y muestra el traspaso del chat anterior, que después archiva. Si todo está en orden, imprime una sola línea."
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
    "d": "Aviso Stop (fin de cada respuesta). Si se tocaron archivos del proyecto y falta la línea en decisions.log, o pendientes.md pasó su tope de 8 KB, devuelve un aviso que la IA lee y corrige; avisa una sola vez por respuesta. Desde la 1.29.0 cierra por bloque de trabajo: avisa tras 15 ediciones sin cerrar. En tareas pequeñas (hasta 2 archivos, ninguno sensible) escribe él mismo la línea."
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
    "d": "Revisa CLAUDE.md, GEMINI.md y AGENTS.md y saca un informe de lo que parece sobrar o estar desfasado: referencias rotas, deriva entre índices, secciones largas y cercanía al tope. No modifica nada. Avisa a los 60 días de la última revisión o cuando un índice llega al 80 % de su tope."
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
    "d": "Añade la línea de la tarea a decisions.log con el formato correcto: python .brain/guardianes/cerrar.py --chat «Proyecto #N» «qué se hizo». Con --carril elige Cambio pequeño (por defecto) o SDD. Es el cierre de una línea: no obliga a tocar pendientes ni fichas salvo que corresponda."
   },
   {
    "n": "Medidor",
    "f": "medir.py",
    "w": "Muestra por chat el coste y las correcciones. Solo lee.",
    "c": "A mano",
    "e": "Solo lee",
    "k": "mano",
    "ek": "ok",
    "d": "Solo lectura. Lee los registros de Claude Code y, por chat, saca coste ponderado, tokens nuevos, salida, arranque, mensajes tuyos y correcciones. --comparar enfrenta dos proyectos, --desglose ID da el coste mensaje a mensaje, --ritual separa cuánto del coste es ritual del arnés y cuánto es trabajo. Con --fabrica suma el gasto de las sesiones de Codex por encargo de la fábrica."
   },
   {
    "n": "Fábrica de IA",
    "f": "fabrica.py",
    "w": "Sella la spec y la carta, comprueba el alcance de cada encargo y vigila el gasto y los topes.",
    "c": "A mano (lo lanza la directora)",
    "e": "Avisa",
    "k": "mano",
    "ek": "warn",
    "d": "Sin IA, solo comprobaciones. Lo usa la directora entre un paso y otro; no es un hook ni vigila en vivo. Congela la spec aprobada y sella la carta, saca una foto de la carpeta de trabajo antes de que trabaje la ejecutora, comprueba que el encargo tiene su requisito y que solo se tocaron los archivos permitidos, anota el gasto de cada papel y lo compara con los topes de la carta. Si algo incumple, sale con error para parar y avisarte."
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
     "revisor-independiente"
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
    "Bloquear",
    "Impedir una acción, como un commit con una clave. Es más fuerte que avisar."
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
    "IA que hace un encargo pequeño dentro de los archivos permitidos (Claude o Codex)."
   ],
   [
    "Encargo",
    "Tarea pequeña de la fábrica: requisito que cumple, archivos permitidos y prueba que la da por buena."
   ],
   [
    "Fábrica de IA",
    "Diseño (spec 035) para trabajar con varias IA con papeles distintos, límites vigilados por programas y tres puertas de aprobación tuyas. Aún en construcción."
   ],
   [
    "Cambio pequeño",
    "Carril corto, para tareas pequeñas."
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
    "Índice de entrada",
    "Archivo corto que lee la IA primero: CLAUDE.md, GEMINI.md o AGENTS.md."
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
    "d": "It is the first thing to run when a chat opens (SessionStart hook). It reads the real state —pending items, unpushed commits, uncommitted changes, last log line— and prints it, so the AI does not depend on remembering. It also launches the pruning, warns about heavy files, secrets, libraries and a new harness version, and shows the previous chat's handover, which it then archives. If all is in order, it prints a single line."
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
    "d": "Stop hook (end of every reply). If project files were touched and the decisions.log line is missing, or pendientes.md went over its 8 KB cap, it returns a warning that the AI reads and fixes; it warns only once per reply. Since 1.29.0 it closes by block of work: it warns after 15 edits without closing. On small tasks (up to 2 files, none sensitive) it writes the line itself."
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
    "d": "It reviews CLAUDE.md, GEMINI.md and AGENTS.md and produces a report of what looks superfluous or outdated: broken references, drift between indexes, long sections and closeness to the cap. It changes nothing. It warns 60 days after the last review or when an index reaches 80 % of its cap."
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
    "d": "It adds the task line to decisions.log in the right format: python .brain/guardianes/cerrar.py --chat \"Project #N\" \"what was done\". With --carril you pick Small change (default) or SDD. It is the one-line close: it does not force you to touch pending items or cards unless needed."
   },
   {
    "n": "Meter",
    "f": "medir.py",
    "w": "Shows cost and corrections per chat. Read only.",
    "c": "By hand",
    "e": "Read only",
    "k": "mano",
    "ek": "ok",
    "d": "Read only. It reads Claude Code's records and, per chat, reports weighted cost, new tokens, output, start-up, your messages and corrections. --comparar pits two projects against each other, --desglose ID gives the cost message by message, --ritual separates how much of the cost is harness ritual and how much is work. With --fabrica it adds up Codex sessions' spend per factory assignment."
   },
   {
    "n": "AI factory",
    "f": "fabrica.py",
    "w": "Seals the spec and the charter, checks each assignment's scope and watches spend and limits.",
    "c": "By hand (the director runs it)",
    "e": "Warns",
    "k": "mano",
    "ek": "warn",
    "d": "No AI, only checks. The director uses it between steps; it is not a hook and does not watch live. It freezes the approved spec and seals the charter, takes a snapshot of the working folder before the executor works, checks that the assignment has its requirement and that only allowed files were touched, records each role's spend and compares it with the charter's limits. If something fails it exits with an error so work stops and you are told."
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
     "revisor-independiente"
    ]
   ]
  ],
  "GL": [
   [
    "Aprobador",
    "A separate agent that reads a spec and answers APPROVED or REJECTED under a fixed rule; in the VMware experiment it stood in for Darwin."
   ],
   [
    "Archive",
    "Folder where finished or old work goes. It is moved there, not deleted."
   ],
   [
    "Block",
    "To stop an action, such as a commit with a key. Stronger than warning."
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
    "Commit",
    "A snapshot of changes saved in the Git history. It is only local until it is pushed."
   ],
   [
    "Constitution",
    "Project rules that are not broken without permission."
   ],
   [
    "Charter",
    "The rules of the game for a factory mission, signed by Darwin: what can be touched, what is forbidden and how much can be spent."
   ],
   [
    "Decision (D-NNN)",
    "Short record that keeps what was decided and why."
   ],
   [
    "Entry index",
    "Short file the AI reads first: CLAUDE.md, GEMINI.md or AGENTS.md."
   ],
   [
    "Director",
    "Design: main agent of a project (Opus) that turns your goal into a spec and hands out assignments. Does not code."
   ],
   [
    "Executor",
    "AI that does one small assignment inside the allowed files (Claude or Codex)."
   ],
   [
    "Assignment",
    "Small factory task: the requirement it meets, allowed files and the test that accepts it."
   ],
   [
    "AI factory",
    "Design (spec 035) for working with several AIs in distinct roles, limits watched by programs and three approval gates of yours. Still being built."
   ],
   [
    "Small change",
    "The short lane, for small tasks."
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
    "Skill",
    "Instruction card for a specific situation."
   ],
   [
    "Spec",
    "Short plan you approve before coding."
   ],
   [
    "Independent reviewer",
    "Another AI, in another chat, that did not do the work and reviews it with fresh eyes: nobody approves their own work."
   ],
   [
    "Start-up",
    "Automatic summary of the project state when a chat opens."
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
   }
  ]
 }
};
