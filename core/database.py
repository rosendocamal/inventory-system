import datetime

class DatabaseManager:
    """
    Clase principal para la gestión de la base de datos.
    """
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
        
    def search_code_in_products(self, data: int) -> dict[str, bool | str | dict[str, str | int | float]]:
        """
        Busca el producto indicado mediante el código de producto dado.

        Parámetro:
        - data (int): El código de producto a buscar.

        Resultado:
        - result (dict[str, bool | str | dict]): retorna un diccionario sobre el estado ('status': bool) y el mensaje
            de resultado o error ('message': str). El estado es True si la operación fue exitosa y False si fue lo
            contrario, mientras que el mensaje o error es un texto personalizado del estado para el usuario. Si la
            operación es exitosa, se añade la clave «product» (dict) con la información y estructura de un producto que
            corresponde con el parámetro indicado.
        """
        result: dict[str, bool | str | dict[str, str | int | float]] = {'status': False, 'message': 'No se realizó ningún cambio.'}
        if data not in self.products:
            result['message'] = 'Producto no encontrado: El código de producto no está registrado.'
            return result

        result['status'] = True
        result['message'] = 'El producto ha sido encontrado con éxito.'
        result['product'] = self.products[data]
        return result
    
    def search_name_in_products(self, data: str) -> dict[str, bool | str | dict[str, str | int | float]]:
        """
        Busca el producto indicado mediante el nombre del producto dado.

        Parámetro:
        - data (str): El nombre del producto a buscar.

        Resultado:
        - result (dict[str, bool | str | dict]): retorna un diccionario sobre el estado ('status': bool) y el mensaje
            de resultado o error ('message': str). El estado es True si la operación de búsqueda fue exitosa y False si 
            fue lo contrario, mientras que el mensaje o error es un texto personalizado del estado para el usuario. Si la
            operación es exitosa, se añade la clave «product» (dict) con la información y estructura de un producto que
            corresponde con el parámetro indicado.
        """
        result: dict[str, bool | str | dict[str, str | int | float]] = {'status': False, 'message': 'No se realizó ningún cambio.'}
        for product in self.products.values():
            if product['name'] == data:
                result['status'] = True
                result['message'] = 'El producto ha sido encontrado con éxito.'
                result['product'] = product
                return result

        result['message'] = 'Producto no encontrado: El nombre del producto no está registrado.'
        return result

    def update_data_in_products(self, data: dict[str, int]) -> dict[str, bool | str]:
        """
        Actualiza las existencias del producto indicado.

        Parámetro:
        - data (dict[str, int]): Ingresa un diccionario con las llaves de «code» y «quantity» correspondientes al código de
            producto y la cantidad del stock a actualizar, respectivamente.

        Resultado:
        - result (dict[str, bool | str | dict]): retorna un diccionario sobre el estado ('status': bool) y el mensaje
            de resultado o error ('message': str). El estado es True si la operación de búsqueda fue exitosa y False si 
            fue lo contrario, mientras que el mensaje o error es un texto personalizado del estado para el usuario. Si la
            operación es exitosa, se añade la clave «product» (dict) con la información y estructura de un producto que
            corresponde con el parámetro indicado.
        """
        result: dict[str, bool | str] = {'status': False, 'message': 'No se realizó ningún cambio.'}
        data_code: int = data['code']
        data_quantity: int = data['quantity']

        if data_code not in self.products:
            result['message'] = 'Existencias sin actualizar: El código de producto no está registrado.'
            return result

        self.products[data_code]['quantity'] = data_quantity + int(self.products[data_code]['quantity'])
        result['status'] = True
        result['message'] = 'Actualización del stock exitosa.'
        return result
    
    def value_from_products(self) -> dict[str, bool | str | float]:
        """
        Realiza la consulta y el cálculo del valor monetario de las
        existencias del inventario.

        Resultado:
        - result (dict[str, bool | str | float]): retorna un diccionario sobre el estado ('status': bool) y el mensaje
            de resultado o error ('message': str). El estado es True si el cálculo fue exitosa y False si 
            fue lo contrario, mientras que el mensaje o error es un texto personalizado del estado para el usuario. Se añade la
            key «stock» para el valor del inventario en formato float.
        """
        result: dict[str, bool | str | float] = {'status': False, 'message': 'Sin datos para visualizar.', 'stock': 0.00}

        stock: float = 0
        for product in self.products.values():
            stock += int(product['quantity']) * float(product['price'])
        else:
            result['status'] = True
            result['message'] = 'Se ha contabilizado el valor monetario del inventario con éxito.'
            result['stock'] = stock
            return result
        
    def view_all_in_products(self) -> dict[str, bool | str | list[dict[str, str | float | int]]]:
        """
        Realiza la consulta y extrae los datos de cada uno de los
        productos y lo entrega empaquetado con formato de diccionarios.

        Resultado:
        - result (dict[str, bool | str | float]): retorna un diccionario sobre el estado ('status': bool) y el mensaje
            de resultado o error ('message': str). El estado es True si la extracción fue exitosa y False si 
            fue lo contrario, mientras que el mensaje o error es un texto personalizado del estado para el usuario. Se añade la
            key «products» para la lista de diccionarios de los productos.
        """
        result: dict[str, bool | str | list[dict[str, str | float | int]]] = {'status': False, 'message': 'Sin datos para visualizar.'}

        data_list: list[dict[str, str | float | int]] = []
        for product in self.products.values():
            data_list.append(product)
        else:
            if data_list:
                result['status'] = True
                result['message'] = 'Datos de productos extraídos.'
                result['products'] = data_list
            return result
        
    def view_stocks_in_products(self) -> dict[str, bool | str | list[dict[str, str | float | int]]]:
        """
        Realiza la consulta y extrae los datos de cada uno de los
        productos y lo entrega empaquetado con formato de diccionarios.

        Resultado:
        - result (dict[str, bool | str | float]): retorna un diccionario sobre el estado ('status': bool) y el mensaje
            de resultado o error ('message': str). El estado es True si la extracción fue exitosa y False si 
            fue lo contrario, mientras que el mensaje o error es un texto personalizado del estado para el usuario. Se añade la
            key «products» para la lista de diccionarios de los productos.
        """
        result: dict[str, bool | str | list[dict[str, str | float | int]]] = {'status': False, 'message': 'Sin datos para visualizar.'}

        data_list: list[dict[str, str | float | int]] = []
        for product in self.products.values():
            if int(product['quantity']) <= 15:
                data_list.append(product)
        else:
            if data_list:
                result['status'] = True
                result['message'] = 'Datos de productos con stock bajo extraídos.'
                result['products'] = data_list
            return result
        
    def view_all_in_transactions(self) -> dict[str, bool | str | list[dict[str, str | int]]]:
        """
        Realiza la consulta y extrae los datos de cada uno de los
        productos y lo entrega empaquetado con formato de diccionarios.

        Resultado:
        - result (dict[str, bool | str | float]): retorna un diccionario sobre el estado ('status': bool) y el mensaje
            de resultado o error ('message': str). El estado es True si la extracción fue exitosa y False si 
            fue lo contrario, mientras que el mensaje o error es un texto personalizado del estado para el usuario. Se añade la
            key «products» para la lista de diccionarios de los productos.
        """
        result: dict[str, bool | str | list[dict[str, str | int]]] = {'status': False, 'message': 'Sin datos para visualizar.'}

        data_list: list[dict[str, str | int]] = []
        for transactions in self.transactions.values():
            data_list.append(transactions)
        else:
            if data_list:
                result['status'] = True
                result['message'] = 'Datos de transacciones extraídos.'
                result['transactions'] = data_list
            return result