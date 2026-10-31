# {{NOMBRE}} — Índice de entrada para {{IA}}

Este archivo (`{{ARCHIVO}}`) es el índice que lee **{{IA}}**. Mismo contenido operativo que los demás índices de entrada del proyecto ({{OTROS}}): si cambia uno, se cambian los demás. Es un índice, no un manual.

---

## Memoria persistente (Cerebro `.brain/`)
{{BLOQUE_IA}}
{{MAPA}}
* **Chats cortos:** avisar a {{DUENO}} cuando la sesión se alargue y recomendar abrir una nueva (`{{NOMBRE}} #N`). Hablarle en lenguaje llano.

## Reglas esenciales
* Idioma de respuesta: **{{IDIOMA}}**, tono técnico y conciso.
* **Alcance estricto:** tocar solo lo que atañe al cambio solicitado; nada de refactors no pedidos.
* **Comando de pruebas tras cada cambio:** `{{PRUEBAS}}`
* Lo irreversible (subir, borrar, gastar, tocar datos reales) se pregunta antes. Lo no probado se dice como no probado.

## Metodología (dos carriles)
1. **SDD** — más de 2 archivos o áreas sensibles (pagos, permisos, datos de usuarios, despliegue): spec en `.brain/specs/NNN-nombre.md` desde `_template.md` y **esperar la aprobación de {{DUENO}}** antes de programar.
2. **Fast-Track** — el resto: aplicar, pruebas en verde y una línea en `.brain/decisions.log`.
