from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DB_USER = "postgres"
DB_PASSWORD = "secret"
DB_HOST = "db"
# DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "mydb"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:" f"{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
