# Esquema del funcionamiento y modelo genérico («cascarón») para la web (2026-11-18)

Borrador para decidir con Darwin. **Nada de esto está programado.** Sirve para la fase 5 de la spec 090 (fábrica y chats) y para que un usuario nuevo adapte el sistema a sus necesidades sin depender de una IA concreta.

## 1. Idea en una frase
El sistema son **archivos y reglas** que no saben qué IA los usa. Las IA son **enchufes intercambiables** que se asignan a **puestos de trabajo**. El usuario no elige IAs, elige **un perfil** (cuánto quiere gastar, cuánto quiere supervisar) y el sistema reparte los puestos.

## 2. Las cinco capas (de abajo arriba)

| Capa | Qué es | ¿Atada a una IA? | Hoy |
|---|---|---|---|
| 1. **Núcleo** | Carpeta de archivos y programas: carta, spec congelada, encargos, estado, gasto, topes, alcance de archivos, evidencia, informe | **No** (son archivos y comandos) | `fabrica.py` y `.brain/fabrica/` |
| 2. **Puestos** | Quién hace qué: dueño, directora, ejecutora, revisora, probadora, administrativa | No (son papeles) | repartidos entre skills |
| 3. **Enchufes de IA** | Cada IA se conecta con el mismo contrato: recibe una orden + una carpeta, devuelve resumen + evidencia + tokens gastados | Aquí viven las diferencias | Claude por Agent, Codex por `codex exec`, DeepSeek por `opencode` |
| 4. **Perfil del usuario** | Un archivo con sus preferencias: umbrales, qué es delicado, qué puertas aprobar, topes, idioma, quién ocupa cada puesto | No | repartido entre carta, skills y guardianes |
| 5. **Web** | Pantallas para ver, aprobar y lanzar; roles de usuario | No | spec 090 fases 1 a 6 |

## 3. Los puestos y su regla de oro
| Puesto | Hace | **No** hace | Modelo por defecto |
|---|---|---|---|
| **Dueño** (humano) | Aprueba la spec, aprueba el informe, firma la carta, prueba lo visible | Nada mecánico | — |
| **Directora** | Decide: escribe la spec, resuelve huecos, acepta o devuelve, habla con el dueño | Programar, correr pruebas, leer diffs | medio |
| **Ejecutora** | Construye un encargo en su carpeta | Decidir requisitos | medio / barato |
| **Revisora** | Lee el diff y el requisito, da veredicto | Cambiar código | medio, distinta de la ejecutora |
| **Probadora** | Prueba el producto de verdad y deja evidencia | Haber construido lo que prueba | medio, distinta de la ejecutora |
| **Administrativa** | Corre pruebas, anota gasto y topes, redacta informes, devuelve resúmenes de ~10 líneas | Juzgar | **la más barata** |

Regla de oro: **cada puesto devuelve un resumen corto y guarda el detalle en `evidencia/`**; la directora solo abre el detalle si el resumen dice «rojo» o «no pude».

## 4. Recorrido de una orden (sirve para cualquier IA)

```
Orden del dueño
      │
      ▼
 ¿Tamaño y riesgo?  ← umbrales del perfil (hoy: 150 y 700 líneas; delicado sí/no)
      │
 ┌────┼────────────────────────┬─────────────────────────────┐
 ▼                             ▼                             ▼
RUTA A  ≤150 líneas        RUTA B  150–700            RUTA C  >700, varios encargos
sin fábrica               camino corto               o delicado: fábrica completa
 │                            │                             │
 1 aviso en una frase      1 spec corta                 1 spec + negocio sellado
 2 UN subagente construye  2 una revisión de spec       2 revisión de spec (≤2 vueltas)
 3 administrativa:         3 un encargo                 3 el dueño aprueba la spec  ◄ puerta (a)
   pruebas + resumen       4 administrativa: alcance,   4 un encargo por requisito
 4 el dueño ve resumen       pruebas, resumen           5 ejecutora → administrativa
   y prueba lo visible     5 revisión solo si hay          → revisora → probadora
                             lógica nueva               6 informe → el dueño  ◄ puerta (c)
                           6 prueba de uso real breve   7 consumo solo si lo pide
```
Frenos en B y C (en A basta con las pruebas): tope por encargo, 3 fallos, 30 min sin avance. El modo automático encadena encargos sin preguntar al dueño entre ellos.

## 5. Contrato del «enchufe de IA» (lo único que cambia entre IAs)
Todo motor se describe con las mismas cinco cosas; si las cumple, vale:
1. **Cómo se lanza:** comando o herramienta (Agent, `codex exec`, `opencode run`, una API).
2. **Qué recibe:** orden en texto + carpeta de trabajo + archivos permitidos.
3. **Qué devuelve:** resumen corto + ruta de la evidencia + tokens gastados.
4. **Límites:** tope de tiempo, de tokens, si puede ejecutar código, si escribe en la carpeta o solo lee.
5. **Garantías:** dónde van sus datos (local, nube del proveedor), si es de confianza para código privado.

