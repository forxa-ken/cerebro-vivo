# Lecciones: arnes-skills

Formato: problema → causa → regla. Las escribe `lecciones.py` en el momento del hito (spec 026).

- **Al añadir una línea a la skill revisor-de-spec la suite falló: 61 líneas, tope 60** → cada SKILL.md (y .en.md) tiene tope de 60 líneas en las pruebas y la skill ya estaba justo en el límite → **antes de añadir contenido a una skill contar sus líneas (wc -l); si está en 60, fusionar el texto nuevo en una viñeta existente en es y en, y volver a lanzar generar_manifiesto.py y la suite** (2026-11-14)
