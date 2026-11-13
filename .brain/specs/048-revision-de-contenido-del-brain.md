# Spec 048: revisión de contenido de `.brain/` (pendiente 44)

- **Estado:** aprobada por Darwin y programada el 2026-11-13 en el arnés 1.50.0 (582 pruebas en verde); sin probar por Darwin
- **Fecha:** 2026-11-13
- **Origen:** idea del gist «LLM Wiki» de Karpathy: la memoria de un proyecto se pudre sin que nadie lo note. Hoy solo se vigilan el tamaño de los archivos (`archivos_gordos.py`) y las rutas rotas de los índices de IA (`revisar_indices.py`, spec 016). Nadie avisa de que dos documentos se contradicen, de que una frase ya no es cierta o de que una página no la enlaza nadie.
- **Es del arnés:** vale para cualquier proyecto con `.brain/`. Nada de lo que se reparte nombra proyectos concretos.

## 1. Objetivo
Un aviso, **sin bloquear nunca**, de tres cosas que pudren la memoria:
1. **Páginas huérfanas:** archivos de `.brain/` (lecciones, decisiones, biblioteca, specs, respuestas) que ningún índice ni documento enlaza.
2. **Afirmaciones que ya no son ciertas:** el documento dice «existe X», «versión N», «hay K lecciones» o cita un comando, archivo o ajuste que ya no está.
3. **Contradicciones entre documentos:** dos sitios dicen cosas incompatibles (por ejemplo, un tope de bytes distinto, o «pendiente» en uno y «hecho» en otro).

## 2. Decisión de diseño (a confirmar)
Dos capas, igual que `revisar_indices` y su skill:
- **Capa barata y fiable (script `revisar_contenido.py`, solo lectura, librería estándar, es/en):** detecta lo comprobable con reglas, sin IA:
  - huérfanas: enlaces `.md` de todo `.brain/` (salvo `archive/`) frente a los archivos existentes;
  - afirmaciones comprobables: archivos/comandos/guardianes citados que no existen, número de versión citado distinto de `VERSION`, cifras de contadores («N lecciones», «N pendientes») distintas de las reales;
  - **candidatos a contradicción:** la misma magnitud con valores distintos (topes en bytes, versiones, números de spec) en documentos distintos.
- **Capa de juicio (skill `revisar-contenido`, es/en):** la IA creadora toma los candidatos y **busca**; para **refutar** no se fía de sí misma (decidido por Darwin el 2026-11-13: quien encuentra el hallazgo tiende a darse la razón). La refutación la hace **otra pasada sin el contexto de la primera**: por defecto un subagente nuevo del mismo modelo que recibe solo las dos frases y la pregunta «¿se contradicen o ya no es cierto, de verdad?» (apoyándose en la skill `revisor-independiente`); y, **opcional y solo para los casos dudosos**, un segundo juez de otra IA si el proyecto lo tiene configurado (mismo criterio que el segundo juez del auditor, spec 044). Solo lo que sobrevive a la refutación llega a Darwin; lo descartado queda en un archivo de descartes y no se repite. Lo que requiere entender el sentido (contradicciones sutiles) lo hace solo esta capa.

## 3. En alcance
- [ ] `revisar_contenido.py` con salida legible y `--json`, y opciones `--descartar CLAVE --motivo`.
- [ ] Aviso en `arranque.py`: **una sola línea** («N hallazgos en la memoria; pide “revisa el contenido”»), solo si los hay y no pasaron `revision_contenido_dias` desde la última revisión; se apaga con `revision_contenido_activa: false`.
- [ ] Ajustes en `guardianes.json` (`revision_contenido_*`), descartes en `revision_contenido.json`.
- [ ] Textos en `textos.py` es/en; skill `revisar-contenido` y su `.en.md`.
- [ ] La skill indica cómo lanzar la refutación independiente (subagente nuevo con solo las dos frases; segundo juez de otra IA opcional).
- [ ] Pruebas con una carpeta `.brain/` de juguete (huérfana, versión vieja, contador falso, tope contradictorio, descarte que no se repite).
- [ ] `VERSION`, `CAMBIOS.md`, `manifiesto.json`.

## 4. Fuera de alcance
- Corregir nada solo: el script y la skill **informan**, no editan.
- Revisar `archive/` (su sentido es ser histórico) ni el código del proyecto.
- Usar IA o internet dentro del script.
- Fundirlo con `revisar_indices.py`: ese revisa los índices de IA; este, el cuerpo de `.brain/`.

## 5. Riesgos
- Falsos positivos (un número que cambia con razón en dos documentos). Por eso solo avisa, hay descartes y la skill refuta antes de proponer.
- Ruido en el arranque: una línea, con intervalo mínimo entre avisos y apagable.
- Coste de la refutación independiente: una IA más por lote; como el script ya filtra, son pocos casos.
- Coste: lee unos pocos cientos de KB; debe tardar menos de un segundo y no romper el arranque si falla (calla).

## 6. Archivos
`revisar_contenido.py` (nuevo), `arranque.py`, `guardianes.json`, `textos.py`, skill `revisar-contenido` (es/en), `tests/`, `VERSION`, `CAMBIOS.md`, `manifiesto.json`.

## 7. Verificación
`python -m unittest discover tests` en verde; pasada real sobre este repo para ver que lo que sale es real. **No probado hasta hacerla.**
