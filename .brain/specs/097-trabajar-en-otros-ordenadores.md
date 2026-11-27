# Spec 097: trabajar los proyectos desde otros ordenadores (puerta web + login local con GitHub)

- **Estado:** borrador reescrito (2026-11-27). Auditado por Codex (veredicto «aprobable con cambios», 7 hallazgos, aplicados en esta versión; informe en `archive/notas-chats/2026-11-27-auditoria-codex-spec-097.md`). **APROBADA por Darwin el 2026-11-27.** **Fase 1 (comprobaciones) CERRADA por Darwin el 2026-11-27**, con los puntos 2 y 5 solo parciales (§9 bis); la fase 2 (§10) está en curso, sin código aún.
- **Fecha:** 2026-11-27
- **Origen:** Darwin: «diseñar un sistema para poder trabajar en otros ordenadores el proyecto o los proyectos que tenga en casa».
- **Se apoya en:** spec 093 (`/sincronizar`), spec 094 (lo local no viaja con git), spec 022 (traspasos dentro de git), spec 090 (web local, pestaña Proyectos y reglas de simulación).
- **Fuera de alcance:** soporte para Mac (orden de Darwin, 2026-11-27).

## 1. Problema
Llegar a un ordenador donde no hay nada, abrir un navegador y acabar con **todos mis proyectos de GitHub** descargados, el arnés listo y la IA trabajando con la memoria del cerebro, sin que nadie vea proyectos que no le corresponden.

## 2. Escenario base de diseño
El ordenador de llegada **no tiene nada**: ni Git, ni Python, ni la IA, ni el arnés, ni los proyectos. Lo único exigible: **navegador, internet y cuenta de GitHub**. Todo se mide contra este caso. `/sincronizar` y `git clone` son el uso diario **después**, no la entrada.

## 3. Decisiones de Darwin (2026-11-27)
1. El navegador es la **puerta de entrada** al ordenador destino; desde ahí se instalan los proyectos en ese ordenador (se trabaja luego en local, con normalidad).
2. Se traen **todos los proyectos que tenga en GitHub** (con casilla para desmarcar).
3. **Todos los usuarios tienen cuenta de GitHub**; GitHub es el sistema de usuarios: no hay contraseñas propias.
4. Cada usuario ve **solo los proyectos para los que tiene permiso** (los que GitHub le permite ver).
5. **Las credenciales NO van en el proyecto.** La regla 7 de la constitución no cambia. Cada usuario las guarda en su ordenador, fuera de git; el proyecto puede llevar, como mucho, la lista de cuáles necesita, sin valores.
6. Se adopta el **login local con GitHub** (§5): sin servidor propio.

## 4. Diseño: dónde vive cada pieza
| Pieza | Dónde vive | Qué hace |
|---|---|---|
| **Página de entrada** | Página pública del arnés (GitHub Pages, estática; pestaña «Instalar», hoy oculta) | Detecta el sistema, explica y entrega **un único paso** de instalación. No guarda usuarios ni datos. |
| **Instalador** | Descarga local, lo ejecuta el usuario | Deja listos Git, Python y la IA y abre la web local. |
| **Web local del cerebro** | El propio ordenador del usuario (spec 090) | Inicia sesión con GitHub, lista los repositorios permitidos, los clona, instala el arnés si se pide. |
| **Perfil del arnés** | Archivo en el ordenador del usuario, fuera de git | Preferencias (carpeta de trabajo, repos excluidos). Sin contraseñas ni tokens en claro. |

**Límite que hay que decir claro:** una página web **no puede instalar programas sola**; siempre hace falta un primer gesto del usuario (descargar, ejecutar, aceptar avisos del sistema). La página lo reduce a un paso, no lo elimina. **No comprobado** cuánto se reduce en un Windows limpio.

