from fastapi import APIRouter, Depends, Query
from datetime import datetime,date
from sqlmodel import Session, select,func
from models import Order,OrderStatus
from database import get_session


router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("/daily-revenue")
async def daily_revenue(summary_date: date | None = Query(default=None), session: Session = Depends(get_session)):
    if summary_date:
        start = datetime.combine(summary_date, datetime.min.time())
        end = datetime.combine(summary_date, datetime.max.time())
        #query = select(func.sum(Order.total_amount)).where(Order.created_at >= start, Order.created_at <= end)
    else:
        start = datetime.combine(datetime.now().date(), datetime.min.time())
        end = datetime.combine(datetime.now().date(), datetime.max.time())
        #query = select(func.sum(Order.total_amount)).where(Order.created_at >= start, Order.created_at <= end)
    
    summary = {}
    total_amount = 0
    for status in OrderStatus:
        select(func.count(Order.id)).where(Order.status == status, Order.created_at >= start, Order.created_at <= end).one()
        summary[status.value] = count
        total_amount += count


    return {
        "summary_date": summary_date,
        "summary": summary,
        "total_amount": total_amount
    }