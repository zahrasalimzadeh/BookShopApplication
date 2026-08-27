from tkinter import Entry, Frame, Label, Menu, Menubutton, PhotoImage, Tk, Toplevel, Canvas, Scrollbar
from tkinter.ttk import Combobox
from PIL import Image, ImageTk

from DataAccess.author_data_access import get_author_list
from DataAccess.book_data_access import get_book_list, insert_book, delete_book, update_book, get_book_by_id, reduce_stock
from DataAccess.publisher_data_access import get_publisher_list
from DataAccess.category_data_access import get_category_list
from DataAccess.customer_data_access import insert_customer
from DataAccess.order_data_access import insert_order_with_items

window = Tk()
window.state("zoomed")
window.title("BookShopApplication")
window.configure(bg="#F4F6F9")

window.grid_columnconfigure(0, weight=1)

book_icon = PhotoImage(file="bookicon.png")
book_icon = book_icon.subsample(25, 25)
window.iconphoto(False, book_icon)

header_frame = Frame(window, bg="#071E3D", width=1280, height=80)
header_frame.grid(row=0, column=0, sticky="ew")
header_frame.grid_propagate(False)

header_frame.grid_rowconfigure(0, weight=1)
header_frame.grid_rowconfigure(1, weight=1)

book_image = PhotoImage(file="book.png")
book_image = book_image.subsample(15, 15)

header_image = Label(header_frame, image=book_image, bg="#071E3D")
header_image.grid(row=0, column=0, rowspan=2, padx=(15, 10))

header_label_1 = Label(header_frame,
                    text="BookStore", 
                    bg="#071E3D",
                    fg="#EBE8E8", 
                    font=("Segoe UI", 16, "bold"))
header_label_1.grid(row=0, column=1, sticky="sw", pady=(10, 0))

header_label_2 = Label(header_frame,
                    text="Find your favorite book", 
                    bg="#071E3D",
                    fg="#9FB0C8", 
                    font=("Segoe UI", 10))
header_label_2.grid(row=1, column=1, sticky="nw", pady=(0, 10))

title_frame = Frame(window, bg="#F4F6F9")
title_frame.grid(row=1, column=0, sticky="ew")

title_label = Label(title_frame, 
                    text="Featured Books", 
                    bg="#F4F6F9",
                    fg="#071E3D", 
                    font=("Segoe UI", 20, "bold"))
title_label.grid(row=0, column=0, sticky="w", padx=(30, 0), pady=(20, 0))

subtitle_label = Label(title_frame,
                    text="A collection of our bestsellers and new arrivals",
                    bg="#F4F6F9",
                    fg="#718096",
                    font=("Segoe UI", 10))
subtitle_label.grid(row=1, column=0, sticky="w", padx=(30, 0))

search_frame = Frame(window, bg="#F4F6F9")
search_frame.grid(row=2, column=0, sticky="ew", padx=30, pady=(15, 0))
search_frame.grid_columnconfigure(0, weight=1)

search_box = Frame(search_frame,
                bg="#F7FAFC", 
                highlightthickness=1,
                highlightbackground="#CBD5E0",
                highlightcolor="#071E3D")
search_box.grid(row=0, column=0, sticky="ew", padx=(0, 15))
search_box.grid_columnconfigure(1, weight=1)

search_icon_block = Frame(search_box, bg="#071E3D", width=46, height=44)
search_icon_block.grid(row=0, column=0, sticky="ns")
search_icon_block.grid_propagate(False)
search_icon_block.grid_columnconfigure(0, weight=1)
search_icon_block.grid_rowconfigure(0, weight=1)

search_icon = Label(search_icon_block,
                    text="🔍", 
                    bg="#071E3D", 
                    fg="#FFFFFF",
                    font=("Segoe UI", 12))
search_icon.grid(row=0, column=0)

