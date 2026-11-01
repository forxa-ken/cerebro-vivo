# Spec 003: Medir el coste real (con caché) y recortar el arranque

- **Estado:** implementada y medida (1.3.1); resultados en 003-resultados.md
- **Fecha:** 2026-11-01

## 1. Objetivo
Las specs 001 y 002 compararon «tokens nuevos», una cifra que **cambia según si la caché estaba caliente** y que no refleja lo que de verdad se paga (escribir en caché cuesta más que leer; leer cuesta una décima; la salida cuesta mucho más). Al desglosar un chat mensaje a mensaje se vio que el primer mensaje gasta ~26k nuevos con arnés frente a ~15k sin él, pero los números no son comparables porque las carpetas gemelas no tenían la misma caché. Meta: (1) tener una **cifra de coste justa**; (2) con ella, decidir con datos qué recortar del arranque; (3) recortar solo lo que de verdad pese.

## 2. En alcance
- [ ] **`medir.py`: coste ponderado.** Nueva columna «Coste» = entrada×1 + escritura de caché×1,25 + lectura de caché×0,1 + salida×5 (pesos configurables, en «tokens equivalentes de entrada»). Se muestra junto a «Nuevos», que se deja. Con `--desglose` imprime, para un chat, el coste mensaje a mensaje con las herramientas usadas.
- [ ] **Separar frío y caliente:** `medir.py` marca un chat como «frío» si su primer mensaje no leyó de caché la mayor parte del prefijo (lectura < 50 % del arranque) y compara solo frío con frío y caliente con caliente.
- [ ] **Banco justo:** `montar.py` deja una carpeta por lado y tarea **reutilizada** entre repeticiones y una ejecución de calentamiento antes de medir (no se cuenta), para que las dos partan igual. Se documenta en `bench/tareas.md`.
- [ ] **Desglose del arranque:** medir cuánto pesa cada pieza del arranque CON (CLAUDE.md, lista de skills, ganchos, resumen del arranque, órdenes de leer constitución y pendientes) cambiando una cada vez en una carpeta de prueba.
- [ ] **Recortes con datos:** solo se recorta lo que pese más de ~1k tokens equivalentes, con interruptor en `guardianes.json`. Candidatos: no pedir leer la constitución y los pendientes si el resumen no marca nada; no pedir copiar el resumen si no hay novedades; skills menos verbosas; `CLAUDE.md` más corto.
- [ ] **Re-medición** de T1, T2 y T3 CON (1.3.0) frente a SIN en igualdad de caché: 2 repeticiones calientes por caso (12 ejecuciones aprox. con los calentamientos). Informe `003-resultados.md` con coste ponderado.
- [ ] Pruebas, `VERSION` 1.3.0, `CAMBIOS.md`, manifiesto.

## 3. Fuera de alcance
- No tocar LoboHook ni subir a GitHub; no borrar nada; no quitar el traspaso entre chats (lo que ganó T3).
- No reabrir el modo ligero salvo el hueco de T2 (b): cuando la IA no escribe la línea y el guardián no la ve, se registra igualmente (se trata dentro de esta spec).

## 4. Plan de implementación
1. Coste ponderado, `--desglose` y frío/caliente en `medir.py` (+ pruebas); volver a calcular con los registros ya existentes, sin gastar nada.
2. Informe corto con esa re-lectura de las 12+6 ejecuciones (¿cambia la conclusión?).
3. Desglose de piezas del arranque (ejecuciones cortas de un solo mensaje).
4. Recortes justificados por los datos; arreglo del hueco del registro.
5. Banco justo y re-medición; informe.

## 5. Plan de verificación
- `python -m unittest discover tests` en verde.
- Criterio de éxito: con coste ponderado y caché igualada, CON ≤ +15 % frente a SIN en T1 y T2, y T3 sigue 2/2. Si no se llega, el informe lo dice y propone el siguiente paso en vez de maquillarlo.

## 6. Riesgos dichos de antemano
- Los pesos de precio cambian con el tiempo: son ajustables y se indica la fecha.
- Con la caché de 5 minutos el calentamiento debe ir justo antes; si pasa el tiempo, la ejecución se descarta y se repite.
- Pocas repeticiones: tendencia, no estadística.

## 7. Cierre
- [x] Spec aprobada por Darwin antes de programar
- [x] Línea añadida a `.brain/decisions.log`
