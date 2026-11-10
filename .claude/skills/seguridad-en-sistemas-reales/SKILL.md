---
name: seguridad-en-sistemas-reales
description: Use when the project will act on real servers, infrastructure or data (VMware, nube, bases de datos) or when writing the motor/reglas de seguridad of such a project.
---

# Seguridad en sistemas reales

Reglas que, en el experimento VMware (rondas 3 y 4, 2026-11-09), separaron al código seguro del que no lo era. Sin ellas, tanto Cerebro Vivo como ODD dejaron un motor que dependía de detalles internos del laboratorio. Con ellas, los dos salieron igual de seguros.

## Cómo (pasos)
1. **Todo cambio pasa por el motor.** La línea de comandos y los módulos no llaman al servidor directamente para cambiar algo.
2. **Si hay duda, se pide visto bueno (fallar hacia lo seguro).** Si no se puede saber si una acción es delicada (estado de la máquina, tamaño, si existe un dato), se trata como delicada.
3. **Las reglas de seguridad no dependen de detalles internos del laboratorio.** Al servidor solo se le consulta por métodos de su interfaz; uno real no tendrá los atributos internos del simulador.
4. **Cada regla de seguridad lleva una prueba con un servidor falso mínimo** (solo `describir` y `ejecutar`, sin atributos internos) que demuestre que sigue exigiendo el visto bueno.
5. **Entradas raras** (nombres vacíos, tamaños cero, negativos, texto o ausentes, nombres repetidos) se rechazan con un error claro y anotado antes de tocar nada.
6. **Lista de comprobación antes de cerrar**, escrita en el resultado: qué acciones son delicadas, qué pasa si falta información, qué pasa con entradas raras, qué se registró, que no hay credenciales. Si un punto falla, se corrige antes de cerrar.
7. **Seguridad sin cambiar lo pedido.** Ninguna IA cambia ni quita un requisito «por seguridad». Si ve un riesgo, lo registra como hueco o propuesta y pregunta a Darwin (en una fábrica de IA, spec 035, regla R9).

## Error que evita (caso real)
- Ronda 3: el motor de una rama preguntaba al servidor `es_en_caliente` y, si no existía, **actuaba sin permiso** sobre una máquina encendida. Sus 29 pruebas no lo detectaban porque solo usaban el laboratorio.
- Ronda 4: dos ramas sin estas reglas reventaban con un error interno ante un servidor distinto: no actuaban, pero por accidente y sin dejar registro.

## Dónde está en el repo
- `.brain/archive/informe-experimento-vmware-ronda3-2026-11-09.md` y `...ronda4-2026-11-09.md` (pruebas y resultados).

## Fuente
- Experimento Cerebro Vivo contra ODD, punto 37 de pendientes (muestra de 1 por casilla: tendencia, no prueba).

## Usada
- Uso real: `python .brain/guardianes/medir.py --skills` (no se anota aquí) (creada el 2026-11-09)
