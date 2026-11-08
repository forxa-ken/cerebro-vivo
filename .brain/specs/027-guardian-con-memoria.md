# Spec 027: guardián con memoria del chat (revisa solo las librerías nuevas antes de subir)

- **Estado:** aprobada por Darwin el 2026-11-08 y programada en 1.27.0 (con aviso recordado si falla la red)
- **Fecha:** 2026-11-08
- **Versión prevista:** arnés 1.27.0
- **Origen de la idea:** punto 28 de pendientes, sacado de la investigación del punto 24: el blog de Databricks «Introducing Omnigent» propone políticas con estado, que recuerdan lo ocurrido antes en la sesión (ejemplo del texto: tras descargar un paquete, pedir aprobación humana antes de `git push`). La idea se adapta aquí; no se copia código ni texto.
- **Regla de Darwin (2026-11-08):** el proceso lo hace el guardián solo, de forma automática; no depende de que la IA lo haga ni de que Darwin se acuerde.

## 1. Objetivo
Hoy cada guardián mira una cosa por separado y la revisión de librerías (`librerias.py`) se lanza a mano. Nadie recuerda que **en este chat** se instaló una librería nueva. Este guardián lo recuerda y, justo antes de `git push`, **hace él mismo la revisión** y decide: si está limpio, deja pasar sin molestar; si hay un problema conocido, para el `git push` y lo explica en llano.

## 2. En alcance
- [ ] Hook `PreToolUse` sobre la herramienta de terminal que mira el comando antes de ejecutarlo. Sin intervención de la IA ni de Darwin.
- [ ] **Qué recuerda** (por chat, en un archivo de estado local ignorado por Git, como `longitud_estado.json`): instalaciones de librerías (`pip install`, `npm install`/`add`, `yarn add`, `pnpm add`, `uv add`, `poetry add`, `cargo add`, `go get`) y cambios en archivos de dependencias.
- [ ] **Qué hace al ver `git push` con instalaciones sin revisar**, solo y en este orden:
  1. Lanza la revisión de `librerias.py` (vulnerabilidades conocidas en OSV.dev y versión mayor nueva en PyPI) sobre lo instalado.
  2. **Limpio:** anota «revisado» y deja pasar el `git push` sin avisar (como mucho una línea informativa).
  3. **Vulnerabilidad conocida:** detiene el `git push` (exit 2) con un mensaje en llano: qué librería, qué problema y qué versión lo corrige. Para seguir, Darwin debe decirlo en el chat y la IA anota `eventos_chat.py permitir "motivo"` (queda en el registro; vale solo para esas librerías).
  4. **Sin red o error al revisar:** no bloquea (el hook nunca debe romper el trabajo); avisa una vez de que no pudo revisar.
- [ ] **Límite honesto:** hoy `librerias.py` solo revisa Python (`requirements.txt`). Si lo instalado es de otro ecosistema (npm, cargo, go), el guardián no puede revisarlo solo: avisa una vez de que no se revisó automáticamente. Ampliar `librerias.py` a esos ecosistemas es trabajo aparte.
- [ ] Ajustes en `guardianes.json`: `eventos_chat_activo` (por defecto sí), `eventos_chat_comandos` (lista editable de comandos de instalación), `eventos_chat_bloquear` (por defecto sí; con `false` solo avisa).
- [ ] Textos del aviso, de la ayuda `--help` y de los mensajes en `textos.py` **en español e inglés**, y prueba de paridad.
- [ ] El instalador y el actualizador añaden el hook y los ajustes.

## 3. Fuera de alcance
- Presupuestos de gasto por sesión y políticas declarativas en un archivo (otras ideas de la misma fuente).
- Revisión automática de npm, cargo y go (ver el límite de arriba).
- Otros eventos con memoria (permisos, descargas): se añadirán si este funciona.
- El ZIP de Mac.

## 4. Plan
1. `eventos_chat.py` (guardián): detección de instalaciones y de `git push`, estado por chat, revisión automática con `librerias.chequear`, comando `permitir`; con pruebas (instala y sube limpio → pasa en silencio; instala y sube con vulnerabilidad simulada → para; sin red → no bloquea; push sin instalación → calla; ecosistema no revisable → avisa una vez; error → deja pasar).
2. Enganche en `.claude/settings.json` (hook `PreToolUse`), en `kit-arranque` (`ajustes_neutros.json`, `instalar.py`) y reparto por el actualizador.
3. Textos es/en en `textos.py`, ayuda `--help` en es/en y nota en `CEREBRO_VIVO.md` y `CEREBRO_VIVO.en.md`.
4. Versión 1.27.0, `CAMBIOS.md`, manifiesto; comprobar el modo inglés en una carpeta temporal.

## 5. Verificación
- `python -m unittest discover tests` en verde, con pruebas nuevas del guardián y de la paridad es/en (la red se simula, sin llamadas reales).
- Proyecto de prueba con un remoto local: instalar una librería sin problemas y hacer `git push` → pasa solo; simular una vulnerabilidad → el `git push` se detiene con el mensaje.
- Darwin: en un proyecto real, comprobar que no estorba cuando todo está limpio.

## 6. Cierre
- [ ] Spec aprobada por Darwin antes de programar
- [ ] Línea añadida a `.brain/decisions.log`
- [ ] Punto 28 de pendientes pasa a «Esperando tu prueba»
