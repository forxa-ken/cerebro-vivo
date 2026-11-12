# Informe del auditor (plantilla; spec 044)

Lo rellena el auditor (interno o externo) y lo recibe quien encargó la revisión. **Solo avisa: no cambia código ni bloquea el cierre.** Todo hallazgo lleva archivo y línea; lo que no se pudo comprobar va aparte, nunca afirmado.

- **Modo:** general / cierre / cierre de spec
- **Quién audita:** (modelo y esfuerzo; si hubo IA externa, cuál)
- **Qué se revisó:** (carpeta, diff o archivos)
- **Veredicto:** apto / apto con reparos / devuelto

## Calidad
1. **[alta|media|baja] `archivo:línea`** — qué falla y por qué incumple el requisito. *Comprobado ejecutando: sí/no.*

## Consumo de recursos
1. **[alta|media|baja] `archivo:línea`** — qué gasta de más (CPU, memoria, disco, red). *Comprobado: sí/no.*

## Seguridad
1. **[alta|media|baja] `archivo:línea`** — qué se puede abusar y cómo. *Comprobado: sí/no.*

## No comprobado
- (lo que no se pudo ejecutar o confirmar, y por qué)

## Coincidencias y discrepancias (solo si hubo dos auditores)
- **Coinciden:** (hallazgos que vieron los dos)
- **Solo el interno:** …
- **Solo el externo:** …

## Gasto
- (tokens y tiempo de cada auditor, si se conocen)
