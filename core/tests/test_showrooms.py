from core.models import CarShowroomSalesHistory, User
from core.serializers import CarShowroomSalesHistorySerializer
from core.tests.factories.cars_factory import CarFactory
from core.tests.factories.customers_factory import CustomerFactory
from core.tests.factories.showrooms_factory import (
    CarShowroomFactory,
    CarShowroomSalesHistoryFactory,
)
from core.tests.factories.users_factory import UserFactory
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

SHOWROOMS_API_ENDPOINT = "/api/showrooms"
SHOWROOMS_HISTORY_API_ENDPOINT = "/api/showroomsaleshistory"


class ShowroomViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory(user_type=User.Profile.SHOWROOM)
        self.showroom1 = CarShowroomFactory(user=self.user)

    def get_authenticated_client(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        return client

    def test_get_showrooms(self):
        client = APIClient()
        response = client.get(f"{SHOWROOMS_API_ENDPOINT}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["name"], self.showroom1.name)

    def test_add_car(self):
        client = self.get_authenticated_client()
        car = CarFactory()
        data = {"car_id": car.id, "amount": 2, "price": 1}
        response = client.post(
            f"{SHOWROOMS_API_ENDPOINT}/{self.showroom1.id}/add-car/", data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get(f"{SHOWROOMS_API_ENDPOINT}/{self.showroom1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["car_amount"][car.id], data["amount"])

        response = client.post(
            f"{SHOWROOMS_API_ENDPOINT}/{self.showroom1.id}/add-car/", data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_invalid_car_id(self):
        client = self.get_authenticated_client()
        data = {"car_id": "str_id", "price": 1, "amount": 2}
        response = client.post(
            f"{SHOWROOMS_API_ENDPOINT}/{self.showroom1.id}/add-car/", data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CarShowroomSalesHistoryViewTestCase(APITestCase):
    def setUp(self):
        self.car = CarFactory()
        customer_user = UserFactory(user_type=User.Profile.CUSTOMER)
        self.customer = CustomerFactory(user=customer_user)
        self.user = UserFactory(user_type=User.Profile.SHOWROOM)
        self.showroom = CarShowroomFactory(user=self.user)

        self.history1 = CarShowroomSalesHistoryFactory(
            car=self.car, showroom=self.showroom, customer=self.customer
        )
        self.history2 = CarShowroomSalesHistoryFactory(
            car=self.car, showroom=self.showroom, customer=self.customer
        )

    def get_authenticated_client(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        return client

    def test_get_car_showroom_list(self):
        client = self.get_authenticated_client()
        response = client.get(f"{SHOWROOMS_HISTORY_API_ENDPOINT}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = CarShowroomSalesHistorySerializer(
            [self.history1, self.history2], many=True
        ).data
        self.assertEqual(response.data, expected_data)

    def test_delete(self):
        client = self.get_authenticated_client()
        response = client.delete(
            f"{SHOWROOMS_HISTORY_API_ENDPOINT}/{self.history1.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(
            CarShowroomSalesHistory.objects.filter(pk=self.history1.id).exists()
        )
        self.assertEqual(
            CarShowroomSalesHistory.objects.filter(is_active=True).count(), 1
        )
        self.assertEqual(CarShowroomSalesHistory.objects.count(), 2)
