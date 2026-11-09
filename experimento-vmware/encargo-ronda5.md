# Encargo de la ronda 5 — mantenimiento (idéntico para las dos ramas)

Eres una IA que **retoma** un proyecto que otra sesión dejó hecho: el sistema de automatización VMware con el módulo **Discos** ya programado (`vmware_auto/discos.py`, `docs/discos.md`, `experimento/resultado.md`). No tienes memoria de esa sesión: solo lo que hay en los archivos de tu carpeta. Trabajas con el método que dice tu `CLAUDE.md`.

## Tarea: mover un disco a otro almacén de datos
Añadir al módulo Discos la operación **mover disco** (migrar un disco de una máquina a otro almacén de datos del laboratorio):
1. Acción nueva en el **motor** y comando de línea de comandos que solo llama al motor (`mover_disco`: máquina, disco, almacén destino).
2. Ampliar `vmware_auto/laboratorio.py` con **un segundo almacén de datos** (espacio propio y limitado); los discos existentes siguen en el primero. Listar discos debe mostrar en qué almacén está cada disco y el espacio libre de cada almacén.
3. Reglas: mover es **delicado**. Con la máquina encendida (o si no se puede saber su estado), o si el disco es grande según el umbral que ya usa el módulo, o si el destino no tiene espacio de sobra, **no actúa sin visto bueno explícito** (el espacio insuficiente es error, no solo aviso). Mover al mismo almacén donde ya está es error claro.
4. Pruebas en `tests/` (todo en verde, incluidas las previas) y documentación breve en `docs/discos.md`.

## Criterios de aceptación (comprobables)
1. `--simular` dice qué haría y no cambia nada (probado).
2. Sin visto bueno explícito no actúa en los casos delicados y anota el rechazo (probado).
3. Todo intento (ensayo, rechazo, hecho, error) queda en el registro con quién, qué, cuándo y perfil (probado).
4. Funciona llamando al motor sin la línea de comandos (probado).
5. Errores claros: máquina, disco o almacén inexistente; mismo almacén; sin espacio; ninguno deja el laboratorio a medias (probado).
6. No se rompe ninguna prueba previa (la prueba ajena `test_soporte_mac` ya falla en Windows: no es tuya); perfil `lab` por defecto; perfiles y credenciales intactos.
7. Al menos 1 fallo provocado propio de mover (por ejemplo el destino se llena justo al ejecutar).

## Límites (obligatorios)
- Nada de servidores reales ni producción; nada de GitHub; ningún secreto en archivos. No instalar software nuevo.
- Alcance estricto: solo mover disco. No tocar `master`, ni otras carpetas del proyecto (ni `vmware-automatizacion-ronda4-*` ni la otra rama de la ronda 5).
- Si tu método exige someter un documento al aprobador: `python experimento/aprobador.py RUTA --modulo "Discos"`. Sin APROBADA no se programa. `ERROR_TECNICO` no es rechazo: relánzalo; si falla 2 veces avisa a Darwin.
- Anota en `experimento/resultado.md`: cuánto te costó orientarte (qué archivos leíste primero), qué heredaste de la sesión anterior y te sirvió, qué no encontraste, qué cuesta tocar el módulo.

## Al terminar
Commit en tu rama; nada de GitHub. El coste lo mide la sesión que coordina, desde fuera.
