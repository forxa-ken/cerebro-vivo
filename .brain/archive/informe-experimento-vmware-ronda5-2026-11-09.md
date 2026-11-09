# Informe ronda 5 (mantenimiento: «mover disco») — 2026-11-09
Claude (cerebro-vivo #35). Muestra de 1 por rama; tendencia, no prueba. Ramas C (ODD + reglas) y D (Cerebro Vivo + reglas), sesiones nuevas sin memoria sobre el módulo Discos de la ronda 4. Solo laboratorio en memoria; nada a GitHub.

| | C (ODD + reglas) | D (Cerebro + reglas) |
|---|---|---|
| Función hecha, criterios 1-7 | sí | sí |
| Pruebas | 95 OK (38 nuevas) | 377 OK salvo `test_soporte_mac` (ajena) |
| Coste (`medir.py`) | ≈ 383k | ≈ 377k |
| Salida / turnos | 32k / 13 | 24k / 16 |
| Cambios en el código | 8 archivos, +548 | spec 003 + 5 archivos de código, 615 líneas en total |
| Orientación | ~15 archivos, sin tropiezos | ~10 lecturas; faltó lista de quién usa `espacio_libre_gb` |
| Dejó a futuro | resultado.md con «notas de retoma» | spec 003, lección, resultado.md |

## Seguridad (`experimento-vmware/prueba_seguridad_ronda5.py`, casos fijados antes)
- Servidor falso mínimo: estado desconocido o raro, encendida, grande, espacio del destino desconocido -> **las dos BLOQUEAN** (0 acciones sin permiso).
- Destino sin espacio y mismo almacén, con `--confirmo`: C da error claro desde el motor; D **deja que lo decida el servidor** (con mi servidor falso, que no valida, ejecutó). Contra el laboratorio real D da error claro. Matiz de diseño, no fallo de permiso: pasa solo con visto bueno dado.
- No se repitió la regresión de añadir/ampliar/quitar con servidor falso; las suites previas siguen en verde en ambas.

## Lectura
Empate en coste y en calidad. Cerebro Vivo (D) dejó más rastro (spec, lección) y lo notó al orientarse (pidió la spec archivada); ODD se orientó con el `resultado.md` anterior. La ventaja de la memoria **no se ve en una sola retoma**. Falta una segunda retoma (o más muestras) para saberlo.
