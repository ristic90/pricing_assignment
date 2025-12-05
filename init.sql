CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    pages INTEGER CHECK (pages > 0),
    rating NUMERIC(2,1) CHECK (rating BETWEEN 0 AND 5),
    price NUMERIC(6,2) CHECK (price >= 0)
);

INSERT INTO books (title, author, pages, rating, price) VALUES
('To Kill a Mockingbird', 'Harper Lee', 324, 4.8, 14.99),
('1984', 'George Orwell', 328, 4.7, 12.95),
('Animal Farm', 'George Orwell', 112, 4.6, 8.99),
('Pride and Prejudice', 'Jane Austen', 279, 4.6, 9.99),
('The Great Gatsby', 'F. Scott Fitzgerald', 180, 4.4, 10.99);