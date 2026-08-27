class Order:
    def __init__(self, id, customer, order_date, items):
        self.id = id
        self.customer = customer
        self.order_date = order_date
        self.items = items