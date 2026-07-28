from .outputs import *
from .inputs import *
from ..domain import Order
from ..services.orderservice import OrderService
import os

    #ORDERS MENU
class SubMenuOrders:
    """
    Representa o submenu responsável pelas operações relacionadas aos pedidos.
    """
    def __init__(self, service: OrderService):
        self.service = service
        self.current_order = None


    def create_order(self):
        os.system('cls')
        print('CRIANDO NOVO PEDIDO')
        name = ask_customer_name()
        email = ask_customer_email()
        if not name or not email:
            show_invalid_input()
            return

        order_number = self.service.create_order({'name': name, 'email': email})
        show_success_order_create(order_number)

        while True:
            inpt_choose = ask_add_itens_or_go_menu()
            if not inpt_choose:
                show_invalid_input()
                continue
            break

        if inpt_choose == '1':
            self.current_order = order_number
        return

    def add_item(self):
        os.system('cls')
        print('ADICIONANDO ITENS AO PEDIDO')
        products_list = self.service.list_products()
        if not products_list:
            show_empty_products_rep()
            return

        if self.current_order is None:
            order_n = ask_order_number()
            order = self.service.find_order(order_n)
            if not isinstance(order, Order):
                show_not_find_order()
                return
            self.current_order = order_n
        else:
            order = self.service.find_order(self.current_order)

        if order.order_status in ('finalizado', 'cancelado'):
            show_order_error('cancelado')
            return

        print(
            f''
            f'ADICIONAR AO PEDIDO nº{self.current_order}:'
            f'\n'
            f'Lista de produtos:'
            )
        show_products_list(products_list)

        while True:
            product_choose = ask_product_name()
            product_qtty = ask_product_qtty()

            if not product_choose or not product_qtty:
                show_invalid_input()
                continue

            product = self.service.find_product(product_choose)

            self.service.add_item(product, product_qtty, order)
            show_success_add_item(product_choose)

            while True:
                inpt_choose = ask_add_more_itens()
                if not inpt_choose:
                    show_invalid_input()
                    continue
                break

            if inpt_choose == '1':
                continue

            show_abort_operation()
            return

    def remove_item(self):
        os.system('cls')
        print('REMOVENDO ITENS DO PEDIDO')
        order_n = ask_order_number()
        order = self.service.find_order(order_n)
        if order.order_status in ('finalizado', 'cancelado'):
            show_order_error(order.order_status)
            return

        if not order.itens:
            show_empty_products_rep()
            return

        show_order_items_list(order)

        item_name = ask_product_name()
        if item_name in order.itens:
            if ask_confirm_product_deletion(item_name) == '1':
                self.service.remove_item(order, item_name)
                show_success_item_remove()

                ask_press_any_key_to_continue()
                return
            show_abort_operation()
            return
        show_invalid_input()

    def find_order(self):
        os.system('cls')
        print('BUSCANDO PEDIDO')
        order_n = ask_order_number()
        order = self.service.find_order(order_n)

        show_order_details(order)
        ask_press_any_key_to_continue()
        return

    def list_orders(self):
        os.system('cls')
        print('LISTANDO TODOS OS PEDIDOS NO SISTEMA')
        show_all_orders(self.service.list_all_orders())
        ask_press_any_key_to_continue()
        return

    def export_order(self):
        os.system('cls')
        print('EXPORTANDO PEDIDO')
        order_n = ask_order_number()

        order = self.service.find_order(order_n)
        self.service.export_order(order)
        show_success_order_export(order_n)
        return

    def complete_order(self):
        os.system('cls')
        print('FINALIZANDO PEDIDO')
        order_n = ask_order_number()

        order = self.service.find_order(order_n)
        if order.order_status in ('finalizado', 'cancelado'):
            show_order_error(order.order_status)
            return

        show_order_details(order)
        print()

        pay_methods = self.service.list_all_payment_methods()
        show_all_payment_methods(pay_methods)
        menu_n = ask_menu_choose()
        if menu_n not in pay_methods:
            show_invalid_input()
            return

        pay_choose = pay_methods[menu_n]

        order = self.service.set_payment_method(order, pay_choose)
        print(f'Forma de pagamento selecionada: {pay_choose}')
        show_success_set_payment_method()
        
        while True:
            inpt_choose = ask_confirm_payment()
            if not inpt_choose:
                show_invalid_input()
                continue
            break

        if inpt_choose == '1':
            if self.service.complete_order(order) is True:
                show_success_complete_order()
                ask_press_any_key_to_continue()
                return
        show_abort_operation()
        return

    def cancel_order(self):
        os.system('cls')
        print('CANCELANDO PEDIDO')
        order_n = ask_order_number()
        
        order = self.service.find_order(order_n)
        if order.order_status in ('finalizado', 'cancelado'):
            show_order_error(order.order_status)
            return

        self.service.cancel_order(order)
        show_success_order_cancel()