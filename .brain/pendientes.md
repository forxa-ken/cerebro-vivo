# Pendientes

Lista viva de **lo que falta**. Una línea por punto. **Numeración fija** (los huecos son puntos ya terminados: están en `archive/hechos-indice.md`).

**Regla de cierre:** cuando Darwin prueba una tarea y confirma, en esa misma respuesta se pasa su detalle a `archive/hechos.md`, se añade su fila a `archive/hechos-indice.md` y se quita de aquí. Si la prueba falla, vuelve a «Falta programar» con una nota de qué falló.

## Falta programar (IA)



- **37:** experimento VMware CERRADO (rondas 1-5, informes en `.brain/archive/informe-*vmware*`). Conclusión: las reglas de seguridad son lo que decide (skill `seguridad-en-sistemas-reales`, arnés 1.30.0); ODD + reglas para tareas puntuales, Cerebro Vivo + reglas para proyectos largos. Falta: (a) HECHO el 2026-11-14 (Go, vcsim y pyvmomi instalados; 25 de 25 pruebas contra vcsim, con un hallazgo: vcsim dice «hecho» al mover disco sin moverlo; informe en `.brain/archive/informe-vcsim-pendiente-37-2026-11-14.md`); (b) HECHO el 2026-11-12 (arnés 1.40.2: `test_soporte_mac` se salta fuera del repo del arnés, donde Git de Windows convierte el fin de línea); (c) la regla «vcsim» de `AGENTS.md` ya no se contradice pero quedó desfasada: falta una frase que admita vcsim como segundo servidor (decide Darwin). Si Darwin lo da por bueno, el 37 se cierra.

- **51:** (spec 046, fases 2 a 5; aparcado por Darwin, 2026-11-13: «un poco básicos pero sirven») más tipos de diagrama en `/diapositivas`: clases y estados, tarta/barras/líneas, ER, Gantt. Se aprueban de una en una cuando Darwin lo pida. Textos es/en.
- **52:** (spec 047, borrador; aparcado por Darwin, 2026-11-13) vídeo de las diapositivas: grabar un lienzo a `.webm` (técnica del Estudio de video de LoboHook, sin copiar código) con voz Kokoro. Esperando la aprobación de la spec antes de programar nada.
- **54:** (spec 050, borrador; espera aprobación de Darwin) (idea de Darwin, 2026-11-14) modo automático de la fábrica (junto al modo normal): la IA es una línea de producción; Darwin entrega órdenes, la línea trabaja sola, **prueba el producto de verdad** (programado no es terminado), pasa guardianes y pruebas, y Darwin ve el resultado y, si es el esperado, se sube. Por definir en una spec: cómo la IA prueba el producto (criterio de «esperado» escrito antes de cada orden), qué decisiones toma sola, qué sigue pidiendo sí (subir, borrar, gastar, seguridad), límite de intentos/coste y registro de cada decisión. Primero como experimento acotado en rama aparte.
- **55:** (idea de Darwin, 2026-11-14) ¿el método dedica demasiado tiempo a cuidarse a sí mismo? **Medido el 2026-11-14 con `medir.py --ritual`:** en cerebro-vivo el mantenimiento del arnés es el 13,5 % del coste, pero aquí el método ES el producto (es desarrollo, no desperdicio); en LoboHook es el 0,9 % (81 chats) y los rituales del arnés en total, 18,9 %. Conclusión: sin problema real. Queda, si Darwin quiere: medir cuánto **ahorra** la memoria (16 a 20 % de coste), podar con `medir.py --skills` y, opcional, un `mantener.py` para lo mecánico. Tope de mantenimiento por chat: descartado por ahora.
- **56:** (idea a estudiar, Darwin 2026-11-14; no se hace ahora, primero terminar lo abierto) marco o «framework» de piezas reutilizables para la fábrica de ensamblaje en línea: cada pieza declara qué recibe, qué entrega, su criterio de «esperado», su evidencia y su dueño. Cautela: no diseñarlo antes de tener 2 o 3 usos reales; lo razonable es extraerlo de lo que se repita en las fases 2 a 6 de la spec 050 (revisor de spec, prueba de uso real, informe, frenos).

## Esperando tu prueba (Darwin)


## Acciones tuyas
