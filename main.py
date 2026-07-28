from app.repositories.orders_repository import OrderRepository
from app.repositories.products_repository import ProductsRepository
from app.services.orderservice import OrderService
from app.interface.menu import Menu

order_repositiry = OrderRepository()
products_repository = ProductsRepository()
service = OrderService(order_repositiry, products_repository)
menu = Menu(service)

menu.execute()