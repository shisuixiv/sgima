import time
from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries" : 3})
def send_email_task(self, to_email : str, subject : str, body : str):
    try:
        time.sleep(4)
        result = {"status" : "sent", "to": to_email, "subject" : subject}
        return result
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)