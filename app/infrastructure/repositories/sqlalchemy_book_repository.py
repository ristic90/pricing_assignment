from typing import List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, DataError

from app.infrastructure.mappers.book_mapper import BookMapper
from app.domain.exceptions import BookAlreadyExists, DatabaseError, BookDoesntExist
from app.infrastructure.database.models.book_sqla import BookORM
from app.domain.entities.book import BookEntity
from app.domain.repositories.book_repository_protocol import BookRepositoryProtocol


class SQLAlchemyBookRepository(BookRepositoryProtocol):
    def __init__(self, session):
        self.session = session

    def get_all_books(self) -> List[BookEntity] | None:
        stmt = select(BookORM)
        result = self.session.execute(stmt)
        books_db: List[BookORM] | None = result.scalars().all()
        books: List[BookEntity] | None = [
            BookMapper.to_entity(book) for book in books_db
        ]
        return books

    def get_book_by_id(self, book_id: int) -> BookEntity:
        book_db = self.session.get(BookORM, book_id)
        if book_db:
            book = BookMapper.to_entity(book_db)
            return book
        else:
            raise BookDoesntExist(book_id)

    def filter_books(self, **filters) -> List[BookEntity] | None:
        stmt = select(BookORM)
        if filters.get("title") is not None:
            stmt = stmt.where(BookORM.title.ilike(f"%{filters['title']}%"))
        if filters.get("min_pages") is not None:
            stmt = stmt.where(BookORM.pages >= filters["min_pages"])
        if filters.get("max_pages") is not None:
            stmt = stmt.where(BookORM.pages <= filters["max_pages"])
        if filters.get("min_rating") is not None:
            stmt = stmt.where(BookORM.rating >= filters["min_rating"])
        if filters.get("max_rating") is not None:
            stmt = stmt.where(BookORM.rating <= filters["max_rating"])
        if filters.get("min_price") is not None:
            stmt = stmt.where(BookORM.price >= filters["min_price"])
        if filters.get("max_price") is not None:
            stmt = stmt.where(BookORM.price <= filters["max_price"])
        books_db: List[BookORM] | None = self.session.scalars(stmt).all()
        books: List[BookEntity] | None = [
            BookMapper.to_entity(book) for book in books_db
        ]
        return books

    def add_book(self, book: BookEntity):
        book_db = BookMapper.to_orm(book)
        try:
            self.session.add(book_db)
            self.session.commit()
            self.session.refresh(book_db)
        except IntegrityError:
            self.session.rollback()
            raise BookAlreadyExists(book.id)
        except SQLAlchemyError:
            self.session.rollback()
            raise DatabaseError
        return BookMapper.to_entity(book_db)

    def update_book(self, book_id: int, book_update_data: dict):
        book_db = self.session.get(BookORM, book_id)

        if not book_db:
            raise BookDoesntExist(book_id)

        for field, value in book_update_data.items():
            if hasattr(book_db, field):
                setattr(book_db, field, value)
        try:
            self.session.commit()
            self.session.refresh(book_db)
        except DataError:  # db field constraint violated
            self.session.rollback()
            raise DatabaseError

        return BookMapper.to_entity(book_db)

    def delete_book(self, book_id: int):
        book_db = self.session.get(BookORM, book_id)
        if not book_db:
            raise BookDoesntExist(book_id)

        try:
            self.session.delete(book_db)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseError
