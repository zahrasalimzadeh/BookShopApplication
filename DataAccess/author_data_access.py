import sqlite3

from Entities.author import Author


def get_author_list():
    author_list = []

    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
        Select  id
        ,       first_name
        ,       last_name
        From    Author""")
        rows = cursor.fetchall()
        for row in rows:
            author = Author(row[0], row[1], row[2])
            author_list.append(author)

    return author_list