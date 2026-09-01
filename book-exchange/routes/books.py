from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select
from database import get_session
from models.book import Book, BookCreate, BookResponse, BookUpdate
from auth import verify_api_key
from typing import Optional, List

router = APIRouter(
    prefix="/books",
    tags=["books"],
    dependencies=[Depends(verify_api_key)]
)

# list all books
@router.get("/", response_model=List[BookResponse], summary="Get all books")
def get_books(
    title: Optional[str] = Query(default=None),
    author: Optional[str] = Query(default=None),
    price: Optional[float] = Query(default=None),
    is_sold: Optional[bool] = Query(default=None),
    session: Session = Depends(get_session)):
   query = select(Book).where(Book.is_sold == False)
   if title:
    query = query.where(Book.title.contains(title))
   if author:
    query = query.where(Book.author.contains(author))
   if price:
    query = query.where(Book.price <= price)

    books = session.exec(query).all()
    return books


# create a new book
@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED, summary="Create a new book")
def create_book(book: BookCreate, session: Session = Depends(get_session),api_key: str = Depends(verify_api_key)):
    # check if the api key is valid
    if api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    new_book = Book.model_validate(book)
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return new_book

#patch a book
@router.patch("/{book_id}", response_model=BookResponse, summary="Patch a book")
def patch_book(book_id: int, book: BookUpdate, session: Session = Depends(get_session),api_key: str = Depends(verify_api_key)):
    # check if the book exists
    book_to_update = session.get(Book, book_id)
    if not book_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    book_data = book.model_dump(exclude_unset=True)
    for key, value in book_data.items():
        setattr(book_to_update, key, value)
    session.add(book_to_update)    
    session.commit()
    session.refresh(book_to_update)
    return book_to_update


#delete a book
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a book")
def delete_book(book_id: int, session: Session = Depends(get_session),api_key: str = Depends(verify_api_key)):

    # check if the book exists
    book_to_delete = session.get(Book, book_id)
    if not book_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    # check if the api key is valid
    if api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key") 
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    session.delete(book)
    session.commit()
    return {"message": "Book deleted successfully"}