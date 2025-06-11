from pydantic import BaseModel
from typing import List
from datetime import datetime
from enum import Enum

class OrderItemBase(BaseModel):
    product_id:int
    quantity:int
    price_at_purchase:float

class OrderItemResponse(OrderItemBase):
    id:int
    class Config:
        from_attributes=True

class OrderStatus(str,Enum):
    pending="pending"
    paid="paid"
    cancelled="cancelled"

class OrderResponse(BaseModel):
    id:int
    total_amount:float
    status:OrderStatus
    created_at:datetime
    items:List[OrderItemResponse]
    class Config:
        from_attributes=True