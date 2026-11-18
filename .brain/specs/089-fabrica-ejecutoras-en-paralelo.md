# Spec 089: ejecutoras en paralelo en la fábrica (Codex y DeepSeek a la vez)

- **Estado:** **borrador, pendiente de que Darwin la apruebe.** Nada de esto está programado ni probado.
- **Fecha:** 2026-11-18
- **Se apoya en:** spec 035 (fábrica con directora, revisor y tres puertas), spec 050 (modo automático, topes y frenos), spec 088 (camino corto), skill `directora-de-fabrica` (ejecutoras Claude, Codex y DeepSeek).
- **Origen:** Darwin pidió (2026-11-18) que la fábrica pueda poner varias ejecutoras a trabajar a la vez, por ejemplo Codex y DeepSeek con encargos distintos, para acortar el tiempo de una misión con varios encargos.

## 1. Objetivo
Que la directora lance **dos encargos independientes al mismo tiempo**, cada uno con su ejecutora, y los cierre **uno por uno** con las mismas defensas de siempre. Se busca ahorrar tiempo de reloj, no gasto: el gasto total es el mismo o algo mayor.

## 2. Qué ya está listo y qué falta
**Ya está listo (leído en `fabrica.py`):** la foto, el alcance, el gasto, los fallos y los frenos de atasco se guardan **por encargo** (`estado/N.foto.json`, `gasto.json` con campo `encargo`, `frenos.json` por encargo). Cada ejecutora ya trabaja en su propio worktree y rama; la foto se hace sobre esa carpeta.

**Falta:**
- Nada comprueba que dos encargos **no se pisen** en archivos.
- La skill dice «un encargo y luego el siguiente»: no describe el paralelo, ni cómo se fusiona.
- Los topes de misión se suman de todos los encargos, pero no hay un tope de **cuántos a la vez**.
- Los avisos de la directora (qué espera, desde cuándo) están pensados para un solo trabajo en marcha.

## 3. Reglas del paralelo
1. **Máximo 2 a la vez.** Más multiplica el gasto, los fallos y la carga de revisión de la directora. Subirlo exige otra decisión de Darwin.
2. **Archivos sin solapes.** Los «Archivos permitidos» de los dos encargos no pueden coincidir en ningún archivo ni carpeta (ni una carpeta contener al archivo del otro). Si coinciden, se lanzan **en serie**.
3. **Independientes de verdad.** Ningún encargo necesita el resultado del otro ni cambia lo que el otro lee (una función, un texto de interfaz, un contrato entre módulos). Ante la duda, en serie.
4. **Cada una en su worktree y rama.** Nunca dos escritoras en la misma carpeta (regla que ya existe).
5. **Se fusionan de una en una.** Primero la que termine antes: alcance, pruebas de la directora, lectura del diff y revisión aparte (si toca). Se fusiona y **se vuelve a correr la prueba completa**. Solo entonces se cierra la segunda y se prueba **sobre el resultado de la primera**. Un conflicto de fusión nunca lo resuelve una ejecutora: lo resuelve la directora o se pregunta a Darwin.
6. **Fallos y gasto por encargo.** Cada encargo lleva sus propios fallos, frenos y gasto; los topes de misión suman los dos. Si salta un tope o el freno de uno, **se para el que saltó**; el otro termina lo que lleva, pero no se lanza nada nuevo hasta que Darwin decida.
7. **Lo delicado no va en paralelo** (lo definido como delicado en la spec 088, sección 2): se hace en serie y con el camino completo.
8. **DeepSeek con su límite:** al ser un servicio gratuito, puede tener límites de uso o de velocidad que no están medidos. Si uno de los dos falla por eso, el otro sigue y el fallo se anota como tal.
9. **La prueba de uso real** (spec 050) se hace al final, **sobre el resultado fusionado**, no por encargo.

## 4. Qué cambia en el código (fase 1, pequeña)
- **Nuevo subcomando `fabrica.py solapes ENCARGO_A.md ENCARGO_B.md`**: lee los «Archivos permitidos» de ambos con `leer_encargo` y sale 1 si algún archivo o carpeta coincide o se contiene. Es la forma de que la regla 2 la haga cumplir un guardián y no solo la lectura de la skill.
- **Tope «a la vez»:** línea de carta `- paralelo_max: 2` (por defecto 2; valor 1 desactiva el paralelo). Se lee igual que `_frenos_carta`.
- **Encargos abiertos:** `foto` anota el encargo como «en marcha» y `gasto` o el cierre lo marca «cerrado»; `foto` rechaza un tercer encargo en marcha. Un encargo en marcha sin avance sigue su freno de atasco.
- **Textos** en `textos.py` es/en, con prueba de paridad.
- Sin cambios en el guardián de alcance, la foto ni el gasto: ya son por encargo.

