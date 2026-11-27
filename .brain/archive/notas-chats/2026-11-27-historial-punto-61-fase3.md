# Historial del punto 61 (spec 090, fase 3), movido de pendientes.md el 2026-11-27

Movido para que `pendientes.md` cupiera bajo su tope de 8 KB al añadir los puntos 65 y 66. Nada se borró.

- **Fase 3, primer tramo (v1.64.0, 2026-11-20):** actualizar e instalar de verdad (simulación previa obligatoria, confirmación, una acción por carpeta).
- **Segundo tramo (v1.65.0):** pestaña Tareas (pruebas, auditor, cerrar tarea) en segundo plano con Parar; revisión aparte del primer tramo hecha y corregida; prueba de uso real sobre una copia hecha por la misma IA (`fabrica/evidencia/090-fase3-uso-real.md`).
- **Auditoría externa (Codex): no apto → corregidos sus 5 hallazgos en v1.65.1** (junction, hijos huérfanos y Parar, simulaciones, riesgo aceptado, Origin).
- **Segunda auditoría (Codex, v1.65.2): corregidos 4 de 6** (hijos en Windows con arranque suspendido, tope de memoria, cerrojo del registro, Origin literal); quedan para cuando haya varias web en un mismo proceso: ligar tareas y simulaciones a la instancia o raíz.
- **Tercera auditoría (v1.65.3): apto con reparos, corregidos.** Límites conocidos en la spec: el instante entre revalidar el guardián y reanudar, y ligar tareas y simulaciones a la instancia.
- **Fase 3 cerrada del todo por Darwin el 2026-11-25 (v1.65.3):** prueba de uso real por otro chat, verde (`fabrica/evidencia/090-fase3-uso-real-2.md`); la simulación de instalar ya avisa de los archivos extra. Queda opcional la prueba por una IA de otra familia.
