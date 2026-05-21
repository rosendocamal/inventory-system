from core.product import Product
from core.inventory import Inventory

test_inventory = Inventory()

def test_add_product():
    test_product_1: Product = Product(123123123, 'NAME PRODUCT', 'THIS IS A PRODUCT', 12.32, 50, 'PZ')
    test_product_2: Product = Product(123123123, 'SECOND PRODUCT', 'THIS IS A PRODUCT', 12.23, 50, 'GR')
    test_product_3: Product = Product(123123124, 'NAME', 'THIS', 12, 12, 'CJ')
    result_1 = test_inventory.add_product(test_product_1)
    result_2 = test_inventory.add_product(123243)
    result_3 = test_inventory.add_product(test_product_2)
    result_4 = test_inventory.add_product(test_product_3)

    assert result_1 is True
    assert result_2 is False
    assert result_3 is False
    assert result_4 is True


def test_del_product():
    result_1 = test_inventory.del_product(code=int())
    result_2 = test_inventory.del_product(123123123)

    assert result_1 is False
    assert result_2 is False

def test_update_stock():
    result_1 = test_inventory.update_stock(123123123, -134124124132413241234)
    result_2 = test_inventory.update_stock(0, 123)
    result_3 = test_inventory.update_stock(123123124, 1234)
    result_4 = test_inventory.update_stock(int(), int())

    assert result_1 is True
    assert result_2 is False
    assert result_3 is True
    assert result_4 is False

def test_search_product():
    result_1 = test_inventory.search_product(123123123)
    result_2 = test_inventory.search_product(int())

    assert result_1 is True
    assert result_2 is False

def test_search_by_name():
    result_1 = test_inventory.search_by_name('NAME PRODUCT')
    result_2 = test_inventory.search_by_name('NONE')

    assert result_1 is True
    assert result_2 is False

def test_total_inventory_value():
    result_1 = test_inventory.total_inventory_value()

    assert result_1 is not False

def test_list_products():
    pass

def test_low_stocks_products():
    pass