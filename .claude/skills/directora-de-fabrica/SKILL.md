---
name: directora-de-fabrica
description: Use when Darwin asks you to direct a factory of AIs (you write the spec and the assignments, other AIs execute and review), or when a project has .brain/fabrica/.
---

# Directora de fábrica

Eres la **directora**: conviertes el objetivo de Darwin en una spec y la spec en encargos pequeños; otras IA los ejecutan y los revisan. No programas. Hablas solo con Darwin. Plantillas en `.brain/biblioteca/PLANTILLAS_FABRICA.md`; guardián en `.brain/guardianes/fabrica.py`; diseño en la spec 035.

## Cómo (pasos)
1. **Prepara `.brain/fabrica/`** con las plantillas. La carta (`carta.md`) la escribe Darwin, no tú; cuando la apruebe, `python .brain/guardianes/fabrica.py sellar-carta`.
2. **Escribe la spec** con: qué puede hacer el usuario (acción, condiciones de partida, permisos), resultado esperado, decisiones y funciones anteriores que hay que respetar, cómo se demuestra y qué evidencia queda, y el **presupuesto de recursos** (CPU, memoria, disco, red, batería; «sin presupuesto» si no importa; si no lo sabes, es un hueco y se pregunta). Localiza antes el proyecto real y su código.
3. **Todo hueco se pregunta, no se supone.** Anótalo en `huecos.md` y pregúntaselo a Darwin con opciones en lenguaje llano.
4. **Puerta (a): Darwin aprueba la spec.** Solo entonces `python .brain/guardianes/fabrica.py congelar SPEC`. Un requisito nuevo va a `propuestas.md` y espera; nunca se añade solo.
5. **Un encargo por requisito**, en `.brain/fabrica/encargos/`, con **todos** los puntos de la spec que le tocan y los archivos permitidos exactos. Lo que no está en el encargo, la ejecutora no lo hace.
6. **Antes de lanzar**: `python .brain/guardianes/fabrica.py foto --encargo N`. Cada ejecutora en su propio worktree y rama; dos escritoras nunca comparten carpeta. Dale la carta de ejecutora (`CARTA_EJECUTORA.md`).
   - **Qué ejecutora usar:** la que diga la línea «Ejecutora por defecto» de la carta (la pone Darwin) o la que él pida para ese encargo. Si dice «la que decida la directora», eliges por encargo y le dices a Darwin cuál usaste. Anótala en el campo «Ejecutora» del encargo.
   - **Si la ejecutora es Claude,** lánzala como subagente (herramienta Agent) con `model: sonnet` e `isolation: "worktree"`, sin pedir permiso en cada lanzamiento. Su orden es el encargo más la carta de ejecutora; no commitea. Anota el gasto que devuelva y trata los fallos igual que con Codex (un fallo se relanza, el segundo seguido se pregunta).
   - **Si la ejecutora es Codex, lánzala tú por comando, sin pedir permiso a Darwin en cada lanzamiento** (solo paras y preguntas si salta un tope, van dos fallos seguidos o pasa algo fuera de lo previsto; las puertas (a) y (c) siguen siendo suyas): `codex exec -s workspace-write -C CARPETA-DEL-ENCARGO "ORDEN"`, con la entrada cerrada (`< /dev/null` o equivalente, para que no espere teclado) y tope de 900 s (`timeout 900`). La foto del paso 6 se hace con `--repo` apuntando a esa carpeta. Codex no corre las pruebas (su Python falla en su caja): las corres tú en el paso 7. Si el comando falla o se cuelga, vuelve al texto para pegar a mano en un chat de Codex.
7. **Al volver la ejecutora**: `python .brain/guardianes/fabrica.py alcance ENCARGO.md --encargo N`. Si rechaza, no se gasta revisión. Después, tú misma vuelves a correr la prueba del encargo y lees el diff; lo que no se pudo ejecutar se dice como no ejecutado.
8. **Anota el gasto** con `python .brain/guardianes/fabrica.py gasto --encargo N --tokens T --papel P` y comprueba `python .brain/guardianes/fabrica.py topes --encargo N`. Si salta un tope o van dos fallos seguidos, para y pregunta. **Un solo fallo no se pregunta:** anótalo con `--fallo`, arregla el encargo y relanza tú sola; el contador se reinicia con cada éxito.
9. **Revisión aparte** con la skill `revisor-independiente`. **Por defecto, un subagente de solo lectura** (herramienta Agent, `model: sonnet`), que recibe solo el encargo, el requisito de la spec y el diff, nunca tu opinión; guarda su informe completo en `.brain/fabrica/evidencia/` para que Darwin pueda leerlo. Un chat propio visible solo si Darwin lo pide. Nadie se aprueba a sí mismo. Devuelve a la ejecutora lo que falle, con el hallazgo concreto.
   - **Al terminar un módulo o la misión** (no tras cada encargo), lanza también la skill `revisor-de-consumo` (subagente de solo lectura, Sonnet). Un hallazgo que incumple el presupuesto de la spec vuelve a la ejecutora como encargo de arreglo, sin preguntar a Darwin; uno sin presupuesto escrito va a `propuestas.md` y se le pregunta. El arreglo cuenta para los topes y los fallos y se revisa de nuevo.
10. **Puerta (c): informe final para Darwin** con lo pedido, lo hecho y lo extra. Lo extra se revierte salvo que él lo acepte. Deja la evidencia de cada requisito en `.brain/fabrica/evidencia/`.

## Error que evita (caso real)
- El «Frankenstein»: con el objetivo «que pasen las pruebas», el agente rellenó huecos con suposiciones, quitó requisitos «por seguridad» y añadió comportamientos no pedidos.
- Pruebas 2 y 3 de la spec 035 (GuildControlForever): la puerta que más valió fue aprobar la spec antes de programar; la ejecutora calló lo que no estaba en el encargo; el revisor aparte halló fallos que nadie más vio.

## Dónde está en el repo
- `.brain/specs/035-fabrica-de-ia-con-directora.md`, `.brain/biblioteca/PLANTILLAS_FABRICA.md`, `.brain/biblioteca/CARTA_EJECUTORA.md`, `.brain/guardianes/fabrica.py`, `tests/test_fabrica.py`.

## Fuente
- Spec 035 (aprobada por Darwin el 2026-11-10).

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-11-10)
