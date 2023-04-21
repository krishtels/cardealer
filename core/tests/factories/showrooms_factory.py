import random

import factory
from core.models import CarShowroom, CarShowroomSalesHistory, ShowroomCars
from core.tests.randomize_value import get_random_specification
from django_countries import countries
from factory.django import DjangoModelFactory


class CarShowroomFactory(DjangoModelFactory):
    name = factory.Faker("company")
    specification = get_random_specification()

    country = factory.Faker("random_element", elements=[x for x in countries])

    @classmethod
    def _create(cls, model_class, user, cars=None, *args, **kwargs):
        showroom = CarShowroom.objects.create(user=user, **kwargs)
        if cars:
            for car in cars:
                ShowroomCars.objects.create(
                    car=car,
                    showroom=showroom,
                    price=round(random.uniform(1, 10), 2),
                )
        return showroom

    class Meta:
        model = CarShowroom


class CarShowroomSalesHistoryFactory(DjangoModelFactory):
    id = factory.Faker("uuid4")
    price = factory.Faker("pydecimal", left_digits=5, right_digits=2, positive=True)
    amount = factory.Faker("pyint", min_value=1, max_value=100)

    @classmethod
    def _create(cls, model_class, showroom, customer, car, *args, **kwargs):
        history = CarShowroomSalesHistory.objects.create(
            showroom=showroom, customer=customer, car=car, **kwargs
        )
        return history

    class Meta:
        model = CarShowroomSalesHistory
