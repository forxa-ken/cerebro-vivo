---
name: subir-a-github
description: Use when Darwin orders to push or upload the project to GitHub, or says "sube".
---

# Subir a GitHub

Solo con la orden de Darwin, salvo el commit de memoria de `traspaso-out salgo`, que lleva su propia excepción.

## Cómo (pasos)
1. Revisar secretos: `python .brain/guardianes/secretos.py`. Si encuentra algo, parar y decírselo a Darwin.
2. Meter en un commit, sin preguntar, los traspasos (`.brain/archive/traspasos/` y `.brain/traspaso.md`) y `.brain/decisions.log`, para que el contexto llegue a otro ordenador.
3. Mirar lo demás que siga sin commitear (`git status --short`), preguntar a Darwin qué hacer con ello y lanzar las pruebas, que deben estar en verde.
4. Enseñar los commits que van a subir (`git log --oneline @{u}..HEAD`) y subir con `git push`. Nunca forzar. Si GitHub rechaza, decirlo y preguntar antes de mezclar.
5. Línea en `.brain/decisions.log` con lo subido, con su commit local.

## Error que evita (caso real)
- Abrir el proyecto en otro ordenador sin los últimos traspasos: quedaban sin commitear y se perdía parte del contexto.

## Dónde está en el repo
- `.claude/skills/subir-a-github`, `guardianes/secretos.py`, `guardianes/guardar_traspaso.py`, spec 022.

## Fuente
- Spec 022

## Usada
- Veces: 0 · Última: — (creada el 2026-11-07, spec 022)
