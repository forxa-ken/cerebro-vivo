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
    "n": "Hay 9 reglas en este repositorio."
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
    "n": "Declara 3 hooks: abrir sesión, enviar mensaje y acabar respuesta."
   },
   {
    "p": "skills/",
    "d": 1,
    "q": "¿Cómo debe actuar la IA en cada situación?",
    "r": "Solo la skill que toca",
    "w": "Viene con el arnés",
    "n": "25 skills en este repositorio."
   },
   {
    "p": "tests/",
    "d": 0,
    "q": "¿Sigue funcionando el método?",
    "r": "Se lanza: python -m unittest discover tests",
    "w": "El arnés",
    "n": "Último pase: 289 pruebas, con 6 saltadas."
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
    "ek": "warn"
   },
   {
    "n": "Notas abiertas",
    "f": "notas_abiertas.py",
    "w": "Avisa de notas nuevas de chats auxiliares.",
    "c": "Al enviar",
    "e": "Avisa",
    "k": "auto",
    "ek": "warn"
   },
   {
    "n": "Aviso de cierre",
    "f": "cierre.py",
    "w": "Recuerda la línea del registro y el tope de pendientes.",
    "c": "Al acabar",
    "e": "Avisa",
    "k": "auto",
    "ek": "warn"
   },
   {
    "n": "Longitud",
    "f": "longitud.py",
    "w": "Avisa de que el chat se ha alargado.",
    "c": "Al acabar",
    "e": "Avisa",
    "k": "auto",
    "ek": "warn"
   },
   {
    "n": "Secretos",
    "f": "secretos.py",
    "w": "Busca claves y tokens. También puede revisar el historial.",
    "c": "Al abrir y en cada commit",
    "e": "Bloquea",
    "k": "auto",
    "ek": "block"
   },
   {
    "n": "Poda",
    "f": "poda.py",
    "w": "Mueve a archivo la memoria vieja. Nunca borra.",
    "c": "Al abrir",
    "e": "Actúa",
    "k": "auto",
    "ek": "act"
   },
   {
    "n": "Git del traspaso",
    "f": "guardar_traspaso.py",
    "w": "Hace commit de la memoria y lo sube.",
    "c": "En traspaso-out salgo",
    "e": "Actúa",
    "k": "auto",
    "ek": "act"
   },
   {
    "n": "Librerías",
    "f": "librerias.py",
    "w": "Vigila versiones. Al abrir solo lee el último resultado; la consulta por internet se lanza aparte.",
    "c": "Al abrir / a mano",
    "e": "Avisa",
    "k": "auto",
    "ek": "warn"
   },
   {
    "n": "Memoria de pruebas",
    "f": "pruebas.py",
    "w": "Sigue las campañas de pruebas y sus hallazgos.",
    "c": "Al abrir",
    "e": "Avisa",
    "k": "auto",
    "ek": "warn"
   },
   {
    "n": "Revisión de índices",
    "f": "revisar_indices.py",
    "w": "Busca referencias rotas y deriva en CLAUDE.md, GEMINI.md y AGENTS.md.",
    "c": "Al abrir / a mano",
    "e": "Avisa",
    "k": "auto",
    "ek": "warn"
   },
   {
    "n": "Archivos gordos",
    "f": "archivos_gordos.py",
    "w": "Avisa cuando un archivo de memoria se acerca a su tope de 8 KB.",
    "c": "Al abrir / a mano",
    "e": "Avisa",
    "k": "auto",
    "ek": "warn"
   },
   {
    "n": "Cierre rápido",
    "f": "cerrar.py",
    "w": "Añade la línea del registro con su formato correcto.",
    "c": "A mano o por la IA",
    "e": "Actúa",
    "k": "mano",
    "ek": "act"
   },
   {
    "n": "Medidor",
    "f": "medir.py",
    "w": "Muestra por chat el coste y las correcciones. Solo lee.",
    "c": "A mano",
    "e": "Solo lee",
    "k": "mano",
    "ek": "ok"
   },
   {
    "n": "Actualizador",
    "f": "actualizar_arnes.py",
    "w": "Trae las mejoras al proyecto, con copia de seguridad.",
    "c": "A mano o con /actualizar",
    "e": "Actúa",
    "k": "mano",
    "ek": "act"
   },
   {
    "n": "Análisis de código",
    "f": "analisis.py",
    "w": "Revisa el código con reglas como funciones demasiado largas.",
    "c": "Apagado aquí",
    "e": "Apagado",
    "k": "off",
    "ek": "off"
   },
   {
    "n": "Base de datos",
    "f": "base_datos.py",
    "w": "Defiende una base de datos SQLite con copias y reglas.",
    "c": "Apagado aquí",
    "e": "Apagado",
    "k": "off",
    "ek": "off"
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
     "traspaso-out"
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
     "spec-antes-de-programar"
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
   ]
  ],
  "GL": [
   [
    "Actualizador",
    "Programa que lleva las mejoras del arnés a un proyecto, sin pisar lo tuyo."
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
    "Fast-Track",
    "Carril rápido, para tareas pequeñas."
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
    "Push",
    "Enviar los commits a GitHub."
   ],
   [
    "Registro",
    "El archivo decisions.log: una línea por tarea terminada."
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
   }
  ],
  "S": [
   {
    "h": "La IA no recuerda",
    "b": [
     "Cada chat empieza de cero.",
     "Lo acordado se pierde al cerrar la conversación.",
     "En proyectos largos, eso cuesta tiempo y errores."
    ],
    "s": "Empieza por el problema. Cualquiera que haya usado una IA en un proyecto largo lo reconocerá."
   },
   {
    "h": "La memoria vive en archivos",
    "b": [
     "Reglas, pendientes, decisiones y planes, cada uno en su sitio.",
     "La IA lee poco al empezar y busca el detalle si hace falta.",
     "Funciona con Claude, Gemini y Codex."
    ],
    "s": "La idea central es sacar la memoria del chat. La verdad está en el código y en estos archivos."
   },
   {
    "h": "Scripts que vigilan el método",
    "b": [
     "Hooks al abrir un chat, al enviar y al acabar cada respuesta.",
     "Un hook pre-commit bloquea claves y tokens.",
     "El resto, sobre todo, avisa de olvidos."
    ],
    "s": "Depender de la disciplina de la IA era el punto débil. Puedes poner el ejemplo de los secretos."
   },
   {
    "h": "Un solo origen, muchos proyectos",
    "b": [
     "Cada cambio tiene versión, registro y huella de archivos.",
     "Los proyectos se actualizan cuando yo decido.",
     "Nunca se pisan datos ni cambios hechos a mano."
    ],
    "s": "Aquí se ve la parte de ingeniería: el método se reparte como un producto."
   },
   {
    "h": "Lo he medido, también lo malo",
    "b": [
     "Respetó lo acordado 5 de 5 veces, frente a 0 de 5.",
     "Gasta de un 7 % a un 16 % más en tareas pequeñas.",
     "El ahorro a largo plazo sigue sin medir."
    ],
    "s": "Di que la muestra es pequeña. Enseñar lo que no salió bien da más credibilidad que un resultado perfecto."
   },
   {
    "h": "Lo siguiente",
    "b": [
     "CI/CD: lanzar las pruebas en cada subida.",
     "Un agente revisor independiente.",
     "Pruebas en proyectos reales de lo más reciente."
    ],
    "s": "Termina con lo que quieres aprender. Son planes: todavía no están hechos."
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
    "n": "There are 9 rules in this repository."
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
    "n": "Declares 3 hooks: session start, message sent and answer finished."
   },
   {
    "p": "skills/",
    "d": 1,
    "q": "How should the AI act in each situation?",
    "r": "Only the skill that applies",
    "w": "Comes with the harness",
    "n": "25 skills in this repository."
   },
   {
    "p": "tests/",
    "d": 0,
    "q": "Does the method still work?",
    "r": "Run with: python -m unittest discover tests",
    "w": "The harness",
    "n": "Last run: 289 tests, 6 skipped."
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
    "ek": "warn"
   },
   {
    "n": "Open notes",
    "f": "notas_abiertas.py",
    "w": "Warns about new notes from helper chats.",
    "c": "On send",
    "e": "Warns",
    "k": "auto",
    "ek": "warn"
   },
   {
    "n": "Closing reminder",
    "f": "cierre.py",
    "w": "Reminds you of the log line and the to-do cap.",
    "c": "On finish",
    "e": "Warns",
    "k": "auto",
    "ek": "warn"
   },
   {
    "n": "Length",
    "f": "longitud.py",
    "w": "Warns that the chat has grown long.",
    "c": "On finish",
    "e": "Warns",
    "k": "auto",
    "ek": "warn"
   },
   {
    "n": "Secrets",
    "f": "secretos.py",
    "w": "Looks for keys and tokens. It can also scan the history.",
    "c": "On open and on every commit",
    "e": "Blocks",
    "k": "auto",
    "ek": "block"
   },
   {
    "n": "Pruning",
    "f": "poda.py",
    "w": "Moves old memory to the archive. Never deletes.",
    "c": "On open",
    "e": "Acts",
    "k": "auto",
    "ek": "act"
   },
   {
    "n": "Handover Git",
    "f": "guardar_traspaso.py",
    "w": "Commits the memory and pushes it.",
    "c": "On traspaso-out salgo",
    "e": "Acts",
    "k": "auto",
    "ek": "act"
   },
   {
    "n": "Libraries",
    "f": "librerias.py",
    "w": "Watches versions. On open it only reads the last result; the online check runs separately.",
    "c": "On open / by hand",
    "e": "Warns",
    "k": "auto",
    "ek": "warn"
   },
   {
    "n": "Test memory",
    "f": "pruebas.py",
    "w": "Tracks test campaigns and their findings.",
    "c": "On open",
    "e": "Warns",
    "k": "auto",
    "ek": "warn"
   },
   {
    "n": "Index review",
    "f": "revisar_indices.py",
    "w": "Looks for broken references and drift in CLAUDE.md, GEMINI.md and AGENTS.md.",
    "c": "On open / by hand",
    "e": "Warns",
    "k": "auto",
    "ek": "warn"
   },
   {
    "n": "Large files",
    "f": "archivos_gordos.py",
    "w": "Warns when a memory file nears its 8 KB cap.",
    "c": "On open / by hand",
    "e": "Warns",
    "k": "auto",
    "ek": "warn"
   },
   {
    "n": "Quick close",
    "f": "cerrar.py",
    "w": "Adds the log line in the right format.",
    "c": "By hand or by the AI",
    "e": "Acts",
    "k": "mano",
    "ek": "act"
   },
   {
    "n": "Meter",
    "f": "medir.py",
    "w": "Shows cost and corrections per chat. Read only.",
    "c": "By hand",
    "e": "Read only",
    "k": "mano",
    "ek": "ok"
   },
   {
    "n": "Updater",
    "f": "actualizar_arnes.py",
    "w": "Brings the improvements into the project, with a backup.",
    "c": "By hand or with /actualizar",
    "e": "Acts",
    "k": "mano",
    "ek": "act"
   },
   {
    "n": "Code analysis",
    "f": "analisis.py",
    "w": "Reviews the code with rules such as functions that are too long.",
    "c": "Off here",
    "e": "Off",
    "k": "off",
    "ek": "off"
   },
   {
    "n": "Database",
    "f": "base_datos.py",
    "w": "Protects a SQLite database with backups and rules.",
    "c": "Off here",
    "e": "Off",
    "k": "off",
    "ek": "off"
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
     "traspaso-out"
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
     "spec-antes-de-programar"
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
   ]
  ],
  "GL": [
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
    "Decision (D-NNN)",
    "Short record that keeps what was decided and why."
   ],
   [
    "Entry index",
    "Short file the AI reads first: CLAUDE.md, GEMINI.md or AGENTS.md."
   ],
   [
    "Fast-Track",
    "The fast lane, for small tasks."
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
    "Pre-commit",
    "Git hook that runs just before a commit is saved."
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
   }
  ],
  "S": [
   {
    "h": "The AI does not remember",
    "b": [
     "Every chat starts from scratch.",
     "What was agreed is lost when the conversation closes.",
     "On long projects, that costs time and mistakes."
    ],
    "s": "Start with the problem. Anyone who has used an AI on a long project will recognise it."
   },
   {
    "h": "Memory lives in files",
    "b": [
     "Rules, to-dos, decisions and plans, each in its place.",
     "The AI reads little at the start and looks up details when needed.",
     "Works with Claude, Gemini and Codex."
    ],
    "s": "The core idea is taking memory out of the chat. The truth lives in the code and in these files."
   },
   {
    "h": "Scripts that watch over the method",
    "b": [
     "Hooks when a chat opens, when a message is sent and when each answer ends.",
     "A pre-commit hook blocks keys and tokens.",
     "The rest mostly warn about what was forgotten."
    ],
    "s": "Relying on the AI's discipline was the weak spot. You can use secrets as the example."
   },
   {
    "h": "One source, many projects",
    "b": [
     "Every change has a version, a log and file fingerprints.",
     "Projects are updated when I decide.",
     "Data and hand-made changes are never overwritten."
    ],
    "s": "This is where the engineering shows: the method is shipped like a product."
   },
   {
    "h": "I measured it, the bad parts too",
    "b": [
     "It kept what was agreed 5 out of 5 times, versus 0 out of 5.",
     "It costs 7 % to 16 % more on small tasks.",
     "Long-term savings are still unmeasured."
    ],
    "s": "Say the sample is small. Showing what did not go well earns more trust than a perfect result."
   },
   {
    "h": "What comes next",
    "b": [
     "CI/CD: running the tests on every push.",
     "An independent reviewer agent.",
     "Testing the latest pieces on real projects."
    ],
    "s": "End with what you want to learn. These are plans: they are not done yet."
   }
  ]
 }
};
