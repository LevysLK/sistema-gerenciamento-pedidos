from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    """
    Representa as formas de pagamento disponíveis.
    """
    def __repr__(self):
        return self.name

    @property
    def name(self):
        return self.__class__.__name__

    #BUSINESS METHODS
    @staticmethod
    def list_all_pay_methods() -> dict[str, str]:
        temp_dict = {}
        for idx, cls in enumerate(PaymentMethod.__subclasses__()):
            if cls.__name__ == 'PaymentNotDefined': #Pula a exibição de pagamento não definido
                continue
            temp_dict[str(idx + 1)] = cls.__name__
        return temp_dict

    def to_dict(self) -> str:
        return self.name

    def from_dict(cls_name: str) -> PaymentMethod:
        for cls in PaymentMethod.__subclasses__():
            if cls.__name__.lower() == cls_name.lower():
                return cls()
        raise ValueError("FORMAPGTO_FROMDICT: Forma de pagamento inválida.")

    @abstractmethod
    def pay(self):
        pass

class PixPayment(PaymentMethod):
    def pay(self):
        return True

class CardPayment(PaymentMethod):
    def pay(self):
        return True

class PaymentNotDefined(PaymentMethod):
    def pay(self):
        raise RuntimeError("FORMAPGTO: Forma de pagamento não definida.")