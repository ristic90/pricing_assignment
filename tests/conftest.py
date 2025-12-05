import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.db_models import Book as BookORM
from app.main import app
from app.pydantic_models import Book, BookUpdate

# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


@pytest.fixture()
def setup_db():
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Preload test data
    session = TestingSessionLocal()
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
    session.add_all(books)
    session.commit()
    session.close()

    yield

    # Drop tables
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session(setup_db):
    """Provide a session for each test."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture()
def item_to_add():
    return Book(
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
