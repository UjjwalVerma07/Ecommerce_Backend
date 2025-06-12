from fastapi import Depends,HTTPException,status,APIRouter
from sqlalchemy.orm import Session
from app.orders.models import OrderStatus
from app.core.database import get_db
from app.auth.models import User
from app.carts.models import CartItem
from app.orders import schemas,models
from app.products.models import Product
from app.oauth2 import get_current_user
router=APIRouter(
    tags=["Checkout"]
)

def check_user(user:User):
    if(user.role!="user"):
        raise HTTPException(status_code=403,detail=f"Users Only")
    
@router.post("/checkout",response_model=schemas.OrderResponse)
def checkout(
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user) 
):
    check_user(current_user)
    cart_items=db.query(CartItem).filter(CartItem.user_id==current_user.id).all()
    if not cart_items:
        raise HTTPException(status_code=400,detail=f"Cart is Empty")
    
    total_amount=0
    for item in cart_items:
        total_amount=total_amount+(item.product.price*item.quantity)
    
    order=models.Order(
        user_id=current_user.id,
        total_amount=total_amount,
        status=OrderStatus.paid
    )
    
    db.add(order)
    db.flush()
    
    for item in cart_items:
        product=db.query(Product).filter(Product.id==item.product_id).first()
        if not product or product.stock<item.quantity:
            raise HTTPException(status_code=400,detail=f"Insufficient stock for product Id {item.product_id}")
        product.stock=product.stock-item.quantity
    
    for item in cart_items:
        db_item = models.OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price_at_purchase=item.product.price
        )
        db.add(db_item)
        
    for item in cart_items:
        db.delete(item)
    
    db.commit()
    db.refresh(order)
    return order