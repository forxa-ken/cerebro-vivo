# Spec 008: migración del objetivo en proyectos ya instalados

- **Estado:** hecha y probada (1.6.0)
- **Fecha:** 2026-11-01

## 1. Objetivo
Un proyecto ya empezado no recibe con `actualizar_arnes.py` el `objetivo.md`, su enlace en los índices ni la regla 10 de la constitución (spec 007), porque son archivos del proyecto. Se añade una opción que lo hace sin pisar nada.

## 2. En alcance
- [ ] `actualizar_arnes.py --migrar-objetivo` (con `--simular` para ver antes): crea `.brain/architecture/objetivo.md` si falta; añade el enlace al objetivo como primer punto de la lista de memoria de cada índice de entrada que exista (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`) si no lo tiene; añade la regla 10 a `constitution.md` si no está.
- [ ] Idempotente: ejecutarlo dos veces no cambia nada la segunda. Copia de seguridad en `.brain/copias_arnes/` de lo que modifique.
- [ ] Si no encuentra el sitio donde insertar (archivo muy cambiado a mano), no toca ese archivo y lo avisa con la línea exacta que hay que pegar.
- [ ] Pruebas, `VERSION` 1.6.0, `CAMBIOS.md`, manifiesto, y quitar el aviso de «a mano» de `GUIA_INSTALACION.md` (paso 3).

## 3. Fuera de alcance
- No reescribir el contenido de los índices ni de la constitución más allá de esas líneas.
- No rellenar `objetivo.md` con un objetivo inventado (queda con «pendiente de escribir»).
- No migrar proyectos desde aquí ni subir a GitHub sin orden.

## 4. Plan
1. Función de migración en `actualizar_arnes.py` reutilizando la copia de seguridad existente.
2. Opción de línea de comandos e informe.
3. Pruebas: proyecto sin objetivo, con índices modificados, idempotencia, simulación sin escribir.
4. Versión, cambios, manifiesto, guía.

## 5. Verificación
- `python -m unittest discover tests` en verde.
- **Prueba de Darwin:** `--migrar-objetivo --simular` en un proyecto ya instalado (p. ej. con Codex), revisar el informe, aplicarlo y preguntarle el objetivo a un chat nuevo de Codex.

## 6. Cierre
- [x] Spec aprobada por Darwin antes de programar
- [ ] Línea en `.brain/decisions.log`
