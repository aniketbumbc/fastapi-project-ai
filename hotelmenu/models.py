from pydantic import BaseModel

class MenuItem(BaseModel):
    id:int
    name:str
    category:str
    description:str
    price:float
    is_available:bool



class MenuResponse(BaseModel):
    status:str
    count:int
    items: list[MenuItem]