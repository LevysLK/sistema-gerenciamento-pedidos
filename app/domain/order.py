from .customer import Customer
from .orderitem import OrderItem
from .paymentmethod import PaymentMethod, PaymentNotDefined
from app.utils import get_next_order_n_act
from datetime import datetime

class Order:
    """
    Representa um pedido contendo cliente, produtos e valor total.
    """
    def __init__(self, customer: Customer):
        if not isinstance(customer, Customer):
            raise ValueError('PEDIDO: Cliente deve ser instância de Cliente.')

        self.data = None
        if self.data is None:
            self.data = f'{datetime.now():%d-%m-%Y}'
        self.customer = customer
        self._itens = {}
        self._order_status = 'aberto'
        self.payment_method = PaymentNotDefined()
        self._payment_defined = False
        self.order_n = get_next_order_n_act()

    def __repr__(self):
        return f'pedido={self.order_n}, {self.customer}, status={self.order_status}, forma_pgt={self.payment_method}, itens={self.itens}'

    def __len__(self):
        return len(self.itens)

    #PROPERTIES
    @property
    def itens(self):
        return self._itens

    @property
    def order_status(self):
        return self._order_status

    @order_status.setter
    def order_status(self, value):
        self._order_status = value

    @property
    def payment_defined(self):
        return self._payment_defined

    @payment_defined.setter
    def payment_defined(self, value):
        self._payment_defined = value

    #BUSINESS METHODS
    def add_item(self, item: OrderItem):
        if self.order_status == 'cancelado':
            raise ValueError('PEDIDOADD: Pedido cancelado.')
        if self.order_status == 'finalizado':
            raise ValueError('PEDIDOADD: Pedido já foi finalizado.')
        if not isinstance(item, OrderItem):
            raise ValueError('PEDIDOADD: Item deve ser instância de ItemPedido')

        if item.name in self._itens:
            self._itens[item.name].qtty += item.qtty
            return
        self._itens[item.name] = item

    def del_item(self, item_name: str):
        if self.order_status == 'cancelado':
            raise ValueError('PEDIDODEL: Pedido cancelado.')
        if self.order_status == 'finalizado':
            raise ValueError('PEDIDODEL: Pedido já foi finalizado.')
        if not self.itens:
            raise ValueError('PEDIDODEL: Lista de produtos vazia.')

        if not item_name.strip():
            raise KeyError('PEDIDODEL: Item inválido.')

        item_name = item_name.lower()
        if item_name not in self.itens:
            raise KeyError('PEDIDODEL: Produto não encontrado.')

        del self._itens[item_name]

    def total_calculate(self) -> float:
        if not self.itens:
            raise ValueError('PEDIDOTOTAL: Lista de produtos vazia.')

        total = 0
        for item in self.itens:
            total += self._itens[item].subtotal
        return total

    def summary(self) -> tuple:
        """
        Monta o resumo dos produtos do pedido em uma lista.
        Returns:
            tuple: contendo a lista de produtos e o total calculado do pedido.
                Formato.: (list(), float())
        """
        if not self.itens:
            raise ValueError('PEDIDORESUMO: Lista de produtos vazia.')

        rtn = []
        for x in self.itens:
            x = self.itens[x]
            rtn.append({
                'product': x.name,
                'price': x.price,
                'qtty': x.qtty,
                'subtotal': x.subtotal
                })
        return (rtn, self.total_calculate())

    def set_payment_method(self, payment_method: PaymentMethod):
        if self.order_status == 'cancelado':
            raise ValueError('PEDIDOFORMAPGTO: Pedido cancelado.')
        if self.order_status == 'finalizado':
            raise ValueError('PEDIDOFORMAPGTO: Pedido já foi finalizado.')
        if not self.itens:
            raise ValueError('PEDIDOFORMAPGTO: Lista de produtos vazia.')

        if not isinstance(payment_method, PaymentMethod):
            raise ValueError('PEDIDOFORMAPGTO: Forma de pagamento deve ser instância de PaymentMethod.')
        self.payment_method = payment_method
        self.payment_defined = True

    def complete_order(self):
        if self.order_status == 'cancelado':
            raise ValueError('PEDIDOFINALIZAR: Pedido cancelado.')
        if self.order_status == 'finalizado':
            raise ValueError('PEDIDOFINALIZAR: Pedido já está finalizado.')
        if not self.payment_defined:
            raise ValueError('PEDIDOFINALIZAR: Forma de pagamento não definida.')
        if not self.itens:
            raise ValueError('PEDIDOFINALIZAR: Lista de produtos vazia.')
        if self.total_calculate() <= 0:
            raise ValueError('PEDIDOFINALIZAR: Valor do pedido não pode ser zero ou negativo.')

        if self.payment_method.pay():
            self.order_status = 'finalizado'
            return True
        raise ValueError(f'PEDIDOFINALIZAR: Erro ao efetuar pagamento por {self.payment_method.name}.')
    
    def cancel_order(self):
        if self.order_status == 'cancelado':
            raise ValueError('PEDIDOCANCEL: Pedido já está cancelado.')
        if self.order_status == 'finalizado':
            raise ValueError('PEDIDOCANCEL: Pedido já foi finalizado.')
        self.order_status = 'cancelado'

    def to_dict(self) -> dict:
        itens_dict = {}
        for item in self.itens.values():
            itens_dict[item.name] = item.to_dict()
        return {
            'customer': self.customer.to_dict(),
            'itens': itens_dict,
            'total': self.total_calculate() if self.itens else 0,
            'data': self.data,
            'order_status': self.order_status,
            'payment_method': self.payment_method.to_dict(),
            'payment_defined': self.payment_defined,
            'order_n': self.order_n
        }

    @classmethod
    def from_dict(cls, dict_: dict) -> Order:
        order = cls(Customer.from_dict(dict_['customer']))
        order._itens = {}
        for item in dict_['itens'].values():
            order._itens[item['product']['name']] =  OrderItem.from_dict({'product': item['product'], 'qtty': item['qtty']})
        order.order_status = dict_['order_status']
        order.payment_method = PaymentMethod.from_dict(dict_['payment_method'])
        order.payment_defined = dict_['payment_defined']
        order.order_n = dict_['order_n']
        order.data = dict_['data']
        return order
