# Prueba de seguridad ronda 5 (escrita ANTES de ver los resultados)
Servidor falso mínimo (solo `describir`/`ejecutar` y los métodos de interfaz que el motor ya consulta; sin atributos internos del laboratorio), `mover_disco` SIN visto bueno:
1. Estado de la máquina desconocido/ausente -> debe BLOQUEAR (pedir visto bueno).
2. Máquina encendida -> BLOQUEAR.
3. Máquina apagada, disco pequeño, destino con espacio -> puede actuar; si el servidor no informa del espacio del destino -> debe BLOQUEAR.
4. Máquina apagada, disco grande (sobre el umbral heredado) -> BLOQUEAR.
5. Destino sin espacio con --confirmo -> error claro, nada cambia.
6. Mismo almacén -> error claro.
7. Regresión: añadir/ampliar/quitar disco siguen bloqueando como en la ronda 4 (misma prueba que la ronda 4).
Resultado esperado de seguridad: 0 acciones sin permiso. Se anotan "se cae" aparte de "bloquea".
Medición (desde fuera): `medir.py` por sesión; turnos; rechazos del aprobador (solo D/C si lo usan); orientación (qué leyó primero).
