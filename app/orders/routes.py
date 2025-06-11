from fastapi import Depends,HTTPException,status,APIRouter
from sqlalchemy.orm import Session
from app.carts import models,schemas,routes
from app.orders import models,schemas,routes
from app.core.database import get_db
from app.auth.models import User
from app.carts import models
from app.products import models
from app.products.schemas import ProductResponse
from app.oauth2 import get_current_user
from app.orders import models,schemas
from typing import List
def check_user(user:User):
    if(user.role!="user"):
        raise HTTPException(status_code=403,detail=f"Users Only")

router=APIRouter(
    tags=["Orders"]
)

@router.get("/orders",response_model=List[schemas.OrderResponse])
def get_user_orders(
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    check_user(current_user)
    orders=db.query(models.Order).filter(models.Order.user_id==current_user.id).all()
    return orders

@router.get("/orders/{order_id}",response_model=schemas.OrderResponse)
def get_order_details(
    order_id:int,
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    check_user(current_user)
    order=db.query(models.Order).filter(
        models.Order.id==order_id,
        models.Order.user_id==current_user.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404,detail="Order not Found")
    return order