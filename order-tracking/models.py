from enum import Enum
from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship


class OrderStatus(str, Enum):
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    PICKED_UP = "picked_up"

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_name: str
    delivery_address: str
    item: str
    status: OrderStatus = Field(default=OrderStatus.PREPARING)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


# schema for creating a new order
class OrderCreate(BaseModel):
    customer_name: str
    delivery_address: str
    item: str

# schema for updating an order
class OrderUpdateStatus(BaseModel):
    status: Optional[OrderStatus] = None
    updated_at: datetime = Field(default_factory=datetime.now)
    delivery_address: Optional[str] = None



#status log for an order
class OrderStatusLog(SQLModel)
    order_id: int
    old_status:str
    new_status:str
    changed_at:datetime

