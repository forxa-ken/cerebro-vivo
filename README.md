# cerebro-vivo

El **meta-arnés «Cerebro Vivo»**: un método para trabajar con una IA sin perder el contexto entre chats y gastando pocos tokens, más las herramientas que lo hacen cumplir. Un solo repositorio, y cada proyecto decide cuándo traerse las mejoras.

## Qué lleva
- **Guardianes** (`.brain/guardianes/`): arranque, cierre, cerrar, poda, tokens, secretos, librerías, pruebas, longitud, análisis, base de datos, índices, notas de chats y **modo auto**.
- **Manual y carta** (`.brain/biblioteca/CEREBRO_VIVO.md`, `CARTA_META_ARNES.md`), plantillas de traspaso y nota de chat.
- **Kits**: de arranque (monta el método en un proyecto nuevo) y de traducción es/en/pt.
- **Skills** genéricas en `.claude/skills/` (incluida `/prompt-inicial`) y sus **pruebas** en `tests/`.
- **Plugin `/plantilla`** (`plantilla-prompt/`) con su `marketplace.json`: el repo también es el marketplace.

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
`--simular` solo enseña qué cambiaría. Al actualizar se guarda antes una copia en `.brain/copias_arnes/`, **no se pisa** lo que el proyecto modificó a mano (se lista; `--forzar RUTA` lo pisa) y nunca se tocan pendientes, specs, decisiones, registro ni `guardianes.json` (las claves nuevas solo se proponen). Al final corre las pruebas del método del proyecto.

## Para mejorar el arnés
Cambiar aquí, subir `VERSION`, anotar en `CAMBIOS.md`, lanzar `python generar_manifiesto.py` y las pruebas (`python -m unittest discover tests`).

## Instalar el plugin `/plantilla`
En la app de escritorio: **+** junto a la caja del chat → **Agregar plugins** → **+** (Agregar marketplace) → **Agregar desde un repositorio** → `forxa-ken/cerebro-vivo` → agregar `plantilla-prompt`. En terminal: `claude plugin install plantilla-prompt --marketplace forxa-ken/cerebro-vivo`. Un repo privado necesita credencial de git para github.com.
