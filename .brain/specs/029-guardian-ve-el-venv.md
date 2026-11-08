# Spec 029: el guardián con memoria del chat ve las librerías del `.venv`

- **Estado:** aprobada por Darwin el 2026-11-08 (camino «completo con red de seguridad») y programada en 1.28.4
- **Fecha:** 2026-11-08
- **Versión prevista:** arnés 1.28.4
- **Origen:** punto 28 de pendientes, reabierto. Modelo #59 probó en `F:\Modelo 2` (con `.venv`): `pip install django==3.2` (fallo conocido GHSA-2gwj-7jmv-h26r) + `git push` subió a GitHub sin aviso.

## 1. Objetivo
Que `eventos_chat.py` revise de verdad lo que se instala en el entorno virtual de un proyecto, que es el caso normal. Causa: `revisar_push` pedía la versión a `importlib.metadata` del Python que ejecuta el hook (el del sistema); no ve el `.venv`, concluía «nada instalado» y dejaba pasar en silencio.

## 2. En alcance
- [x] Orden de confianza para saber qué versión consultar a OSV.dev: **1)** lo instalado en el `.venv` (o `venv`) de la raíz del proyecto, preguntándoselo a su propio Python en una sola llamada; **2)** la versión fijada en el propio comando (`nombre==versión`); **3)** el Python del hook, como hasta ahora.
- [x] **Ya no se deja pasar en silencio lo que no se pudo mirar:** si de una librería instalada no se encuentra versión en ninguno de los tres sitios, se avisa una vez (no bloquea) con un texto nuevo `eventos_chat_sin_version`, en español e inglés.
- [x] Pruebas con un `.venv` **real** creado en una carpeta temporal y el hook corriendo con el Python del sistema (lección de 2026-11-08).

## 3. Fuera de alcance
- Entornos con otro nombre u otra ruta (`env`, `.env`, `../venv`, conda, poetry fuera del proyecto): caen en 2) o 3), y si no hay versión, avisa.
- Instalaciones en una carpeta distinta de la raíz del proyecto (`cd sub && pip install`).
- npm, cargo y go (siguen sin revisarse solos, como en la spec 027).

## 4. Verificación
- `python -m unittest discover tests` en verde, con las pruebas nuevas.
- Darwin: repetir la prueba de Modelo #59 en un proyecto con `.venv` (instalar `django==3.2` en el venv y `git push`): debe detenerse.

## 5. Cierre
- [x] Spec aprobada por Darwin antes de programar
- [x] Línea en `.brain/decisions.log`
- [x] Punto 28 de pendientes pasa a «Esperando tu prueba»
