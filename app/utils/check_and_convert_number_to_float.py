
def check_and_convert_number_to_float(inpt_str: str) -> float|None:
    """
    Checa se o input são números válidos e converte para float.
    Returns:
        float: Retorna o número convertido em float()
        None: Caso gere ValueError na conversão.
    """
    try:
        number = float(inpt_str)
    except ValueError:
        return None
    return number