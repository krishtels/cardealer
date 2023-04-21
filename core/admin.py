from django.contrib import admin

from .models import (
    Car,
    CarShowroom,
    CarShowroomDiscount,
    CarShowroomSalesHistory,
    Customer,
    Provider,
    ProviderCars,
    ProviderDiscount,
    ProviderSalesHistory,
    ShowroomCars,
    User,
)

Models = (
    Car,
    CarShowroom,
    CarShowroomDiscount,
    CarShowroomSalesHistory,
    Customer,
    Provider,
    ProviderCars,
    ProviderDiscount,
    ProviderSalesHistory,
    ShowroomCars,
    User,
)


admin.site.register(Models)
