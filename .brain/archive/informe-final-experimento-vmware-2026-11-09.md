# Informe final del experimento Cerebro Vivo contra ODD (rondas 1 a 4, 2026-11-09)

Claude (cerebro-vivo #34) para Darwin. Reúne los cuatro informes de ronda (`informe-experimento-vmware-ronda1..4-2026-11-09.md`) y los lleva a conclusiones por niveles. **Todo con muestra de 1 por casilla y por ronda: son tendencias, no pruebas.** Sin GitHub, sin servidores reales, sin `vcsim`: solo laboratorio en memoria.

## 1. Qué se hizo
| Ronda | Módulo | Ramas | Qué cambió |
|---|---|---|---|
| 1 | Instantáneas (A) y Clonado (B) | A Cerebro Vivo, B ODD | Módulos distintos; contaminada por cuelgues de Codex |
| 2 | Los mismos | A, B | Cuelgues corregidos (`stdin=DEVNULL`); aprobador con tope de tiempo |
| 3 | Redes (igual en todas) | A, B, C (ODD + reglas de seguridad) | Primer módulo común; entra la variable «reglas de seguridad» |
| 4 | Discos (igual en todas) | A, B, C, D (Cerebro Vivo + reglas) | Diseño 2×2 completo: método × reglas de seguridad |

Aprobador fijo: Codex con la regla de `AGENTS.md`. Constructor: la misma IA en todas las ramas.

## 2. Nivel calidad funcional
- **Empate en las cuatro rondas:** todas las ramas cumplieron 7 de 7 criterios con prueba cada uno (11 ramas en total). Pruebas nuevas por módulo: 17 a 35. Tamaño del código del módulo: 330–490 líneas, sin diferencia sistemática.
- **Ningún método produjo un módulo roto.** El único fallo en las suites (`test_soporte_mac`, fin de línea de Windows en las ramas con el arnés completo) es ajeno al módulo y de entorno.
- **Calidad fina (mensajes, documentación):** en las pruebas de línea de comandos ejecutadas (6 a 10 casos por rama y ronda) los mensajes son claros, en español y con los mismos códigos de salida en todas. Diferencia menor y repetida: Cerebro Vivo (A) tendió a imprimir listados como JSON o diccionarios; ODD los dio como texto legible.
- **Lectura:** con la misma IA y un encargo con criterios claros, el método no cambia si el módulo funciona. Cambia cómo llega y qué deja alrededor.

## 3. Nivel seguridad (la diferencia que sí apareció)
Prueba repetida en las rondas 2, 3 y 4: un servidor falso mínimo, sin los atributos internos del laboratorio, y petición sin visto bueno.

| Ronda | Cerebro Vivo (A) | ODD (B) | ODD + reglas (C) | Cerebro Vivo + reglas (D) |
|---|---|---|---|---|
| 2 (Clonado) | sin hallazgo | **clona grande sin permiso** | no existía | no existía |
| 3 (Redes) | **actúa sin permiso** | se cae (no actúa, por accidente) | bloquea y pide permiso | no existía |
| 4 (Discos) | se cae (por accidente) | se cae (por accidente) | bloquea y pide permiso | bloquea y pide permiso |

- **Sin reglas explícitas, los dos métodos ataron su motor al laboratorio.** Dos veces se actuó sin permiso (una en cada método) y tres veces el código solo se salvó reventando con un error interno, sin mensaje claro ni registro. Ninguna de sus pruebas lo detectaba.
- **Con reglas explícitas (C, D): 0 fallos** en las tres rondas donde existieron. Cerebro Vivo con reglas (D) iguala a ODD con reglas (C).
- **Lo que decide la seguridad son las reglas, no el método.** Lo que sospechaba Darwin («ODD falla en seguridad en algún punto; mejor con parámetros») se confirma, y se amplía: Cerebro Vivo sin parámetros falla igual.
- **Sesgos a tener presentes:** las pruebas las diseñé yo después de ver el primer hallazgo (ronda 2); C y D recibieron esas reglas justo para esa prueba, así que acertarla confirma que las reglas funcionan, no que el método por sí solo lo logre.

## 4. Nivel coste (`medir.py`, mismo instrumento)
| Ronda | A (Cerebro Vivo) | B (ODD) | C (ODD + reglas) | D (CV + reglas) |
|---|---|---|---|---|
| 1 | 744k | 257k | | |
| 2 | 481k | 372k | | |
| 3 | 778k | 265k | 542k | |
| 4 | 398k | 385k | 344k | 360k |
| **Media** | **≈ 600k** | **≈ 320k** | **≈ 443k** | 360k |

- Arranque idéntico en todas (≈ 74–76k): el arnés completo no encarece la apertura del chat. El sobrecoste de Cerebro Vivo está en el trabajo posterior: spec previa, rechazos del aprobador, lecciones y cierre.
- **ODD solo es la opción más barata (≈ la mitad)**, pero la brecha se cerró de ×2,9 (ronda 1) a ×1,0 (ronda 4) conforme se arreglaron los cuelgues y la regla ambigua del aprobador («vcsim»). En la ronda 4, con un encargo ya afinado, las cuatro cuestan lo mismo (344k–398k).
- **Las reglas de seguridad cuestan poco:** C ≈ +40% sobre B de media, pero en la ronda 4 C fue la más barata.
- **Lectura:** gran parte del «coste del método» eran fricciones del montaje (cuelgues, regla ambigua, rechazos de contenido por specs que se contradecían), no del método en sí. Una estimación honesta del sobrecoste estructural de Cerebro Vivo está entre 0 y +50%.

## 5. Nivel proceso y aprobador
- **El aprobador no es determinista:** mismo texto, veredictos contrarios (C en la ronda 3 lo anotó). Acumulado: A tuvo muchos más rechazos (5, 7, 6, 1) que B (1, 1, 0, 0). Parte es técnica (cuelgues, regla «vcsim» ambigua), parte es real: la spec de Cerebro Vivo se escribe antes y más detallada, y ofrece más puntos donde rechazar; ODD propone el documento de tareas ya más corto y B llegó a APROBADA a la primera en las rondas 3 y 4 (en las rondas 1 y 2 tuvo un rechazo cada una).
- **Los rechazos de contenido real fueron útiles** (visto bueno dicho de dos maneras, falta de ensayo previo), y los rechazos por ambigüedad de regla no lo fueron: hay que mantener el reglamento del aprobador sin contradicciones.
- **Causa raíz de los peores cuelgues:** Codex esperaba entrada estándar. Fallo del montaje, no del método ni de la herramienta (corregido). La lección: medir sin haber depurado el instrumento contamina la comparación.
- **Tiempo:** no hay cifra fiable (relojes que no cuadran); se midió en turnos y tokens. Turnos medios de la IA: A 19–43, B 10–18.

## 6. Nivel mantenimiento y memoria (lo que el experimento NO pudo medir)
- Cerebro Vivo deja lecciones, registro y specs para sesiones futuras; ODD deja `odd/tasks/` y documentación. **El valor de la memoria entre sesiones no aparece en un encargo de una sola sesión.** Sí se vio un efecto real: las lecciones de A/D de la ronda 4 (p. ej. «escribir cada regla una vez») ya salen de las rondas anteriores.
- **Coste de tocar el módulo después:** todas dicen «bajo». ODD admitió un acoplamiento oculto (el motor conoce el módulo); eso es un riesgo de diseño, no de método.
- Dos rondas con módulo distinto por rama (la 1 y la 2) mezclan módulo y método; las rondas 3 y 4 ya son limpias.

## 7. Qué NO prueba este experimento (límites)
1. Muestra de 1 por casilla: la diferencia entre rondas dentro de un mismo método es tan grande como entre métodos.
2. Misma IA constructora y aprobador fijo: no sabemos cómo cambia con otra IA.
3. Solo laboratorio en memoria; sin `vcsim`, `pyvmomi` ni servidor real. Las reglas de seguridad importan precisamente cuando llegue el servidor real.
4. Una sola sesión por módulo: no mide el efecto acumulado de la memoria ni el coste de retomar.
5. Las pruebas de seguridad las diseñé yo, con la ayuda del hallazgo previo.

## 8. Conclusiones finales (por niveles)
1. **Calidad:** empate. Elegir método no cambia si el módulo funciona.
2. **Seguridad:** gana tener reglas explícitas, en cualquiera de los dos métodos. Sin ellas los dos fallan igual. Esto ya está en el arnés (1.30.0, skill `seguridad-en-sistemas-reales`).
3. **Coste:** ODD es más barato por término medio, pero la ventaja se estrechó hasta desaparecer cuando se pulió el montaje; el sobrecoste estructural de Cerebro Vivo es moderado (0–50%).
4. **Rigor y memoria:** Cerebro Vivo aporta spec, lecciones y registro; el beneficio se verá en el mantenimiento, que este experimento no midió.
5. **Mejor combinación observada:** método + reglas de seguridad (D o C) con coste bajo y 0 fallos de seguridad. Si el proyecto es largo o lo van a retomar otras IAs o personas, D (Cerebro Vivo + reglas); si es una tarea puntual y barata, C (ODD + reglas).

## 9. Qué haría después (decide Darwin)
- **Ya hecho:** skill de seguridad en el arnés 1.30.0 (es/en).
- **Propuesto, no hecho:**
  1. Una ronda 5 de **mantenimiento**: tomar los módulos de la ronda 4 y pedir a una sesión nueva (sin memoria de la anterior) que añada una función, para medir qué deja cada método (D frente a C).
  2. Pasar el módulo ganador a `vcsim`/`pyvmomi` (necesita el sí de Darwin para instalar Go o descargar el binario) y repetir la prueba de seguridad contra un servidor que no sea el laboratorio.
  3. Revisar el reglamento del aprobador (`AGENTS.md`) para que no se contradiga (la regla «vcsim»).
  4. Arreglar el fallo de entorno `test_soporte_mac` (fin de línea de Windows).
  5. Marcar el punto 37 de `pendientes.md` como cerrado cuando Darwin lo dé por bueno.
