# Spec 094: lo que es de cada ordenador no viaja con git

- **Estado:** **implementada en v1.62.0** (pedida por Darwin el 2026-11-20). Falta probarla en dos ordenadores reales.
- **Fecha:** 2026-11-20
- **Se apoya en:** spec 093 (`/sincronizar`), spec 019 (`arnes_repo`).
- **Origen:** Darwin trabaja en dos ordenadores con rutas distintas (`F:` y `C:`). Prominimap y YuGiWoW vivían dentro de la carpeta `AddOns` del juego, con `arnes_repo` escrito en `guardianes.json` (una ruta de `F:`) y `arranque_estado.json` subido a git.

## 1. Problema
- `arnes_repo` (ruta del repo del arnés en ESTE ordenador) estaba en `guardianes.json`, que va a GitHub: en el otro ordenador apuntaba a una carpeta que no existe, y cambiarlo allí creaba un choque al sincronizar.
- `arranque_estado.json` y `cierre_estado.json` son estados de cada ordenador, pero en proyectos viejos estaban subidos a git y cambiaban en cada chat.

## 2. Qué cambia
1. `arnes_repo` va en `.brain/guardianes/guardianes.local.json` (en `.gitignore`). Se lee primero ahí; si falta, de `guardianes.json` (proyectos anteriores).
2. `actualizar_arnes.py` mueve el `arnes_repo` antiguo de `guardianes.json` al archivo local, y el instalador ya lo escribe directamente allí.
3. `asegurar_estado_local`: añade a `.gitignore` los estados locales y, si estaban subidos, los saca del índice con `git rm --cached` (el archivo no se borra; no hace commit). Lo hace el actualizador en cada proyecto.

## 3. Fuera de alcance
- No cambia nada de los datos del proyecto ni sube ni commitea por su cuenta. El `git rm --cached` queda como cambio preparado para el siguiente commit del proyecto.

## 4. Pruebas
- `tests/test_arnes_actualizar.py`: movida de `arnes_repo`, prioridad del archivo local, ignorar y sacar del índice sin borrar (y que simular no escriba), segunda pasada sin cambios; el instalador y el actualizador adaptados.
