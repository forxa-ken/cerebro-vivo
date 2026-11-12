# Carta de la ejecutora (spec 035, fase 1)

Versión reducida de las reglas de Cerebro Vivo para la IA que **ejecuta** un encargo (Claude, Codex Luna o Gemini). Se copia o se enlaza desde el `AGENTS.md` (o `CLAUDE.md`) del worktree de la ejecutora. La ejecutora no necesita leer el resto de `.brain/`.

## 1. Qué haces

Haces **un** encargo: el archivo `.brain/fabrica/encargos/NNN-nombre.md` que te indiquen. Léelo entero antes de tocar nada.

```markdown
- Toca solo los "archivos permitidos" del encargo. Ni uno más, aunque parezca lo correcto.
- Haz todos los puntos de la spec que el encargo lista, y solo esos.
- No añadas ni quites requisitos, ni cambies lo pedido "por seguridad" o "por limpieza".
- No instales dependencias nuevas ni abras accesos nuevos.
- No hagas commit, no subas nada a GitHub, no cambies de rama.
- No escribas en `.brain/` salvo tu nota (apartado 3).
```

## 2. Si algo no está claro

Si la spec o el encargo tienen un hueco, o ves un riesgo, **para y dilo**; no rellenes con una suposición. Anótalo en tu nota como «hueco» y la directora lo lleva a Darwin.

## 3. Tu nota al terminar

Al acabar, o al pararte, escribe `.brain/notas-chats/AAAA-MM-DD-HHMM-<nombre>.md` con la plantilla de `PLANTILLA_NOTA_CHAT.md`: tarea, archivos tocados, qué probaste y qué no pudiste probar (dilo con honestidad: «no pude ejecutar X»), y los huecos o dudas.

## 4. Ventana y topes

Trabaja con una ventana de unos 200.000 tokens. Si se llena antes de acabar, para, deja el traspaso en tu nota y la directora abre un chat nuevo con él. Los topes de gasto, de encargos y de fallos están en `.brain/fabrica/carta.md` (no la edites). Si se alcanza uno, para y avisa.

## 5. Qué entregas

El cambio en tus archivos permitidos y la nota. La directora comprobará el diff contra la lista de permitidos y volverá a correr la prueba del encargo; lo que no se ejecutó se dirá como no ejecutado.
