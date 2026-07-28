from ..domain import Product, Order, PaymentMethod

#ORDERS OUTPUTS
def show_not_find_order():
     return print('Pedido não encontrado.')

def show_success_order_cancel():
    return print(f'Pedido cancelado com sucesso!')

def show_success_order_create(order_number: str|int|float):
    return print(f'Pedido nº{order_number} criado com sucesso!')

def show_success_order_export(order_number: str|int|float):
    return print(f'Pedido nº{order_number} exportado com sucesso!')

def show_order_error(msg_to_show: str):
    """
    Exibe a mensagem 'Este pedido está/foi' seguida do texto complementar.

    Args:
        msg_to_show: texto que complementa a mensagem exibida.
    """
    return print(f'Este pedido está/foi {msg_to_show}.')

def show_success_add_item(item_name: str):
    return print(f'Produto {item_name!r} adicionado com sucesso!')

def show_success_item_remove():
    return print(f'Item removido com sucesso!')

def show_order_items_list(order: Order):
    """
    Exibe uma lista formatada dos itens contidos no pedido.

    Formato: 
        Item: 'nome', Quantidade: 'quantidade' un.
    """
    print('Itens existentes no pedido:')
    for item in order.itens.values():
        name = item.name
        qtty = item.qtty
        print(
            f'  Item: {name!r}, Quantidade: {qtty!r} un.'
        )
    print()

def show_order_details(order: Order):
    """
    Exibe um resumo completo do pedido selecionado.

    Informações exibidas: 
        - Número do pedido.
        - Data de criação.
        - Nome do cliente.
        - Lista de produtos, preços, quantidades e subtotais.
        - Status do pedido (aberto, finalizado ou cancelado).
        - Forma de pagamento.
        - Valor total do pedido.
    """
    payment_met = f'Forma de pagamento: "{order.payment_method}"'
    summary_itens, total = order.summary() if order.itens else (None, 0)
    print(f'Resumo do pedido nº{order.order_n}')
    print(
    f'Data: {order.data}',
    f'Cliente: {order.customer.name.capitalize()}, Contato: {order.customer.email!r}',
    sep='\n'
    )

    if summary_itens is not None:
        print(f'Itens no pedido:')
        for idx, item in enumerate(summary_itens, 1):
            print(
                f'    {idx}. {item["product"].capitalize()} - R${item["price"]:.2f} - Quantidade: {item['qtty']}un',
                f'    Subtotal: R${item['subtotal']:.2f}',
                sep='\n'
                )
    else:
        print(f'>>> Pedido está vazio <<<')

    print(
        f'Status do pedido: {order.order_status!r}',
        f'{payment_met if order.order_status not in ('aberto', 'cancelado') else ''}',
        f'Total do pedido: R${total:.2f}',
        sep='\n',
     )

def show_all_orders(order_list: list[Order]):
    """
    Exibe as informações dos pedidos da lista fornecida.

    Informações exibidas: 
        - Número do pedido, nome do cliente e contato.
        - Status do pedido (aberto, finalizado ou cancelado)
    """
    for order in order_list:
        print(
            f'Pedido nº{order['order_n']}, Cliente: {order['customer']['name'].capitalize()!r}, Contato: {order['customer']['email']!r}',
            f'Status: {order['order_status']!r}',
            f'',
            sep='\n'
        )

def show_success_complete_order():
    return print(f'Pedido pago e finalizado com sucesso!')


#PRODUCTS OUTPUTS
def show_not_find_product():
     return print('Produto não encontrado.')

def show_product_already_exists():
    return print('Este produto já existe.')

def show_success_product_create():
    return print(f'Produto cadastrado com sucesso!')

def show_success_product_deletion():
    return print(f'Produto deletado com sucesso!')

def show_success_product_update():
    return print(f'Produto alterado com sucesso!')

def show_empty_products_rep():
    return print(f'Não há produtos cadastrados. Faça o cadastro primeiro.')

def show_products_list(products: list[Product]):
    """
    Exibe as informações dos produtos da lista fornecida.

    Formato: 
        Produto: 'nome' - Preço: R$ 'preço'.
    """
    for product in products:
        print(
            f'  Produto: {product["name"].capitalize()} -',
            f'Preço: R${product["price"]:.2f}'
        )
    print()

def show_product_details(product: Product):
    print(
        f'  Produto: {product.name.capitalize()!r}',
        f'  Preço: R${product.price:.2f}',
        sep='\n'
    )


#PAYMENTS OUTPUTS
def show_all_payment_methods(payment_methods: dict[str, PaymentMethod]):
    """
    Exibe todas as formas de pagamento permitidas.

    Formato: 
        'opção' - Pagamento via 'forma de pagamento'.
    """
    print('Métodos de pagamento aceitos:')
    for key, value in payment_methods.items():
        value = f'Pagamento via {value.replace("Card", "Cartão").replace("Payment", "")}'
        print(f'{key} - {value}')

def show_success_set_payment_method():
    return print(f'Forma de pagamento selecionada com sucesso!')


#GENERAL OUTPUTS
def show_invalid_input():
    return print('Entrada inválida.')

def show_abort_operation():
    return print(f'Operação cancelada!')