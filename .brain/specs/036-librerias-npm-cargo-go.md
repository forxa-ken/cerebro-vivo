# Spec 036: `librerias.py` y `eventos_chat.py` también para npm, cargo y go (punto 32)

- **Estado:** borrador (2026-11-11), a aprobar por Darwin antes de programar
- **Origen:** hoy `librerias.py` solo lee `requirements.txt` y consulta OSV.dev con el ecosistema `PyPI`; `eventos_chat.py` reconoce `npm install`, `cargo add` y `go get`, pero de esos tres solo avisa una vez de que no pudo revisarlos. OSV.dev cubre los tres ecosistemas con la misma API.

## 1. En alcance
- [ ] `librerias.py`: leer, además de `requirements.txt`, las versiones fijadas de `package-lock.json` (npm), `Cargo.lock` (cargo) y `go.sum`/`go.mod` (go) si existen; consultar OSV con los ecosistemas `npm`, `crates.io` y `Go`.
- [ ] Versión mayor nueva: solo PyPI por ahora; npm (registry.npmjs.org) y crates.io solo si hay prueba sencilla; Go queda sin ese chequeo (se dice en el resumen).
- [ ] `eventos_chat.py`: tras `npm install`, `cargo add` o `go get`, revisar lo recién instalado con OSV igual que con pip (limpio: pasa; vulnerabilidad: detiene el `git push`), y quitar el aviso de «no pude revisarlo» para esos tres.
- [ ] Ajustes en `guardianes.json` (claves nuevas que se proponen, no se pisan): ecosistemas activos y archivos a leer.
- [ ] Proyecto sin ninguno de esos archivos: calla, como hoy.
- [ ] Textos nuevos en `textos.py` es/en; skill `vigilar-librerias` (es/en) actualizada.
- [ ] Pruebas con respuestas de OSV simuladas (sin red) para cada ecosistema.

## 2. Fuera de alcance
- Instalar o actualizar librerías por el usuario.
- Otros ecosistemas (Maven, NuGet, Composer…).
- Auditar dependencias transitivas más allá de lo que fija el archivo de bloqueo.

## 3. Riesgos
- Los archivos de bloqueo pueden ser enormes (cientos de paquetes): consulta por lotes (OSV `querybatch`) y tope de tamaño.
- Sin red o respuesta rara: se conserva el estado anterior y no se bloquea nada (como hoy).

## 4. Archivos
`librerias.py`, `eventos_chat.py`, `textos.py`, `guardianes.json`, skill `vigilar-librerias` (es/en), `tests/`, `VERSION`, `CAMBIOS.md`, `manifiesto.json`.

## 5. Verificación
`python -m unittest discover tests` en verde; una prueba real a mano con un proyecto que tenga `package-lock.json` (no probada hasta hacerla).
