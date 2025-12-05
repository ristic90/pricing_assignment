def test_get_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_all_books(client):
    response = client.get("/books")
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_book_by_id(client):
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json()["author"] == "George Orwell"


def test_add_book(client, item_to_add):
    response = client.post(
        "/books",
        json=item_to_add.model_dump(),
    )
    assert response.status_code == 201
    assert response.json()["author"] == "Adder Addition"

    # get all books
    response = client.get("/books")
    assert len(response.json()) == 4


def test_delete_book(client):
    response = client.delete("/books/1")
    assert response.status_code == 204
    # get all books
    response = client.get("/books")
    assert len(response.json()) == 2
