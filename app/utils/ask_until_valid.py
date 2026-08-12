from collections.abc import Callable
from typing import TypeVar


ReturnType = TypeVar('ReturnType')

def ask_until_valid(ask_func: Callable[[], ReturnType | None], error_types: tuple[type[Exception], ...], error_output: Callable[[], None]) -> ReturnType:
    """
    Executa uma função de entrada até obter um resultado válido.

    Args:
        ask_func:
            Função sem parâmetros que retorna um valor ou None.
        error_types:
            Tupla contendo as exceções que devem ser tratadas.
        error_output:
            Função responsável por exibir a mensagem de erro 
            ao levantar exceção ou ask_func retornar None.
    Returns:
        ReturnType:
            Valor válido retornado por ask_func.
    """
    while True:
        try:
            func_rtn = ask_func()
        except error_types:
            error_output()
            continue

        if func_rtn is None:
            error_output()
            continue

        return func_rtn