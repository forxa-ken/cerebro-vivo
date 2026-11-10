# Diario de la prueba R13: una fábrica de IA que mejora un programa de verdad

Este diario cuenta, día a día y en lenguaje llano, qué se hizo, por qué y qué salió. Sirve de materia prima para explicarlo en la página pública, de forma que lo entienda cualquier persona, sin saber informática. Se escribe en orden y no se borra nada: lo nuevo se añade al final.

## Idea en dos frases
Una IA «directora» reparte el trabajo como un jefe de obra: escribe qué hay que hacer, otra IA («la obrera», Codex) lo hace, y una tercera («la revisora») lo comprueba con ojos nuevos. La persona (Darwin) decide y firma; el dinero (los «tokens», lo que cuesta pensar a una IA) tiene topes.

## Cómo se explica cada pieza a una persona mayor
- **Directora:** la que planifica y revisa, como quien dirige una reforma.
- **Obrera (Codex):** hace una tarea concreta y se retira. No ve el conjunto.
- **Revisora:** otra IA que no hizo el trabajo y lo mira con la lupa; así nadie se corrige a sí mismo.
- **Encargo:** una hoja con una sola tarea pequeña, con lo que se puede y no se puede tocar.
- **Carta:** las reglas del juego firmadas por Darwin (qué está prohibido, cuánto se puede gastar).
- **Tokens:** como los minutos de una llamada: cada pensamiento de la IA gasta y hay un tope.
- **Ventana de 200.000 tokens:** la memoria de trabajo de la IA; cuando se llena, hay que pasar apuntes a una IA nueva («traspaso»).

## 10 de noviembre de 2026

### Qué se hizo (por la mañana)
- Programa de prueba: **TraductorVoz**, que escucha un audio y pone subtítulos traducidos en pantalla.
- Se le pidió a la fábrica reorganizar el programa por dentro en tres partes (entrada de sonido, cerebro, salida de subtítulos) **sin cambiar lo que hace**.
- Seis encargos pequeños a Codex (001 a 006). La revisora independiente los miró: «apto con reparos»; los reparos se arreglaron en el encargo 006.
- Gasto de Codex: unos 510.000 tokens de un millón permitido; el encargo más grande usó 134.000, por debajo de la ventana de 200.000.
- Resultado: 40 pruebas automáticas en verde.

### Qué se hizo (por la tarde)
- **Prueba con un audio real, antes y después.** Mismo audio, programa antiguo contra programa reorganizado: 8 frases idénticas en texto, traducción, idioma y persona que habla. Un 3 % más rápido. La reorganización no estropeó nada.
- **Corrección de un dato propio:** se había anotado que ese audio tenía 2 voces; en realidad tiene 4. Se corrigió en la evidencia. Lección: contrastar lo anotado con lo real.
- **Prueba de Darwin con la ventana real** del programa (5 minutos): alemán, francés y chino; sin fallos comunicados.

### Un hallazgo que salió por casualidad
- Con un audio en alemán (dos voces, una mujer dice una sola frase hacia el segundo 18) el programa detecta bien el idioma y traduce bien, pero **no distingue quién habla**: pone a las dos personas como «hablante 1».
- Causa explicada en llano: el programa corta el audio en frases cuando hay un silencio, y pone una sola «huella de voz» por frase. Si dos personas hablan seguidas, sin pausa, caen en la misma frase.
- Con un vídeo de aprendizaje de alemán (origen: YouTube, desde el minuto 1:58) pasó lo mismo: casi todo «hablante 1», y alguna frase con dos personas dentro.
- Una idea sencilla (mirar la voz cada pocos segundos) resultó demasiado ruidosa. Una vía más prometedora (un modelo que detecta quién habla en cada instante) está por investigar y por comprobar su licencia. **Pendiente 39.**

### Decisiones y su porqué
- **El desarrollo del programa continúa en su propio proyecto**, no en el cerebro general. La fábrica ya cumplió su objetivo (verla funcionar de principio a fin). Se creó un chat propio de TraductorVoz con una «directora» que ya tiene todo el contexto.
- **Codex no tiene chat visible.** Trabaja por comandos, sin ventana: la directora lo lanza, él escribe una nota y un archivo de registro, y se apaga. Todo queda en esos archivos, que es lo que se puede enseñar.
- **El cambio de chat lo hace la directora,** no Codex. Codex solo debe parar y dejar sus apuntes si se le llena la ventana; no tiene aviso automático (Claude sí). Por eso hay que probarlo.
- **Prueba B (pendiente 19):** un encargo grande y controlado, con tope de gasto bajo, para forzar a propósito que Codex llene la ventana y comprobar que para, deja los apuntes y la directora relanza el trabajo.
- Nada se sube a internet ni se descarga sin permiso de Darwin. Las claves personales las pega él.

### Qué salió mal o fue incómodo (también se cuenta)
- No existía el chat del traductor: todo el trabajo se había hecho desde otros chats. Se creó hoy.
- La clave del servicio de traducción en la nube (DeepL) no estaba guardada en el programa; Darwin la recuperó de su cuenta.
- Un guardián de la fábrica solo comprueba el gasto **después** de cada encargo, no durante: no puede cortar a la obrera a mitad de trabajo.

### Qué falta
- Prueba B del pendiente 19 (ventana llena de Codex y chat nuevo).
- Investigar la separación de voces (pendiente 39), con carta nueva firmada por Darwin.
- Informe final de R13: gasto por papel y lecciones. Después, actualizar el pendiente 19.

