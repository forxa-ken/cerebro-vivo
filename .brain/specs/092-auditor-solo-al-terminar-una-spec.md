# Spec 092: el auditor de cierre solo avisa cuando una spec (o un encargo de la fábrica) termina

- **Estado:** **implementada en v1.61.4** (aprobada por Darwin el 2026-11-19: «Sí, escríbelo y prográmalo»). Falta que Darwin la pruebe en Prominimap (actualizar el arnés allí).
- **Fecha:** 2026-11-19
- **Se apoya en:** spec 044 (auditor de dos modos), spec 033 (cierre por bloque), spec 038 (avisos repetidos), spec 091 (`fabrica.py cerrar-encargo`).
- **Origen:** Darwin, desde Prominimap: el aviso «lanza el auditor» sale en cada respuesta mientras haya cambios sin commitear, aunque se acabe de cerrar y auditar. Y: «en modo normal no se hacen encargos, se programa sin más; solo se debería activar por spec terminada».

## 1. Problema
`cierre.py` pedía el auditor en **cada respuesta** que dejara código sin commitear (spec 044: «mira esto aunque el bloque siga abierto»). No guardaba que ya se hubiera auditado, y solo la spec 038 lo callaba tras 3 repeticiones seguidas en el mismo chat. Además se pensó para la fábrica, donde hay encargos; en modo normal no los hay.

## 2. Qué cambia
1. **El aviso solo sale si hay un cierre pendiente de auditar.** Un cierre pendiente se marca de forma explícita:
   - **Modo normal:** `python .brain/guardianes/auditor.py terminada NNN` al terminar una spec (NNN = número o nombre). Solo se marca si entre los archivos cambiados hay código o configuración (los documentos no se auditan).
   - **Modo fábrica** (`modo_fabrica: true`): `fabrica.py cerrar-encargo` lo marca solo cuando el cierre mecánico sale en verde (también se puede marcar a mano con `terminada`).
2. **Se quita el aviso por cada respuesta con cambios sin commitear.** Sin marca, el auditor no avisa nunca; para una revisión suelta existe `/auditor general` o `/auditor cierre` a mano.
3. **`python .brain/guardianes/auditor.py auditada`** borra la marca cuando el auditor ya pasó. Mientras la marca existe, el aviso sigue saliendo (con el límite de repeticiones de la spec 038); en cuanto se da por auditada, no vuelve.
4. El aviso dice **qué se cerró** (la spec o el encargo) y qué comando usar al acabar; si había archivos sensibles, mantiene la sugerencia del auditor externo.
5. `auditor_cierre: false` sigue apagándolo todo (`terminada` responde que está apagado y no marca nada).
6. La marca vive en `.brain/guardianes/auditor_pendiente.json` (estado local: no se reparte ni se sube; va en `.gitignore`).

## 3. Fuera de alcance
- No lanza el auditor ni ninguna IA: solo avisa, como antes.
- No cambia quién audita ni los modos `general`, `cierre`, `spec`.
- Los demás avisos del cierre (línea del registro, tope de pendientes, longitud, hitos) no cambian.

## 4. Pruebas
- Sin marca y con código sin commitear: no avisa.
- Con marca: avisa (nombre de la spec o del encargo); tras `auditada`: no avisa.
- `terminada` solo con documentos: no marca. Con `auditor_cierre: false`: no marca.
- `cerrar-encargo` en verde con `modo_fabrica` marca; en rojo o sin modo fábrica, no.
- Paridad es/en de los textos nuevos; archivo de estado ilegible no tumba el cierre.

## 5. Riesgos honestos
- Si la IA olvida marcar `terminada`, el auditor no avisa. Es el cambio de fondo (de «siempre» a «cuando se pide»); la skill `cerrar-una-tarea` y la del auditor lo recuerdan al terminar una spec.
