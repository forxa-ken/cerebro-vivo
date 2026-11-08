# Spec 024: Cerebro Vivo y su página también en inglés

- **Estado:** aprobada por Darwin el 2026-11-07 («Sí, empieza»). Fase 1 hecha y publicada (gh-pages `a09ce01`, comprobada en la página real): selector ES/EN, 179 textos y `datos.js` en los dos idiomas, `comprobar_idiomas.py` en la rama de la página. Fase 2 hecha (1.22.0, sin subir): `textos.py` con los avisos de los 17 guardianes en es/en, ajuste `idioma` (por defecto `es`), el instalador lo guarda y `test_textos.py`; comprobada en un proyecto de prueba en inglés. Quedan en español la ayuda de `--help` y el texto que los guardianes escriben dentro de la memoria (pasa a la fase 3). Fase 3 hecha (1.25.0, sin subir): ediciones `.en.md` de las skills, de `CEREBRO_VIVO`, de las plantillas y del kit, más `README.en.md` y `MANUAL_DE_USO.en.md`; el actualizador y el instalador eligen según `idioma`
- **Fecha:** 2026-11-07
- **Versión prevista:** arnés 1.22.0 (fase 2) y 1.23.0 (fase 3); la fase 1 solo toca la página

## 1. Objetivo
Darwin pidió la localización a inglés «en cerebro y la página». Así, una persona que no habla español puede leer la página e instalar el método en su proyecto, con los avisos, las skills y los manuales en inglés.

Tamaño medido: el arnés reparte 88 archivos (unas 8.400 líneas). Unas 3.900 son guardianes y documentación; unas 2.900 son pruebas y no hace falta traducirlas. La página tiene 600 líneas.

## 2. En alcance
**Fase 1, la página** (rama gh-pages):
- [ ] Selector ES / EN arriba, con el kit propio `kit-traduccion` (`idiomas.js` + `i18n_motor.js`). Recuerda la elección y elige inglés solo si el navegador no está en español.
- [ ] Todos los textos en los dos idiomas, más la prueba de paridad (`paridad_idiomas.py`), que avisa si falta una clave.
- [ ] Pestaña «Cambios»: el historial sigue en español (viene de `CAMBIOS.md`); en inglés se avisa con una línea.

**Fase 2, lo que el método dice en pantalla:**
- [ ] Ajuste por proyecto `"idioma": "es" | "en"` en `guardianes.json` (por defecto `es`, así no cambia nada en los proyectos que ya existen).
- [ ] Mensajes de los guardianes (arranque, cierre, avisos) sacados a un `textos.py` con `es` y `en`, más una prueba de que ninguna clave falta.
- [ ] El instalador (`kit-arranque`) pregunta el idioma y lo guarda.

**Fase 3, lo que lee la IA y la persona:**
- [ ] Edición inglesa de las 26 skills, de `CEREBRO_VIVO.md`, del manual, de las plantillas y de `constitution` (la regla de idioma dice «responder en el idioma del proyecto»).
- [ ] `actualizar_arnes.py` copia la edición del idioma del proyecto; el manifiesto guarda la huella de las dos.
- [ ] `README.md` con un enlace a `README.en.md`.

## 3. Fuera de alcance
- **Los nombres de archivos, carpetas y comandos siguen en español** (`.brain/pendientes.md`, `guardianes/`, `/actualizar`, `traspaso-in`). Cambiarlos rompería los proyectos que ya existen y sus pruebas.
- Las pruebas, `decisions.log`, las specs y `CAMBIOS.md` siguen en español.
- Otros idiomas (el kit lo permite más adelante sin rehacer nada).
- Traducción automática con servicios de pago: la traducción la escribe la IA en el chat.
- El ZIP de Mac.

## 4. Plan
1. Fase 1: página bilingüe; comprobarla en la página real a ancho de móvil y de escritorio; subirla solo con la orden de Darwin.
2. Fase 2: `textos.py`, el ajuste `idioma`, guardianes e instalador; pruebas; `VERSION` 1.22.0, `CAMBIOS.md`, manifiesto.
3. Fase 3: ediciones inglesas y actualizador; pruebas; `VERSION` 1.23.0.
Cada fase se cierra y se prueba por separado; un chat nuevo por fase si el chat se alarga.

## 5. Verificación
- `python -m unittest discover tests` en verde en cada fase, con pruebas nuevas de paridad (página, mensajes y skills).
- Un proyecto de prueba en una carpeta temporal con `"idioma": "en"`: el arranque y el cierre hablan en inglés; con `es` todo sigue igual.
- Darwin: abrir la página y cambiar a EN; más adelante, instalar en un proyecto de prueba en inglés.

## 6. Cierre
- [ ] Spec aprobada por Darwin antes de programar
- [ ] Línea en `.brain/decisions.log` al cerrar cada fase
- [ ] Ficha D-NNN: «nombres en español, contenido en dos idiomas»
