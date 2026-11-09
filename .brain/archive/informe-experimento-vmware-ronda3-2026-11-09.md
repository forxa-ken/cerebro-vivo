# Informe del experimento Cerebro Vivo contra ODD — Ronda 3 (2026-11-09)

Claude (cerebro-vivo #34) para Darwin. Módulo **Redes**, mismo encargo (`experimento/encargo-ronda3.md`) en tres ramas: **A** Cerebro Vivo, **B** ODD solo, **C** ODD + reglas de seguridad en su CLAUDE.md. Carpetas `vmware-automatizacion-ronda3-A/B/C`. **Muestra de 1 por lado: tendencia, no prueba.** Nada subido a GitHub; solo laboratorio en memoria.

## Calidad por criterios (comprobado ejecutando)
| | A | B | C |
|---|---|---|---|
| Criterios del encargo | 7 de 7 | 7 de 7 | 7 de 7 |
| Pruebas nuevas de Redes | 29 | 21 | 26 |
| Suite (ramas B y C solo traen las pruebas del proyecto) | 346, 1 fallo ajeno (`test_soporte_mac`, fin de línea de Windows) | 43 OK | 48 OK |
| Líneas de `vmware_auto` | 409 | 384 | 436 |
| Documento de uso | `docs/redes.md` | `odd/redes-uso.md` | `docs/redes.md` |

## Coste (`medir.py` igual en las tres)
| | A | B | C |
|---|---|---|---|
| Coste total | ≈ 778k | ≈ 265k | ≈ 542k |
| Tokens nuevos | 91k | 49k | 70k |
| Salida | 40k | 17k | 33k |
| Turnos de la IA | 43 | 13 | 29 |

B cuesta ≈ un tercio de A; C queda en medio. Todas empezaron con caché caliente (sin sesgo entre ellas).

## Aprobador (Codex), según `experimento/aprobaciones.jsonl`
- A: 7 llamadas, 6 RECHAZADA + 1 APROBADA (4 rechazos fueron la ambigüedad de «vcsim», ya aclarada: no cuentan contra el método).
- B: **1 llamada, APROBADA a la primera.**
- C: 8 llamadas, 7 RECHAZADA + 1 APROBADA (C anota veredictos contradictorios para el mismo texto: el aprobador no es determinista).

## Prueba de seguridad igual en las tres (ejecutada)
Servidor falso mínimo, **sin atributos internos del laboratorio** (solo `describir` y `ejecutar`), máquina que puede estar encendida; se pide conectar/desconectar red **sin visto bueno**:

| Caso | A | B | C |
|---|---|---|---|
| Servidor falso, sin visto bueno | **EJECUTA sin pedir permiso** | se cae con `AttributeError` (no actúa, pero no por regla: sin mensaje claro ni anotación) | **BLOQUEA** pidiendo visto bueno |
| Servidor dice «encendida» | **EJECUTA** | se cae igual | BLOQUEA |
| Servidor dice «apagada» | ejecuta (correcto) | se cae (no puede) | ejecuta (correcto) |
| Entradas raras (vacío, espacios, `None`, número) | error claro (aunque `ValueError` crudo) | error, pero `None`/número dan «no existe la máquina None» | error claro y específico con texto «debe ser un texto» |

- **A: cierra mal.** El motor pregunta al servidor `es_en_caliente`; si el servidor no lo tiene, asume «no es en caliente» y actúa. Es el mismo hueco que mostró B en la ronda 2: con un servidor real (`vcsim`/`pyvmomi`) un cambio en caliente pasaría sin visto bueno. Sus 29 pruebas no lo detectan. Compensa con una regla extra buena: exige **ensayo previo** registrado antes de actuar en caliente.
- **B: depende del laboratorio.** `redes.validar` lee `lab.vms` y `lab.redes`; con otro servidor falla por la fuerza (cierra, pero por accidente). El propio B lo admite: «el motor conoce el módulo».
- **C: falla seguro.** Si no puede saber que la máquina está apagada, la trata como encendida y pide visto bueno. Tiene pruebas con servidor falso (`TestSeguridadServidorFalso`). **Ojo, sesgo de la prueba:** C recibió esas reglas de seguridad justo para este escenario; el resultado confirma que las reglas funcionan, no que ODD solo lo hiciera. B, que es ODD sin reglas, no lo hizo.

## Línea de comandos (ejecutada: listar, bloqueo en caliente, ensayo, confirmo, apagada, inexistente, red caída, red llena)
- Las tres bloquean con código 2 sin visto bueno, ensayan sin tocar nada y dan errores claros en español para máquina inexistente, red caída y red llena. El laboratorio se reinicia en cada llamada de la línea de comandos en las tres.
- Diferencias menores: A imprime el listado como JSON (menos legible que el texto de B y C); B avisa en el ensayo «en caliente: exige visto bueno»; C pide `--red` como opción en vez de argumento posicional.

## Conclusión (tendencia, muestra de 1)
- **Calidad funcional: empate** (7 de 7 en las tres).
- **Seguridad: C > B > A**, con la salvedad del sesgo de C. Confirma lo que dijo Darwin: ODD falla por seguridad si no se le dan parámetros; con parámetros (C) la corrige. Cerebro Vivo (A) tampoco la garantiza: su spec aprobada no pedía «fallo seguro» y la regla «actuar si el servidor no sabe» se coló.
- **Coste: B < C < A.** Los parámetros de seguridad cuestan ≈ 2× lo de B pero ≈ 0,7× lo de A.
- Idea aplicable al arnés: añadir a las reglas de Cerebro Vivo la lista de seguridad de C («si falta información, tratar como delicado»; probar con servidor falso mínimo).

## Pendiente de decidir (Darwin)
Si se quiere repetir con más muestras (ronda 4) o si se lleva la lista de seguridad de C al arnés. No hecho nada de eso.