## 5. Login local con GitHub (sin servidor propio)
- **Tipo de aplicación: GitHub App con flujo de dispositivo** (se muestra un código, el usuario lo aprueba en `github.com`). Se elige GitHub App y **no** OAuth App porque la OAuth App solo puede pedir el permiso `repo`, que **incluye escritura** en repositorios privados; la GitHub App permite permisos finos. Requisitos: registrar la app, activar en ella el flujo de dispositivo, y definir expiración del código, intervalo de sondeo, tiempo máximo de espera y qué pasa si el usuario deniega. Riesgo conocido del flujo: suplantación (phishing); la web muestra siempre el nombre de la app y la dirección exacta donde se aprueba.
- **Permisos exactos pedidos:** `Contents: read` y `Metadata: read`, ninguno de escritura. Para repositorios de **organizaciones** hay que instalar o autorizar la app en cada organización; la web lo explica y lista lo que quedó sin acceso. **Por comprobar** (§9).
- GitHub devuelve **quién es** el usuario y **qué repositorios puede ver**; la web solo lista y descarga esos. Así «solo ve lo que tiene permiso» lo garantiza GitHub, no un sistema propio.
- **Token:** solo en el **almacén seguro del sistema operativo** (en Windows, el Administrador de credenciales). **No** se acepta un archivo local «ignorado por git» como alternativa: no cifra nada. Si el sistema no tiene almacén seguro, la web **no guarda** el token y pide iniciar sesión cada vez. El token de usuario de una GitHub App **caduca (8 horas por defecto)** y se renueva con su token de renovación, guardado igual; «cerrar sesión» borra ambos y la web avisa de que puede revocarse también desde GitHub.
- **Git sin token a la vista:** el clonado usa Git Credential Manager (o GitHub CLI) para que el token **no** aparezca en direcciones, argumentos, configuración ni registros.
- **Seguridad de la web local (criterios comprobables, con pruebas desde un origen externo):** escucha solo en `127.0.0.1`; comprueba estrictamente `Host` y `Origin`; sin CORS abierto; cada acción con efecto (iniciar sesión, cerrar sesión, clonar, instalar) exige una **señal anti-falsificación** y se rechaza si llega de otra página; permisos comprobados en el código en cada acción, no solo ocultando botones; registro de acciones (`web_actividad.log` ya existe).
- **Ninguna operación sube nada a GitHub** (regla 9): la web solo lee y clona.
- **Sin servidor propio:** no hay hosting, coste ni cuentas que custodiar. Si más adelante se quisiera un servicio centralizado, sería otra spec.

## 6. Flujo
1. Ordenador vacío → abrir la dirección pública del arnés.
2. La página ofrece el instalador del sistema detectado (un paso).
3. El instalador deja Git, Python y la IA listos y abre la web local.
4. «Iniciar sesión con GitHub» (aprobar el código en `github.com`).
5. La web lista **solo** los repositorios que ese usuario puede ver, paginando la respuesta de GitHub: los **propios, de organizaciones y de colaboración**. **Selección inicial:** marcados los repositorios normales; **forks y archivados aparecen ocultos y desmarcados** (un botón los muestra). Se enseña el tamaño total de lo marcado y el aviso explícito de que **se descargarán a este ordenador**.
6. Simulación previa (qué carpetas se crearán, cuánto espacio) y confirmación.
7. Clonado en la carpeta de trabajo elegida. Los repositorios sin arnés se clonan igual y se marcan «sin arnés»; instalarlo es opcional y con simulación (spec 090).
8. Al terminar, aviso de lo que **no** viaja (secretos, archivos ignorados, programas locales como VMware) y de qué credenciales necesita cada proyecto.
9. Uso diario: `/sincronizar`.

## 7. Lo que no viaja (límites honestos)
- Secretos, `.env` y archivos ignorados por git: cada usuario los repone en su ordenador.
- Programas o máquinas locales de un proyecto (por ejemplo VMware): no se instalan solos.
- Lo no subido a GitHub no existe en el ordenador de llegada.

