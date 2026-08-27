import sqlite3
from datetime import datetime


def insert_order_with_items(customer_id, cart_items):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()

        order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(f"""
        INSERT INTO "Order" (customer_id, order_date)
        VALUES ({customer_id}, '{order_date}');""")

        order_id = cursor.lastrowid

        for book_id, item in cart_items.items():
            quantity = item["quantity"]
            unit_price = item["book"].price
            cursor.execute(f"""
            INSERT INTO OrderItem (order_id, book_id, quantity, unit_price)
            VALUES ({order_id}, {book_id}, {quantity}, {unit_price});""")

        connection.commit()
        return order_id