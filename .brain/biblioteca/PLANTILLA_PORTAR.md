# Portar desde NOMBRE_DEL_HERMANO (plantilla; spec 043)

Copia este archivo a donde diga `archivo_portar` en `proyectos_hermanos` de `guardianes.json` (por ejemplo `.brain/portar-NOMBRE.md`). El guardián `hermanos.py` lo lee: **respeta los tres encabezados `##` tal cual**.

## Último portado
- `0000000` (hash de un commit del hermano: solo cuentan los posteriores a este)

## Pendiente
- (nota libre de lo que se sabe que falta; el guardián no usa esta sección: calcula él lo pendiente)

## Hecho
Un commit del hermano deja de salir como pendiente cuando su hash (7 caracteres o más) aparece en esta sección, **también si se decidió no portarlo**.

### `abc1234` · título corto del commit
- **Qué cambia:** (una línea)
- **Adaptar:** (qué hay que cambiar para este proyecto)
- **No portar:** (la parte que no aplica; si es todo el commit, escribe «no aplica» y por qué)
