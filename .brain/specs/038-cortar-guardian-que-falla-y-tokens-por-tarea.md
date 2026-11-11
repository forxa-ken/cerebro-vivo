# Spec 038: cortar un guardián que falla repetido y medir tokens por tarea terminada (punto 31)

- **Estado:** borrador (2026-11-11), a aprobar por Darwin antes de programar
- **Origen:** idea del punto 24 (The Harness Effect). Dos mejoras separadas, programables por separado.

## 1. En alcance
### 1A. Cortar un guardián que falla repetido
- [ ] Contar, por guardián, cuántas veces seguidas su aviso se ignoró o dio error (estado en un JSON junto a los demás `*_estado.json`).
- [ ] Con `guardian_fallos_max` fallos seguidos (por defecto 3) ese guardián se silencia durante el chat y el resumen de arranque lo dice una vez: «el guardián X se apagó por fallar N veces». Nunca se apaga el de secretos ni el cierre (los de seguridad).
- [ ] Se reactiva con un comando o al pasar un día; textos es/en.
### 1B. `medir.py`: tokens por tarea terminada
- [ ] Definir «tarea terminada» = línea nueva en `decisions.log` (spec 033: un bloque cerrado).
- [ ] `medir.py` muestra tokens (entrada+salida) entre cierres y su media por tarea; también en `--comparar`.

## 2. Fuera de alcance
- Cambiar los avisos existentes (punto 30 ya hecho) o los umbrales de los otros guardianes.
- Medir calidad de las tareas: solo coste.

## 3. Riesgo
Apagar un guardián útil por error. Por eso: solo avisos informativos, nunca los de seguridad, siempre visible en el arranque y reversible.

## 4. Archivos
`cierre.py` y los guardianes que registren avisos, `medir.py`, `textos.py`, `guardianes.json`, `tests/`, `VERSION`, `CAMBIOS.md`, `manifiesto.json`.

## 5. Verificación
`python -m unittest discover tests` en verde; medir un chat real con `medir.py` (no probada hasta hacerla).
