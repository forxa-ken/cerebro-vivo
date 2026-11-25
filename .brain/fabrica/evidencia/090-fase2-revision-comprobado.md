# Revision 090 fase 2: lo comprobado, lo que falta y el resumen (parte de 090-fase2-revision.md)

## Lo que SÍ comprobé que está bien
- **Las simulaciones no escriben en el proyecto.** Montí una copia completa del repo como «repo» y un proyecto git con CLAUDE.md, settings.json, estado local seguido por git y `guardianes.json` con `auditor_externo` antiguo. Tras `simular_actualizar` y `simular_instalar` (ligero, medio, completo) comparé contenido y fecha de modificación de todos los archivos, incluido `.git`: **cero cambios**. Leí además el código de `sincronizar(simular=True)` (`actualizar_arnes.py:514-521`), `completar_configuracion` (`:224-232`), `asegurar_estado_local` (`:177-204`, el `git ls-files` es solo lectura), `migrar_auditor`, `completar_hooks`, `completar_fichas_skills`, y `instalar(simular=True)` (`instalar.py:40-90, 291-399`): todos protegen la escritura con `simular`. `instalar` con simular sale antes del `sincronizar` real, del `.gitignore`, del `git init` y del hook de secretos (`instalar.py:399`).
- Clave solo en cabecera para POST (`web.py:279`, la de la URL no vale; probado). Host comprobado (`web.py:226-228`): `evil.com` y `localhost.evil.com` dan 403. `Origin: null` da 403. Token: un solo uso, ligado a la acción, caduca (`web.py:303-322`). Tope de cuerpo 4096.
- JS: no usa `innerHTML`, `eval` ni `document.write` (grep); todo con `textContent`. Un nombre con `<img onerror>` se guarda tal cual y se pinta como texto.
- Nada del usuario llega a un shell: `ejecutar` solo despacha 4 acciones fijas; el nivel se valida contra `NIVELES`; la ruta se resuelve siempre contra el registro y se usa la ruta registrada, no la recibida (`web_proyectos.py:212,219`).
- Mayúsculas/minúsculas, `/`, barra final, `..`, punto y espacio finales y nombre corto 8.3: todos se reconocen como el mismo proyecto ya registrado.
- Capa de reglas: denegar por defecto (`permitido`, `web_proyectos.py:33-39`), rol desconocido o acción desconocida = denegado, y el 403 se anota. La web es solo cliente de `ejecutar()`.
- Paridad es/en de claves `web_*` (la prueba lo exige y la leí; no conté las claves una a una).


## Falta o sobra respecto a la spec
- **Hecho según 12.1 y 12.3 fase 2:** registro, añadir (con confirmación), versión y atraso, simulación de actualizar e instalar.
- **Falta (menor):** «avisos» por proyecto (12.1.1) no aparecen; «añadir eligiendo su carpeta» es un cuadro de texto, no un selector; lo que 12.4 llama pestañas «permisos y colaboradores» llega en fases posteriores (aceptable). No hay confirmación de las simulaciones (correcto: solo miran).
- **Spec 13.1/13.2, dónde queda corto:** los roles existen (`ROLES`, `permitido`) y se comprueban, pero **son globales, no por proyecto** (13.1 «roles por proyecto», 13.2.4 «un Brain por proyecto»), y `USUARIO_LOCAL` está fijo, así que hoy la comprobación de permisos solo la ejercitan las pruebas. El almacenamiento (13.2.3 «pieza intercambiable») no está detrás de ninguna interfaz: son funciones sueltas de archivo JSON. 13.5 (permisos por ruta y `web_permisos.json`) no está, y la propia spec 10 lo anota como pendiente. Registrar en la spec que esto se difiere a propósito.
- **Suposiciones de la ejecutora que resuelven huecos de la spec:** tope de log de 2 MB sin rotación (ver A2); cuerpo máx. 4096; tokens de 300 s; registro en `.brain/web_proyectos.json`; en proyectos que no son el repo del arnés todo da 409; la simulación de instalar usa valores fijos (B4).
- **Sobra:** nada relevante. El cambio en `instalar.py` (solo añade `web_proyectos` a GUARDIANES) es correcto y necesario.


## Pruebas: ¿cubren lo que dicen?
Cubren bien: matriz de roles, denegar lo desconocido y anotar, registrar/ver, no tocar la carpeta al registrar, simulaciones sin escritura (en un proyecto simple y en carpeta vacía), nivel malo, solo proyectos registrados, token de un solo uso y por acción, clave en URL no vale, Origin ajeno, tipo 415, cuerpo mal formado/enorme, y paridad es/en.
**No cubren (y mis ataques las encontraron):** prefijo `\\?\` y duplicados por forma de ruta (A1); tope del log y qué pasa al pasarse (A2); concurrencia (A3); JSON anidado (B3); `pendientes.md` por enlace/junction (B1); UNC y rutas relativas (B2); simulaciones sobre un proyecto **con git, CLAUDE.md existente y `.claude/settings.json`** (la prueba `test_simular_actualizar_cuenta_y_no_escribe` usa un proyecto mínimo y `test_simular_instalar_no_escribe` solo una carpeta vacía: no pasan por `fusionar_indice`, `fusionar_ajustes` ni `asegurar_estado_local` con git); `Origin: null`; Host malicioso en POST (hay en fase 1 para GET). El camino «lectura» solo se prueba llamando a la capa, no por HTTP, porque el servidor fija siempre `USUARIO_LOCAL`.
Una prueba que sí vale la pena añadir: la que hice yo, que compara el árbol completo (contenido y fecha, con `.git`) de un proyecto con git antes y después de las tres simulaciones.


## Lo que NO pude comprobar
- Nada con clics reales en el navegador (el JS lo leí, no lo ejecuté): pestañas, el `confirm`, el selector de nivel, el aspecto en móvil.
- La prueba de enlace simbólico real en Windows (se salta sin permiso); sí probé una junction de directorio.
- Un proyecto real de `F:\World of Warcraft` (no lo toqué, como se pidió) ni un proyecto con `core.fsmonitor`.
- Comportamiento en Mac/Linux (rutas, mayúsculas, `realpath`).
- Rutas UNC a un servidor remoto real; solo `\\127.0.0.1\c$`.


## Resumen para quien decide
Nada de lo revisado cambia un proyecto en esta fase. Arreglar A1-A3 antes de la fase 3; B1-B3 son pequeños y baratos; B4-B5 son de honestidad del texto. Decisión para Darwin: si registrar cualquier carpeta (incluida de red) es lo que quiere (B2).
