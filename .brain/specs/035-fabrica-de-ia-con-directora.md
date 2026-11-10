# Spec 035: Fábrica de IA con directora y varias IA en un proyecto

- **Estado:** aprobada por Darwin el 2026-11-10 tal como está (las preguntas 1 y 4 de la sección 7 siguen abiertas y se deciden al empezar la Fase 1; cada fase pide su visto bueno)
- **Fecha:** 2026-11-09
- **Cierra:** pendiente 19 (varias IA con responsabilidades distintas) y el diseño de la fábrica pedida por Darwin.

## 1. Objetivo
Definir cómo trabajan varias IA a la vez en un mismo proyecto sin pisarse y sin hacer lo que nadie pidió. Una **directora** convierte el objetivo de Darwin en una spec; **ejecutoras** hacen encargos pequeños; un **revisor** independiente verifica; **programas (guardianes)** hacen cumplir los límites. Darwin aprueba en tres puertas.

**Problema real que evita:** el «Frankenstein» de un autor externo (vídeo «Cómo hacer que una IA construya el proyecto que tú quieres»): con un objetivo de «que pasen las pruebas», el agente rellenó los huecos de la spec con suposiciones, quitó requisitos «por seguridad» y añadió comportamientos no pedidos (cambió un token por OAuth con QR). Pasar pruebas no basta; los huecos de la spec los decide un humano.

