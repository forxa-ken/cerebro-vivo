# Cambios del arnés

Una línea por versión. Subir `VERSION`, anotar aquí y lanzar `python generar_manifiesto.py` antes de dar por buena una mejora.

## 1.0.0 (2026-10-31)
- Primer repositorio propio del meta-arnés (spec 087 de LoboHook). Trae todo lo hecho hasta hoy: guardianes (incluido el **modo auto**, `cerrar.py --indices/--hecho`, `indices.py`, `notas_abiertas.py`), manual `CEREBRO_VIVO.md` y carta, plantillas, kit de arranque y de traducción, skills genéricas (con `/prompt-inicial`), pruebas del método y el plugin `plantilla-prompt` 0.2.0 (`/plantilla`).
- Nuevo: `actualizar_arnes.py` (en cada proyecto) y `actualizar.py` (en este repo) para traer las mejoras sin pisar lo modificado a mano.
