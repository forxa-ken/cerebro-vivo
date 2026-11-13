# Cómo funciona el aviso en cadena

- **Fuente:** chat cerebro-vivo #19, pendiente 47
- **Fecha:** 2026-11-13

El aviso en cadena (arnés 1.48.0) salta al cerrar una tarea, solo si el chat editó algo que casa con `si` y nada que casa con `salvo`. Las reglas viven en `cadenas` de `guardianes.json`, con el texto en es/en; se apaga con `cadenas_activas: false`. Solo avisa: no bloquea, y si se repite sin atenderse se apaga en ese chat.
