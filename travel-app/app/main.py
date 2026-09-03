from fastapi import FastAPI
from app.routes.planner import router as planner_router
app = FastAPI(title='Travel App', description='Aggreate travel data from multiple sources to provide a comprehensive view of travel destinations')

@app.get('/')
async def root():
    return {"app": "Travel App",
    "version": "1.0.0",
    "enpoints":{
        "POST /api/v1/plan": "Create a new travel plan (Aggregated)",
        "GET /api/v1/plan/stream": "Stream a travel plan by Sever send events to client",
        "GET /api/v1/plan/cache-stash": "Cache stash for travel plan",
        "DELETE /api/v1/plan/cache-stash": "Delete cache stash for travel plan",
    }}


app.include_router(planner_router)