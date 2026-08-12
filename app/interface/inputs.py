from ..utils import check_and_convert_number_to_float

#CUSTOMERS INPUTS
def ask_customer_name() -> str | None:
     """
     Returns:
          str: nome do cliente em letras minúsculas.
          None: caso a entrada seja vazia.
     """
     name = input('Qual o nome do cliente? ').strip()

     if not name:
          return None
     return name.lower()

def ask_customer_email() -> str | None:
     """
     Returns:
          str: email válido em letras minúsculas.
          None: caso a entrada seja vazia.
     """
     email = input('Qual o email do cliente? ').strip()
     if not email:
          return None

     if email.count('.') < 1 or email.count('@') != 1 or len(email) < 8:
          return None
     return email.lower()


#ORDERS INPUTS
def ask_order_number() -> int | None:
     """
     Returns:
          int: número válido do pedido informado pelo usuário.
          None: caso a entrada seja inválida.
     """
     number = input('Qual o o número do pedido? ').strip()
     number = check_and_convert_number_to_float(number)
     if number is None:
          return None
     if number <= 0:
          return None
     if number % 1 != 0:
          return None
     return int(number)

def ask_add_more_itens() -> str | None:
     """
     Returns:
          str: número válido da opção selecionada (1=sim ou 2=não).
          None: caso a entrada seja inválida.
     """
     inpt_choose = input('Deseja adicionar mais produtos? 1=Sim, 2=Não: ').strip()
     if len(inpt_choose) != 1 or inpt_choose not in ('1', '2'):
          return None
     return inpt_choose

def ask_add_itens_or_go_menu() -> str | None:
     """
     Returns:
          str: número válido da opção selecionada (1=sim ou 2=voltar ao menu).
          None: caso a entrada seja inválida.
     """
     inpt_choose = input('Deseja adicionar itens neste pedido? 1=Sim, 2=Voltar ao menu: ').strip()
     if len(inpt_choose) != 1 or inpt_choose not in ('1', '2'):
          return None
     return inpt_choose


#PRODUCTS INPUTS
def ask_product_name() -> str | None:
     """
     Returns:
          str: nome do produto em letras minúsculas.
          None: caso a entrada seja vazia.
     """
     name = input('Qual o nome do produto? ').strip()

     if not name:
          return None
     return name.lower()

def ask_product_price() -> float | None:
     """
     Returns:
          float: preço válido informado pelo usuário.
          None: caso a entrada seja inválida.
     """
     price = input('Qual o preço do produto? ').strip()
     price = check_and_convert_number_to_float(price)
     if price is None:
          return None
     if price <= 0:
          return None
     return price

def ask_product_qtty() -> int | None:
     qtty = input('Qual a quantidade do produto? ').strip()
     qtty = check_and_convert_number_to_float(qtty)
     if qtty is None:
          return None
     if qtty <= 0:
          return None
     if qtty % 1 != 0:
          return None
     return int(qtty)

def ask_confirm_product_deletion(prod_name: str) -> str | None:
     """
     Returns:
          str: número válido da opção selecionada (1=sim ou 2=não).
          None: caso a entrada seja inválida.
     """
     inpt_choose = input(f'Confirmar exclusão do produto {prod_name.capitalize()!r}? 1=Sim, 2=Não: ').strip()
     if len(inpt_choose) != 1 or inpt_choose not in ('1', '2'):
          return None
     return inpt_choose

def ask_field_to_edit() -> tuple:
     """
     Pergunta ao usuário qual campo será editado.

     Returns:
          tuple: tupla contendo um ou mais pares (campo, função).
               Ex.: (('name', ask_product_name),)
     """
     temp_dict = {
          '1': 
          {'option': 'Editar nome', 
           'action': (
                ("name", ask_product_name),
          )},
          '2': 
          {'option': 'Editar preço', 
           'action': (
                ("price", ask_product_price),
          )},
          '3': 
          {'option': 'Editar ambos', 
           'action': (
                ("name", ask_product_name), 
                ("price", ask_product_price),
          )},
          '9': 
          {'option': 'Cancelar edição',
          'action': (
               ('action', False),
          )}
     }

     print()
     for key, item in temp_dict.items():
          print(f'{key}. {item['option']}')
     print()

     while True:
          inpt_choose = input(f'O que deseja editar? ').strip()
          if inpt_choose not in temp_dict:
               print('Entrada inválida.')
               continue

          return temp_dict[inpt_choose]['action']


#PAYMENTS INPUTS
def ask_confirm_payment() -> str | None:
     """
     Returns:
          str: número válido da opção selecionada (1=sim ou 2=não).
          None: caso a entrada seja inválida.
     """
     inpt_choose = input('Confirmar pagamento? 1=Sim, 2=Não: ').strip()
     if len(inpt_choose) != 1 or inpt_choose not in ('1', '2'):
          return None
     return inpt_choose


#GENERAL INPUTS
def ask_menu_choose() -> str:
     return str(input('Escolha uma opção: ').strip())

def ask_press_enter_to_continue():
     return input('Tecle ENTER para continuar...')


