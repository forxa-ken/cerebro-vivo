# Manual de uso de Cerebro Vivo (para Darwin)

Guía práctica, sin jerga. Para el porqué de cada cosa está `.brain/biblioteca/CEREBRO_VIVO.md`; este manual responde a «¿qué hago yo y cuándo?». Versión del arnés al escribirlo: 1.3.1.

## 1. Qué es, en una frase
Un conjunto de carpetas, avisos automáticos y costumbres para que la IA **recuerde lo acordado entre chats** y no te haga repetirlo. La memoria vive en la carpeta `.brain/` de cada proyecto.

## 2. Qué sabemos y qué no (medido el 2026-11-01)
- **Demostrado:** al retomar un trabajo en un chat nuevo, con el arnés se respetó lo acordado 5 de 5 veces; sin él, 0 de 5.
- **Demostrado:** en tareas pequeñas gasta de un 7 % a un 16 % **más**. No ahorra ahí.
- **Demostrado (un solo proyecto, ~80 fichas):** tener índice no mejoró el acierto y salió ~19 % más caro; con el índice roto tampoco falló nadie.
- **Sin medir:** que ahorre a la larga en un proyecto real. Es una idea razonable, no un hecho.
- Úsalo donde hay **muchos chats seguidos** sobre lo mismo. En una tarea suelta no compensa.

## 3. Empezar un proyecto nuevo
1. Doble clic en `instalar_kit.bat` (abre una ventana), o en terminal:
```bash
python .brain/biblioteca/kit-arranque/instalar.py RUTA_DEL_PROYECTO --nombre MiProyecto --dueno Darwin --nivel completo
```
2. Abre un chat en la carpeta del proyecto. El arranque mostrará solo un resumen del estado.
3. Para el primer encargo, usa `/prompt-inicial` en el chat (se explica en la sección 3 bis).

## 3 bis. Empezar bien un chat: `/prompt-inicial` y las demás plantillas
Un encargo completo evita idas y vueltas. **`/prompt-inicial`** te ayuda a escribirlo: escribe `/prompt-inicial` en el chat. Viene incluida al instalar el arnés (carpeta `.claude/skills/prompt-inicial`), no hay que instalar nada más y no gasta IA extra.

Te pide **objetivo, cómo sabré que está bien, qué NO quiero, material, cómo trabajar** (spec con aprobación o rápido, paso a paso), **plazos, costes, idioma y qué debo probar yo**. Te avisa de lo que falta y espera tu visto bueno antes de actuar. En un proyecto ya empezado ofrece además retomar el traspaso, un pendiente, una spec o el estado.

**Para Gemini o Codex:** pídele a Claude «la versión para Gemini/Codex» y deja la plantilla en blanco en `.brain/biblioteca/PLANTILLA_PROMPT_INICIAL.md`.

*(El panel `/plantilla` y su plugin se quitaron en la versión 1.4.0 por poco útiles.)*

**Otras plantillas que usa el método (ya vienen con el arnés):**
| Plantilla | Para qué | Dónde |
|---|---|---|
| Traspaso | Pasar de un chat a otro sin perder nada | `.brain/biblioteca/PLANTILLA_TRASPASO.md` |
| Nota de chat auxiliar | Dejar lo que hizo un chat que recibió un encargo de otro | `.brain/biblioteca/PLANTILLA_NOTA_CHAT.md` |
| Spec | Plan corto que apruebas antes de programar | `.brain/specs/_template.md` |
| Ficha de decisión | Por qué se decidió algo (`D-NNN`) | `.brain/decisions/_template.md` (la crea el kit en cada proyecto) |
| Registro de pruebas | Qué te toca probar y cómo | `.brain/pruebas/_plantilla.md` |

## 4. Un día normal de trabajo
- **Al abrir un chat:** la IA te resume en 4-5 viñetas dónde se quedó. Si no lo hace, pídeselo.
- **Mientras trabajas:** tareas pequeñas (hasta 2 archivos) van por el carril rápido. Cambios grandes o delicados (pagos, base de datos, licencias) piden una **spec** primero: un papel corto con objetivo, qué entra, qué no y cómo se prueba. Tú la apruebas antes de que se programe.
- **Al terminar una tarea:** la IA anota una línea en `.brain/decisions.log`. Si se le olvida, un aviso automático se lo recuerda. A mano:
```bash
python .brain/guardianes/cerrar.py --chat "Proyecto #N" "qué se hizo"
```
- **Cuando pruebas algo y funciona:** díselo en el chat; la IA lo pasa de `pendientes.md` a `hechos`.
- **Lo irreversible se pregunta:** subir a GitHub, borrar, gastar. No lo hace sin tu orden.

