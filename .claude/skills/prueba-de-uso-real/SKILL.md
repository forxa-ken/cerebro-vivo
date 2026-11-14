---
name: prueba-de-uso-real
description: Use when a factory in automatic mode (spec 050) has an assignment built and it must be tested in real use, with saved evidence, before it can be called delivered; or when you must test a product that another AI built.
---

# Prueba de uso real

Programado no es terminado. Esta skill dice **cómo probar de verdad** lo que otra IA construyó y qué evidencia dejar. La haces **tú, que no lo construiste** (otro modelo, o al menos otro chat con estas instrucciones). Si lo construiste tú, para: avisa a la directora para que lo pruebe otra IA.

## Qué recibes
- El **criterio de «esperado»** (`.brain/fabrica/esperado.md`), escrito **antes** de construir. Es tu vara de medir: pruebas lo pedido, no algo más fácil.
- El encargo y el producto (la rama de trabajo). No la conversación de quien lo construyó.

## Cómo (pasos)
Primero, según el producto:
- **Herramientas de línea de comandos y guardianes:** ejecútalas de verdad con casos **buenos** y casos **malos**; compara la salida con el criterio y comprueba que lo malo se **rechaza** (código de salida y mensaje).
- **Documentos, skills y páginas generadas:** genéralos y ábrelos (la página, en el navegador integrado); comprueba que cargan, que no hay peticiones externas ni errores de consola y que el recorrido pedido funciona.
- **Aplicaciones con pantalla:** abre la aplicación y haz el recorrido de un usuario con el control del navegador o del ordenador, si existe.
- **Lo que una IA no puede juzgar** («se ve bien», «se entiende»): márcalo **no probado**. Pasa a «Esperando tu prueba (Darwin)». Nunca lo declares hecho.

## Dónde queda la evidencia
1. Guarda comandos, salidas y capturas en `.brain/fabrica/evidencia/` (por ejemplo `REQ-1/salida-buenos.txt`).
2. Escribe `.brain/fabrica/evidencia/REQ-1.md` con la plantilla de `PLANTILLAS_FABRICA` (sección 10): quién construyó, quién probó, el criterio probado **citado entre «…» tal como está en `esperado.md`**, casos buenos y malos ejecutados, archivos de evidencia, resultado (verde / rojo / no probado) y la lista **No probado**, que nunca se deja vacía sin explicarlo.
3. Comprueba: `python .brain/guardianes/fabrica.py entregar REQ-1`. Sale 0 solo si la evidencia está completa: otra IA probó, el criterio citado existe, los archivos existen y no están vacíos, y el resultado es verde. Con rojo, o con no probado, sale 1.

## Contra la prueba trampa
- Una prueba **sin evidencia guardada cuenta como no hecha.**
- Si no puedes citar el criterio, estás probando otra cosa: para y pregunta.
- Un resultado verde con la lista «No probado» vacía sin explicación es sospechoso: justifica por qué no queda nada.

## Error que evita
- La IA se aprueba a sí misma, o da por bueno algo porque pasó las pruebas del código aunque nadie lo usó de verdad.

## Dónde está en el repo
- `.claude/skills/prueba-de-uso-real`, `.brain/guardianes/fabrica.py` (`entregar`), `PLANTILLAS_FABRICA` (sección 10), spec 050 (fase 4).

## Fuente
- Spec 050 (petición de Darwin, 2026-11-14)

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-11-14)
