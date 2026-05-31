from .models import Product, Transaction

class Inventory:
    def __init__(self, storage) -> None:
        self.database = storage

    def add_product(self, product: Product) -> dict[str, bool | str]:
        result: dict[str, bool | str] = {'status': False, 'message': 'No se realizó ningún cambio.'}

        info_product: dict[str, str | int | float] = product.to_dict()
        info_insert: dict[str, bool | str] = self.database.save_to_products(info_product)
        result['message'] = info_insert['message']

        if info_insert['status'] is False:
            info_transaction: dict[str, str | int] = Transaction('ADD FAILED PRODUCT', product.code).to_dict()
            self.database.save_to_transactions(info_transaction)
            return result
        
        result['status'] = True
        info_transaction: dict[str, str | int] = Transaction('ADD PRODUCT', product.code).to_dict()
        self.database.save_to_transactions(info_transaction)
        
        return result

    def del_product(self, code: int) -> dict[str, bool | str]:
        result: dict[str, bool | str] = {'status': False, 'message': 'No se realizó ningún cambio.'}
        

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