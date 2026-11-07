---
name: actualizar
description: Use when Darwin types /actualizar or the arranque says there is a new arnés version available for this project.
---

# /actualizar — traer la versión nueva del arnés a este proyecto

Hace todo el proceso sin que Darwin escriba comandos. El actualizador guarda copia de seguridad, no pisa lo modificado a mano y no toca datos (pendientes, specs, decisiones, registro).

## Cómo (pasos)
1. Simular: `python .brain/guardianes/actualizar_arnes.py --simular`. Contar a Darwin en 3-4 viñetas llanas: de qué versión a cuál, qué trae de nuevo (mirar `CAMBIOS.md` del repo del arnés, solo las versiones nuevas), cuántos archivos cambian, qué se retira y si hay alguno modificado a mano. Si dice «No se copia nada» (nivel ligero o medio), contárselo a Darwin y parar.
2. Pedir su sí. Si hay archivos modificados a mano (`!`), decir cuáles son y que NO se pisarán salvo que él lo pida; lo retirado sin modificar pasa a la copia de seguridad.
3. Con el sí: `python .brain/guardianes/actualizar_arnes.py`. Añade solo las claves de configuración que falten, anota `arnes_repo` y completa las fichas de skills de `.brain/experiencia/indice.md`. Si el actualizador que corrió era anterior a 1.19.0, lanzarlo otra vez para que aplique los retirados.
4. Si las pruebas del método salen rojas, NO seguir: decir cuáles y la ruta de la copia de seguridad (`.brain/copias_arnes/`). Un fallo de una prueba que ya fallaba antes (guardianes propios del proyecto) se explica, no se oculta.
5. Reiniciar Claude Code si cambió `.claude/settings.json`. Cerrar con la línea en el registro.

## Error que evita (caso real)
- Actualizar a mano con comandos largos (un proyecto llegó a llevar 9 versiones de retraso) y olvidar los pasos de después: la ficha de skills y las claves nuevas, que dejaban pruebas en rojo.

## Dónde está en el repo
- `.brain/guardianes/actualizar_arnes.py` (`version_disponible`, `completar_configuracion`, `completar_fichas_skills`), specs 019 y 021

## Fuente
- spec 019 (petición de Darwin, 2026-11-04)

## Usada
- Veces: 0 · Última: — (creada el 2026-11-04)
