# Spec 030: el guardián con memoria del chat olvida lo que no está instalado y no confunde `2>&1` con una librería

- **Estado:** pedida por Darwin el 2026-11-08 («lo vamos a arreglar, no se puede dejar así»); programada en 1.28.5
- **Origen:** informe de Modelo #59 tras la spec 029. El guardián ya detiene el push con `django==3.2`, pero (a) siguió bloqueando después de desinstalar django o de que la orden se detuviera antes de ejecutarse, sin forma de limpiarlo salvo `permitir` o un chat nuevo; (b) el aviso decía «se instalaron librerías (2)»: el «2» era `2>&1` de la orden, tomado por el nombre de una librería.

## 1. En alcance
- Antes de apuntar la orden actual, se quita del recuerdo del chat lo que no está instalado ni en el `.venv`/`venv` del proyecto ni en el Python del hook (pendientes, versiones fijadas y bloqueos). Solo actúa si hay entorno virtual. Lo que instala la propia orden en curso se sigue revisando (se purga antes de apuntarla).
- Las redirecciones (`2>&1`, `>fichero`, `2>/dev/null`) ya no cuentan como nombre de librería.

## 2. Fuera de alcance
- Comando manual «olvidar»: no hace falta, el recuerdo se limpia solo. `permitir` sigue igual.
- Entornos sin `.venv`/`venv` en la raíz: se comportan como antes.

## 3. Verificación
- `python -m unittest discover tests` en verde (3 pruebas nuevas, con `.venv` real).
- Darwin/Modelo #59: tras `pip uninstall django`, un `git push` pasa sin aviso; con django 3.2 instalado sigue deteniéndose.
