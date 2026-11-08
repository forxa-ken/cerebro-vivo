---
name: cero-dependencias
description: Use when you must generate Excel, PDF, GIF or similar files and want to avoid installing libraries.
---

# Zero dependencies

## How (steps)
1. Look first in Python's standard library (zipfile, csv, hashlib, urllib).
2. Excel .xlsx: zipfile + hand-written XML. PDF: the PDF standard fonts, written by hand. GIF: own GIF89a encoder in JS.
3. Copy the pattern of the existing file instead of inventing a new one.
4. Check the visual result by eye (the PDF's look has not been reviewed yet).

## Error it prevents (real case)
- Nothing to install and nothing that breaks when a library is updated.

## Where it lives in the repo
- `audit_export.py`, `sales_export.py`, `static/js/gif_encoder.js`

## Source
- herramientas.md (Reports without dependencies), letter §16

## Used
- Times: 0 · Last: — (created on 2026-10-31, spec 079)
