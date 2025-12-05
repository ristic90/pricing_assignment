import logging
import random
from typing import List

from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session

import app.database_operations as db_operations
from app.database import get_db
from app.exceptions import DatabaseError, BookAlreadyExists, \
    BookDoesntExist
from app.pydantic_models import Book, BookUpdate

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/health", status_code=status.HTTP_200_OK)
def check_health():
    return {"status": "ok"}


@app.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[Book],
)
def get_all_books(db: Session = Depends(get_db)):
    books_db = db_operations.get_all_books(db)
    books = [Book.model_validate(book) for book in books_db]
    return books


@app.get(
    "/books/{book_id}",
    status_code=status.HTTP_200_OK,
    response_model=Book,
)
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    book = db_operations.get_book_by_id(book_id, db)
    book = Book.model_validate(book)
    logger.info(f"[GET] Book retrieved by id: {book}")
    return book


@app.get(
    "/books",
    status_code=status.HTTP_200_OK,
    response_model=List[Book] | None,
)
def filter_books(
        title: str | None = None,
        min_pages: int | None = None,
        max_pages: int | None = None,
        min_rating: float | None = None,
        max_rating: float | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        db: Session = Depends(get_db),
):
    filtered_books = db_operations.filter_books(
        db,
        title,
        min_pages,
        max_pages,
        min_rating,
        max_rating,
        min_price,
        max_price,
    )
    books = [Book.model_validate(book) for book in filtered_books]
    logging.info(f"[GET] Filtered books: {books}")
    return books


@app.post(
    "/books",
    status_code=status.HTTP_201_CREATED,
    response_model=Book,
)
def add_book(book: Book, db: Session = Depends(get_db)):
    if not book.id:
        book.id = random.randint(1000, 9999)
    try:
        book_db = db_operations.add_book_item(book, db)
    except BookAlreadyExists as e:
        raise HTTPException(status_code=409, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    else:
        book = Book.model_validate(book_db)
        logger.info(f"[POST] Book created {book}")
        return book


@app.put(
    "/books/{book_id}",
    status_code=status.HTTP_200_OK,
    response_model=Book,
)
def update_book(book_id: int, book_update: BookUpdate,
                db: Session = Depends(get_db)):
    try:
        updated_book_db = db_operations.update_book(
            book_id,
            book_update,
            db,
        )
    except BookDoesntExist as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
    except DatabaseError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
    updated_book = Book.model_validate(updated_book_db)
    logger.info(f"[PUT] Updated book: {updated_book}")
    return updated_book


@app.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    try:
        db_operations.delete_book(book_id, db)
    except BookDoesntExist as e:
        raise HTTPException(
            status_code=404,
            detail=f"Book with id {book_id} not found",
        )
    except DatabaseError as e:
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
    logger.info(f"[DELETE] Deleted book with id {book_id}")
