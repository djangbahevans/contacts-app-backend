from pathlib import Path
from typing import List

from jinja2 import Template
from passlib.context import CryptContext
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

TEMPLATE_FOLDER = Path(__file__).parent / 'templates/email'


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain: str, hash: str):
    return pwd_context.verify(plain, hash)


async def send_email(recipients: List[str], subject: str, payload: str, template: str):
    t = Template(
        open(TEMPLATE_FOLDER / template, encoding="utf-8").read())

    message = Mail(
        from_email=settings.mail_from,
        to_emails=recipients,
        subject=subject,
        html_content=t.render(**payload)
    )
    try:
        sg = SendGridAPIClient(settings.sendgrid_api_key)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)