## 8. Seguridad: requisitos mínimos
- Nada de claves en el repositorio, en la página ni en el código (regla 7).
- **Regla 8, llamada por llamada.** Cada llamada externa lleva tiempo máximo y un resultado definido si falla: autenticación (cancela y deja iniciar de nuevo), listado y clonado (reintento acotado y mensaje claro; lo ya clonado se conserva), descarga del instalador y de Git/Python/la IA (se detiene y explica qué falta). **Aclaración honesta:** en un ordenador vacío sin internet **no hay plan B posible** para la primera instalación; internet es requisito. El plan B local aplica a **después**: los proyectos ya clonados siguen funcionando con git sin red.
- Acciones de escritura en disco (clonar, instalar) siempre con simulación previa y confirmación.
- **Instalador verificable:** versiones **fijadas** de Git, Python y la IA; firma verificable con una clave **independiente de la página** (un hash en la misma página que la descarga no acredita quién lo creó); se declara si pide permisos de administrador; el código del instalador es revisable; ante un fallo se detiene sin dejar nada a medias. **Los repositorios clonados son contenido de terceros: ni el instalador ni la web ejecutan nada de ellos** al clonar; la IA solo los ejecuta cuando el usuario lo pide.
- **Auditoría independiente antes de dar acceso a otras personas** (skills `auditor` y `seguridad-en-sistemas-reales`).

## 9. Lo no comprobado (hay que verificarlo antes de construir)
1. Que una GitHub App con `Contents: read` y `Metadata: read` basta para listar y clonar repositorios privados, también de organizaciones, y cuántos pasos de autorización pide cada organización. (Auditoría de Codex, 2026-11-27: la OAuth App obligaría a dar escritura; por eso se eligió GitHub App.)
2. Que el instalador reduce de verdad a un paso en un Windows limpio, y cómo se instala/inicia sesión la IA.
3. Que los hooks, guardianes y skills del arnés arrancan bien tras clonar en un ordenador recién preparado.
4. Dónde guardar el token de forma segura en Windows sin dependencias nuevas.
5. Comportamiento con muchos repositorios o muy grandes (tiempo, disco).

## 9 bis. Resultados de la fase 1 (2026-11-27, parcial)
**Punto 1, leyendo la documentación de GitHub (no probado con una app real):**
- La GitHub App con token de usuario sirve para listar: `GET /user/installations` (instalaciones a las que el usuario tiene acceso) y `GET /user/installations/{id}/repositories` (repositorios, con el nivel de acceso de esa persona; pide `Metadata: read`). Una sola llamada a la primera sirve además para **comprobar de forma periódica** a qué organizaciones sigue teniendo acceso.
- **Hallazgo que cambia el diseño:** el token de usuario solo alcanza lo que **la app tiene instalado Y el usuario puede ver**. Si la app no está instalada en un repositorio, ese repositorio **no aparece**. Por tanto, para «todos mis proyectos» el usuario debe **instalar la app una vez en su cuenta eligiendo «todos los repositorios»** (los nuevos entran solos) y, en cada organización, la instala un propietario. La web debe guiar ese paso y avisar de lo que quedó fuera.
- **SAML/SSO:** si una organización lo exige y el usuario no lo ha completado, su token no la alcanza; la web debe detectarlo y explicarlo.
- **Sin confirmar:** que `Contents: read` basta para clonar por HTTPS con ese token (es lo esperado, pero requiere probarlo con una app registrada). Registrar una app es un cambio en la cuenta de GitHub de Darwin: **no se hace sin su orden expresa**.

**GitHub App de prueba registrada (2026-11-27, orden de Darwin):** `cerebro-vivo-prueba-fase1` (cuenta `forxa-ken`, privada: solo instalable en esa cuenta), permisos de lectura de `Contents` y `Metadata`, flujo de dispositivo activado, webhook desactivado, caducidad de tokens de usuario activada. Su identificador público (Client ID) es `Iv23licHqTiqtdTwJKEw`; no es un secreto. **No se ha generado clave privada ni secreto de cliente** (el flujo de dispositivo no los necesita). Es una app de prueba: se borra al terminar la fase 1 o se rehace con el nombre definitivo. Aún **no instalada** en ningún repositorio.

