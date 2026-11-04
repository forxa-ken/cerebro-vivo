# Spec 013: que el arnés funcione también en Mac

- **Estado:** hecha y probada en Windows por las pruebas del repo (1.11.0); la parte de Mac sigue sin probar, falta la prueba de Darwin en un Mac
- **Nota al programar:** la revisión no halló nada más propio de Windows: las pruebas y `bench/` usan `sys.executable` y los guardianes ya normalizan rutas. El `.claude/settings.json` de este repo se dejó con `python` (solo cambia lo que escribe el instalador).
- **Fecha:** 2026-11-03

## 1. Objetivo
Hoy el arnés se ha escrito y probado solo en Windows. Los guardianes son Python con la librería estándar, así que casi todo debería valer en Mac, pero nadie lo ha comprobado. Se quiere dejarlo preparado y comprobado para Mac sin romper Windows.

## 2. En alcance
- [ ] **Revisión del código** buscando lo propio de Windows: comando `python` frente a `python3`, `instalar_kit.bat`, `instalar_gui.py` (tkinter), codificación de la consola, rutas con `\`, comandos de shell en pruebas y en `bench/`. Resultado: lista corta de qué hay que cambiar.
- [ ] **Ganchos de Claude Code** (`.claude/settings.json` y el que instala el kit): que llamen a un Python que exista en cada sistema (`python3` en Mac/Linux, `python` en Windows) sin que el dueño toque nada, o que el instalador escriba el comando correcto según el sistema.
- [ ] **Instalador:** equivalente de `instalar_kit.bat` para Mac (`instalar_kit.command`, doble clic), y aviso claro si falta Python o tkinter.
- [ ] **Pruebas:** que `python3 -m unittest discover tests` pase en Mac; las que no valgan en Mac se adaptan o se saltan con motivo (`skipUnless`), no se borran.
- [ ] Manual: sección corta «Usar el arnés en Mac». `VERSION` subida, `CAMBIOS.md`, manifiesto regenerado.

## 3. Fuera de alcance
- Linux (probablemente vale, pero no se promete).
- Cambiar el funcionamiento del método; solo portabilidad.
- Actualizar proyectos o subir a GitHub sin orden de Darwin.

## 4. Riesgos
- **No hay Mac a mano:** todo lo que se cambie solo se puede probar en Windows. La parte de Mac queda **sin probar** hasta que Darwin (o alguien con Mac) corra las pruebas y una instalación. Se dirá así en `CAMBIOS.md`.
- Un cambio en el comando de los ganchos no debe romper los proyectos ya instalados en Windows: el actualizador no pisa lo modificado a mano.

## 5. Plan
1. Revisar el código y listar qué hay de Windows.
2. Ganchos e instalador portables; `.command` para Mac.
3. Adaptar pruebas; manual; versión y manifiesto.
4. Probar en Windows que nada se rompe.

## 6. Verificación
- `python -m unittest discover tests` en verde en Windows.
- **Prueba de Darwin en Mac:** `python3 -m unittest discover tests`; instalar el kit en un proyecto vacío con `instalar_kit.command`; abrir Claude Code y ver que el arranque muestra el resumen.

## 7. Cierre
- [x] Spec aprobada por Darwin antes de programar
- [x] Línea añadida a `.brain/decisions.log`
