import factory
from core.models import User
from django.contrib.auth.hashers import make_password
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = make_password("password")
    user_type = User.Profile.NONE

    class Meta:
        model = User
