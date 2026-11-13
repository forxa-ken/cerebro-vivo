# Spec 042: varias IA que colaboran en un proyecto, y Gemini como obrera de la fábrica (punto 19)

- **Estado:** aprobada por Darwin el 2026-11-12 y programada en 1.42.0 (la parte B, Gemini como obrera, retirada por Darwin el 2026-11-13: Google cerró el comando `gemini` para cuentas personales y no se quiere pagar)
- **Fecha:** 2026-11-12
- **Cierra:** la parte que quedaba abierta del punto 19 (la fábrica con directora ya está en la spec 035). Recoge además el requisito R12 de la spec 035 (`indices_ajenos`), nunca programado.
- **Pedido por Darwin el 2026-11-12:** (1) incluir a Gemini como obrera de la fábrica; (2) especificar las IA colaborativas.

## 1. Objetivo
Que Claude, Codex y Gemini trabajen a la vez en un mismo proyecto sin pisarse: cada una con su papel, sus archivos y su forma de leer las reglas. Y que la directora de la fábrica pueda elegir a Gemini como obrera igual que hoy elige a Claude o a Codex.

## 2. Qué se sabe y qué no
- **Sabido (repo):** hoy `revisar_indices.py` ya lee `CLAUDE.md`, `GEMINI.md` y `AGENTS.md`. La carta de la ejecutora (`CARTA_EJECUTORA.md`) ya dice «Claude o Codex». Codex se lanza por comando (`codex exec`); Claude, como subagente.
- **Sabido (internet, fuentes de terceros, sin verificar contra la versión instalada):** Gemini CLI se lanza sin pantalla con `gemini -p "ORDEN"`. Su modo de aprobación se fija con `--approval-mode` (`default`, `auto_edit`, `yolo`, `plan`); sin aprobación automática se queda esperando. Puede pedir confianza en la carpeta la primera vez.
- **Instalado el 2026-11-12 (orden de Darwin):** Gemini CLI 0.68.0 (`npm install -g @google/gemini-cli`). Su `--help` confirma los indicadores `-p`, `--approval-mode` (`default`, `auto_edit`, `yolo`, `plan`), `--skip-trust`, `-s` y `--include-directories`.
- **No sabido:** **no ha iniciado sesión con la cuenta de Google de Darwin**, así que ningún encargo se ha ejecutado todavía con Gemini: el inicio de sesión lo hace él. Qué archivo de reglas lee por defecto (`GEMINI.md` frente a `AGENTS.md`) y si la obrera Gemini tiene Python en su caja, se comprueba en el primer encargo mínimo.

## 3. En alcance
### Cómo encajan los modos y los archivos de entrada (aclaración de Darwin, 2026-11-12)
- **Modo normal** (una sola IA): no cambia nada. Si trabaja Claude, manda `CLAUDE.md`; si trabaja Gemini, `GEMINI.md`; si trabaja Codex, `AGENTS.md`. Cada uno con su índice propio, como hoy. Con una sola IA no hay nada que repartir.
- **Modo fábrica** (directora y obreras): ya existe y se activa con `/fabrica si`.
- **Colaboración** (varias IA con papeles): se tratará como una **capa que se añade solo cuando el proyecto la activa**, no como un modo nuevo ni como una reescritura de los tres índices.
- **Un archivo adicional**, `.brain/colaboracion.md`, con la matriz de papeles y las reglas para no pisarse. Los tres índices no se reescriben: cada uno recibe **una sola línea** que remite a ese archivo, y solo en los proyectos que activan la colaboración. Así no se repite ninguna regla y el modo normal queda intacto.
- `biblioteca/IAS_COLABORATIVAS.md` (es/en) es la **plantilla** de ese archivo; el proyecto copia la suya a `.brain/colaboracion.md` y la adapta.

