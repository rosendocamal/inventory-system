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

        info_del: dict[str, bool | str] = self.database.delete_from_products(code)
        result['message'] = info_del['message']

        if info_del['status'] is False:
            info_transaction: dict[str, str | int] = Transaction('REMOVE FAILED PRODUCT', code).to_dict()
            self.database.save_to_transactions(info_transaction)
            return result
        
        result['status'] = True
        info_transaction: dict[str, str | int] = Transaction('REMOVE PRODUCT', code).to_dict()
        self.database.save_to_transactions(info_transaction)

        return result

    def search_by_code(self, code: int) -> dict[str, bool | str | Product]:
        result: dict[str, bool | str | Product] = {'status': False, 'message': 'No se realizó ningún cambio.'}

        info_search: dict[str, bool | str | dict[str, str | int | float]] = self.database.search_code_in_products(code)
        result['message'] = info_search['message']

        info_transaction: dict[str, str | int] = Transaction('PRODUCT SEARCH', code).to_dict()
        self.database.save_to_transactions(info_transaction)
        
        if result['status'] is False:
            return result

        name, description, price, quantity, unity = info_search['product]']['name'], info_search['product]']['description'], info_search['product]']['price'], info_search['product]']['quantity'], info_search['product]']['unity']

        product_found = Product(code, name, description, price, quantity, unity)
        
        result['status'] = True
        result['product'] = product_found

        return result


    def search_by_name(self, name: str) -> bool | Product:
        for product in self.products.values():
            if product.name == name:
                return product
        return False
    
    def update_stock(self, code: int, quantity: int = 0) -> bool:
        if code not in self.products:
            return False
        self.products[code].update_quantity(quantity)
        self.transactions[datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')] = Transaction('UPDATE STOCK', code)
        return True

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