search_entry = Entry(search_box,
    bg="#F7FAFC",
    fg="#718096",
    insertbackground="#071E3D",
    font=("Tahoma", 12),
    relief="flat",
    bd=0
)
search_entry.grid(row=0, column=1, sticky="ew", ipady=10, padx=(12, 12))
search_entry.insert(0, "Search by Title, Author, or Publisher,...")

def clear_placeholder(event):
    if search_entry.get() == "Search by Title, Author, or Publisher,...":
        search_entry.delete(0, "end")
        search_entry.configure(fg="#071E3D")

def restore_placeholder(event):
    if search_entry.get().strip() == "":
        search_entry.insert(0, "Search by Title, Author, or Publisher,...")
        search_entry.configure(fg="#718096")
    elif len(books_frame.winfo_children()) == 0:
        search_entry.delete(0, "end")
        search_entry.insert(0, "Search by Title, Author, or Publisher,...")
        search_entry.configure(fg="#718096")
        load_books()

def perform_search(event=None):
    text = search_entry.get()
    if text == "Search by Title, Author, or Publisher,...":
        text = ""
    load_books(text)

search_entry.bind("<FocusIn>", clear_placeholder)
search_entry.bind("<FocusOut>", restore_placeholder)

search_entry.bind("<Return>", perform_search)
search_icon.bind("<Button-1>", perform_search)

def show_add_book_form():
    form = Toplevel(window)
    form.title("Add New Book")
    form.geometry("350x440")
    form.configure(bg="#F4F6F9")

    Label(form, text="Title", bg="#F4F6F9", fg="#071E3D", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20, pady=(20, 0))
    title_entry = Entry(form, font=("Segoe UI", 10))
    title_entry.pack(fill="x", padx=20, pady=(0, 10))

    Label(form, text="Price", bg="#F4F6F9", fg="#071E3D", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20)
    price_entry = Entry(form, font=("Segoe UI", 10))
    price_entry.pack(fill="x", padx=20, pady=(0, 10))

    Label(form, text="Stock", bg="#F4F6F9", fg="#071E3D", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20)
    stock_entry = Entry(form, font=("Segoe UI", 10))
    stock_entry.pack(fill="x", padx=20, pady=(0, 10))

    Label(form, text="Cover Image Path", bg="#F4F6F9", fg="#071E3D", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20)
    cover_entry = Entry(form, font=("Segoe UI", 10))
    cover_entry.pack(fill="x", padx=20, pady=(0, 10))

    Label(form, text="Author", bg="#F4F6F9", fg="#071E3D", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20)
    author_values = [author.get_information() for author in get_author_list()]
    author_combobox = Combobox(form, values=author_values, state="readonly", font=("Segoe UI", 10))
    author_combobox.pack(fill="x", padx=20, pady=(0, 10))

    Label(form, text="Publisher", bg="#F4F6F9", fg="#071E3D", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20)
    publisher_values = [publisher.get_information() for publisher in get_publisher_list()]
    publisher_combobox = Combobox(form, values=publisher_values, state="readonly", font=("Segoe UI", 10))
    publisher_combobox.pack(fill="x", padx=20, pady=(0, 10))

    Label(form, text="Category", bg="#F4F6F9", fg="#071E3D", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20)
    category_values = [category.get_information() for category in get_category_list()]
    category_combobox = Combobox(form, values=category_values, state="readonly", font=("Segoe UI", 10))
    category_combobox.pack(fill="x", padx=20, pady=(0, 15))

    def submit_clicked(event=None):
        title = title_entry.get()
        price = float(price_entry.get())
        stock = int(stock_entry.get())
        author_id = int(author_combobox.get().split('-')[0])
        publisher_id = int(publisher_combobox.get().split('-')[0])

        category_id = None
        if category_combobox.get():
            category_id = int(category_combobox.get().split('-')[0])

        cover_image = cover_entry.get().strip()
        if cover_image == "":
            cover_image = None
        insert_book(title, price, stock, cover_image, publisher_id, author_id, category_id)

        load_books()
        form.destroy()

    submit_btn = Label(form, text="Submit", bg="#071E3D", fg="white",
                        font=("Segoe UI", 10, "bold"), cursor="hand2")
    submit_btn.pack(fill="x", padx=20, ipady=6)
    submit_btn.bind("<Button-1>", submit_clicked)

