from core.models import (
    Car,
    CarShowroomSalesHistory,
    ProviderCars,
    ProviderSalesHistory,
    ShowroomCars,
)
from django.db.models import Count, Q


def buy_car_from_provider(car, showroom, provider, price):
    try:
        showroom_car_price = (
            ShowroomCars.objects.filter(showroom__id=showroom.id)
            .select_related("car")
            .get(car__id=car.id)
        )
    except ShowroomCars.DoesNotExist:
        showroom_car_price = None
    if showroom_car_price:
        showroom_car_price.amount += 1
        showroom_car_price.save()
    else:
        showroom_car_price = ShowroomCars.objects.create(
            car=car,
            showroom=showroom,
            price=price,
            amount=1,
        )
        showroom_car_price.save()
    ProviderSalesHistory.objects.create(
        car=car,
        provider=provider,
        showroom=showroom,
        price=price,
    )
    showroom.balance -= price
    showroom.save()
    return


def get_car_best_price(cars):
    best_price = {}
    for car in cars:
        car_price = ProviderCars.objects.filter(car=car).order_by("price_with_discount")
        if car_price is None:
            continue
        else:
            price = car_price[0].price_with_discount
            provider = car_price[0].provider
            best_price[car] = [price, provider]

    return best_price


def get_cars_to_buy(showroom):
    cars_to_buy = []
    for specification in showroom.specification:
        cars = find_cars_by_specification(specification)
        cars_sold = (
            cars.filter(carshowroomsaleshistory__showroom=showroom)
            .annotate(total_sales=Count("carshowroomsaleshistory"))
            .order_by("-total_sales")
        )
        cars_not_sold = cars.exclude(id__in=cars_sold.values_list("id", flat=True))

        cars_to_buy.extend(cars_sold)
        cars_to_buy.extend(cars_not_sold)

    return cars_to_buy


def find_cars_by_specification(specification):
    filter_query = Q()
    for key in specification:
        if key == "engine_volume":
            filter_query &= Q(**{f"{key}__gte": specification[key]})
        elif key != "max_price":
            filter_query &= Q(**{key: specification[key]})

    cars = Car.objects.filter(filter_query)

    return cars


def find_best_order_in_showroom(cars, max_price):
    best_price = {}
    for car in cars:
        car_price = ShowroomCars.objects.filter(
            car=car, price_with_discount__lte=max_price
        ).order_by("price_with_discount")
        if car_price is None:
            continue
        else:
            price = car_price[0].price
            showroom = car_price[0].showroom
            best_price[car] = [price, showroom]

    return best_price


def buy_car_from_showroom(car, showroom, customer, price):
    CarShowroomSalesHistory.objects.create(
        car=car,
        customer=customer,
        showroom=showroom,
        price=price,
    )
    customer.balance -= price
    customer.save()
    return
