from fastapi import FastAPI
#from app.indexing_pipeline import indexing_pipeline
from routes.query import router as query_router
app = FastAPI(title="RAG API", description="API for RAG", version="1.0.0")
app.include_router(query_router)
@app.get("/")
def read_root():
    return {"message": "Hello World"}

