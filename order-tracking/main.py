from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import get_session, create_tables
from routes.orders import router as orders_router
from routes.stats import router as stats_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("Database tables created")
    yield
    print("Application shutdown")

app = FastAPI(title="Order Management System", description="API for managing orders and statistics", version="1.0.0", lifespan=lifespan)
app.include_router(orders_router)
app.include_router(stats_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Order Management System"}