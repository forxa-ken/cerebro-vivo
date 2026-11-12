# Spec 046: diagramas y gráficos completos dentro de `/diapositivas`, por fases

- **Estado:** fase 1 (flowchart y sequenceDiagram) **aprobada por Darwin el 2026-11-12 («hagamos lo simple») e implementada en 1.46.0, sin probar por Darwin**. Las fases 2 a 5 y la spec 047 (vídeo) quedan para después; se aprueban una a una.
- **Fecha:** 2026-11-12
- **Origen:** Darwin preguntó si se puede generar gráficos desde los Markdown (por ejemplo un UML que explique el proceso) y pidió que sea **completo, hecho por partes**. Hoy `diapositivas.py` solo muestra diagramas hechos con texto y tablas.

## 1. Objetivo
Que una diapositiva (y cualquier `.md` del proyecto que se presente) pueda llevar **dibujos de verdad** escritos como texto: procesos, UML, estados, bases de datos, calendarios y gráficos de cifras. Se pintan solos como SVG dentro del `.html`, **sin instalar nada, sin internet y sin librerías** (Python estándar, es/en).

## 2. Decisión de diseño (a confirmar)
**Escribir los diagramas con un subconjunto de la sintaxis Mermaid** (bloque ```` ```mermaid ````) y dibujarlos con nuestro propio código Python, sin Mermaid ni internet.
- **Por qué:** es el estándar; el mismo `.md` se ve ya dibujado en GitHub y VS Code y la IA lo escribe bien. No inventamos un idioma nuevo.
- **Coste:** hay que escribir un lector y un dibujante por cada tipo. Es lo que parte el trabajo en fases.
- **Si algo no se entiende:** la diapositiva muestra el texto original en un bloque de código y el script avisa (mensaje es/en en `textos.py`). Nunca rompe la presentación.
- **Alternativa descartada:** sintaxis propia (más fácil de programar, pero solo vale aquí). Se puede reabrir si Darwin prefiere la fase 1 más rápida.

## 3. Fases (cada una se aprueba, se programa, se prueba y se cierra aparte)
| Fase | Tipos de diagrama | Para qué sirve | Tamaño |
| :--- | :--- | :--- | :--- |
| **1** | `flowchart` (cajas y flechas, de izquierda a derecha o de arriba abajo, con etiquetas en las flechas y formas básicas) y `sequenceDiagram` (quién habla con quién, en orden) | El proceso de una tarea, quién llama a quién, el ciclo del arnés | Mediano: incluye el dibujo automático de posiciones |
| **2** | `classDiagram` (clases con atributos y métodos, herencia, composición, asociación) y `stateDiagram-v2` (estados y transiciones) | UML de estructura y ciclo de vida de un punto de `pendientes.md` | Grande |
| **3** | `pie` (tarta), barras y líneas simples, `xychart` | Cifras: tokens, pruebas, versiones | Mediano |
| **4** | `erDiagram` (entidades y relaciones), `gantt` (calendario), `journey` o mapas mentales si Darwin los quiere | Bases de datos, planes en el tiempo | Grande |
| **5** | Pulido: temas claro y oscuro, zoom y ancho de móvil, exportar el diagrama a PNG/SVG suelto, medir el consumo del dibujo | Que se vea bien en cualquier pantalla | Pequeño |

**Cada fase incluye (sin repetirlo en la lista):** textos es/en, skill `/diapositivas` (es y `.en.md`) con cuándo usar el tipo y la regla de que **el dibujo sale de los archivos leídos, no se inventa**, una línea en el manual (es y en), versión nueva, `CAMBIOS.md`, manifiesto, ejemplo real en `.brain/diapositivas/` y revisión de la página pública (`gh-pages`; no se sube sin orden de Darwin).

## 4. En alcance (común a todas las fases)
- [ ] Bloque ```` ```mermaid ```` dentro de una diapositiva; lo no soportado cae a texto con aviso.
- [ ] SVG inline con los colores del tema del visor (claro y oscuro); texto escapado; sin HTML ni enlaces dentro del bloque.
- [ ] Posicionamiento automático sin librerías (capas para `flowchart`, columnas para `sequenceDiagram`, etc.).
- [ ] Límites para que se lea bien (p. ej. 12 nodos por diapositiva); pasado el límite, aviso y texto, o el diagrama pasa a su propia diapositiva.
- [ ] Pruebas por tipo: tantos elementos como líneas; bloque inválido cae a texto y avisa; sin peticiones externas; UTF-8 en consola de Windows; `--comprobar` sigue contando las secciones igual; paridad es/en en verde.

## 5. Fuera de alcance
- Cargar Mermaid o PlantUML reales desde internet o instalarlos.
- Diagramas de arquitectura en la nube (C4, bloques), mapas de git, mapas mentales y todo lo no listado en las fases, salvo que Darwin lo pida.
- Edición en el navegador y animaciones.
- Cambiar el resto del arnés o del visor.

## 6. Riesgos
- **«Completo» es muy grande:** Mermaid entero son miles de líneas. Mitigación: subconjunto por tipo (lo que se usa de verdad) y fases; cada tipo se declara con su lista de lo que sí soporta.
- **Dibujos feos con textos largos o muchos nodos.** Mitigación: ajuste de línea en las cajas y límites; si no cabe, cae a texto.
- **La IA inventa un proceso que no existe.** Mitigación: la skill manda sacarlo de los archivos leídos y citarlos en la última diapositiva.
- **`diapositivas.py` se pasa del tope de archivos gordos.** Mitigación: cada pintor va en su propio archivo (`diagramas_*.py`) desde la fase 1.

## 7. Verificación
- `python -m unittest discover tests` en verde tras cada fase.
- Abrir el ejemplo de la fase en el navegador (claro, oscuro y ancho de móvil). **Sin probar por Darwin hasta que lo haga.**

## 8. Cierre
- [ ] Spec aprobada por Darwin antes de programar (la fase 1 primero)
- [ ] Línea añadida a `.brain/decisions.log` al cerrar cada fase
