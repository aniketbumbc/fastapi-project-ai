from sqlmodel import create_engine, Session, SQLModel
from models.user import User
from models.book import Book

User.model_rebuild()
Book.model_rebuild()

engine = create_engine("sqlite:///./book-exchange.db", echo=True)

def create_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
