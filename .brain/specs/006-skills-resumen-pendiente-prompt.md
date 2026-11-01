# Spec 006: Separar /resumen, /pendiente y /prompt-inicial

- **Estado:** hecha y probada (1.4.2)
- **Fecha:** 2026-11-01

## 1. Objetivo
Hoy `/prompt-inicial` mezcla escribir un encargo con ver el estado del proyecto; en un proyecto ya empezado soltó el resumen en vez de la plantilla. Se separa en tres comandos, cada uno con un solo trabajo.

## 2. En alcance
- [ ] **`/prompt-inicial`:** vuelve a ser solo la plantilla para escribir un encargo (tipo y modo, campos opcionales, avisos sin bloquear, armar el prompt y esperar visto bueno). Se quita el paso que mira el estado y ofrece opciones.
- [ ] **`/resumen` (skill nueva):** solo lee y cuenta el estado en 4-5 viñetas llanas. Lee `pendientes.md` y la última línea de `decisions.log`; no escribe nada.
- [ ] **`/pendiente` (skill nueva):** con nombre (`/pendiente programar`) muestra esa lista; sin nombre, menú con Falta programar, Esperando tu prueba, Acciones tuyas y Specs abiertas.
- [ ] Entradas nuevas en el índice de experiencia, `CEREBRO_VIVO.md`, `MANUAL_DE_USO.md` y `README.md`.
- [ ] `VERSION` 1.4.2, `CAMBIOS.md`, `python generar_manifiesto.py`, prueba del actualizador para las dos skills nuevas.

## 3. Fuera de alcance
- Skills en `.agents/skills/` para Codex (pendiente 7): va aparte; hasta entonces `/resumen` y `/pendiente` solo en Claude Code.
- No tocar el traspaso (`traspaso-entre-chats`) ni el aviso de arranque.
- No subir a GitHub sin orden de Darwin.

## 4. Plan
1. Editar `prompt-inicial/SKILL.md`.
2. Crear `resumen/SKILL.md` y `pendiente/SKILL.md` con el formato de las demás skills.
3. Actualizar documentos, índice, `VERSION`, `CAMBIOS.md` y manifiesto.
4. Añadir la prueba y lanzar `python -m unittest discover tests`.

## 5. Verificación
- Pruebas en verde.
- **Prueba de Darwin:** en un chat nuevo, escribir `/resumen`, `/pendiente` y `/prompt-inicial`; el primero cuenta, el segundo muestra menú, el tercero enseña la plantilla.

## 6. Cierre
- [x] Spec aprobada por Darwin antes de programar
- [ ] Línea en `.brain/decisions.log`
