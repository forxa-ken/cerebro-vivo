# Informe del experimento Cerebro Vivo contra ODD — Ronda 2 (2026-11-09)

Claude (cerebro-vivo #33) para Darwin. Mismos módulos que la ronda 1 (A: Instantáneas con Cerebro Vivo; B: Clonado con ODD), ramas nuevas `exp2-*` desde master, mismo encargo con reglas de la ronda 2. **Muestra de 1 por lado: tendencia, no prueba.** Esta ronda ya no sufre los cuelgues: la causa (Codex esperaba la entrada estándar) está corregida.

## Resultado de calidad (comprobado por mí)
| | A (Cerebro Vivo) | B (ODD) |
|---|---|---|
| Criterios del encargo | 7 de 7, con prueba | 7 de 7, con prueba |
| Pruebas del módulo | 17 nuevas | 32 nuevas (49 en total) |
| Suite completa | 1 fallo ajeno (instalador de Mac, fin de línea de Windows en ese checkout; no es del módulo) | todo en verde |
| Líneas de `vmware_auto` | ≈ 378 | ≈ 377 |
| Documento de uso | `INSTANTANEAS.md` | `docs/clonado.md` |

## Aprobador (Codex)
- **A:** 9 llamadas: 1 error técnico (no cuenta), 7 RECHAZADA y 1 APROBADA. Las 7 rechazadas llegaron en unos 2 minutos: A reintentó deprisa por detalles que su spec no escribía (lo dice en su `resultado.md`).
- **B:** 3 llamadas: 1 error técnico (timeout, justo cuando el arreglo aún no estaba en su carpeta), 1 RECHAZADA (faltaba dejar explícito que todo clonado pasa por el motor con ensayo) y 1 APROBADA.
- Mismo patrón que la ronda 1: A, que escribe la spec antes, es rechazada más veces; B llega antes a la aprobación. El aprobador no es determinista, así que no es concluyente.

## Coste (`medir.py` igual en las dos)
| | A | B |
|---|---|---|
| Coste total | ≈ 481k | ≈ 372k |
| Tokens nuevos | 67k | 69k |
| Salida | 29k | 24k |
| Arranque | 75k | 74k |
| Turnos de la IA | 26 | 18 |
| Caché al empezar | caliente | fría |

- A cuesta ≈ 1,3 veces B (en la ronda 1 era 2,9, con cuelgues). En tokens nuevos están igual. La diferencia está en turnos y salida: los reintentos del aprobador.
- Ojo: la caché de A empezó «caliente» y la de B «fría», lo que abarata a A en el «coste»; es un sesgo pequeño a favor de A.

## Ronda 1 frente a ronda 2
- A bajó de 744k a 481k y B de 257k a 372k (B subió: más pruebas y más tareas). Las diferencias entre rondas dentro de un mismo lado son del mismo orden que la diferencia entre lados, así que **no hay una conclusión firme sobre cuál método es mejor**.
- Constante en las dos rondas: calidad equivalente (7 de 7); Cerebro Vivo cuesta algo más por el rigor previo (spec) y los rechazos del aprobador; ODD llega antes al resultado.

## Lo que decide Darwin
Calidad fina (claridad de errores, nombres, documentación): revisar `vmware_auto/INSTANTANEAS.md`, `docs/clonado.md` y `experimento/resultado.md` de cada rama (carpetas `vmware-automatizacion-ronda2-A` y `-B`).

## Análisis a fondo (leído el código de las dos ramas)
- **Diseño A:** el motor ganó un parámetro opcional `detalle` y el módulo es una fachada fina (34 líneas) que solo llama al motor; el motor no sabe nada de instantáneas. Cuatro operaciones, tres con visto bueno donde toca.
- **Diseño B:** el motor importa `clonado` y, para decidir si un clon es «grande», lee `self.backend.vms` (estructura interna del laboratorio). Con un backend real (`vcsim`) sin ese atributo, la plantilla se tomaría como tamaño 0 y un clon grande **no pediría visto bueno** cuando el usuario no indica CPU/memoria. Hallazgo por lectura del código, no probado; se arreglaría preguntando el tamaño al backend. Hoy, en el laboratorio, funciona.
- **Cobertura:** B tiene más pruebas (32 frente a 17) para una operación; A tiene 17 para cuatro. Los 7 criterios están cubiertos en ambos.
- **Memoria que queda:** A deja lecciones y una línea en `decisions.log`; B deja `odd/tasks/` y `docs/`. El valor de la memoria de A solo se ve en sesiones futuras: este experimento no lo mide.
- **Límite común:** el laboratorio se reinicia en cada llamada de la línea de comandos; solo B lo declara.
- **Sesgo del módulo:** A tiene tres acciones que exigen visto bueno frente a una de B, así que el aprobador tenía más sitios donde rechazar la spec de A.

## Verificación de calidad (ejecutada, 2026-11-09)
- **Hueco de B CONFIRMADO con una prueba:** plantilla de 16 CPU / 64 GB, `motor.clonar("plantilla-grande", ["x1"])` sin indicar CPU/memoria. Con el laboratorio de B: BLOQUEADO (bien). Con un backend que no expone `.vms` (como lo sería uno real): **clona sin visto bueno**. La regla de seguridad depende de un detalle interno del laboratorio y ninguna de las 32 pruebas de B lo detecta.
- **Línea de comandos, 6 casos por rama (simular, falta de visto bueno, máquina/instantánea/plantilla inexistente, nombre repetido o ya existente):** ambas dan mensajes claros en español, no tocan nada y bloquean lo delicado. Sin diferencia apreciable de claridad.
- **Documentación:** las dos traen comandos, ejemplos, códigos de salida y fallos provocados. B además documenta el umbral de «grande» con valores; A documenta el gasto de 2 GB por instantánea.
- **A:** sin hallazgos negativos en estas pruebas. Límite común: restaurar/borrar no exigen haber ensayado antes, solo `--confirmo` (así lo fija la spec 001).
