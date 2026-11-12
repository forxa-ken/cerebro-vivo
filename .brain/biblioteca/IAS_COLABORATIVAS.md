# Colaboración entre IA (plantilla; spec 042)

Este archivo vive en `.brain/colaboracion.md` solo en los proyectos que activan `/colabora si`. Con una sola IA no se usa. **Cada regla está escrita una sola vez, aquí**: los índices (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`) solo traen una línea que remite a este archivo.

## 1. Papeles (rellena la tabla; no inventes: pregunta al dueño)

| IA | Archivo de entrada | Hace | Archivos que puede escribir | Archivos que nunca toca |
| :--- | :--- | :--- | :--- | :--- |
| Claude | `CLAUDE.md` | (p. ej. dueña de `.brain/` y del código) | (a completar) | (a completar) |
| Codex | `AGENTS.md` | (p. ej. solo lo que diga su encargo) | los del encargo, en su worktree | `.brain/`, salvo su nota |
| Gemini | `GEMINI.md` | (p. ej. textos, traducciones, documentación) | los del encargo, en su worktree | `.brain/`, salvo su nota; seguridad y dinero |

Quita las filas de las IA que no participen.

## 2. No pisarse
- Dos IA que escriben **nunca comparten carpeta de trabajo**: cada una en su worktree y su rama.
- Lo que edita una, la otra lo ve solo tras el commit.
- Nadie escribe en `.brain/decisions.log` salvo quien cierra el bloque (el dueño de `.brain/`).
- Si dudas de qué archivo es tuyo, para y pregunta al dueño; no rellenes con una suposición.

## 3. Notas entre IA
Al terminar o pararte, deja una nota en `.brain/notas-chats/` (plantilla `PLANTILLA_NOTA_CHAT.md`): qué hiciste, qué tocaste, qué no pudiste probar. El arranque la muestra a la siguiente IA.

## 4. Lo que se descubre se comparte
Antes de investigar algo, mira `.brain/hallazgos-compartidos.md` (si existe) y el de los proyectos hermanos. Tras investigar algo útil para varios, anótalo ahí.
