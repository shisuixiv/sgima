import time
from celery import shared_task
from celery.utils.log import get_task_logger
from app.car.models import Car

logger = get_task_logger(__name__)

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries" : 3})
def send_email_task(self, to_email : str, subject : str, body : str):
    try:
        time.sleep(4)
        result = {"status" : "sent", "to": to_email, "subject" : subject}
        return result
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)

@shared_task
def process_car_creation(car_id):
    car = Car.objects.get(id=car_id)

# app/car/tasks.py
from celery import shared_task
import asyncio
from bot.bot import send_car_notification

@shared_task
def send_car_notification_task(car_data):
    asyncio.run(send_car_notification(car_data))
