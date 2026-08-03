from .inputs import (
    ask_menu_choose,
)

from .outputs import (
    show_invalid_input,
    )

from ..services.orderservice import OrderService
from .menu_orders import SubMenuOrders
from .menu_products import SubMenuProducts
import os
import time

class Menu:
    """
    Representa o menu principal responsável por coordenar a navegação entre os submenus,
    exibir as opções disponíveis e direcionar o fluxo da aplicação.
    """
    def __init__(self, service: OrderService):
        self.service = service
        self._orders_menu = SubMenuOrders(service)
        self._products_menu = SubMenuProducts(service)

        self._menu_dict = {
            'menu_title': 'MENU PRINCIPAL',

            '1': {
                'text': 'Menu de produtos.', 
                'action': '_sub_menu_products'
            },
            '2': {
                'text': 'Menu de pedidos.', 
                'action': '_sub_menu_orders'
            },
            '0': {
                'text': 'Sair', 
                'action': exit
            },
        }

        self._sub_menu_orders = {
            'menu_title': 'MENU DE PEDIDOS',

            '1': {
                'text': 'Criar pedido.', 
                'action': self._orders_menu.create_order
            },
            '2': {
                'text': 'Adicionar item ao pedido.', 
                'action': self._orders_menu.add_item
            },
            '3': {
                'text': 'Remover item do pedido.', 
                'action': self._orders_menu.remove_item
            },
            '4': {
                'text': 'Buscar pedido.', 
                'action': self._orders_menu.find_order
            },
            '5': {
                'text': 'Listar todos pedidos.', 
                'action': self._orders_menu.list_orders
            },
            '6': {
                'text': 'Reimprimir pedido.', 
                'action': self._orders_menu.export_order
            },
            '7': {
                'text': 'Concluir pedido.', 
                'action': self._orders_menu.complete_order
            },
            '8': {
                'text': 'Cancelar pedido.', 
                'action': self._orders_menu.cancel_order
            },
            '9': {
                'text': 'Voltar ao menu principal.', 
                'action': '_menu_dict'
            },
        }

        self._sub_menu_products = {
            'menu_title': 'MENU DE PRODUTOS',
            '1': {
                'text': 'Criar produto.', 
                'action': self._products_menu.create_product
            },
            '2': {
                'text': 'Deletar produto.', 
                'action': self._products_menu.delete_product
            },
            '3': {
                'text': 'Editar produto.', 
                'action': self._products_menu.edit_product
            },
            '4': {
                'text': 'Listar todos os produtos.', 
                'action': self._products_menu.list_products
            },
            '9': {
                'text': 'Voltar ao menu principal.', 
                'action': '_menu_dict'
            }
        }

    def __repr__(self):
        return f'Classe MENU que faz a execução dos menus em prompt e gerencia inputs/outputs.'

    #MENU FUNCTION
    def execute(self, menu_to_show=None):
        while True:
            if menu_to_show is None:
                menu_options = self._menu_dict
            else:
                menu_options = getattr(self, menu_to_show)

            os.system('cls')
            print(menu_options['menu_title'])

            for key, item in menu_options.items():
                if len(key) > 2: #pular exibição do 'menu_title' novamente.
                    continue
                print(f'{key}. {item["text"]}')
            print()

            while True:
                menu_key_choosed = ask_menu_choose()
                if menu_key_choosed not in menu_options or len(menu_key_choosed) > 2:
                    show_invalid_input()
                    continue
                break

            if isinstance(menu_options[menu_key_choosed]['action'], str): #se 'action' for str (no caso dos submenus) volta o loop para exibição do outro menu
                menu_to_show=menu_options[menu_key_choosed]['action']
                continue
            else:
                menu_options[menu_key_choosed]['action']()
                time.sleep(1.5)
                continue