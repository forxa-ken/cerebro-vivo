# Spec 015: instalar el kit en un proyecto que ya tiene Claude (fusión sin pisar)

- **Estado:** implementada en 1.13.0 y probada con las pruebas del repo (Windows); falta probarla en un proyecto real (p. ej. Guild Control Forever)
- **Fecha:** 2026-11-04
- **Nota de número:** la 014 queda reservada para el «aviso de versión nueva», que aún no está escrita.

## 1. Objetivo
Hoy `instalar.py` nunca pisa un archivo que ya existe. En un proyecto que ya trae `CLAUDE.md` (o `GEMINI.md`, `AGENTS.md`) o `.claude/settings.json`, eso deja el kit a medias: la IA no ve el índice de memoria y los avisos automáticos no se activan. Del `CLAUDE.md` avisa; del `settings.json` calla. Se quiere que el instalador **añada lo suyo sin quitar nada de lo del proyecto**, y que avise siempre de lo que no pudo hacer.

## 2. En alcance
- [x] **Índices de IA ya existentes** (`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`): se añade **al final** un bloque delimitado por `<!-- cerebro-vivo:inicio -->` y `<!-- cerebro-vivo:fin -->` con las líneas de memoria que hoy lleva el índice del kit (bloque de la IA + mapa). No se toca ni una línea anterior. Si el bloque ya está, no se repite (instalar dos veces da lo mismo que una).
- [x] **Adoptar el contenido existente (nada se pierde):** el script no entiende textos, así que lo hace en dos tiempos.
  1. *Mecánico (instalador):* guarda una copia **íntegra** del índice original en `.brain/archive/adoptado/CLAUDE.original.md` (igual para GEMINI/AGENTS) y deja en `.brain/pendientes.md` una tarea «Adaptar lo que ya tenía el proyecto». El `CLAUDE.md` conserva todo su texto más el bloque nuevo.
  2. *Inteligente (la IA, en el primer chat tras instalar):* lee la copia original y reparte lo que contiene en su sitio: objetivo y descripción → `architecture/objetivo.md`; reglas y prohibiciones → `constitution.md`; decisiones con su porqué → `decisions/`; mapa de archivos y comandos → `referencias.md`; tareas abiertas → `pendientes.md`. Después acorta `CLAUDE.md` a índice **solo si Darwin lo aprueba** viendo antes qué fue a dónde; lo que no encaje se deja en `referencias.md` tal cual, nunca se descarta. La copia original se conserva siempre (mover, no borrar).
  - Skill nueva `adoptar-indice-existente` con esos pasos, para que cualquier IA los siga igual.
- [x] **`.claude/settings.json` ya existente:** se lee y se **fusiona**:
  - `hooks`: por cada evento (`SessionStart`, `Stop`, `UserPromptSubmit`) se añade la entrada del kit solo si no hay ya un comando que llame a ese guardián. Los hooks propios del proyecto se conservan tal cual.
  - `permissions.deny`: unión de listas, sin duplicar.
  - Cualquier otra clave (`env`, `model`, `allow`…) queda intacta.
  - Si el JSON está roto o no es un objeto, **no se toca** y se avisa con las líneas exactas para pegar a mano.
- [x] **Copia de seguridad:** antes de modificar un archivo existente se guarda `NOMBRE.antes-de-cerebro-vivo` al lado (una sola vez; si ya existe esa copia, no se sobrescribe).
- [x] **Simulación (`simular`):** cuenta y lista lo que se fusionaría, sin escribir nada. El resumen distingue «creados», «fusionados» y «respetados».
- [x] **Avisos claros** en el resultado (y en la ventana `instalar_gui.py`): qué archivos se fusionaron y que hay que reiniciar Claude Code para que cuenten los hooks nuevos.
- [x] **Pruebas** en `tests/test_kit_arranque.py`: índice existente recibe el bloque y conserva su texto; segunda instalación no duplica; `settings.json` con hooks propios conserva los propios y añade los del kit; JSON roto no se toca y avisa; `simular` no escribe; copia de seguridad creada una sola vez.
- [x] `VERSION` a 1.13.0, línea en `CAMBIOS.md`, manifiesto regenerado, nota en el manual.

## 3. Fuera de alcance
- Reescribir el `CLAUDE.md` del proyecto sin que Darwin vea y apruebe el reparto (el instalador solo añade; el reparto lo propone la IA).
- Fusionar `.gitignore` (ya añade líneas sin borrar) ni el hook `pre-commit` de Git (ya avisa si hay otro).
- Detectar conflictos de significado (p. ej. un `CLAUDE.md` que contradiga el método): solo se añade el bloque.
- Actualizar proyectos o subir a GitHub sin orden de Darwin.

## 4. Riesgos
- Si el proyecto ya tenía un hook `Stop` con otro propósito, ahora corren los dos; el orden no está garantizado. Se avisa en el resultado.
- Quitar el kit de un proyecto fusionado: los marcadores `cerebro-vivo:inicio/fin` permiten borrar el bloque a mano; los hooks se reconocen por el nombre del guardián.
- Probado solo en Windows (el entorno actual); la lógica es JSON y texto, sin rutas especiales.

## 5. Plan
1. Función `fusionar_indice(ruta, bloque, hechos)` y `fusionar_ajustes(ruta, nuevos, hechos)` en `instalar.py`; `escribir_sin_pisar` sigue igual para el resto.
2. Usarlas en los puntos donde hoy se llama a `poner(archivo…)` y `poner(".claude/settings.json"…)`; retirar el aviso viejo de «no se tocó».
3. Pruebas; versión, cambios, manifiesto, manual.
4. Ejecutar `python -m unittest discover tests` completo.

## 6. Cierre
- [x] Spec aprobada por Darwin antes de programar
- [x] Pruebas en verde
- [x] Línea añadida a `.brain/decisions.log`
