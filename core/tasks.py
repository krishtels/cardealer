from celery import shared_task
from django.utils import timezone
from tools.functions import (
    buy_car_from_provider,
    buy_car_from_showroom,
    find_best_order_in_showroom,
    find_cars_by_specification,
    get_car_best_price,
    get_cars_to_buy,
)

from core.models import (
    CarShowroom,
    CarShowroomDiscount,
    Customer,
    ProviderCars,
    ProviderDiscount,
    ShowroomCars,
)


@shared_task
def buy_cars_from_provider_to_showroom():
    for showroom in CarShowroom.objects.filter(is_active=True).exclude(
        specification=None
    ):
        if showroom.balance <= 0:
            continue

        cars_to_buy = get_cars_to_buy(showroom)
        if not cars_to_buy:
            continue
        best_price = get_car_best_price(cars_to_buy)

        for car in best_price:
            if showroom.balance >= best_price[car][0]:
                buy_car_from_provider(
                    car=car,
                    showroom=showroom,
                    provider=best_price[car][1],
                    price=best_price[car][0],
                )


@shared_task
def buy_cars_from_showroom_to_customer():
    for customer in Customer.objects.filter(is_active=True).exclude(specification=None):
        if customer.balance <= 0:
            continue

        for specification in customer.specification:
            cars = find_cars_by_specification(specification)
            max_price = specification["max_price"]
            if not cars:
                continue
            best_price = find_best_order_in_showroom(cars, max_price)

            for car in best_price:
                if customer.balance >= best_price[car][0]:
                    buy_car_from_showroom(
                        car=car,
                        customer=customer,
                        showroom=best_price[car][1],
                        price=best_price[car][0],
                    )


@shared_task
def check_passed_discounts():
    showroom_discounts = CarShowroomDiscount.objects.filter(is_active=True)
    for discount in showroom_discounts:
        if discount.date_end < timezone.now().date():
            discount.is_active = False
            discount.save()

            showroom = discount.showroom
            cars = find_cars_by_specification(discount.params)
            for car in cars:
                try:
                    showroom_car_price = (
                        ShowroomCars.objects.filter(showroom__id=showroom.id)
                        .select_related("car")
                        .get(car__id=car.id)
                    )
                except ShowroomCars.DoesNotExist:
                    showroom_car_price = None
                if showroom_car_price:
                    showroom_car_price.save()

    provider_discounts = ProviderDiscount.objects.filter(is_active=True)
    for discount in provider_discounts:
        if discount.date_end < timezone.now().date():
            discount.is_active = False
            discount.save()

            provider = discount.provider
            cars = find_cars_by_specification(discount.params)
            for car in cars:
                try:
                    provider_car_price = (
                        ProviderCars.objects.filter(provider__id=provider.id)
                        .select_related("car")
                        .get(car__id=car.id)
                    )
                except ProviderCars.DoesNotExist:
                    provider_car_price = None
                if provider_car_price:
                    provider_car_price.save()
