from sqlalchemy import Column,Integer,String,Float
from app.core.database import Base
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__="products"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    description=Column(String)
    price=Column(Float,nullable=False)
    stock=Column(Integer,nullable=False)
    category=Column(String)
    image_url=Column(String)
    
    order_items=relationship("OrderItem",back_populates="product")