**App de prueba `cerebro-vivo-prueba-fase1` BORRADA por Darwin (2026-11-27).** **ACTUALIZACIÓN (2026-11-27): la app definitiva de abajo fue borrada por error y se registró de nuevo con los mismos ajustes. Client ID VIGENTE: `Iv23liCXSlLiXiOOndBi` (público, no es secreto); el App ID y el Client ID de abajo ya no valen. Falta comprobar que Darwin la instaló con «todos los repositorios».**
**GitHub App DEFINITIVA registrada (2026-11-27, orden de Darwin):** nombre «Cerebro Vivo» (identificador `cerebro-vivo`, cuenta `forxa-ken`), **App ID 5957873**, **Client ID `Iv23li0fWF2wrIaLWnph`** (público, no es secreto). Instalable por **cualquier cuenta** (decisión de Darwin: otras personas inician sesión con su propio GitHub). Permisos solo de lectura: `Contents: read` y `Metadata: read` (comprobado en el formulario antes de crearla). Flujo de dispositivo activado, webhook desactivado, página de inicio la página pública del arnés. **No se generó clave privada ni secreto de cliente.** Sin comprobar aún: que los tokens de usuario caducan a las 8 h (se verá en el primer login real) y que la app aún **no está instalada** en ningún repositorio (hay que instalarla con «todos los repositorios»). La app de prueba `cerebro-vivo-prueba-fase1` queda sin uso: borrarla o dejarla es decisión de Darwin.

**Prueba real del punto 1 (2026-11-27, 19:31), con la app instalada solo en `Duoplanning`:**
- El flujo de dispositivo **funciona**: se pide el código a GitHub, el usuario lo aprueba y GitHub entrega un token de usuario que caduca a las **8 horas (28800 s)**, con token de renovación a ~181 días.
- `GET /user/installations` devolvió la instalación de `forxa-ken` con selección «solo seleccionados»; `.../repositories` devolvió **únicamente `Duoplanning`** (privado). Confirma que **solo se ve lo que la app tiene instalado**.
- **`Contents: read` basta para clonar** un repositorio privado por HTTPS con ese token (clonado correcto, sin que el token apareciera en argumentos ni en la salida).
- Otro repositorio privado no instalado (`Modelo`) **se rechazó con error 403**: el permiso mínimo se cumple.
- **Hallazgo de usabilidad:** el botón «Authorize» de GitHub quedó **desactivado en el panel de navegador de Claude** y hubo que aprobarlo en Chrome normal. Para el producto final, la web local debe abrir el navegador del usuario por defecto, no uno incrustado.
- **Ampliado a «todos los repositorios» (19:34):** la instalación pasó a `all` y el token de usuario listó los **15** repositorios de `forxa-ken` (los mismos que `gh repo list`: 11 privados y 4 públicos, ninguno archivado ni fork). El primer intento de guardar el cambio no se aplicó; hay que verificar siempre recargando.
- El token se usó solo en memoria durante la prueba y no se escribió en ningún archivo; el clon de prueba se borró.

**Punto 4 (en este ordenador):** Git, Python 3.12 y Git Credential Manager están instalados; el almacén de Windows existe. **Comprobado (2026-11-27, con un valor falso, no un token real):** desde Python 3.12 solo con la biblioteca estándar (`ctypes` sobre `advapi32`: `CredWriteW`, `CredReadW`, `CredDeleteW`) se guarda, se lee de vuelta idéntico y se borra en el Administrador de credenciales de Windows; tras borrar no queda rastro (`cmdkey /list`). **Sin dependencias nuevas, sin archivo con el token.** Límite: la entrada queda ligada al usuario de Windows y no es un cofre contra malware que corra como ese mismo usuario. Mac y Linux quedan fuera de esta comprobación (Mac, olvidado por orden de Darwin). El script de prueba no se guardó en el repositorio.

