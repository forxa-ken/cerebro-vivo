# Plantillas de la fábrica de IA (spec 035, fase 1)

Para un proyecto donde una **directora** (Opus) convierte el objetivo de Darwin en una spec, **ejecutoras** hacen encargos pequeños y un **revisor** independiente verifica. Esto son solo las plantillas: se copian a `.brain/fabrica/` del proyecto cuando Darwin decide montar una fábrica. Las hace cumplir el guardián `.brain/guardianes/fabrica.py` (fase 2); de la carta lee las líneas `clave: número`.

## 1. Carta de la fábrica

Archivo `.brain/fabrica/carta.md`. **Solo la escribe Darwin**; la directora la lee y no la edita (lo vigilará un guardián).

```markdown
# Carta de la fábrica: <proyecto>
- Objetivo: <una frase, en palabras de Darwin>
- Prohibido: <lo que ninguna IA puede hacer: dependencias nuevas, tocar X, subir a GitHub…>
- Tope por encargo: 2 ventanas de ~200.000 tokens o 400.000 gastados; salta el primero que se alcance (se para y se pregunta)
- Tope por misión: 10 encargos y 1.000.000 de tokens de Codex
- Freno general: si el gasto semanal de Codex baja del 50 % libre, parar y preguntar
- Fallos: dos seguidos en un mismo encargo = parar y avisar a Darwin
- tope_encargo_tokens: 400000
- tope_mision_encargos: 10
- tope_mision_tokens: 1000000
- libre_semanal_minimo: 50
- fallos_seguidos_max: 2
- Ejecutora por defecto: <Codex | Claude | la que decida la directora>. La eliges tú; con «la que decida la directora» ella elige por encargo y te dice cuál usó. Para un encargo concreto puedes pedir otra en el chat.
- Directora: Opus, esfuerzo medio, una por proyecto. Lectura detallada de resultados: Sonnet, esfuerzo medio
```

## 2. Roles

Archivo `.brain/fabrica/roles.md`: quién hace qué y quién es dueño de cada archivo. El archivo ajeno se lee, no se escribe. Nadie se aprueba a sí mismo.

```markdown
# Roles de la fábrica
| Papel | Quién | Puede escribir | No puede |
|---|---|---|---|
| Directora | Claude Opus (un chat por proyecto) | spec, encargos, huecos, propuestas, evidencia | programar; editar la carta; hablar con nadie que no sea Darwin |
| Ejecutora | Claude o Codex Luna | solo los archivos que lista su encargo, en su propio worktree y rama; su nota en `.brain/notas-chats/` | commitear; tocar el resto de `.brain/`; añadir o quitar requisitos |
| Revisor | Claude en otro chat | su informe | cambiar el código que revisa |
| Darwin | persona | la carta; aprueba las tres puertas | — |
```

## 3. Las tres puertas de Darwin

1. **La spec**, antes de lanzar nada. Debe tener: qué puede hacer el usuario (acción, condiciones de partida, permisos), resultado esperado, qué decisiones y funciones anteriores hay que respetar, cómo se demuestra y qué evidencia queda guardada, y el **presupuesto de recursos** (CPU, memoria, disco, red, batería: cuánto puede gastar; si no importa, se escribe «sin presupuesto»).
2. **Cada hueco** de la spec: se registra y se pregunta; nadie lo rellena con una suposición.
3. **El informe final**: lo pedido, lo hecho y lo extra. Lo extra se revierte salvo que Darwin lo acepte.

Tras aprobar la spec se guarda su huella con `python .brain/guardianes/fabrica.py congelar SPEC`. Un requisito nuevo va a las propuestas y espera su aprobación.

## 4. Encargo

Archivo `.brain/fabrica/encargos/NNN-nombre.md`. Lo escribe la directora. **Sin requisito aprobado, el encargo se rechaza.** Debe listar **todos** los puntos de la spec que le tocan: lo que no está listado, la ejecutora no lo hace.

```markdown
# Encargo NNN: <nombre>
- Requisito que cumple: <R-n de la spec aprobada> (obligatorio)
- Puntos de la spec que entran: <lista completa, no un resumen>
- Archivos permitidos: <rutas exactas; una carpeta termina en />
- Prohibido en este encargo: <dependencias, accesos nuevos, otros archivos>
- Prueba que lo da por bueno: <comando o comprobación concreta>
- Evidencia que debe dejar: <qué se anota y dónde>
- Ejecutora: <Claude / Codex Luna (esfuerzo)> · worktree y rama: <nombre>
```

## 5. Evidencia

Archivo `.brain/fabrica/evidencia/REQ-n.md`: uno por requisito cerrado. Una comprobación que no se ejecutó se escribe como «no ejecutada», nunca se omite.

```markdown
# Evidencia del requisito R-n
- Encargo(s): NNN
- Qué se comprobó y cómo: …
- Resultado: <verde / rojo / no ejecutada, con el motivo>
- Archivos tocados (el guardián de alcance, o a mano si aún no existe): …
- Gasto: <tokens por papel>
- Lo extra que apareció: <nada / lista>
```

## 6. Huecos y propuestas

