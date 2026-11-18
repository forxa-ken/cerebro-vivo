# Spec 091: la fábrica mide el gasto de la directora por encargo y cierra cada encargo con un solo comando

- **Estado:** **aprobada por Darwin el 2026-11-18** (con las dos propuestas de la sección 7: el gasto de la directora solo se muestra, no entra en los topes; `cerrar-encargo` nunca acepta el encargo, eso lo decide la directora).
- **Fecha:** 2026-11-18
- **Se apoya en:** spec 035 (fábrica), spec 050 (modo automático y topes), spec 088 (camino corto); `fabrica.py` y `medir.py`.
- **Origen:** pasos 1 y 2 del esquema `.brain/archive/notas-chats/2026-11-18-esquema-cascaron-generico.md` (sección 9) y huecos del informe `2026-11-18-revision-de-la-fabrica.md`. Darwin: el cascarón genérico es solo para él por ahora; un solo perfil (el suyo).

## 1. Objetivo
Dos mejoras pequeñas y de bajo riesgo, sin cambiar cómo trabaja la fábrica:
1. **Ver cuánto gasta la directora en cada encargo.** Hoy `gasto.json` solo guarda lo que gastan ejecutora, revisora y Codex; lo de la directora no se mide por encargo, y los topes y el informe no lo cuentan.
2. **Un comando que cierre cada encargo.** Hoy la directora encadena a mano varios comandos (`alcance`, pruebas, `gasto`, `avance`…). Un solo `cerrar-encargo` los corre en orden y devuelve un resumen de ~10 líneas, con el detalle guardado en `evidencia/`.

## 2. En alcance (In-Scope)
### Paso 1: gasto de la directora por encargo
- [ ] `medir.py` ya reconoce los chats de la directora (`directora_de_proyecto`). Añadir que reparta su gasto **por encargo** usando las marcas de tiempo de `estado/` (inicio y cierre de cada encargo): lo gastado entre ambas va a ese encargo; lo de fuera, a «sin encargo» (spec, informe, charla con Darwin).
- [ ] Nuevo papel `directora` en `gasto.json` (mismo formato que los demás: `encargo`, `tokens`, `papel`, `fallo`), anotado por el comando de la sección siguiente, no a mano.
- [ ] El informe final y `topes` muestran el gasto de la directora **como línea aparte**; entra en el total, pero se ve separado.
- [ ] Texto nuevo en `textos.py` es/en.

### Paso 2: `fabrica.py cerrar-encargo --encargo N`
- [ ] Corre en orden: `alcance` (archivos tocados dentro de lo permitido), pruebas del proyecto, anotación del gasto de la directora del encargo, `avance` con nota automática.
- [ ] Devuelve un **resumen corto**: verde/rojo por paso, tokens por papel, archivos tocados. Guarda el detalle en `evidencia/` del encargo.
- [ ] Si algún paso falla, **no oculta nada**: el resumen dice «rojo» y en cuál; no marca el encargo como cerrado.
- [ ] **No decide ni acepta**: la directora sigue leyendo el diff y aceptando o devolviendo. El comando solo ahorra pasos mecánicos.
- [ ] Los comandos sueltos actuales **siguen funcionando** igual (compatibilidad).
- [ ] Texto es/en y pruebas automáticas.

## 3. Fuera de alcance (Out-of-Scope)
- `roles.json`, `perfil.json`, adaptadores por motor y reescritura neutra de skills (pasos 3 a 5 del esquema): otra spec, si Darwin la pide.
- Spec 089 (ejecutoras en paralelo, en pausa), spec 090 (web) y `pendientes.md`: no se tocan.
- Prominimap ni ningún proyecto ajeno.
- Cambiar umbrales (150/700 líneas), topes, esfuerzo de los modelos o el reparto de papeles.
- Subir nada a GitHub ni regenerar el ZIP de Mac.

## 4. Plan de implementación
1. `medir.py`: función que reparte el gasto de la directora entre encargos a partir de `estado/` (solo lectura de los chats, sin escribir en ellos).
2. `fabrica.py`: papel `directora` en `gasto`, línea aparte en `informe` y `topes`.
3. `fabrica.py`: orden `cerrar-encargo` que reutiliza `alcance`, `gasto` y `avance` ya existentes (no duplicar lógica).
4. Textos es/en; actualizar la skill `directora-de-fabrica` (es/en) para usar el comando nuevo.
5. Pruebas; subir `VERSION`, `CAMBIOS.md`, `python generar_manifiesto.py`.

## 5. Plan de verificación
- `python -m unittest discover tests` en verde, con pruebas nuevas: reparto por encargo con chats de ejemplo, `cerrar-encargo` verde, rojo por alcance, rojo por pruebas, y compatibilidad de los comandos sueltos.
- **Prueba de uso real** (Darwin la verá): un encargo pequeño en un proyecto de prueba cerrado con `cerrar-encargo`; comprobar que el resumen coincide con lo que dicen los archivos.
- Comprobar a mano el gasto de la directora de un encargo ya hecho contra lo que enseña `medir.py` por su lado.

## 6. Riesgos y límites honestos
- **El reparto por tiempo es aproximado:** si la directora trabaja en dos encargos a la vez o charla con Darwin en medio, parte del gasto se atribuye mal. Se presenta como estimación, no como cifra exacta.
- **Los chats de Claude y de Codex se leen por separado**; esta spec solo mide a la directora (Claude). Si la directora fuera otro motor, no se mediría.
- **Ejecutar pruebas desde el comando** depende de que el proyecto declare cómo se corren; si no lo declara, el paso se marca «sin pruebas definidas» (no verde).
- Nada de esto está probado en un encargo real todavía.

## 7. Preguntas abiertas para Darwin
- ¿El gasto de la directora **cuenta para los topes** de la carta (puede parar la misión) o solo se **muestra**? Propuesta: solo mostrar al principio, hasta ver que la cifra es fiable.
- ¿`cerrar-encargo` debe **aceptar** el encargo solo cuando todo da verde, o dejarlo siempre a la directora? Propuesta: siempre a la directora.

## 8. Cierre
- [ ] Spec aprobada por Darwin antes de programar
- [ ] Pruebas en verde y prueba de uso real hecha
- [ ] Skill actualizada es/en, `VERSION`, `CAMBIOS.md` y manifiesto
- [ ] Línea añadida a `.brain/decisions.log`
