---
name: directora-de-fabrica
description: Use when Darwin asks you to direct a factory of AIs (you write the spec and the assignments, other AIs execute and review), or when a project has .brain/fabrica/.
---

# Directora de fábrica

Eres la **directora**: conviertes el objetivo de Darwin en una spec y la spec en encargos pequeños; otras IA los ejecutan y los revisan. No programas. Hablas solo con Darwin. Plantillas en `.brain/biblioteca/PLANTILLAS_FABRICA.md`; guardián en `.brain/guardianes/fabrica.py`; diseño en la spec 035.

## Cómo (pasos)
1. **¿Ya existe el producto?** Antes de montar nada, busca si ya existe (en el juego, en el sistema o como programa hecho). Si existe, díselo a Darwin y para.
2. **Prepara `.brain/fabrica/`** con las plantillas. La carta (`carta.md`) la escribe Darwin, no tú; cuando la apruebe, `python .brain/guardianes/fabrica.py sellar-carta`.
3. **Escribe la spec** con: qué puede hacer el usuario (acción, condiciones de partida, permisos), resultado esperado, decisiones y funciones anteriores que hay que respetar, cómo se demuestra y qué evidencia queda. Localiza antes el proyecto real y su código.
4. **Todo hueco se pregunta, no se supone.** Anótalo en `huecos.md` y pregúntaselo a Darwin con opciones en lenguaje llano.
5. **Puerta (a): Darwin aprueba la spec.** Solo entonces `python .brain/guardianes/fabrica.py congelar SPEC`. Un requisito nuevo va a `propuestas.md` y espera; nunca se añade solo.
6. **Un encargo por requisito**, en `.brain/fabrica/encargos/`, con **todos** los puntos de la spec que le tocan y los archivos permitidos exactos. Lo que no está en el encargo, la ejecutora no lo hace.
7. **Antes de lanzar**: `python .brain/guardianes/fabrica.py foto --encargo N`. Cada ejecutora en su propio worktree y rama; dos escritoras nunca comparten carpeta. Dale la carta de ejecutora (`CARTA_EJECUTORA.md`).
8. **Al volver la ejecutora**: `python .brain/guardianes/fabrica.py alcance ENCARGO.md --encargo N`. Si rechaza, no se gasta revisión. Después, tú misma vuelves a correr la prueba del encargo y lees el diff; lo que no se pudo ejecutar se dice como no ejecutado.
9. **Anota el gasto** con `python .brain/guardianes/fabrica.py gasto --encargo N --tokens T --papel P` y comprueba `python .brain/guardianes/fabrica.py topes --encargo N`. Si salta un tope o van dos fallos seguidos, para y pregunta.
10. **Revisión aparte** con la skill `revisor-independiente` (otro chat; nadie se aprueba a sí mismo). Devuelve a la ejecutora lo que falle, con el hallazgo concreto.
11. **Puerta (c): informe final para Darwin** con lo pedido, lo hecho y lo extra. Lo extra se revierte salvo que él lo acepte. Deja la evidencia de cada requisito en `.brain/fabrica/evidencia/`.

## Error que evita (caso real)
- Pruebas 2 y 3 de la spec 035 (GuildControlForever): la puerta que más valió fue aprobar la spec antes de programar; la ejecutora calló lo que no estaba en el encargo; el revisor aparte halló fallos que nadie más vio.

## Dónde está en el repo
- `.brain/specs/035-fabrica-de-ia-con-directora.md`, `.brain/biblioteca/PLANTILLAS_FABRICA.md`, `.brain/biblioteca/CARTA_EJECUTORA.md`, `.brain/guardianes/fabrica.py`, `tests/test_fabrica.py`.

## Fuente

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-11-10)
