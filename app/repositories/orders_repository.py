from ..config import paths
from ..domain import Order
from ..utils import (json_handler, check_and_convert_number_to_float)
import json

class OrderRepository:
    """
    Responsável pela persistência dos pedidos no sistema.
    """
    def __repr__(self):
        return 'Classe contendo dicionário com todos os objetos Pedido, e métodos para add, del, buscar, listar.'

    #BUSINESS METHODS
    @staticmethod
    def export_order(order: Order):
        order_n = order.order_n
        json_handler.save_to(paths.EXPORT_ORDER_JASON/f'order_{order_n}_export.json', order.to_dict())

    @staticmethod
    def _push_orders_list(orders_list: list[dict]):
        json_handler.save_to(paths.REPOSITORY_ORDERS_JSON, orders_list)

    @staticmethod
    def _get_orders_list(empty_ignore=False) -> list[dict]:
        try:
            temp_list = json_handler.read_from(paths.REPOSITORY_ORDERS_JSON)
        except (FileNotFoundError, json.JSONDecodeError):
            if empty_ignore:
                temp_list = []
            else:
                raise FileNotFoundError('Não há pedidos salvos.')
        return temp_list

    def save_order(self, order: Order):
        if not isinstance(order, Order):
            raise ValueError('PEDIDOREPOSITORY_SALVAR: Pedido deve ser instância de Pedido')
        temp_list = self._get_orders_list(empty_ignore=True)
        temp_list.append(order.to_dict())
        self._push_orders_list(temp_list)
        return True

    def delete_order(self, order_n: int):
        temp_list = self._get_orders_list()
        for idx, order in enumerate(temp_list):
            if order['order_n'] == order_n:
                del temp_list[idx]
                self._push_orders_list(temp_list)
                return True
        raise KeyError('PEDIDOREPOSITORY_DELETAR: Pedido não encontrado.')

    def replace_order(self, old_order: Order, new_order: Order | None=None):
        if new_order is None:
            new_order = old_order

        temp_list = self._get_orders_list()

        for idx, order in enumerate(temp_list):
            if order['order_n'] == old_order.order_n:
                temp_list[idx] = new_order.to_dict()
                self._push_orders_list(temp_list)
        return True

    def list_orders(self) -> list[dict]:
        return self._get_orders_list()

    def find_order(self, order_n: int) -> Order:
        order_n = check_and_convert_number_to_float(order_n)

        if order_n % 1 != 0:
            raise KeyError('PEDIDOREPOSITORY_BUSCAR: Número de pedido inválido.')

        temp_list = self._get_orders_list()
        for order in temp_list:
            if int(order_n) == order['order_n']:
                return Order.from_dict(order)
        raise KeyError('PEDIDOREPOSITORY_BUSCAR: Pedido não encontrado.')
