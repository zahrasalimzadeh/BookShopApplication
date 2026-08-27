import sqlite3
from Entities.category import Category


def get_category_list():
    category_list = []

    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
        Select  id
        ,       title
        From    Category""")
        rows = cursor.fetchall()
        for row in rows:
            category = Category(row[0], row[1])
            category_list.append(category)

    return category_list


def insert_category(title):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute(f"""
        INSERT INTO Category (title)
        VALUES ('{title}');""")
        connection.commit()