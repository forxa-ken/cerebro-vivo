# Spec 050: modo automático de la fábrica (línea de producción con prueba de uso real)

- **Estado:** borrador, **esperando la aprobación de Darwin** (no se programa nada hasta entonces).
- **Fecha:** 2026-11-14
- **Cierra:** pendiente 54.
- **Origen:** Darwin quiere usar la fábrica como una línea de producción: él entrega órdenes, la línea trabaja sola, el producto se prueba de verdad («programado no es terminado») y, si el resultado es el esperado, se sube. Quiere dos modos de la fábrica: **normal** y **automático**.
- **Se apoya en:** spec 035 (fábrica con directora, revisor y tres puertas), spec 040 (`/fabrica si|no|estado`), skills `directora-de-fabrica`, `revisor-independiente` e `implementada-no-es-hecha`, y el experimento VMware (las reglas explícitas deciden más que el método).

## 1. Objetivo
Añadir a la fábrica un segundo modo, **automático**, donde la directora y las ejecutoras recorren una orden completa **sin pedir permiso en los pasos intermedios**, y entregan a Darwin un resultado **ya probado de uso real**, con un informe corto. Darwin decide una sola vez al final: aceptar (y entonces se sube con su orden) o descartar.

**Problema real que evita:** hoy cada decisión pequeña se pregunta (Darwin acaba diciendo «sí» sin leer) y, peor, una tarea se da por terminada solo porque pasó las pruebas del código. El método ya dice «implementada no es hecha», pero nadie lo comprueba solo.

## 2. Cómo funciona (visión en llano)
1. **Orden:** Darwin entrega una orden corta, el **modelo de negocio** (lo que se quiere) y su **criterio de «esperado»** (cómo se sabe que salió bien). Sin criterio, la directora lo propone y Darwin lo aprueba antes de empezar; en modo automático no se arranca sin él.
2. **Spec revisada:** la directora diseña la spec y un **revisor de spec** (otra IA, crítica y severa) comprueba que cumple el modelo de negocio, sin inventar ni omitir; hasta 3 vueltas, y si no se resuelve se pregunta a Darwin.
3. **Línea:** la directora escribe los encargos; las ejecutoras programan; todo en una **rama aparte** (nunca en `main`).
4. **Control de calidad automático:** pruebas del proyecto, guardianes (secretos, manifiesto, paridad es/en) y la **prueba de uso real** (sección 4).
5. **Informe de entrega:** una página llana con lo pedido, lo hecho, lo extra, qué se probó de verdad, qué **no** se pudo probar, y las decisiones que tomó la línea por su cuenta.
6. **Darwin decide:** acepta o descarta la rama. Subir a GitHub sigue siendo solo con su orden.

## 3. Reparto de decisiones (las tres listas)
- **La línea decide sola (y lo anota):** nombres, orden de los pasos, organización de archivos dentro del encargo, cómo repartir el trabajo entre ejecutoras, reintentos tras un fallo de prueba, y la **opción más conservadora** ante un hueco pequeño de la spec (la que toca menos y se deshace con facilidad).
- **Sigue pidiendo el sí de Darwin (la línea se para y lo pregunta, o lo deja anotado como pregunta abierta y termina el resto):** subir a GitHub o a la página pública; borrar datos o historial; gastar dinero o pasar el tope de la carta; tocar secretos, claves o configuración personal; cambiar quién puede acceder a algo; añadir o quitar **requisitos** de la spec; instalar programas; tocar proyectos ajenos al encargo.
- **Nunca hace (ni con el modo automático ni pidiéndolo la IA):** forzar un `push`, reescribir historial publicado, saltarse un guardián o una prueba, borrar evidencia, actuar sobre servidores o datos reales sin las reglas de la skill `seguridad-en-sistemas-reales`.
- **Huecos grandes de la spec** (los que cambian lo que el usuario puede hacer): se mantiene la regla de la spec 035: se registran y se preguntan; la línea no los asume. En modo automático se **para ese encargo**, sigue con los que no dependen de él y lo deja en el informe.

