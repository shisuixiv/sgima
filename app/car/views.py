from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import filters
from rest_framework import permissions

from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache


from asgiref.sync import async_to_sync
from app.filters import CarFilter
from app.car.pagination import CustomPagination
from app.car.models import Car
from app.car.serializers import CarSerializer

from bot.bot import send_car_notification

class CarViewsetsAPI(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    permission_classes = [IsAuthenticated]

    pagination_class = CustomPagination

    filter_backend = {DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter}
    filterSet_class = CarFilter

    search_fields = ["brand", "model", "number"]
    ordering_fieilds = ["date", "brand", "probeg"]


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
    
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        car = serializer.save(user=request.user)

        car = Car.objects.create()
        process_car_creation.delay(car.id)

        return Response({"status": "Объявление генерируется"})

class CarNotication(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        car = serializer.save(user=self.request.user)
        
        car_data = {
            "user": car.user.username ,
            "brand": car.brand ,
            "model": car.model ,
            "number": car.number ,
            "probeg": car.probeg ,
            "caraka_transfer": car.caraka_transfer,
            "type_car": car.type_car,
            "data": car.data
        }

        async_to_sync(send_car_notification)(car_data)