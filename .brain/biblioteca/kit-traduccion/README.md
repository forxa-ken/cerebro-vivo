# Kit de traducción (spec 057, D-052)

Idiomas para una web o app en 3 archivos, sacados del sistema de un proyecto real. **Opcional** en el kit de arranque: `instalar.py DESTINO --traduccion` (o la casilla de la ventana). Se copia a `static/i18n/` del proyecto nuevo, más el test `tests/test_paridad_idiomas.py`.

## Cómo se usa
1. Cargar en la página `idiomas.js` y después `i18n_motor.js` (ver `ejemplo.html`).
2. Marcar cada texto con `data-i18n="clave"` (también `-html`, `-placeholder`, `-title`, `-aria`).
3. Poner `<select data-i18n-selector></select>` donde quieras el selector: se rellena solo.
4. En código: `KitI18n.t("clave")`, `KitI18n.setIdioma("en")`. El idioma elegido se recuerda en el navegador.

## Añadir un idioma (ejemplo: francés)
1. En `idiomas.js`, en `"idiomas"`: `"fr": "Français"`.
2. En `"textos"`: un bloque `"fr": {…}` con las **mismas claves** que `es`.
3. Ejecutar `python paridad_idiomas.py` (o `python -m unittest tests.test_paridad_idiomas`): dice qué claves faltan.

`idiomas.js` es JSON estricto (comillas dobles, sin comas al final) para que el test pueda leerlo. Si un texto debe ser igual en todos los idiomas (una marca), añade su clave a `"iguales_permitidos": [...]`.

## Qué NO trae
El traductor automático por diccionario de aquel proyecto, ni traducciones con IA de pago. Las traducciones se escriben (o se piden en el chat) y se pegan en `idiomas.js`.
