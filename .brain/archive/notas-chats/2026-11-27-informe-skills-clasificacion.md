# Informe de skills: uso y utilidad (spec 096, fases 1 y 2)

- **Fecha:** 2026-11-27 · **Comando:** `python .brain/guardianes/medir.py --skills --todos`
- **Alcance:** 25 carpetas de registros de Claude Code (todos los proyectos de trabajo; se dejaron fuera los experimentos `bench`, `scratch`, `ronda`, `rama-` y `encargo`). Solo Claude Code: no cuenta lo que hicieron Codex ni Gemini.
- **Qué cuenta «usos» y «lecturas»:** usos = llamadas a la herramienta Skill o comandos `/skill`; lecturas = la IA abrió el `SKILL.md` sin pasar por esa herramienta (nuevo en esta medición).
- **Resultado:** **33 de 44 skills se usan** en algún proyecto (contra 15 de 44 al medir solo este repo). Las 11 sin ningún uso ni lectura están en la sección 4.
- **Esto es una propuesta.** No se ha quitado, fusionado ni cambiado ninguna skill. Cada cambio espera el sí de Darwin.

## 1. Núcleo (se usa a menudo)
| Skill | Usos | Lecturas | Proyectos | KB |
|---|---|---|---|---|
| traspaso-in | 634 | 6 | 13 | 4,7 |
| subir-a-github | 74 | 2 | 10 | 1,3 |
| directora-de-fabrica | 73 | 24 | 7 | **14,8** |
| actualizar | 34 | 2 | 9 | 2,1 |
| traspaso-out | 32 | 0 | 6 | 2,9 |
| pendiente | 28 | 0 | 8 | 1,4 |
| auditor | 24 | 0 | 6 | 4,2 |
| fabrica | 16 | 10 | 7 | 5,5 |
| trocea | 15 | 0 | 5 | 2,0 |
| pendientes-solo-lo-que-falta | 13 | 0 | 6 | 0,9 |
| version | 12 | 0 | 7 | 1,8 |

Propuesta: dejarlas y solo afinar su descripción. La excepción es `directora-de-fabrica` (ver sección 3).

## 2. A demanda (poco uso, pero cada una tiene su motivo)
`prompt-inicial`, `cerrar-una-tarea` (2 usos y 4 lecturas, pero el cierre ocurre en cada chat vía hooks: el 0 engañaba), `revisor-de-consumo`, `secretos-fuera-del-repo`, `spec-antes-de-programar`, `quitar-codigo-antiguo-con-test`, `licencia-antes-de-usar`, `prueba-de-uso-real`, `revisor-de-spec` (solo lecturas), `vigilar-librerias` (solo lecturas), `revisar-indices-de-ia`, `revisor-independiente`, `cero-dependencias`, `colabora`, `diapositivas`, `guardian-avisa-o-bloquea` (solo lecturas), `leccion`, `resumen`, `acorta`, `revisar-contenido`.

También entran aquí tres sin uso que los guardianes o otras skills sí citan y que son recientes o de uso raro:
- `sincronizar` (spec 093, citada por 4 guardianes), `hermanos` (citada por 4 guardianes), `chat-nuevo` (2 guardianes y `CLAUDE.md`), `memoria-traspaso` (4 skills y 1 guardián la citan).
- `seguridad-en-sistemas-reales`: 0 usos, pero está pensada para proyectos que actúan sobre servidores reales (VMware). Se queda; su valor es evitar un daño, no repetirse.

Propuesta: se quedan. Mejorar solo la descripción de las que se usan menos de lo que cabría esperar.

## 3. Fusionar o acortar
- **`adopta` + `adoptar-indice-existente`** (1,8 + 2,4 KB; 3 y 1 usos). `adopta` se declara «atajo» de la otra. Propuesta: dejar una sola, con `/adopta` como nombre corto.
- **`directora-de-fabrica` (14,8 KB, la mayor, 73 usos y 24 lecturas).** Se usa mucho, así que pesa cada vez que se carga. Propuesta: cuerpo corto con lo esencial y el detalle en archivos aparte que se leen solo si hace falta. **Espera al pendiente 62** (revisión de la fábrica), porque lo que salga de ahí puede cambiar su contenido.
- **`revisor-de-spec` (7,5 KB; solo lecturas, un proyecto).** Mismo trato: trocear tras el 62.
- **`fabrica` (5,5 KB).** Mirarla junto con la anterior.
- **Los tres revisores** (`revisor-independiente`, `revisor-de-spec`, `revisor-de-consumo`): hacen cosas distintas y se usan; no fusionar. Solo comprobar que sus descripciones dejan claro cuál elegir.

## 4. Candidatas a archivar (0 usos, 0 lecturas en ningún proyecto)
Las seis de abajo se moverían a `.brain/archive/skills/`, **nunca se borrarían**. Son candidatas, no sentencias: con pocos chats un 0 es una tendencia.
| Skill | KB | Por qué es candidata | Duda antes de archivar |
|---|---|---|---|
| implementada-no-es-hecha | 0,8 | La regla 5 de la constitución y `pendientes-solo-lo-que-falta` ya la dicen | Ninguna: es repetición |
| explicar-a-darwin-en-llano | 0,8 | `CLAUDE.md` y la memoria de Darwin ya piden lenguaje llano; nadie la cita | Si se archiva, la regla queda solo en esos sitios |
| probar-guardian-en-windows | 0,8 | Sin citas; la lección de consolas de Windows ya está en `lecciones/` | Revisar que esa lección cubre todo |
| mover-no-borrar | 0,8 | 0 usos; dos skills la nombran, pero la regla es general | Quizá mejor fundirla en `trocea` |
| buscar-en-la-memoria | 1,6 | 0 usos; existe `buscar.py`, que el arranque ya recomienda | Su descripción puede estar mal: **revisar antes de archivar**, porque es justo lo que el pendiente 66 quiere potenciar |
| guardar-respuesta | 1,7 | 0 usos; `respuestas.py` hace el trabajo | Dos skills la citan |

Las otras cinco sin uso (`sincronizar`, `hermanos`, `chat-nuevo`, `memoria-traspaso`, `seguridad-en-sistemas-reales`) quedan en la sección 2 y no se proponen para archivar.

## 5. Lo que este informe no sabe
- No mide Codex ni Gemini: una skill que solo usen ellos saldría con 0.
- Una skill usada «de memoria» por la IA, sin leer el archivo ni llamarla, sale con 0.
- `sincronizar` y `hermanos` son recientes: 0 aún no dice nada.
- Un proyecto con el arnés viejo puede no tener todavía una skill nueva.

## 6. Qué decide Darwin
1. ¿Archivar las seis candidatas de la sección 4, todas o algunas? Recomendado: las tres seguras (`implementada-no-es-hecha`, `explicar-a-darwin-en-llano`, `probar-guardian-en-windows`) y dejar las otras tres a la espera de revisarlas.
2. ¿Fusionar `adopta` con `adoptar-indice-existente`? Recomendado: sí.
3. ¿Trocear `directora-de-fabrica`, `revisor-de-spec` y `fabrica` después del pendiente 62? Recomendado: sí.
