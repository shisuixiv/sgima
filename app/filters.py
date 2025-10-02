import django_filters
from app.car.models import Car

class CarFilter(django_filters.FilterSet):
    date_from = django_filters.NumberFilter(field_name='data', lookup_expr="gte")
    date_to = django_filters.NumberFilter(field_name='data', lookup_expr="lte")
    brand = django_filters.CharFilter(field_name='brand', lookup_expr="icontains")
    type_car = django_filters.CharFilter(field_name='type_car', lookup_expr="type_car")

    class Meta:
        model = Car
        fields = ["brand", "type_car", "carabka_transfer"]