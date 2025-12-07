from typing import Annotated, Optional

from pydantic import BaseModel, Field


class BookAPI(BaseModel):
    id: Annotated[Optional[int], Field(gt=0)] = None
    title: Annotated[str, Field(min_length=1)]
    author: Annotated[str, Field(min_length=1)]
    pages: Annotated[int, Field(ge=0)]
    rating: Annotated[float, Field(ge=0, le=5)]
    price: Annotated[float, Field(ge=0, le=9999.99)]

    model_config = {"from_attributes": True}

    def __repr__(self):
        return (
            f"<Book(id={self.id}, title={self.title}, "
            f"author={self.author}, pages={self.pages}, "
            f"rating={self.rating}, price={self.price})>"
        )

    def __str__(self):
        return (
            f"<Book(id={self.id}, title={self.title}, "
            f"author={self.author}, pages={self.pages}, "
            f"rating={self.rating}, price={self.price})>"
        )


class BookFilter(BaseModel):
    title: Optional[str] = None
    min_pages: Optional[int] = Field(None, ge=0)
    max_pages: Optional[int] = Field(None, ge=0)
    min_rating: Optional[float] = Field(None, ge=0, le=5)
    max_rating: Optional[float] = Field(None, ge=0, le=5)
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)


class BookUpdate(BaseModel):
    title: Annotated[Optional[str], Field(min_length=1)] = None
    author: Annotated[Optional[str], Field(min_length=1)] = None
    pages: Annotated[Optional[int], Field(ge=0)] = None
    rating: Annotated[Optional[float], Field(ge=0, le=5)] = None
    price: Annotated[Optional[float], Field(ge=0, le=9999.99)] = None