def show_edit_book_form():
    if selected_book_id is None:
        return

    book = get_book_by_id(selected_book_id)

    form = Toplevel(window)
    form.title("Edit Book")
    form.geometry("350x440")
    form.configure(bg="#F4F6F9")

    Label(form, text="Title", bg="#F4F6F9", fg="#071E3D", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20, pady=(20, 0))
    title_entry = Entry(form, font=("Segoe UI", 10))
    title_entry.insert(0, book.title)
    title_entry.pack(fill="x", padx=20, pady=(0, 10))

    Label(form, text="Price", bg="#F4F6F9", fg="#071E3D", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20)
    price_entry = Entry(form, font=("Segoe UI", 10))
    price_entry.insert(0, book.price)
    price_entry.pack(fill="x", padx=20, pady=(0, 10))

    Label(form, text="Stock", bg="#F4F6F9", fg="#071E3D", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20)
    stock_entry = Entry(form, font=("Segoe UI", 10))
    stock_entry.insert(0, book.stock)
    stock_entry.pack(fill="x", padx=20, pady=(0, 10))

    Label(form, text="Cover Image Path", bg="#F4F6F9", fg="#071E3D", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20)
    cover_entry = Entry(form, font=("Segoe UI", 10))
    if book.cover_image:
        cover_entry.insert(0, book.cover_image)
    cover_entry.pack(fill="x", padx=20, pady=(0, 10))

    Label(form, text="Author", bg="#F4F6F9", fg="#071E3D", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20)
    author_values = [author.get_information() for author in get_author_list()]
    author_combobox = Combobox(form, values=author_values, state="readonly", font=("Segoe UI", 10))
    author_combobox.set(book.author.get_information())
    author_combobox.pack(fill="x", padx=20, pady=(0, 10))

    Label(form, text="Publisher", bg="#F4F6F9", fg="#071E3D", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20)
    publisher_values = [publisher.get_information() for publisher in get_publisher_list()]
    publisher_combobox = Combobox(form, values=publisher_values, state="readonly", font=("Segoe UI", 10))
    publisher_combobox.set(book.publisher.get_information())
    publisher_combobox.pack(fill="x", padx=20, pady=(0, 10))

    Label(form, text="Category", bg="#F4F6F9", fg="#071E3D", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20)
    category_values = [category.get_information() for category in get_category_list()]
    category_combobox = Combobox(form, values=category_values, state="readonly", font=("Segoe UI", 10))
    if book.category:
        category_combobox.set(book.category.get_information())
    category_combobox.pack(fill="x", padx=20, pady=(0, 15))

    def submit_clicked(event=None):
        title = title_entry.get()
        price = float(price_entry.get())
        stock = int(stock_entry.get())
        author_id = int(author_combobox.get().split('-')[0])
        publisher_id = int(publisher_combobox.get().split('-')[0])

        category_id = None
        if category_combobox.get():
            category_id = int(category_combobox.get().split('-')[0])

        cover_image = cover_entry.get().strip()
        if cover_image == "":
            cover_image = None
        update_book(selected_book_id, title, price, stock, cover_image, author_id, publisher_id, category_id)

        load_books()
        form.destroy()

    submit_btn = Label(form, text="Submit", bg="#071E3D", fg="white",
                        font=("Segoe UI", 10, "bold"), cursor="hand2")
    submit_btn.pack(fill="x", padx=20, ipady=6)
    submit_btn.bind("<Button-1>", submit_clicked)

def delete_selected_book():
    if selected_book_id is None:
        return

    delete_book(selected_book_id)
    load_books()

manage_btn = Menubutton(search_frame,
    text="Manage Books  ▾",
    bg="#071E3D",
    fg="#FFFFFF",
    activebackground="#16345E",
    activeforeground="#FFFFFF",
    font=("Segoe UI", 11, "bold"),
    relief="flat",
    bd=0,
    cursor="hand2"
)
manage_btn.grid(row=0, column=1, ipady=8, ipadx=10)

