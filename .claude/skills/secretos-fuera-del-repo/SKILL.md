---
name: secretos-fuera-del-repo
description: Use when adding a key, token, webhook URL or personal data file, or before any git push.
---

# Secretos fuera del repo

## Cómo (pasos)
1. Las claves viven en `.env` / variables del alojamiento, nunca en el código ni en Git.
2. Datos de usuario y webhooks van en `.gitignore`.
3. El hook pre-commit (`secretos.py --instalar-hook`) bloquea un secreto de formato real; no usar `--no-verify` sin motivo.
4. Si una clave se filtra: cambiarla primero, limpiar el historial después (ver `architecture/secretos.md`).

## Error que evita (caso real)
- Los commits de la spec 008 llevaban una URL de webhook real de Discord.

## Dónde está en el repo
- `.gitignore`, `.brain/guardianes/secretos.py`, `.brain/architecture/secretos.md`

## Fuente
- D-020, D-046

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-10-31, spec 079)
