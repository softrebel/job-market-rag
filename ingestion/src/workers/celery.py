from celery import Celery

from config.settings import settings


celery = Celery("ingestion", broker=settings.REDIS_URL)