manage_menu = Menu(manage_btn, tearoff=0, font=("Segoe UI", 10))
manage_menu.add_command(label="➕    Add New Book", 
                        foreground="#136136",
                        font=("Segoe UI", 12),
                        command=show_add_book_form)
manage_menu.add_separator()
manage_menu.add_command(label="✏️    Edit Selected Book",
                        foreground="#1B55C0", 
                        font=("Segoe UI", 12),
                        command=show_edit_book_form)
manage_menu.add_separator()
manage_menu.add_command(label="🗑️Delete Selected Book", 
                        foreground="#C62828", 
                        font=("Segoe UI", 12),
                        command=delete_selected_book)

manage_btn["menu"] = manage_menu

category_filter_frame = Frame(window, bg="#F4F6F9")
category_filter_frame.grid(row=3, column=0, sticky="ew", padx=30, pady=(10, 0))

selected_category_id = None

def show_category(category_id):
    global selected_category_id
    selected_category_id = category_id
    load_books(category_id=selected_category_id)

all_categories_btn = Label(category_filter_frame, text="All", bg="#071E3D", fg="white",
                        font=("Segoe UI", 10, "bold"), cursor="hand2")
all_categories_btn.pack(side="left", padx=(0, 8), ipady=5, ipadx=12)
def show_all_categories(event=None):
    show_category(None)

all_categories_btn.bind("<Button-1>", show_all_categories)

def make_category_handler(cat_id):
    def handler(event=None):
        show_category(cat_id)
    return handler
for category in get_category_list():
    category_btn = Label(category_filter_frame, text=category.title, bg="#E2E8F0", fg="#071E3D",
                        font=("Segoe UI", 10, "bold"), cursor="hand2")
    category_btn.pack(side="left", padx=(0, 8), ipady=5, ipadx=12)
    category_btn.bind("<Button-1>", make_category_handler(category.id))

BOOKS_PER_ROW = 7

books_container = Frame(window, bg="#F4F6F9")
books_container.grid(row=4, column=0, sticky="nsew", padx=30, pady=(10, 20))

window.grid_rowconfigure(4, weight=1)
window.grid_rowconfigure(5, weight=0)

books_container.grid_rowconfigure(0, weight=1)
books_container.grid_columnconfigure(0, weight=1)

books_canvas = Canvas(books_container, bg="#F4F6F9", highlightthickness=0)
books_canvas.grid(row=0, column=0, sticky="nsew")

books_scrollbar = Scrollbar(books_container, orient="vertical", command=books_canvas.yview)
books_scrollbar.grid(row=0, column=1, sticky="ns")

books_canvas.configure(yscrollcommand=books_scrollbar.set)

books_frame = Frame(books_canvas, bg="#F4F6F9")
books_frame_window = books_canvas.create_window((0, 0), window=books_frame, anchor="nw")

def _on_books_frame_configure(event=None):
    books_canvas.configure(scrollregion=books_canvas.bbox("all"))

books_frame.bind("<Configure>", _on_books_frame_configure)

def _on_books_canvas_configure(event):
    books_canvas.itemconfig(books_frame_window, width=event.width)

books_canvas.bind("<Configure>", _on_books_canvas_configure)

def _on_mousewheel(event):
    if event.delta:
        books_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    else:
        if event.num == 4:
            books_canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            books_canvas.yview_scroll(1, "units")

def _bind_mousewheel(event):
    books_canvas.bind_all("<MouseWheel>", _on_mousewheel)
    books_canvas.bind_all("<Button-4>", _on_mousewheel)
    books_canvas.bind_all("<Button-5>", _on_mousewheel)

def _unbind_mousewheel(event):
    books_canvas.unbind_all("<MouseWheel>")
    books_canvas.unbind_all("<Button-4>")
    books_canvas.unbind_all("<Button-5>")

