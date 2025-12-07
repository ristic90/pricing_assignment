from fastapi import Depends
from app.domain.repositories.book_repository_protocol import BookRepositoryProtocol
from app.application.services.book_service import BookService
from app.infrastructure.repositories.sqlalchemy_book_repository import (
    SQLAlchemyBookRepository,
)
from app.infrastructure.database.session import get_db


def get_book_repository(db=Depends(get_db)) -> BookRepositoryProtocol:
    return SQLAlchemyBookRepository(db)


def get_book_service(
    repo: BookRepositoryProtocol = Depends(get_book_repository),
) -> BookService:
    return BookService(repo)
