from email.message import EmailMessage
import aiosmtplib
from app.core.config import settings

async def send_email(to_email:str,subject:str,body:str):
    message=EmailMessage()
    message["From"]=settings.MAIL_FROM
    message["To"]=to_email
    message.set_content(body)
    
    await aiosmtplib.send(
        message,
        hostname=settings.MAIL_HOST,
        port=int(settings.MAIL_PORT)
    )