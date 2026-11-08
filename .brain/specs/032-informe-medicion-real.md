# Informe 032 · Medición real del arnés en Modelo 2, LoboHook y cerebro-vivo (2026-11-08)

- **Estado:** informe (solo lectura; no se cambió nada del arnés). Arnés 1.28.8.
- **Pedido por Darwin:** medir de forma exhaustiva en los proyectos que ya llevan tiempo trabajando, para decidir qué recortar (continúa el informe 028 y el punto 4 de pendientes).

## 1. Qué se midió y cómo
Se leyeron los registros de Claude Code (`~/.claude/projects/…/*.jsonl`), solo lectura. Muestra: **Modelo 2** 16 chats (1.551 llamadas), **LoboHook** 84 chats (7.460), **cerebro-vivo** 27 chats (2.247); se descartaron los chats de menos de 3 llamadas. Se excluyó la carpeta `F:\Modelo` (es un bot, no un proyecto con el arnés).

- **Unidad de coste:** tokens equivalentes de entrada: entrada + 1,25 × escritura de caché + 0,1 × lectura de caché + 5 × salida (la misma lógica que `medir.py`).
- **Cada llamada a la IA se clasifica** por lo que hizo: **trabajo** (código, lectura, edición de lo del proyecto, respuestas), **memoria** (skills del arnés, `cerrar.py`, `lecciones.py`, `decisions.log`, `pendientes`, `hechos`, traspasos), **chat nuevo** (`start_session`, `detach_session`…), **aviso** (llamada que responde a un aviso del guardián de cierre), **app** (`update_plan`, `wrap_up`: son de la app de Claude, no del arnés) y **mantenimiento del arnés** (`CAMBIOS.md`, manifiesto, actualizador; solo tiene sentido en cerebro-vivo).
- **Límites:** la clasificación es por reglas sobre el texto de las herramientas, no es perfecta. Una llamada mixta cuenta como trabajo. Los tokens de un texto se estiman a 3,6 caracteres por token. No hay proyecto gemelo sin arnés: **no se mide beneficio, solo coste y frecuencia**.

## 2. Resultado 1: dónde se va el coste (porcentaje del coste total)

| | Modelo 2 | LoboHook | cerebro-vivo |
|---|---|---|---|
| Trabajo | 80,8 % | 78,4 % | 48,2 % |
| Memoria (rituales del arnés) | 10,2 % | 14,7 % | 18,0 % |
| Chat nuevo | 2,9 % | 1,5 % | 6,6 % |
| Aviso de guardián (llamada extra) | 2,5 % | 0,9 % | 2,1 % |
| Contexto inyectado por hooks | 0,7 % | 0,5 % | 1,2 % |
| **Total atribuible al arnés** | **≈16 %** | **≈18 %** | **≈28 %** |
| App (no es del arnés) | 2,7 % | 3,8 % | 6,6 % |
| Mantenimiento del arnés | 0,9 % | 0,7 % | 18,4 % |

- En proyectos de trabajo real **entre un sexto y un quinto del coste es ritual del arnés**. En cerebro-vivo es mayor porque aquí el arnés es el propio trabajo (por eso el 18,4 % de mantenimiento no cuenta como sobrecoste).
- Fracción de llamadas rituales (memoria + chat nuevo + aviso): 18 % en Modelo 2, 21 % en LoboHook, 48 % en cerebro-vivo.

## 3. Resultado 2: el arranque es barato; el ritual está durante el chat
- Mediana de arranque: **76k** (Modelo 2), **74k** (LoboHook), **76k** (cerebro-vivo). Lo que pone el arnés al empezar (`CLAUDE.md`, constitución, pendientes, lista de skills, resumen de arranque) es **~4k en cerebro-vivo y ~7k en LoboHook: un 5-9 %**. El resto es de Claude Code (instrucciones, herramientas, conectores).
- Los cuerpos de las skills (~12k en cerebro-vivo) solo cargan si se llaman.
- Los hooks inyectan unos 1.000-1.250 tokens por chat al arrancar (SessionStart) y ~0,5-1,2 % del coste en total.
- Conclusión: **recortar el arranque no mueve la aguja**; los 10k que creció el arranque de LoboHook (69k → 79k entre el 26 de octubre y el 8 de noviembre) no los explican los archivos del arnés (probable origen: herramientas o conectores de Claude Code, no comprobado).

## 4. Resultado 3: los avisos del guardián de cierre
| | Modelo 2 | LoboHook | cerebro-vivo |
|---|---|---|---|
| Avisos | 41 | 71 | 46 |
| Por chat | 2,6 | 0,85 | 1,7 |
| Chats con al menos uno | 14 de 16 | 41 de 84 | 25 de 27 |
| «Registro (decisions.log)» | 24 | 35 | 10 |
| «Chat largo / traspaso» | 10 | 33 | 19 |
| «Hito sin lección» | 7 | 1 | 17 |
| Coste de responderlos | 2,5 % | 0,9 % | 2,1 % |

