from collections.abc import Callable
from .outputs import *
from .inputs import *
from ..utils.ask_until_valid import ask_until_valid
from ..services.orderservice import OrderService
from ..config.configs import STATUS_CANCELED, STATUS_COMPLETED, STATUS_OPEN
import os

    #ORDERS MENU
class SubMenuOrders:
    """
    Representa o submenu responsável pelas operações relacionadas aos pedidos.
    """
    def __init__(self, service: OrderService):
        self.service = service
        self.current_order = None

    def _find_order_or_show_error(self, order_n: int) -> Order | None:
        try:
            return self.service.find_order(order_n)
        except (KeyError, ValueError):
            show_not_found_order()
        except FileNotFoundError:
            show_empty_orders_rep()
        return None

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

        if inpt_choose == '2':
            show_abort_operation()
            return

        self.current_order = order_number



    def add_item(self):
        os.system('cls')
        print('ADICIONANDO ITENS AO PEDIDO')
        if not self.service.check_empty_products_rep():
            show_empty_products_rep()
            return

        products_list = self.service.list_products()

        if self.current_order is None:
            order_n = ask_until_valid(ask_order_number, ValueError, show_invalid_input)
            order = self._find_order_or_show_error(order_n)
            if not order:
                return

            if order.order_status in (STATUS_COMPLETED, STATUS_CANCELED):
                show_order_error(STATUS_CANCELED)
                return
            self.current_order = order_n
        else:
            order = self.service.find_order(self.current_order)

        if order.order_status in (STATUS_COMPLETED, STATUS_CANCELED):
            show_order_error(STATUS_CANCELED)
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
            if product_choose is None:
                show_invalid_input()
                continue

            product_qtty = ask_until_valid(ask_product_qtty, ValueError, show_invalid_input)

            try:
                product = self.service.find_product(product_choose)
            except KeyError:
                show_not_found_product()
                return

            self.service.add_item(product, product_qtty, order)
            show_success_add_item(product_choose)

            while True:
                inpt_choose = ask_add_more_itens()
                if not inpt_choose:
                    show_invalid_input()
                    continue
                break

            if inpt_choose == '2':
                self.current_order = None
                show_abort_operation()
                return

    def remove_item(self):
        os.system('cls')
        print('REMOVENDO ITENS DO PEDIDO')

        order_n = ask_until_valid(ask_order_number, KeyError, show_invalid_input)
        order = self._find_order_or_show_error(order_n)
        if not order:
            return

        if order.order_status in (STATUS_COMPLETED, STATUS_CANCELED):
            show_order_error(order.order_status)
            return

        if not order.itens:
            show_empty_products_rep()
            return
        show_order_items_list(order)

        while True:
            item_name = ask_product_name()
            if not item_name:
                show_invalid_input()
                continue

            if item_name not in order.itens:
                show_invalid_input()
                continue
            break

        while True:
            confirm_del = ask_confirm_product_deletion(item_name)
            if not confirm_del:
                show_invalid_input()
                continue
            break
            
        if  confirm_del == '2':
            show_abort_operation()
            return

        self.service.remove_item(order, item_name)
        show_success_item_remove()

    def find_order(self):
        os.system('cls')
        print('BUSCANDO PEDIDO')

        order_n = ask_until_valid(ask_order_number, ValueError, show_invalid_input)
        order = self._find_order_or_show_error(order_n)
        if not order:
            return

        print()
        show_order_details(order)
        ask_press_enter_to_continue()

    def list_orders(self):
        os.system('cls')
        print('LISTANDO TODOS OS PEDIDOS NO SISTEMA')

        try:
            show_all_orders(self.service.list_all_orders())
        except FileNotFoundError:
            show_empty_orders_rep()
            return

        ask_press_enter_to_continue()

    def export_order(self):
        os.system('cls')
        print('EXPORTANDO PEDIDO')

        order_n = ask_until_valid(ask_order_number, ValueError, show_invalid_input)
        order = self._find_order_or_show_error(order_n)
        if not order:
            return

        self.service.export_order(order)
        show_success_order_export(order_n)
        return

    def complete_order(self):
        os.system('cls')
        print('FINALIZANDO PEDIDO')

        order_n = ask_until_valid(ask_order_number, ValueError, show_invalid_input)
        order = self._find_order_or_show_error(order_n)
        if not order:
            return

        if order.order_status in (STATUS_COMPLETED, STATUS_CANCELED):
            show_order_error(order.order_status)
            return

        print()
        show_order_details(order)
        print()

        pay_methods = self.service.list_all_payment_methods()
        show_all_payment_methods(pay_methods)

        while True:
            menu_n = ask_menu_choose()
            if menu_n not in pay_methods:
                show_invalid_input()
                continue
            break

        pay_choose = pay_methods[menu_n]

        try:
            order = self.service.set_payment_method(order, pay_choose)
        except ValueError:
            show_fail_payment_set()
            return

        print(f'Forma de pagamento selecionada: {pay_choose}')
        show_success_set_payment_method()
        print()
        
        while True:
            inpt_choose = ask_confirm_payment()
            if not inpt_choose:
                show_invalid_input()
                continue
            break

        if inpt_choose == '2':
            show_abort_operation()
            return

        try:
            order_complete = self.service.complete_order(order)
            if order_complete:
                show_success_complete_order()
                ask_press_enter_to_continue()
        except Exception as error:
            show_fail_to_complete_order(error)
            ask_press_enter_to_continue()
            return


    def cancel_order(self):
        os.system('cls')
        print('CANCELANDO PEDIDO')

        order_n = ask_until_valid(ask_order_number, ValueError, show_invalid_input)
        order = self._find_order_or_show_error(order_n)
        if not order:
            return

        if order.order_status in (STATUS_COMPLETED, STATUS_CANCELED):
            show_order_error(order.order_status)
            return

        self.service.cancel_order(order)
        show_success_order_cancel()