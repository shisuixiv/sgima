from rest_framework.routers import DefaultRouter
from app.car.views import CArViewsetsAPI

router = DefaultRouter()
router.register('car', CArViewsetsAPI, basename='car')

urlpatterns = [
    
]

urlpatterns += router.urls