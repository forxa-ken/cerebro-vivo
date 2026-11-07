# Spec 023: /version y qué hacer si /actualizar no existe

- **Estado:** implementada (falta la prueba de Darwin)
- **Fecha:** 2026-11-07
- **Versión prevista:** arnés 1.21.0

## 1. Objetivo
En Modelo 2, con el arnés 1.12.0, `/actualizar` no existía (llegó en la 1.17.0) y no había forma rápida de saber la versión del proyecto. Darwin pidió un comando `/version` y que la página explique cómo actualizar en ese caso.

## 2. En alcance
- [x] Skill `/version`, solo de lectura: versión instalada, versión disponible, novedades y cómo actualizar (incluido el caso de un proyecto anterior a la 1.17.0).
- [x] Fila en `.brain/experiencia/indice.md` y mención en `MANUAL_DE_USO.md` y `CEREBRO_VIVO.md`.
- [x] Página pública: el caso «si `/actualizar` no existe» y el comando `/version`.

## 3. Fuera de alcance
- Un guardián o un script nuevo: la skill lee dos archivos pequeños.
- Que `/version` llegue a un proyecto antiguo sin actualizarlo una vez a mano: es imposible, igual que con `/actualizar`.

## 4. Verificación
- `python -m unittest discover tests` en verde.
- Darwin: en un proyecto actualizado, escribir `/version` y comprobar que dice la versión y si hay otra más nueva.
