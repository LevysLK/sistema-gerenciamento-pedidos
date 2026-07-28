from .product import Product
from app.utils import check_and_convert_number_to_float

class OrderItem:
    """
    Representa um item incluso no pedido, contendo o produto e sua quantidade.
    """
    def __init__(self, product: Product, qtty: int):
        if not isinstance(product, Product):
            raise ValueError('ITEMPEDIDO: Produto deve ser instância de Produto.')
        self.name = product.name
        self.price = product.price

        qtty = check_and_convert_number_to_float(qtty)
        if qtty % 1 != 0 or qtty <= 0:
            raise ValueError('ITEMPEDIDO: Quantidade inválida.')

        self.product = product
        self.qtty = int(qtty)

    def __repr__(self):
        return f'product={self.name}, qtty={self.qtty}'

    @property
    def subtotal(self):
        return self.price * self.qtty

    #BUSINESS METHODS
    def to_dict(self) -> dict:
        return {
            'product': self.product.to_dict(),
            'qtty': self.qtty
        }

    @classmethod
    def from_dict(cls, dict_: dict) -> OrderItem:
        qtty = dict_['qtty']
        product = Product.from_dict(dict_['product'])
        return cls(product, qtty)