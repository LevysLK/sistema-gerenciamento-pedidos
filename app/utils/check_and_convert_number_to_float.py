
def check_and_convert_number_to_float(inpt_str: str, cls=None) -> float:
    """
    Checa se o input são números válidos e converte para float.
    cls=Forneça a classe para que a mensagem de erro tenha um melhor rastreio em caso de ocorrência.
    Returns:
        float: Retorna o número convertido em float()
    """
    try:
        inpt_str = float(inpt_str)
    except:
        raise ValueError(
            f'Número inválido: {inpt_str!r}'
            if cls is None
            else f'{cls.__name__.upper()}: Número inválido {inpt_str!r}'
        )
    return inpt_str