from django.db import models
from app.users.models import User
# Create your models here.

CARABKA_TRANSFER = (
    ("Автомат", "Автомат"),
    ("Механика", "Механика"),
    ("Эдекторкар", "Эдекторкар"),
)

TYPE_CAR = (
    ("Седан", "Седан"),
    ("Универсал", "Универсал"),
    ("Грузовой", "Универсал"),
)

class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    brand = models.CharField(
        max_length=155,
        verbose_name='Бранд'
    )
    model = models.CharField(
        max_length=155,
        verbose_name='Модел'
    )
    number = models.CharField(
        max_length=50,
        verbose_name='Номер машины'
    )
    probeg = models.CharField(
        max_length=155,
        verbose_name='Пробег'
    )
    carabka_transfer = models.CharField(
        max_length=155,
        verbose_name='карабока передачи',
        choices=CARABKA_TRANSFER,
        default=None
    )   
    type_car = models.CharField(
        max_length=155,
        verbose_name='Тип ',
        choices=TYPE_CAR,
        default=None
    )
    date = models.CharField(
        max_length=100,
        verbose_name='Год Выпуска'
    )

    def __str__(self):
        return self.brand

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'    