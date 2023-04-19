from factory.django import DjangoModelFactory
import factory
import factory.fuzzy
from core.models import Car


class CarFactory(DjangoModelFactory):
    engine_type = factory.fuzzy.FuzzyChoice(Car.EngineType.choices[0])
    brand = factory.Faker("word")
    model = factory.Faker("word")
    color = factory.Faker("color_name")
    engine_volume = factory.Faker("pyfloat", min_value=0.00, max_value=10.0)

    class Meta:
        model = Car
