from typing import List

from app.domain.entities.book import BookEntity
from app.domain.repositories.book_repository_protocol import BookRepositoryProtocol
from app.domain.services.book_service_protocol import BookServiceProtocol


class BookService(BookServiceProtocol):
    def __init__(self, book_repository: BookRepositoryProtocol):
        self.book_repository = book_repository

    def get_all_books(self) -> List[BookEntity] | None:
        return self.book_repository.get_all_books()

    def get_book_by_id(self, book_id: int) -> BookEntity:
        return self.book_repository.get_book_by_id(book_id)

    def filter_books(self, **filters) -> List[BookEntity] | None:
        return self.book_repository.filter_books(**filters)

    def add_book(self, book_add_data: dict) -> BookEntity:
        book = BookEntity(**book_add_data)
        return self.book_repository.add_book(book)

    def update_book(self, book_id: int, book_update_data: dict) -> BookEntity:
        return self.book_repository.update_book(book_id, book_update_data)

    def delete_book(self, book_id) -> None:
        self.book_repository.delete_book(book_id)
