---
name: cero-dependencias
description: Use when you must generate Excel, PDF, GIF or similar files and want to avoid installing libraries.
---

# Cero dependencias

## Cómo (pasos)
1. Buscar primero en la biblioteca estándar de Python (zipfile, csv, hashlib, urllib).
2. Excel .xlsx: zipfile + XML escrito a mano. PDF: fuentes estándar del PDF escritas a mano. GIF: codificador GIF89a propio en JS.
3. Copiar el patrón del archivo existente en vez de inventar uno nuevo.
4. Revisar a ojo el resultado visual (la apariencia del PDF aún no se ha revisado).

## Error que evita (caso real)
- Nada que instalar y nada que se rompe al actualizar una librería.

## Dónde está en el repo
- `audit_export.py`, `sales_export.py`, `static/js/gif_encoder.js`

## Fuente
- herramientas.md (Informes sin dependencias), carta §16

## Usada
- Veces: 0 · Última: — (creada el 2026-10-31, spec 079)
