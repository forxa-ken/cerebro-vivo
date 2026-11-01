# Spec 005: Quitar herramientas poco útiles (uso_tokens, modo auto, plugin /plantilla)

- **Estado:** hecha (1.4.0), sin commitear
- **Fecha:** 2026-11-01

## 1. Objetivo
Darwin pidió quitar tres herramientas que no aportan lo suficiente: `uso_tokens.py` (duplicado por `medir.py`), el **modo auto** (`modo_auto.py`) y el **plugin `/plantilla`**. `cerrar.py` se queda (lo usan el cierre, la constitución y varias skills).

## 2. En alcance
- Borrar `uso_tokens.py` (lo que `medir.py` tomaba de él pasa a `medir.py`), `modo_auto.py` y su prueba, `plantilla-prompt/` y `.claude-plugin/`.
- Quitar el aviso `PreToolUse` de `.claude/settings.json` y del instalador, sus ajustes de `guardianes.json`, `plugins_requeridos` (queda vacío), `.gitignore` y la lista de pruebas del manifiesto.
- Actualizar manuales, README, CLAUDE.md, `/prompt-inicial` y las pruebas del repo.
- `VERSION` 1.4.0, `CAMBIOS.md`, manifiesto, pruebas en verde.

## 3. Fuera de alcance
- No tocar proyectos que ya usan el arnés (el actualizador no borra nada) ni subir a GitHub.
- Los archivos siguen en el historial de git por si hace falta recuperarlos.

## 4. Verificación
`python -m unittest discover tests` en verde (181 pruebas: las 17 del modo auto ya no existen).

## 5. Cierre
- [x] Pedido por Darwin en el chat ("Solo los tres")
- [x] Línea en `.brain/decisions.log`
