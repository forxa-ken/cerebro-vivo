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
- Severo no es inventar: si no puedes citar la frase, no es un hallazgo.

## Error que evita
- La directora se aprueba su propia spec y rellena huecos con suposiciones («Frankenstein»); el revisor distinto, con citas, lo deja a la vista antes de gastar encargos.

## Dónde está en el repo
- `.claude/skills/revisor-de-spec`, `.brain/guardianes/fabrica.py` (`sellar-negocio`, `veredicto`, `vueltas`), spec 050 (fase 2).

## Fuente
- Spec 050 (petición de Darwin, 2026-11-14)

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-11-14)
