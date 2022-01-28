from pathlib import Path
from fastapi import Request
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from passlib.context import CryptContext

from app.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


__conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME=settings.mail_from_name,
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates/email'
)

def hash(password: str):
    return pwd_context.hash(password)


def verify(plain: str, hash: str):
    return pwd_context.verify(plain, hash)


async def send_email(recipient: str, subject: str, payload: str, template: str):
    message = MessageSchema(
        subject=subject,
        recipients=[recipient],
        template_body=payload
    )
    
    fm = FastMail(config=__conf)
    await fm.send_message(message=message, template_name=template)
