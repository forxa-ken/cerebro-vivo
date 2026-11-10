# {{NOMBRE}} — Índice de entrada para {{IA}}

Este archivo (`{{ARCHIVO}}`) es el índice que lee **{{IA}}**. Mismo contenido operativo que los demás índices de entrada del proyecto ({{OTROS}}): si cambia uno, se cambian los demás. Es un índice, no un manual.

---

## Memoria persistente (Cerebro `.brain/`)
{{BLOQUE_IA}}
{{MAPA}}
* **Lecciones:** al resolver un hito (error resuelto, archivo delicado, cambio grande) apuntar la lección en el momento con `/leccion`; el guardián `hitos.py` no deja cerrar sin ella. Leer `.brain/lecciones/` antes de repetir ese trabajo.
* **Chats cortos:** cuando la sesión se alargue, escribir el traspaso y abrir tú el chat nuevo (`{{NOMBRE}} #N`), salvo que `/chat-nuevo no` lo haya apagado. **{{DUENO}} autoriza de forma permanente abrir ese chat nuevo de forma automática** (herramientas `start_session` y `detach_session`), sin pedirle permiso cada vez. Hablarle en lenguaje llano.

## Reglas esenciales
* Idioma de respuesta: **{{IDIOMA}}**, tono técnico y conciso.
* **Alcance estricto:** tocar solo lo que atañe al cambio solicitado; nada de refactors no pedidos.
* **Comando de pruebas tras cada cambio:** `{{PRUEBAS}}`
* Lo irreversible (subir, borrar, gastar, tocar datos reales) se pregunta antes. Lo no probado se dice como no probado.

## Metodología (dos carriles)
1. **SDD** — más de 2 archivos o áreas sensibles (pagos, permisos, datos de usuarios, despliegue): spec en `.brain/specs/NNN-nombre.md` desde `_template.md` y **esperar la aprobación de {{DUENO}}** antes de programar.
2. **Cambio pequeño** — el resto: aplicar, pruebas en verde y una línea en `.brain/decisions.log`.
