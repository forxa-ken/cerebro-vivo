# Spec 007: objetivo.md y skills para Codex en el instalador (pendientes 6 y 7)

- **Estado:** hecha y probada (1.5.0)
- **Fecha:** 2026-11-01

## 1. Objetivo
- **6:** que el objetivo del proyecto quede escrito en el cerebro y no solo en el chat de una IA (caso real: Modelo, Codex no lo sabía).
- **7:** que las skills también lleguen a `.agents/skills/` para Codex (se invocan con `$`).

## 2. En alcance
- [ ] `instalar.py` crea `.brain/architecture/objetivo.md` desde una plantilla nueva (`plantillas/objetivo.md`): objetivo, para quién, cómo sabré que está bien, qué NO.
- [ ] Los tres índices de entrada (`indice_ia.md`) enlazan `objetivo.md` como lo primero a leer.
- [ ] La constitución (plantilla) añade la regla: todo objetivo dado por el dueño se escribe en `objetivo.md` en la misma respuesta.
- [ ] El instalador y `actualizar_arnes.py` copian cada skill de `.claude/skills/` a `.agents/skills/` solo si el proyecto usa Codex (`AGENTS.md`).
- [ ] Pruebas nuevas; `VERSION` 1.5.0, `CAMBIOS.md`, manifiesto.

## 3. Fuera de alcance
- No migrar proyectos ya instalados (Modelo, LoboHook, Correo): se actualizan después con `actualizar_arnes.py --simular`.
- No tocar `F:\Modelo`, no subir a GitHub sin orden.
- Este repo (cerebro-vivo) no gana `objetivo.md` propio en esta spec.

## 4. Plan
1. Plantilla `objetivo.md` y su alta en `instalar.py`.
2. Enlace en `indice_ia.md` y regla en la plantilla de constitución.
3. Copia de skills a `.agents/skills/` (instalador y actualizador), solo con Codex.
4. Pruebas, versión, cambios, manifiesto.

## 5. Verificación
- `python -m unittest discover tests` en verde.
- **Prueba de Darwin:** instalar en un proyecto de prueba con Codex, abrir un chat nuevo de Codex y preguntarle el objetivo; escribir `$resumen`.

## 6. Cierre
- [x] Spec aprobada por Darwin antes de programar
- [ ] Línea en `.brain/decisions.log`
