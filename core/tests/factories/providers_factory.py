import random
from typing import List

import factory
from core.models import Provider, ProviderCars, ProviderSalesHistory
from django_countries import countries
from factory.django import DjangoModelFactory


class ProviderFactory(DjangoModelFactory):
    name = factory.Faker("company")
    year_founded = factory.Faker("date")
    country = factory.Faker("random_element", elements=[x for x in countries])

    @classmethod
    def _create(cls, model_class, user, cars: List[int] = None, *args, **kwargs):
        provider = Provider.objects.create(user=user, **kwargs)

        if cars:
            [
                ProviderCars.objects.create(
                    car=car,
                    provider=provider,
                    price=round(random.uniform(1, 10), 2),
                )
                for car in cars
            ]
        return provider

    class Meta:
        model = Provider


class ProviderSalesHistoryFactory(DjangoModelFactory):
    id = factory.Faker("uuid4")
    price = factory.Faker("pydecimal", left_digits=5, right_digits=2, positive=True)
    amount = factory.Faker("pyint", min_value=1, max_value=100)

    @classmethod
    def _create(cls, model_class, showroom, provider, car, *args, **kwargs):
        history = ProviderSalesHistory.objects.create(
            showroom=showroom, provider=provider, car=car, **kwargs
        )
        return history

    class Meta:
        model = ProviderSalesHistory
