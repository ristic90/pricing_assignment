from sqlalchemy import select
from sqlalchemy.exc import DataError, SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session

from app.db_models import Book as BookORM
from app.exceptions import DatabaseError, BookAlreadyExists, \
    BookDoesntExist
from app.pydantic_models import Book, BookUpdate


def get_all_books(db: Session):
    stmt = select(BookORM)
    result = db.execute(stmt)
    return result.scalars().all()


def get_book_by_id(book_id: int, db: Session):
    return db.get(BookORM, book_id)


def filter_books(
        db: Session,
        title: str | None = None,
        min_pages: int | None = None,
        max_pages: int | None = None,
        min_rating: float | None = None,
        max_rating: float | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
):
    stmt = select(BookORM)
    if title:
        stmt = stmt.where(BookORM.title == title)
    if min_pages:
        stmt = stmt.where(BookORM.pages >= min_pages)
    if max_pages:
        stmt = stmt.where(BookORM.pages <= max_pages)
    if min_rating:
        stmt = stmt.where(BookORM.rating >= min_rating)
    if max_rating:
        stmt = stmt.where(BookORM.rating <= max_rating)
    if min_price:
        stmt = stmt.where(BookORM.price >= min_price)
    if max_price:
        stmt = stmt.where(BookORM.price <= max_price)
    books = db.scalars(stmt).all()
    return books


def add_book_item(book: Book, db: Session):
    book_db = BookORM(**book.model_dump())
    try:
        db.add(book_db)
        db.commit()
        db.refresh(book_db)
    except IntegrityError:
        db.rollback()
        raise BookAlreadyExists(
            f"Book with ID {book.id} already exists",
        )
    except SQLAlchemyError:
        db.rollback()
        raise DatabaseError("Database error")
    return book_db


def update_book(book_id: int, book_update: BookUpdate, db: Session):
    book = db.query(BookORM).filter(BookORM.id == book_id).first()

    if not book:
        raise BookDoesntExist(
            f"Book with ID {book.id} doesnt exists",
        )

    update_data = book_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(book, field, value)

    try:
        db.commit()
        db.refresh(book)
    except DataError:  # db field constraint violated
        db.rollback()
        raise DatabaseError("Database error")

    return book


def delete_book(book_id: int, db: Session):
    book = db.query(BookORM).filter(BookORM.id == book_id).first()
    if not book:
        raise BookDoesntExist(f"Book with id {book_id} not found")

    try:
        db.delete(book)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseError("Database error")
