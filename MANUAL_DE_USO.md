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
3. Para el primer encargo, usa `/prompt-inicial` en el chat o el panel `/plantilla` (los dos se explican en la sección 3 bis).

## 3 bis. Empezar bien un chat: `/prompt-inicial`, `/plantilla` y las demás plantillas
Un encargo completo evita idas y vueltas. Hay dos ayudas para escribirlo; ambas piden lo mismo: **objetivo, cómo sabré que está bien, qué NO quiero, material, cómo trabajar** (spec con aprobación o rápido, modo auto o paso a paso), **plazos, costes, idioma y qué debo probar yo**. Te avisan de lo que falta y esperan tu visto bueno antes de actuar. En un proyecto ya empezado ofrecen además retomar el traspaso, un pendiente, una spec o el estado.

| Ayuda | Cómo se usa | Gasta IA extra |
|---|---|---|
| **`/prompt-inicial`** (skill) | Escribe `/prompt-inicial` en el chat. Viene incluida al instalar el arnés (carpeta `.claude/skills/prompt-inicial`); no hay que instalar nada más | No |
| **`/plantilla`** (panel visual, plugin `plantilla-prompt`) | Abre un panel con la plantilla para rellenar. Tiene un botón **Mejorar con IA**: reescribe el prompt armado con Haiku, te enseña la propuesta y tú eliges «Usar» o «Descartar»; nunca se envía sola | Un poco, solo si pulsas «Mejorar con IA» |

**Instalar el plugin `/plantilla` (una sola vez, en la app de escritorio):**
1. Pulsa el **+** junto a la caja del chat → **Agregar plugins**.
2. Pulsa **+** (Agregar marketplace) → **Agregar desde un repositorio**.
3. Escribe `forxa-ken/cerebro-vivo` y agrega el plugin `plantilla-prompt`.

En terminal, lo mismo:
```bash
claude plugin install plantilla-prompt --marketplace forxa-ken/cerebro-vivo
```
- **Ojo:** este repo está hoy solo en tu ordenador (subirlo a GitHub es el pendiente 1). Mientras no esté en GitHub, esa instalación no funcionará. Un repositorio privado también necesita que tengas la credencial de git para github.com.
- Si falta, el aviso de arranque (`arranque.py`) te lo recuerda. Más detalle en `plantilla-prompt/README.md` (en este repo) o en `.brain/mods/README.md` (en los proyectos que lo instalaron).
- **Para Gemini o Codex:** pídele a Claude «la versión para Gemini/Codex» y deja la plantilla en blanco en `.brain/biblioteca/PLANTILLA_PROMPT_INICIAL.md`.

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
- **Modo auto** (`modo_auto.py`): deja que la IA avance sola dentro de una spec aprobada y bloquea lo que se sale. Solo si tú lo activas; `desactivar` lo apaga.

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
