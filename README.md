# cerebro-vivo

[Read it in English](README.en.md)

El **meta-arnés «Cerebro Vivo»**: un método para trabajar con una IA sin perder el contexto entre chats y gastando pocos tokens, más las herramientas que lo hacen cumplir. Un solo repositorio, y cada proyecto decide cuándo traerse las mejoras.

**Manual de uso para el día a día: [`MANUAL_DE_USO.md`](MANUAL_DE_USO.md).**

## Fuentes
- Lee, Yoonho; Nair, Roshen; Zhang, Qizheng; Lee, Kangwook; Khattab, Omar; Finn, Chelsea. *Meta-Harness: End-to-End Optimization of Model Harnesses*. arXiv:2603.28052, marzo de 2026 (https://arxiv.org/abs/2603.28052): artículo de Stanford sobre el término «meta-harness».
- Databricks. *Introducing Omnigent: a meta-harness to combine, control and share your agents*, junio de 2026 (https://www.databricks.com/blog/introducing-omnigent-meta-harness-combine-control-and-share-your-agents): capa de orquestación sobre agentes de IA.
- Nygard, Michael. *Documenting Architecture Decisions*, noviembre de 2011 (https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions): origen de los registros de decisiones (ADR), base de `decisions.log` y `decisions/`.
- Fowler, Martin. *Architecture Decision Record* (https://www.martinfowler.com/bliki/ArchitectureDecisionRecord.html): el registro de decisiones como conjunto de ADR.
- Microsoft. *Maintain an architecture decision record (ADR)*, Azure Well-Architected Framework (https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record).
- Red Hat. *Why you should be using architecture decision records to document your project* (https://www.redhat.com/en/blog/architecture-decision-records).
- InfoQ. *AWS Publishes Guide to Architecture Decision Records*, junio de 2022 (https://www.infoq.com/news/2022/06/aws-adr-guide/): guía de AWS sobre ADR.
- GitHub (Microsoft). *Spec Kit*, repositorio `github/spec-kit`, agosto de 2025, licencia MIT (https://github.com/github/spec-kit): desarrollo guiado por especificaciones; origen de la «constitución» (`constitution.md`) como reglas del proyecto, como en este método. Su README indica crearla una vez por proyecto.
- GitHub. *Spec-Driven Development* (`spec-driven.md`) (https://github.com/github/spec-kit/blob/main/spec-driven.md): define la constitución como un conjunto de principios inmutables, con un proceso de enmiendas con fecha.
- Delimarsky, Den. *Spec-driven development with AI: get started with a new open source toolkit*, GitHub Blog, 2 de septiembre de 2025 (https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/): anuncio del Spec Kit (no nombra la constitución).

La implementación es propia, centrada en el trabajo colaborativo entre agentes de IA y la persistencia del contexto entre chats.

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

