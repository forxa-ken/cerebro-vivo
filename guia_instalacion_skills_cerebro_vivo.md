# Guía paso a paso: Instalación de las Skills y el Meta-Arnés «Cerebro Vivo»

Este documento registra con exactitud los pasos realizados en este equipo y en el proyecto `F:\Modelo` para dejar instaladas y operativas las **skills de Cerebro Vivo** en los tres entornos de IA (**Antigravity/Gemini**, **Claude Code** y **GPT Codex**).

---

## Resumen rápido: dónde viven las skills en tu equipo

En tu configuración existen **3 niveles complementarios** donde están instaladas las skills de Cerebro Vivo:

| Nivel / Entorno | Ruta donde viven las skills | Quién las lee | Cómo se instalaron |
| :--- | :--- | :--- | :--- |
| **1. Plugin global de Antigravity** | `C:\Users\darwi\.gemini\config\plugins\cerebro-vivo\skills\` | **Antigravity / Gemini** (en cualquier proyecto) | Clonando/copiando el plugin `cerebro-vivo` en la carpeta global de plugins de Antigravity. |
| **2. Kit de proyecto y skills de Claude** | `F:\Modelo\.claude\skills\` + `F:\Modelo\.brain\` | **Claude Code** (y guardianes del proyecto) | Ejecutando el instalador del kit de arranque (`instalar_kit.bat` / `instalar.py`) desde `F:\Proyectos Antigravity\cerebro-vivo`. |
| **3. Skills locales del proyecto para Codex / Agentes** | `F:\Modelo\.agents\skills\` | **GPT Codex** y **Antigravity** (a nivel de proyecto) | Adaptando e instalando las 15 skills desde `.claude/skills/` a `.agents/skills/` y validándolas con `quick_validate.py` (`Spec 005`). |

---

## Paso 1 — Instalar el Kit de Arranque de «Cerebro Vivo» en el proyecto (`F:\Modelo`)

Este paso creó toda la memoria persistente (`.brain/`), los 14 guardianes automáticos (`.brain/guardianes/`), los tres índices espejo (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`), los hooks de `.claude/settings.json` y las 14 skills originales en `.claude/skills/`.

### Opción A: Con ventana gráfica (la más cómoda)
1. Ir a la carpeta del repositorio matriz del arnés (`F:\Proyectos Antigravity\cerebro-vivo`) o a cualquier proyecto que ya tenga el kit.
2. Hacer doble clic en **`instalar_kit.bat`** (que abre `instalar_gui.py`).
3. Rellenar los campos en la ventana:
   - **Carpeta del proyecto:** `F:\Modelo`
   - **Nombre del proyecto:** `Modelo`
   - **Tu nombre (dueño):** `darwin`
   - **Idioma de las respuestas:** `español`
   - **Comando de pruebas:** `python -m unittest discover tests`
   - **IA que se usarán:** marcar `Claude`, `Antigravity / Gemini` y `GPT Codex`
   - **Nivel:** elegir **`Completo`** (instala memoria + guardianes + skills + pruebas del método)
4. Pulsar **Instalar** y confirmar el resumen.

### Opción B: Por terminal (equivalente exacto en 1 comando)
```powershell
python "F:\Proyectos Antigravity\cerebro-vivo\.brain\biblioteca\kit-arranque\instalar.py" "F:\Modelo" --nombre Modelo --dueno darwin --idioma español --pruebas "python -m unittest discover tests" --ias claude,gemini,codex --nivel completo
```

### Comprobación automática tras instalar el kit
```powershell
python "F:\Modelo\.brain\biblioteca\kit-arranque\instalar.py" "F:\Modelo" --comprobar
```
*(Verifica que los 14 guardianes compilan, que `arranque.py --manual`, `cierre.py`, `secretos.py` y `pruebas.py` responden sin fallos y que `tests.test_cerebro_indices` está en verde).*

---

## Paso 2 — Instalar el Plugin Global de «Cerebro Vivo» en Antigravity

