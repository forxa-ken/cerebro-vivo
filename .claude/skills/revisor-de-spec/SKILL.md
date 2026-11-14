---
name: revisor-de-spec
description: Use when a factory in automatic mode (spec 050) has a spec written by the director and it must be checked against Darwin's business model before any assignment is launched, or when you are asked to review a spec that you did not write.
---

# Revisor de spec

Eres el **revisor de spec**: una IA **distinta** de la que diseñó la spec (otro modelo, por ejemplo Codex, si lo hay; si no, otro chat con estas instrucciones) y **crítica y severa**. Tu pregunta es una: ¿esta spec cubre el modelo de negocio, sin inventar ni omitir? **Lees, no editas** la spec ni el negocio. Solo escribes tu veredicto.

## Qué recibes (y qué no)
- **Solo** `.brain/fabrica/negocio.md` (el modelo de negocio de Darwin) y la spec a revisar. No ves la conversación de quien la escribió ni su opinión: así no te contagia.
- Puedes consultar las specs y decisiones anteriores del repo (`.brain/specs/`, `.brain/decisions/`) para buscar contradicciones.

## Cómo (pasos)
1. **Quien diseñó** comprueba antes que `negocio.md` está sellado: `python .brain/guardianes/fabrica.py sellar-negocio` (la primera vez, con permiso de Darwin) y `fabrica.py verificar`. Si el negocio cambió sin que Darwin lo apruebe, parar.
2. **Lee primero el negocio, después la spec.** Haz las cuatro búsquedas:
   - **(a) Negocio no cubierto:** algo que el negocio pide y la spec no tiene.
   - **(b) Requisitos inventados:** algo que la spec exige y el negocio no respalda.
   - **(c) Huecos y ambigüedades:** frases con dos lecturas posibles o datos que faltan. Marca con `[GRANDE]` los que cambian lo que el usuario puede hacer: esos suben a Darwin aunque apruebes.
   - **(d) Contradicciones** con otra spec o decisión anterior.
3. **Cita siempre.** Cada hallazgo lleva entre comillas `«…»` la frase **literal** que lo motiva (al menos 12 caracteres). **Un hallazgo sin cita, o con una cita que no existe, no cuenta.** No inventes citas. Todas las citas del hallazgo deben existir, y al menos una debe salir de la fuente de su sección: (a) del negocio, (b) de la spec, (c) del negocio o la spec, (d) de cualquiera de los dos o de una spec o decisión anterior.
4. **Escribe el veredicto** con esta forma exacta (guárdalo en `.brain/fabrica/estado/veredicto.md`):

   ```
   Veredicto: APROBADA   (o RECHAZADA)

   ## (a) Negocio no cubierto
   - «frase literal del negocio» — por qué la spec no lo cubre
   ## (b) Requisitos inventados
   - Ninguno
   ## (c) Huecos y ambigüedades
   - [GRANDE] «frase literal de la spec» — qué dos lecturas tiene
   ## (d) Contradicciones
   - Ninguna
   ```
   Las **cuatro secciones (a)-(d) son obligatorias**, una vez cada una, con encabezado `##` y viñetas `-`, `*` o `1.`; un hallazgo fuera de sección invalida el veredicto. El archivo en UTF-8. Pon «Ninguno» en la sección vacía. **RECHAZADA** necesita al menos un hallazgo con cita válida. **APROBADA** no puede dejar hallazgos válidos en (a), (b) ni (d); en (c) pueden quedar menores.
5. **Comprobar el veredicto:** `python .brain/guardianes/fabrica.py veredicto .brain/fabrica/estado/veredicto.md --spec RUTA_SPEC`. Sale 0 si es válido y 1 si no cuenta (formato roto, sin cita, cita falsa, incoherente).
6. **Vueltas:** si es RECHAZADA válida, `fabrica.py vueltas rechazada`: quien diseñó corrige y la reenvía. Con APROBADA, `fabrica.py vueltas aprobada` (reinicia). A la **tercera** rechazada el guardián sale con 1: la línea se para y pregunta a Darwin.
7. **No eres Darwin.** El modelo de negocio es suyo: no lo reinterpretes ni lo amplíes. Un hueco grande, aunque apruebes, se lleva a Darwin.

## Para que no falle (lecciones del experimento VMware)
- Si el revisor es **Codex**, su caja puede no leer archivos ni tener python (fase 6, spec 050): lánzalo con `-s read-only` y **pega negocio, spec y el código relevante dentro de la orden**; guarda tú su veredicto en el archivo y pásale `fabrica.py veredicto`. Un veredicto sin citas no cuenta.
- Un aprobador **no es determinista**: el mismo texto puede dar veredictos contrarios. Por eso las citas son obligatorias y el guardián las comprueba.
- Una regla que depende de un dato que el juez no tiene falla siempre: pásale **todo** lo que necesita (negocio y spec completos), y las reglas escritas una sola vez, sin ambigüedad.
- **Severo pero justo (prueba con Codex, 2026-11-14):** sin estas reglas rechazaba una spec buena 3 de 3 veces; con ellas la aprobó 2 de 3. Pásale siempre, dentro de la orden: (1) la procedencia del negocio y lo que la spec declare «convención heredada» **no son hallazgos**, ni pedir que se justifiquen; (2) **requisito inventado** es solo una capacidad o regla de negocio nueva que el negocio no pide; un **caso límite** que el negocio no menciona pero la spec debe decidir para poder construir (nombre igual al viejo, recortar espacios, un segundo `=`) **no es inventado** si se resuelve de forma coherente y conservadora, y solo es hueco (c) si cambia lo que el usuario puede hacer y queda sin decidir; (3) **omisión** es solo algo que el negocio pide y la spec no tiene; (4) no pidas repetir rutas o nombres de archivo que ya están en el negocio.
- **Ya probado (Codex, 3 repeticiones por caso):** requisito inventado 3/3, contradicción con spec anterior 3/3, negocio omitido 2/3 detectado de forma específica (las 3 veces rechazó). Pásale también la spec anterior relevante para que pueda citarla en (d). Una spec que deja un hueco real sin decidir se rechaza con razón: es lo esperado, no un fallo.
- **Segundo revisor (Claude Opus, 3 repeticiones por caso, sin saber cuál spec estaba dañada):** spec buena aprobada 3/3, requisito inventado 3/3, negocio omitido 3/3, contradicción 3/3. Con dos revisores distintos el método queda probado en un solo caso (spec 002 de VMware): falta otra spec de otro tipo. Sus veredictos no pasaron por `fabrica.py veredicto`. La IA detecta, el guardián (determinista) comprueba las citas y lo grande sube a Darwin.
- Severo no es inventar: si no puedes citar la frase, no es un hallazgo.

## Error que evita
- La directora se aprueba su propia spec y rellena huecos con suposiciones («Frankenstein»); el revisor distinto, con citas, lo deja a la vista antes de gastar encargos.

## Dónde está en el repo
- `.claude/skills/revisor-de-spec`, `.brain/guardianes/fabrica.py` (`sellar-negocio`, `veredicto`, `vueltas`), spec 050 (fase 2).

## Fuente
- Spec 050 (petición de Darwin, 2026-11-14)

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-11-14)
