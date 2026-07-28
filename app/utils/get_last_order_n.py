import json
from app.config import paths
from app.config import configs
from .json_handler import read_from


def get_last_order_n_json() -> int:
    """
    Lê do arquivo JSON qual é o número do último pedido e retorna como int()
    """
    order_n = configs.INITIAL_ORDERS_NUMBER
    try:
        order_list = read_from(paths.REPOSITORY_ORDERS_JSON)
        if len(order_list) > 0:
            order_n = order_list[-1]['order_n'] + 1
        return order_n
    except (FileNotFoundError, json.JSONDecodeError):
        return order_n


if configs.REPOSITORY_TYPE == 'json':
    get_last_order_n = get_last_order_n_json