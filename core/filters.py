from django_filters import rest_framework as filters

from core.models import (
    Car,
    CarShowroom,
    CarShowroomDiscount,
    CarShowroomSalesHistory,
    Customer,
    Provider,
    ProviderDiscount,
    ProviderSalesHistory,
    User,
)


class CarFilter(filters.FilterSet):
    class Meta:
        model = Car
        fields = {
            "engine_volume": ["exact", "gte", "lte"],
            "brand": ["exact", "icontains"],
            "model": ["exact", "icontains"],
            "color": ["exact", "icontains"],
            "engine_type": ["exact"],
        }


class CarShowroomFilter(filters.FilterSet):
    class Meta:
        model = CarShowroom
        fields = [
            "name",
            "country",
            "is_active",
        ]


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = [
            "user_type",
            "is_active",
            "username",
            "first_name",
            "last_name",
        ]


class CustomerFilter(filters.FilterSet):
    class Meta:
        model = Customer
        fields = {
            "age": ["exact", "gte", "lte"],
            "sex": ["exact"],
            "country": ["exact"],
            "is_active": ["exact"],
        }


class ProviderFilter(filters.FilterSet):
    class Meta:
        model = Provider
        fields = {
            "year_founded": ["exact", "gte", "lte"],
            "name": ["exact", "icontains"],
            "country": ["exact"],
            "is_active": ["exact"],
        }


class CarShowroomDiscountFilter(filters.FilterSet):
    class Meta:
        model = CarShowroomDiscount
        fields = {
            "date_start": ["exact", "gte", "lte"],
            "date_end": ["exact", "gte", "lte"],
            "name": ["exact", "icontains"],
            "percent": ["exact", "gte", "lte"],
            "is_active": ["exact"],
        }


class ProviderDiscountFilter(filters.FilterSet):
    class Meta:
        model = ProviderDiscount
        fields = {
            "date_start": ["exact", "gte", "lte"],
            "date_end": ["exact", "gte", "lte"],
            "name": ["exact", "icontains"],
            "percent": ["exact", "gte", "lte"],
            "is_active": ["exact"],
        }


class CarShowroomSalesHistoryFilter(filters.FilterSet):
    class Meta:
        model = CarShowroomSalesHistory
        fields = [
            "showroom",
            "car",
        ]


class ProviderSalesHistoryFilter(filters.FilterSet):
    class Meta:
        model = ProviderSalesHistory
        fields = [
            "provider",
            "car",
        ]
