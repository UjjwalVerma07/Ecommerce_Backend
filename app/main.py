from fastapi import FastAPI
from app.core.database import Base,engine
from app.auth.routes import router as auth_router
from app.products.routes import router as product_admin_router
from app.products.public_routes import public_router 
from app.carts.routes import router as cart_router
from app.checkout.routes import router as checkout_router
from app.orders.routes import router as order_routes


app=FastAPI(title="E-Commerce Backend")
Base.metadata.create_all(bind=engine)
app.include_router(auth_router)
app.include_router(product_admin_router)
app.include_router(public_router)
app.include_router(cart_router)
app.include_router(checkout_router)
app.include_router(order_routes)