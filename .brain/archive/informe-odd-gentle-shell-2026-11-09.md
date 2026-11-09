# Informe: Organic Driven Development (Gentle Shell) frente a Cerebro Vivo
Fecha: 2026-11-09. Fuente: docs/readme-reference.md y README de Gentle-Programming/gentle-shell, leídos por un subagente. Las partes marcadas (resumen) vienen de un resumen automático del README y no están verificadas en texto literal. No se leyó la carpeta `odd/` del repo.

## 1. Qué es ODD
- El flujo diario de Gentle Shell (paquete npm `gentle-pi`, espacio de trabajo para el agente de terminal Pi). Es una capa de instrucciones sobre herramientas existentes, no una CLI, un motor de estado ni un harness de ejecución.
- Corre en cada petición, sin que el usuario pida flujo ni plan. Preguntas, revisiones y propuestas son de solo lectura hasta que se pide un cambio.

## 2. Cómo funciona (7 pasos)
1. Authorize (leer solo si no hay permiso de implementar). 2. Explore. 3. Resolve uncertainty (una pregunta solo ante una decisión real). 4. Classify: small o large, reevaluado tras cada lote. 5. Track antes de la primera escritura, solo si es grande. 6. Implement por tareas, ~400 líneas por commit (orientativo), Conventional Commits, rama de funcionalidad. 7. Close: resultado verificado, fallos y siguiente paso.

Idea central: **el tamaño no clasifica; clasifica el «resume test»**. Un trabajo es grande solo si no se puede retomar a partir de la petición más `git diff`. El trabajo pequeño no deja ningún documento.

## 3. Piezas concretas
- Un documento por funcionalidad grande: `odd/tasks/<nombre>.md` (objetivo, alcance, tareas con IDs estables, criterios de aceptación, evidencia, siguiente paso) + espejo en Engram (`odd/<nombre>/tasks`), paquete de memoria aparte (`gentle-engram`).
- Revisión por riesgo (RDD, activa por defecto en Gentle AI v4): tras cada commit una herramienta `gentle_review` valora el riesgo; bajo = silencio, medio = se difiere al PR, alto = se revisa ya.
- Delegación solo con motivo (paralelismo o contexto), nunca por tamaño; verificador independiente si hay riesgo alto.
- TDD según configuración, no porque existan tests.
- Entrega por estrategia: `ask-on-risk` (defecto), `auto-chain`, `single-pr`, `exception-ok`.
- Repo (resumen): `bin/ contracts/ docs/ extensions/ odd/ prompts/ runtime/ scripts/ skills/ tests/ themes/`, MIT, ~2,1k estrellas.

## 4. Comparación con Cerebro Vivo
| Tema | ODD / Gentle Shell | Cerebro Vivo |
| :--- | :--- | :--- |
| Qué es | Flujo de trabajo del agente en cada petición | Memoria persistente + guardianes + skills por proyecto |
| Problema que ataca | Exceso de proceso en trabajo pequeño; retomar trabajo grande | Que la IA no recuerde entre chats y el contexto cueste dinero |
| Memoria | Un documento por funcionalidad grande + Engram | `.brain/` (pendientes, registro, decisiones, traspaso entre chats) |
| Quién vigila | Instrucciones y revisión nativa por riesgo | Guardianes automáticos (hooks) que avisan o bloquean |
| Trabajo pequeño | Sin artefactos | Cierre por bloque (1.29.0): no pide registro hasta 15 ediciones |
| Público | Programadores en terminal (Pi) | Darwin, dueño no técnico: lenguaje llano, es/en |
| Prueba de que funciona | Benchmarks propios n=1 por celda; admiten que pruebas estáticas no demuestran cumplimiento | Mediciones propias (`medir.py`, banco T1-T3); punto 4 pendiente |

## 5. Qué se parece
- Ambos rechazan el proceso pesado por defecto y escalan solo cuando hace falta. Es el mismo espíritu que el cierre por bloque (spec 033).
- Ambos dejan lo que hace falta para retomar sin recontar la historia.
- Ambos admiten que sus reglas no garantizan que la IA las cumpla y quieren medirlo.

## 6. Qué tiene ODD que Cerebro no tiene
- **Criterio de «grande» por el resume test**, más fino que contar archivos o ediciones (nosotros usamos el contador de 15 ediciones sin cerrar).
- **Revisión por riesgo tras cada commit** (bajo/medio/alto). Cerebro tiene el punto 23 (revisor independiente) sin empezar.
- **IDs estables de tareas con criterios de aceptación** en el documento de funcionalidad, y regla explícita de reanudación que reconcilia código y pruebas.
- Estrategias de entrega (PR encadenados, apilados) y commits por unidad de trabajo.

## 7. Qué tiene Cerebro que ODD no muestra
- Guardianes automáticos con hooks que bloquean o avisan (secretos, hitos sin lección, longitud del chat, librerías con vulnerabilidades).
- Traspaso entre chats y entre IA distintas, pensado para chats cortos.
- Dueño no técnico como usuario objetivo: informes en llano, pendientes con «esperando tu prueba».
- Doble idioma, manifiesto con huellas y actualización segura entre proyectos.

## 8. Ideas aprovechables (a decidir por Darwin)
1. Usar el resume test como segundo criterio de cierre por bloque, además del contador de 15 ediciones (se enlaza con puntos 30 y 31).
2. Para el punto 23 (revisor independiente): ODD ya trae un diseño probado en la práctica (valorar riesgo y revisar solo si es medio o alto), que evita revisar todo.
3. IDs estables de tareas con criterios de aceptación en las specs grandes.
Nada de esto está hecho ni probado en Cerebro.

## 9. Límites del informe
- Subagente: no leyó `odd/`, `skills/` ni `contracts/`, ni la parte final de la página de referencia. La estructura del repo y la sección de diferencias vienen de un resumen del README.
- Los benchmarks de Gentle Shell son suyos, con n=1 por celda; no están contrastados.
- La comparación con Cerebro sale de CLAUDE.md, la carta maestra y los pendientes; no la hice línea a línea contra el código.
