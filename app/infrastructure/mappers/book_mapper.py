from app.domain.entities.book import BookEntity
from app.infrastructure.database.models.book_sqla import BookORM


class BookMapper:
    @staticmethod
    def to_entity(orm_obj: BookORM) -> BookEntity:
        return BookEntity(
            id=orm_obj.id,
            title=orm_obj.title,
            author=orm_obj.author,
            pages=orm_obj.pages,
            price=orm_obj.price,
            rating=orm_obj.rating,
        )

    @staticmethod
    def to_orm(entity: BookEntity) -> BookORM:
        return BookORM(
            id=entity.id,
            title=entity.title,
            author=entity.author,
            pages=entity.pages,
            price=entity.price,
            rating=entity.rating,
        )