## 5. Qué cambia en las skills y documentos (fase 2)
- `directora-de-fabrica` (es/en): paso nuevo «paralelo», con las reglas de la sección 3, el uso de `solapes` y el orden de fusión.
- `PLANTILLAS_FABRICA` (es/en): cómo esperar a dos trabajos a la vez («espero X desde las H y Y desde las H»).
- `CARTA_META_ARNES`: una línea. `VERSION`, `CAMBIOS.md`, `manifiesto.json` y regenerar el ZIP de Mac **solo si Darwin lo pide**.

## 6. Fuera de alcance
- Más de 2 ejecutoras a la vez.
- Paralelo entre fábricas o proyectos distintos.
- Que las ejecutoras se coordinen entre sí: solo habla cada una con la directora.
- Resolver conflictos de fusión automáticamente.
- Tocar los encargos en marcha de Prominimap ni de `empresa-virtual-sim`.

## 7. Riesgos y límites honestos
- **El mayor riesgo es el solape oculto:** dos encargos que no comparten archivos pero sí un contrato (por ejemplo, uno cambia lo que el otro llama). `solapes` solo ve archivos, no eso; lo cubre el juicio de la directora (regla 3) y la prueba completa tras cada fusión.
- **Más trabajo para la directora:** dos revisiones y dos fusiones seguidas pueden tardar más que lo ahorrado si los encargos son pequeños. Por eso el paralelo solo compensa en encargos de varios minutos cada uno; en camino corto (un solo encargo) no aplica.
- **El gasto no baja:** se paga lo mismo (o más, si hay una fusión difícil).
- **Cuotas:** Codex y DeepSeek pueden tener límites distintos y no medidos cuando van a la vez.
- **Sin probar.** Nada de esto se ha estrenado; hay que medirlo antes de confiar en él.

## 8. Plan de verificación
1. Pruebas automáticas (`python -m unittest discover tests`): `solapes` con archivos iguales, carpeta que contiene a un archivo y encargos sin solape; el tope `paralelo_max`; tercer encargo rechazado; paridad es/en.
2. **Estreno en una fábrica de prueba** (no en Prominimap ni en `empresa-virtual-sim`): dos encargos pequeños sin solape, uno con Codex y otro con DeepSeek, lanzados a la vez.
3. Medir con `python .brain/guardianes/medir.py --fabrica`: tiempo de reloj total frente a lanzarlos en serie, y gasto de cada uno.
4. Comprobar que la fusión en orden y la prueba completa tras cada una dejan todo en verde.
5. Probar el caso malo a propósito: dos encargos con un archivo en común; `solapes` debe frenarlo.
6. Anotar el resultado en la sección 10.

## 9. Criterio para confirmar, apretar o retirar
- **Confirmar** si, en al menos 3 misiones reales con encargos paralelos, el tiempo de reloj baja de forma clara y nada llegó roto a Darwin.
- **Apretar** (volver a 1, o exigir revisión aparte en los dos) si un solape oculto se coló, aunque se detectara luego.
- **Retirar** si el ahorro es pequeño o hay un solo fallo grave de fusión o de pérdida de trabajo.

## 10. Resultados de las pruebas reales
- (vacío; aún sin estrenar)

## 11. Preguntas para Darwin antes de aprobar
- ¿Máximo 2 a la vez te sirve, o quieres dejar abierto subirlo más adelante por carta?
- ¿El paralelo se activa solo cuando la directora lo ve claro (con aviso a ti), o solo si tú lo pides en la misión?
- ¿Para un mismo tipo de encargo prefieres que no se mezcle DeepSeek con lo importante, como ya dice la skill (revisión aparte siempre con DeepSeek)?

## 12. Cierre
- [ ] Spec aprobada por Darwin antes de programar
- [ ] Fase 1 programada y probada (sección 4)
- [ ] Fase 2 hecha, es/en (sección 5), `VERSION`, `CAMBIOS.md` y `manifiesto.json` al día
- [ ] Estreno en fábrica de prueba y medición (sección 8)
- [ ] Resultado anotado en la sección 10 y decisión tomada (sección 9)
- [ ] Línea añadida a `.brain/decisions.log`
