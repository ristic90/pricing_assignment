from sqlalchemy import Column, Integer, String, Float

from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    pages = Column(Integer)
    rating = Column(Float)
    price = Column(Float)

    def __repr__(self):
        return (
            f"<BookORM(id={self.id}, title={self.title}, "
            f"author={self.author}, pages={self.pages}, "
            f"rating={self.rating}, price={self.price})>"
        )
