class BookEntity:
    def __init__(
        self,
        id: int,
        title: str,
        author: str,
        pages: int,
        price: float,
        rating: float,
    ):
        self.id = id
        self.title = title
        self.author = author
        self.pages = pages
        self.price = price
        self.rating = rating

    def to_dict(self):
        return {k: v for k, v in vars(self).items() if v is not None}

    def __repr__(self):
        return (
            f"<BookEntity(id={self.id}, title={self.title}, "
            f"author={self.author}, pages={self.pages}, "
            f"rating={self.rating}, price={self.price})>"
        )

    def __str__(self):
        return (
            f"<BookEntity(id={self.id}, title={self.title}, "
            f"author={self.author}, pages={self.pages}, "
            f"rating={self.rating}, price={self.price})>"
        )