- Cada aviso obliga a una llamada extra que relee todo el contexto.
- **Lecciones apuntadas:** Modelo 2 10 reales y 1 «ninguna»; LoboHook 2 reales y 0; **cerebro-vivo 12 reales y 24 «ninguna»**. En cerebro-vivo **2 de cada 3 avisos de «hito sin lección» acabaron en «no hay nada que aprender»**: el guardián da falsas alarmas aquí (en Modelo 2 solo 1 de 11).
- **Cierres por chat (`cerrar.py`):** 39 en 16 chats (2,4 por chat) en Modelo 2, 92 en 87 en LoboHook (1,1) y **205 en 28 en cerebro-vivo (7,3 por chat)**. Cerebro-vivo cierra una línea por cada tarea pequeña.

## 5. Resultado 4: el ritual crece con el tiempo
- LoboHook (ritual + aviso sobre su coste, por día): 10-11 % los tres primeros días (25-27 oct), 28-35 % el 28 y 31 oct, entre 13 y 30 % en noviembre. Media de los últimos chats: ~20 %, el doble del inicio.
- Modelo 2: 17 % → 23 % entre el 4 y el 8 de noviembre.
- Son pocos chats por día; es una tendencia, no una estadística.

## 6. Resultado 5: skills
- Usadas de verdad: 8 de 29 (cerebro-vivo), 8 de 29 (Modelo 2), 16 de 43 (LoboHook). `traspaso-in` domina (31, 29 y 15 llamadas). A cero en los tres: `acorta`, `adopta`, `adoptar-indice-existente`, `chat-nuevo`, `explicar-a-darwin-en-llano`, `guardian-avisa-o-bloquea`, `implementada-no-es-hecha`, `leccion`, `memoria-traspaso`, `traspaso-out`, `trocea`.
- Cuidado: un cero no siempre es «no sirve»: varias se aplican por los textos de los guardianes sin llamar a la skill, y el medidor no las ve.
- La lista de skills pesa ~1k tokens al arrancar: quitar 20 sin uso ahorraría ~0,7k.

## 7. Calidad (sin grupo de control)
Correcciones tuyas por chat: Modelo 2 **0,69**, LoboHook **0,36**, cerebro-vivo **0,52**. No se puede atribuir al arnés: trabajan en cosas distintas.

## 8. Lo que ya sabíamos de los bancos controlados (specs 003 y 004, arnés 1.3.1, 5 repeticiones)
- Tareas pequeñas: sobrecoste de **+7 %** (T1) y **+16 %** (T2), con el mismo acierto con y sin arnés (5/5 y 5/5).
- Retomar un trabajo a medias (T3): **con arnés 5/5 aciertos, sin arnés 0/5**, a un coste de +59 %.
- Índices de fichas (spec 004): +19 % de coste y el mismo acierto.
- **Esos números son de la 1.3.1.** El arnés tiene hoy 25 versiones más y no se ha vuelto a medir con banco.

## 9. Respuesta a «¿es un Frankenstein?»
- **El arranque no.** Es casi todo de Claude Code; lo del arnés es un 5-9 %.
- **El ritual durante el chat sí pesa:** del 16 al 18 % del coste en los dos proyectos reales y 2 de cada 3 avisos de lecciones en cerebro-vivo no sirvieron. Ese sexto del coste se justifica solo si compensa en lo que el arnés sí ganó (recordar entre chats: T3, 5/5 frente a 0/5); **en proyectos reales no hay medida del beneficio**.
- **Más piezas que las que se usan:** 8 de 29 skills.

## 10. Propuestas (ninguna hecha; decide Darwin)
1. **Cierre una sola vez por chat o por bloque de trabajo**, no una línea por tarea pequeña (cerebro-vivo: 7,3 por chat). Es el recorte con más probabilidad de ahorrar, porque cada cierre es una llamada que relee todo.
2. **Hito sin lección:** exigir menos (p. ej. solo si hubo un error que se repitió), porque en cerebro-vivo el 67 % acabó en «ninguna». Antes de tocarlo, comprobar por qué en Modelo 2 sí acierta casi siempre.
3. **Skills a cero:** no quitarlas aún; fusionar las que repiten lo que ya dicen los guardianes (`leccion`, `cerrar-una-tarea`, `chat-nuevo`) cuando haya más chats medidos.
4. **Repetir el banco T1-T3 con la 1.28.8** (5 repeticiones por lado) para saber el sobrecoste actual y cumplir el punto 4 de pendientes. Hasta entonces, los guardianes nuevos siguen congelados.
5. **Si se quiere repetir esta medición:** el script usado es temporal (no está en el repo). Si interesa, se convierte en `medir.py --ritual` con su prueba y su versión.