## 5. Cambiar de chat sin perder nada
- Un chat largo cuesta más y se vuelve torpe. Cuando te lo avise, o cuando lleves mucho rato, pide «prepara el traspaso y el chat nuevo».
- La IA escribe `.brain/traspaso.md` (qué pediste, qué se decidió, qué falta, qué NO hacer). El chat nuevo lo muestra solo al arrancar.
- Si un chat auxiliar recibe un encargo de otro, deja su nota en `.brain/notas-chats/`.

## 6. Dónde está cada cosa
| Qué buscas | Dónde |
|---|---|
| Lo que falta por hacer | `.brain/pendientes.md` |
| Lo que ya se hizo y probaste | `.brain/archive/hechos-indice.md` (el detalle, en `hechos.md`) |
| Qué se hizo y cuándo | `.brain/decisions.log` |
| Por qué se decidió algo | `.brain/decisions/indice.md` y sus fichas `D-NNN` |
| Reglas que no se tocan | `.brain/constitution.md` |
| Planes aprobados | `.brain/specs/` |
| El método completo | `.brain/biblioteca/CEREBRO_VIVO.md` |

**Los índices (`decisions/indice.md`, `archive/hechos-indice.md`) son a demanda:** el arranque no los lee; solo se abren cuando hace falta buscar una ficha. En la prueba (spec 004, ~80 fichas) no mejoraron el acierto y costaron algo más, así que se mantienen pero sin cargarlos siempre. Los archivos de entrada (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`) se mantienen cortos y con enlaces al cerebro.

**Gemini y Codex:** `/prompt-inicial` y los ganchos de Claude Code (el resumen automático al abrir y el aviso al cerrar) no funcionan allí; el proyecto se adapta al método escrito en `GEMINI.md` / `AGENTS.md`. En Codex las skills se invocan con `$prompt-inicial` y deben estar en `.agents/skills/` (Codex no lee `.claude/skills/`). Abre siempre un chat nuevo: un chat ya abierto no recarga el archivo de entrada.

## 7. Traer mejoras a un proyecto que ya lo usa
Primero **simular** (no escribe nada), luego actualizar:
```bash
python .brain/guardianes/actualizar_arnes.py --simular
python .brain/guardianes/actualizar_arnes.py
```
Guarda una copia antes, no pisa lo que cambiaste a mano y nunca toca tus pendientes, specs, decisiones ni registro. Un proyecto antiguo sin registro previo usa `--forzar-todo`, **solo** después de ver la lista con `--simular`.

## 8. Medir si te está ayudando
```bash
python .brain/guardianes/medir.py
```
Enseña por chat el coste, los mensajes tuyos y cuántas veces tuviste que corregir a la IA. Ideas para un proyecto real: apuntar la media **antes** de poner el arnés, ponerlo, y comparar 3-4 semanas después. Otras opciones: `--comparar CARPETA_CON CARPETA_SIN`, `--tarea TEXTO` (solo un tipo de tarea), `--desglose ID` (un chat mensaje a mensaje). Solo lee; no cambia nada.

## 9. Avisos y guardianes que verás
- **Arranque** (al abrir un chat): estado real de pendientes, commits sin subir, última línea del registro.
- **Cierre** (al acabar una respuesta): avisa si falta la línea del registro. Una sola vez.
- **Modo ligero:** en tareas pequeñas con pruebas en verde, la línea del registro se escribe sola.
- **Secretos:** `python .brain/guardianes/secretos.py` busca claves o datos personales; `--historial` revisa también lo ya guardado en git. Pásalo antes de subir nada a internet.

## 10. Reglas para ti
- No subas nada a GitHub sin pasar por `secretos.py` y sin decidirlo tú.
- Si un resultado «parece demasiado bueno», pide que lo pruebe y lo diga como no probado si no pudo.
- Tras cambiar cualquier archivo **de este repo**: subir `VERSION`, anotar `CAMBIOS.md`, `python generar_manifiesto.py` y `python -m unittest discover tests`.

## 11. Cuando algo no va
| Síntoma | Qué hacer |
|---|---|
| No sale el resumen al abrir el chat | Pídele a la IA que ejecute `python .brain/guardianes/arranque.py` |
| Te pide leer demasiado | Chat nuevo con traspaso; los chats largos son lo que más cuesta |
| Un aviso se repite o molesta | Díselo; los topes están en `.brain/guardianes/guardianes.json` |
| Dudas de si algo se rompió al actualizar | `python -m unittest discover tests` y las copias están en `.brain/copias_arnes/` |
