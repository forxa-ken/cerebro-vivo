# Auditoría de Codex a la spec 097 (2026-11-27)

Revisor: Codex (solo lectura). Veredicto: APROBABLE CON CAMBIOS. Los 7 hallazgos se aplicaron en la spec.

## Hallazgos

1. **Alta — El permiso mínimo para repositorios privados no está resuelto.**  
   Cita: «lectura de repositorios; sin escritura».  
   La spec mezcla OAuth App y GitHub App como si ofrecieran los mismos permisos. En OAuth Apps, el scope `repo` permite leer y escribir en repositorios privados, además de otras acciones; no es solo lectura. Una GitHub App sí permite configurar permisos más específicos, como `Contents: read` y `Metadata: read`. [Scopes de OAuth Apps](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/scopes-for-oauth-apps), [permisos de GitHub Apps](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/choosing-permissions-for-a-github-app).  
   **Arreglo:** decidir el tipo de app y documentar los permisos exactos para listar y clonar repositorios privados, incluidas las autorizaciones de organizaciones.

2. **Alta — El almacenamiento alternativo del token puede dejarlo en claro.**  
   Cita: «en el almacén de credenciales del sistema operativo o en un archivo local ignorado por git».  
   Que un archivo esté ignorado por Git no lo cifra ni lo protege de otros procesos o usuarios del ordenador. Además, «Caduca o se revoca» no fija una política: los tokens de OAuth App no tienen necesariamente una caducidad breve; los tokens de usuario de GitHub App caducan por defecto a las ocho horas y pueden requerir renovar también el token de actualización. [Caducidad y revocación](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/token-expiration-and-revocation), [tokens de GitHub App](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/refreshing-user-access-tokens).  
   **Arreglo:** exigir almacenamiento seguro del sistema operativo, definir caducidad, renovación, cierre de sesión y borrado. No aceptar el archivo ignorado como alternativa equivalente. Para Git por HTTPS, especificar cómo evitar que el token quede en URL, configuración, argumentos o registros; GitHub recomienda Git Credential Manager o GitHub CLI en Windows. [Credenciales Git](https://docs.github.com/en/get-started/git-basics/caching-your-github-credentials-in-git).

3. **Alta — El control de la web local está expresado como intención, no como requisito comprobable.**  
   Cita: «protección contra peticiones falsas desde otras páginas».  
   `127.0.0.1` por sí solo no define esa protección. Una web maliciosa podría intentar enviar peticiones al servicio local; faltan controles concretos contra CSRF, comprobación estricta de origen y host, CORS permisivo y acciones con efectos iniciadas por peticiones del navegador.  
   **Arreglo:** convertir estos controles en criterios verificables para cada endpoint, especialmente clonar, instalar y cerrar sesión; incluir pruebas desde un origen externo.

4. **Alta — La promesa del instalador no está lista para aprobarse.**  
   Cita: «Deja listos Git, Python y la IA».  
   No se especifican versiones, procedencia, firma, permisos de administrador, actualizaciones ni qué código se ejecuta. Publicar un hash en la misma página que sirve la descarga no acredita por sí solo quién creó el instalador. Y clonar proyectos de terceros introduce contenido que la IA o el instalador podrían después ejecutar.  
   **Arreglo:** definir artefactos y versiones fijadas, firma verificable con clave independiente de la página, permisos requeridos, revisión del código ejecutable y comportamiento ante fallos. Probarlo en un Windows limpio antes de prometer «un paso».

5. **Alta — Choca con la regla 8 y con el escenario de entrada.**  
   Cita: «sin red, los proyectos ya clonados siguen funcionando con git».  
   Esto cubre el uso diario de proyectos existentes, pero no es un plan B local para las llamadas externas necesarias al inicio: autenticación, descarga del instalador, Git, Python, la IA y los repositorios. En un ordenador vacío, sin red, no hay copia local con la que continuar.  
   **Arreglo:** especificar, para cada llamada externa, límites de tiempo y resultado ante fallo; aclarar qué partes del escenario vacío requieren internet y cómo se satisface la regla 8 en ellas.

6. **Media — Hay contradicción en qué significa descargar «todos» los proyectos.**  
   Citas: «todos los proyectos» y «forks y archivados ocultos por defecto, todo marcado».  
   Si forks y archivados están ocultos, no pueden quedar todos marcados por defecto; tampoco se precisa si «todos» incluye repositorios de organizaciones, colaboraciones y repositorios grandes.  
   **Arreglo:** definir el conjunto exacto que se lista, cómo se pagina la respuesta de GitHub y qué selección inicial se aplica a repositorios ocultos.

7. **Media — El flujo de dispositivo está sin elegir y omite condiciones importantes.**  
   Cita: «flujo de dispositivo o aplicación OAuth de GitHub».  
   GitHub admite flujo de dispositivo para GitHub Apps, pero hay que habilitarlo en la configuración; su uso está pensado para herramientas de escritorio o sin navegador. GitHub también advierte del riesgo de suplantación de la app y phishing en ese flujo. [Flujo de dispositivo](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app), [recomendaciones OAuth](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/best-practices-for-creating-an-oauth-app).  
   **Arreglo:** seleccionar el flujo y tipo de app, registrar la aplicación, justificar el riesgo y definir expiración del código, intervalos de sondeo, límites de espera y tratamiento de aprobación denegada.

## Falta para aprobar

Resolver los puntos anteriores y añadir criterios de aceptación para autorización de repositorios privados, paginación y errores, protección de la web local, instalación verificable, credenciales de Git y prueba completa en Windows limpio. La regla 9 también exige dejar explícito que ninguna operación sube cambios a GitHub sin orden de Darwin.

## Veredicto

**APROBABLE CON CAMBIOS.** El planteamiento puede funcionar, pero el login, el manejo de tokens y la cadena de instalación aún no tienen decisiones ni garantías suficientes para construirlo con seguridad.
