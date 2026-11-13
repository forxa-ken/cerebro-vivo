---
name: diapositivas
description: Use when Darwin types /diapositivas (with or without a topic or a document name) or asks to explain something as slides or a presentation.
---

# /diapositivas — presentaciones para humanos, con una sola orden

Convierte un tema o un documento en diapositivas que se abren en el navegador, sin instalar nada (spec 045). Darwin no escribe Markdown ni comandos.

## Cómo (pasos)
1. Leer lo que va detrás del comando:
   - **Sin nada:** tema `resumen` (estado del proyecto).
   - **`resumen`, `version`, `traspaso`, `auditoria`:** `version` = última entrada de `CAMBIOS.md`; `traspaso` = `.brain/traspaso.md` (o el último archivado); `auditoria` = el último informe del auditor.
   - **`doc NOMBRE`** (o un nombre que parece un archivo): modo documento, ver el paso 4.
   - **Texto libre:** el tema que pida Darwin.
2. Leer **solo** los archivos del tema; nada que no salga de ellos. Escribir `.brain/diapositivas/AAAA-MM-DD-tema.md` con la plantilla `biblioteca/PLANTILLA_DIAPOSITIVAS.md` (o `.en.md` si el proyecto está en inglés). Una línea `---` separa cada diapositiva. Reglas: **máximo 12 diapositivas y 6 viñetas por diapositiva**, frases cortas y en llano (subviñetas con 2 espacios de sangría, hasta 3 niveles) (la skill de explicar en llano), lo no probado como «sin probar», y en la última diapositiva los archivos de los que sale todo.
3. Ejecutar `python .brain/guardianes/diapositivas.py .brain/diapositivas/AAAA-MM-DD-tema.md`. Se abre solo en el navegador. Decir a Darwin en una línea dónde quedó y cómo moverse (flechas, `o` para ver todas, Ctrl+P para PDF). No empezar nada más.
4. **Modo documento** (`doc NOMBRE`): localizar con `python .brain/guardianes/diapositivas.py --buscar NOMBRE`. Si sale un solo archivo, seguir. Si salen varios (salida 3), **preguntar a Darwin cuál**, nunca elegir. Si no sale ninguno (salida 2), decirlo y no inventar. Después:
   - El tope de 12 diapositivas **no aplica**. La primera diapositiva es un **índice** con todas las secciones (`##`) del documento.
   - **Cada sección del original tiene al menos una diapositiva**, con el texto de su título copiado tal cual como `## título`.
   - Pasadas 20 diapositivas el script lo parte solo en partes enlazadas.
   - La última diapositiva dice qué documento se presentó y qué secciones se condensaron mucho, con su ruta.
   - Antes de dar nada por hecho, comprobar: `python .brain/guardianes/diapositivas.py --comprobar ORIGINAL.md DIAPOSITIVAS.md`. Si falta alguna sección, añadirla y repetir.
5. **Diagramas (spec 046, fase 1):** si una diapositiva se entiende mejor con un dibujo, escribir un bloque ```` ```mermaid ```` con `flowchart LR` (o `TD`: cajas y flechas, p. ej. el ciclo de una tarea) o `sequenceDiagram` (quién habla con quién, en orden). Máximo 15 cajas, o 7 participantes y 24 mensajes. El dibujo **sale de los archivos leídos**, no se inventa. Si el script avisa de que un diagrama no se pudo dibujar, corregirlo o dejarlo como texto; los demás tipos (clases, estados, tarta, etc.) aún no existen.
6. Los `.html` se pueden rehacer y no se suben a Git (el script deja un `.gitignore` local). Los `.md` sí.

## Error que evita (caso real)
- Resumir un documento largo en pocas diapositivas sin avisar y dejar fuera secciones enteras sin que Darwin lo viera. El índice, la regla «una diapositiva por sección» y `--comprobar` lo hacen visible. La comprobación mira que cada sección aparezca, no que el resumen sea fiel: eso lo revisa Darwin.

## Dónde está en el repo
- `.brain/guardianes/diapositivas.py`, `.brain/biblioteca/PLANTILLA_DIAPOSITIVAS.md`, `tests/test_diapositivas.py`, spec 045.

## Fuente
- Spec 045 (idea del gist «LLM Wiki» de Karpathy, petición de Darwin, 2026-11-12)

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-11-12)
