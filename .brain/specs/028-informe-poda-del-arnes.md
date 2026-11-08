# Spec 028: informe de poda del arnés (qué sobra, qué mejorar, qué eliminar)

- **Estado:** informe con propuestas; **nada se ha tocado**. Cada recorte necesita el visto bueno de Darwin.
- **Fecha:** 2026-11-08 · arnés 1.27.0
- **Qué se miró:** este repo (código, skills, documentos, registro, informes de las specs 001-004). **No** se miraron LoboHook ni los demás proyectos: lo que allí se use o no se use no consta aquí.

## 0. Hechos medidos (de los informes del propio repo)
- El arnés **no ahorra tokens en tareas pequeñas**: +35 % (caché fría) y +92 % (caliente) frente a trabajar sin él (spec 003). La diferencia viene sobre todo del número de mensajes de la IA, no del peso del arnés (~2-3k de arranque).
- Donde **sí** gana: retomar un trabajo a medias con traspaso (T3: 2/2 frente a 0/2 sin arnés). Es el único resultado favorable medido, y la prueba la diseñamos nosotros.
- Los **índices de fichas no ayudaron** a 80 fichas: mismo acierto (10/10) y 19 % más caros (spec 004). Un solo proyecto, 2 repeticiones.
- Nadie ha medido todavía el arnés en un proyecto real durante semanas (punto 4 de pendientes, sin hacer). **Es la pregunta que decide todo lo demás.**
- Todo el arnés tiene 9 días (146 de 148 líneas del registro son de noviembre): ~20 guardianes, 29 skills, 351 pruebas, ~5.000 líneas de guardianes, ~130 KB de documentos.

## 1. Candidatos a ELIMINAR o dejar de repartir (propuesta)
| Qué | Por qué | Confianza |
|---|---|---|
| `base_datos.py` (257 líneas) y `analisis.py` (210) | Apagados por defecto, nacieron para un proyecto concreto (LoboHook), 0 menciones en el registro. Pasan a ser un extra opcional fuera del reparto general. | Media (no sé si LoboHook los usa) |
| Documentos de instalación solapados: `README.md`, `MANUAL_DE_USO.md` (+ `.en`), `CONTEXTO_PARA_OTRA_CUENTA.md`, `guia_instalacion_skills_cerebro_vivo.md`, `biblioteca/GUIA_INSTALACION.md` | Cinco textos que explican casi lo mismo (~43 KB). Dejar uno por público (usar / instalar) y borrar el resto. | Alta en el solape; hay que leerlos para decidir cuál queda |
| Puntos 22 (Jenkins/GitHub), 23 (agente revisor), 19 (varias IA), 25 (jerga) de pendientes | Ideas sin empezar y sin un problema vivido detrás. Archivar en `archive/` («mover, no borrar») hasta que duelan. | Alta |
| Skills de una sola regla que ya están en la constitución: `mover-no-borrar`, `implementada-no-es-hecha`, `explicar-a-darwin-en-llano`, `pendientes-solo-lo-que-falta`, `cero-dependencias`, `licencia-antes-de-usar`, `quitar-codigo-antiguo-con-test` | Cada skill añade su descripción al listado de **todas** las sesiones. Si la regla ya está en la constitución, la skill duplica. Comprobar cuáles ya están allí antes de quitar. | Media |

## 2. Candidatos a FUSIONAR o simplificar
- **Higiene de memoria repartida en 5 piezas** (`poda.py`, `archivos_gordos.py`, `revisar_indices.py` con 382 líneas, `indices.py`, skill `trocea`/`acorta`): todas vigilan tamaño y orden de `.brain/`. Fusionar en una sola. **Importante:** el punto 29 («jardinero de documentación») sería la sexta; hacerlo como parte de esa fusión, no como guardián nuevo.
- **Índices de fichas** (`indices.py`, `hechos-indice.md`): la spec 004 no los justifica a 80 fichas. Propuesta: mantenerlos solo cuando un proyecto pase de ~150 fichas; no exigirlos por defecto.
- **Una skill por comando de traspaso/chat** (`traspaso-in`, `traspaso-out`, `memoria-traspaso`, `chat-nuevo`, `longitud.py`, `guardar_traspaso.py`): hacen una sola función repartida en 6 sitios.
- **Textos duplicados es/en**: es la regla de Darwin y se mantiene, pero cada guardián nuevo cuesta el doble. Razón de más para no crear guardianes nuevos.

## 3. Defectos reales a MEJORAR
1. **[ARREGLADO en 1.27.1] El actualizador no instalaba los hooks.** `/actualizar` trae los archivos pero no toca `.claude/settings.json`; un guardián nuevo (como el de la 027) no se activa hasta volver a lanzar el instalador. Es el hueco más serio: el arnés se reparte «a medias».
2. **Los contadores «Veces: N» de las skills son 0 en 28 de 29**, aunque hoy se usó `traspaso-in`. O no se actualizan o no sirven: arreglarlos (para poder podar con datos) o quitarlos.
3. **[ARREGLADO en 1.27.1] El hook nuevo corría en cada orden de terminal y cada edición** (~0,16 s cada vez). Solo `Bash`/`PowerShell` hacen falta; `Edit|Write|MultiEdit` se añadieron solo para la base de `requirements.txt` y no compensan. Propuesta: quitarlos.
4. **8 puntos «esperando tu prueba» sin probar** (algunos desde el arnés 1.9.0). Dos caminos: convertir en pruebas automáticas lo que se pueda (14, 21, 26 son comprobables sin ti) y dejarte solo lo que exige tu mirada (17 Mac, 20/27 chat nuevo).
5. **Lecciones repetidas:** 2 de las 4 lecciones son el mismo error (escribir código con scripts/heredoc y escapes). Subirlo a regla de la constitución.
6. **Pendientes en 7,7 de 8 KB** y con líneas muy largas: acortar cada punto a 1-2 líneas y mover el detalle a su spec.
7. **Informe 003 pendiente de cumplir:** recortar el ritual de arranque y de cierre en tareas pequeñas. Se propuso el 2026-11-01 y los criterios de éxito (≤ +15 %) nunca se cumplieron.

## 4. Lo que se mantiene (tiene evidencia o es base)
`.brain/` + traspaso + cierre con registro (es lo que ganó T3), `secretos.py`, `librerias.py` + `eventos_chat.py`, `actualizar_arnes.py`, `medir.py` y `bench/` (son los que permiten decidir con datos), pruebas, bilingüe.

## 5. Orden propuesto
1. Arreglar el actualizador de hooks (3.1) y quitar `Edit|Write` del hook nuevo (3.3). Son defectos, no recortes.
2. **Medir en un proyecto real** con `medir.py` durante 2-3 semanas (punto 4). Sin esto, todo lo demás es opinión.
3. Mientras tanto, **congelar guardianes nuevos** (puntos 29, 30, 31, 32 en espera) y probar los 8 puntos pendientes.
4. Con las cifras: decidir los recortes de la sección 1 y 2, de uno en uno, con spec corta y «mover, no borrar».

## 6. Lo que no sé
- Qué guardianes y skills usan de verdad LoboHook y los otros proyectos (puede que `base_datos.py` sea esencial allí).
- Si el sobrecoste de tokens importa en tu plan de uso, o si pesa más la fiabilidad del traspaso.
- Cuántas de las skills se invocan solas por la descripción (el contador falla, ver 3.2).
