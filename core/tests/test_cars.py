from core.models import Car, User
from core.tests.factories.cars_factory import CarFactory
from core.tests.factories.users_factory import UserFactory
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

CAR_API_ENDPOINT = "/api/cars"


class CarViewTestCase(APITestCase):
    def setUp(self):
        self.car1 = CarFactory()
        self.user = UserFactory(user_type=User.Profile.PROVIDER)

    def get_authenticated_client(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        return client

    def get_unauthenticated_client(self):
        client = APIClient()
        return client

    def test_create_same_car(self):
        data = {
            "engine_type": self.car1.engine_type,
            "brand": self.car1.brand,
            "model": self.car1.model,
            "color": self.car1.color,
            "engine_volume": self.car1.engine_volume,
        }
        client = self.get_authenticated_client()
        response = client.post(f"{CAR_API_ENDPOINT}/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Car.objects.count(), 1)

    def test_create_without_permission(self):
        data = {
            "engine_type": Car.EngineType.Gasoline,
            "brand": "brand",
            "model": "model",
            "color": "color",
            "engine_volume": 0,
        }
        client = self.get_unauthenticated_client()

        response = client.post(f"{CAR_API_ENDPOINT}/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
