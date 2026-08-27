import sqlite3
from Entities.customer import Customer


def insert_customer(first_name, last_name, phone_number):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute(f"""
        INSERT INTO Customer (first_name, last_name, phone_number)
        VALUES ('{first_name}', '{last_name}', '{phone_number}');""")
        connection.commit()
        return cursor.lastrowid


def get_customer_list():
    customer_list = []

    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
        Select  id
        ,       first_name
        ,       last_name
        ,       phone_number
        From    Customer""")
        rows = cursor.fetchall()
        for row in rows:
            customer = Customer(row[0], row[1], row[2], row[3])
            customer_list.append(customer)

    return customer_list