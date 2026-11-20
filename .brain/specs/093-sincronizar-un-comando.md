# Spec 093: `/sincronizar`, un comando que deja el ordenador al día con GitHub

- **Estado:** **implementada en v1.62.0** (pedida por Darwin el 2026-11-20). Falta que Darwin la pruebe en el otro ordenador.
- **Fecha:** 2026-11-20
- **Origen:** Darwin, al pasar a trabajar en otro ordenador: «cuando vaya a ese ordenador pueda dar un comando y se sincronice con lo que haya en git… solo poner sincronizar y el ordenador quede listo para trabajar».

## 1. Qué hace
- Skill `/sincronizar` (Claude: `/sincronizar`; Codex: `$sincronizar`) y guardián `sincronizar.py`. También vale `python .brain/guardianes/sincronizar.py` a mano.
- Hace `git fetch` y `git pull --ff-only`: **solo avanza**. Nunca mezcla, nunca pisa, nunca sube nada.
- Después ejecuta `arranque.py --manual` (ya con lo recién bajado): estado, traspaso, versión del arnés.
- `--simular` cuenta lo que haría sin tocar nada; `--sin-arranque` omite el resumen.

## 2. Casos
- Al día: lo dice. Con cambios nuevos: los baja y cuenta cuántos.
- Rama separada de GitHub (cambios locales sin subir + cambios nuevos): no toca nada y lo explica.
- Cambios locales que chocan con lo que baja: git se niega, se cuenta y no se toca nada.
- Commits locales sin subir y archivos sin commitear: se avisa (no se suben sin orden de Darwin).
- Sin internet, sin remoto o fuera de un repositorio: mensaje claro, código de salida 1.

## 3. Fuera de alcance
- No sube (`push`), no hace `merge`/`rebase`/`stash`/`reset`, no instala nada ni actualiza el arnés de un proyecto (para eso `/actualizar`).
- No clona: la primera vez en un ordenador nuevo hace falta `git clone` (queda dicho en la skill).

## 4. Pruebas
- `tests/test_sincronizar.py`: repos temporales con un remoto local (al día, baja, simular, separada, choque, sin remoto, fuera de git); paridad es/en de los textos y de la skill.
