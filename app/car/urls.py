from rest_framework.routers import DefaultRouter
from app.car.views import CarViewsetsAPI, CarNotication

router = DefaultRouter()
router.register(r'car', CarViewsetsAPI, basename='car')
router.register('notification', CarNotication, basename='car-notification')

urlpatterns = []

urlpatterns += router.urls