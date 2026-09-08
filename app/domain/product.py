from app.utils import check_and_convert_number_to_float

class Product:
    """
    Representa um produto disponível para venda.
    """
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def __repr__(self):
        return f'produto={self.name!r}, price={self.price!r}'

    #PROPERTIES
    @property
    def price(self):
        return self._price
    @price.setter
    def price(self, value):
        value = check_and_convert_number_to_float(value)
        if value is None:
            raise ValueError('PRODUTO: Valor inválido.')
        if value <= 0:
            raise ValueError('PRODUTO: Valor inválido.')
        self._price = value

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        if not value.strip():
            raise ValueError('PRODUTO: Nome inválido.')

        if len(value) < 3 or len(value) > 30:
            raise ValueError('PRODUTO: Nome inválido.')

        if any(
            char in ('.', ',', '/', '\\', '|', '*', '+')
            for char in value
        ):
            raise ValueError('CLIENTE: Nome inválido.')

        self._name = value.strip().lower()

    #BUSINESS METHODS
    @classmethod
    def from_dict(cls, dict_: dict) -> Product:
        name = dict_['name']
        price = dict_['price']
        return cls(name, price)

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'price': self.price
        }
