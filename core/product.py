class Product:
    def __init__(self, code: int, name: str, description: str, price: float, quantity: int, unity: str) -> None:
        self.code = code
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.unity = unity

    def __str__(self) -> str:
        return f'{self.code:13} | {self.name[: 36 if len(self.name) >= 36 else len(self.name) - 1]:<36} | {self.quantity:5} {self.unity:<3}'
    
    def total_value(self) -> float:
        return self.quantity * self.price

    def update_quantity(self, quantity: int) -> None:
        self.quantity += quantity