# -*- coding: utf-8 -*-
"""Las 5 preguntas de la spec 004 y cómo se comprueba cada respuesta. Respuestas sacadas de las fichas de LoboHook
(D-062, D-054, D-055); la 5 no consta en ningún archivo."""
import re

# (texto, [patrones que TODOS deben aparecer], [patrones prohibidos])
PREGUNTAS = {
    1: ("¿Cuántos créditos y a qué precio es el pack de recarga M de créditos de IA?",
        [r"10[.\s]?000", r"9[.,]99"], []),
    2: ("¿Cuántos flujos de botones y cuántas acciones permite el plan Esencial?",
        [r"\b15\b", r"\b8\b"], []),
    3: ("¿Qué identificadores tienen las cuentas de prueba y por qué no chocan con uno real de Discord?",
        [r"001", r"006", r"(15|quince) ceros"], []),
    4: ("¿Cuántos días de aviso exige cambiar la tabla de consumo de créditos de IA?",
        [r"\b30\b"], []),
    5: ("¿Qué se decidió sobre el pago con Bizum?",
        [r"(?i)no consta|no figura|no aparece|no hay (ninguna )?(decisi|referencia|nada)|no se (ha )?(decidi|encontr|menciona)|no encontr"],
        [r"(?i)se decidi[óo] (aceptar|usar|a[ñn]adir|que)"]),
}

FORMATO = "Responde en una o dos frases. Si no consta en la memoria del proyecto, di «no consta»."


def juzgar(n, respuesta):
    """Devuelve 'acierta', 'falla' o 'inventa' (solo en la pregunta sin respuesta)."""
    _, debe, prohibido = PREGUNTAS[n]
    ok = all(re.search(p, respuesta) for p in debe) and not any(re.search(p, respuesta) for p in prohibido)
    if ok:
        return "acierta"
    return "inventa" if n == 5 else "falla"
