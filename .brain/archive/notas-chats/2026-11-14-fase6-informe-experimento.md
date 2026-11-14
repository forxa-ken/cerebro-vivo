# Informe del experimento de la fase 6 (spec 050), chat #26, 2026-11-14

**Dónde:** copia desechable `F:\Proyectos Antigravity\vmware-automatizacion-fase6`, rama `linea/fase6-experimento` (commit `6321af5`, sin remoto). Informe de entrega y evidencia dentro de la copia: `.brain/fabrica/informe.md`, `.brain/fabrica/evidencia/R1.md` y `R1/`. El proyecto original no se tocó (0 cambios). Nada subido.

## Resumen llano
La línea construyó la orden `renombrar_vm` (renombrar una máquina del laboratorio en memoria) y otra IA la probó de verdad con 30 casos más un script: **verde**. Pero **la línea tuvo que parar una vez** (el revisor de spec rechazó 3 veces y el freno saltó) y descubrimos 4 fallos del propio arnés. Resultado: el modo automático funciona de punta a punta, no se aprueba solo y los frenos funcionan, pero aún tiene aristas.

## Medidas
- **¿Resultado esperado?** Sí: criterio de `esperado.md` cumplido en uso real (consola y proceso único). Sin probar por Darwin; lo que no se juzga: si los mensajes de error se entienden.
- **Paradas:** 1 (spec rechazada 3 veces por Codex; el guardián `vueltas` salió con 1). Se siguió en la copia por desviación declarada (la directora resolvió con la opción conservadora); en un proyecto real habría esperado a Darwin. 0 fallos de la ejecutora (reintentos 0 de 3), sin atasco.
- **Decisiones propias de la línea:** nombre igual al viejo se rechaza; más de un `=` es formato malo; recorte de espacios en los extremos; ensayo fallido anotado solo para `renombrar_vm`; «prueba de uso real» sacada de la spec como requisito de producto; criterio `esperado.md` corregido antes de construir (el laboratorio se reinicia en cada comando de consola).
- **Gasto:** ejecutora Sonnet 72.113 tokens, probador Opus 90.644, Codex (revisor, 5 llamadas) ≈ 115.000 no anotados en la carta; directora no medido. Tiempo: unos 12 minutos de reloj (15:44 a 15:56), la revisión de spec fue lo más lento (Codex sin poder leer archivos, 5 intentos).
- **Lo que no pudo probar:** comprensión de mensajes; perfil prod (no existe); el revisor de spec con specs dañadas a propósito (fase 2 sigue sin probar con repeticiones); Darwin no ha probado nada.

## Hallazgos del arnés (para pendientes)
1. **Pruebas `.en.md` tras `actualizar`:** en proyectos en español fallan 5 pruebas copiadas del arnés (`test_diapositivas`, `ArrancarTest`, `EntregarTest`, `InformeTest` de `test_fabrica`, y una de Mac preexistente) porque leen plantillas `.en.md` que no llegan. Decidir: que se salten sin la edición en inglés, o que `actualizar` las traiga.
2. **Guardián `alcance`:** solo reconoce requisitos `R1` (regex `\bR\d+\b`), no `R-1` como pide la plantilla; y cuenta como ajenas las ediciones de la directora a spec y encargo hechas después de la `foto`.
3. **Revisor de spec:** severo por deporte (3 de sus hallazgos pedían justificar convenciones heredadas) pero con hallazgos buenos (nombre igual, `=` en nombres, contradicción real con el motor: no anota ensayos fallidos). Con Codex, la caja no lee archivos: hay que pasarle el texto en la orden (-s read-only) y guardar yo el veredicto. Dos veredictos sin cita no contaron, como debe ser.
4. **Procedencia del negocio:** el revisor rechazó la primera vez por «negocio sin aprobación de Darwin»; en un uso real el negocio lo escribe él.
5. **Copia a medio actualizar:** el traspaso decía «actualizado» pero la copia estaba en 1.29.2 con 91 fallos; hubo que repetir `actualizar.py`. Comprobar siempre `arnes_instalado.json` y correr las pruebas.
6. Rarezas del producto (no pedidas): nombres que solo difieren en mayúsculas, espacios internos, orden del listado.
