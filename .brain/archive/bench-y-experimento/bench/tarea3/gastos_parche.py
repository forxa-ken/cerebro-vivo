
def exportar_json(gastos, ruta):
    """A MEDIAS: escribe un JSON con los gastos. Falta el formato acordado."""
    import json
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(gastos, f)
