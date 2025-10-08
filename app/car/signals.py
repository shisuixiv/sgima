from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.cache import cache
from app.car.models import Car

@receiver([post_save, post_delete], sender=Car)
def clear_car_cache(sender, instance, **kwargs):
    cache.delete(f"user_cars_{instance.user_id}")
    cache.delete(f"car_{instance.id}")
# car/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Car

from bot.bot import send_car_notification
from app.tasks import send_car_notification_task 
@receiver(post_save, sender=Car)
def notify_admin(sender, instance, created, **kwargs):
    if created:
        car_data = {
            "user": instance.user.username,  # <- вместо объекта User
            "brand": instance.brand,
            "model": instance.model,
            "number": instance.number,
            "date": str(instance.date),      # если это datetime
            "carabka_transfer": instance.carabka_transfer,
            "type_car": instance.type_car,
            "probeg": instance.probeg,
        }
        send_car_notification_task.delay(car_data)

    