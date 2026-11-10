# Informe final de la prueba R13: la fábrica de IA con TraductorVoz (2026-11-10)

**Pregunta de la prueba:** ¿puede una fábrica de IA (directora, obrera, revisora) mejorar un programa real de principio a fin, con orden, con gasto controlado y sin romperlo?
**Respuesta corta:** sí. Se reorganizó TraductorVoz en tres capas sin cambiar lo que hace, con evidencia de que sigue igual. Con salvedades, que se cuentan abajo.

## Qué se pidió y qué se hizo
- **Programa:** TraductorVoz (traductor de voz en directo con subtítulos). Rama `tres-capas`, solo en el ordenador de Darwin.
- **Misión 1:** separar el programa en entrada de audio, motor y salida de subtítulos, sin cambiar su comportamiento (encargos 001 a 006). 001 puso pruebas a lo existente; 002 a 004 hicieron la separación; 005 documentó; 006 corrigió los reparos de la revisión.
- **Misión 2 (prueba B):** encargo 007, pruebas de 9 módulos, usado para ver el relevo de Codex cuando se llena su espacio de trabajo.
- **Reparto de papeles:** directora (Claude), obrera (Codex Luna), revisora (otro chat de Claude, que no escribió el código). Darwin decide y firma las cartas.

## Resultados
| Cosa | Resultado |
|---|---|
| Pruebas automáticas | de 17 (encargo 001) a 70 al final; todas en verde |
| Revisión independiente de 001 | aprobado con observaciones menores |
| Revisión independiente de 002-005 | apto con reparos; ningún encargo devuelto; reparos hechos en el 006 |
| Comportamiento idéntico (R5) con audio real de 64 s | 8 frases iguales en texto, traducción, idioma y hablante; un 3 % más rápido |
| Prueba de Darwin con la ventana real | alemán, francés y chino, sin fallos comunicados |
| Relevo de Codex (prueba B) | funcionó: paró en el punto de control, dejó traspaso, otro Codex siguió sin repetir |

## Gasto de Codex (tokens, lo que cuesta pensar a una IA)
| Encargo | Tokens |
|---|---|
| 001 | 73.500 |
| 002 | 35.423 |
| 003 (dos tandas) | 134.444 |
| 004 | 134.428 |
| 005 | 43.151 |
| 006 | 89.173 |
| 007 (primera tanda, relevo y arreglo) | 228.505 |
| **Total** | **738.624 de 1.000.000 permitidos** |
- Solo el encargo 007 superó su tope (228.505 sobre 150.000), con permiso de Darwin. Ninguna tanda sola llegó a la ventana de 200.000.
- **No medido:** lo que gastaron la directora y las revisoras. Falta el medidor (sigue en el pendiente 19).

## Lo que la prueba NO demostró
- **El aviso automático al llenarse la ventana de Codex.** Nadie la llenó. El relevo se probó por una parada ordenada, no por un desbordamiento. Darwin decidió no construir un vigilante en vivo y aceptar el riesgo (tope de 200.000 por tanda, encargos pequeños, guardián al terminar cada tanda).
- **Revisión independiente del 007** (solo añade pruebas, no toca el programa).
- **Ventana, atajos, pausa y cambio de fuente** se probaron por Darwin a mano, sin pruebas automáticas; el revisor anotó huecos en `cambiar_fuente`, `pausar` y el cierre por silencio.
- **Voz a voz, micrófono, Mac:** fuera de la misión.

## Hallazgo del programa (no de la fábrica)
- **El programa no separa bien a las personas que hablan.** Corta por silencio y pone una huella de voz por frase; dos voces seguidas salen como una. Visto con dos audios en alemán y uno en inglés. Evidencia en `TraductorVoz-notas/evidencia-hablantes-aleman.md`. Pendiente 39, con carta nueva y permiso de descarga aparte.

## Lecciones de la fábrica (qué funcionó y qué dolió)
1. **Funcionó:** encargos pequeños y una sola cosa por encargo; ninguno devuelto.
2. **Funcionó:** la revisora distinta de la obrera encontró reparos reales que se corrigieron.
3. **Funcionó:** comparar el programa antiguo y el nuevo con un audio real. Las pruebas automáticas solas no lo habrían demostrado.
4. **Dolió:** el guardián solo mira el gasto al terminar cada tanda; no corta a mitad. El 007 se pasó por eso.
5. **Dolió:** la «foto» de control del guardián se tomó sobre la carpeta equivocada (la principal, no la de trabajo de la obrera); su «dentro del alcance» no valió y hubo que comprobarlo a mano. Tomarla con `--repo` de la carpeta de trabajo antes de lanzar.
6. **Dolió:** el Python de Codex no funcionaba en su caja; las pruebas las corrió la directora con el entorno del proyecto.
7. **Aprendido:** Codex no corre ganchos ni abre chats. El arnés instalado en Codex sirve para escribir y leer traspasos; el relevo lo hace la directora lanzando una orden nueva con ese traspaso.
8. **Aprendido:** una anotación a mano puede estar mal (el audio de prueba tenía 4 voces y se había apuntado 2). Corregir contrastando con lo real.
9. **Orden:** el chat de la directora se crea en el proyecto propio, no en cerebro-vivo. Aquí queda el informe y las lecciones.

## Qué queda
- Medidor de gasto de la fábrica (Codex y directora), pendiente 19.
- Separación de voces (pendiente 39).
- Posible revisión independiente del 007.
- Ordenar el disco al final (mover proyectos, renombrar carpeta, `git worktree repair`).

## Dónde está todo
- Diario en lenguaje llano: `.brain/archive/diario-fabrica-r13.md`.
- Hechos: `archive/hechos.md`, puntos 13 y 19-B.
- En `F:\Proyectos\TraductorVoz-notas`: revisiones, logs de Codex, evidencias y `resultado-prueba-B.md`.
- En TraductorVoz: `.brain/fabrica/` (cartas, spec, encargos, estado, gasto) y `.brain/notas-chats/`.