Archivos `.brain/fabrica/huecos.md` y `.brain/fabrica/propuestas.md`. Los escribe la directora con lo que le cuentan la ejecutora y el revisor.

```markdown
# Hueco H-n (abierto / resuelto por Darwin el AAAA-MM-DD)
- Dónde: <requisito o punto de la spec>
- Qué falta decidir: …
- Opciones vistas: …
- Respuesta de Darwin: …

# Propuesta P-n (esperando / aprobada / rechazada)
- Quién la propone y por qué: …
- Requisito nuevo o cambio: …
```

## 7. Seguridad sin cambiar lo pedido

Ninguna IA cambia ni quita un requisito «por seguridad». Si ve un riesgo, lo registra como hueco o propuesta y pregunta a Darwin.

## 8. Revisión por riesgo

El revisor comprueba que lo entregado responde al requisito, contrasta cada hallazgo con el código real y los ordena por gravedad. Lo trivial se corrige y se anota. Lo que afecta a un requisito o a una decisión anterior se escala a Darwin.

## 9. Criterio de «esperado» (modo automático, spec 050)

Archivo `.brain/fabrica/esperado.md`. Lo escribe Darwin (o la directora lo propone y Darwin lo aprueba) **antes** de construir nada. En modo automático, `fabrica.py arrancar` (y `foto`, que lo llama sola) **bloquea** el encargo si falta, si los dos campos obligatorios siguen con `<…>` o si se está en `main`. Los campos obligatorios son «Cómo se sabe que salió bien» y «Casos malos»; si de verdad no aplica, se escribe «no aplica» con el motivo.

```markdown
# Criterio de «esperado»: <orden>
- Lo que se pide (negocio): <una frase, en palabras de Darwin>
- Cómo se sabe que salió bien: <comprobación observable, no «que se vea bien»> (obligatorio)
- Casos buenos (deben funcionar): <lista>
- Casos malos (deben rechazarse): <lista, o «no aplica» con el motivo> (obligatorio)
- Lo que una IA no puede juzgar (queda para Darwin): <aspecto, comprensión…>
```

## 10. Evidencia de uso real (modo automático, spec 050)

Archivo `.brain/fabrica/evidencia/REQ-n.md`, escrito por **otra IA distinta de la que construyó**. Los archivos de evidencia (comandos, salidas, capturas) van dentro de `.brain/fabrica/evidencia/`. `fabrica.py entregar REQ-n` **bloquea** la entrega si falta cualquier campo, si «Probó» es igual que «Construyó», si «Criterio probado» no cita una frase literal de `esperado.md` entre «…», si un archivo de evidencia no existe o está vacío, o si el resultado no es verde. «Rojo» vuelve a la ejecutora; «no probado» pasa a «Esperando tu prueba (Darwin)».

```markdown
# Evidencia de uso real del requisito R-n
- Construyó: <IA que construyó>
- Probó: <IA distinta que hizo la prueba>
- Criterio probado: «<frase literal copiada de esperado.md>»
- Casos buenos ejecutados: <comando → qué salió>
- Casos malos ejecutados: <comando → cómo se rechazó, o «no aplica» con el motivo>
- Resultado: <verde / rojo / no probado, con el motivo>
- No probado: <lo que una IA no puede juzgar, o «nada» con el motivo> (nunca vacío)
- Evidencia guardada: <rutas dentro de .brain/fabrica/evidencia/, separadas por comas>
```

## 11. Informe de entrega y frenos (modo automático, spec 050)

**Informe de entrega:** archivo `.brain/fabrica/informe.md`, una página llana para Darwin. `fabrica.py informe` comprueba que están las seis secciones y que **ninguna queda vacía sin explicación** (un «nada» lleva su motivo). Con él Darwin decide una sola vez: aceptar o descartar la rama.

```markdown
# Informe de entrega: <orden>
## Lo pedido
- <la orden y el criterio de «esperado», en palabras de Darwin>
## Lo hecho
- <qué se construyó, por requisito>
## Lo extra
- <lo que apareció sin pedirlo (se revierte salvo que Darwin lo acepte), o «nada: motivo»>
## Lo probado de verdad
- <qué se probó de uso real, quién lo probó y dónde está la evidencia>
## Lo no probado
- <lo que ninguna IA pudo juzgar o no se pudo ejecutar; pasa a «Esperando tu prueba (Darwin)», o «nada: motivo»>
## Decisiones de la línea por su cuenta
- <cada decisión que tomó la línea sin preguntar (nombres, orden, opción conservadora ante un hueco pequeño), o «nada: motivo»>
```

**Frenos:** `fabrica.py frenos --encargo N` para el encargo a los **3 fallos** o a los **30 minutos sin avance** y deja `.brain/fabrica/estado/parada-N.md` con dónde quedó. `foto` lo llama sola; `gasto` (sin fallo), `foto` y `entregar` anotan avance; `avance --encargo N --nota «…»` lo anota a mano. Solo Darwin reanuda: `frenos --encargo N --reanudar`. La carta puede cambiar los topes con las líneas `- auto_reintentos_max: 3` y `- auto_atasco_minutos: 30`.
