# Revisión independiente, spec 090 fase 2 (2026-11-20)

Revisor: IA aparte, solo lectura. Partí de cero. Lo único escrito es este informe; mis pruebas de ataque se hicieron en carpetas temporales del sistema (nunca en el repo ni en proyectos reales).

## Veredicto: APTO CON REPAROS

Lo esencial de la fase 2 se cumple: las simulaciones **no escribieron nada** en un proyecto (lo comprobé aparte, ver abajo), los POST exigen clave en cabecera, Host y origen, token de un solo uso por acción, y la lista de acciones está cerrada. Hay 3 hallazgos de gravedad (a) que conviene arreglar antes de la fase 3 (cuando las acciones sí escriban), y varios (b).

Pruebas existentes: `python -m unittest tests.test_web_proyectos tests.test_web` -> 32 pruebas, OK (1 saltada, la del enlace simbólico).


**Troceado el 2026-11-25** (pasaba del tope de 8 KB; copia integra en `.brain/archive/troceado/2026-11-25-090-fase2-revision.md`). El resto del informe, tal cual:
- Hallazgos (a, b, c): `090-fase2-revision-hallazgos.md`
- Lo comprobado, falta o sobra, pruebas, lo no comprobado y resumen: `090-fase2-revision-comprobado.md`
