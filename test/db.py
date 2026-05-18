import sqlite3
from pathlib import Path

DB_NAME = "base"

def connect():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def auth_user(login, password):
    sql = """
        SELECT users.id, users.full_name, roles.name AS role
        FROM users
        JOIN roles ON roles.id = users.role_id
        WHERE users.login = ? AND users.password = ?
    """
    with connect() as conn:
        row = conn.execute(sql, (login, password)).fetchone()
        return dict(row) if row else None


def get_products(search="", supplier="Все поставщики", sort_stock=""):
    sql = """
        SELECT
            products.article,
            products.name,
            units.name AS unit,
            products.price,
            suppliers.name AS supplier,
            manufacturers.name AS manufacturer,
            categories.name AS category,
            products.discount,
            products.stock_quantity,
            products.description,
            products.photo_url
        FROM products
        LEFT JOIN categories ON categories.id = products.category_id
        LEFT JOIN manufacturers ON manufacturers.id = products.manufacturer_id
        LEFT JOIN suppliers ON suppliers.id = products.supplier_id
        LEFT JOIN units ON units.id = products.unit_id
        WHERE 1 = 1
    """
    params = []

    if search:
        sql += """
            AND (
                products.article LIKE ? OR
                products.name LIKE ? OR 
                products.description LIKE ? OR
                categories.name LIKE ? OR
                manufacturers.name LIKE ? OR
                suppliers.name LIKE ?
            )
        """
        params += [f"%{search}%"] * 6

    if supplier and supplier != "Все поставщики":
        sql += " AND suppliers.name = ?"
        params.append(supplier)

    if sort_stock == "По возрастанию":
        sql += " ORDER BY products.stock_quantity ASC"
    elif sort_stock == "По убыванию":
        sql += " ORDER BY products.stock_quantity DESC"
    else:
        sql += " ORDER BY products.name"

    with connect() as conn:
        return [dict(row) for row in conn.execute(sql, params).fetchall()]


def get_suppliers():
    with connect() as conn:
        rows = conn.execute("SELECT name FROM suppliers ORDER BY name").fetchall()
        return [row["name"] for row in rows]


def get_names(table):
    with connect() as conn:
        rows = conn.execute(f"SELECT name FROM {table} ORDER BY name").fetchall()
        return [row["name"] for row in rows]


def get_or_create_id(conn, table, name):
    if not name:
        return None
    row = conn.execute(f"SELECT id FROM {table} WHERE name = ?", (name,)).fetchone()
    if row:
        return row["id"]
    cur = conn.execute(f"INSERT INTO {table}(name) VALUES (?)", (name,))
    return cur.lastrowid


def add_product(data):
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
                data["article"], data["name"], category_id, manufacturer_id,
                supplier_id, unit_id, data["price"], data["discount"],
                data["stock_quantity"], data["description"], data["photo_url"]
            ))
            conn.commit()
            return True, "Товар добавлен"
    except sqlite3.IntegrityError:
        return False, "Товар с таким артикулом уже есть"


def update_product(article, data):
    with connect() as conn:
        category_id = get_or_create_id(conn, "categories", data["category"])
        manufacturer_id = get_or_create_id(conn, "manufacturers", data["manufacturer"])
        supplier_id = get_or_create_id(conn, "suppliers", data["supplier"])
        unit_id = get_or_create_id(conn, "units", data["unit"])

        conn.execute("""
            UPDATE products
            SET name = ?, category_id = ?, manufacturer_id = ?, supplier_id = ?,
                unit_id = ?, price = ?, discount = ?, stock_quantity = ?,
                description = ?, photo_url = ?
            WHERE article = ?
        """, (
            data["name"], category_id, manufacturer_id, supplier_id,
            unit_id, data["price"], data["discount"], data["stock_quantity"],
            data["description"], data["photo_url"], article
        ))
        conn.commit()
        return True, "Товар изменён"


def delete_product(article):
    if in_orders(article):
        return False, "Товар есть в заказе, удалить нельзя"
    with connect() as conn:
        conn.execute("DELETE FROM products WHERE article = ?", (article,))
        conn.commit()
    return True, "Товар удалён"


def in_orders(article):
    with connect() as conn:
        row = conn.execute(
            "SELECT id FROM order_items WHERE product_article = ? LIMIT 1",
            (article,)
        ).fetchone()
        return row is not None
