class Author:
    def __init__(self, id, firstname, lastname):
        self.id = id
        self.first_name = firstname
        self.last_name = lastname

    def get_information(self):
        return f"{self.id}-{self.first_name} {self.last_name}"

    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"