books_canvas.bind("<Enter>", _bind_mousewheel)
books_canvas.bind("<Leave>", _unbind_mousewheel)

cart_bar = Frame(window, bg="white", height=70, highlightthickness=1, highlightbackground="#E2E8F0")
cart_bar.grid(row=5, column=0, sticky="ew")
cart_bar.grid_propagate(False)
cart_bar.grid_columnconfigure(0, weight=1)
cart_bar.grid_rowconfigure(0, weight=1)

cart_summary_frame = Frame(cart_bar, bg="white")
cart_summary_frame.grid(row=0, column=0, sticky="w", padx=30)

items_count_label = Label(cart_summary_frame, text="🛒 0 items", bg="white",
                        fg="#071E3D", font=("Segoe UI", 12, "bold"))
items_count_label.grid(row=0, column=0, padx=(0, 8))

total_price_label = Label(cart_summary_frame, text="💰 Total: $0.00", bg="white",
                        fg="#071E3D", font=("Segoe UI", 12, "bold"))
total_price_label.grid(row=0, column=1)

checkout_btn = Label(cart_bar, text="💳  Proceed to Checkout", bg="#071E3D", fg="white",
                    font=("Segoe UI", 11, "bold"), cursor="hand2")
checkout_btn.grid(row=0, column=1, sticky="e", padx=30, ipady=8, ipadx=15)

selected_book_id = None

cart = {}

def update_cart_summary():
    total_items = sum(item["quantity"] for item in cart.values())
    total_price = sum(item["book"].price * item["quantity"] for item in cart.values())
    items_count_label.config(text=f"🛒 {total_items} items")
    total_price_label.config(text=f"💰 Total: ${total_price:.2f}")

def show_cart_view(event=None):
    cart_window = Toplevel(window)
    cart_window.title("Your Cart")
    cart_window.geometry("420x400")
    cart_window.configure(bg="#F4F6F9")

    Label(cart_window, text="Your Cart", bg="#F4F6F9", fg="#071E3D",
        font=("Segoe UI", 14, "bold")).pack(anchor="w", padx=20, pady=(20, 10))

    items_container = Frame(cart_window, bg="#F4F6F9")
    items_container.pack(fill="both", expand=True, padx=20)

    def refresh_cart_window():
        for child in items_container.winfo_children():
            child.destroy()

        if len(cart) == 0:
            Label(items_container, text="Your cart is empty", bg="#F4F6F9",
                fg="#718096", font=("Segoe UI", 10)).pack(pady=20)
            return

        for book_id, item in cart.items():
            row = Frame(items_container, bg="white", highlightthickness=1,
                        highlightbackground="#E2E8F0")
            row.pack(fill="x", pady=5)

            info_label = Label(row, bg="white", fg="#071E3D", font=("Segoe UI", 10, "bold"),
                            text=f"{item['book'].title}\n${item['book'].price * item['quantity']:.2f}",
                            justify="left")
            info_label.pack(side="left", padx=10, pady=10)

            def decrease_qty(event=None, book_id=book_id):
                cart[book_id]["quantity"] -= 1
                if cart[book_id]["quantity"] <= 0:
                    del cart[book_id]
                update_cart_summary()
                refresh_cart_window()

            def increase_qty(event=None, book_id=book_id):
                book_obj = cart[book_id]["book"]
                if cart[book_id]["quantity"] + 1 > book_obj.stock:
                    return
                cart[book_id]["quantity"] += 1
                update_cart_summary()
                refresh_cart_window()

            def remove_item(event=None, book_id=book_id):
                del cart[book_id]
                update_cart_summary()
                refresh_cart_window()

            controls = Frame(row, bg="white")
            controls.pack(side="right", padx=10)

            minus_btn = Label(controls, text="➖", bg="#F4F6F9", fg="#071E3D",
                            font=("Segoe UI", 10, "bold"), cursor="hand2", width=3)
            minus_btn.pack(side="left", padx=2)
            minus_btn.bind("<Button-1>", decrease_qty)

            qty_label = Label(controls, text=str(item["quantity"]), bg="white", fg="#071E3D",
                            font=("Segoe UI", 10, "bold"), width=2)
            qty_label.pack(side="left")

            plus_btn = Label(controls, text="➕", bg="#F4F6F9", fg="#071E3D",
                            font=("Segoe UI", 10, "bold"), cursor="hand2", width=3)
            plus_btn.pack(side="left", padx=2)
            plus_btn.bind("<Button-1>", increase_qty)

            remove_btn = Label(controls, text="✖", bg="white", fg="#C62828",
                            font=("Segoe UI", 11, "bold"), cursor="hand2", width=3)
            remove_btn.pack(side="left", padx=(8, 0))
            remove_btn.bind("<Button-1>", remove_item)

    refresh_cart_window()


