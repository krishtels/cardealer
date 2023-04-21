from datetime import datetime, timedelta

import factory.fuzzy
import pytz
from core.models import CarShowroomDiscount, ProviderDiscount, ShowroomCars
from core.tests.randomize_value import get_random_specification
from factory.django import DjangoModelFactory
from tools.functions import find_cars_by_specification
from tools.models import Discount


class DiscountFactory(DjangoModelFactory):
    name = factory.Faker("word")
    description = factory.Faker("text", max_nb_chars=200)
    amount_to_get_sale = factory.Faker("pyint", min_value=1, max_value=100)
    percent = factory.Faker(
        "pydecimal", left_digits=2, right_digits=2, min_value=0, max_value=100
    )
    params = get_random_specification()

    date_start = factory.fuzzy.FuzzyDateTime(
        start_dt=datetime.now(pytz.utc),
        end_dt=datetime.now(pytz.utc) + timedelta(days=3),
    )
    date_end = factory.fuzzy.FuzzyDateTime(
        start_dt=datetime.now(pytz.utc) + timedelta(days=4),
        end_dt=datetime.now(pytz.utc) + timedelta(days=7),
    )

    class Meta:
        model = Discount
        abstract = True


class CarShowroomDiscountFactory(DiscountFactory):
    @classmethod
    def _create(cls, model_class, showroom, *args, **kwargs):
        discount = CarShowroomDiscount.objects.create(showroom=showroom, **kwargs)
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
                showroom_car_price.price_with_discount = (
                    showroom_car_price.price * (100 - discount.percent) / 100
                )
                showroom_car_price.save()
        return discount

    class Meta:
        model = CarShowroomDiscount


class ProviderDiscountFactory(DiscountFactory):
    @classmethod
    def _create(cls, model_class, provider, *args, **kwargs):
        discount = ProviderDiscount.objects.create(provider=provider, **kwargs)
        return discount

    class Meta:
        model = ProviderDiscount
