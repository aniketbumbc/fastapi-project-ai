from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from models.book import Book

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    email: str = Field(unique=True)
    college:str

    books: list["Book"] = Relationship(back_populates="owner")


    # request body  for create user
    class UserCreate(SQLModel):
        username: str
        email: str
        college: str

    # response body
    class UserResponse(SQLModel):
        id: int
        username: str
        email: str
        college: str


    # avoid circular import

    User.model_rebuild()