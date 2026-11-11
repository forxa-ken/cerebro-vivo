# Spec 040: comando `/fabrica si|no|estado` (modo fábrica persistente)

- **Estado:** aprobada por Darwin el 2026-11-11 y programada en 1.37.0 (sin subir).
- **Origen:** Darwin no quiere que el modo fábrica dependa de acordarse en cada chat: «el sentido de la fábrica es el trabajo autónomo de la IA; si hay que intervenir en todos los chats, no se hace nada». Quiere poder usar el proyecto de las dos maneras (fábrica o normal), con un comando, y que el modo **se quede** entre chats.

## 1. En alcance
- [ ] Ajuste `modo_fabrica` (true/false, por defecto false) en `.brain/guardianes/guardianes.json` del proyecto. Vive en el proyecto, no en la máquina: todos los chats de ese proyecto lo respetan, también en otro ordenador.
- [ ] `python .brain/guardianes/fabrica.py modo si|no|estado` (sin palabra = `estado`), con textos es/en en `textos.py`.
  - `si`: activa el ajuste y, si falta, prepara `.brain/fabrica/` con las plantillas (sin tocar lo que ya exista). La carta la sigue escribiendo Darwin.
  - `no`: apaga el ajuste. No borra `.brain/fabrica/` ni la evidencia.
  - `estado`: dice en qué modo está y, si es fábrica, qué puerta falta (carta sellada, spec aprobada).
- [ ] Skill `/fabrica` (es + `.en.md`), igual que `/chat-nuevo`: lee la palabra, ejecuta el script y dice el resultado en una línea.
- [ ] **El arranque lo avisa solo cuando está activado:** una línea al principio del resumen: «Modo fábrica ACTIVADO: eres la directora (skill `directora-de-fabrica`): no programas, escribes spec y encargos». Con el modo apagado el arranque queda exactamente como hoy.
- [ ] Una carpeta `.brain/fabrica/` sin el ajuste (proyectos de antes) sigue como hoy: la skill se puede cargar a mano. No se activa nada sin que Darwin lo pida.
- [ ] Pruebas: el ajuste se activa y apaga; persiste al recargar; `si` no pisa lo existente; el arranque muestra la línea solo con el modo activo; paridad es/en.

## 2. Fuera de alcance
- Activar la fábrica por detección automática o sin orden de Darwin.
- Cambiar el funcionamiento de la fábrica (puertas, topes, encargos): solo el interruptor.
- Más modos (p. ej. «revisora»): no por ahora.

## 3. Riesgo
- Una IA que lea «modo fábrica» y deje de ayudar en tareas pequeñas. Mitigación: `/fabrica no` lo apaga al instante y la línea de arranque dice cómo apagarlo.
- Dos ajustes parecidos (`chat_nuevo_auto`, `modo_fabrica`): se mantiene el mismo patrón para no confundir.

## 4. Archivos
`fabrica.py`, `arranque.py`, `textos.py`, `guardianes.json`, `.claude/skills/fabrica/SKILL.md` y `.en.md`, `tests/`, manual (`CEREBRO_VIVO.md` y `.en.md`), `VERSION` (1.37.0), `CAMBIOS.md`, `manifiesto.json`.

## 5. Verificación
`python -m unittest discover tests` en verde (local y Actions); probar en un proyecto con fábrica real (TraductorVoz u otro): `/fabrica si`, abrir chat nuevo y ver que arranca como directora sin decírselo. No probado hasta hacerlo.
