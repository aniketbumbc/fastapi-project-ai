from fastapi import FastAPI
from fastapi import Request
import uvicorn

app = FastAPI(
    title="Swiggy Order Service",
    description=("Internal API managing orders"),
    version="1.1",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

@app.get("/")
def read_root():
    """Read endpoint Health Check"""
    return {"message": "Welcome to swiggy order service","status":"healthy"}


@app.get("/about")
def about_root():
    """Return API metadata"""
    return {
        "services": "order-service",
        "team": "Backend",
        "region":"ap-south-1",
        "version":"1.1"
    }




@app.get("/debug/request-info", tags=["Debug"])
async def request_info(request:Request):
    """Inspect Raw Request"""
    return{
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
    }