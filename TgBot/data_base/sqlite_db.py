import sqlite3 as sq
from datetime import datetime

base = sq.connect('db.db')
cur = base.cursor()
def sql_start():
    create_product_table()
    create_sell_table()


def create_product_table():
    cur.execute('''CREATE TABLE IF NOT EXISTS product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    product_type TEXT,
    description TEXT,
    photo TEXT,
    price INT,
    count INT)''')
    base.commit()


def add_product(data):
    cur.execute(
        f"""INSERT INTO product (name, product_type, description, photo, price, count)
            VALUES ('{data['name']}', '{data['product_type']}', '{data['description']}', '{data['photo']}', '{data['price']}', '{data['count']}')"""
    )
    base.commit()


def get_all_products():
    return cur.execute('SELECT * FROM product').fetchall()

def get_available_products():
    return cur.execute('SELECT * FROM product WHERE count > 0').fetchall()


def get_product_by_id(id):
    return cur.execute(f"SELECT * FROM product WHERE id = '{id}'").fetchall()
def get_all_products_by_type(type):
    return cur.execute(f"SELECT * FROM product WHERE product_type == '{type}'").fetchall()

def get_available_products_by_type(type):
    return cur.execute(
        f"SELECT * FROM product WHERE product_type = '{type}' AND count > 0"
    ).fetchall()




def remove_product(id):
    cur.execute(f'DELETE FROM product WHERE id == {id}')
    base.commit()


def update_product_count(product_id, count):
    cur.execute(f"UPDATE product SET count = {count} WHERE id = {product_id}")
    base.commit()

def decrease_product_count(product_id: int, amount: int = 1):
    cur.execute(
        f"""UPDATE product
            SET count = count - {amount}
            WHERE id = {product_id}"""
    )
    base.commit()






def create_sell_table():
    cur.execute('''CREATE TABLE IF NOT EXISTS sell(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tg_id INT,
    user_name TEXT,
    name TEXT,
    product_id INT,
    address TEXT,
    telephone TEXT,
    date DATE,
    status TEXT,
    review TEXT
      )''')
    base.commit()





def add_sell(data, user, product_id):
    cur.execute(
        f"""INSERT INTO sell (tg_id, user_name, name, product_id, address, telephone, date, status, review)
            VALUES (
                '{user.id}',
                '{user.username}',
                '{data['name']}',
                '{product_id}',
                '{data['address']}',
                '{data['telephone']}',
                '{datetime.now()}',
                'created',
                ''
            )"""
    )
    base.commit()
    return cur.lastrowid


def update_sell_status(sell_id, status):
    cur.execute(
        f"""UPDATE sell
            SET status = '{status}'
            WHERE id = {sell_id}"""
    )
    base.commit()


def update_sell_review(sell_id, review):
    cur.execute(
        f"""UPDATE sell
            SET review = '{review}'
            WHERE id = {sell_id}"""
    )
    base.commit()





def get_product_id_by_sell(sell_id):
    result = cur.execute("SELECT product_id FROM sell WHERE id = ?", (sell_id,)).fetchone()
    return result[0] if result else None
