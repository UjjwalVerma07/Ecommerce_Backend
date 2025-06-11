from fastapi import APIRouter,Depends,status,Query,HTTPException
from sqlalchemy.orm import Session
from app.products import models,schemas
from app.core.database import get_db
from app.auth.models import User
from typing import List
from sqlalchemy import and_,or_

public_router=APIRouter(
    prefix="/products",
    tags=["Public Products"]
)
  
#Working
@public_router.get("/",response_model=List[schemas.ProductResponse])
def list_products(
    db:Session=Depends(get_db),
    category:str=Query(None),
    min_price:float=Query(None,ge=0),
    max_price:float=Query(None,ge=0),
    sort_by:str=Query("price",regex="^(price|name)$"),
    page:int=Query(1,ge=1),
    page_size:int=Query(10,ge=1)
    
):
    query=db.query(models.Product)
    if category:
        query=query.filter(models.Product.category.ilike(f"%{category}%"))
    if min_price is not None:
        query=query.filter(models.Product.price>=min_price)
    if max_price is not None:
        query=query.filter(models.Product.price<=max_price)
    
    #Sorting
    if sort_by=="price":
        query=query.order_by(models.Product.price.asc())
    elif sort_by=="name":
        query=query.order_by(models.Product.name.asc())
        
    #Pagination
    
    products=query.offset((page-1)*page_size).limit(page_size).all()
    return products

#Working
@public_router.get("/search",response_model=List[schemas.ProductResponse])
def search_products(db:Session=Depends(get_db),keyword:str=Query(...,min_length=1)):
    results=db.query(models.Product).filter(
        or_(
            models.Product.name.ilike(f"%{keyword}%"),
            models.Product.description.ilike(f"%{keyword}%"),
            models.Product.category.ilike(f"%{keyword}%")
        )
    ).all()
    return results

#Working
@public_router.get("/{id}",response_model=schemas.ProductResponse)
def get_product_detail(id:int,db:Session=Depends(get_db)):
    product=db.query(models.Product).filter(models.Product.id==id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Product Not Found")
    return product


          
    
    
    
    
    
