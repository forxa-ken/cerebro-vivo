---
name: chat-nuevo
description: Use when Darwin types /chat-nuevo (si, no or estado) or asks to turn on or off that the AI opens the new chat by itself when the chat gets long.
---

# /chat-nuevo — abrir solo el chat nuevo, sí o no

Activa, desactiva o muestra el ajuste `chat_nuevo_auto` de `.brain/guardianes/guardianes.json`. Por defecto está activado: al pasar el aviso de chat largo, la IA escribe el traspaso y abre ella misma el chat nuevo.

## Cómo (pasos)
1. Leer la palabra detrás del comando: `si` (activar), `no` (desactivar) o `estado` (solo mirar). Sin palabra, `estado`.
2. Ejecutar `python .brain/guardianes/longitud.py --chat-nuevo PALABRA`.
3. Decir a Darwin en una línea cómo queda, con el texto que imprime el script. No tocar nada más.

## Error que evita (caso real)
- En Guild Control Forever #14 y #15 llegó el aviso de chat largo y la IA no abrió el chat nuevo: dio la frase para pegar y en el #15 dijo que la app se lo rechazaba sin haberlo intentado. La regla solo estaba en la memoria de cerebro-vivo.

## Dónde está en el repo
- `.claude/skills/chat-nuevo`, `.brain/guardianes/longitud.py` (`chat_nuevo`), `guardianes.json` (`chat_nuevo_auto`), spec 025.

## Fuente
- Spec 025 (petición de Darwin, 2026-11-07)

## Usada
- Veces: 0 · Última: — (creada el 2026-11-07)
