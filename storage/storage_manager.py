import sqlite3

class DatabaseManager:
    def __init__(self, path) -> None:
        self.path: str = path
        self.initialize_database()

    def get_connection(self) -> sqlite3.Connection:
        connection: sqlite3.Connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def keep_connection(self, sql_statement: str, **kwargs):
        try:
            with self.get_connection() as connection:
                connection.execute(sql_statement, **kwargs)
        except sqlite3.OperationalError as error:
            pass
        else:
            pass
        finally:
            # I'd add logs here
            pass 
                
    def initialize_database(self):
        create_tables: str ='''
            CREATE TABLE IF NOT EXISTS products (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                code_product    INTEGER UNIQUE NOT NULL,
                type            TEXT NOT NULL,
                quantity        INTEGER NOT NULL,
                date            TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS transactions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                code        INTEGER UNIQUE NOT NULL,
                name        TEXT NOT NULL,
                description TEXT NOT NULL,
                price       REAL NOT NULL,
                quantity    INTEGER NOT NULL,
                unity        TEXT NOT NULL
            );
        '''

    def insert_data(self, data: dict):
        '''
        esto debe recibir un diccionario de la siguiente forma (ejemplo):
        {
            "type": "product",
            "code": 12341241234,
            "name": "REFRESCO COLA",
            "description": esto es una bebida refrescante,
            "price": 1341234
            "unit": "PZ"
        }
        '''

        statements = {
            'products': '''INSERT INTO products (code, name, description, price, quantity, unity) (?, ?, ?, ?, ?, ?);''',
            'transactions': '''INSERT INTO transactions (code_product, type, quantity, date) (?, ?, ?, ?);'''
        }
        insert_statement: str = statements[data['type']]
        self.keep_connection(insert_statement, params=())

    def read_data(self):
        pass

    def update_data(self):
        pass

    def delete_data(self):
        pass

class StorageManager:
    def __init__(self, database: DatabaseManager) -> None:
        self.database = database

    def save(self, data) -> None:
        self.database.insert_data(data)

    def delete(self) -> None:
        pass

    def update(self) -> None:
        pass

    def view(self):
        pass


# quizás use math case con diccionarios (con tipos type()) para analizar
