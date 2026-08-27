import sqlite3

from Entities.publisher import Publisher


def get_publisher_list():
    publisher_list = []

    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
        Select  id
        ,       title
        From    Publisher""")
        rows = cursor.fetchall()
        for row in rows:
            publisher = Publisher(row[0], row[1])
            publisher_list.append(publisher)

    return publisher_list