## 4. Prueba de uso real (el corazón de la spec)
La prueba de uso real **la hace una IA distinta de la que construyó** (el revisor independiente), con instrucciones propias, y deja **evidencia guardada** (comandos, salidas, capturas). El tipo de prueba depende del producto:
- **Herramientas de línea de comandos y guardianes:** ejecutarlas de verdad con casos buenos y casos malos, comparar la salida con el criterio de «esperado» y comprobar que lo malo se **rechaza**.
- **Documentos, skills y páginas generadas:** generarlos y abrirlos (la página, en el navegador integrado); comprobar que cargan, que no hay peticiones externas ni errores de consola y que el recorrido pedido funciona.
- **Aplicaciones con pantalla:** abrir la aplicación y hacer el recorrido de un usuario, con el control del navegador o del ordenador cuando exista.
- **Lo que una IA no puede juzgar** (si «se ve bien», si «se entiende»): se marca **«no probado»** y pasa a la lista «Esperando tu prueba (Darwin)». Nunca se declara hecho.
- **Contra la prueba trampa:** el revisor recibe el criterio de «esperado» escrito **antes** de construir, y la evidencia debe mostrar que se probó lo pedido y no algo más fácil. Una prueba sin evidencia cuenta como no hecha.

## 5. Frenos
- **Carta de la fábrica** (spec 035, R2): topes de gasto, de número de encargos y de tiempo; los escribe Darwin y la directora no puede editarlos.
- **Intentos:** como máximo 3 reintentos por encargo; al tercer fallo se para ese encargo y se informa.
- **Atasco:** si pasa un tiempo sin avance (por defecto 30 minutos), la línea para y deja un informe corto de dónde quedó.
- **Rama aparte:** nada llega a `main` sin la aceptación de Darwin. Descartar = borrar la rama; no deja rastro en `main`.
- **Interruptor:** `/fabrica modo normal` (o `no`) apaga el modo automático al instante.

## 6. En alcance (por fases; cada una se aprueba y se prueba aparte)
**Fase 1 — el modo y el interruptor.**
- [ ] Ajuste `fabrica_automatica` (true/false, por defecto false) en `.brain/guardianes/guardianes.json`, solo válido con `modo_fabrica` encendido.
- [ ] `python .brain/guardianes/fabrica.py automatico si|no|estado`, con textos es/en en `textos.py`; `estado` dice qué falta (carta sellada, criterio de «esperado», rama de trabajo).
- [ ] El arranque lo avisa solo cuando está activado: «Modo fábrica AUTOMÁTICO».
- [ ] Skill `/fabrica` ampliada (es y `.en.md`) con la palabra `automatico`.

**Fase 2 — revisor de spec (primera puerta de la línea).**
- [ ] **Modelo de negocio congelado:** archivo corto escrito por Darwin con el modelo de negocio y lo que se quiere; la IA no lo edita (guardián, con huella como la carta de la spec 035).
- [ ] **Skill `revisor-de-spec`** (es y `.en.md`): una IA **distinta** de la que diseñó la spec (otro modelo, o al menos otro chat con instrucciones propias) y **crítica y severa**. Solo recibe el modelo de negocio y la spec, no la conversación de quien la escribió.
- [ ] **Veredicto estructurado:** APROBADA o RECHAZADA, con (a) partes del modelo de negocio que la spec no cubre, (b) requisitos que la spec **inventa** sin respaldo en el negocio, (c) huecos y ambigüedades, (d) contradicciones con decisiones o specs anteriores. **Todo rechazo cita** la frase del modelo de negocio (o de la spec) que lo motiva; un rechazo sin cita no cuenta.
- [ ] **Vueltas:** si rechaza, quien diseñó corrige y vuelve a enviar; máximo 3 vueltas. Si sigue rechazada, la línea se para y pregunta a Darwin. Los **huecos grandes** siguen subiendo a Darwin aunque el revisor apruebe.
- [ ] **Se prueba antes de confiarle nada:** con las specs reales del repo (buenas) y con copias dañadas a propósito (un requisito inventado, una parte del negocio omitida, una contradicción), comprobando que aprueba las buenas y rechaza las dañadas. Se repite cada caso más de una vez, porque un aprobador no es determinista (lección del experimento VMware).
- [ ] Pasarle siempre todos los datos que sus reglas necesitan (lección del experimento: una regla que depende de un dato que el juez no tiene siempre falla) y reglas escritas una sola vez, sin ambigüedad.

