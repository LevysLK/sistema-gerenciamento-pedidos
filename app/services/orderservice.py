from ..domain import (Customer, Order, OrderItem, Product, PaymentMethod)
from app.repositories.orders_repository import OrderRepository
from app.repositories.products_repository import ProductsRepository

class OrderService:
    """
    Coordena as operações relacionadas aos pedidos entre menus, domínios e repositórios.
    """
    def __init__(self, order_rep: OrderRepository, prod_rep: ProductsRepository):
        self._order_rep = order_rep
        self._prod_rep = prod_rep

    def __repr__(self):
        return f'Classe gerenciadora com métodos de construção de pedidos, clientes, produtos, etc.'


    #PRODUCTS ACTIONS
    def create_product(self, product: dict):
        """
        Args:
            product: dicionário contendo os dados do produto
            formato: {'name': name, 'price': price}
        """
        product = Product(**product)

        self._prod_rep.save_product(product)
        return True

    def find_product(self, product_name: str) -> Product:
        return self._prod_rep.find_product(product_name)

    def list_products(self) -> list[dict]:
        return self._prod_rep.list_products()
    
    def delete_product(self, product: Product):
        self._prod_rep.delete_product(product.name)

    def edit_product(self, product_on_system: Product, changes: dict):
        """
        Edita o campo selecionado do produto em questão.
        Args:
            changes: 
                dict contendo as chaves 'name', 'price' ou ('name', 'price').
            product_on_system: 
                Produto (objeto) encontrado no sistema.
        Returns:
            False: caso os valores de alteração forem iguais aos que já estão no sistema.
        """
        new_product = Product(product_on_system.name, product_on_system.price)
        for key, value in changes.items():
            setattr(new_product, key, value)

        if (
            'name' in changes and new_product.name == product_on_system.name
        ) or (
            'price' in changes and new_product.price == product_on_system.price
        ):
            return False

        self._prod_rep.replace_product(product_on_system, new_product)


    #ORDERS ACTIONS
    def create_order(self, customer: dict) -> int:
        """
        Args:
            customer: dicionário contendo os dados do cliente.
            formato: {'name': name, 'email': email} 
        Returns:
            int: order number
        """
        customer = Customer(**customer)
        order = Order(customer)

        self._order_rep.save_order(order)
        order_number = order.order_n
        return order_number

    def find_order(self, order_n: int) -> Order:
        return self._order_rep.find_order(order_n)

    def add_item(self, product: Product, qtty: int, order: Order):
        item = OrderItem(product, qtty)
        order.add_item(item)
        self._order_rep.replace_order(order)

    def remove_item(self, order: Order, item_name: str):
        if not order.itens:
            return
        order.del_item(item_name)
        self._order_rep.replace_order(order)

    def list_all_orders(self) -> list[dict]:
        orders_list = self._order_rep.list_orders()
        return orders_list

    def export_order(self, order: Order):
        self._order_rep.export_order(order)

    def cancel_order(self, order: Order):
        order.cancel_order()
        self._order_rep.replace_order(order)

    def complete_order(self, order: Order) -> bool:
        if order.complete_order() is True:
            self._order_rep.replace_order(order)
            return True
        return False


    #PAYMENT ACTIONS
    def list_all_payment_methods(self) -> dict[str, str]:
        return PaymentMethod.list_all_pay_methods()

    def set_payment_method(self, order: Order, payment_method: str) -> Order: 
        payment_set = PaymentMethod.from_dict(payment_method)
        order.set_payment_method(payment_set)
        return order