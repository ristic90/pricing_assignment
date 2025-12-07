from app.domain.entities.book import BookEntity


def test_get_book_by_id(book_service_mock, mock_repo):
    book_id = 1
    expected_book = BookEntity(
        id=1, title="Book 1", author="Author 1", pages=50, rating=1.0, price=10.99
    )
    mock_repo.get_book_by_id.return_value = expected_book
    result = book_service_mock.get_book_by_id(book_id)

    mock_repo.get_book_by_id.assert_called_once_with(book_id)
    assert result == expected_book


def test_filter_books(book_service_mock, mock_repo):
    expected_books = [
        BookEntity(
            id=1, title="Book 1", author="Author 1", pages=50, rating=1.0, price=10.99
        ),
        BookEntity(
            id=2, title="Book 2", author="Author 2", pages=50, rating=1.0, price=10.99
        ),
    ]
    mock_repo.filter_books.return_value = expected_books

    filters = {"min_pages": 10, "max_price": 11}
    result = book_service_mock.filter_books(**filters)

    mock_repo.filter_books.assert_called_once_with(**filters)
    assert result == expected_books
