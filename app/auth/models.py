from sqlalchemy import Column,String,Integer,Enum,Boolean,ForeignKey,DateTime
from app.core.database import Base
from sqlalchemy.orm import relationship
import enum

class UserRole(str,enum.Enum):
    admin="admin"
    user="user"

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    hashed_password=Column(String,nullable=False)
    role=Column(Enum(UserRole),default=UserRole.user)
    #cart_items = relationship("CartItem", back_populates="user")
    cart_items = relationship("CartItem", back_populates="user")
    # orders=relationship("Order",back_populates="user")

    
class PasswordResetToken(Base):
    __tablename__="password_reset_tokens"
    
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    token=Column(String,unique=True,nullable=False,index=True)
    is_used=Column(Boolean,default=False)
    expires_at=Column(DateTime)
    
    user=relationship("User")
    
    
from app.orders.models import Order  # import last

User.orders = relationship("Order", back_populates="user")