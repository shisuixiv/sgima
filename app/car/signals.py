from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.cache import cache
from app.car.models import Car

@receiver([post_save, post_delete], sender=Car)
def clear_car_cache(sender, instance, **kwargs):
    cache.delete(f"user_cars_{instance.user_id}")
    cache.delete(f"car_{instance.id}")