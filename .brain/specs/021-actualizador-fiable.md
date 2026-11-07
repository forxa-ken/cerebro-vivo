# Spec 021: actualizador fiable

- **Estado:** implementada
- **Fecha:** 2026-11-07
- **Versión prevista:** arnés 1.19.0

## 1. Objetivo
Que actualizar un proyecto deje lo que dice que deja. Hoy, comprobado con pruebas en carpeta temporal (chat #16):
- Lo retirado del arnés sigue en los proyectos (pasó con la skill vieja de LoboHook).
- Un corte a media escritura deja un archivo roto, que luego se toma por «modificado a mano» y no se repara.
- Se anota la versión nueva aunque algún archivo se haya quedado viejo.
- No se compara la huella del manifiesto: acepta una falsa.
- `--simular` no anuncia todo lo que hará después.
- En un proyecto de nivel ligero o medio copia guardianes y pruebas que allí quedan rotos (punto 14, caso `F:\Pegatinas`).
- `README.md:38` y `CEREBRO_VIVO.md:122` dicen que las claves nuevas «solo se proponen», y desde la spec 019 se añaden.

## 2. En alcance
- [x] **Retirados.** `manifiesto.json` gana la lista `retirados`.
  - `generar_manifiesto.py` la mantiene solo: lo que estaba en el manifiesto anterior y ya no está entra en la lista, y lo que vuelve sale. Avisa por pantalla de cada entrada nueva.
  - Lista inicial, sacada del historial de Git: `modo_auto.py`, `uso_tokens.py`, `test_modo_auto.py`, `traspaso-entre-chats`, `cambio-de-ia`, `test_cambio_de_ia.py`.
- [x] **Qué hace el actualizador con un retirado** (también con su copia en `.agents/skills/`):

  | Estado en el proyecto | Qué hace |
  |---|---|
  | Sin tocar (huella igual a la registrada) | Lo mueve a la copia de seguridad, nunca lo borra, y lo quita del registro |
  | Modificado a mano o sin registro | No lo toca y lo lista |
  | Ya no existe | Lo quita del registro |

  Además borra la carpeta que quede vacía y, si era una skill, su fila de `.brain/experiencia/indice.md`, para no dejar un enlace roto.
- [x] **Escritura atómica.** Todo lo que escribe el actualizador pasa por un archivo temporal en la misma carpeta y `os.replace`: archivos del arnés, registro, `guardianes.json`, índice de skills y migración del objetivo. Un corte deja el archivo viejo o el nuevo entero, y al relanzar se completa lo que faltó.
- [x] **Versión honesta.** El registro conserva `version` y gana `sin_aplicar`, con las rutas que se quedaron viejas. El informe lo dice: «1.19.0 aplicada salvo N archivos».
- [x] **Comprobar huella.** Antes de escribir nada, cada archivo del repo debe coincidir con su huella del manifiesto. Si uno no coincide o falta, se para sin tocar el proyecto y explica el motivo. El kit hace la misma comprobación antes de empezar a instalar, para no quedarse a medias.
- [x] **Nivel guardado (punto 14).** El kit anota `nivel` en `.brain/arnes_instalado.json` también en ligero y medio.
  - El actualizador, en un proyecto de esos niveles, no copia nada y dice cómo subir a completo (`instalar.py RUTA --nivel completo`).
  - Proyectos antiguos sin `nivel`: si no tienen `guardianes.json`, se tratan igual.
  - `--forzar-todo` sigue sirviendo para adoptar un proyecto antiguo a propósito.
- [x] **`--simular` completo.** Anuncia también retirados, filas que se quitan, fichas de skills que se añaden (incluidas las de skills que aún no están copiadas) y lo que quedaría en `sin_aplicar`.
- [x] **Textos.** Corregir `README.md:38`, `CEREBRO_VIVO.md:122` y el comentario de `claves_nuevas`. Añadir los retirados a la skill `/actualizar`.

## 3. Fuera de alcance
- Grupos B y C del análisis: `secretos.py`, `cierre.py`, el traspaso y el método.
- Actualizar proyectos reales. Eso lo decides tú después, con `/actualizar`.
- Línea nueva en el arranque por `sin_aplicar`: se repetiría en cada chat. En LoboHook, por ejemplo, hay hoy 1 archivo modificado a mano. Se cuenta al actualizar, que es cuando se decide.
- Reparar por sí solo archivos ya cortados antes de esta versión: no se distinguen de uno modificado a mano. Seguirán listados y se arreglan con `--forzar RUTA`.
- Subir a GitHub sin tu orden.

## 4. Plan de implementación
1. Pruebas primero en `tests/test_arnes_actualizar.py`: una por cada fallo de la sección 1, que deben fallar antes del arreglo.
2. `actualizar_arnes.py`: escritura atómica, comprobar huella, retirados, `sin_aplicar`, nivel y simulación completa.
3. `generar_manifiesto.py`: lista `retirados`.
4. `instalar.py`: anotar `nivel` y comprobar el manifiesto antes de empezar.
5. Textos, `VERSION` 1.19.0, `CAMBIOS.md`, `python generar_manifiesto.py`. Sin ZIP de Mac: Darwin lo pidió así, su amigo no lo está usando.

## 5. Plan de verificación
- `python -m unittest discover tests`, todo en verde. Casos nuevos:
  - Retirado sin tocar, modificado a mano y ausente.
  - Corte simulado a mitad de la copia y relanzado.
  - Huella falsa: no se escribe nada.
  - Nivel medio: no se copia nada.
  - `--simular` no escribe y anuncia lo mismo que hace la ejecución real.
- Dos pruebas cambian a propósito: `test_desde_el_repo_con_simular` usa una carpeta vacía, que ahora el actualizador no aceptaría (se le añade `guardianes.json`), y la lista exacta de archivos del nivel ligero en `test_kit_arranque.py` gana `.brain/arnes_instalado.json`.
- Ensayo con copias temporales de `F:\Pegatinas` y LoboHook: actualizar y comprobar el resultado sin tocar los originales.

## 6. Riesgos
- **Primera actualización desde dentro de un proyecto:** la lanza el actualizador viejo, que no conoce los retirados. Se aplican en la siguiente actualización (la lista es acumulativa, no se pierde nada) o al momento con `python actualizar.py RUTA` desde este repo.
- **Dejar de repartir un archivo a propósito:** si se saca del manifiesto, entra en retirados y se quita de los proyectos donde esté sin tocar. Por eso el generador lo avisa, y el archivo queda en la copia de seguridad.
- **Manifiesto desfasado mientras se desarrolla:** el kit y el actualizador se negarán a trabajar hasta regenerarlo. Es lo buscado, pero se notará en más pruebas a la vez que la de ahora.

## 7. Cierre
- [x] Spec aprobada por Darwin antes de programar
- [x] Punto 14 pasado a «Esperando tu prueba» en `pendientes.md`
- [x] Línea añadida a `.brain/decisions.log`
