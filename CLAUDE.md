# cerebro-vivo — Índice de entrada para Claude

Repositorio del **meta-arnés «Cerebro Vivo»**: el método, los guardianes, las skills y los kits que usan los proyectos de Darwin. Cada proyecto (LoboHook es uno más) trae las mejoras con `actualizar_arnes.py`. Es un índice, no un manual.

---

## Memoria persistente (Cerebro `.brain/`)
* **Al iniciar sesión** el resumen de arranque llega solo (hook `SessionStart`); copiarlo al usuario en 4-5 viñetas. Leer `.brain/constitution.md` y `.brain/pendientes.md`.
* **Al terminar cada tarea:** el hook `Stop` avisa si falta la línea en `decisions.log`; cierre rápido: `python .brain/guardianes/cerrar.py --chat "cerebro-vivo #N" "qué se hizo"`.
* **Pendientes:** [`.brain/pendientes.md`](.brain/pendientes.md) (solo lo que falta). **Registro:** [`.brain/decisions.log`](.brain/decisions.log).
* **Reglas innegociables:** [`.brain/constitution.md`](.brain/constitution.md). **Decisiones:** [`.brain/decisions/indice.md`](.brain/decisions/indice.md).
* **Manual del método y de todos los comandos:** [`.brain/biblioteca/CEREBRO_VIVO.md`](.brain/biblioteca/CEREBRO_VIVO.md); carta maestra en `CARTA_META_ARNES.md`.
* **Traspaso entre chats:** si existe `.brain/traspaso.md`, el arranque lo muestra solo; al proponer un chat nuevo se escribe antes (plantilla en `.brain/biblioteca/PLANTILLA_TRASPASO.md`).
* **Notas de chats auxiliares:** el chat que recibe un encargo de otro deja su nota en `.brain/notas-chats/` (plantilla en `.brain/biblioteca/PLANTILLA_NOTA_CHAT.md`).
* **Chats cortos:** cuando la sesión se alargue, escribir el traspaso y abrir el chat nuevo yo mismo (`/chat-nuevo` lo activa o apaga). Hablarle en lenguaje llano.

## Cómo se reparte el arnés
* Lo que llega a los proyectos está listado en **`manifiesto.json`** (huella de cada archivo) con la versión de **`VERSION`**. Tras cambiar cualquier archivo del arnés: subir `VERSION`, anotar en `CAMBIOS.md` y lanzar `python generar_manifiesto.py` (una prueba falla si se olvida). **El ZIP de Mac está en pausa:** solo se regenera si Darwin lo pide, con `python generar_zip_mac.py`.
* Un proyecto se actualiza con `python .brain/guardianes/actualizar_arnes.py --simular` (y luego sin `--simular`), o desde aquí con `python actualizar.py RUTA --simular`. No pisa lo modificado a mano ni toca datos ni configuración.
* Esto es el origen único: nada de LoboHook ni de otro proyecto entra aquí (lo vigila `tests/test_arnes_repo.py`).

## Reglas esenciales
* Idioma de respuesta: **español**, tono técnico y conciso. **Alcance estricto:** solo lo que atañe al cambio pedido.
* **Pruebas tras cada cambio:** `python -m unittest discover tests`
* Lo irreversible (subir a GitHub, borrar, gastar) se pregunta antes. **No subir a GitHub sin orden de Darwin**, salvo el commit de memoria de `traspaso-out salgo`. Lo no probado se dice como no probado.