Para que **Antigravity** tenga siempre disponibles las **15 skills** (incluyendo `/plantilla` y `/prompt-inicial`) y las reglas base (`rules/AGENTS.md`) en cualquier proyecto sin tener que copiarlas cada vez:

1. Ubicar la carpeta de plugins globales de Antigravity en Windows:
   ```text
   C:\Users\darwi\.gemini\config\plugins\cerebro-vivo\
   ```
2. Asegurarse de que contenga la estructura del plugin (repositorio `https://github.com/forxa-ken/cerebro-vivo`):
   - `plugin.json` (manifiesto del plugin versión `1.0.0`)
   - `rules/AGENTS.md` (reglas base siempre activas en Antigravity)
   - `skills/<nombre-skill>/SKILL.md` (las 15 carpetas de skills)
3. Verificar en el gestor de plugins de Antigravity que **`Cerebro Vivo`** aparezca habilitado.

---

## Paso 3 — Instalar y adaptar las 15 Skills para GPT Codex y Agentes del proyecto (`.agents/skills/`)

Dado que **GPT Codex** (y el estándar `.agents/skills/` del proyecto) descubre las skills locales dentro de `F:\Modelo\.agents\skills\` y no dentro de `.claude/skills/`, se siguió este procedimiento (documentado en [`.brain/specs/005-skills-cerebro-vivo-codex.md`](.brain/specs/005-skills-cerebro-vivo-codex.md)):

1. **Crear la carpeta destino en el proyecto:**
   ```powershell
   New-Item -ItemType Directory -Force -Path "F:\Modelo\.agents\skills"
   ```
2. **Crear una subcarpeta por cada una de las 15 skills** con su archivo `SKILL.md`:
   - `cero-dependencias`
   - `cerrar-una-tarea`
   - `explicar-a-darwin-en-llano`
   - `guardian-avisa-o-bloquea`
   - `implementada-no-es-hecha`
   - `licencia-antes-de-usar`
   - `mover-no-borrar`
   - `pendientes-solo-lo-que-falta`
   - `probar-guardian-en-windows`
   - `prompt-inicial`
   - `quitar-codigo-antiguo-con-test`
   - `secretos-fuera-del-repo`
   - `spec-antes-de-programar`
   - `traspaso-entre-chats`
   - `vigilar-librerias`
3. **Adaptar el contenido de cada `SKILL.md` en `.agents/skills/`:**
   - Encabezado YAML obligatorio (`---`) con `name:` (en minúsculas con guiones, coincidiendo con el nombre de su carpeta) y `description:` clara en una sola línea.
   - Sustituir referencias de otros proyectos o rutas de Python inexistentes (`venv\Scripts\python.exe`) por los comandos reales de `Modelo` (`python .brain/guardianes/...` y `python -m unittest discover tests`) y enlazar con `AGENTS.md` y `.brain/constitution.md`.
4. **Validar el formato de las 15 skills y correr los tests del proyecto:**
   ```powershell
   python -m unittest discover tests
   ```
5. **Cómo usarlas en un chat nuevo:**
   - Se activan automáticamente cuando la tarea coincide con su descripción, o invocándolas explícitamente con `$nombre-de-skill` (por ejemplo, `$prompt-inicial` en Codex o `/plantilla` en Antigravity).

---

## Paso 4 — Cómo actualizar el arnés y las skills en el futuro

Cuando hagas mejoras en el repositorio matriz (`F:\Proyectos Antigravity\cerebro-vivo`), puedes traerlas a `F:\Modelo` sin perder nada de lo que hayas hecho aquí:

1. **Ver qué cambiaría (modo simulación, sin tocar archivos):**
   ```powershell
   python .brain/guardianes/actualizar_arnes.py --simular
   ```
2. **Aplicar la actualización (guarda copia de seguridad automática en `.brain/copias_arnes/`):**
   ```powershell
   python .brain/guardianes/actualizar_arnes.py
   ```
