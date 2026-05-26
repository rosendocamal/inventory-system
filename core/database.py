import sqlite3

class DatabaseManager:
    def __init__(self, path: str) -> None:
        self.path: str = path
        self.connection: sqlite3.Connection = sqlite3.connect(self.path)
        self.connection.row_factory = sqlite3.Row
        self.create_tables()
                
    def create_tables(self):
        statements: list[str] = [
            '''PRAGMA foreign_keys = ON;''',
            
            '''CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code INTEGER UNIQUE NOT NULL,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                id_unity INTEGER NOT NULL,

                FOREIGN KEY (id_unity) REFERENCES units(unity)
            );''',

            '''CREATE TABLE IF NOT EXISTS units (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                unity TEXT UNIQUE KEY NOT NULL,    
            );'''

            '''CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_type TEXT NOT NULL,
                affected_product_code INTEGER NOT NULL,
                transaction_date TEXT NOT NULL,
                
                FOREING KEY (transaction_type) REFERENCES types_transaction(id),
                FOREING KEY (affected_id_product) INTEGER products(id)
            );''',

            '''INSERT INTO units (unity) VALUES ('PZ');
            INSERT INTO units (unity) VALUES ('CJ');
            INSERT INTO units (unity) VALUES ('GR');
            INSERT INTO units (unity) VALUES ('KG');
            INSERT INTO units (unity) VALUES ('ML');
            INSERT INTO units (unity) VALUES ('LT');
            INSERT INTO units (unity) VALUES ('M');'''
        ]

        try:
            with self.connection as connection:
                cursor: sqlite3.Cursor = connection.cursor()
                for statement in statements:
                    cursor.execute(statement)
                connection.commit()

                #prox feature: add logs
                print('Las tablas han sido creadas con éxito.')
        except sqlite3.OperationalError:
            # prox feature: add logs
                print('Las tablas no han sido creadas.')
            
    def insert_data_in_products(self, data: dict) -> dict[str, bool]:
        statements: dict[str, str] = {
            'search_by_code': '''SELECT code FROM products WHERE code = ?;''',

            'search_by_id_unity': '''SELECT id FROM units WHERE unity = ?;''',

            'insert_info_product': '''INSERT INTO products (code, name, description, quantity, price, id_unity) VALUES (?, ?, ?, ?, ?, ?);'''
        }

        try:
            with self.connection as connection:
                cursor: sqlite3.Cursor = connection.cursor()

                code, name, description, quantity, price, unity = data['code'], data['name'], data['description'], data['quantity'], data['price'], data['unity']

                cursor.execute(statements['search_by_code'], code)
                id_code = cursor.fetchall()[0]

                if id_code == code:
                    return {'status': False, 'if_code_exists': True, 'if_data_complete': False}

                cursor.execute(statements['search_by_id_unity'], unity)
                id_unity = cursor.fetchall()[0]
                cursor.execute(statements['insert_info_product'], (code, name, description, quantity, price, id_unity))

                connection.commit()

                #prox feature: add logs
                print('Los datos han sido insertados correctamente a «products».')
                return {'status': True, 'if_code_exists': False, 'if_data_complete': True}
        except sqlite3.OperationalError, KeyError:
            # prox feature: add logs
                print('Los datos no han sido insertados a «products».')
                return {'status': True, 'if_code_exists': False, 'if_data_complete': False}

    def insert_data_in_transactions(self, data: dict):
        statements: dict[str, str] = {
            'search_by_id_type': '''SELECT id FROM units WHERE unity = ?;''',

            'search_by_id_code': '''SELECT id FROM products WHERE code = ?;''',

            'insert_info_transaction': '''INSERT INTO transactions (transaction_type, affected_product_code, transaction_date) VALUES (?, ?, ?);'''
        }

        try:
            with self.connection as connection:
                cursor: sqlite3.Cursor = connection.cursor()

                transaction_type, product_code, transaction_date = data['transaction_type'], product_code['product_code'], data['transaction_date']
                cursor.execute(statements['search_by_id_type'], transaction_type)
                id_transaction_type = cursor.fetchall()[0]
                cursor.execute(statements['search_by_id_code'], product_code)
                id_product_code = cursor.fetchall()[0]
                cursor.execute(statements['insert_info_transaction'], (id_transaction_type, id_product_code, transaction_date))

                connection.commit()

                #prox feature: add logs
                print('Los datos han sido insertados correctamente a «transactions».')
        except sqlite3.OperationalError, KeyError:
            # prox feature: add logs
                print('Los datos no han sido insertados a «transactions».')

def delete_data_in_products(self):
    """El futuro de la función:
    1) Buscar que el código exista y avisar si o no existe,
    2) Verificar que el producto no tenga stock, que tenga 0 y avisar si diferente a 0,
    3) Realizar las consultas para eliminar el producto
    """