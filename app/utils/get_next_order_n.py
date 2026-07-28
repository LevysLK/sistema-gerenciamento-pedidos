import json
from app.config import paths
from app.config import configs
from .json_handler import read_from


def get_next_order_n_json() -> int:
    """
    Lê do arquivo JSON qual é o número do último pedido e retorna o próximo como int().

    Caso o arquivo ainda não exista, ou não contenha pedidos, retorna o número inicial configurado.
    """
    order_n = configs.INITIAL_ORDERS_NUMBER

    try:
        order_list = read_from(paths.REPOSITORY_ORDERS_JSON)
        if order_list:
            return max(x['order_n'] for x in order_list) + 1
        return order_n

    except FileNotFoundError:
        return order_n
    except  json.JSONDecodeError as error:
        raise RuntimeError(
            "O arquivo de pedidos contém um JSON inválido."
        ) from error


if configs.REPOSITORY_TYPE == 'json':
    get_next_order_n_act = get_next_order_n_json