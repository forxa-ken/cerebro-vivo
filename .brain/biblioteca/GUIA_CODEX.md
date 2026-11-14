# Receta corta: instalar Cerebro Vivo en un proyecto con GPT Codex

Para quien va a trabajar con **GPT Codex**. La guía general (todas las IAs) es `GUIA_INSTALACION.md`; aquí solo lo que cambia con Codex. Probado el instalador con `--ias codex` en una carpeta de prueba; **no probado dentro de Codex real**.

## 1. Instalar
Desde el repo del arnés (cambia las rutas y el nombre):
```powershell
python "RUTA_REPO_ARNES\.brain\biblioteca\kit-arranque\instalar.py" "RUTA_PROYECTO" --nombre NOMBRE --dueno DUENO --idioma español --pruebas "python -m unittest discover tests" --ias codex --nivel completo
```
O con ventana: doble clic en `instalar_kit.bat` y marca solo Codex en «IA que se usarán».

Crea `AGENTS.md` (el índice que lee Codex), `.brain/` (memoria, constitución, pendientes), los guardianes, las pruebas y las **skills en `.agents/skills/`** (como hay `AGENTS.md`, se copian solas). También deja `.claude/` con los ganchos de Claude Code: no estorba, Codex no lo usa.

## 2. Comprobar
```powershell
python "RUTA_PROYECTO\.brain\biblioteca\kit-arranque\instalar.py" "RUTA_PROYECTO" --comprobar
```
Todo debe salir con ✅. El aviso de «Hooks de Claude Code» es normal y no afecta a Codex.

## 3. Cómo se usa (lo que cambia respecto a Claude)
- **Las skills se invocan con `$`, no con `/`:** `$resumen`, `$pendiente`, `$traspaso-in`, `$traspaso-out`, `$adopta`, `$acorta`, `$trocea`, `$subir-a-github`, `$version`.
- **Codex no corre ganchos:** no hay resumen al abrir ni aviso al cerrar. Al abrir un chat, pídele: «lee `AGENTS.md`, `.brain/traspaso.md` y `.brain/pendientes.md` y cuéntame el estado». O ejecuta tú `python .brain/guardianes/arranque.py --manual`.
- **Al terminar una tarea:** que escriba la línea del registro con `python .brain/guardianes/cerrar.py --chat "nombre #N" "qué se hizo"`.
- **Cambiar de chat o de IA:** `$traspaso-out salgo` en el chat que dejas y `$traspaso-out entro` (o `$traspaso-in entro`) en el nuevo; solo una IA a la vez trabaja en el proyecto.
- **No funciona en Codex:** `/prompt-inicial` ni los avisos automáticos.
- **Codex como auditor desde Claude:** si Claude está instalado, `python .brain/guardianes/auditor.py codex` imprime el comando `codex exec` en solo lectura (en Windows lleva el ajuste del sandbox; sin él Codex no puede ejecutar `python`).

## 4. Actualizar más adelante
```powershell
python .brain/guardianes/actualizar_arnes.py --simular
python .brain/guardianes/actualizar_arnes.py
```
No pisa lo que modificaste a mano y, como hay `AGENTS.md`, actualiza también `.agents/skills/`.
