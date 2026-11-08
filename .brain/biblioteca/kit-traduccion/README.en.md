# Translation kit (spec 057, D-052)

Languages for a website or app in 3 files, taken from the system of a real project. **Optional** in the starter kit: `instalar.py DESTINO --traduccion` (or the checkbox in the window). It is copied to the new project's `static/i18n/`, plus the test `tests/test_paridad_idiomas.py`.

## How to use it
1. Load `idiomas.js` on the page, then `i18n_motor.js` (see `ejemplo.html`).
2. Mark each text with `data-i18n="key"` (also `-html`, `-placeholder`, `-title`, `-aria`).
3. Put `<select data-i18n-selector></select>` where you want the selector: it fills itself in.
4. In code: `KitI18n.t("key")`, `KitI18n.setIdioma("en")`. The chosen language is remembered in the browser.

## Add a language (example: French)
1. In `idiomas.js`, under `"idiomas"`: `"fr": "Français"`.
2. Under `"textos"`: a `"fr": {…}` block with the **same keys** as `es`.
3. Run `python paridad_idiomas.py` (or `python -m unittest tests.test_paridad_idiomas`): it tells you which keys are missing.

`idiomas.js` is strict JSON (double quotes, no trailing commas) so the test can read it. If a text must be the same in every language (a brand name), add its key to `"iguales_permitidos": [...]`.

## What it does NOT include
The automatic dictionary translator from that project, or paid AI translations. Translations are written (or requested in the chat) and pasted into `idiomas.js`.
