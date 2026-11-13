# Hechos (tareas terminadas y probadas)

> Aquí va el detalle de cada tarea **ya probada por Darwin**. `pendientes.md` solo guarda lo que falta.
> **No abrir completo:** consultar `hechos-indice.md` y leer solo la entrada necesaria (buscar `## <Nº>`).
> La **numeración es fija**: el número que tenía el punto en `pendientes.md` no cambia al moverlo aquí.

## 36 · Prueba de retomar en el cierre (spec 041, arnes 1.41.0)
**Fecha:** 2026-11-13 · **Ref:** 
Probado por Darwin el 2026-11-13: con una decision solo hablada, la IA cerro con 2 ediciones sin aviso del guardian. Un solo caso; medicion a mano el 2026-11-27 opcional

## 42 · Modo colaborativo (spec 042, arnes 1.42.0)
**Fecha:** 2026-11-13 · **Ref:** 
Probado por Darwin: /colabora si y no, e indices_ajenos con reinstalar. Gemini como obrera NO probado (pendiente 54)

## 23 · Auditor (spec 044, arnes 1.44.0)
**Fecha:** 2026-11-13 · **Ref:** 
Probado por Darwin: estado y quien spec; aviso con codigo sale y con solo .md no

## 35 · Cierre por bloque (spec 033, arnes 1.29.0)
**Fecha:** 2026-11-13 · **Ref:** 
Probado por Darwin; medir.py --ritual: 119 avisos en 55 chats (2,2 por chat), 26,8 % del coste atribuible al arnes

## 30 · Avisos de los guardianes con el como arreglarlo (arnes 1.40.1)
**Fecha:** 2026-11-13 · **Ref:** 
Probado por Darwin con fabrica.py verificar: el aviso dice que comando lanzar

## 31 · Guardian que se repite y tokens por tarea (spec 038)
**Fecha:** 2026-11-13 · **Ref:** 
Probado por Darwin: medir.py --ultimos 3 muestra la tabla y Por tarea terminada

## 38 · Hook pre-commit de secretos funciona en worktrees
**Fecha:** 2026-11-10 · **Ref:** CAMBIOS 1.35.1
Arnes 1.35.1. El hook buscaba secretos.py con ruta relativa y fallaba en la carpeta de la pagina (worktree gh-pages). Ahora lo busca en el repo principal. Probado por Claude el 2026-11-10 en la pagina real: commit limpio pasa y commit con token falso se bloquea; prueba automatica con worktree real (410 pruebas).

## 20 · Chat nuevo solo (arnés 1.23.0 a 1.26.2)
**Fecha:** 2026-11-08 · **Ref:** chat Modelo #62 a #63
Probado por Darwin en Modelo 2 el 2026-11-08: el chat #62 recibió el aviso de chat largo a ~203k tokens (umbral normal 200000), abrió solo el chat nuevo con start_session (18 s después), lo separó con detach_session (2 s después) y el chat #63 contó el traspaso en 5 viñetas llanas con una sola pregunta final (captura de Darwin). Comprobado en los registros de Modelo 2. Umbral devuelto a 200000.

## 21 · Nada suelto ni viejo: traspaso-out salgo con remoto (spec 022, 1.20.0)
**Fecha:** 2026-11-08 · **Ref:** archive/hechos.md
Probado por Darwin el 2026-11-08 con Modelo #61 en un proyecto con GitHub: traspaso-out salgo hizo commit solo de la memoria (439b298, 7 archivos de .brain, verificado en GitHub), lo subio y listo el codigo suelto (prueba_suelta.py y otros) sin meterlo. El aviso de «hay una versión nueva» de /actualizar le ayuda (Darwin). Hallazgo aparte: hitos.py no reconocia lecciones.py con PowerShell (arreglado en 1.28.7).

