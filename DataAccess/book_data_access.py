import sqlite3

from Entities.author import Author
from Entities.book import Book
from Entities.publisher import Publisher
from Entities.category import Category


def get_book_list():
    book_list = []

    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
SELECT Book.id,
    Book.title,
    Book.price,
    Book.stock,
    Book.cover_image,
    Book.publisher_id,
    Publisher.title,
    Book.author_id,
    Author.first_name,
    Author.last_name,
    Book.category_id,
    Category.title
FROM   Book
Inner  Join Author    ON Book.author_id    = Author.id
Inner  Join Publisher ON Book.publisher_id = Publisher.id
Left   Join Category  ON Book.category_id  = Category.id""")
        rows = cursor.fetchall()
        for row in rows:
            book_author = Author(row[7], row[8], row[9])
            book_publisher = Publisher(row[5], row[6])
            book_category = Category(row[10], row[11]) if row[10] is not None else None
            book = Book(row[0], row[1], row[2], row[3], row[4], book_author, book_publisher, book_category)
            book_list.append(book)

    return book_list


def get_book_by_id(book_id):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute(f"""
SELECT Book.id,
       Book.title,
       Book.price,
       Book.stock,
       Book.cover_image,
       Book.publisher_id,
       Publisher.title,
       Book.author_id,
       Author.first_name,
       Author.last_name,
       Book.category_id,
       Category.title
FROM   Book
Inner  Join Author    ON Book.author_id    = Author.id
Inner  Join Publisher ON Book.publisher_id = Publisher.id
Left   Join Category  ON Book.category_id  = Category.id
Where  Book.id = {book_id}""")
        row = cursor.fetchone()
        book_author = Author(row[7], row[8], row[9])
        book_publisher = Publisher(row[5], row[6])
        book_category = Category(row[10], row[11]) if row[10] is not None else None
        book = Book(row[0], row[1], row[2], row[3], row[4], book_author, book_publisher, book_category)

        return book


def insert_book(title, price, stock, cover_image, publisher_id, author_id, category_id):
    cover_image_value = f"'{cover_image}'" if cover_image else "NULL"
    category_id_value = category_id if category_id else "NULL"
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute(f"""
        INSERT INTO Book (
                     title,
                     price,
                     stock,
                     cover_image,
                     publisher_id,
                     author_id,
                     category_id
                 )
                 VALUES (
                     '{title}',
                     {price},
                     {stock},
                     {cover_image_value},
                     {publisher_id},
                     {author_id},
                     {category_id_value}
                 );""")
        connection.commit()


def update_book(book_id, title, price, stock, cover_image, author_id, publisher_id, category_id):
    cover_image_value = f"'{cover_image}'" if cover_image else "NULL"
    category_id_value = category_id if category_id else "NULL"
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute(f"""
        UPDATE Book
        SET  title = '{title}',
             price = {price},
             stock = {stock},
             cover_image = {cover_image_value},
             publisher_id = {publisher_id},
             author_id = {author_id},
             category_id = {category_id_value}
        WHERE id = {book_id}""")
        connection.commit()


def delete_book(book_id):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute(f"""
        Delete From Book
        WHERE id = {book_id}""")
        connection.commit()


def reduce_stock(book_id, quantity):
    with sqlite3.connect("BookShopDB.db") as connection:
        cursor = connection.cursor()
        cursor.execute(f"""
        UPDATE Book
        SET  stock = stock - {quantity}
        WHERE id = {book_id}""")
        connection.commit()