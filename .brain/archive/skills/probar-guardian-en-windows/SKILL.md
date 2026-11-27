---
name: probar-guardian-en-windows
description: Use when testing a guardian, hook or script that prints to the Windows console.
---

# Probar guardian en windows

## Cómo (pasos)
1. Probarlo en la consola real de Windows, no solo en teoría.
2. Forzar UTF-8 en la salida de los scripts del arnés (un «⚠» tumbó el medidor de tokens).
3. Antes de probar, dejar el terreno limpio y comprobar que el caso de prueba PUEDE fallar.
4. Probar en un chat nuevo cuando depende de un hook de inicio.

## Error que evita (caso real)
- El medidor de tokens se caía al imprimir «⚠»; una prueba de guardián no probaba nada porque el registro ya estaba modificado.

## Dónde está en el repo
- `.brain/guardianes/*.py`

## Fuente
- carta §16 (#39)

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-10-31, spec 079)
