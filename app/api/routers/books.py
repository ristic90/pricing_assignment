import logging
import random
from typing import List

from fastapi import routing, Depends, status, HTTPException

from app.api.dependencies import get_book_service
from app.application.services.book_service import BookService
from app.domain.entities.book import BookEntity
from app.domain.exceptions import DatabaseError, BookAlreadyExists, BookDoesntExist
from app.api.models import BookAPI, BookUpdate, BookFilter

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

router = routing.APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
def check_health():
    return {"status": "ok"}


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[BookAPI],
)
def get_all_books(service: BookService = Depends(get_book_service)):
    books = service.get_all_books()
    books = [BookAPI.model_validate(book.to_dict()) for book in books]
    return books


@router.get(
    "/books/{book_id}",
    status_code=status.HTTP_200_OK,
    response_model=BookAPI,
)
async def get_book_by_id(
    book_id: int, service: BookService = Depends(get_book_service)
):
    try:
        book = service.get_book_by_id(book_id)
        book = BookAPI.model_validate(book.to_dict())
        logger.info(f"[GET] Book retrieved by id: {book}")
        return book
    except BookDoesntExist as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/books",
    status_code=status.HTTP_200_OK,
    response_model=List[BookAPI] | None,
)
def filter_books(
    filters: BookFilter = Depends(),
    service: BookService = Depends(get_book_service),
):
    filter_data = filters.model_dump(exclude_unset=True)
    filtered_books = service.filter_books(**filter_data)
    print("Filtered books: ", filtered_books)
    books = [BookAPI.model_validate(book.to_dict()) for book in filtered_books]
    logging.info(f"[GET] Filtered books: {books}")
    return books


@router.post(
    "/books",
    status_code=status.HTTP_201_CREATED,
    response_model=BookAPI,
)
def add_book(book: BookAPI, service: BookService = Depends(get_book_service)):
    if not book.id:
        book.id = random.randint(1000, 9999)
    try:
        book: BookEntity = service.add_book(book.model_dump())
    except BookAlreadyExists as e:
        raise HTTPException(status_code=409, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))

    book: BookAPI = BookAPI.model_validate(book.to_dict())
    logger.info(f"[POST] Book created {book}")
    return book


@router.put(
    "/books/{book_id}",
    status_code=status.HTTP_200_OK,
    response_model=BookAPI,
)
def update_book(
    book_id: int,
    book_update: BookUpdate,
    service: BookService = Depends(get_book_service),
):
    print("Book update: ", book_update)
    try:
        book: BookEntity = service.update_book(
            book_id,
            book_update.model_dump(exclude_unset=True),
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
    updated_book = BookAPI.model_validate(book.to_dict())
    logger.info(f"[PUT] Updated book: {updated_book}")
    return updated_book


@router.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_book(book_id: int, service: BookService = Depends(get_book_service)):
    try:
        service.delete_book(book_id)
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
