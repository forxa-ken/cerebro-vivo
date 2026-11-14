# Lecciones: metodo-herramientas-y-rutas

Formato: problema → causa → regla. Las escribe `lecciones.py` en el momento del hito (spec 026).

- **Edge headless desde Bash no creó el PDF y no dio error** → la salida se perdió con el pipe y la ruta con espacios → **usar PowerShell Start-Process -Wait con --headless=new y --print-to-pdf entre comillas, y comprobar que el archivo existe** (2026-11-11)
- **gh run watch observó el run anterior ya terminado, no el nuevo** → tomé el último run de la lista antes de que GitHub registrara el push → **esperar unos segundos y comprobar que headSha del run coincide con el commit subido** (2026-11-11)
- **Edit sobre datos.js de la carpeta de la página falló con 'File has not been read yet'** → el archivo era de otra carpeta (_cv_pagina) y yo solo lo había mirado con sed/grep por Bash, no con Read → **antes de Edit en un archivo, leerlo con Read aunque ya se haya visto con grep; lanzar el Read y el Edit en mensajes distintos** (2026-11-12)
- **Tres ediciones a la vez fallaron en la carpeta de la pagina (_cv_pagina)** → la herramienta Edit exige haber leido el archivo en este chat y yo lance las ediciones sin leerlo → **antes de editar archivos de otra carpeta (la pagina publica) leer con Read la linea exacta; las tres ediciones se lanzan juntas solo despues de leerlas** (2026-11-14)
