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
    @classmethod
    def list_all_pay_methods(cls) -> dict[str, str]:
        temp_list = [
            payment_class 
            for payment_class in cls.__subclasses__()
            if payment_class is not PaymentNotDefined
            ]
        return {
            str(idx): payment_class.__name__
            for idx, payment_class in enumerate(temp_list, 1)
        }

    def to_dict(self) -> str:
        return self.name

    @classmethod
    def from_dict(cls, cls_name: str) -> PaymentMethod:
        for payment_cls in cls.__subclasses__():
            if payment_cls.__name__.lower() == cls_name.lower():
                return payment_cls()
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