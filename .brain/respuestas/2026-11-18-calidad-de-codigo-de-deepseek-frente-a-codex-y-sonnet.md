# Calidad de código de DeepSeek frente a Codex y Sonnet

- **Fuente:** chat cerebro-vivo #35, prueba con Darwin
- **Fecha:** 2026-11-18

Encargo: `inventario.py` (gestor con JSON, escritura atómica, errores, CLI) más `test_inventario.py`, tope de 30k tokens. Una sola ejecución de cada uno. Los tres pasan el comprobador con casos difíciles (JSON corrupto sin sobrescribir, flotantes, emojis, CLI).

- DeepSeek V4.1 Flash Free: 17 s, ~12.700 tokens, 18 pruebas propias.
- Codex high: 118 s, 13.443 tokens, 19 pruebas propias.
- Sonnet 5.5: ~27 s, 12 pruebas propias.

Revisión a ciegas (subagente Sonnet de solo lectura, autores ocultos; fidelidad / corrección / robustez / legibilidad / pruebas):
- Codex high: 8 / 9 / 9 / 6 / 9, primera. Guarda primero a disco y actualiza la memoria solo si va bien; CLI siempre código 1. Defecto: algo sobreingeniado y carga muy estricta.
- DeepSeek: 8 / 6 / 6 / 8 / 6, segunda. Muta la memoria antes de guardar; carga acepta cantidad 0 y no valida el precio; errores de argparse salen con código 2 en vez de 1.
- Sonnet: 8 / 6 / 5 / 7 / 5, tercera. Redondeo bancario en `valor_total`, código muerto, pruebas de CLI superficiales.

Lectura: DeepSeek es correcto en lo pedido y muy rápido, pero tiene más huecos en robustez que Codex; por eso la skill exige revisión aparte con DeepSeek. Límites: una ejecución cada uno y el revisor es también Sonnet.

Internet (fuentes de terceros, cifras en parte de DeepSeek): cerca de los mejores en SWE-bench (~79-81 %), peor en pruebas más duras y en cambios grandes y ambiguos; 4-8 veces más barato. La versión gratuita de OpenCode figura como «por tiempo limitado»; que no retiene ni entrena con los datos viene de resúmenes de terceros, sin confirmar en la página oficial.
