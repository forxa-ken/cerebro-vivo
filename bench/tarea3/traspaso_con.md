# Traspaso (chat anterior → este)

**Tarea a medias:** exportar el resumen a JSON (`exportar_json` en `gastos.py`, ya existe un borrador).

**Formato acordado con Darwin (no negociable):**
- Archivo con tres claves, en este orden: `total_centimos`, `por_categoria`, `n_gastos`.
- Los importes van en **céntimos enteros** (12.50 € → 1250), nunca decimales.
- `por_categoria` es un objeto con las categorías en **minúsculas** y sin espacios sobrantes, ordenadas alfabéticamente.
- `exportar_json(gastos, ruta)` recibe la lista de gastos de `leer()`.
- Falta además la opción `--json RUTA` en la línea de comandos.

**Hecho:** borrador de `exportar_json` y su prueba mínima. **Falta:** el formato de arriba, la opción `--json`, y sus pruebas.
