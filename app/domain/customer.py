
class Customer:
    """
    Representa um cliente cadastrado no sistema.
    """
    def __init__(self, name: str, email: str):
        name = name.strip()
        if not name:
            raise ValueError('CLIENTE: Nome inválido.')
        if len(name) < 3:
            raise ValueError('CLIENTE: Nome inválido.')
        if any(
            char in ('.', ',', '-', '/', '\\', '|', '_', '*', '+')
            or char.isdigit()
            for char in name
        ):
            raise ValueError('CLIENTE: Nome inválido.')

        email = email.strip()

        if (
            len(email) < 8
            or email.count("@") != 1
            or " " in email
        ):
            raise ValueError("CLIENTE: e-mail inválido.")

        user, domain = email.split("@")

        if (
            not user
            or "." not in domain
            or domain.startswith(".")
            or domain.endswith(".")
        ):
            raise ValueError("CLIENTE: e-mail inválido.")

        self.name = name.lower()
        self.email = email.lower()

    def __repr__(self):
        return f'cliente={self.name!r}, email={self.email!r}'

    #BUSINESS METHODS
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'email': self.email
        }

    @classmethod
    def from_dict(cls, dict_: dict) -> Customer:
        name = dict_['name']
        email = dict_['email']
        return cls(name, email)