items_count_label.bind("<Button-1>", show_cart_view)

def show_checkout_form(event=None):
    if len(cart) == 0:
        return

    form = Toplevel(window)
    form.title("Checkout")
    form.geometry("350x400")
    form.configure(bg="#F4F6F9")

    total_items = sum(item["quantity"] for item in cart.values())
    total_price = sum(item["book"].price * item["quantity"] for item in cart.values())

    Label(form, text="Customer Information", bg="#F4F6F9", fg="#071E3D",
        font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=20, pady=(20, 5))
    Label(form, text=f"{total_items} items — Total: ${total_price:.2f}", bg="#F4F6F9",
        fg="#718096", font=("Segoe UI", 9)).pack(anchor="w", padx=20, pady=(0, 15))

    Label(form, text="First Name", bg="#F4F6F9", fg="#071E3D", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20)
    first_name_entry = Entry(form, font=("Segoe UI", 10))
    first_name_entry.pack(fill="x", padx=20, pady=(0, 10))

    Label(form, text="Last Name", bg="#F4F6F9", fg="#071E3D", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20)
    last_name_entry = Entry(form, font=("Segoe UI", 10))
    last_name_entry.pack(fill="x", padx=20, pady=(0, 10))

    Label(form, text="Phone Number", bg="#F4F6F9", fg="#071E3D", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=20)
    phone_entry = Entry(form, font=("Segoe UI", 10))
    phone_entry.pack(fill="x", padx=20, pady=(0, 10))

    error_label = Label(form, text="", bg="#F4F6F9", fg="#C62828",
                        font=("Segoe UI", 9), wraplength=310, justify="left")
    error_label.pack(anchor="w", padx=20)

    def submit_clicked(event=None):
        first_name = first_name_entry.get().strip()
        last_name = last_name_entry.get().strip()
        phone = phone_entry.get().strip()

        if first_name == "" or last_name == "" or phone == "":
            error_label.config(text="لطفاً همه‌ی اطلاعات مشتری رو پر کن.")
            return

        customer_id = insert_customer(first_name, last_name, phone)

        insert_order_with_items(customer_id, cart)

        for book_id, item in cart.items():
            reduce_stock(book_id, item["quantity"])

        cart.clear()
        update_cart_summary()
        load_books()
        form.destroy()

        success_window = Toplevel(window)
        success_window.title("Success")
        success_window.geometry("300x120")
        success_window.configure(bg="#F4F6F9")
        Label(success_window, text="✅ Order placed successfully!", bg="#F4F6F9",
            fg="#071E3D", font=("Segoe UI", 11, "bold")).pack(expand=True)

    submit_btn = Label(form, text="Submit Order", bg="#071E3D", fg="white",
                        font=("Segoe UI", 10, "bold"), cursor="hand2")
    submit_btn.pack(fill="x", padx=20, pady=(10, 0), ipady=6)
    submit_btn.bind("<Button-1>", submit_clicked)


checkout_btn.bind("<Button-1>", show_checkout_form)

