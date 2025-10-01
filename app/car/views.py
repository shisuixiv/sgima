from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from rest_framework.response import Response

from app.car.models import Car
from app.car.serializers import CarSerializer

class CArViewsetsAPI(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user_id = request.user.id
        cache_key = f"user_cars_{user_id}"
        cars = cache.get(cache_key)

        if not cars:
            print("Null")
            queryset = self.get_queryset().filter(user_id=user_id)
            serializer = self.get_serializer(queryset, many=True)
            cars = serializer.data
            cache.set(cache_key, cars, timeout=60*5)
        else:
            print("Берем из кэша!")

        return Response(cars)

    def retrieve(self, request, *args, **kwargs):
        car_id = kwargs.get('pk')
        cache_key = f"car_{car_id}"
        car = cache.get(cache_key)

        if not car:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            car = serializer.data
            cache.set(cache_key, car, timeout=60*5)
        else:
            pass

        return Response(car)