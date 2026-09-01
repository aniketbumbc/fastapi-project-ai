from sqlmodel import create_engine, Session
from models.user import User
from models.book import Book

engine = create_engine("sqlite:///./book-exchange.db",echo=True)

def create_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session