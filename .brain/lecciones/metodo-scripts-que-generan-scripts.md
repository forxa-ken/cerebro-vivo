# Lecciones: metodo-scripts-que-generan-scripts

Formato: problema → causa → regla. Las escribe `lecciones.py` en el momento del hito (spec 026).

- **Un script de limpieza escrito con un heredoc de Python que reescribía otro script con regex dentro de una cadena sin r quedó roto (los \n pasaron a saltos de línea reales, SyntaxError)** → las barras invertidas se interpretan dos veces al generar código desde código → **No generar un script con otro script: escribir el archivo entero con la herramienta Write y probarlo sobre un clon antes de usarlo. Y para reescribir historial de git: respaldo con git bundle, trabajar en un clon, comprobar restos en cada commit, y empujar con --force-with-lease apuntando al SHA visto** (2026-11-12)
