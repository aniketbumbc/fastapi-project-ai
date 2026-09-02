from fastapi import FastAPI
from database import create_tables
from routes import books, users

app = FastAPI(title="Book Exchange API", description="API for the Book Exchange project", version="1.0.0")

app.include_router(books.router)
app.include_router(users.router)


@app.on_event("startup")
def startup_event():
    create_tables()



@app.get("/")
def read_root():
    return {"message": "Hello, Welcome to the Book Exchange API!"}