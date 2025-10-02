from rest_framework.routers import DefaultRouter
from app.car.views import CarViewsetsAPI

router = DefaultRouter()
router.register('car', CarViewsetsAPI, basename='car')

urlpatterns = []

urlpatterns += router.urls