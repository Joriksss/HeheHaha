PRAGMA foreign_keys = ON;

CREATE TABLE roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id INTEGER NOT NULL,
    full_name TEXT NOT NULL,
    login TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    FOREIGN KEY (role_id) REFERENCES roles(id)
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE manufacturers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE units (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE pickup_points (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    address TEXT NOT NULL UNIQUE
);

CREATE TABLE products (
    article TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category_id INTEGER,
    manufacturer_id INTEGER,
    supplier_id INTEGER,
    unit_id INTEGER,
    price REAL NOT NULL CHECK(price >= 0),
    discount INTEGER NOT NULL DEFAULT 0 CHECK(discount >= 0 AND discount <= 100),
    stock_quantity INTEGER NOT NULL DEFAULT 0 CHECK(stock_quantity >= 0),
    description TEXT,
    photo_url TEXT,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
    FOREIGN KEY (unit_id) REFERENCES units(id)
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    order_date TEXT,
    delivery_date TEXT,
    pickup_point_id INTEGER,
    client_name TEXT,
    receive_code TEXT,
    status TEXT,
    FOREIGN KEY (pickup_point_id) REFERENCES pickup_points(id)
);

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_article TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_article) REFERENCES products(article)
);


heredef add_product(data):
    try:
        with connect() as conn:
            category_id = get_or_create_id(conn, "categories", data["category"])
            manufacturer_id = get_or_create_id(conn, "manufacturers", data["manufacturer"])
            supplier_id = get_or_create_id(conn, "suppliers", data["supplier"])
            unit_id = get_or_create_id(conn, "units", data["unit"])

            conn.execute("""
                INSERT INTO products(
                    article, name, unit_id, price, supplier_id, manufacturer_id, category_id,
                    discount, stock_quantity, description, photo_url
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data["article"],
                data["name"],
                unit_id,
                data["price"],
                supplier_id,
                manufacturer_id,
                category_id,
                data["discount"],
                data["stock_quantity"],
                data["description"],
                data["photo_url"]
            ))

            conn.commit()
            return True, "Товар добавлен"

    except sqlite3.IntegrityError:
        return False, "Товар с таким артикулом уже есть"

    except sqlite3.Error as error:
        return False, f"Ошибка базы данных: {error}"


def update_product(article, data):
    try:
        with connect() as conn:
            category_id = get_or_create_id(conn, "categories", data["category"])
            manufacturer_id = get_or_create_id(conn, "manufacturers", data["manufacturer"])
            supplier_id = get_or_create_id(conn, "suppliers", data["supplier"])
            unit_id = get_or_create_id(conn, "units", data["unit"])

            conn.execute("""
                UPDATE products
                SET 
                    name = ?,
                    unit_id = ?,
                    price = ?,
                    supplier_id = ?,
                    manufacturer_id = ?,
                    category_id = ?,
                    discount = ?,
                    stock_quantity = ?,
                    description = ?,
                    photo_url = ?
                WHERE article = ?
            """, (
                data["name"],
                unit_id,
                data["price"],
                supplier_id,
                manufacturer_id,
                category_id,
                data["discount"],
                data["stock_quantity"],
                data["description"],
                data["photo_url"],
                article
            ))

            conn.commit()
            return True, "Товар изменён"

    except sqlite3.Error as error:
        return False, f"Ошибка изменения: {error}"


def get_products(search="", supplier="Все поставщики", sort_stock=""):
    search = search.strip() if search else ""

    sql = """
        SELECT
            products.article,
            products.name,
            units.name AS unit,
