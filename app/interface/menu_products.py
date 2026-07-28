from .outputs import *
from .inputs import *
from ..services.orderservice import OrderService
import os

    #PRODUCTS MENU
class SubMenuProducts:
    """
    Representa o submenu responsável pelas operações relacionadas aos produtos.
    """

    def __init__(self, service: OrderService):
        self.service = service


    def create_product(self):
        os.system('cls')
        print('CADASTRANDO NOVO PRODUTO')
        prod_name = ask_product_name()
        prod_price = ask_product_price()
        if not prod_name or not prod_price:
            show_invalid_input()
            return

        self.service.create_product({'name': prod_name, 'price': prod_price})
        show_success_product_create()
        return

    def delete_product(self):
        os.system('cls')
        print('REMOVENDO PRODUTO DO SISTEMA')
        product_name = ask_product_name()
        product = self.service.find_product(product_name)
        if not product:
            show_invalid_input()
            return

        inpt_choose = ask_confirm_product_deletion(product.name)
        if not inpt_choose:
            show_invalid_input()
            return

        if inpt_choose == '2':
            show_abort_operation()
            return

        self.service.delete_product(product)
        show_success_product_deletion()
        ask_press_any_key_to_continue()

    def edit_product(self):
        os.system('cls')
        print('EDITANDO PRODUTO')
        product_name = ask_product_name()
        product = self.service.find_product(product_name)

        show_product_details(product)

        changes = {}
        for act_name, act in ask_field_to_edit():
            if act is False: #False representa a opção de cancelar edição
                show_abort_operation()
                return
            changes[act_name] = act()

        if self.service.edit_product(product, changes) is False:
            show_product_already_exists()
            return
        show_success_product_update()

    def list_products(self):
        os.system('cls')
        print('LISTANDO TODOS OS PRODUTOS DO SISTEMA')
        show_products_list(self.service.list_products())

        ask_press_any_key_to_continue()