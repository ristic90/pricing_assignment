import pytest

from app import database_operations
from app.exceptions import BookAlreadyExists


def test_get_all_books(db_session):
    books = database_operations.get_all_books(db_session)
    assert len(books) == 3


def test_get_book_by_id(db_session):
    book = database_operations.get_book_by_id(1, db_session)
    assert book.id == 1
    assert book.title == "1984"


def test_filter_books_by_title(db_session):
    books = database_operations.filter_books(
        db_session,
        title="The Hobbit",
    )
    assert len(books) == 1
    assert books[0].author == "Tolkien"


def test_filter_book_by_price_range(db_session):
    books = database_operations.filter_books(
        db_session,
        min_price=11,
        max_price=20,
    )
    assert len(books) == 2


def test_add_book_item(db_session, item_to_add):
    database_operations.add_book_item(item_to_add, db_session)
    books = database_operations.get_all_books(db_session)
    assert len(books) == 4


def test_add_book_item_twice(db_session, item_to_add):
    database_operations.add_book_item(item_to_add, db_session)
    with pytest.raises(BookAlreadyExists) as exc_info:
        database_operations.add_book_item(item_to_add, db_session)

    assert f"Book with ID {item_to_add.id} already exists" in str(
        exc_info.value,
    )


def test_update_book(db_session, item_to_update):
    updated_book = database_operations.update_book(
        1,
        item_to_update,
        db_session,
    )
    assert updated_book.id == 1
    assert updated_book.author == item_to_update.author
    assert updated_book.pages == item_to_update.pages


def test_delete_book(db_session):
    database_operations.delete_book(1, db_session)
    books = database_operations.get_all_books(db_session)
    assert len(books) == 2
