from fastapi import HTTPException,status,APIRouter,Depends
from sqlalchemy.orm import Session
from app.auth import models,schemas,utils
from app.core.database import get_db
from app.utils.email import send_email
from app.utils.logging import logger
from datetime import datetime, timedelta

router=APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

reset_tokens={}

@router.post("/signup",status_code=status.HTTP_201_CREATED)
def signup(user:schemas.UserCreate,db: Session = Depends(get_db)):
    existing_user=db.query(models.User).filter(models.User.email==user.email).first()
    if existing_user:
        logger.warning(f"Signup Failed - email exists:{user.email}")
        raise HTTPException(status_code=400,detail=f"Email Already Registerd")
    hashed_password=utils.hash_password(user.password)
    new_user=models.User(name=user.name,email=user.email,hashed_password=hashed_password,role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"User Registerd:{user.email}")
    return {"message":"Signup Successfull!!"}

@router.post("/signin",response_model=schemas.Token)
def signin(login:schemas.UserLogin,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==login.email).first()
    if not user or not utils.verify_password(login.password,user.hashed_password):
        logger.warning(f"Login Failed:{login.email}")
        raise HTTPException(status_code=401,detail=f"Invalid Credentials")
    
    access_token=utils.create_access_token(data={"sub":user.email,"role":user.role})
    refresh_token=utils.create_access_token(
        data={"sub":user.email,"type":"refresh"},
        expires_delta=timedelta(days=7)
    )
    logger.info(f"User logged in :{user.email}")
    return {"access_token":access_token,"refresh_token":refresh_token}

@router.post("/forgot-password")
async def forgot_password(payload:schemas.ForgotPasswordRequest,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==payload.email).first()
    if not user:
        logger.warning(f"Forgot Password for non-existent email:{payload.email}")
        raise HTTPException(status_code=404,detail="User not Found")

    db.query(models.PasswordResetToken).filter(models.PasswordResetToken.user_id==user.id,
            models.PasswordResetToken.is_used==False).update({models.PasswordResetToken.is_used:True})
    
    token,expiry=utils.generate_reset_token()
    db_token=models.PasswordResetToken(
        user_id=user.id,
        token=token,
        is_used=False,
        expires_at=expiry
    )
    db.add(db_token)
    db.commit()
    reset_link = f"http://localhost:8025/reset-password?token={token}"
    await send_email(
        to_email=user.email,
        subject="Password Reset Link",
        body=f"Click to reset your password: {reset_link}"
    )
    logger.info(f"Password reset email sent to: {user.email}")
    return {"message": "Password reset email sent"}
    
    
@router.post("/reset-password")
def reset_password(payload:schemas.ResetPasswordRequest,db:Session=Depends(get_db)):
    db_token=db.query(models.PasswordResetToken).filter(
        models.PasswordResetToken.token==payload.token,
        models.PasswordResetToken.is_used==False
    ).first()
    if not db_token or db_token.expires_at<datetime.utcnow():
        logger.error("Invalid or expired reset token")
        raise HTTPException(status_code=400,detail="Invalid or expired Reset Token")
    
    user=db.query(models.User).filter(models.User.id==db_token.user_id).first()
    if not user:
        raise HTTPException(status_code=404,detail=f"User Not Found")
    user.hashed_password=utils.hash_password(payload.new_password)
    db_token.is_used=True
    db.commit()
    logger.info(f"Password successfully reset for : {user.id}")
    return {"message":"Password has been sent successfully!!"}
    