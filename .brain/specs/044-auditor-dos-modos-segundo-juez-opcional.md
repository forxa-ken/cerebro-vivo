# Spec 044: auditor (dos modos, ejecutor externo Codex; genérico, va en el arnés)

- **Estado:** APROBADA por Darwin el 2026-11-12 y programada en el arnés 1.44.0 (23 pruebas en verde); falta probarla en un trabajo real con la IA (punto 23). Sin subir a GitHub.
- **Fecha:** 2026-11-12
- **Origen:** Darwin quiere aprender a montar una IA que verifique las pruebas y los errores de la IA principal, exigente en **calidad, consumo de recursos y seguridad**. Hoy el arnés tiene `revisor-independiente` (calidad) y `revisor-de-consumo`, pero solo los usa la fábrica, y la seguridad vive aparte (`seguridad-en-sistemas-reales`).
- **Genérica:** no nombra proyectos concretos (lo vigila `tests/test_arnes_repo.py`).

## 0. Nombre y diferencia con el revisor de la fábrica
- **Se llama «auditor»** (skill `auditor`, comando `/auditor`, ajustes `auditor_*`) para no confundirlo con el **revisor** que ya existe en la fábrica (`revisor-independiente`, `revisor-de-consumo`).
- **Revisor (fábrica):** comprueba que **lo que entregó una obrera** (Codex o Gemini) responde a **su encargo y al requisito de la spec**. Está atado a un encargo y solo existe dentro de la fábrica.
- **Auditor (esta spec):** funciona en **cualquier proyecto**, sin encargo ni fábrica; en la fábrica entra solo en el **cierre de la spec**, no en cada encargo. Audita **todo** (código, cambios de una tarea, y también lo que hace la directora: specs, asignaciones, integraciones) **buscando fallos e intentando romperlo**, en calidad, consumo y seguridad. No sustituye al revisor: la fábrica sigue usando el suyo.

## 1. Objetivo
Un auditor que se pueda llamar en cualquier proyecto, sin fábrica, que junte las tres miradas y que Darwin pueda elegir **quién lo ejecuta**. Solo avisa: nunca cambia código ni bloquea el cierre.

## 2. Decisiones de Darwin (2026-11-12) — donde choquen con la sección 2b, **manda la 2b** (es posterior)
- **Dos modos:** (1) **revisión general**: busca huecos de calidad, consumo y seguridad en el código o carpeta que se indique; (2) **revisión de cierre**: mira lo que cambió en una tarea.
- **Un juez por defecto y un segundo juez opcional:** (A) **subagente interno** con instrucciones adversas (intenta romper el trabajo), siempre disponible; (B) **IA externa** de otra familia (Codex) como **segundo juez, opcional y apagado por defecto**: Darwin lo activa y lo apaga cuando quiera.
- **Solo avisa.** El informe lo decide Darwin; no bloquea el cierre.
- **Auditor de cierre ACTIVADO por defecto**, con interruptor; se ejecuta **solo si el cierre incluye cambios de código o configuración** (no si solo se tocó memoria, documentos o el registro), para no gastar en cierres de papeleo.
- **IA externa:** al principio se pensó apagada por defecto; tras la prueba, Darwin aceptó que Codex sea principal en revisión general y cierre de spec (sección 2b).
- **Comando `/auditor`:** `general` (revisa el proyecto o la carpeta indicada), `cierre` (revisa lo cambiado en la tarea actual), `cierre si|no|estado` (interruptor del auditor de cierre) y `externo general-y-spec|siempre|no|estado`.
- **Modelo y esfuerzo (decididos por Darwin, 2026-11-12):** la **directora siempre es Opus 5.5 en medio**; su **auditor interno es Sonnet 5.5 en medio** (siempre un modelo distinto del que escribió). El **segundo juez externo (Codex)** usa el modelo «Sol 6.0» en medio que Darwin indicó: nombre `gpt-6-sol` **verificado** (se ejecutó con él en las rondas 1 y 2 y en la revisión general); va en el ajuste `auditor_modelo_externo`. Para el código que hacen Codex o Gemini **no** audita el auditor por encargo: lo revisa el revisor de la fábrica; el auditor entra en el **cierre de la spec**, donde audita lo que la directora decidió y juzgó (la spec, los encargos, su veredicto sobre los informes del revisor y la integración final). Ajustes `auditor_modelo`, `auditor_modelo_externo` y `auditor_esfuerzo` para cambiarlos a mano. Sonnet auditando a un Opus es un modelo **menos potente que el autor**: es decisión de Darwin y la prueba de fallos plantados dirá si basta.

