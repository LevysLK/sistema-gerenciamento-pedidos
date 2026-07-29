from ..config import paths
from ..domain import Product
from ..utils import json_handler
import json

class ProductsRepository:
    """
    Responsável pela persistência dos produtos no sistema.
    """
    def __repr__(self):
        return 'Classe contendo dicionário com todos os objetos Produto, e métodos para add, del, buscar, listar.'

    #BUSINESS METHODS
    @staticmethod
    def _push_products_list(prod_list: list[dict]):
        json_handler.save_to(paths.REPOSITORY_PRODUCTS_JSON, prod_list)

    @staticmethod
    def _get_products_list(empty_ignore=False) -> list[dict]:
        try:
            temp_list = json_handler.read_from(paths.REPOSITORY_PRODUCTS_JSON)
        except (FileNotFoundError, json.JSONDecodeError):
            if empty_ignore:
                temp_list = []
            else:
                raise FileNotFoundError('Não há produtos salvos.')
        return temp_list

    def save_product(self, product: Product):
        if not isinstance(product, Product):
            raise ValueError('PRODUTOREPOSITORY_SALVAR: Produto deve ser instância de Produto')

        temp_list = self._get_products_list(empty_ignore=True)
        for item in temp_list:
            if item['name'] == product.name:
                raise KeyError('PRODUTOREPOSITORY_SALVAR: Produto já cadastrado.')

        temp_list.append(product.to_dict())
        self._push_products_list(temp_list)
        return True

    def replace_product(self, old_product: Product, new_product: Product | None=None):
        if new_product is None:
            new_product = old_product

        temp_list = self._get_products_list()

        for idx, product in enumerate(temp_list):
            if product['name'] == old_product.name:
                temp_list[idx] = new_product.to_dict()
                self._push_products_list(temp_list)
        return True

    def delete_product(self, product_name: str):
        temp_list = self._get_products_list()
        for idx, product in enumerate(temp_list):
            if product_name.lower() == product['name']:
                del temp_list[idx]
                self._push_products_list(temp_list)
                return True
        raise KeyError('PRODUTOREPOSITORY_DELETAR: Produto não encontrado.')

    def list_products(self) -> list[dict]:
        return self._get_products_list()

    def find_product(self, product_name: str) -> Product | bool:
        """
        Returns:
            Product: objeto Product encontrado no sistema.
            False: caso não encontre o produto pedido.
        """
        if not product_name:
            return False
        temp_list = self._get_products_list()
        for product in temp_list:
            if product_name.lower() == product['name']:
                return Product.from_dict(product)
        return False