# Guía paso a paso: instalar y actualizar Cerebro Vivo en un proyecto

Vale para cualquier proyecto (`RUTA_PROYECTO`) y para los tres entornos de IA: **Claude Code**, **Antigravity/Gemini** y **GPT Codex**. Versión del arnés al escribirla: 1.5.1.

## Dónde viven las skills

| Entorno | Ruta dentro del proyecto | Cómo llegan |
| :--- | :--- | :--- |
| Claude Code | `.claude/skills/` | Las pone el instalador y las mantiene el actualizador. |
| GPT Codex (y Antigravity a nivel de proyecto) | `.agents/skills/` | Desde la 1.5.0 el instalador y el actualizador las copian solos **si el proyecto tiene `AGENTS.md`**. Se invocan con `$nombre`, no con `/`. |
| Antigravity/Gemini global (opcional, antiguo) | `%USERPROFILE%\.gemini\config\plugins\cerebro-vivo\` | Plugin del repo viejo `cerebro-vivo-plugins`. **Está desfasado:** tiene una `plantilla` antigua y no tiene `resumen`, `pendiente` ni los cambios de `prompt-inicial`. Para Gemini conviene usar las skills de `.agents/skills/` de cada proyecto. |

**Panel `/plantilla` («Prompt inicial»):** es un plugin de Claude Code aparte (carpeta `plantilla-prompt/`, del repo viejo `cerebro-vivo-plugins`) que abre un formulario con botones para escribir el encargo (tipo de tarea, objetivo, cómo sabré que está bien, qué NO quiero) y lo inserta en el chat o lo guarda en blanco como `.md` para Gemini/Codex. Funciona en el equipo donde está instalado el plugin. Vive en este repo (carpeta `plantilla-prompt/`, recuperada en la 1.7.0) pero **no es un archivo de proyecto**: `actualizar_arnes.py` no lo instala ni lo actualiza. Se instala una vez por equipo en Claude Code (`/plugin marketplace add RUTA_DE_ESTE_REPO` y `/plugin install plantilla-prompt@cerebro-vivo`, o copiando la carpeta; detalle en `plantilla-prompt/README.md`) y se actualiza trayendo el repo y repitiendo ese paso. Sus botones de estado ponen `/pendiente` y `/resumen` en el chat. Para el encargo escrito a mano, `/prompt-inicial` sigue siendo la skill del arnés.

Skills actuales (18): `cero-dependencias`, `cerrar-una-tarea`, `explicar-a-darwin-en-llano`, `guardian-avisa-o-bloquea`, `implementada-no-es-hecha`, `licencia-antes-de-usar`, `mover-no-borrar`, `pendiente`, `pendientes-solo-lo-que-falta`, `probar-guardian-en-windows`, `prompt-inicial`, `quitar-codigo-antiguo-con-test`, `resumen`, `secretos-fuera-del-repo`, `spec-antes-de-programar`, `traspaso-in`, `traspaso-out`, `vigilar-librerias`.

## Paso 1 — Instalar el kit en un proyecto nuevo

**Opción A, con ventana:** doble clic en `instalar_kit.bat` (abre `instalar_gui.py`) y rellenar carpeta, nombre, dueño, idioma, comando de pruebas, IA que se usarán y nivel (`Completo` para memoria + guardianes + skills + pruebas).

**En Mac (spec 013, sin probar en un Mac real):** doble clic en `instalar_kit.command` (si no abre: `chmod +x instalar_kit.command` en Terminal una vez); necesita `python3` y tkinter.

**Opción B, por terminal:**
```powershell
python "RUTA_REPO_ARNES\.brain\biblioteca\kit-arranque\instalar.py" "RUTA_PROYECTO" --nombre NOMBRE --dueno DUENO --idioma español --pruebas "python -m unittest discover tests" --ias claude,gemini,codex --nivel completo
```

**Comprobación tras instalar:**
```powershell
python "RUTA_PROYECTO\.brain\biblioteca\kit-arranque\instalar.py" "RUTA_PROYECTO" --comprobar
```

Qué crea (nivel completo): `.brain/` (memoria, constitución, pendientes, specs), los guardianes, un índice por IA (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`), los hooks de `.claude/settings.json`, las skills y **`.brain/architecture/objetivo.md`** (desde la 1.5.0).

**Después de instalar:** rellenar `objetivo.md` (objetivo, cómo sabremos que está bien, qué NO queremos). Todas las IA lo leen primero.

## Paso 2 — Skills de Codex

Con `AGENTS.md` presente, el paso 1 ya deja las skills en `.agents/skills/`. No hace falta adaptarlas a mano. Para usarlas en un chat nuevo de Codex: `$resumen`, `$pendiente`, `$prompt-inicial`.

## Paso 3 — Actualizar un proyecto ya instalado

Desde el proyecto:
```powershell
python .brain/guardianes/actualizar_arnes.py --simular
python .brain/guardianes/actualizar_arnes.py
```
La primera línea solo enseña qué cambiaría. La segunda lo aplica y guarda copia en `.brain/copias_arnes/`. No pisa lo que modificaste a mano.

**Qué trae:** guardianes, skills (también a `.agents/skills/` si hay `AGENTS.md`), manual, plantillas y pruebas del método.

**Proyecto que ya estaba instalado antes de la 1.5.0:** el objetivo no llega con la actualización normal (son archivos del proyecto). Después de actualizar, lanza la migración, que solo añade y guarda copia:
```powershell
python .brain/guardianes/actualizar_arnes.py --migrar-objetivo --simular
python .brain/guardianes/actualizar_arnes.py --migrar-objetivo
```
Crea `.brain/architecture/objetivo.md` si falta (con «pendiente de escribir»), enlaza el objetivo en `CLAUDE.md`, `GEMINI.md` y `AGENTS.md`, y añade la regla a la constitución. Si algún índice está tan cambiado que no encuentra el sitio, no lo toca y te dice la línea exacta que pegar. Repetirla no cambia nada. Después hay que **escribir el objetivo real** en `objetivo.md`.

**La actualización no es automática:** nada se actualiza solo. Hay que lanzar el comando en cada proyecto (lee el repo de `arnes_repo` en `guardianes.json`, o una dirección git).

## Paso 4 — Probar que funciona

En un chat nuevo: `/resumen` (Codex: `$resumen`) debe contar el estado; `/pendiente` debe dar un menú; preguntar «¿cuál es el objetivo?» debe responderse desde `objetivo.md`.
