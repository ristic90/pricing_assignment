import pytest

from app.domain.exceptions import BookDoesntExist, BookAlreadyExists


def test_get_all_books(sqlalchemy_repo):
    result = sqlalchemy_repo.get_all_books()

    assert len(result) == 3


def test_get_book_by_id(sqlalchemy_repo):
    book_id = 1
    result = sqlalchemy_repo.get_book_by_id(book_id)

    assert result.id == book_id


def test_get_book_by_id_nonexisting(sqlalchemy_repo):
    book_id = 100
    with pytest.raises(BookDoesntExist) as exc_info:
        sqlalchemy_repo.get_book_by_id(book_id)

    assert f"Book with ID={book_id} doesn't exist" == str(
        exc_info.value,
    )


def test_filter_books(sqlalchemy_repo):
    filters = {"min_pages": 300, "max_pages": 400, "max_rating": 4.8}
    result = sqlalchemy_repo.filter_books(**filters)

    assert len(result) == 1
    assert result[0].id == 1


def test_filter_books_no_result(sqlalchemy_repo):
    filters = {"min_price": 80}
    result = sqlalchemy_repo.filter_books(**filters)

    assert result == []


def test_add_book(sqlalchemy_repo, entity_book_add):
    result = sqlalchemy_repo.add_book(entity_book_add)

    assert result.title == entity_book_add.title


def test_add_book_already_exists(sqlalchemy_repo, entity_book_add):
    entity_book_add.id = 1
    with pytest.raises(BookAlreadyExists) as exc_info:
        sqlalchemy_repo.add_book(entity_book_add)

    assert f"Book with ID={entity_book_add.id} already exists" == str(exc_info.value)


def test_update_book(sqlalchemy_repo, entity_book_update_data):
    book_id = 1
    updated_book = sqlalchemy_repo.update_book(book_id, entity_book_update_data)

    assert updated_book.title == "The Updated Title"


def test_update_book_not_found(sqlalchemy_repo, entity_book_update_data):
    book_id = 10000
    with pytest.raises(BookDoesntExist) as exc_info:
        sqlalchemy_repo.update_book(book_id, entity_book_update_data)

    assert f"Book with ID={book_id} doesn't exist"