**Fase 3 — criterio de «esperado» y rama de trabajo.**
- [ ] Plantilla de orden con el criterio de «esperado» obligatorio (en `PLANTILLAS_FABRICA`, es y en).
- [ ] Un guardián que **bloquea** arrancar un encargo en modo automático si falta el criterio o si se está en `main`.

**Fase 4 — prueba de uso real.**
- [ ] Skill `prueba-de-uso-real` (es y `.en.md`): cómo probar cada tipo de producto, dónde queda la evidencia y qué se marca «no probado».
- [ ] Guardián que exige la evidencia guardada antes de dar un encargo por entregado.

**Fase 5 — informe de entrega y frenos.**
- [ ] Plantilla de informe de entrega (lo pedido / hecho / extra / probado / no probado / decisiones por su cuenta).
- [ ] Contador de reintentos y aviso de atasco.

**Fase 6 — experimento acotado.**
- [ ] Una orden real y pequeña, en un proyecto de prueba y en rama aparte, para ver qué pasa. Se mide: si el resultado era el esperado, qué decisiones tomó sola, cuántas veces hubo que parar, qué no pudo probar, y qué reglas faltaron.

## 7. Fuera de alcance
- Que el modo automático sea el modo por defecto, o que se active solo.
- Subir a GitHub o a la página pública sin orden de Darwin; forzar `push`; tocar `main` directamente.
- Cambiar las puertas humanas de la spec 035 en el modo normal.
- Probar contra servidores, dinero o datos reales.
- Sustituir al revisor independiente por la misma IA que construye.
- Tocar proyectos ajenos (LoboHook, Guild Control Forever u otros).

## 8. Riesgos
- **La IA se aprueba a sí misma o prueba algo más fácil.** Mitigación: revisor distinto, criterio escrito antes, evidencia obligatoria; es el riesgo principal y el experimento (fase 6) debe buscarlo a propósito.
- **«Frankenstein»:** rellenar huecos con suposiciones y añadir lo no pedido. Mitigación: huecos grandes se paran; lo extra va al informe y se revierte salvo aceptación.
- **Errores en cadena:** una decisión mala pequeña se vuelve base de la siguiente. Mitigación: reintentos limitados, rama aparte, informe con todas las decisiones propias.
- **Falsa tranquilidad:** un informe verde que no prueba lo importante. Mitigación: la sección «no probado» es obligatoria y nunca se deja vacía sin explicarlo.
- **El revisor de spec no es determinista ni infalible** (mismo texto, veredictos contrarios, o severo por deporte). Mitigación: citas obligatorias, pruebas repetidas con specs buenas y dañadas antes de confiarle nada, y que el modelo de negocio siga siendo de Darwin.
- **Coste:** muchas sesiones sin supervisión. Mitigación: topes de la carta y de tiempo.
- **Lo que una IA no puede probar** (aspecto, comprensión): sigue siendo de Darwin.

## 9. Verificación
- `python -m unittest discover tests` en verde en cada fase (con pruebas del interruptor, de los guardianes que bloquean y de la paridad es/en).
- Experimento de la fase 6 con informe archivado. **Sin probar por Darwin hasta que lo haga.**

## 10. Preguntas abiertas para Darwin (se deciden antes de la fase 1)
1. ¿Los topes por defecto (3 reintentos, 30 minutos sin avance) te parecen bien, o prefieres otros?
2. ¿Quién hace la prueba de uso real: siempre una IA distinta (más segura y más cara) o, para tareas pequeñas, la misma ejecutora con evidencia?
3. ¿Qué proyecto de prueba usamos para la fase 6 (uno desechable, no un proyecto real)?
4. ¿El revisor de spec debe ser siempre **otro modelo** (por ejemplo Codex), o basta con otro chat de Claude con instrucciones distintas?

## 11. Cierre
- [ ] Spec aprobada por Darwin antes de programar
- [ ] Versión nueva, `CAMBIOS.md`, manifiesto y manual (es y en) en cada fase; página pública revisada (no se sube sin orden)
- [ ] Línea añadida a `.brain/decisions.log` al cerrar cada fase
