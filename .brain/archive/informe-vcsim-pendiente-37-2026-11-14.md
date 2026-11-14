# Informe: reglas de seguridad contra `vcsim` (pendiente 37, punto a)

Claude (cerebro-vivo #23) para Darwin, 2026-11-14. **Sin servidor real. Una sola ejecución. Las pruebas las diseñé yo y yo escribí el adaptador: no hay un segundo par de ojos.**

## Qué se hizo
- Con el sí de Darwin se instaló Go 1.27.4 (winget), se compiló `vcsim` desde el código de govmomi (`go install ...@latest` falla por un `replace` en su `go.mod`; compilar el clon sí funciona) y `pip install pyvmomi`.
- Módulo probado: el ganador de la ronda 5 (Cerebro Vivo + reglas, `vmware-automatizacion-ronda5-D`, discos y mover disco).
- Nuevo en esa carpeta (sin commitear allí): `vmware_auto/vcsim.py` (adaptador con la misma interfaz que el laboratorio: `describir`, `ejecutar`, `estado_vm`, `tamano_disco`, `espacio_libre_almacen`) y `tests/test_vcsim_seguridad.py` (25 pruebas; cada una arranca su propio `vcsim` limpio; se saltan si no hay `vcsim.exe` o `pyvmomi`).
- **El motor (`motor.py`, `discos.py`) no se tocó.** Es la prueba: las mismas reglas, otro servidor.

## Resultado: 25 de 25 en verde, con un hallazgo
1. **Sin visto bueno no se toca nada (9 casos):** borrar máquina, apagar y reiniciar de golpe, borrar y restaurar instantánea, quitar disco, y ampliar, añadir o mover un disco con la máquina encendida. En todos se lanzó la confirmación requerida, el servidor quedó idéntico y el registro anotó «rechazada».
2. **Con visto bueno se ejecuta** (borrar máquina apagada, quitar disco, apagar).
3. **El ensayo (`--simular`) no cambió nada** en 7 acciones.
4. **Máquina apagada y cambio pequeño: sin visto bueno; grande (100 GB o más): con visto bueno.**
5. **Errores:** máquina, disco o almacén inexistentes, ampliar para encoger, y que el perfil `prod` no se cuela por `vcsim`: no actúan.
6. **Servidor que no sabe responder:** si el servidor no contesta `estado_vm`, `tamano_disco` o `espacio_libre_almacen`, el motor lo trata como delicado y pide visto bueno. **Esto cierra el hueco que A y B vieron en las rondas 2 y 3** (servidor sin ese método → pasaba sin visto bueno): en este módulo (D) ya está cerrado.
7. **Hallazgo nuevo:** `vcsim` responde «hecho» a `RelocateVM_Task` (mover disco) **sin mover nada** (probado con localizador de disco y con almacén a nivel de máquina). Un servidor que dice «hecho» sin hacerlo no lo detecta el motor: el registro habría anotado «hecho». Se añadió en el adaptador una **lectura de vuelta** que compara el resultado y falla si no coincide; la prueba lo fija.

## Lo que NO se probó (límites)
- Es un simulador (se presenta como vCenter 6.5), no un servidor real.
- Margen de destino de «mover disco» (los almacenes de `vcsim` son de 4 TB; el caso de poco espacio no se provoca).
- Instantáneas: las máquinas de `vcsim` no traen; solo se probó que sin visto bueno se rechazan, no que se borren con él.
- `apagar_ordenado`, discos «bloqueados» (no existe en vSphere) y la regla de «cambio en caliente» con el servidor real.
- Tests de concurrencia y la CLI con `vcsim` (la CLI solo conecta el laboratorio).

## Lectura para el método
- **Las reglas viven en el motor y por eso se trasladan:** el mismo motor protegió con otro servidor sin cambios. Es un dato a favor de «reglas explícitas en código, no en consejos».
- **La lectura de vuelta debería ser regla general** (verificar el efecto tras actuar), no un parche del adaptador: candidata a la skill `seguridad-en-sistemas-reales`.
- **Punto (c) del pendiente 37 (la regla «vcsim» del `AGENTS.md` del aprobador):** la contradicción ya estaba resuelta (línea 16 de `AGENTS.md`: el laboratorio en memoria es la forma aceptada en esa fase). Ahora que `vcsim` se instaló con el sí de Darwin, esa línea queda desfasada; conviene una frase que lo admita como segundo servidor. No lo he editado.
- Un fallo ajeno, `test_soporte_mac` (fin de línea de Windows) en esa copia del experimento; en el arnés ya se arregló en la 1.40.2.
