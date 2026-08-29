 from fastapi import APIRouter, Depends, HTTPException, Query
 from sqlmodel import Session
 from database import get_session
 from models import Order, OrderCreate, OrderUpdate

 router = APIRouter(prefix="/orders", tags=["orders"])

 @router.post("/", response_model=Order)
 async def create_order(order: OrderCreate, session: Session = Depends(get_session)):
    new_order = Order(**order.model_dump())
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    return new_order

 @router.get("/", response_model=List[Order])
 async def list_orders(
    status: Optional[OrderStatus] = Query(default=None, description="Filter by order status"),
    created_date: Optional[datetime] = Query(default=None, description="Filter by creation date YYYY-MM-DD"),
    skip: int = Query(default=0, ge=0, description="Number of items to skip"),
    limit: int = Query(default=10, ge=1, le=100, description="Number of items to return"),
    session: Session = Depends(get_session)):
    query = select(Order)
    if status:
        query = query.where(Order.status == status)
    if created_date:
      start= datetime.combine(created_date, datetime.min.time())
      end = datetime.combine(created_date, datetime.max.time())
      query = query.where(Order.created_at >= start, Order.created_at <= end)
    
    query = query.offset(skip).limit(limit)
    orders = session.exec(query).all()
    return orders