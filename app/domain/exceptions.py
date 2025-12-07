class BookAlreadyExists(Exception):
    def __init__(self, book_id: int):
        super().__init__(f"Book with ID={book_id} already exists")

    pass


class BookDoesntExist(Exception):
    def __init__(self, book_id: int):
        super().__init__(f"Book with ID={book_id} doesn't exist")


class DatabaseError(Exception):
    def __init__(self):
        super().__init__(f"Database error occurred")
