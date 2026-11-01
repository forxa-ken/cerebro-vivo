# Spec 002: Modo ligero para tareas pequeñas

- **Estado:** aprobada (Darwin, 2026-11-01); implementada (1.2.0 + texto de CLAUDE.md 1.2.1); medición parcial: funciona pero no ahorra, ver 002-resultados.md
- **Fecha:** 2026-11-01

## 1. Objetivo
La prueba de la spec 001 mostró que, en tareas pequeñas, el arnés gasta entre un 17 % y un 43 % más de tokens nuevos que no usarlo, aunque logra lo mismo. Parte de ese coste es el cierre: el guardián `cierre.py` **obliga a la IA a dar otra vuelta** (aviso con código 2) para escribir la línea del registro. Meta: que una tarea pequeña no cueste esa vuelta extra, sin perder el registro ni la memoria. **Criterio de éxito:** CON arnés ≤ +10 % de tokens nuevos frente a SIN en T1 y T2, y T3 sigue 2/2.

## 2. En alcance
- [ ] **Cierre ligero en `cierre.py`:** si en la respuesta se tocaron como mucho `max_archivos` archivos (por defecto 2), ninguno es «sensible» (pagos, permisos, base de datos, despliegue, secretos: lista en `guardianes.json`) y no se tocó nada de `.brain/`, el propio guardián escribe una línea automática en `decisions.log` («(auto) tocó X, Y») y **no bloquea**: cero tokens de la IA. Si no se cumple, todo sigue como hoy (aviso y línea escrita por la IA).
- [ ] Ajustes nuevos en `guardianes.json`: `modo_ligero_activo` (true), `modo_ligero.max_archivos`, `modo_ligero.sensibles`. Se puede apagar.
- [ ] **Cierre exige verde (mejora 2 de la spec 001):** en el cierre normal, el aviso recuerda que la línea se escribe solo con las pruebas en verde, y la línea automática solo se escribe si el último comando de pruebas de la respuesta salió bien (si no se puede saber, no escribe y avisa como hoy).
- [ ] **Arranque más corto:** el resumen del arranque omite las líneas «sin novedad» (p. ej. secretos sin avisos) y se queda en lo que requiere acción; la instrucción de copiárselo a Darwin se mantiene en una sola línea.
- [ ] Pruebas nuevas (cierre ligero activo/inactivo, archivo sensible, 3 archivos, verde/rojo, línea automática marcada) y que las existentes sigan en verde.
- [ ] Subir `VERSION` a 1.2.0, `CAMBIOS.md`, manifiesto y manual `CEREBRO_VIVO.md` (una nota breve del modo ligero).

## 3. Fuera de alcance
- No tocar `CLAUDE.md` plantilla, `modo_auto`, poda ni los demás guardianes.
- No tocar LoboHook ni adoptarlo allí; no subir a GitHub; no borrar nada.
- No cambiar el comportamiento del traspaso entre chats (es lo que ganó T3).

## 4. Plan de implementación
1. Ampliar `cierre.py` (`evaluar` sigue siendo función pura; la escritura de la línea va en `main`).
2. Ajustes en `guardianes.json` (neutros) y `arranque.py` (resumen más corto).
3. Pruebas; subir versión; manifiesto.
4. **Medición:** repetir con el arnés 1.2.0 el lado CON de T1 y T2 (2 repeticiones cada una) y T3 (2 repeticiones): 6 ejecuciones. Se reutiliza el lado SIN ya medido (mismo modelo y esfuerzo). Informe en `.brain/specs/002-resultados.md`.

## 5. Plan de verificación
- `python -m unittest discover tests` en verde.
- Criterio de éxito de la sección 1.

## 6. Riesgos dichos de antemano
- La línea automática es menos informativa que la de la IA: se marca «(auto)». Si Darwin la echa de menos, se puede subir `max_archivos` a 0 (apaga el modo).
- Una tarea de 1 archivo puede ser importante; por eso existe la lista de sensibles.
- 2 repeticiones por caso: tendencia, no estadística.

## 7. Cierre
- [x] Spec aprobada por Darwin antes de programar
- [ ] Línea añadida a `.brain/decisions.log`
