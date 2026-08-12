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
        product_name = ask_product_name()
        if product_name is None:
            show_invalid_input()
            return

        self.service.create_product({'name': prod_name, 'price': prod_price})
        show_success_product_create()
        return

    def delete_product(self):
        os.system('cls')
        print('REMOVENDO PRODUTO DO SISTEMA')
        product_name = ask_product_name()
        if product_name is None:
            show_invalid_input()
            return

        product = self._find_product_or_show_error(product_name)
        if product is None:
            return

        while True:
            inpt_choose = ask_confirm_product_deletion(product.name)
            if not inpt_choose:
                show_invalid_input()
                continue
            break

        if inpt_choose == '2':
            show_abort_operation()
            return

        self.service.delete_product(product)
        show_success_product_deletion()
        ask_press_enter_to_continue()

    def edit_product(self):
        os.system('cls')
        print('EDITANDO PRODUTO')

        product_name = ask_product_name()
        if product_name is None:
                    show_invalid_input()
                    return

        try:
            product = self.service.find_product(product_name)
        except KeyError:
            show_not_found_product()
            return

        show_product_details(product)

        changes = {}
        for act_name, act in ask_field_to_edit():
            if not act: #False representa a opção de cancelar edição
                show_abort_operation()
                return
            changes[act_name] = act()

        if not self.service.edit_product(product, changes):
            show_product_already_exists()
            return
        show_success_product_update()

    def list_products(self):
        os.system('cls')
        print('LISTANDO TODOS OS PRODUTOS DO SISTEMA')
        show_products_list(self.service.list_products())

        ask_press_enter_to_continue()