### A. IA colaborativas
- [ ] **Comando `/colabora si|no|estado`** (como `/fabrica`): ajuste `modo_colaborativo` en `guardianes.json`, apagado por defecto. Con `si`: crea `.brain/colaboracion.md` desde la plantilla si no existe, añade la línea de remite en los índices que existan (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`) y el arranque dice «MODO COLABORATIVO ACTIVADO». Con `no`: quita esas líneas y el aviso (el archivo `colaboracion.md` se conserva, mover-no-borrar). Con `estado` o sin palabra: solo muestra cómo está. Se pide como skill `colabora` (es/en) y script `colabora.py`. No abre ningún chat nuevo.
- [ ] **Matriz de papeles**, dentro de esa plantilla (es/en): por cada IA, qué archivos lee, cuáles puede escribir y cuáles nunca. Propuesta de partida: Claude, dueña de `.brain/` y del código; Codex, solo lo que diga el encargo, en su worktree; Gemini, solo lo que diga el encargo (por ejemplo traducciones). Nadie escribe en `.brain/decisions.log` salvo quien cierra.
- [ ] **Una IA, un archivo de entrada:** `CLAUDE.md` (Claude), `AGENTS.md` (Codex y quien lo lea), `GEMINI.md` (Gemini). Cada uno remite a las mismas reglas; ninguno las repite (cada regla se escribe una sola vez).
- [ ] **`indices_ajenos` (R12)** en `guardianes.json`: lista de archivos de índice que el instalador y `actualizar_arnes.py` **no tocan** aunque se use `--ias gemini` o `--ias codex`. Se programa en el instalador y en el actualizador.
- [ ] **No pisarse:** regla única en la matriz: dos IA escritoras nunca comparten carpeta de trabajo (worktree y rama distintos, como ya exige la fábrica); lo que edite una, la otra lo ve solo tras el commit.
- [ ] **Notas entre IA:** cada IA deja su nota en `.brain/notas-chats/` (ya existe la plantilla); el guardián de arranque las muestra a la siguiente.
- [ ] Prueba en `tests/` de que `indices_ajenos` se respeta en instalar y actualizar, y de que el documento existe en es y en.

### B. Gemini como obrera de la fábrica
- [ ] Skill `directora-de-fabrica` (es/en): nueva viñeta «Si la ejecutora es Gemini»: lanzarla por comando con `gemini -p`, sin pedir permiso en cada lanzamiento, en el worktree del encargo, con entrada cerrada y tope de 900 s, igual que Codex; modo de aprobación `auto_edit` por defecto (la directora no usa `yolo`); mismas reglas de fallos (un fallo se relanza, dos seguidos se pregunta).
- [ ] `CARTA_EJECUTORA.md` y `.en.md`: «Claude, Codex o Gemini»; el nombre de la IA que ejecuta se anota en el campo «Ejecutora» del encargo.
- [ ] La directora puede elegirla por encargo si la carta dice «la que decida la directora». Criterio sugerido: Gemini para encargos de texto, traducciones o documentación; no para seguridad ni dinero.
- [ ] **Gasto:** `medir.py --fabrica` hoy lee los registros de Codex. Para Gemini no hay lector; se anota a mano con `fabrica.py gasto` y se dice en la nota que no se mide solo.
- [ ] **Si `gemini` no está instalado**, la directora no lo inventa: se lo dice a Darwin y vuelve al texto para pegar a mano, igual que con Codex.

## 4. Fuera de alcance
- Instalar Gemini CLI o configurarlo con la cuenta de Darwin: lo decide y lo hace él.
- Medir el gasto de Gemini automáticamente (no hay registros conocidos).
- Cambiar a Claude o a Codex como obreras, o los topes de la fábrica.
- Más IA (Cursor, Copilot…).

## 5. Riesgos
- **Documentar un comando sin haberlo ejecutado.** Mitigación: las viñetas de Gemini se marcan «no probado con Gemini» hasta que Darwin instale `gemini` y corra una prueba mínima (un encargo de una sola traducción).
- Gemini puede leer otro archivo de reglas del esperado; hasta comprobarlo, el encargo lleva las reglas copiadas dentro del propio texto.
- Más IA significa más superficie para pisarse; por eso la regla de worktree por escritora no admite excepciones.

## 6. Preguntas para Darwin
1. ¿Gemini obrera para qué tipo de encargos? **Respondida: texto, traducciones y documentación; nunca seguridad ni dinero.**
2. ¿Instalar Gemini CLI? **Respondida: sí; instalado el 2026-11-12 (0.68.0).** Falta que Darwin inicie sesión.
3. ¿Los papeles de la matriz de la sección 3A? **Sin responder; Darwin preguntó antes cómo quedan los archivos y se resolvió con el archivo adicional `.brain/colaboracion.md`.**

## 7. Archivos
`biblioteca/IAS_COLABORATIVAS.md` y `.en.md` (nuevos), `directora-de-fabrica/SKILL.md` y `.en.md`, `CARTA_EJECUTORA.md` y `.en.md`, instalador y `actualizar_arnes.py`, `guardianes.json`, `textos.py` (si hay avisos), `CLAUDE.md` (una línea), `tests/`, `VERSION`, `CAMBIOS.md`, `manifiesto.json`.

## 8. Verificación
`python -m unittest discover tests` en verde. Prueba de `indices_ajenos` con un proyecto de juguete que tenga un `AGENTS.md` ajeno. La parte de Gemini queda **no probada** hasta que `gemini` esté instalado y se corra un encargo mínimo.

Fuentes consultadas (terceros, sin verificar): [referencia de Gemini CLI](https://geminicli.com/docs/cli/cli-reference.md), [modo headless](https://gemini-cli-site.pages.dev/docs/en/cli/headless).
