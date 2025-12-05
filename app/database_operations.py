from fastapi import HTTPException
from sqlalchemy.exc import DataError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.db_models import Book as BookORM
from app.pydantic_models import Book, BookUpdate


def get_all_books(db: Session):
    return db.query(BookORM).all()


def get_book_by_id(book_id: int, db: Session):
    book = db.query(BookORM).get(book_id)
    return Book.model_validate(book)


def filter_books(
    title: str | None,
    min_pages: int | None,
    max_pages: int | None,
    min_rating: float | None,
    max_rating: float | None,
    min_price: float | None,
    max_price: float | None,
    db: Session,
):
    books = db.query(BookORM)
    if title:
        books = books.filter(BookORM.title == title)
    if min_pages:
        books = books.filter(BookORM.pages >= min_pages)
    if max_pages:
        books = books.filter(BookORM.pages <= max_pages)
    if min_rating:
        books = books.filter(BookORM.rating >= min_rating)
    if max_rating:
        books = books.filter(BookORM.rating <= max_rating)
    if min_price:
        books = books.filter(BookORM.price >= min_price)
    if max_price:
        books = books.filter(BookORM.price <= max_price)
    books = [Book.model_validate(b) for b in books.all()]
    return books


def add_book_item(book: Book, db: Session):
    book_db = db.query(BookORM).filter(BookORM.id == book.id).first()
    if not book_db:
        book_db = BookORM(**book.model_dump())

        try:
            db.add(book_db)
            db.commit()
            db.refresh(book_db)
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Database error",
            )
        else:
            return Book.model_validate(book_db)
    else:
        raise HTTPException(
            status_code=409,
            detail=f"Book with ID {book.id} already exists",
        )


def update_book(book_id: int, book_update: BookUpdate, db: Session):
    book = db.query(BookORM).filter(BookORM.id == book_id).first()

    if not book:
        raise HTTPException(
            status_code=404,
            detail=f"Book with id {book_id} not found",
        )

    update_data = book_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(book, field, value)

    try:
        db.commit()
    except DataError:  # db field constraint violated
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Invalid numeric value/range",
        )

    return Book.model_validate(book)


def delete_book(book_id: int, db: Session):
    book = db.query(BookORM).filter(BookORM.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=404,
            detail=f"Book with id {book_id} not found",
        )
    try:
        db.delete(book)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error")
