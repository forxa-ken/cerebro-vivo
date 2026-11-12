# Spec 045: `/diapositivas`, presentaciones para humanos sin instalar nada

- **Estado:** aprobada por Darwin el 2026-11-12 e implementada en 1.45.0; sin probar por Darwin en un trabajo real.
- **Fecha:** 2026-11-12
- **Origen:** idea vista en el gist «LLM Wiki» de Karpathy (Marp: diapositivas escritas en Markdown). Darwin: «así es más fácil de entender para los humanos» y pidió un sistema de uso fácil. Eligió la opción 1: script propio, sin dependencias.

## 1. Objetivo
Que Darwin pueda pedir «explícamelo en diapositivas» con **una sola orden** y obtener una presentación que se abre en el navegador, sin instalar nada y sin salir del método (Python estándar, es/en).

## 2. En alcance
- [ ] **`.brain/guardianes/diapositivas.py`**: convierte un `.md` (diapositivas separadas por una línea `---`) en **un solo `.html`** autocontenido (CSS y JS dentro, cero peticiones a internet, funciona sin conexión).
  - Uso: `python .brain/guardianes/diapositivas.py ARCHIVO.md [--salida RUTA.html] [--no-abrir]`. Por defecto escribe el `.html` junto al `.md` y lo abre en el navegador (`webbrowser`, librería estándar).
  - Markdown admitido (subconjunto pequeño y fijo): `# título`, `## subtítulo`, listas con `-` y numeradas, **negrita**, *cursiva*, `código`, bloques de código, citas `>`, enlaces `http(s)` y tablas simples. Una cabecera opcional `---` inicial con `titulo:` e `idioma:` (es/en).
  - **Seguridad:** el HTML que escriba el `.md` se escapa (no se pasa tal cual); solo enlaces `http`, `https` o relativos; el visor no ejecuta nada del contenido.
  - **Visor:** flechas, espacio, Inicio/Fin y clic para moverse; tecla `o` = vista general de todas; barra de progreso; texto grande y legible; claro u oscuro según el sistema; adaptado a móvil. **Imprimir (Ctrl+P → PDF)** da una diapositiva por página: así hay PDF sin instalar nada.
- [ ] **Skill `/diapositivas [tema]`** (es + `.en.md`), el sistema de uso fácil:
  - Sin tema: la IA elige **resumen del proyecto**. Con tema: `resumen`, `version` (última entrada de `CAMBIOS.md`), `traspaso`, `auditoria` (último informe) o texto libre de Darwin.
  - **`/diapositivas doc NOMBRE`** (o `/diapositivas NOMBRE` si coincide con un archivo): presenta un documento concreto de `.brain/biblioteca/`, `.brain/specs/` o la raíz (carta maestra, manual, una spec, un informe). La IA busca el archivo por nombre; si coinciden dos, pregunta cuál. Sin coincidencia, lo dice y no inventa.
  - **Documentos largos sin perder nada callado (modo `doc`):** el tope de 12 diapositivas **no aplica**. Reglas: (1) la primera diapositiva es un **índice** con todas las secciones (`##`) del documento; (2) **cada sección tiene al menos una diapositiva**, así nada se omite sin que se vea; (3) si pasa de 20 diapositivas, se parte en **partes** (`-parte-1.html`, `-parte-2.html`) enlazadas entre sí; (4) la última diapositiva dice qué documento se presentó y, si una sección se condensó mucho, cuál (con su ruta, para ir al original). El tope de 6 viñetas por diapositiva sigue.
  - La IA lee solo los archivos del tema, escribe `.brain/diapositivas/AAAA-MM-DD-tema.md` siguiendo la plantilla, lanza el script y dice en una línea dónde quedó. Darwin no escribe Markdown ni comandos.
  - Reglas de claridad para humanos (temas `resumen`, `version`, `traspaso`, `auditoria` y libre): máximo 12 diapositivas, máximo 6 viñetas por diapositiva, frases cortas y en llano (skill `explicar-a-darwin-en-llano`); lo no probado se marca como «sin probar»; nada inventado que no salga de los archivos.
- [ ] **Plantilla** `biblioteca/PLANTILLA_DIAPOSITIVAS.md` y `.en.md`: portada, «dónde estamos», «qué cambió», «qué falta», «qué debes probar», cierre con una pregunta.
- [ ] **Textos del script** (mensajes y errores) en `textos.py`, es y en. El visor toma su idioma de la cabecera `idioma:`.
- [ ] `.brain/diapositivas/` guarda los `.md` (se versionan) y se **ignora el `.html` generado** (se puede rehacer; el script deja un `.gitignore` local en esa carpeta, sin tocar el del proyecto). Solo el script, la skill y la plantilla se reparten a los proyectos (manifiesto), nunca las presentaciones.
- [ ] Una línea en el manual (`CEREBRO_VIVO.md` y `.en.md`), versión **1.45.0**, `CAMBIOS.md`, manifiesto.
- [ ] Pruebas del modo `doc`: se localiza el archivo por nombre; con dos coincidencias no elige solo; el índice lista todas las secciones; cada `##` del original aparece en alguna diapositiva (comprobación automática del `.md` generado frente al original); partición en partes a partir de 20.
- [ ] Pruebas: el parser (títulos, listas, tablas, escapado de HTML, `---`), el `.html` tiene tantas diapositivas como separadores y ninguna petición externa, salida en UTF-8 en consola de Windows, `--no-abrir` no abre nada, paridad es/en, manifiesto al día.

## 3. Fuera de alcance
- Exportar a PowerPoint o PDF con Marp (queda como posible mejora: solo si `marp` ya está instalado).
- Imágenes, vídeo, animaciones, notas del orador, temas de colores a elegir, edición en el navegador.
- Un guardián que bloquee o avise de algo: `/diapositivas` es una herramienta que Darwin pide, no un aviso automático.
- Cambiar el resto del arnés, el arranque o los textos que no sean de esta función.

## 4. Riesgos
- **La IA rellena diapositivas con cosas que no están en los archivos.** Mitigación: la skill manda leer primero y citar el archivo de origen en la última diapositiva; lo no probado se dice.
- **Markdown con HTML malicioso o enlaces `javascript:`.** Mitigación: escapado y lista corta de enlaces permitidos, con prueba.
- **Consola de Windows y tildes.** Mitigación: salida UTF-8 y la prueba de la skill `probar-guardian-en-windows`.
- **Presentaciones viejas que enseñen datos desactualizados.** Mitigación: la fecha va en el nombre y en la portada; los `.html` no se versionan.

## 5. Archivos
`.brain/guardianes/diapositivas.py`, `textos.py`, `.claude/skills/diapositivas/SKILL.md` y `.en.md`, `.brain/biblioteca/PLANTILLA_DIAPOSITIVAS.md` y `.en.md`, `tests/test_diapositivas.py`, `.brain/experiencia/indice.md`, `.brain/biblioteca/kit-arranque/instalar.py`, `generar_manifiesto.py`, `CEREBRO_VIVO.md` y `.en.md`, `VERSION` (1.45.0), `CAMBIOS.md`, `manifiesto.json`.

## 6. Verificación
`python -m unittest discover tests` en verde. Prueba real de Darwin: escribir `/diapositivas`, ver que se abre el navegador con el resumen, moverse con las flechas, pulsar `o` e imprimir a PDF. **Sin probar** hasta que Darwin lo haga.

## 7. Cierre
- [ ] Spec aprobada por Darwin antes de programar
- [ ] Pruebas en verde y manifiesto regenerado
- [ ] Línea añadida a `.brain/decisions.log`
- [ ] Punto 49 pasa a «Esperando tu prueba»
