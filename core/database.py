import datetime

class DatabaseManager:
    def __init__(self) -> None:
        self.products: dict[int, dict[str, str | int | float]] = {
            1000000000000: {
                'type': 'product',
                'code': 1000000000000,
                'name': 'PRODUCT NAME 0',
                'description': 'THIS IS A PRODUCT',
                'quantity': 10000,
                'price': 250.75,
                'unity': 'PZ'
            },
            1000000000001: {
                'type': 'product',
                'code': 1000000000001,
                'name': 'PRODUCT NAME 1',
                'description': 'THIS IS A PRODUCT',
                'quantity': 40000,
                'price': 250.75,
                'unity': 'PZ'
            },
            1000000000002: {
                'type': 'product',
                'code': 1000000000002,
                'name': 'PRODUCT NAME 3',
                'description': 'THIS IS A PRODUCT',
                'quantity': 40000,
                'price': 250.25,
                'unity': 'PZ'
            },
            1000000000003: {
                'type': 'product',
                'code': 1000000000003,
                'name': 'PRODUCT NAME 3',
                'description': 'THIS IS A PRODUCT',
                'quantity': 30000,
                'price': 205.75,
                'unity': 'KG'
            }
        }
        self.transactions: dict[str, dict[str, str | int]] = {}
    
    def save_to_transactions(self, data: dict[str, str | int]) -> None:
        """
        Guarda las transacciones solicitadas para su incorporación al historial.

        Parámetro:
        - data (dict): recibe un diccionario con la información y estructura adecuada
            transacción (ver clase Transaction).
        """
        self.transactions[datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')] = data
        
    def save_to_products(self, data: dict) -> dict[str, bool | str]:
        """
        Guarda los nuevos productos del inventario.

        Parámetro:
        - data (dict): recibe un diccionario con la información y estructura de un producto
            (ver clase Product)

        Resultado:
        - result (dict[str, bool | str]): retorna un diccionario sobre el estado (bool) y el mensaje
            de resultado o error (str)
        """
        result: dict[str, bool | str] = {'status': False, 'message': 'No se realizó ningún cambio.'}

        try:
            if data['code'] in self.products:
                result['message'] = 'Producto rechazado: El código de producto está registrado.'
                return result
        except KeyError:
            result['message'] = 'Producto rechazado: Información del producto incompleta.'
            return result
        
        self.products[data['code']] = data
        result['status'] = True
        result['message'] = 'Producto agregado con éxito.'
        return result
    
    def delete_from_products(self, data: int) -> dict[str, bool | str]:
        """
        Elimina el producto del inventario indicado mediante el código de producto.
        
        Parámetro:
        - data (int): El código de producto a eliminar.

        Resultado:
        - result (dict[str, bool | str]): retorna un diccionario sobre el estado ('status': bool) y el mensaje
            de resultado o error ('message': str). El estado es True si la operación fue exitosa y False si fue
            lo contrario, mientras que el mensaje o error es un texto personalizado del estado para el usuario.
        """
        result: dict[str, bool | str] = {'status': False, 'message': 'No se realizó ningún cambio.'}
        if data not in self.products:
                result['message'] = 'Producto no eliminado: El código de producto no está registrado.'
                return result
        product_quantity = int(self.products[data]['quantity'])
        if product_quantity != 0:
            result['message'] = 'Producto no eliminado: '
            result['message'] += 'Posee inventario negativo.' if product_quantity < 0 else 'Posee inventario positivo.'
            return result
        
        self.products.pop(data)
        result['status'] = True
        result['message'] = 'Producto eliminado con éxito.'
        return result
        
    def update_data_in_products(self):
        pass
    def query_data_in_products(self):
        pass