import factory.fuzzy
from core.models import Customer
from core.tests.randomize_value import get_random_specification
from django_countries import countries
from factory.django import DjangoModelFactory


class CustomerFactory(DjangoModelFactory):
    sex = factory.fuzzy.FuzzyChoice(Customer.Gender.choices[0])
    phone_number = factory.Faker("phone_number")
    balance = factory.Faker("pydecimal", left_digits=5, right_digits=2, positive=True)
    age = factory.Faker("pyint", min_value=18, max_value=100)
    country = factory.Faker("random_element", elements=[x for x in countries])
    specification = get_random_specification()

    @classmethod
    def _create(cls, model_class, user, *args, **kwargs):
        customer = Customer.objects.create(user=user, **kwargs)
        return customer

    class Meta:
        model = Customer
