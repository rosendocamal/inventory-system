from .product import Product
# from storage.storage_manager import StorageManager

class Inventory:
    def __init__(self) -> None:
        self.products: dict[int, Product] = {}

    def add_product(self, product: Product) -> bool:
        if not isinstance(product, Product):
            return False
        
        try:
            if product.code in self.products:
                return False
            """
            info_product: dict[str, str | int | float] = {
                'type': 'product',
                'code': product.code,
                'name': product.name,
                'description': product.description,
                'quantity': product.quantity,
                'price': product.price,
                'unity': product.unity
            }
            """
        except AttributeError as e:
            return False
        
        self.products[product.code] = product
        return True

    def del_product(self, code: int) -> bool:
        if code not in self.products:
            return False
        
        if self.products[code].quantity != 0:
            return False
        
        self.products.pop(code)
        return True

    def update_stock(self, code: int, quantity: int) -> bool:
        if code not in self.products:
            return False
        
        self.products[code].update_quantity(quantity)
        return True

    def search_product(self, code: int) -> bool:
        if code not in self.products:
            return False
        
        print(self.products[code])
        return True

    def search_by_name(self, name: str) -> bool:
        for product in self.products.values():
            if product.name == name:
                print(product)
                return True

        return False

    def total_inventory_value(self) -> None:
        total_value: float = 0

        for product in self.products.values():
            total_value += product.total_value()
        
        print(total_value)

    def list_products(self) -> None:
        print(self.products.values())
        
    def low_stock_products(self) -> None:
        for product in self.products.values():
            if 0 <= product.quantity <= 15:
                print(product)