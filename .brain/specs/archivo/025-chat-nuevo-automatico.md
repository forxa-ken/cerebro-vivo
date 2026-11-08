# Spec 025: abrir el chat nuevo solo, como regla común, y /chat-nuevo para activarlo o no

- **Estado:** implementada
- **Fecha:** 2026-11-07

## 1. Objetivo
En Guild Control Forever #14 y #15 el aviso de chat largo llegó, pero la IA no intentó abrir el chat nuevo: dio la frase para pegar y en el #15 dijo «la herramienta me lo rechaza» sin haberla llamado. En cerebro-vivo sí lo abría, porque la regla («ábrelo tú, inténtalo siempre primero») solo estaba en la memoria personal de este proyecto. Darwin pidió que sea regla común para todo proyecto con Cerebro Vivo y un comando para activarla o desactivarla.

## 2. En alcance (In-Scope)
- [x] Ajuste `chat_nuevo_auto` en `guardianes.json` (por defecto `true`; el actualizador lo añade a los proyectos).
- [x] Aviso de `longitud.py` firme: con el ajuste activo, llamar SIEMPRE a `start_session` primero; prohibido decir que la app lo rechaza sin haberla llamado; la frase para pegar solo si la llamada da error. Con el ajuste apagado: recomendar el chat nuevo y dejar la frase, sin abrirlo.
- [x] `longitud.py --chat-nuevo si|no|estado` cambia o muestra el ajuste; skill `/chat-nuevo` que lo usa.
- [x] Skill `traspaso-in`: nunca decir «rechazado» sin haber llamado a la herramienta.
- [x] Textos en es y en (spec 024).

## 3. Fuera de alcance (Out-of-Scope)
- Cambiar la memoria o el `CLAUDE.md` de cada proyecto (llega con el aviso y la skill al actualizar).
- Fase 3 de la spec 024.

## 4. Verificación
- Tests: `python -m unittest discover tests` (todo en verde); `tests/test_longitud.py` cubre los dos textos y el comando.
- Darwin: en Guild Control Forever, tras `/actualizar`, al pasar de 200k el chat nuevo debe abrirse solo; `/chat-nuevo no` lo deja en solo aviso.
