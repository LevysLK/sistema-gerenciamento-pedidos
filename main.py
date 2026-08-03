from app.repositories.orders_repository import OrderRepository
from app.repositories.products_repository import ProductsRepository
from app.services.orderservice import OrderService
from app.interface.menu import Menu

#GENERAL INPUTS FOR JSON USE
from app.utils.json_handler import check_temp_files
from app.interface.inputs import ask_press_enter_to_continue

order_repositiry = OrderRepository()
products_repository = ProductsRepository()
service = OrderService(order_repositiry, products_repository)
menu = Menu(service)

temp_files = check_temp_files()
if temp_files:
    print('Há arquivos temporários, não tratados, no sistema. Verifique antes de continuar!')
    for item in temp_files:
        print(item)
    print()
    ask_press_enter_to_continue()

menu.execute()