# Traspaso completo del chat #40 al #41 (2026-11-18)

- **IA que lo escribe:** Claude
- **IA que sigue:** (por decidir)
- **Hora:** 2026-11-18

## 1. Lo último que pidió Darwin (palabras literales)
- «/traspaso salgo». Antes: «Sí, aprobada» (spec 091), «Confirma los cambios del árbol de trabajo con un mensaje razonable», «pasale la informacion a cerebro vivo 38».

## 2. Decisiones
- Tomadas: spec 091 aprobada con dos propuestas: el gasto de la directora solo se muestra (no cuenta en los topes salvo que la carta nombre `directora` en `topes_papeles`); `cerrar-encargo` nunca acepta el encargo. Commit único con todo el árbol (incluidos cambios de otros chats).
- Abiertas: si el gasto de la directora va también en el informe final (hoy no se tocó el validador del informe).

## 3. Estado de cada punto en curso
- Spec 091 (`.brain/specs/091-...md`): aprobada y programada como v1.61.3. 724 pruebas OK. Sin probar en un encargo real.
- `medir.gasto_directora_entre` (ventana de tiempo, sin caché) y `fabrica.cerrar_encargo` (alcance, pruebas por `comando_pruebas` de la carta, gasto de la directora, avance; evidencia en `evidencia/cerrar-encargo-N.md`; sin `comando_pruebas` sale rojo). `foto` guarda `hora`. Skill directora-de-fabrica es/en con el atajo.
- Chat #38 avisado por mensaje de lo ocurrido.

## 4. Sin subir a GitHub
- Commit local `d5712ae`. Sin commitear: `decisions.log` (línea del #40), nota archivada de la revisión (cambio menor del arranque) y estos traspasos.

## 5. Qué debe probar Darwin
- Cerrar un encargo real con `python .brain/guardianes/fabrica.py cerrar-encargo ENCARGO.md --encargo N` y revisar el resumen y `evidencia/cerrar-encargo-N.md`.

## 6. NO hacer (descartado)
- Programar pasos 3 a 5 del esquema (roles.json, perfil.json, skills neutras, web) sin otra spec. Tocar spec 089, Prominimap, spec 090 o pendientes.md desde aquí.

## 7. Lecciones apuntadas en este chat
- Ninguna nueva. Nota técnica: escribir tests con `\n` mediante heredoc de Python rompe los escapes; usar chr(92)/chr(10) o editar con Edit.
