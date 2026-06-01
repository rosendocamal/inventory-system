from .models import Product, Transaction
from .database import DatabaseManager

class Inventory:
    """
    Clase principal para la gestión de las funciones del sistema de inventario.
    """
    
    def __init__(self, storage: DatabaseManager) -> None:
        self.database = storage

    def add_product(self, product: Product) -> dict[str, bool | str]:
        """
        Gestiona con los datos introducidos y la base de datos el agregado de productos al inventario.

        Parámetros:
        - product (class Product): recibe un objeto con todas los datos del producto por agregar.

        Resultado:
        - result (dict): devuelve un diccionario indicando el éxito de la operación (True o False) y
            el mensaje describiendo de manera breve el evento.
        """
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
        """
        Gestiona con el código introducido y la base de datos la eliminación del producto indicado del inventario.

        Parámetros:
        - code (int): recibe el código de producto

        Resultado:
        - result (dict): devuelve un diccionario indicando el éxito de la operación (True o False) y
            el mensaje describiendo de manera breve el evento.
        """
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

    def search_by_code(self, code: int) -> dict[str, bool | str | dict[str, str | int | float]]:
        """
        Realiza una búsqueda en la base de datos el código introducido del producto.

        Parámetros:
        - code (int): recibe el código de producto

        Resultado:
        - result (dict): devuelve un diccionario indicando el éxito de la operación (True o False) y
            el mensaje describiendo de manera breve el evento. Si la operación fue exitosa (True) se
            añade la key «product» con los datos del producto buscado, también en formato de diccionario.
        """
        result: dict[str, bool | str | dict[str, str | int | float]] = {'status': False, 'message': 'No se realizó ningún cambio.'}

        info_search: dict[str, bool | str | dict[str, str | int | float]] = self.database.search_code_in_products(code)
        result['message'] = str(info_search['message'])

        info_transaction: dict[str, str | int] = Transaction('PRODUCT CODE SEARCH', code).to_dict()
        self.database.save_to_transactions(info_transaction)
        
        if info_search['status'] is False:
            return result
        
        result['status'] = True
        result['product'] = info_search['product']

        return result

    def search_by_name(self, name: str) -> dict[str, bool | str | dict[str, str | int | float]]:
        """
        Realiza una búsqueda en la base de datos el nombre introducido del producto.

        Parámetros:
        - name (int): recibe el nombre del producto.

        Resultado:
        - result (dict): devuelve un diccionario indicando el éxito de la operación (True o False) y
            el mensaje describiendo de manera breve el evento. Si la operación fue exitosa (True) se
            añade la key «product» con los datos del producto buscado, también en formato de diccionario.
        """
        result: dict[str, bool | str | dict[str, str | int | float]] = {'status': False, 'message': 'No se realizó ningún cambio.'}

        info_search: dict[str, bool | str | dict[str, str | int | float]] = self.database.search_name_in_products(name)
        result['message'] = str(info_search['message'])

        info_transaction: dict[str, str | int] = Transaction('PRODUCT NAME SEARCH', -1).to_dict()
        self.database.save_to_transactions(info_transaction)
        
        if info_search['status'] is False:
            return result
        
        result['status'] = True
        result['product'] = info_search['product']

        return result
    
    def update_stock(self, code: int, quantity: int = 0) -> dict[str, bool | str]:
        """
        Actualiza la cantidad del inventario del producto señalado.

        Parámetros:
        - code (int): recibe el código de producto.
        - quantity (int): recibe la cantidad por actualizar, por defecto es 0

        Resultado:
        - result (dict): devuelve un diccionario indicando el éxito de la operación (True o False) y
            el mensaje describiendo de manera breve el evento.
        """
        result: dict[str, bool | str] = {'status': False, 'message': 'No se realizó ningún cambio.'}

        info_search: dict[str, bool | str] = self.database.update_data_in_products({'code': code, 'quantity': quantity})
        result['message'] = str(info_search['message'])
        
        if info_search['status'] is False:
            info_transaction: dict[str, str | int] = Transaction('FAILED PRODUCT STOCK UPDATE', code).to_dict()
            self.database.save_to_transactions(info_transaction)
            return result
        
        result['status'] = True
        info_transaction: dict[str, str | int] = Transaction('PRODUCT STOCK UPDATE', code).to_dict()
        self.database.save_to_transactions(info_transaction)
        
        return result

    def total_inventory_value(self) -> dict[str, bool | str | float]:
        """
        Realiza una consulta a la base de datos para obtener el valor total, en términos monetarios, del inventario.

        Resultado:
        - result (dict): devuelve un diccionario indicando el éxito de la operación (True o False),
            el mensaje describiendo de manera breve el evento y con el valor del stock.
        """
        info_value: dict[str, bool | str | float] = self.database.value_from_products()

        info_transaction: dict[str, str | int] = Transaction('QUERY INVENTORY VALUE', -1).to_dict()
        self.database.save_to_transactions(info_transaction)

        return info_value

    def list_products(self) -> dict[str, bool | str | list[dict[str, str | int | float]]]:
        """
        Realiza una consulta a la base de datos para obtener todos los productos en un formato de lista con
        diccionarios.

        Resultado:
        - result (dict): devuelve un diccionario indicando el éxito de la operación (True o False),
            el mensaje describiendo de manera breve el evento y con la lista de los diccionarios de
            productos (siempre y cuando la operación hay sido existosa).
        """
        info_products: dict[str, bool | str | list[dict[str, str | int | float]]] = self.database.view_all_in_products()

        info_transaction: dict[str, str | int] = Transaction('VIEW ALL PRODUCTS', -1).to_dict()
        self.database.save_to_transactions(info_transaction)

        return info_products
        
    def low_stock_products(self) -> dict[str, bool | str | list[dict[str, str | float | int]]]:
        """
        Realiza una consulta a la base de datos para obtener todos los productos en un formato de lista con
        diccionarios. Se filtra aquellos que tienen menos o igual a 15 de existencias. Se entrega los valores
        filtrados.

        Resultado:
        - result (dict): devuelve un diccionario indicando el éxito de la operación (True o False),
            el mensaje describiendo de manera breve el evento y con la lista de los diccionarios de
            productos con stock menor o igual a 15 (siempre y cuando la operación hay sido existosa).
        """
        info_low_stocks: dict[str, bool | str | list[dict[str, str | float | int]]] = self.database.view_stocks_in_products()

        info_transaction: dict[str, str | int] = Transaction('VIEW STOCK LOW', -1).to_dict()
        self.database.save_to_transactions(info_transaction)

        return info_low_stocks
    
    def list_transactions(self) -> dict[str, bool | str | list[dict[str, str | int]]]:
        """
        Realiza una consulta a la base de datos para obtener todas las transacciones en un formato de lista con
        diccionarios.

        Resultado:
        - result (dict): devuelve un diccionario indicando el éxito de la operación (True o False),
            el mensaje describiendo de manera breve el evento y con la lista de los diccionarios de
            transacciones (siempre y cuando la operación hay sido existosa).
        """
        info_transactions: dict[str, bool | str | list[dict[str, str | int]]] = self.database.view_all_in_transactions()

        info_transaction: dict[str, str | int] = Transaction('VIEW ALL TRANSACTIONS', -1).to_dict()
        self.database.save_to_transactions(info_transaction)

        return info_transactions