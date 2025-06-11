from pydantic import BaseModel,HttpUrl
from typing import Optional,List

class ProductBase(BaseModel):
    name:str
    description:Optional[str]
    price:float
    stock:int
    category:str
    image_url:str

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass 

class ProductResponse(ProductBase):
    id:int
    class Config:
        from_attributes=True