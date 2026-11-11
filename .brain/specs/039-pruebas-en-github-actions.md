# Spec 039: pruebas automáticas en GitHub Actions (punto 22)

- **Estado:** aprobada por Darwin el 2026-11-11 y programada (workflow en Ubuntu y Windows; sin ejecutar en GitHub todavía). Darwin eligió GitHub Actions (no Jenkins) el 2026-11-11.
- **Origen:** punto 22. Hoy las pruebas (`python -m unittest discover tests`) solo corren si alguien las lanza en el PC de Darwin.

## 1. En alcance
- [ ] Un archivo `.github/workflows/pruebas.yml` que, en cada `push` a `main` y en cada pull request, instala Python 3.12 y lanza `python -m unittest discover tests`.
- [ ] Sin dependencias ni claves: el repo es público y las pruebas solo usan la biblioteca estándar. Sin «secrets».
- [ ] Si falla, GitHub marca el commit en rojo y avisa a Darwin por correo (aviso estándar de GitHub, sin configurar nada).
- [ ] Primera ejecución en Ubuntu y, si hace falta, también en Windows (Darwin trabaja en Windows). Las pruebas que dependan del PC de Darwin (rutas `F:\`, fin de línea CRLF, estado de `.brain` local) se arreglan o se marcan como omitidas con motivo, sin esconder fallos reales.
- [ ] Una insignia de estado en el README (opcional; Darwin decide).

## 2. Fuera de alcance
- Guardianes que miran el PC o los chats de Darwin (no tienen sentido en la nube).
- Subir versiones, publicar `gh-pages` o regenerar el manifiesto de forma automática.
- Jenkins.
- Llevar el workflow a los proyectos: es solo de este repo; no entra en `manifiesto.json`.

## 3. Riesgo
- Al estrenarlo pueden salir pruebas rojas que en el PC de Darwin pasan (diferencias de Linux o de la máquina limpia). Es información útil, no un fallo del workflow.
- Los minutos de Actions son gratis en repos públicos; si el repo pasara a privado, hay cuota mensual (comprobar entonces).

## 4. Archivos
`.github/workflows/pruebas.yml`, ajustes puntuales en `tests/` si salen diferencias de entorno, `CAMBIOS.md`. Al ser solo del repo no cambia `VERSION` ni `manifiesto.json` (confirmar con la prueba que vigila el manifiesto).

## 5. Verificación
- La primera ejecución en GitHub se ve en la pestaña Actions en verde; no se da por hecho hasta verla. Requiere subir a GitHub, que solo se hace con orden de Darwin.
- En local: `python -m unittest discover tests` sigue en verde.
