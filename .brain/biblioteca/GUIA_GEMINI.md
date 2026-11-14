# Receta corta: instalar Cerebro Vivo en un proyecto con Gemini (Antigravity)

Para quien va a trabajar con **Antigravity/Gemini**. La guía general (todas las IAs) es `GUIA_INSTALACION.md`; aquí solo lo que cambia con Gemini. Probado el instalador con `--ias gemini` en una carpeta de prueba; **no probado dentro de Antigravity real**.

## 1. Instalar
Desde el repo del arnés (cambia las rutas y el nombre):
```powershell
python "RUTA_REPO_ARNES\.brain\biblioteca\kit-arranque\instalar.py" "RUTA_PROYECTO" --nombre NOMBRE --dueno DUENO --idioma español --pruebas "python -m unittest discover tests" --ias gemini --nivel completo
```
O con ventana: doble clic en `instalar_kit.bat` y marca solo Gemini en «IA que se usarán».

Crea `GEMINI.md` (el índice que lee Gemini), `.brain/` (memoria, constitución, pendientes), los guardianes y las pruebas. También deja `.claude/` con los ganchos de Claude Code: no estorba, Gemini no lo usa.

**Skills para Gemini:** las de proyecto de Antigravity viven en `.agents/skills/` y el instalador solo las copia **si el proyecto tiene `AGENTS.md`**. Con `--ias gemini` solo no se crean. Si quieres las skills, instala con `--ias gemini,codex` (se invocan con `$nombre`, no con `/`).

## 2. Comprobar
```powershell
python "RUTA_PROYECTO\.brain\biblioteca\kit-arranque\instalar.py" "RUTA_PROYECTO" --comprobar
```
Todo debe salir con ✅. El aviso de «Hooks de Claude Code» es normal y no afecta a Gemini.

## 3. Cómo se usa (lo que cambia respecto a Claude)
- **Gemini no corre ganchos:** no hay resumen al abrir ni aviso al cerrar. Al abrir un chat, pídele: «lee `GEMINI.md`, `.brain/traspaso.md` y `.brain/pendientes.md` y cuéntame el estado». O ejecuta tú `python .brain/guardianes/arranque.py --manual`.
- **Al terminar una tarea:** que escriba la línea del registro con `python .brain/guardianes/cerrar.py --chat "nombre #N" "qué se hizo"`.
- **Cambiar de chat o de IA:** escribe `salgo` en el chat que dejas y `entro` en el nuevo; solo una IA a la vez trabaja en el proyecto.
- **No funcionan en Gemini:** `/prompt-inicial` ni los avisos automáticos.
- **Plugin global antiguo** (`%USERPROFILE%\.gemini\config\plugins\cerebro-vivo`): está desfasado, no lo uses.

## 4. Actualizar más adelante
```powershell
python .brain/guardianes/actualizar_arnes.py --simular
python .brain/guardianes/actualizar_arnes.py
```
No pisa lo que modificaste a mano.
