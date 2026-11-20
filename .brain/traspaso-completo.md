# Traspaso completo del chat #38 al #39 (2026-11-20)

- **IA que lo escribe:** Claude
- **IA que sigue:** Claude (en otro ordenador)
- **Hora:** 2026-11-20 13:10

## 1. Lo último que pidió Darwin (palabras literales)
- «Yo voy a trabajar en otro ordenador. Tengo que hacer un traspaso out en el proyecto. Y ¿cómo le digo para que se descargue los archivos desde GitHub?»

## 2. Decisiones
- Tomadas: sin rol «curador» (spec 090, 13.4); aprobar es del dueño salvo que lo conceda por ruta (13.5); se registrarán todos los proyectos actuales, cada uno con perfil propio en pestañas (12.4); revisión exhaustiva de la fábrica (sección 15 de la spec 090), hecha por otro chat; el auditor de cierre solo avisa al terminar una spec o encargo, con `auditor.py terminada NNN` / `auditada` (spec 092, aprobada por Darwin).
- Abiertas: orden de fases de la web y «fábrica y chats solo ver estado al principio» (propuestos, falta su sí expreso); qué hacer con cada pieza de la fábrica según el informe.

## 3. Estado de cada punto en curso
- Web local (spec 090): fase 1 hecha (v1.61.0); spec en borrador con secciones 12 a 15, sin aprobar.
- Auditor (spec 092): hecho en v1.61.4, 733 pruebas en verde; **sin probar por Darwin**. Arnés 1.61.4 aplicado en Prominimap (venía de 1.60.15) y YuGiWoW (venía de 1.61.3), con copia de seguridad; sin commitear en esos proyectos.
- Prominimap: la suite completa da 5 fallos (2 de `test_cerebro_indices`, que pasan solos, y 3 del addon: `test_spec013`, `test_spec021`, `test_world_nav`); no se comprobó si fallaban antes. `tests/test_cerebro_indices.py` está modificado a mano y no se pisó.
- Revisión de la fábrica: hecha por otro chat, informe en `.brain/archive/notas-chats/2026-11-18-revision-de-la-fabrica.md` (sin commitear). Spec 089 en pausa.
- Pendientes: 61 (web), 62 (revisión de la fábrica), 63 (probar auditor en Prominimap).

## 4. Sin subir a GitHub
- Commits locales: `5936305`…`e05565c` (v1.61.0 a v1.61.4 y la memoria del 18). 4 sin subir.
- Sin commitear: `.brain/archive/notas-chats/2026-11-18-revision-de-la-fabrica.md` (modificado) y los archivos del traspaso.

## 5. Qué debe probar Darwin
- En Prominimap, tras `actualizar_arnes.py`: cerrar un bloque con código y comprobar que el aviso del auditor ya no vuelve en cada respuesta, solo tras `auditor.py terminada NNN`.

## 6. NO hacer (descartado)
- Rol curador. Subir sin orden. Ejecutar acciones desde la web con texto libre (lista cerrada). Ampliar la fábrica antes de decidir con el informe.

## 7. Lecciones apuntadas en este chat
- Ninguna nueva. Aviso práctico: en esta herramienta, un `\n` escrito dentro de un script en bash se convierte en salto de línea real; para escribir `\n` en un archivo usar `chr(92)+"n"`.
