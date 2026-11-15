# Traspaso del chat #28 al #29 (2026-11-15)

- **IA que lo escribe:** Claude
- **IA que sigue:** Claude

## Lo último que pidió Darwin
- «Sí, commit y avisa a la directora» (hecho: commit `b126996`, v1.59.0; aviso enviado a la directora del proyecto nuevo, el chat «empresa-virtual-sim #2»).
- Antes pidió: «hay que implementar que no esté preguntando entre encargos que los haga directamente» (modo automático).

## Espera su respuesta
- Nada pendiente de contestar.

## Qué se hizo en el chat #28
- Revisor de spec probado con una segunda spec de otro tipo (spec 001 de VMware, 4 de 4 con Claude Opus, 1 repetición): v1.58.2, página pública al día (gh-pages `0697420`).
- Lección `arnes-pruebas-y-manifiesto` troceada en dos temas; lecciones nuevas `arnes-skills` y una en `arnes-fabrica`.
- **Primera prueba real del modo automático:** proyecto nuevo `F:\Proyectos Antigravity\empresa-virtual-sim` (repo privado `forxa-ken/empresa-virtual-sim`, arnés 1.58.2): simulador de empresa virtualizada para que Darwin aprenda. Negocio aprobado y sellado; spec 001 v3 aprobada, carta y esperado sellados, 7 encargos, línea ya trabajando en la rama `fase1` (el chat de la directora es «empresa-virtual-sim #2»).
- v1.59.0: la skill `directora-de-fabrica` (es/en) dice que en automático no se pregunta entre encargos. Causa: la regla estaba en la spec y en `/fabrica` pero no en la skill que sigue la directora.

## Pendiente de arreglar en cerebro-vivo (hallazgos del auditor de cierre, sobre v1.59.0; sin grave)
1. La lista de «solo paras por…» quedó resumida: faltan gastar dinero, instalar programas, configuración personal, cambiar accesos y los «nunca» (forzar push, saltarse guardián o prueba, borrar evidencia). Completarla o remitir con claridad a la sección 3 de la spec 050.
2. La skill dice «dos fallos seguidos» (paso 8, spec 035) y la spec 050 habla de 3 reintentos y freno a los 3 fallos: decidir cuál manda en automático y escribirlo.
3. Aclarar que el hueco pequeño conservador matiza el paso 3 («todo hueco se pregunta») solo en automático, y dónde se anota (`huecos.md` e informe); no saltarse la pregunta del paso 9 (hallazgo de consumo sin presupuesto); recordar `gasto`/`topes` tras cada encargo; nombrar la prueba de uso real y `entregar`.
4. La prueba `DirectoraAutomaticoTest` solo vigila la primera viñeta: añadir marcas de la sección 3 de la spec 050 («sección 3 de la spec 050» / «section 3 of spec 050»).
- Al arreglar: subir VERSION (1.59.1), CAMBIOS, `generar_manifiesto.py`, pruebas; el tope de las skills es 60 líneas (hoy 44).

## Estado de subida
- Sin subir a GitHub: commit `b126996` (v1.59.0). Todo lo anterior está subido.
- Proyecto nuevo `empresa-virtual-sim`: commit `46499e5` subido; la directora hace sus propios commits.

## Lo que debe hacer Darwin
- Esperar el informe de la línea (`.brain/fabrica/informe.md` en `empresa-virtual-sim`) y probar el simulador. Si la línea para, la directora le preguntará.
- Decidir si se sube la 1.59.0 y si, al acabar la ronda, se trae al proyecto con `python .brain/guardianes/actualizar_arnes.py --simular` (no actualizar mientras la línea trabaja).

## NO hacer
- No subir a GitHub ni a la página sin orden de Darwin. No tocar `vmware-automatizacion` original, LoboHook ni Guild Control. No actualizar archivos de `empresa-virtual-sim` mientras la línea trabaja.
- Si hay hallazgos del arnés durante la prueba, apuntarlos aquí (cerebro-vivo es el repo del método), no arreglarlos en el proyecto nuevo.
