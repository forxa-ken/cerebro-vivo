# Pendientes

Lista viva de **lo que falta**. Una línea por punto. **Numeración fija** (los huecos son puntos ya terminados: están en `archive/hechos-indice.md`).

**Regla de cierre:** cuando Darwin prueba una tarea y confirma, en esa misma respuesta se pasa su detalle a `archive/hechos.md`, se añade su fila a `archive/hechos-indice.md` y se quita de aquí. Si la prueba falla, vuelve a «Falta programar» con una nota de qué falló.

## Falta programar (IA)
- **4:** repetir el banco T1-T3 (specs 003 y 004, 5 repeticiones por lado) con la 1.29.0 para saber el sobrecoste actual; hasta entonces los guardianes nuevos siguen congelados. Cuesta dinero: Darwin da el visto bueno. Informe 032 (medición real) hecho.

- **19:** diseñar (spec aparte) cómo colaboran varias IA con responsabilidades distintas en un proyecto (caso Guild Control Forever: Claude con `.brain/`, Gemini solo traducciones con `AGENTS.md`). A decidir: qué lee/escribe cada IA, cómo no pisarse, `indices_ajenos` en `guardianes.json`. Detalle en `archive/pendientes-detalle-2026-11-08.md`.

- **22:** automatizaciones en la nube (Jenkins o GitHub; hoy todo corre en local). Antes: explicarle a Darwin cada opción en llano y que elija. Sin empezar.

- **23:** aprender a montar un agente que verifique las pruebas y errores de la IA principal (revisor independiente; idea somera de Darwin; sale de `F:\Arquitectura de desarrollo`, REC-003/004/005). Explicárselo en llano y hacerlo paso a paso con él. Sin empezar.

- **32:** ampliar `librerias.py` y el guardián `eventos_chat.py` a npm, cargo y go (OSV.dev los cubre; hoy solo avisa). Spec antes; es/en.

- **29:** idea del punto 24 (OpenAI): guardián que detecte memoria desactualizada. Informe 028: hacerlo dentro de la fusión de higiene de memoria, no como guardián nuevo. Spec antes; es/en.

- **30:** idea del punto 24 (OpenAI): que los avisos de los guardianes digan cómo arreglar el problema, no solo qué falló; revisar los de `textos.py` en es/en. Sin empezar.

- **31:** idea del punto 24 (The Harness Effect): cortar un guardián que falla repetidamente y que `medir.py` dé tokens por tarea terminada. Spec antes; es/en.


- **36:** mejora (idea de ODD, informe `archive/informe-odd-gentle-shell-2026-11-09.md`): usar el «resume test» (¿se puede retomar el trabajo solo con la petición y los cambios del código?) como segundo criterio, junto al contador de 15 ediciones del cierre por bloque y a la regla de «más de 2 archivos» de `spec-antes-de-programar`. Pequeño y reversible. Hacerlo después de ver los resultados del punto 35 (`medir.py --ritual`). Spec antes; es/en. Sin empezar.

- **37:** experimento VMware CERRADO (rondas 1-5, informes en `.brain/archive/informe-*vmware*`). Conclusión: las reglas de seguridad son lo que decide (skill `seguridad-en-sistemas-reales`, arnés 1.30.0); ODD + reglas para tareas puntuales, Cerebro Vivo + reglas para proyectos largos. Falta: (a) repetir la prueba de seguridad contra `vcsim`/`pyvmomi` (necesita el sí de Darwin para instalar Go); (b) arreglar `test_soporte_mac` (fin de línea de Windows); (c) revisar la regla «vcsim» de `AGENTS.md` del aprobador.

## Esperando tu prueba (Darwin)
- **35:** cierre por bloque (spec 033, arnés 1.29.0): el guardián ya no pide la línea de registro hasta 15 archivos editados sin cerrar. Prueba: trabaja en un chat de cerebro-vivo con varias tareas pequeñas y comprueba que no salta el aviso en cada una; al final del bloque, pídele a la IA que cierre. Si falla, dime qué aviso salió. Medir con `python .brain/guardianes/medir.py --ritual` en 2 semanas.
## Acciones tuyas