## 2b. Reparto de ejecutores (recomendado y aceptado por Darwin, 2026-11-12, tras las rondas 1 y 2)
Evidencia: `archive/informe-prueba-auditor-2026-11-12.md` y `archive/prueba-auditor-ronda2/INFORME.md`. Sonnet 5.5, Opus 5.5 y Codex hallaron 11/11 en la ronda 1; en la ronda 2 (fallos sutiles) Sonnet y Opus 11/11 y Codex 9/11 sin ejecutar y 10/11 ejecutando (7 reproducidos, el único que reprodujo la carrera de folios), con ~8k tokens frente a ~70k. Cada uno falló en algo distinto: juntos cubren todo. Son dos pruebas con código de juguete: **no miden el sesgo de familia** ni dicen qué modelo es mejor en general.
- **Cierre rutinario** (hubo cambios de código o configuración, pero no es cierre de spec): **Sonnet 5.5 medio solo** (interno, rápido, sin salir a una herramienta externa).
- **Revisión general y cierre de spec de la fábrica:** **Codex principal + Sonnet 5.5 medio**, y el informe marca en qué coinciden y en qué discrepan. Opus **no** se usa de auditor: empató con Sonnet, tardó unas seis veces más y la directora ya es Opus (auditaría a su misma familia).
- **Ajuste `auditor_externo`** (en `guardianes.json`; sustituye al antiguo `auditor_externo`): `"general-y-spec"` (por defecto: Codex entra en revisión general y cierre de spec), `"siempre"` (también en cierres rutinarios) o `"no"` (no se llama a ninguna IA externa ni se gasta con ella). `/auditor externo general-y-spec|siempre|no|estado`. **Esto es una propuesta de implementación de la IA; Darwin la confirma al aprobar la spec.**
- **Si Codex no está instalado o falla:** se dice claro en el informe y sigue el interno solo; nunca se oculta.
- **Codex en Windows:** siempre con `-c 'windows.sandbox="unelevated"'` y `-s read-only` (ver el final de la spec).
- Cambiar modelos a mano: `auditor_modelo`, `auditor_modelo_externo`, `auditor_esfuerzo`.

## 3. En alcance
- [ ] Skill `auditor` (es/en): un procedimiento con los dos modos y los dos ejecutores, que **reutiliza** `revisor-independiente`, `revisor-de-consumo` y `seguridad-en-sistemas-reales` en vez de copiarlos.
- [ ] **Ejecutor A (interno):** subagente de solo lectura, sin ver el razonamiento de quien escribió. Instrucción adversa («demuestra que falla»). **Ejecuta** las pruebas y los guardianes; no se limita a leer. Idealmente con un modelo distinto del que escribió.
- [ ] **Ejecutor externo (Codex):** ajuste `auditor_externo` descrito en la sección 2b, gestionado por `auditor.py` (mismo patrón que `/colabora`; el arranque lo recuerda entre chats como línea informativa). Llamada: `codex exec -m <auditor_modelo_externo> -c model_reasoning_effort=medium -c 'windows.sandbox="unelevated"' -s read-only`, con la misma tarea y formato de informe que el interno. En `"no"` no se lanza ninguna IA externa. Gemini queda fuera hasta que Darwin pruebe el punto 42.
- [ ] **Interruptor del cierre:** ajuste `auditor_cierre` en `guardianes.json`, **verdadero por defecto**. `cierre.py` **solo avisa** a la IA («lanza el auditor de cierre») cuando hubo cambios de código o configuración y el ajuste está encendido; no puede lanzar el subagente por sí mismo, lo lanza la IA. **No probado** que la IA obedezca el aviso (como los demás guardianes).
- [ ] **Formato único de informe** (plantilla `PLANTILLA_INFORME_REVISION.md`, es/en): veredicto, hallazgos por gravedad con archivo y línea, lo «no comprobado», en tres bloques (calidad, consumo, seguridad).
- [x] **Qué cuenta como «sensible»** (1.44.1: lo lee `auditor.py`; `quien cierre ARCHIVO…` responde `externo?` y `cierre.py` añade el aviso de sugerir el externo) para sugerir `auditor_externo="siempre"` en el modo de cierre: lista en `guardianes.json` (`revision_sensibles`), con valores neutros por defecto.
- [x] **Prueba de fallos plantados:** hecha en dos rondas (2026-11-12); resultados en la sección 2b. Queda como regla: repetirla si se cambia de modelo o se sospecha que el auditor falla en algo real.

