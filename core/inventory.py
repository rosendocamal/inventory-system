from product import Product
from storage.storage_manager import StorageManager

class Inventory:
    def __init__(self, storage: StorageManager) -> None:
        self.storage_manager = storage

    def add_product(self, product: Product):
        new_product: dict[str, str | int | float] = {
            'type': 'product',
            'code': product.code,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'unity': product.unity
        }
        if not self.search_product(product.code):
            self.storage_manager.save(new_product)
        else:
            # alert: the product existed
            pass

    def del_product(self, code: int) -> None:
        if not self.search_product(code):
            # the product 
            pass
        self.storage_manager.delete(code)

    def update_stock(self, code: int, quantity: int) -> None:
        self.storage_manager.update(code, quantity)

    def search_product(self, code: int) -> None:
        self.storage_manager.view(code)

    def search_by_name(self, name: str) -> None:
        self.storage_manager.view(name)

    def total_inventory_value(self) -> None:
        self.storage_manager.view()

    def list_products(self) -> None:
        all_products: dict = self.storage_manager.view()
        

    def low_stock_products(self) -> None:
        self.storage_manager.view()