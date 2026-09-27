from celery import Celery
from app.core.config import settings


CELERY_BACKEND = settings.CELERY_BACKEND
CELERY_BROKER = settings.CELERY_BROKER


celery_app = Celery(
    "ResumeLens",
    backend=CELERY_BACKEND,
    broker=CELERY_BROKER,
    include=["app.tasks.email_tasks"]
)