Ejemplo de archivo `roles.json` (idea, no existe):
```
directora:      motor claude, modelo sonnet, esfuerzo medio
ejecutora:      motor codex,  modelo luna,   esfuerzo alto   (alternativa: claude sonnet)
revisora:       motor claude, modelo sonnet, solo lectura
probadora:      motor claude, modelo sonnet, distinta de la ejecutora
administrativa: motor claude, modelo haiku
```
Reglas que el sistema comprueba solo: revisora y probadora ≠ ejecutora; un motor sin garantía de privacidad no ocupa puestos con código privado.

## 6. Qué hoy está atado a Claude y habría que soltar
- Las **skills** hablan de «subagente Agent», `start_session`, `ToolSearch`, hooks `Stop`: son de Claude Code. → Reescribir las reglas como **texto neutro** («lanza al puesto X») y dejar cada herramienta en un **adaptador**.
- `fabrica.py`, los archivos y los guardianes **ya son neutros**: pueden quedarse.
- El **medidor de gasto** lee registros de Claude y de Codex por separado. → Que cada adaptador devuelva sus tokens en el mismo formato.
- La **apertura de chats** (directora, traspaso) depende de la app de escritorio. → En la web, un «trabajo» es un proceso que el adaptador lanza y vigila; el chat es opcional.

## 7. Cómo lo adapta cada usuario (el perfil)
Un asistente de 6 preguntas en lenguaje llano genera `perfil.json`, y de ahí salen la carta, los umbrales y `roles.json`:
1. ¿Qué te preocupa más: **gastar poco**, **ir rápido** o **que no se rompa nada**?
2. ¿Qué IAs tienes disponibles y cuáles puedes pagar? (cuentas y límites)
3. ¿Hay **código o datos privados** que no deben salir de tu equipo?
4. ¿Qué cosas son **delicadas** para ti? (pagos, datos de clientes, servidores…)
5. ¿Cuántas veces quieres **aprobar**: solo la spec y el informe, o más?
6. ¿Cuánto quieres **supervisar** el gasto: avisar solo, o parar al llegar a un tope?

Perfiles de partida (el usuario los retoca):
| Perfil | Umbrales | Revisiones | Puestos baratos | Para quién |
|---|---|---|---|---|
| **Ahorro** | A hasta 300 líneas | Solo grandes | Todo lo posible | quien paga cada token |
| **Equilibrado** (el de hoy) | A ≤150, B ≤700 | Grandes y con lógica nueva | Administrativa | uso normal |
| **Máxima garantía** | A solo texto/estilo | Siempre, con IA distinta | Ninguno | código crítico o con terceros |

## 8. Qué ve la web (propuesta mínima)
- **Panel de la misión:** ruta (A/B/C), encargos y su estado, gasto por puesto con la directora incluida, tiempo.
- **Pantalla de roles:** qué motor ocupa cada puesto, con aviso si alguna regla se rompe (revisora = ejecutora).
- **Pantalla de perfil:** las 6 preguntas y los umbrales, con el efecto en una frase.
- **Puertas:** aprobar spec e informe desde la web, con permisos por rol (spec 090 §9).
- Los **resúmenes** son lo que se muestra; el detalle queda a un clic.

## 9. Pasos para llegar ahí (de menos a más riesgo)
1. Medir el gasto de la directora **por encargo** en `gasto.json` (hoy sin medir).
2. `fabrica.py cerrar-encargo`: un solo comando que corre alcance y pruebas, anota el gasto y devuelve el resumen.
3. Definir `roles.json` y `perfil.json` con valores de hoy (sin cambiar el comportamiento).
4. Reescribir las skills en texto neutro y mover lo específico de Claude, Codex y OpenCode a adaptadores.
5. La web los lee (solo lectura) y luego permite editarlos.

## 10. Decisiones abiertas para Darwin
- ¿Los **perfiles de partida** son esos tres, o prefieres solo uno y que el usuario ajuste?
- ¿Quién ocupa los puestos por defecto para un usuario **nuevo** sin cuentas de pago: solo un motor (el que tenga) en todos los puestos?
- ¿El producto es **para ti y tu círculo** o para público general? Cambia la privacidad, los permisos y el soporte.
- ¿Un motor sin garantías de privacidad (como DeepSeek) se permite si el usuario lo marca, o se prohíbe?

## 11. Lo que no sé
- Si Haiku aguanta las tareas de la administrativa (sin probar).
- El gasto real de la directora por encargo (sin medir).
- Si un motor distinto de Claude, Codex y OpenCode cumple el contrato de la sección 5.