## 28 · Guardián con memoria del chat revisa el .venv (specs 027, 029 y 030, 1.28.5)
**Fecha:** 2026-11-08 · **Ref:** archive/hechos.md
Probado por Darwin el 2026-11-09 (confirmado tras las pruebas de Modelo #59 y #60 en F:/Modelo 2): con django==3.2 en el .venv el git push se detiene; con humanize==4.16.0 pasa callado. Arreglos: 1.28.4 (ve el .venv), 1.28.5 (olvida lo no instalado; 2>&1 no es una libreria). Sin comprobar: .venv en otra ruta; bloqueo con npm/cargo/go (punto 32). Commit vacio 9222812 en el GitHub de Modelo 2.

## 0 · Proyecto creado con el kit de arranque
**Fecha:** 2026-10-31
Estructura de Cerebro Vivo instalada con `instalar.py`.

## 1 · Repo subido a GitHub privado
**Fecha:** 2026-11-01
Subido a `forxa-ken/cerebro-vivo` (arnés 1.4.1, `e1b483b`) por orden de Darwin. Retirado de pendientes en cerebro-vivo #6.

## 9 · Índice central `.brain/INDICE.md` (DESCARTADO)
**Fecha:** 2026-11-01
Idea de Darwin (versión híbrida). Descartada por Darwin en cerebro-vivo #6: el ahorro de tokens nunca se demostró y añadía un archivo más que leer al arrancar. Los tres archivos de IA siguen como hasta ahora.

## 10 · Skills /resumen, /pendiente y /prompt-inicial separadas (spec 006)
**Fecha:** 2026-11-01
Arnés 1.4.2. Probado por Darwin en un chat nuevo.

## 2 · Retirar el repo viejo `cerebro-vivo-plugins` (decisión tomada)
**Fecha:** 2026-11-01
Darwin pidió retirar el punto de pendientes. El repo viejo NO se ha borrado ni tocado: borrarlo es irreversible y requiere su orden expresa sobre el repo.

## 6 · objetivo.md en el instalador (spec 007, arnés 1.5.0)
**Fecha:** 2026-11-01
Probado por Darwin en `F:\prueba` con Codex: existe `.brain/architecture/objetivo.md` y el chat nuevo lo leyó y dijo que el objetivo aún está por definir (correcto en un proyecto recién creado). La parte `.agents/skills/` (punto 7) sigue abierta.

## 12 · Migrar el objetivo a proyectos ya instalados (spec 008, arnés 1.6.0)
**Fecha:** 2026-11-01
Probado por Darwin: `--migrar-objetivo` creó el objetivo en un proyecto ya instalado (lo usó con Gemini). No se comprobó después la pregunta del objetivo en un chat nuevo de Codex.

## 7 · Skills para Codex en .agents/skills (spec 007, arnés 1.5.0)
**Fecha:** 2026-11-02
Probado por Darwin: con `AGENTS.md` en el proyecto, el actualizador copia las skills a `.agents/skills/` y Codex las usa.

## 11 · Panel /plantilla recuperado (spec 009, arnés 1.7.0)
**Fecha:** 2026-11-02
Probado por Darwin: el plugin `plantilla-prompt` se instala desde este repo y el panel `/plantilla` funciona.

## 3 · Primera adopción real en LoboHook
**Fecha:** 2026-11-07
Darwin confirma que `/actualizar` funciona en LoboHook. Su registro (chat #86) dice que ya estaba en 1.18.2, sin nada que traer, y que `CEREBRO_VIVO.md` figura modificado a mano y no se pisó. No hizo falta `--forzar-todo`. La skill vieja `traspaso-entre-chats` se eliminó de LoboHook el mismo día, con orden de Darwin.

## 18 · `/traspaso-in` abre el chat nuevo solo (arnés 1.12.0 y 1.18.2)
**Fecha:** 2026-11-07
Probado por Darwin en LoboHook. Su confirmación no detalla si miró en el sidebar el mismo nivel del chat nuevo ni si su resumen coincidía con lo hablado.

## 14 · Actualizador fiable (spec 021, arnés 1.19.0; con hooks desde 1.27.1)
**Fecha:** 2026-11-08
Darwin confirma «14 ok» tras probarlo en un proyecto real. Su confirmación no detalla en cuál, ni si lo retirado fue a `.brain/copias_arnes/`, ni qué decidió sobre `modo_auto.py`, `uso_tokens.py` y `test_modo_auto.py` de LoboHook. Además hay prueba automática de punta a punta (`tests/test_esperando_prueba.py`, 1.28.2).

## 26 · `/version` (spec 023, arnés 1.21.0)
**Fecha:** 2026-11-08
Darwin confirma «26 ok». Su confirmación no detalla si probó en Modelo 2 ni qué versión le dijo. Además hay prueba automática de los datos que lee y del aviso de versión nueva (`tests/test_arnes_esperando_prueba.py`, 1.28.3).

## 13 · `traspaso-in` y `traspaso-out` en Codex y Gemini (specs 010 y 011, arnés 1.9.0)
**Fecha:** 2026-11-08
Probado por Darwin en `F:\Modelo` (arnés 1.28.3) con capturas. Codex: `$traspaso-in salgo` escribió traspaso corto y completo; `$traspaso-in entro` en chat nuevo contó 5 viñetas y una pregunta; `$traspaso-out salgo` hizo commit local de solo `.brain/` (`b62ef7a`, 20 archivos), no subió por no haber remoto y avisó de 180 archivos sueltos. Gemini: `traspaso-out entro` contó 4 viñetas y una pregunta. Observaciones: el primer `entro` falló porque Darwin abrió el chat nuevo mientras `salgo` seguía escribiendo (5 min); hay que esperar el aviso de «Traspaso preparado». Sin la palabra, `$traspaso-in` se toma como `salgo`. La suite en el entorno restringido de Codex da errores de permisos y `git push`, no del arnés. La subida a GitHub de `salgo` no se probó (el proyecto no tiene remoto).

## 17 · Soporte para Mac (spec 013, arnés 1.11.0) — SIN PROBAR
**Fecha:** 2026-11-08
Decisión de Darwin: quien tenía que probarlo en un Mac no lo va a hacer, así que el punto sale de «Esperando tu prueba» pero **no cuenta como probado**. El código se queda (instalador con `python3`, `instalar_kit.command`, aviso de tkinter) y ya está marcado «sin probar en un Mac real» en la spec 013, `CEREBRO_VIVO` (es/en) y `GUIA_INSTALACION`. Solo lo cubren las pruebas automáticas en Windows. Si alguien lo prueba en un Mac: `python3 -m unittest discover tests`, doble clic en `instalar_kit.command` (si no abre, `chmod +x instalar_kit.command`) y abrir Claude Code en un proyecto de prueba. El ZIP de Mac sigue en pausa.

## 33 · El aviso de cierre no atribuye al chat lo que trajo `/actualizar` (spec 031, arnés 1.28.6)
**Fecha:** 2026-11-08
Probado por Darwin en LoboHook (de 1.25.0 a 1.28.7): tras `/actualizar` y tras reiniciar Claude Code, pidió al chat solo añadir una línea de prueba a `.brain/pendientes.md`. Al terminar, el cierre no mostró ningún aviso (Darwin: «no salió nada») y el registro pegado no contiene cuadro de «Stop hook feedback» en ese tramo. Los archivos repartidos por `/actualizar` no se atribuyeron al chat. Aparte: esa prueba destapó un fallo del actualizador con el venv entre comillas (arreglado en 1.28.8).


## 4 · Repetir el banco T1-T3 (specs 003 y 004) con la 1.29.0 — DESCARTADO
**Fecha:** 2026-11-09
Darwin decidió no repetirlo (30 chats de prueba, coste en dinero). Motivo: el informe 032 ya midió el coste con datos reales (16-28 % ritual del arnés) y el efecto de la 1.29.0 se mide gratis con `python .brain/guardianes/medir.py --ritual` (punto 35, en 2 semanas). Los guardianes nuevos pasan a decidirse según ese resultado.

## 19 · Fábrica de IA y varias IA con papeles (specs 035, 042 y 043) — programación TERMINADA
**Fecha:** 2026-11-12
Todo lo programado: fábrica y directora (1.32.0 a 1.34.0), medidor de gasto (`medir.py --fabrica`, 1.40.0), modo colaborativo y Gemini como obrera (spec 042, 1.42.0) y proyectos hermanos (spec 043, 1.43.0). No queda nada por programar en este punto; lo que espera la prueba de Darwin está en los puntos 31 (coste por tarea terminada), 42 y 43. Texto que tenía en pendientes:

- **19:** [spec 035 APROBADA el 2026-11-10; Fases 1, 2 y 3 HECHAS el 2026-11-10 (plantillas en `biblioteca/PLANTILLAS_FABRICA` y `CARTA_EJECUTORA`, guardián `fabrica.py`, arnés 1.32.0, sin subir); skills y regla R9 en arnés 1.33.0; prueba mínima R13 HECHA el 2026-11-10 (informe en `archive/informe-r13-traductorvoz-2026-11-10.md`) y prueba de Codex con ventana llena cerrada (hechos 19-B; el tope de 200k es riesgo aceptado: lo cubre el diseño de encargos pequeños, no una medición en vivo); medidor de gasto de Codex HECHO el 2026-11-10 (arnés 1.34.0, `medir.py --fabrica`); coste de la directora en `medir.py --fabrica` HECHO el 2026-11-12 (arnés 1.40.0); el coste por tarea terminada sigue en el punto 31; la parte de varias IA con papeles quedó programada en la spec 042 (arnés 1.42.0, punto 42); la spec 043 (proyectos hermanos) quedó programada el 2026-11-12 (arnés 1.43.0, punto 43)] diseño original: cómo colaboran varias IA con responsabilidades distintas en un proyecto (caso Guild Control Forever: Claude con `.brain/`, Gemini solo traducciones con `AGENTS.md`). Decidido en la 042: qué lee/escribe cada IA, cómo no pisarse, `indices_ajenos` en `guardianes.json`. Detalle en `archive/pendientes-detalle-2026-11-08.md`.
  - **Prueba de ventana llena de Codex: CERRADA el 2026-11-10 por decisión de Darwin** (detalle en `archive/hechos.md`, punto 19-B). Relevo probado; aviso automático en vivo NO probado (riesgo conocido y barato: tope 200k por tanda, encargos pequeños, guardián al terminar cada tanda; vigilante en vivo solo si algún día un desbordamiento duele).

## 19-B · Prueba de Codex con ventana llena y relevo (spec 035, fábrica) — CERRADA con matiz
**Fecha:** 2026-11-10
Prueba hecha en TraductorVoz (encargo 007, pruebas de 9 módulos). Codex paró solo en el punto de control (113.176 tokens), dejó su traspaso en `.brain/notas-chats/`, y un Codex nuevo, lanzado por la directora solo con ese traspaso, terminó los módulos 5-9 sin repetir nada (74.609 tokens); un tercero pequeño arregló una prueba (40.720). Total 228.505 sobre tope 150.000, pasado con permiso de Darwin; 70 pruebas verdes, mezclado en `tres-capas` (solo local), sin revisión independiente. **Lo probado:** parada ordenada, traspaso escrito y relevo lanzado por la directora. **Lo NO probado:** el aviso automático al llenarse de verdad la ventana de 200.000 (nadie la llenó) y un corte en vivo. Darwin decidió no construir un vigilante en vivo por ahora (el guardián `fabrica.py` solo mira el gasto al terminar cada tanda; el sobrecoste fue de ~38.000 tokens). Pruebas anteriores de traspaso en Codex: punto 13 (los chats nuevos los abrió Darwin a mano; Codex no corre ganchos). Detalle: `F:\Proyectos\TraductorVoz-notas
esultado-prueba-B.md` y `archive/diario-fabrica-r13.md`.

**Decisión final de Darwin (2026-11-10, chat #43):** el tope de 200.000 queda como **riesgo aceptado, protegido por el diseño del encargo y no por medición en vivo**. Codex no tiene contador de tokens ni ganchos (lo confirmó él mismo: decide a ojo), así que ninguna carta puede hacer que pare al llegar al tope. Lo que lo cubre: encargos pequeños, un punto de control dentro del encargo, y el guardián `fabrica.py` que cuenta el gasto al terminar cada tanda; el peor caso visto fue pasarse ~38.000 tokens. El cambio de chat lo hace la directora, no Codex. Un vigilante en vivo solo se construye si algún día un desbordamiento cuesta caro.

## 41 · `/fabrica` y Codex por `codex exec` (spec 040, arnés 1.37.0 a 1.37.4) — PROBADO
**Fecha:** 2026-11-11 (chat #47)
Darwin lo probó en GuildControlForever y TraductorVoz con el arnés 1.37.4: el modo fábrica se recuerda entre chats y arranca la directora; la directora lanza Codex con `codex exec` sin pedir permiso en cada encargo y solo para al segundo fallo seguido o si salta un tope. Spec 040; arnés 1.37.0 a 1.37.4.

## 40 · Resumen en llano de los trabajos citados en «Fuentes» — CERRADO sin escribirlo
**Fecha:** 2026-11-12 (chat #47)
Darwin ordenó cerrar el punto. No se escribió el resumen (un autor externo, Stanford, Meta-Harness, Databricks, ADR, GitHub Spec Kit, fábrica de software). Los enlaces siguen en la sección «Fuentes» del README para quien quiera leerlos. Texto original del punto: resumen en llano, para que Darwin los lea, de los trabajos citados en «Fuentes» (README): un autor externo (un proyecto externo), Stanford (Meta-Harness), Databricks (Omnigent), ADR (Nygard, Fowler, Microsoft, Red Hat, AWS), GitHub Spec Kit (constitution.md, spec-driven.md, blog de Delimarsky) y fábrica de software (Cusumano 1991, Greenfield y Short 2004). Qué dice cada uno, qué tomamos y qué es propio. Sin empezar; no es código.

## 25 · Distancia con un proyecto externo (un autor externo) — CERRADO
**Fecha:** 2026-11-12 (chat #47)
Cerrado por orden de Darwin. Hecho en el arnés 1.34.1 a 1.35.3; Darwin decidió no renombrar nada. Detalle original: distancia con un proyecto externo. HECHO el 2026-11-10 (arnés 1.34.1, 1.34.2 y 1.35.0): un autor externo, Stanford (Meta-Harness) y Databricks (Omnigent) como «Fuentes» en README, manual y página; «Fast-Track» pasó a «Cambio pequeño» / «Small change». Investigado en Internet: constitución, decisión y registro de decisiones son términos estándar del sector (Spec Kit, ADR), no de un autor externo; pendiente no existe en un proyecto externo; meta-arnés es ya un término público. Fuentes ampliadas (1.35.2) con ADR (Nygard, Fowler, Microsoft, Red Hat, AWS) y Spec Kit, para cubrir decisión y constitución sin renombrar. Cerrado el 2026-11-11 (1.35.3): Darwin decide no renombrar nada (meta-arnés, pendiente, constitución y decisión se quedan) y la bibliografía de constitución (GitHub Spec Kit, spec-driven.md, blog de Delimarsky) queda publicada; la lista de autores está completa y, si aparece otro, Darwin lo dirá.

## 50 · Diagramas en `/diapositivas` (spec 046 fase 1, arnés 1.46.0 y 1.46.1) — PROBADO

26-11-13 (arnés 1.46.0 y 1.46.1, spec 046 fase 1): diagramas Mermaid (`flowchart` y `sequenceDiagram`) dibujados como SVG dentro de `/diapositivas`, sin internet. Darwin los probó con el ejemplo y confirma: «bien, un poco básicos pero de momento sirven». Comprobado además por la IA en capturas (claro y 600 px); **sin probar en oscuro ni en Mac**. Los otros tipos (clases, estados, tarta, ER, Gantt: fases 2 a 5) y el vídeo (spec 047) siguen aparcados hasta que Darwin los pida.

## 49 · `/diapositivas`: presentaciones para humanos (spec 045, arnés 1.45.0 a 1.46.2) — PROBADO

26-11-13 (arnés 1.45.0 a 1.46.2): Darwin la probó con un resumen del proyecto y con la carta del meta-arnés en modo documento (el script preguntó cuál de las dos cartas; salieron 26 secciones en 29 diapositivas, en 2 partes) y confirma. En la prueba se corrigieron un índice renumerado y se añadieron las subviñetas (1.46.2). Comprobado también por la IA en capturas de Edge; **sin probar `Ctrl+P` a PDF por la IA, ni en oscuro, ni en Mac**. Que el resumen sea fiel al original lo juzga Darwin.

## 29 · Memoria desactualizada: `revisar_indices.py` avisa de rutas rotas (spec 037, arnés 1.36.0) — PROBADO

26-11-13: Darwin lanzó `python .brain/guardianes/revisar_indices.py` y confirma. Salida: «Sin hallazgos» (CLAUDE.md al 75 % de su tope, 5 avisos descartados, última revisión 2026-11-13). **Límite:** no se vio ningún aviso real, así que la detección de rutas rotas solo está comprobada por las pruebas automáticas (el aviso de `colaboracion.md` era un falso positivo y se descartó).

## 43 · Proyectos hermanos (spec 043, arnés 1.43.0) — PROBADO

26-11-13: Retail configurado para mirar a Forever (`proyectos_hermanos` en su `guardianes.json` y `.brain/portar-forever.md` con «Último portado» `51514c8`). El guardián y el aviso del arranque dan 35 commits de Forever sin portar, reales. Darwin confirma («43 probado»). **Límite:** esos 35 aún no se han repasado (algunos, como el del arnés, serán «no aplica»); la dirección habitual es Forever → Retail.
