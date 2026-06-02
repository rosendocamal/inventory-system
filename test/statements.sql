-- Create tables

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

-- Example testing
/*
INSERT INTO products (code, name, description, quantity, price, id_unity) VALUES (1000000000000, 'PRODUCT NAME 0', 'THIS IS A PRODUCT NAME 0', 1000, 254.75, 1);
INSERT INTO products (code, name, description, quantity, price, id_unity) VALUES (1000000000001, 'PRODUCT NAME 1', 'THIS IS A PRODUCT NAME 1', 2000, 254.15, 1);
INSERT INTO products (code, name, description, quantity, price, id_unity) VALUES (1000000000002, 'PRODUCT NAME 2', 'THIS IS A PRODUCT NAME 2', 3000, 250.25, 1);
INSERT INTO products (code, name, description, quantity, price, id_unity) VALUES (1000000000003, 'PRODUCT NAME 3', 'THIS IS A PRODUCT NAME 3', 4000, 250.35, 1);
INSERT INTO products (code, name, description, quantity, price, id_unity) VALUES (1000000000004, 'PRODUCT NAME 4', 'THIS IS A PRODUCT NAME 4', 5000, 251.45, 1);
INSERT INTO products (code, name, description, quantity, price, id_unity) VALUES (1000000000005, 'PRODUCT NAME 5', 'THIS IS A PRODUCT NAME 5', 1000, 251.55, 1);
INSERT INTO products (code, name, description, quantity, price, id_unity) VALUES (1000000000006, 'PRODUCT NAME 6', 'THIS IS A PRODUCT NAME 6', 1000, 252.55, 1);
INSERT INTO products (code, name, description, quantity, price, id_unity) VALUES (1000000000007, 'PRODUCT NAME 7', 'THIS IS A PRODUCT NAME 7', 1000, 252.25, 1);
INSERT INTO products (code, name, description, quantity, price, id_unity) VALUES (1000000000008, 'PRODUCT NAME 8', 'THIS IS A PRODUCT NAME 8', 1000, 253.15, 1);
INSERT INTO products (code, name, description, quantity, price, id_unity) VALUES (1000000000009, 'PRODUCT NAME 9', 'THIS IS A PRODUCT NAME 9', 7004, 253.15, 2);

SELECT id FROM units WHERE unity = 'PZ';
INSERT INTO units (unity) VALUES ('PZ');
SELECT id FROM units WHERE unity = 'PZ';

INSERT INTO units (unity) VALUES ('ML');
SELECT id FROM units WHERE unity = 'ML';
*/

-- Save to transactions

/* Second search the category in categories and extract the id category with next commands:
    SELECT category FROM categories WHERE category = 'ADD PRODUCT';
    INSERT INTO categories (category) VALUES ('ADD PRODUCT');
    SELECT category FROM categories WHERE category = 'ADD PRODUCT';
   Before the execute first line command, if exist id, then next process.
   If not exist category id, then insert command and repeat first line command and extract the id.
   Logic step is similar to search code product in first statement sql.
*/
SELECT category FROM categories WHERE category = ?;
INSERT INTO categories (category) VALUES (?);

SELECT id FROM products WHERE code = ?;

/* Third insert the transactions with the next command:
    INSERT INTO transactions (category, affected_product_code, transaction_date) VALUES (1, 2, '2025-09-25 12:12:12');
*/

INSERT INTO transactions (category, affected_product_code, transaction_date) VALUES (?, ?, ?);

-- Save to products

/* First search the code in products table with next command:
    SELECT code FROM products WHERE code = 1000000000000;
   If exists code, then failure add.
   If not exists code, the add product with next commands.
*/
SELECT code FROM products WHERE code = ?;

/* Second search the unity in units and extract the id unit with next commands:
    SELECT id FROM units WHERE unity = 'PZ';
    INSERT INTO units (unity) VALUES ('PZ');
    SELECT id FROM units WHERE unity = 'PZ';
   Before the execute first line command, if exist id, then next process.
   If not exist unit id, then insert command and repeat first line command and extract the id.
*/
SELECT id FROM units WHERE unity = ?;
INSERT INTO units (unity) VALUES (?);


/* Third insert the product with the next command (example):
    INSERT INTO products (code, name, description, quantity, price, id_unity) VALUES (1000000000000, 'PRODUCT NAME 0', 'THIS IS A PRODUCT NAME 0', 1000, 254.75, 1);
*/

INSERT INTO products (code, name, description, quantity, price, id_unity) VALUES (?, ?, ?, ?, ?, ?);

-- Delete from products

/* First execute command for delete product.
   If failured search, then not continue with delete.
*/
SELECT code FROM products WHERE code = ?;

/* Second execute command.
   If quantity is not equal a zero, then stop.
*/
SELECT quantity FROM products WHERE code = ?;

/* Third step. If quantity is equal to zero, the execute delete.
   Altenartive command:
    DELETE FROM products WHERE code = ? AND quantity == ?;
*/
DELETE FROM products WHERE code = ?;

-- Search code in products

/* If right search, then execute command */
SELECT code,
    name ,
    description,
    quantity,
    price,
    (units.unity)
FROM products
INNER JOIN units ON units.id = products.id_unity
WHERE code = ?;

-- Search name in products

/* If right search, then execute command */
SELECT code,
    name ,
    description,
    quantity,
    price,
    (units.unity)
FROM products
INNER JOIN units ON units.id = products.id_unity
WHERE name = ?;

-- Update data in products

UPDATE products
SET quantity = (SELECT quantity FROM products WHERE code = ?) + ?
WHERE code = ?;

-- Value from products

SELECT (quantity * price) FROM products;

-- View all products

SELECT code, name, description, quantity, price, units.unity
FROM products
INNER JOIN units ON units.id = products.id_unity;

-- View low stocks in products

SELECT code, name, description, quantity, price, units.unity
FROM products
INNER JOIN units ON units.id = products.id_unity
WHERE quantity <= 15;

-- View all in transactions

SELECT transactions.id, categories.category, products.code, transaction_date 
FROM transactions
INNER JOIN categories ON categories.id = transactions.category
INNER JOIN products ON products.id = transactions.affected_product_code;