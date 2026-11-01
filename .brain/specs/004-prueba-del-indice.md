# Spec 004: ¿Ayudan los índices? (prueba pequeña, solo lectura)

- **Estado:** hecha y medida; resultados en 004-resultados.md
- **Fecha:** 2026-11-01

## 1. Objetivo
Saber si el patrón «índice corto + detalle aparte» (`hechos-indice.md` → `hechos.md`, `decisions/indice.md` → fichas) hace que la IA encuentre un dato archivado **más barato y sin equivocarse**, frente a no tener índice. Hoy no está medido: las specs 001-003 midieron el arnés entero, no esta pieza. Pregunta concreta: con un archivo histórico grande, ¿el índice ahorra lecturas y evita errores?

## 2. Idea de la prueba (con datos reales de LoboHook)
Se usa una **copia** de `LoboHook/.brain` (solo lectura sobre el original, que no se toca): 78 fichas de decisión (`D-001…D-078`), `decisions/indice.md` (14,7 KB), `archive/hechos.md` (26 KB, ~82 entradas) y `hechos-indice.md` (9 KB). Sin código ni git, para que la IA solo pueda responder con el archivo. Revisado: no contiene claves ni datos personales (las coincidencias son solo la palabra «secreto»). Se hace en una carpeta fuera de LoboHook y fuera de este repo; no se sube a GitHub.

Tres lados, mismo texto de pregunta, chats nuevos de un solo mensaje y solo lectura:
- **A — con índice:** copia tal cual (índices + fichas + regla «leer solo la ficha que corresponda»).
- **B — sin índice:** se quitan `decisions/indice.md` y `hechos-indice.md` y la regla; quedan las fichas sueltas.
- **C — índice viejo:** como A, con 5 filas del índice cambiadas a propósito (ficha equivocada o descripción falsa). Mide el riesgo de no mantenerlo.

**Las 5 preguntas** (respuesta a comprobar contra la ficha al montar):
1. ¿Cuántos créditos y a qué precio es el pack de recarga M? → 10.000 créditos, $9.99 (D-062).
2. ¿Cuántos flujos y acciones permite el plan Esencial? → 15 flujos y 8 acciones (D-054).
3. ¿Qué identificadores tienen las cuentas de prueba y por qué no chocan con uno real? → `…001` a `…006`; un ID real de Discord nunca empieza por 15 ceros (D-055).
4. ¿Cuántos días de aviso exige cambiar la tabla de consumo de créditos de IA? → 30 días (D-062; el detalle no está en la línea del índice). Se cambió la pregunta de «juntar dos fichas» porque D-054 (30 IA, vigente) y D-062 (créditos) no dejan clara una única respuesta: queda como hallazgo a anotar en el informe (un índice con dato viejo).
5. (sin respuesta) ¿Qué se decidió sobre el pago con Bizum? → no consta en ningún sitio; debe decir «no consta».

Las preguntas 1-3 piden un detalle que está en la ficha y **no** en la línea del índice, para que el índice solo sirva de mapa.

## 3. En alcance
- [ ] `bench/indice/montar.py`: copia el `.brain` de LoboHook (solo lectura) y monta las carpetas A, B y C fuera de ambos proyectos.
- [ ] `bench/indice/preguntas.md`: las 5 preguntas y la respuesta correcta de cada una.
- [ ] `bench/indice/verificar.py`: compara la respuesta con la correcta (acierta / falla / inventa).
- [ ] Medir con `medir.py` el coste ponderado y, con `--desglose`, cuántas lecturas hizo y de cuántos bytes.
- [ ] 2 repeticiones por lado y pregunta: 3 lados × 5 preguntas × 2 = **30 chats cortos** de un mensaje (caché igualada con un calentamiento antes de cada tanda, como en la spec 003).
- [ ] Informe `004-resultados.md` y una línea en el README solo si hay conclusión.

## 4. Fuera de alcance
- No tocar LoboHook ni GuildControl, no subir a GitHub, no borrar nada.
- No cambiar el arnés ni `VERSION` en esta spec: solo medir. Si el resultado pide un cambio, va en otra spec.
- No lanzar ningún chat de prueba hasta que Darwin lo ordene.

## 5. Plan de verificación y criterio
- Acierto: A debe acertar ≥ 9/10 y la pregunta sin respuesta debe salir «no consta».
- Coste: A debería costar menos que B en las preguntas de una entrada. Si A ≥ B, el informe dice que el índice **no ahorra** a este tamaño.
- C frente a A: si C falla más, queda demostrado que un índice sin mantener es un riesgo y se propone un guardián que lo compruebe.
- `python -m unittest discover tests` en verde con las piezas nuevas.

## 6. Riesgos dichos de antemano
- Es un solo proyecto (LoboHook): la prueba habla de su tamaño y estilo, no de todos.
- Si A y B salen iguales, puede ser que ~80 fichas sean pocas para notar diferencia; se dice así en el informe.
- Es un solo proyecto y las líneas del índice ya traen datos: si la IA responde solo con la línea, el índice «gana» sin abrir la ficha; se anota cuántas veces ocurre.
- Pocas repeticiones: tendencia, no estadística.
- Coste estimado: chats cortos y de solo lectura, mucho menos que las specs 001-003.

## 7. Cierre
- [x] Spec aprobada por Darwin antes de programar
- [x] Línea añadida a `.brain/decisions.log`
