from datetime import datetime, timedelta

import factory.fuzzy
import pytz
from core.models import CarShowroomDiscount, ProviderDiscount
from core.tests.randomize_value import get_random_specification
from factory.django import DjangoModelFactory
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
        end_dt=datetime.now(pytz.utc) + timedelta(days=2),
    )
    date_end = factory.fuzzy.FuzzyDateTime(
        start_dt=datetime.now(pytz.utc) + timedelta(days=3)
    )

    class Meta:
        model = Discount
        abstract = True


class CarShowroomDiscountFactory(DiscountFactory):
    @classmethod
    def _create(cls, model_class, showroom, *args, **kwargs):
        discount = CarShowroomDiscount.objects.create(showroom=showroom, **kwargs)
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
