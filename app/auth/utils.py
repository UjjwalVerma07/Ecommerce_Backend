import secrets
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime,timedelta
from app.core.config import settings

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(plain_password:str,hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_reset_token():
    return secrets.token_urlsafe(32)

def generate_reset_token(expire_minutes=30):
    return secrets.token_urlsafe(32), datetime.utcnow() + timedelta(minutes=expire_minutes)