### Decisiones de la 1.44.1 (tras la auditoría del auditor sobre sí mismo)
- El aviso de cierre **no mira `.brain/*` ni `.claude/*`** (están en `ignorar_cambios`): es intencionado en un proyecto cliente, donde son la memoria y el arnés, no su código. En este repo (el arnés) eso deja sordo el aviso para guardianes y skills: allí se lanza `/auditor` a mano.
- El aviso mira los cambios aunque el cierre por bloques siga abierto (<15 ediciones), pero no avisa si esa respuesta no editó nada. Puede repetirse en respuestas seguidas con ediciones; **no probado** cuánto molesta.
- `auditor_cierre` es verdadero por defecto en todos los sitios (`auditor.cierre_activo`); acepta «false»/«no»/«0».
- `guardianes.json` ilegible (JSON roto, raíz que no es objeto): `/auditor cierre|externo` **no escribe** y lo dice; con BOM se lee bien.
- `auditor_modelo_externo` y `auditor_esfuerzo` solo admiten letras, cifras y `. _ : / -` (entran en una línea de comandos); si no, vale el por defecto.
- README/LICENSE/CHANGELOG sin extensión no cuentan como código.

## 4. Fuera de alcance
- Bloquear el cierre o corregir código automáticamente.
- Revisar cierres que solo tocan memoria, documentos o el registro.
- Gemini como auditor.
- Tocar la fábrica: sigue usando sus skills como hasta ahora.

## 5. Riesgos
- **Sesgo de la misma familia:** un Claude revisando a otro Claude comparte puntos ciegos. Se reduce con pruebas reales, instrucción adversa y modelo distinto; solo la IA externa da ojos de otra familia. No está medido hasta hacer la prueba de fallos plantados.
- **Coste:** cada revisión gasta tokens y la IA externa los suma; por eso en cierres rutinarios entra solo si se pide (`siempre`).
- **Coste (medición):** cada revisión gasta tokens; la spec debe medirlo (`medir.py`) antes de recomendar un uso habitual.
- **Falsos avisos:** por eso solo avisa y exige archivo y línea en cada hallazgo.

## 6. Archivos
Skill `auditor` (es/en), `PLANTILLA_INFORME_REVISION` (es/en), `auditor.py` (nuevo, solo el ajuste del ejecutor externo), `guardianes.json` (`auditor_cierre`, `auditor_externo`, `auditor_modelo`, `revision_sensibles`), `cierre.py`, `arranque.py`, `textos.py`, `generar_manifiesto.py` (**añadir las plantillas nuevas a INCLUIR**, lección 1.42.0), `tests/`, `VERSION`, `CAMBIOS.md`, `manifiesto.json`.

## 7. Verificación
`python -m unittest discover tests` en verde; la prueba de fallos plantados con el interno solo y con el ejecutor externo encendido; comprobar que con `auditor_externo="no"` no llama a ninguna IA externa. comprobar que `cierre.py` avisa solo con cambios de código y con el ajuste encendido. **No probado hasta hacerla.**

- **Codex y `python` en Windows (comprobado 2026-11-12):** el sandbox por defecto de Codex en esta máquina (`[windows] sandbox = "elevated"` en `~/.codex/config.toml`) corre con otro usuario que no puede leer la carpeta de Python del perfil de Darwin y da «Acceso denegado». Arreglo sin tocar permisos del sistema: lanzar con `codex exec -c 'windows.sandbox="unelevated"' -s read-only ...`; así `python` funciona y sigue sin poder escribir (probado: `PermissionError`). `auditor.py` debe pasar ese ajuste al llamar a Codex en Windows.
