import datetime
from .models import Product, Transaction
# from storage.storage_manager import StorageManager

class Inventory:
    def __init__(self) -> None:
        self.products: dict[int, Product] = {
            1000000000000: Product(1000000000000, 'PRODUCT 1', 'THIS IS A PRODUCT 1', 134.00, 50, 'PZ'),
            1000000000001: Product(1000000000001, 'PRODUCT 2', 'THIS IS A PRODUCT 2', 134.00, 1, 'PZ'),
            1000000000002: Product(1000000000002, 'PRODUCT 3', 'THIS IS A PRODUCT 3', 134.00, 2, 'PZ'),
            1000000000003: Product(1000000000003, 'PRODUCT 4', 'THIS IS A PRODUCT 4', 134.00, 3, 'PZ'),
            1000000000004: Product(1000000000004, 'PRODUCT 5', 'THIS IS A PRODUCT 5', 134.00, -34, 'PZ'),
            1000000000005: Product(1000000000005, 'PRODUCT 6', 'THIS IS A PRODUCT 6', 134.00, 34, 'PZ'),
            1000000000006: Product(1000000000006, 'PRODUCT 7', 'THIS IS A PRODUCT 7', 134.00, 62, 'PZ')
            }
        self.transactions: dict[str, Transaction] = {}

    def add_product(self, product: Product) -> bool | str:
        # if not isinstance(product, Product):
        #     return f'No es clase de Producto {type(product)}\n{product.to_dict()}'
        try:
            if product.code in self.products:
                return 'El producto ya existe.'
        except AttributeError:
            return 'El producto ha sido rechazado por información incompleta.'
        self.products[product.code] = product
        self.transactions[datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')] = Transaction('ADD PRODUCT', product.code)
        return True

    def del_product(self, code: int) -> bool:
        if code not in self.products:
            return False
        if self.products[code].quantity != 0:
            return False
        self.products.pop(code)
        self.transactions[datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')] = Transaction('DELETE PRODUCT', code)
        return True

    def update_stock(self, code: int, quantity: int = 0) -> bool:
        if code not in self.products:
            return False
        self.products[code].update_quantity(quantity)
        self.transactions[datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')] = Transaction('UPDATE STOCK', code)
        return True

    def search_product(self, code: int) -> bool | Product:
        if code not in self.products:
            return False
        return self.products[code]

    def search_by_name(self, name: str) -> bool | Product:
        for product in self.products.values():
            if product.name == name:
                return product
        return False

    def total_inventory_value(self) -> float:
        total_value: float = 0

        for product in self.products.values():
            total_value += product.total_value()
        else:
            return total_value

    def list_products(self):
        return self.products.values()
        
    def low_stock_products(self) -> list[Product]:
        low_stocks: list[Product] = []
        for product in self.products.values():
            if product.quantity <= 15:
                low_stocks.append(product)
        else:
            return low_stocks