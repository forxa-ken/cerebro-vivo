# cerebro-vivo

El **meta-arnés «Cerebro Vivo»**: un método para trabajar con una IA sin perder el contexto entre chats y gastando pocos tokens, más las herramientas que lo hacen cumplir. Un solo repositorio, y cada proyecto decide cuándo traerse las mejoras.

**Manual de uso para el día a día: [`MANUAL_DE_USO.md`](MANUAL_DE_USO.md).**

## Qué lleva
- **Guardianes** (`.brain/guardianes/`): arranque, cierre, cerrar, poda, medidor, secretos, librerías, pruebas, longitud, análisis, base de datos, índices, notas de chats.
- **Manual y carta** (`.brain/biblioteca/CEREBRO_VIVO.md`, `CARTA_META_ARNES.md`), plantillas de traspaso y nota de chat.
- **Plugin `/plantilla`** (`plantilla-prompt/`, panel de Claude Code; se instala aparte, no lo reparte el actualizador).
- **Kits**: de arranque (monta el método en un proyecto nuevo) y de traducción es/en/pt.
- **Skills** genéricas en `.claude/skills/` (incluidas `/prompt-inicial`, `/resumen` y `/pendiente`) y sus **pruebas** en `tests/`.

## Qué está demostrado y qué no (medición de 2026-11-01, specs 001-003)
- **Demostrado:** al retomar un trabajo en un chat nuevo, con el arnés se respetó lo acordado 5 de 5 veces; sin él, 0 de 5 (inventaba el formato). En tareas sueltas y pequeñas los dos funcionan igual.
- **Coste:** en tareas pequeñas el arnés gasta de un 7 % a un 16 % más que no usarlo (caché igualada, sonnet 5.5). No ahorra en esas tareas.
- **Hipótesis (sin medir aún):** en un proyecto real y largo, el arnés ahorra a la larga porque evita repetir explicaciones y rehacer trabajo por errores; sin método, esas repeticiones cuestan más. Se comprueba con `python .brain/guardianes/medir.py` en proyectos reales durante semanas.
- **Índices (spec 004, un solo proyecto real):** con ~80 fichas, tener índice no mejoró el acierto (30/30 en los tres casos) y salió ~19 % más caro que no tenerlo; un índice con filas falsas tampoco hizo fallar. No se demuestra que el índice ahorre a ese tamaño.
- Detalle: `.brain/specs/001-resultados.md`, `002-resultados.md`, `003-resultados.md`, `004-resultados.md`.

## Empezar un proyecto nuevo
```bash
python .brain/biblioteca/kit-arranque/instalar.py RUTA_PROYECTO --nombre Mi --dueno Ana --nivel completo
```
(o doble clic en `instalar_kit.bat`). Anota en el proyecto de dónde se actualiza (`arnes_repo` en `.brain/guardianes/guardianes.json`).

## Traer las mejoras a un proyecto que ya lo usa
Desde el propio proyecto:
```bash
python .brain/guardianes/actualizar_arnes.py --simular
python .brain/guardianes/actualizar_arnes.py
```
O desde este repo:
```bash
python actualizar.py RUTA_PROYECTO --simular
python actualizar.py RUTA_PROYECTO
```
`--simular` solo enseña qué cambiaría. Al actualizar se guarda antes una copia en `.brain/copias_arnes/` y **no se pisa** lo que el proyecto modificó a mano (se lista; `--forzar RUTA` lo pisa). Lo que el arnés retiró sale del proyecto a esa copia, salvo que se haya modificado. Nunca se tocan pendientes, specs, decisiones ni registro; en `guardianes.json` solo se añaden las claves que falten, sin cambiar las que hay. Un proyecto de nivel ligero o medio no recibe nada. Al final corre las pruebas del método del proyecto.

## Para mejorar el arnés
Cambiar aquí, subir `VERSION`, anotar en `CAMBIOS.md`, lanzar `python generar_manifiesto.py` y las pruebas (`python -m unittest discover tests`).

