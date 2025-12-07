from typing import cast
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.dependencies import get_book_service
from app.application.services.book_service import BookService
from app.infrastructure.database.base import Base
from app.infrastructure.database.models.book_sqla import BookORM
from app.infrastructure.database.session import get_db
from app.api.models import BookAPI, BookUpdate
from app.domain.entities.book import BookEntity
from app.domain.repositories.book_repository_protocol import BookRepositoryProtocol
from app.infrastructure.repositories.sqlalchemy_book_repository import (
    SQLAlchemyBookRepository,
)
from app.main import app

# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture
def mock_repo() -> BookRepositoryProtocol:
    return cast(
        BookRepositoryProtocol, Mock()
    )  # fix type checking in book_service fixture


@pytest.fixture
def book_service_mock(mock_repo):
    return BookService(mock_repo)


@pytest.fixture
def in_memory_db():
    engine = create_engine(
        "sqlite:///./test.db",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(
        bind=engine,
    )

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        Base.metadata.drop_all(bind=engine)
        db.close()


@pytest.fixture()
def filled_db(in_memory_db):
    # Preload test data
    books = [
        BookORM(
            id=1,
            title="1984",
            author="George Orwell",
            pages=328,
            rating=4.7,
            price=12.95,
        ),
        BookORM(
            id=2,
            title="Dune",
            author="Frank Herbert",
            pages=412,
            rating=4.8,
            price=14.99,
        ),
        BookORM(
            id=3,
            title="The Hobbit",
            author="Tolkien",
            pages=300,
            rating=4.9,
            price=10.99,
        ),
    ]
    in_memory_db.add_all(books)
    in_memory_db.commit()
    in_memory_db.close()

    return in_memory_db


@pytest.fixture()
def sqlalchemy_repo(filled_db):
    return SQLAlchemyBookRepository(filled_db)


@pytest.fixture
def book_service(sqlalchemy_repo):
    return BookService(sqlalchemy_repo)


@pytest.fixture()
def client(filled_db, sqlalchemy_repo, book_service):
    def override_get_db():
        yield filled_db

    def override_get_book_repository():
        return sqlalchemy_repo

    def override_get_book_service():
        return book_service

    app.dependency_overrides[get_db] = override_get_db()
    app.dependency_overrides[get_book_service] = override_get_book_service
    app.dependency_overrides[get_db] = override_get_book_repository
    return TestClient(app)


@pytest.fixture()
def entity_book_add():
    return BookEntity(
        id=4,
        title="The Added Book",
        author="Adder Addition",
        pages=50,
        rating=2.2,
        price=5.99,
    )


@pytest.fixture()
def entity_book_update_data():
    return {"title": "The Updated Title", "price": 12.49, "rating": 2.2}


@pytest.fixture()
def item_to_add():
    return BookAPI(
        id=4,
        title="The Added Book",
        author="Adder Addition",
        pages=50,
        rating=2.2,
        price=5.99,
    )


@pytest.fixture()
def item_to_update():
    return BookUpdate(
        author="Update Author",
        pages=10,
    )
