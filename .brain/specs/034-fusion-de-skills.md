# Spec 034: fusión de skills (verificación y plan; sin ejecutar)

- **Estado:** DESCARTADA por Darwin el 2026-11-08: el ahorro (~0,3k tokens al arrancar, <0,5 %) no compensa el riesgo de romper instalador, textos, constitución y pruebas. Se probó un cambio en `traspaso-out` (1.29.1) y se revirtió; no se quitó ni fusionó ninguna skill. El análisis de abajo queda como referencia.
- **Hallazgo previo:** el «jardinero de documentación» (punto 29) no es una skill, es la sexta pieza de higiene de memoria (informe 028); va dentro de la fusión de higiene, no como guardián nuevo.

## 1. Qué se leyó
Cuerpos completos de `traspaso-in`, `traspaso-out`, `memoria-traspaso`, `chat-nuevo`, `leccion`, `adopta`, y cabecera de `acorta`, `trocea`, `adoptar-indice-existente`, `revisar-indices-de-ia`. El resto (cerrar-una-tarea y las de una regla) se vio por tamaño. El uso real del informe 032: 11 de 29 skills a cero en los tres proyectos.

## 2. Candidatas, de más a menos clara
| Grupo | Solapamiento comprobado | Propuesta |
|---|---|---|
| `traspaso-in` ↔ `traspaso-out` | `salgo` de uno repite los pasos 1-3 del otro; `entro` es casi idéntico (arranque.py `--manual`, mover el traspaso, 4-5 viñetas, una pregunta). La diferencia real es solo abrir chat nuevo (in) o subir memoria con `guardar_traspaso.py` (out). | Un cuerpo común (`traspaso`) con dos secciones: «mismo IA» y «otra IA». Conservar los dos nombres de comando como alias. |
| `adopta` + `adoptar-indice-existente` + `acorta` | `adopta` ya dice «leer la skill X y seguirla» para cada una. | Una skill `adopta` con los tres pasos dentro; `acorta` sigue como alias de un paso. |
| `trocea` + `revisar-indices-de-ia` | Ambas vigilan tamaño y orden de `.brain/` (informe 028, §2). | Una skill de higiene de memoria, junto al guardián único de higiene (punto 29). |
| `chat-nuevo` + `memoria-traspaso` | Son comandos de 3 pasos que invocan un script o leen un archivo. | Plegarlas dentro de `traspaso`. |
| `leccion` + `cerrar-una-tarea` | `leccion` lo dicen ya los textos del guardián `hitos.py`. | **No fusionar**: son el seguro de dos guardianes que sí se usan. Revisar solo cuando se retoque el aviso (propuesta 2 del 032: se deja como está). |

## 3. Ahorro real y límites
- Arranque: la lista de skills pesa ~1k tokens; de 29 a ~20 ahorra **~0,3k**, casi nada. La ganancia es de mantenimiento: cada skill va en dos idiomas, entra en el manifiesto y la prueba de paridad, y 2 textos duplicados cada vez.
- Riesgo: algunas skills actúan como comando que Darwin escribe (`/acorta`, `/trocea`, `/leccion`); quitarlas sin alias rompe su costumbre. Por eso se plantean alias.
- No se comprobó cómo se anotan las skills «aplicadas por el guardián sin llamar a la skill»: el medidor no las ve (límite del informe 032).

## 4. Pasos si Darwin aprueba
1. Fusionar primero `traspaso-in` y `traspaso-out` (la más repetida, 31 llamadas).
2. Luego `adopta` + las dos.
3. Higiene de memoria junto al punto 29.
4. Cada paso: es/en, manifiesto, VERSION, pruebas de paridad en verde.
