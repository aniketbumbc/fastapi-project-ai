from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_tables
from routes.reviews import router as reviews_router


@asynccontextmanager
async def lifespan(app:FastAPI):
    create_tables()
    print("Database tables created")
    yield
    # shutdown: cleanup activity
    print("Shutting down application")



app = FastAPI(title="Movie Review API", description="Reviews movies rating", lifespan=lifespan)

app.include_router(reviews_router)


@app.get("/")
def root():
    return {"Message": "Welcome to movie rating app."}