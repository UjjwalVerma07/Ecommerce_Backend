from pydantic import BaseModel
from typing import List
from app.products.schemas import ProductResponse

class CartItemBase(BaseModel):
    product_id:int
    quantity:int

class CartItemCreate(CartItemBase):
    pass 

class CartItemUpdate(BaseModel):
    quantity:int
    
class CartItemResponse(CartItemBase):
    product:ProductResponse
    quantity:int
    
    class Config:
        form_attributes=True

class CartResponse(BaseModel):
    items:List[CartItemResponse]
