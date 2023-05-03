import pytest
from core.models import User
from core.tests.factories.discount_factories import (
    CarShowroomDiscountFactory,
    ProviderDiscountFactory,
)
from core.tests.factories.providers_factory import ProviderFactory
from core.tests.factories.showrooms_factory import CarShowroomFactory
from core.tests.factories.users_factory import UserFactory
from rest_framework.test import APIClient


@pytest.fixture
def get_carshowroom_discount():
    showroom_user = UserFactory(user_type=User.Profile.SHOWROOM)
    showroom = CarShowroomFactory(user=showroom_user)
    return CarShowroomDiscountFactory(showroom=showroom)


@pytest.fixture
def get_authenticated_client(request):
    user = UserFactory(user_type=request.param)
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def get_provider_discount():
    provider_user = UserFactory(user_type=User.Profile.PROVIDER)
    provider = ProviderFactory(user=provider_user)
    return ProviderDiscountFactory(provider=provider)


@pytest.fixture
def get_provider_discount_valid_data():
    return {"name": "ddd", "description": "wds", "amount_to_get_sale": 2}
