---
name: hermanos
description: Use when the project has sibling projects (same origin, different variant), the arranque says "N commits de X sin portar", or Darwin asks to set up or adopt a "portar" file.
---

# Proyectos hermanos — qué falta portar, calculado solo

Un proyecto «hermano» comparte origen con este (otra variante o edición). Lo que se hace en uno y falta en el otro se calcula con git en vez de depender de la memoria (spec 043). **Solo lectura**: el guardián no hace `fetch` ni cambia nada; si el hermano no está accesible, calla.

## Cómo (pasos)
1. **Configurar un hermano** (lo pide Darwin; él da la ruta): en `.brain/guardianes/guardianes.json`, `proyectos_hermanos`: `[{"nombre": "...", "ruta": "C:/ruta/al/hermano", "rama": "main", "archivo_portar": ".brain/portar-NOMBRE.md"}]`. Se admiten varios.
2. **Crear el archivo de portar** desde `.brain/biblioteca/PLANTILLA_PORTAR.md` (secciones `## Último portado`, `## Pendiente`, `## Hecho`). Poner en «Último portado» un commit del hermano que ya esté al día.
3. **Adoptar un archivo de portar que ya existía con otro formato:** conservarlo, añadir los tres encabezados y pasar a «Hecho» cada commit ya portado o descartado con su hash (7 caracteres o más). No inventar hashes: sacarlos de `git log` del hermano.
4. **Leer el aviso:** el arranque dice «N commits de X sin portar». Ver la lista con `python .brain/guardianes/hermanos.py`. Portar (o decidir «no aplica») y anotar el hash en «Hecho» con qué cambia, qué adaptar y qué no portar. El guardián no hace `cherry-pick`: lo decide una persona o la IA del proyecto.
5. **Hallazgos compartidos:** antes de investigar, mirar `.brain/hallazgos-compartidos.md` del hermano; tras investigar algo útil para varios, anotarlo en el propio (plantilla `PLANTILLA_HALLAZGOS.md`).

## Error que evita (caso real)
- Dos variantes de un mismo proyecto: el archivo de «portar» llevaba semanas diciendo «Pendiente: (nada)» mientras el otro seguía avanzando, y lo descubierto se investigaba dos veces.

## Dónde está en el repo
- `.claude/skills/hermanos`, `.brain/guardianes/hermanos.py`, `arranque.py`, `guardianes.json` (`proyectos_hermanos`), `biblioteca/PLANTILLA_PORTAR.md`, `PLANTILLA_HALLAZGOS.md`, spec 043.

## Fuente
- Spec 043 (petición de Darwin, 2026-11-12)

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-11-12)
