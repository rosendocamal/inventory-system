import sqlite3

class DatabaseManager:

    def __init__(self, db_name: str = 'test_db.db') -> None:
        self.db_name: str = db_name
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_name)
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS units (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    unity TEXT UNIQUE NOT NULL   
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT UNIQUE NOT NULL
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code INTEGER UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL,
                    id_unity INTEGER NOT NULL,
                    FOREIGN KEY (id_unity) REFERENCES units(id)
                );
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category INTEGER NOT NULL,
                    affected_product_code INTEGER NOT NULL,
                    transaction_date TEXT DEFAULT (datetime('now', 'localtime')),
                    FOREIGN KEY (affected_product_code) REFERENCES products(id) ON DELETE CASCADE,
                    FOREIGN KEY (category) REFERENCES categories(id)
                );
            """)
            conn.commit()

    def _get_or_create_unit(self, cursor: sqlite3.Cursor, unity_name: str) -> int:
        cursor.execute("INSERT OR IGNORE INTO units (unity) VALUES (?);", (unity_name,))
        if cursor.lastrowid:
            return cursor.lastrowid
        cursor.execute("SELECT id FROM units WHERE unity = ?;", (unity_name,))
        return int(cursor.fetchone()["id"])

    def _get_or_create_category(self, cursor: sqlite3.Cursor, category_name: str) -> int:
        cursor.execute("INSERT OR IGNORE INTO categories (category) VALUES (?);", (category_name,))
        if cursor.lastrowid:
            return cursor.lastrowid
        cursor.execute("SELECT id FROM categories WHERE category = ?;", (category_name,))
        return int(cursor.fetchone()["id"])

    def save_to_transactions(self, data: dict) -> None:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            category_id = self._get_or_create_category(cursor, data["category"])
            
            cursor.execute("SELECT id FROM products WHERE code = ?;", (data["affected_product_code"],))
            product_row = cursor.fetchone()
            if not product_row:
                return
            product_id = product_row["id"]
            
            transaction_date = data.get("transaction_date")
            if transaction_date:
                cursor.execute("""
                    INSERT INTO transactions (category, affected_product_code, transaction_date) 
                    VALUES (?, ?, ?);
                """, (category_id, product_id, transaction_date))
            else:
                cursor.execute("""
                    INSERT INTO transactions (category, affected_product_code) 
                    VALUES (?, ?);
                """, (category_id, product_id))
            conn.commit()

    def save_to_products(self, data: dict) -> dict[str, bool | str]:
        result: dict[str, bool | str] = {'status': False, 'message': 'No se realizó ningún cambio.'}
        required_keys = ['code', 'name', 'description', 'quantity', 'price', 'unity']
        
        if not all(k in data for k in required_keys):
            result['message'] = 'Producto rechazado: Información del producto incompleta.'
            return result

        with self._get_connection() as conn:
            cursor = conn.cursor()
            unit_id = self._get_or_create_unit(cursor, data['unity'])
            try:
                cursor.execute("""
                    INSERT INTO products (code, name, description, quantity, price, id_unity) 
                    VALUES (?, ?, ?, ?, ?, ?);
                """, (data['code'], data['name'], data['description'], data['quantity'], data['price'], unit_id))
                conn.commit()
            except sqlite3.IntegrityError:
                result['message'] = 'Producto rechazado: El código de producto está registrado.'
                return result
                
        result.update({'status': True, 'message': 'Producto agregado con éxito.'})
        return result

    def delete_from_products(self, data: int) -> dict[str, bool | str]:
        result: dict[str, bool | str] = {'status': False, 'message': 'No se realizó ningún cambio.'}
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT quantity FROM products WHERE code = ?;", (data,))
            row = cursor.fetchone()
            
            if not row:
                result['message'] = 'Producto no eliminado: El código de producto no está registrado.'
                return result
                
            product_quantity = int(row["quantity"])
            if product_quantity != 0:
                result['message'] = 'Producto no eliminado: '
                result['message'] += 'Posee inventario negativo.' if product_quantity < 0 else 'Posee inventario positivo.'
                return result
            
            cursor.execute("DELETE FROM products WHERE code = ?;", (data,))
            conn.commit()
            
        result.update({'status': True, 'message': 'Producto eliminado con éxito.'})
        return result

    def _map_product_rows(self, rows: list[sqlite3.Row]) -> list[dict]:
        return [
            {
                'code': row['code'],
                'name': row['name'],
                'description': row['description'],
                'quantity': row['quantity'],
                'price': row['price'],
                'unity': row['unity']
            } for row in rows
        ]

    def search_code_in_products(self, data: int) -> dict[str, bool | str | dict]:
        result: dict[str, bool | str | dict] = {'status': False, 'message': 'No se realizó ningún cambio.'}
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT code, name, description, quantity, price, units.unity
                FROM products
                INNER JOIN units ON units.id = products.id_unity
                WHERE code = ?;
            """, (data,))
            row = cursor.fetchone()
            
            if not row:
                result['message'] = 'Producto no encontrado: El código de producto no está registrado.'
                return result
                
            result['product'] = self._map_product_rows([row])[0]
            result.update({'status': True, 'message': 'El producto ha sido encontrado con éxito.'})
            return result

    def search_name_in_products(self, data: str) -> dict[str, bool | str | dict]:
        result: dict[str, bool | str | dict] = {'status': False, 'message': 'No se realizó ningún cambio.'}
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT code, name, description, quantity, price, units.unity
                FROM products
                INNER JOIN units ON units.id = products.id_unity
                WHERE name = ?;
            """, (data,))
            row = cursor.fetchone()
            
            if not row:
                result['message'] = 'Producto no encontrado: El nombre del producto no está registrado.'
                return result
                
            result['product'] = self._map_product_rows([row])[0]
            result.update({'status': True, 'message': 'El producto ha sido encontrado con éxito.'})
            return result

    def update_data_in_products(self, data: dict[str, int]) -> dict[str, bool | str]:
        result: dict[str, bool | str] = {'status': False, 'message': 'No se realizó ningún cambio.'}
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE products
                SET quantity = quantity + ?
                WHERE code = ?;
            """, (data['quantity'], data['code']))
            conn.commit()
            
            if cursor.rowcount == 0:
                result['message'] = 'Existencias sin actualizar: El código de producto no está registrado.'
                return result
                
        result.update({'status': True, 'message': 'Actualización del stock exitosa.'})
        return result

    def value_from_products(self) -> dict[str, bool | str | float]:
        result: dict[str, bool | str | float] = {'status': False, 'message': 'Sin datos para visualizar.', 'stock': 0.00}
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(quantity * price) AS total_value FROM products;")
            row = cursor.fetchone()
            
            if row and row["total_value"] is not None:
                result.update({
                    'status': True,
                    'message': 'Se ha contabilizado el valor monetario del inventario con éxito.',
                    'stock': float(row["total_value"])
                })
        return result

    def view_all_in_products(self) -> dict[str, bool | str | list[dict]]:
        result: dict[str, bool | str | list[dict]] = {'status': False, 'message': 'Sin datos para visualizar.'}
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT code, name, description, quantity, price, units.unity
                FROM products
                INNER JOIN units ON units.id = products.id_unity;
            """)
            rows = cursor.fetchall()
            
            if not rows:
                return result
                
            result.update({
                'status': True,
                'message': 'Datos de productos extraídos.',
                'products': self._map_product_rows(rows)
            })
            return result

    def view_stocks_in_products(self) -> dict[str, bool | str | list[dict]]:
        result: dict[str, bool | str | list[dict]] = {'status': False, 'message': 'Sin datos para visualizar.'}
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT code, name, description, quantity, price, units.unity
                FROM products
                INNER JOIN units ON units.id = products.id_unity
                WHERE quantity <= 15;
            """)
            rows = cursor.fetchall()
            
            if not rows:
                return result
                
            result.update({
                'status': True,
                'message': 'Datos de productos con stock bajo extraídos.',
                'products': self._map_product_rows(rows)
            })
            return result

    def view_all_in_transactions(self) -> dict[str, bool | str | list[dict]]:
        result: dict[str, bool | str | list[dict]] = {'status': False, 'message': 'Sin datos para visualizar.'}
        
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT t.id, c.category, p.code AS product_code, t.transaction_date 
                FROM transactions t
                INNER JOIN categories c ON c.id = t.category
                INNER JOIN products p ON p.id = t.affected_product_code;
            """)
            rows = cursor.fetchall()
            
            if not rows:
                return result
                
            result.update({
                'status': True,
                'message': 'Datos de transacciones extraídos.',
                'transactions': [
                    {
                        'id': row['id'],
                        'category': row['category'],
                        'affected_product_code': row['product_code'],
                        'transaction_date': row['transaction_date']
                    } for row in rows
                ]
            })
            return result