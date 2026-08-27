from fastapi import FastAPI,Query,HTTPException
from models import MenuItem, MenuResponse
from data import menu_items

app=FastAPI(title="Hotel menu API", description="Read only api for kiosk and app")


@app.get("/")
def root():
    return{"message":"Welcome hotel menu api"}


@app.get("/menu",response_model=MenuResponse)
def get_menu(category:str | None = Query(None, description="Filter by category")):
    if category:
        filter_data = [item for item in menu_items if item["category"] == category.lower()]
        if not filter_data:
            raise HTTPException(status_code=404, detail="No item found in category")
        return MenuResponse(count=len(filter_data),items=filter_data,status="Success")

    return MenuResponse(count=len(menu_items),items=menu_items, status="Success")


@app.get("/menu/{id}",response_model=MenuItem)
def get_item(id:int):
    for item in menu_items:
        if item["id"] == id:
            return item

    raise HTTPException(status_code=404, detail="No item found in the list")

