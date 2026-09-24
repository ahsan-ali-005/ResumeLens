from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from app.core.config import settings

MAIL_USERNAME = settings.MAIL_USERNAME
MAIL_PASSWORD = settings.MAIL_PASSWORD
MAIL_FROM = settings.MAIL_FROM
MAIL_PORT = settings.MAIL_PORT
MAIL_SERVER = settings.MAIL_SERVER
MAIL_STARTTLS=settings.MAIL_STARTTLS
MAIL_SSL_TLS = settings.MAIL_SSL_TLS
USE_CREDENTIALS=settings.USE_CREDENTIALS


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




async def send_confirmation_email_service():

    await fastmail.send_message(message=MessageSchema(

        recipients=['mr.ahsanali005@gmail.com'],
        subject="Hey! how are you?",
        body="I am reaching out because i want to.......",
        subtype=MessageType.plain
    )

    )

    return {"message" : "Email Sent!"}
