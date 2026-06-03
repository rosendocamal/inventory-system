import sqlite3
from pathlib import Path

file_db = Path('.', 'managerDB.py')

with sqlite3.connect(file_db) as con:
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code INTEGER UNIQUE NOT NULL,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            id_unity INTEGER NOT NULL,
            FOREIGN KEY (id_unity) REFERENCES units(unity)
        );

        CREATE TABLE IF NOT EXISTS units (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            unity TEXT UNIQUE NOT NULL   
        );

        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category INT NOT NULL,
            affected_product_code INTEGER NOT NULL,
            transaction_date TEXT NOT NULL,
            FOREIGN KEY (affected_product_code) REFERENCES products(id),
            FOREIGN KEY (category) REFERENCES categories(id)
        );

        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT UNIQUE NOT NULL
        );
        ''')
    
    product: tuple = (1000000000008, 'PRODUCT NAME 8', 'THIS IS A PRODUCT NAME 8', 1000, 253.15, 'PZ')
    SELECT category FROM categories WHERE category = ?;
    INSERT INTO categories (category) VALUES (?);

    SELECT id FROM products WHERE code = ?;