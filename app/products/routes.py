from fastapi import APIRouter,Depends,HTTPException,status,Query
from sqlalchemy.orm import Session
from app.products import models,schemas
from app.core.database import get_db
from app.auth.models import User
from app.oauth2 import get_current_user
from typing import List

router=APIRouter(
    prefix="/admin/products",
    tags=["Admin-Product Managment"]
)

def check_admin(user:User):
    if(user.role!="admin"):
        raise HTTPException(status_code=403,detail=f"Admin Only")


@router.post("/",response_model=schemas.ProductResponse)
def create_product(product:schemas.ProductCreate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    check_admin(current_user)
    new_product=models.Product(name=product.name,description=product.description,
                               price=product.price,stock=product.stock,
                               category=product.category,image_url=product.image_url)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.get("/",response_model=List[schemas.ProductResponse])
def get_products(skip:int=Query(0,ge=0),limit:int=Query(10,ge=1),
    db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    check_admin(current_user)
    products_list=db.query(models.Product).offset(skip).limit(limit).all()
    return products_list

@router.get("/{id}",response_model=schemas.ProductResponse)
def get_product_by_id(id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    check_admin(current_user)
    product=db.query(models.Product).filter(models.Product.id==id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Product not Found")
    return product


@router.put("/{id}",response_model=schemas.ProductResponse)
def update_product(id:int,updated_product:schemas.ProductUpdate,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    check_admin(current_user)
    product=db.query(models.Product).filter(models.Product.id==id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Product not found")
    product.name=updated_product.name
    product.description=updated_product.description
    product.price=updated_product.price
    product.stock=updated_product.stock
    product.category=updated_product.category
    product.image_url=updated_product.image_url
    
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id:int,db:Session=Depends(get_db),current_user:User=Depends(get_current_user)):
    check_admin(current_user)
    product=db.query(models.Product).filter(models.Product.id==id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f"Product Not Found")
    db.delete(product)
    db.commit
    return {"Message":"Product Deleted Successfullyy"}