**Punto 5, parcial (2026-11-27, solo tamaños, sin clonar):** los 15 repos de `forxa-ken` suman ~1,4 GB en GitHub. Dos concentran casi todo: `yu-gi-wow` (~1 GB) y `LoboGelido` (~320 MB); el resto está bajo 52 MB (mediana ~3 MB). **Consecuencia de diseño:** la web debe mostrar el tamaño antes de clonar, no clonar todo de golpe, y ofrecer clonado superficial (`--depth 1`) para los grandes. **Sin medir:** tiempos reales de clonado y el efecto de los hooks sobre repos grandes.

**Pruebas en un Windows 10 Home limpio (2026-11-27, equipo físico distinto al de casa; hechas a mano, no hay instalador aún):**
- **Punto 2, parcial:** Git 2.56.1 y Python 3.12.10 se instalan con `winget` (`Git.Git`, `Python.Python.3.12`), con hash verificado. **Git pide permisos de administrador** (UAC); Python no avisó. Tras instalar hay que **abrir una terminal nueva**: la abierta no reconoce los programas nuevos (el instalador debe avisarlo). Sin medir la IA (Claude Code no se instaló).
- **Punto 1 repetido en limpio:** login de dispositivo OK (el navegador de esa máquina tenía ya la sesión de GitHub abierta), clonado privado superficial de `Duoplanning` en 2,3 s. El primer código se tecleó mal; la web local debe mostrarlo en grande y avisar de la caducidad (~10 min).
- **Hallazgo:** `Duoplanning` (Android) **no trae `.brain`**: clonar un proyecto no instala el arnés. La web debe ofrecerlo (`actualizar_arnes.py`). Decisión de diseño pendiente de Darwin.
- **Punto 3, parcial:** `arranque.py --manual` del repo `cerebro-vivo` clonado funciona sin errores en el equipo limpio (salida JSON con acentos escapados; cosmético). Pruebas: **809 en ~187 s, 3 errores y 8 saltadas**, todos de `test_web`/`test_web_proyectos.TestHttp`. Son **intermitentes**: sueltas pasan; en una segunda tanda fallaron 2 distintas. Causa: `WinError 10053` (conexión anulada por el software del equipo) al enviar datos y esperar un `405`. Dos explicaciones sin distinguir: antivirus/cortafuegos de esa máquina, o el servidor local cierra sin leer el cuerpo. Sin arreglar. Hooks de Claude Code **sin probar** (no instalado ahí).
- **Requisito añadido por Darwin (2026-11-27):** el instalador **descarga todo** y ofrece **como opción** instalar Claude Code, Codex y/o Antigravity (cualquier combinación o **ninguna**: instalar una IA es opcional; Gemini CLI fuera salvo que Darwin lo pida) y lanzar las elegidas; las lanza con el arnés y los proyectos ya listos. **Sin comprobar:** cómo se instala cada IA (Claude Code, Codex y Antigravity; esta última es un editor, no una terminal, y no sé qué índice lee del arnés), si hay `winget` o instalador oficial para cada una, y cómo inicia sesión cada una en un equipo nuevo. Cada IA con su índice (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`) ya lo trae el arnés.
- **Las tres IA están en winget (comprobado 2026-11-27 buscando, sin instalar):** `Anthropic.ClaudeCode` (2.1.332), `OpenAI.Codex` (Codex CLI 0.172.0) y `Google.Antigravity` (2.35.2, instalada hoy en el PC de casa en `%LOCALAPPDATA%\Programs\antigravity`, o sea por usuario). **Sin comprobar:** si piden administrador, cómo inician sesión en un equipo nuevo y qué índice del arnés lee Antigravity. Hay otros paquetes con nombres parecidos no oficiales: el instalador debe fijar el `Id` exacto, nunca buscar por nombre.
- **Claude Code instalado en el equipo limpio (2026-11-27):** `winget install --id Anthropic.ClaudeCode -e --source winget` → 2.1.332, descarga de 384 MB con hash verificado, sin aviso de administrador, PATH nuevo (hay que abrir terminal nueva); `claude --version` responde. **Iniciar sesión y hooks, probado (2026-11-27):** `claude` en el clon de `cerebro-vivo` pidió iniciar sesión (cuenta de Darwin) y luego **confiar en la carpeta** porque declara hooks en `.claude/settings.json` (pregunta obligatoria, por proyecto; por defecto «No, exit»; la web/instalador debe explicarla y nunca confiar por el usuario). Tras confiar, **el hook `SessionStart` se ejecutó solo** y mostró el resumen de arranque (estado, pendientes, lecciones). Abrió en **modo automático por defecto** (aviso de Claude Code): el instalador debe decirlo antes. Claude Code **no crea acceso directo**: se abre con `claude` en terminal. **También probado:** `hola` obtuvo respuesta en español tras leer `CLAUDE.md`, y `/skills` listó **44 skills del proyecto** activas (el clon es la versión subida; la copia local tiene 40 porque quitó 4 en commits sin subir). **Punto 3 cubierto** en Windows 10 Home limpio salvo: hook `Stop` al cerrar, y las 3 pruebas web intermitentes (arriba).
- **Matiz sobre «limpio»:** ese equipo ya tenía **Antigravity 2.29.0 instalada con winget** (por usuario; winget ofrece la 2.35.2) y no estaba en el PATH de la terminal. Sin Git ni Python sí estaba vacío. Consecuencia: el instalador debe **detectar lo ya instalado y no reinstalarlo**, y ofrecer actualizar. Además `winget list` sin `--source winget` pidió aceptar los términos de `msstore`: el instalador usa siempre `--source winget --accept-source-agreements`.
- Quedan en esa máquina Git, Python, `%USERPROFILE%\prueba-097` y la autorización de la app en la cuenta de Darwin (conviene revocarla).

**Puntos 2 y 3 (resto) y 5:** solo bloquean la fase 4 (instalador); necesitan un ordenador o máquina **limpia** y repositorios reales; no se pueden comprobar aquí con rigor. Pendientes de que Darwin indique dónde probar.

## 10. Fases propuestas (cada una se aprueba aparte)
1. **Comprobaciones** (§9, puntos 1 a 3) en un ordenador o máquina limpia; sin construir nada.
2. **Login local con GitHub** y listado de repositorios permitidos (solo lectura) en la web local. **HECHA y probada por Darwin (2026-11-27, v1.71.0, commit 9e7393b):** login real, 15 repositorios listados.
3. **Clonado** con simulación y confirmación, y aviso de lo que no viaja.
4. **Instalador y página de entrada** (mostrar la pestaña «Instalar»; ver pendiente 64).
5. **Auditoría independiente** y prueba de uso real en un ordenador sin nada.

## 11. Descartado
- Servicio web con servidor propio y sistema propio de usuarios y contraseñas (coste y riesgo; innecesario con GitHub).
- Credenciales dentro del proyecto, también en cofre cifrado (regla 7).
- Trabajar solo dentro del navegador con la IA en la nube (opción A): queda como plan B futuro, no se construye.
- Contenedor tipo Docker y paquete portable (exigen instalar algo antes: no cumplen el escenario base).

## 12. Pruebas previstas y criterios de aceptación
- Pruebas automáticas con GitHub simulado: listado filtrado por permisos y paginado, token que no se escribe en el repositorio ni aparece en direcciones, argumentos o registros, tiempo máximo y resultado ante fallo de cada llamada externa.
- Pruebas de la web local **desde un origen externo**: toda acción con efecto se rechaza sin la señal anti-falsificación o con `Host`/`Origin` ajenos.
- Aceptación del instalador: firma verificada con clave independiente, versiones fijadas, sin dejar restos si falla.
- Aceptación de privados y organizaciones: un repositorio privado y uno de organización se listan y clonan solo con los permisos mínimos.
- Prueba de uso real al final (fase 5) en un ordenador vacío, con evidencia guardada.
