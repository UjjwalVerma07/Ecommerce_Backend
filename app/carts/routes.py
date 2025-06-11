from typing import List
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.carts import models,schemas
from app.products.models import Product
from app.core.database import get_db
from app.oauth2 import get_current_user
from app.auth.models import User

router=APIRouter(prefix="/cart",tags=["Cart"])

def check_user(user:User):
    if(user.role!="user"):
        raise HTTPException(status_code=403,detail=f"User Only")
    
#For Posting in Cart
@router.post("",response_model=schemas.CartItemResponse)
def add_to_cart(item:schemas.CartItemCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    check_user(current_user)
    product=db.query(Product.id==item.product_id).first()
    product_obj = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Product Not Found")
    cart_item=db.query(models.CartItem).filter_by(user_id=current_user.id,product_id=item.product_id).first()
    if cart_item:
        tocheck=cart_item.quantity+item.quantity
        if tocheck<=product_obj.stock:
            cart_item.quantity=cart_item.quantity+item.quantity
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"The Requested Quantity Cant Be Fullfilled Now")
    else:
        cart_item=models.CartItem(user_id=current_user.id,product_id=item.product_id,quantity=item.quantity)
        to_check=cart_item.quantity
        if to_check>product_obj.stock:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"The Requested Quantity Cant Be Fullfilled Now")
    db.add(cart_item)
    
    db.commit()
    db.refresh(cart_item)
    return cart_item
    

#For Getting in Cart
@router.get("/",response_model=schemas.CartResponse)
def view_cart(db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    check_user(current_user)
    items=db.query(models.CartItem).filter(models.CartItem.user_id==current_user.id).all()
    return {"items": items}

#For Deleting in Cart
@router.delete("/{product_id}",status_code=204)
def remove_from_cart(product_id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    check_user(current_user)
    cart_item=db.query(models.CartItem).filter(models.CartItem.product_id==product_id,models.CartItem.user_id==current_user.id).first()
    if not cart_item:
        raise HTTPException(status_code=404,detail=f"Item Not Found in Cart")
    
    db.delete(cart_item)
    db.commit()
    return {"message":"Item From Cart Deleted Successfully!!"}
 
#For Updating in Cart
#Need To check Tommorrow   
@router.put("/{product_id}",response_model=schemas.CartResponse)
def update_quantity(product_id:int,data:schemas.CartItemUpdate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    check_user(current_user)
    cart_item=db.query(models.CartItem).filter(models.CartItem.user_id==current_user.id,models.CartItem.product_id==product_id).first()
    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Item Not Found in Cart")
    cart_item.quantity=data.quantity
    db.commit()
    db.refresh(cart_item)
    return {"items": [cart_item]} 
    