## 2. Qué se sabe y qué no (investigado el 2026-11-09)
- **Codex:** familia GPT-6 (Astra, Sol, Luna). Luna es la barata; según agregadores, peor que Sonnet 5.5 en pruebas de código (SWE-bench Pro 62,7 % frente a 81,3 %; DeepSWE 66,6 % frente a 71,0 %). Nada fiable sobre su obediencia a instrucciones. `codex exec` corre sin pedir permisos y, por defecto, en solo lectura; hay un reporte (openai/codex#24135) de que las herramientas MCP se cancelan en ese modo. **No probado por nosotros.**
- **Sonnet 5.5:** contexto de 1M y salida de 128K. Anthropic reconoce que rinde peor en esfuerzo «máximo» por cambios fuera de lo pedido; hay reportes de exceso de sub-agentes y de pararse a preguntar. Varias fuentes sugieren que **Opus dirija y Sonnet ejecute**. Son opiniones, no pruebas.
- **Consecuencia:** la directora es Opus a esfuerzo medio o alto (nunca máximo); lo que haya que garantizar lo garantizan programas, no la obediencia de una IA.

## 3. En alcance (In-Scope)
- [ ] **R1 · Papeles y dueños.** Un solo proyecto, varios chats con papeles: directora (Opus, única que habla con Darwin, no programa), ejecutora (Claude, o Codex con Luna para volumen), revisor (Claude en otro chat con instrucciones distintas; nadie se aprueba a sí mismo). Cada archivo tiene un solo dueño; el ajeno se lee, no se escribe. Los roles quedan en un archivo único.
- [ ] **R2 · Carta de la fábrica.** Archivo corto escrito por Darwin: objetivo, prohibiciones, gasto, número de encargos y tiempo máximos. La directora no puede editarlo (guardián).
- [ ] **R3 · Tres puertas humanas.** (a) Darwin aprueba la **spec** antes de lanzar nada. (b) Todo **hueco** de la spec se registra y se pregunta a Darwin; nadie asume. (c) Darwin aprueba el **informe final** (lo pedido, lo hecho, lo extra). Lo extra se revierte salvo que él lo acepte.
- [ ] **R4 · Spec congelada.** Tras aprobarla se guarda su huella. Un requisito nuevo va a un archivo de «propuestas» y espera aprobación. Ningún chat puede añadir ni quitar requisitos.
- [ ] **R5 · Contenido mínimo de la spec** (de un autor externo): qué puede hacer el usuario (acción, condiciones de partida, permisos), resultado esperado, qué decisiones y funciones anteriores hay que respetar, cómo se demuestra y qué evidencia queda guardada.
- [ ] **R6 · Encargo.** Archivo corto en `.brain/fabrica/encargos/` con: requisito que cumple (obligatorio), archivos permitidos, prueba que lo da por bueno. Un encargo sin requisito aprobado se rechaza solo.
- [ ] **R7 · Comprobaciones automáticas (sin IA).** Guardián de **alcance del encargo** (diff contra archivos permitidos), pruebas del requisito en verde, sin dependencias ni accesos nuevos, sin secretos, topes de gasto/encargos/tiempo, parada y aviso tras dos fallos seguidos. Un control que falla impide dar el encargo por terminado; uno que no se ejecutó queda visible.
- [ ] **R8 · Revisión por riesgo.** El revisor comprueba que lo entregado responde al requisito, contrasta cada hallazgo con el código real y lo ordena por gravedad. Lo trivial se corrige y se anota; lo que afecta a un requisito o a una decisión anterior se escala a Darwin.
- [ ] **R9 · Seguridad sin cambiar lo pedido.** Ninguna IA cambia un requisito «por seguridad». Si ve un riesgo, lo registra como hueco o propuesta y pregunta. Se añade esta regla a la skill `seguridad-en-sistemas-reales`.
- [ ] **R10 · Evidencia por requisito.** Cada requisito cerrado deja en `.brain/fabrica/evidencia/` qué se comprobó, cómo y el resultado.
- [ ] **R11 · Aislamiento.** Cada ejecutora trabaja en su propio worktree y rama; el revisor lee sin cambiar. Dos escritoras nunca comparten carpeta.
- [ ] **R12 · Instalador respeta lo ajeno** (`indices_ajenos` en `guardianes.json`): reinstalar con `--ias gemini` o `--ias codex` no añade el bloque de memoria a un `AGENTS.md` que su dueño no quiere tocado.
- [ ] **R13 · Prueba mínima antes de nada autónomo.** Un solo encargo, ida y vuelta directora → ejecutora → revisor → directora, en un proyecto de prueba, midiendo gasto de cada IA. Dos variantes: todo Claude, y ejecutora Codex Luna. Si el puente con Codex no funciona sin desactivar su protección, se informa a Darwin y no se sigue por esa vía.

## 4. Fuera de alcance (Out-of-Scope)
- No programar la fábrica completa ni dejarla autónoma hasta que R13 salga bien y Darwin lo apruebe.
- No instalar Go ni `vcsim` (prohibición vigente de Darwin).
- No tocar `CLAUDE.md` ni la constitución.
- No subir nada a GitHub sin orden de Darwin.
- No cambiar los proyectos que ya usan el arnés (el reparto llegaría después con `VERSION`, `CAMBIOS.md` y manifiesto).

## 5. Plan de implementación (por fases; cada una con visto bueno de Darwin)
1. **Fase 0 · Aprobar esta spec** y decidir las preguntas abiertas (sección 7).
2. **Fase 1 · Archivos y reglas:** carta de la fábrica, formato de encargo y de evidencia, archivo de roles, registro de huecos y propuestas (es/en).
3. **Fase 2 · Guardianes:** alcance del encargo, huella de la spec congelada, protección de la carta, topes y parada (textos es/en en `textos.py`).
4. **Fase 3 · Skills:** `directora-de-fabrica`, `revisor-independiente` y la regla de R9 en `seguridad-en-sistemas-reales` (cada una con edición `.en.md`).
5. **Fase 4 · Prueba mínima (R13)** y medición del gasto.
6. **Fase 5 · Decidir con datos:** ampliar, ajustar o descartar.
7. Instalador `indices_ajenos` (R12) puede ir en paralelo; es independiente.

## 6. Plan de verificación
- Tests: `python -m unittest discover tests` (todo en verde); una prueba por guardián nuevo y la de paridad es/en.
- Prueba mínima R13: con un requisito de ejemplo, comprobar que (a) un encargo fuera de la lista de archivos se rechaza sin gastar IA, (b) un hueco provoca pregunta y no suposición, (c) un requisito añadido por la ejecutora queda en «propuestas», (d) el informe final lista lo extra.
- Medir gasto por papel con `medir.py`. Lo no probado se dice como no probado.

## 6b. Resultados de las pruebas hechas (2026-11-09)
- **Prueba 1 · addon CopyChatLB (WoW):** ejecutora Codex Luna (alto), ~63k + ~49k tokens; el revisor devolvió el encargo 1 y se corrigió en 1b. No se probó en el juego: Darwin descartó el producto porque ya existía (Darwin aclaró el 2026-11-10 que comprobar si el producto ya existía fue algo puntual de ese addon, no un paso de la fábrica).
- **Prueba 2 · módulo «iconos de clase» de GuildControlForever:** directora (Opus, esta sesión) con spec aprobada por Darwin; ejecutora y revisor aparte, ambos Claude Sonnet. El revisor dio «apto con reparos» y halló 3 fallos menores (variable global suelta, icono que podía quedarse si el juego no avisa al quitar la barra) y 2 huecos de la spec (aviso de barras apagadas, prueba automática). Se devolvió a la ejecutora, se corrigió y la directora lo comprobó (sintaxis LuaJIT, 4 pruebas, sin locales nuevos de primer nivel). **Darwin lo probó en el juego y funciona**, en español e inglés. Commit local `3274e33` del addon, sin subir.
- **Lo que enseñan:** (1) el revisor aparte sirvió de verdad: sin él esos reparos no se habrían visto; (2) la puerta humana que más valió fue aprobar la spec antes de programar (Darwin añadió ahí tamaño y opacidad); (3) la ejecutora hizo bien lo que se le pidió y calló lo que no se le pidió (aviso y pruebas), así que el encargo debe listar **todos** los puntos de la spec; (4) la directora tuvo que localizar el proyecto real y su código antes de encargar.
- **Lo que NO se probó:** la prueba 2 no usó Codex ni los guardianes de alcance (fases 2 y 3 siguen sin programar); el alcance de archivos lo vigiló la directora a mano. No se midió el gasto con `medir.py`.
- **Prueba 3 · módulo «posición vertical del icono» (GuildControlForever), 2026-11-10:** directora Claude, ejecutora Codex Luna (alto), spec aprobada por Darwin. Codex terminó con salida 0 y ~40.478 tokens. El guardián `alcance.py` lo dejó pasar: tocó solo los 4 archivos permitidos. La directora comprobó: sintaxis LuaJIT de los 3 .lua, 4 pruebas del módulo y las 295 del addon (OK, 8 omitidas), diff de 18 líneas leído a mano. Codex no pudo ejecutar Python ni LuaJIT en su entorno y lo dijo con honestidad. **Darwin lo probó en el juego (2026-11-10): funciona, el icono se mueve al instante.** No se lanzó revisor aparte (diff mínimo). Gasto medido: solo los tokens del log de Codex; `medir.py` sigue sin usarse.
- **Respuestas ya dadas por los hechos:** pregunta 2 (proyecto de prueba): CopyChatLB y GuildControlForever; pregunta 3: primera prueba con Codex Luna, segunda solo Claude.

## 7. Preguntas abiertas para Darwin
1. ¿Opus como directora solo en las decisiones, y la lectura detallada de resultados en Sonnet para ahorrar cuota?
   - **Respondida por Darwin (2026-11-10):** directora Opus con esfuerzo medio, una por proyecto (no una general, para no mezclar); lectura detallada de resultados en Sonnet esfuerzo medio.
2. ¿Cuál es el proyecto de prueba para R13 (no LoboHook)?
3. ¿Codex Luna en esfuerzo alto como ejecutora desde la primera prueba, o primero solo Claude?
4. ¿Topes iniciales de la carta (encargos, gasto, tiempo)?
   - **APROBADO por Darwin (2026-11-10):** criterio: el gasto semanal de Codex está al 99 % libre; prima llegar al objetivo sin agotar el crédito. Topes: **por encargo** hasta 2 ventanas de ~200.000 tokens (≈400.000 gastados); salta el primero que se alcance (400.000 gastados o 2 ventanas) y se para y pregunta. **Por misión:** hasta 10 encargos y 1.000.000 de tokens de Codex. **Freno general:** si el gasto semanal de Codex baja del 50 % libre, parar y preguntar. Se revisan con datos en la Fase 5.
   - **Codex bajo reglas de Cerebro (aprobado):** la ejecutora recibe una versión reducida de las reglas (tope de ventana de 200k, traspaso al llenarse, nota en `.brain/notas-chats/`); no escribe en el resto de `.brain/`. El chat nuevo de Codex lo abre el director con el traspaso que Codex dejó. Comprobar antes qué del arnés (`AGENTS.md`, guardianes) funciona con Codex; `traspaso-in`/`traspaso-out` en Codex ya los probó Darwin el 2026-11-08 (punto 13, hechos.md); lo que NO está probado es el aviso automático de ventana llena en Codex (el hook `Stop` es de Claude) y que la directora abra el chat nuevo de Codex con su traspaso. La carta de ejecutora entra en la Fase 1.

## 8. Límites honestos
- Los guardianes atrapan el desvío en archivos y pruebas, no el de significado: si un requisito está mal escrito, todos cumplen y sale mal. Por eso la puerta (a) es la más importante.
- Una fábrica multiplica los chats y el gasto; el costo real solo se sabe midiendo R13.

## 9. Cierre
- [x] Spec aprobada por Darwin antes de programar (2026-11-10)
- [ ] Línea añadida a `.brain/decisions.log`
- [x] Pendiente 19 enlazado a esta spec en `pendientes.md`
