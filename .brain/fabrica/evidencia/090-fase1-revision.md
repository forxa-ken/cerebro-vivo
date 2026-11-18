# Revision independiente, spec 090 fase 1 (web local de solo lectura)

Archivos: .brain/guardianes/web.py, tests/test_web.py, claves web_* de .brain/guardianes/textos.py (+ buscar.py y medir.py solo como dependencias).
Solo lectura; no se ejecuto nada del codigo revisado, se leyo.

## Veredicto
Sin hallazgos graves. Ninguna ruta de salida de .brain/ por /api/doc, ningun XSS, ninguna inyeccion de comandos, comparacion de clave en tiempo constante. Hay 1 hallazgo medio-bajo (fuga por enlace simbolico via el buscador) y varios menores.

## Lo verificado y correcto
- Escucha: ("127.0.0.1", puerto) en web.py:238. Correcto.
- Clave: secrets.token_urlsafe(16) (128 bits), hmac.compare_digest (web.py:197). Se exige en todas las rutas GET, incluida "/". Sin cabeceras CORS y X-Clave exige preflight; OPTIONS devuelve 405: una web ajena no puede leer.
- DNS rebinding: Host debe ser 127.0.0.1 o localhost (web.py:193); Host vacio o ajeno da 403. Ademas hace falta la clave.
- /api/doc: ruta_segura (web.py:39-55) usa realpath + commonpath contra realpath(.brain). Cubre "..", %2e%2e (parse_qs decodifica antes), enlaces simbolicos y junctions que apunten fuera, unidades distintas (ValueError capturado), prefijo hermano (.brain-x), NUL. Solo .md y decisions.log.
- XSS: todo se pinta con textContent; los textos T.* tambien. PAGINA % {"lang": idioma()} solo inserta es/en; no hay otro "%" en la plantilla. Respuestas de datos son text/plain o JSON con nosniff.
- Subproceso medir.py: lista de argumentos (sin shell), opcion tomada de MEDIR (lista cerrada de 3), nada del usuario llega al comando (web.py:105-116).
- No escribe: ningun do_* de escritura; POST/PUT/DELETE/PATCH/OPTIONS -> 405.
- Textos: las 23 claves web_* existen en es y en, mismas claves; las usadas por la pagina existen.

## Hallazgos

### H1 (media-baja) Fuga por enlace simbolico de archivo en /api/buscar
- web.py:221 -> buscar.py:98. buscar.archivos() lista por nombre (os.walk no sigue directorios, pero si lista enlaces a archivo llamados *.md) y buscar() hace open() sin realpath. ruta_segura NO se aplica a este camino.
- Reproduccion: crear dentro de .brain/lecciones/ un enlace x.md hacia un archivo fuera de .brain (p. ej. mklink .brain\lecciones\x.md C:\Windows\win.ini), arrancar web.py y pedir /api/buscar?q=<palabra del archivo externo>. Devuelve titulo y hasta 2 lineas (160 car.) del archivo externo. /api/doc para ese enlace si da 404, asi que la proteccion es inconsistente.
- Requiere poder plantar un enlace en .brain/ (en Windows exige privilegio o modo desarrollador; un repo clonado con symlinks tambien puede traerlo). Fuga parcial, solo lectura.
- Arreglo sugerido: en web.py filtrar los resultados con ruta_segura(raiz, r["archivo"]) antes de devolverlos (y filtrar tambien lista()).

### H2 (baja) TOPE_TEXTO_ESTADO no trunca: vacia
- web.py:58-60 y :76. leer() devuelve None si el archivo supera el tope, y estado() lo convierte en "". Si pendientes.md pasa de 20 000 bytes (hoy 5 120) el Inicio muestra PENDIENTES vacio sin aviso. Igual con decisions.log > 1 MB (hoy 53 554 bytes): "ultima linea" vacia (web.py:79) y /api/doc da 404 sin distinguir "demasiado grande" de "no existe".
- Reproduccion: poner 25 000 bytes en pendientes.md y pedir /api/estado.

### H3 (baja) Sin timeout de conexion ni limite de subprocesos
- web.py:175 (Manejador sin atributo timeout) y :223. Una conexion local abierta sin enviar peticion retiene un hilo indefinidamente (la clave se mira despues de leer la peticion). /api/medir autenticado puede lanzar varios medir.py de hasta 120 s en paralelo. Solo DoS local propio; no explotable desde fuera.

### H4 (baja) Puerto fijo en Windows
- web.py:238. http.server.HTTPServer pone allow_reuse_address=1; en Windows eso permite que otro proceso local abra el mismo puerto con --puerto N y reciba conexiones (incluida la URL con clave). Con puerto aleatorio (por defecto) el riesgo es casi nulo; ya es un atacante local con el mismo usuario.

### H5 (informativa) Clave en la URL
- web.py:258. La clave queda en el historial del navegador y en la linea de comandos del navegador (webbrowser.open). Sin Referrer-Policy; hoy no hay enlaces externos que la filtren. Aceptable por diseno de la spec.

### H6 (informativa) medir.py ignora la raiz del servidor
- web.py:112 pasa cwd=raiz pero medir.py usa su propio RAIZ/--proyecto por defecto; con una raiz distinta de la del script (solo ocurre en pruebas) mediria otro proyecto. Sin impacto hoy.

## Pruebas que no prueban lo que dicen (tests/test_web.py)
- T1 (:87-91) test_no_sale_de_brain: el titulo promete enlaces simbolicos pero no hay ninguna prueba con enlace (ni siquiera con skip si Windows no deja crearlo). Tampoco prueba que decisions.log SI se sirve ni el prefijo hermano. Por eso H1 no se detecto. Los casos "/etc/passwd" y "C:/Windows/win.ini" pasan trivialmente (no empiezan por .brain/); los que de verdad cuentan son ".brain/../fuera.md" y el %2e%2e.
- T2 (:98-101) test_medir_solo_acepta_la_lista_cerrada: nunca ejecuta medir con exito, asi que no comprueba que --skills/--fabrica/--ritual existan ni que la salida llegue; `sorted(web.MEDIR) == [...]` es tautologico con la constante.
- T3 (:103-111) "pagina_sin_inyeccion": solo busca la cadena "innerHTML"; no detecta insertAdjacentHTML, outerHTML, document.write ni eval. El nombre promete mas de lo que prueba. La comprobacion de claves usadas ignora las dinamicas T['web_c_'+c] y T['web_medir_'+n].
- T4 (:73-75) test_ningun_metodo_escribe: solo mira el 405; no comprueba que nada se escribio, ni HEAD (que da 501) ni que el 405 se de sin clave.
- T5 (:60-61) test_solo_escucha_en_loopback: comprueba la direccion del socket, correcto pero no prueba que un cliente por otra interfaz no conecte (aceptable).
- No hay prueba de las cabeceras de seguridad (CSP, nosniff) ni de la pagina "/" renderizada.

## Resumen de gravedad
Graves: 0. Medios: 0. Medio-bajo: H1. Bajos: H2, H3, H4. Informativos: H5, H6. Pruebas flojas: T1-T4.
