from app.core.celery import celery_app
from app.services.email import send_confirmation_email_service, send_password_reset_email_service
from asgiref.sync import async_to_sync



@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_confirmation_email_task(self, name: str, email: str, token: str):

    try:
        sync_send = async_to_sync(send_confirmation_email_service)
        return sync_send(name,email,token)

    except Exception as exc:
        raise self.retry(exc=exc)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_password_reset_email_task(self, name: str, email: str, token: str):

    try:
        sync_send = async_to_sync(send_password_reset_email_service)
        return sync_send(name,email,token)

    except Exception as exc:
        raise self.retry(exc=exc)