def create_book_card(parent, book, row, column):
    card = Frame(parent, bg="white", highlightthickness=2,
                highlightbackground="#E2E8F0", width=220, height=300)
    card.grid(row=row, column=column, padx=10, pady=10, sticky="n")
    card.grid_propagate(False)
    if book.cover_image:
        pil_img = Image.open(book.cover_image)
        pil_img = pil_img.resize((130, 165))
        cover_img = ImageTk.PhotoImage(pil_img)
        cover_label = Label(card, image=cover_img, bg="white")
        cover_label.image = cover_img
        cover_label.pack(pady=(10, 10), padx=10)
    else:
        cover_label = Frame(card, bg="#CBD5E0", width=133, height=200)
        cover_label.pack(pady=(10, 10), padx=10)
        cover_label.pack_propagate(False)

    title_label = Label(card, text=book.title, bg="white", fg="#071E3D",
                        font=("Segoe UI", 11, "bold"), wraplength=200, justify="left")
    title_label.pack(anchor="w", padx=10)

    def select_card(event=None):
        global selected_book_id
        for child in parent.winfo_children():
            child.configure(highlightbackground="#E2E8F0")
        card.configure(highlightbackground="#071E3D")
        selected_book_id = book.id

    card.bind("<Button-1>", select_card)
    cover_label.bind("<Button-1>", select_card)
    title_label.bind("<Button-1>", select_card)

    author_label = Label(card, text=book.author.get_fullname(), bg="white",
                        fg="#718096", font=("Segoe UI", 9))
    author_label.pack(anchor="w", padx=10)

    price_stock_frame = Frame(card, bg="white")
    price_stock_frame.pack(fill="x", padx=10, pady=(5, 5))

    price_label = Label(price_stock_frame, text=f"${book.price}", bg="white",
                        fg="#071E3D", font=("Segoe UI", 11, "bold"))
    price_label.pack(side="left")

    stock_label = Label(price_stock_frame, text=f"Stock: {book.stock}", bg="white",
                        fg="#071E3D", font=("Segoe UI", 10, "bold"))
    stock_label.pack(side="right")

    add_to_cart_btn = Label(card, text="Add to Cart", bg="#071E3D", fg="white",
                            font=("Segoe UI", 10, "bold"), cursor="hand2")
    add_to_cart_btn.pack(fill="x", padx=10, pady=(5, 10), ipady=5)

    def add_to_cart(event=None):
        current_qty_in_cart = cart[book.id]["quantity"] if book.id in cart else 0

        if current_qty_in_cart + 1 > book.stock:
            warning_window = Toplevel(window)
            warning_window.title("Not Enough Stock")
            warning_window.geometry("300x120")
            warning_window.configure(bg="#F4F6F9")
            Label(warning_window, text=f"Only {book.stock} left in stock!", bg="#F4F6F9",
                fg="#C62828", font=("Segoe UI", 11, "bold")).pack(expand=True)
            return

        if book.id in cart:
            cart[book.id]["quantity"] += 1
        else:
            cart[book.id] = {"book": book, "quantity": 1}

        update_cart_summary()

    add_to_cart_btn.bind("<Button-1>", add_to_cart)


def load_books(search_text="", category_id=None):
    children = books_frame.winfo_children()
    for child in children:
        child.destroy()

    book_list = get_book_list()

    if search_text.strip() != "":
        search_text_lower = search_text.lower()
        book_list = [
            book for book in book_list
            if search_text_lower in book.title.lower()
            or search_text_lower in book.author.get_fullname().lower()
            or search_text_lower in book.publisher.title.lower()
            or search_text_lower in str(book.price)
        ]

    if category_id is not None:
        book_list = [
            book for book in book_list
            if book.category is not None and book.category.id == category_id
        ]

    for index, book in enumerate(book_list):
        row = index // BOOKS_PER_ROW
        column = index % BOOKS_PER_ROW
        create_book_card(books_frame, book, row, column)

    books_frame.update_idletasks()
    books_canvas.configure(scrollregion=books_canvas.bbox("all"))
    books_canvas.yview_moveto(0)

load_books()
window.mainloop()