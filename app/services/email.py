from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from fastapi.templating import Jinja2Templates
from app.core.config import settings
from pathlib import Path

MAIL_USERNAME = settings.MAIL_USERNAME
MAIL_PASSWORD = settings.MAIL_PASSWORD
MAIL_FROM = settings.MAIL_FROM
MAIL_PORT = settings.MAIL_PORT
MAIL_SERVER = settings.MAIL_SERVER
MAIL_STARTTLS=settings.MAIL_STARTTLS
MAIL_SSL_TLS = settings.MAIL_SSL_TLS
USE_CREDENTIALS=settings.USE_CREDENTIALS

DOMAIN_URL = settings.DOMAIN_URL

fastmail = FastMail(ConnectionConfig(
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_FROM=MAIL_FROM,
    MAIL_SERVER=MAIL_SERVER,
    MAIL_PORT=MAIL_PORT,
    MAIL_STARTTLS=MAIL_STARTTLS,
    MAIL_SSL_TLS=MAIL_SSL_TLS,
    USE_CREDENTIALS=USE_CREDENTIALS
))

templates_dir = Jinja2Templates(directory="app/templates/emails")




async def send_confirmation_email_service(name: str, email: str, token: str):

    confirmation_url = f"{DOMAIN_URL}auth/verify-email?token={token}"
    template = templates_dir.get_template("email_confirmation.html")
    html_content = template.render(name=name, confirmation_url=confirmation_url)
    await fastmail.send_message(message=MessageSchema(

        recipients=[email],
        subject="Confirm your Email!",
        body=html_content,
        subtype=MessageType.html
    )

    )

    return True


async def send_password_reset_email_service(name: str, email: str, token: str):

    reset_url = f"{DOMAIN_URL}auth/reset_password?token={token}"
    template = templates_dir.get_template("password_reset.html")
    html_content = template.render(name=name, reset_url=reset_url)

    await fastmail.send_message(message=MessageSchema(

        subject="Reset Your Password!",
        recipients=[email],
        body=html_content,
        subtype=MessageType.html

    )
    
    )

    return True