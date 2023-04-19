from datetime import datetime

import pytz
from core.models import Provider, ProviderSalesHistory, User
from core.tests.factories.cars_factory import CarFactory
from core.tests.factories.providers_factory import ProviderFactory
from core.tests.factories.showrooms_factory import CarShowroomFactory
from core.tests.factories.users_factory import UserFactory
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

PROVIDER_API_ENDPOINT = "/api/providers"
PROVIDERS_HISTORY_API_ENDPOINT = "/api/providersaleshistory"


class ProviderViewTestCase(APITestCase):
    def setUp(self):
        self.user1 = UserFactory(user_type=User.Profile.PROVIDER)
        self.provider1 = ProviderFactory(user=self.user1)
        self.user2 = UserFactory(user_type=User.Profile.PROVIDER)

    def get_authenticated_client(self):
        client = APIClient()
        client.force_authenticate(user=self.user1)
        return client

    def test_get_providers(self):
        client = self.get_authenticated_client()
        response = client.get(f"{PROVIDER_API_ENDPOINT}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.provider1.name)

    def test_create_provider(self):
        client = self.get_authenticated_client()
        data = {
            "name": "New Provider",
            "date": str(datetime.now(pytz.utc)),
            "country": "RU",
            "user": self.user2.id,
        }
        response = client.post(f"{PROVIDER_API_ENDPOINT}/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        provider_count = Provider.objects.count()
        self.assertEqual(provider_count, 2)
        self.assertEqual(Provider.objects.last().name, "New Provider")

    def test_add_car(self):
        client = self.get_authenticated_client()
        car = CarFactory()
        data = {"car_id": car.id, "price": 1}
        response = client.post(
            f"{PROVIDER_API_ENDPOINT}/{self.provider1.id}/add-car/", data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get(f"{PROVIDER_API_ENDPOINT}/{self.provider1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["car_price"][car.id], data["price"])

        response = client.post(
            f"{PROVIDER_API_ENDPOINT}/{self.provider1.id}/add-car/", data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_invalid_car_id(self):
        client = self.get_authenticated_client()
        data = {"car_id": "str_id", "price": 1}
        response = client.post(
            f"{PROVIDER_API_ENDPOINT}/{self.provider1.id}/add-car/", data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProviderSalesHistoryViewTestCase(APITestCase):
    def setUp(self):
        self.car = CarFactory()
        showroom_user = UserFactory(user_type=User.Profile.SHOWROOM)
        self.showroom = CarShowroomFactory(user=showroom_user)
        self.user = UserFactory(user_type=User.Profile.PROVIDER)
        self.provider = ProviderFactory(user=self.user)

        self.valid_data = {
            "showroom": self.showroom.id,
            "provider": self.provider.id,
            "car": self.car.id,
            "price": 1000,
            "amount": 1,
        }

    def get_authenticated_client(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        return client

    def test_create(self):
        client = self.get_authenticated_client()
        response = client.post(
            f"{PROVIDERS_HISTORY_API_ENDPOINT}/", self.valid_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProviderSalesHistory.objects.count(), 1)
        self.assertEqual(ProviderSalesHistory.objects.get().price, 1000)
