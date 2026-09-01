from sqlmodel import Field, SQLModel, Relationship
from typing import Optional



class Book(SQLModel, table=True):
    __tablename__ = "books"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str
    price: float
    is_sold: bool = Field(default=False)
    owner_id: int = Field(foreign_key="users.id")
    owner: Optional["User"] = Relationship(back_populates="books")


   
    # avoid circular import
    from models.user import User
    Book.model_rebuild()

    # request body for create book
    class BookCreate(SQLModel):
        title: str
        author: str
        price: float
        is_sold: bool = False
        owner_id: int

    # response body
    class BookResponse(SQLModel):
        id: int
        title: str
        author: str
        price: float
        is_sold: bool
        owner_id: int