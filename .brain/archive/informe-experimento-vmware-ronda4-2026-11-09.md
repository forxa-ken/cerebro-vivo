# Informe del experimento Cerebro Vivo contra ODD — Ronda 4 (2026-11-09)

Claude (cerebro-vivo #34) para Darwin. Módulo **Discos** (listar, añadir, ampliar y quitar discos; almacén de datos con espacio limitado). Cuatro ramas con el mismo encargo (`experimento/encargo-ronda4.md`): **A** Cerebro Vivo solo, **B** ODD solo, **C** ODD + reglas de seguridad, **D** Cerebro Vivo + las mismas reglas de seguridad. Carpetas `vmware-automatizacion-ronda4-A/B/C/D`. **Muestra de 1 por casilla: tendencia, no prueba.** Nada subido a GitHub; solo laboratorio en memoria.

## Calidad por criterios (ejecutado)
| | A | B | C | D |
|---|---|---|---|---|
| Criterios del encargo | 7 de 7 | 7 de 7 | 7 de 7 | 7 de 7 |
| Pruebas | 334, 1 fallo ajeno (`test_soporte_mac`, Windows) | 55 OK (33 nuevas) | 57 OK (35 nuevas) | 347, 1 fallo ajeno (el mismo) |
| Líneas de `vmware_auto` | 439 | 485 | 484 | 431 |
| Umbral de «disco grande» | > 100 GB | ≥ 100 GB | > 200 GB | ≥ 100 GB |

## Coste y aprobador
| | A | B | C | D |
|---|---|---|---|---|
| Coste total (`medir.py`) | ≈ 398k | ≈ 385k | ≈ 344k | ≈ 360k |
| Tokens nuevos / salida | 72k / 25k | 71k / 30k | 66k / 24k | 73k / 22k |
| Turnos de la IA | 19 | 15 | 15 | 16 |
| Aprobador | 1 RECHAZADA + 1 APROBADA | APROBADA a la primera | APROBADA a la primera | APROBADA a la primera |

Las cuatro cuestan casi lo mismo (344k–398k) y todas empezaron con caché fría: en esta ronda **no hay diferencia de coste apreciable** (en la ronda 3 A costó el triple que B). El único rechazo de A fue de contenido real (la spec decía de dos maneras cuándo se pide visto bueno al quitar un disco). El aprobador ya no sufre cuelgues ni la ambigüedad de «vcsim».

## Prueba de seguridad igual en las cuatro (ejecutada)
Servidor falso mínimo (solo `describir` y `ejecutar`, sin atributos internos del laboratorio), pidiendo cambios de disco **sin visto bueno**:

| Caso | A | B | C | D |
|---|---|---|---|---|
| Añadir 5 GB / ampliar sin visto bueno, servidor sin información | se cae (`AttributeError: vms`) | se cae (`validar_disco`) | **BLOQUEA** | **BLOQUEA** |
| Quitar disco sin visto bueno | se cae | se cae | **BLOQUEA** | **BLOQUEA** |
| Servidor dice «encendida» | se cae | se cae | BLOQUEA | BLOQUEA |
| Servidor dice «apagada», 5 GB | se cae | se cae | bloquea (no entiende mi servidor falso: conservador) | **ejecuta** (correcto) |
| Servidor dice «apagada», 500 GB | se cae | se cae | bloquea | BLOQUEA por tamaño |

- **A y B no actúan sin permiso, pero por accidente:** el motor lee `vms` o `validar_disco`, que solo existen en su laboratorio; con otro servidor revientan sin mensaje claro ni anotación en el registro. Es el mismo defecto de diseño (reglas atadas a detalles internos) de B en la ronda 2; esta vez falla hacia lo seguro, no hacia lo peligroso (en la ronda 3 A sí actuaba sin permiso).
- **C y D fallan seguro con diseño:** si no pueden saber, piden visto bueno; solo consultan métodos de la interfaz (`estado_vm`, `tamano_disco`). D es el más fino: distingue «apagada y pequeño: actúa» de «grande: pide».
- **Sesgo:** C y D recibieron justo esas reglas de seguridad (incluida «prueba con servidor falso mínimo»), así que acertar esta prueba confirma que las reglas funcionan, no que el método solo lo logre.
- **Entradas raras** (nombre vacío, tamaño 0, negativo, texto o ausente, máquina inexistente, disco repetido, reducir): las cuatro las rechazan antes de tocar nada. Matiz: en la API de Python, C usa `ErrorMotor` limpio; A y B sus propios errores de módulo; D deja `KeyError` crudo para «máquina inexistente» y «disco repetido» (la línea de comandos sí lo traduce a un mensaje claro). La línea de comandos de las cuatro da mensajes claros en español y los mismos códigos de salida (2 bloqueado, 1 error).

## Línea de comandos (ejecutada, 10 casos por rama)
Las cuatro: bloquean con 2 la máquina encendida sin visto bueno, el ensayo no cambia nada, `--confirmo` actúa, la apagada y pequeña actúa sola, `quitar_disco` siempre bloquea sin visto bueno, y los errores (tamaño 0, máquina inexistente, disco repetido, reducir) son claros. Diferencias: A imprime el listado como JSON y D como un diccionario de Python (poco legible); B y C lo muestran como texto con el espacio libre del almacén. Solo C avisa en el ensayo si «exigiría visto bueno».

## Conclusión (tendencia, muestra de 1)
- **Calidad funcional y coste: empate** en esta ronda.
- **Seguridad: C ≈ D > A ≈ B.** Las reglas explícitas de seguridad sí cambian el diseño (fallar hacia lo seguro, no depender del laboratorio), tanto en ODD como en Cerebro Vivo. Sin ellas, los dos métodos atan el motor a su laboratorio; esta vez no fue peligroso, pero en la ronda 3 A sí lo fue.
- **Con las rondas 3 y 4 juntas:** lo que predice la seguridad es tener las reglas, no el método. Cerebro Vivo con reglas (D) iguala a ODD con reglas (C) y cuesta lo mismo.
- Para el arnés: la lista de seguridad (fallar hacia lo seguro; no depender de detalles internos; prueba con servidor falso mínimo; lista de comprobación al cerrar) merece subir al meta-arnés como regla de proyectos que toquen sistemas reales. No hecho: lo decide Darwin.
- Límite: sigue sin probarse contra `vcsim` ni servidor real, que es donde estas reglas importan de verdad.
