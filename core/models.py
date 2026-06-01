import datetime

class Product:
    """Clase para modelar Producto."""

    def __init__(self, code: int, name: str, description: str, price: float, quantity: int, unity: str) -> None:
        self.code = code
        self.name = name.upper()
        self.description = description.upper()
        self.price = price
        self.quantity = quantity
        self.unity = unity.upper()

    def __str__(self) -> str:
        return f'{self.code:13} | {self.name[: 36 if len(self.name) >= 36 else len(self.name) - 1]:<36} | {self.quantity:5} {self.unity:<3}'
    
    def total_value(self) -> float:
        return self.quantity * self.price

    def update_quantity(self, quantity: int = 0) -> None:
        self.quantity += quantity

    def to_dict(self) -> dict[str, str | int | float]:
        return {
            'type': 'product',
            'code': self.code,
            'name': self.name,
            'description': self.description,
            'quantity': self.quantity,
            'price': self.price,
            'unity': self.unity
            }

class Transaction:
    """Clase para modelar una Transacción."""
    def __init__(self, transaction_type: str, product_code: int) -> None:
        self.type = transaction_type
        self.product_code = product_code
        self.transaction_date = datetime.datetime.now()

    def __str__(self) -> str:
        return f'{self.type[: 13 if len(self.type) >= 13 else len(self.type) - 1]:<13} | {self.product_code:13} | {self.transaction_date.strftime('%Y/%m/%d %H:%M:%S')}'
    
    def to_dict(self) -> dict[str, str | int]:
        return {
            'type': 'transaction',
            'transaction': self.type,
            'product_code': self.product_code,
            'transaction_date': self.transaction_date.strftime('%Y/%m/%d %H:%M:%S')
        }