### Prueba B: ¿qué pasa cuando a la obrera se le acaba el espacio? (tarde del 10-nov)
- **Qué se quería ver:** que la obrera (Codex), al quedarse sin espacio de trabajo, pare, deje apuntes y que otra obrera nueva siga donde lo dejó la anterior, sin repetir nada.
- **Qué se hizo:** un encargo grande (nº 007): escribir pruebas automáticas para 9 módulos del programa, con una parada ordenada a mitad (después del módulo 4).
- **Qué pasó:** la primera Codex paró sola en ese punto y dejó sus apuntes escritos. La directora lanzó una Codex nueva dándole solo esos apuntes, y esta siguió desde el módulo 5 hasta el 9 sin rehacer nada. **El relevo funcionó.**
- **Lo que NO se pudo comprobar:** el espacio de 200.000 no llegó a llenarse (la primera obrera usó 113.000). La parada fue ordenada, no forzada. Si Codex avisa por sí sola cuando de verdad se le llena la memoria sigue sin saberse («no concluyente»).
- **Dinero:** el tope del encargo era 150.000 y se gastaron 187.785. Se pasó porque el guardián solo cuenta después de cada tanda: no puede cortar a mitad. Era un riesgo ya conocido y se confirmó. Total de la fábrica: unos 698.000 de 1.000.000.
- **Estado del trabajo:** 70 pruebas, 69 bien y 1 error en una prueba nueva (parece fallo de la propia prueba, sin confirmar). Todo en una rama aparte, sin mezclar con el programa.
- **Lección:** la «foto» de control del guardián se tomó sobre la carpeta equivocada; hay que tomarla sobre la carpeta de trabajo de la obrera antes de lanzar.
- **Qué falta (lo decide Darwin):** si se acepta pasarse del tope, arreglar esa prueba, revisión independiente y mezclar. Y si quiere un encargo aún mayor para ver el aviso de ventana llena de verdad.

### Cierre del encargo 007 (10-nov)
- **Qué se hizo:** Darwin autorizó pasarse del tope de gasto. Una tercera Codex, pequeña, arregló la única prueba que fallaba (le faltaba un dato que el programa sí tiene). Las 70 pruebas pasaron y el trabajo se mezcló con el programa, solo en el ordenador de Darwin.
- **Dinero:** 228.505 tokens contra un tope de 150.000, pasado con permiso. Total de la fábrica: unos 739.000 de 1.000.000.
- **Por qué sin revisora:** el encargo solo añade pruebas y no toca el programa. Queda a elección de Darwin pedir la revisión igualmente.
- **Qué quedó demostrado:** el relevo entre obreras funciona con solo unos apuntes escritos. **Qué no:** el aviso automático cuando de verdad se llena la memoria.

### Decisión de cierre sobre la ventana llena (10-nov)
- Darwin preguntó si no se estaba complicando demasiado. Se vio que sí: construir un vigilante que corte a Codex en vivo es trabajo nuevo y sin comprobar, y el único desbordamiento real fue de unos 38.000 tokens (poco dinero).
- **Se decidió** dejarlo simple: tope de 200.000 por tanda, encargos pequeños y el guardián que mira el gasto al terminar cada tanda. Si algún día un desbordamiento cuesta caro, se construye el vigilante.
- **Un detalle aprendido:** que el arnés esté instalado en Codex sirve para escribir y leer los apuntes, pero Codex no ejecuta avisos automáticos como Claude, y no abre chats: eso lo hace la directora, con una orden nueva.

## Cómo seguir este diario
Cada entrada nueva lleva fecha, y responde a: qué se hizo, por qué, qué salió mal, qué falta. Lenguaje de calle; si hay una palabra técnica, va con su explicación al lado.

## 10 de noviembre de 2026 (tarde) · La directora del traductor prepara la prueba B

### Qué se hizo
- La directora (la IA que reparte el trabajo) abrió su propio chat dentro del proyecto del traductor, leyó los apuntes que le dejó el chat anterior y le contó a Darwin cómo está todo: seis encargos hechos y revisados, 40 pruebas automáticas en verde, y un problema pendiente (el programa no separa bien las voces de dos personas que hablan seguidas).
- Escribió el borrador del encargo 007 y de su carta (el documento con las reglas y los topes de gasto). Es un encargo grande a propósito: pedir a Codex que escriba muchas pruebas automáticas para casi todo el programa, de modo que tenga que leer tanto que su «ventana» (la memoria de trabajo de la IA, que se llena) se llene de verdad.

### Por qué
- Hay que comprobar un caso que aún no se ha visto: qué hace Codex cuando se le llena la memoria. Debe parar solo, dejar apuntes escritos y que la directora abra un chat nuevo de Codex que siga donde se quedó. Los seis encargos anteriores fueron demasiado pequeños para llenarla.
- Es un trabajo útil y sin riesgo: solo añade pruebas, no cambia cómo funciona el programa, no descarga nada ni usa internet.

### Qué salió mal o fue incómodo
- El nombre «prueba B» solo existía en la conversación con Darwin, no en ningún archivo; hubo que preguntarle al otro chat qué decía exactamente.
- El control de gasto solo mira al terminar el encargo, no durante. Por eso el tope se puso bajo (300.000 de un millón) y la directora revisará el consumo cuando se llene cada ventana.
- Las reglas actuales eran un borrador y prohíben cosas nuevas; por eso hace falta una carta nueva que firme Darwin antes de lanzar a nadie.

### Qué falta
- Que Darwin firme la carta 007 y apruebe el encargo. Hasta entonces no se lanza a Codex.
- Después de la prueba B, la separación de voces, con su propia carta (necesitará descargar un modelo nuevo, y eso solo con el sí de Darwin).
