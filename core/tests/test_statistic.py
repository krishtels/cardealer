from core.models import CarShowroomSalesHistory, User
from core.serializers import CarShowroomSalesHistorySerializer
from core.tests.factories.cars_factory import CarFactory
from core.tests.factories.customers_factory import CustomerFactory
from core.tests.factories.providers_factory import (
    ProviderFactory,
    ProviderSalesHistoryFactory,
)
from core.tests.factories.showrooms_factory import (
    CarShowroomFactory,
    CarShowroomSalesHistoryFactory,
)
from core.tests.factories.users_factory import UserFactory
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

SHOWROOMS_API_ENDPOINT = "/api/showrooms"
CUSTOMERS_API_ENDPOINT = "/api/customers"


class CarShowroomStatisticTestCase(APITestCase):
    def setUp(self):
        self.car = CarFactory()
        customer_user = UserFactory(user_type=User.Profile.CUSTOMER)
        self.customer = CustomerFactory(user=customer_user)
        self.user = UserFactory(user_type=User.Profile.SHOWROOM)
        self.showroom = CarShowroomFactory(user=self.user)
        provider_user = UserFactory(user_type=User.Profile.PROVIDER)
        self.provider = ProviderFactory(user=provider_user)

        self.history1 = CarShowroomSalesHistoryFactory(
            car=self.car, showroom=self.showroom, customer=self.customer
        )
        self.history2 = CarShowroomSalesHistoryFactory(
            car=self.car, showroom=self.showroom, customer=self.customer
        )
        self.provider_history = ProviderSalesHistoryFactory(
            car=self.car, showroom=self.showroom, provider=self.provider
        )

    def get_authenticated_client(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        return client

    def test_get_number_of_sells(self):
        client = self.get_authenticated_client()
        response = client.get(
            f"{SHOWROOMS_API_ENDPOINT}/{self.showroom.id}/number-of-sell/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["number_of_sales"],
            self.history1.amount + self.history2.amount,
        )

    def test_get_showroom_profit(self):
        client = self.get_authenticated_client()
        response = client.get(f"{SHOWROOMS_API_ENDPOINT}/{self.showroom.id}/profit/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        profit_sum = (
            self.history1.amount * self.history1.price
            + self.history2.amount * self.history2.price
        )
        self.assertEqual(
            response.data["profit"],
            profit_sum,
        )

    def test_get_unique_customers(self):
        client = self.get_authenticated_client()
        response = client.get(
            f"{SHOWROOMS_API_ENDPOINT}/{self.showroom.id}/unique-customers/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            len(response.data["unique_customers"]),
            1,
        )

    def test_get_unique_providers(self):
        client = self.get_authenticated_client()
        response = client.get(
            f"{SHOWROOMS_API_ENDPOINT}/{self.showroom.id}/unique-providers/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            len(response.data["unique_providers"]),
            1,
        )


class CustomerStatisticTestCase(APITestCase):
    def setUp(self):
        self.car = CarFactory()
        self.user = UserFactory(user_type=User.Profile.CUSTOMER)
        self.customer = CustomerFactory(user=self.user)
        showroom_user = UserFactory(user_type=User.Profile.SHOWROOM)
        self.showroom = CarShowroomFactory(user=showroom_user)

        self.history1 = CarShowroomSalesHistoryFactory(
            car=self.car, showroom=self.showroom, customer=self.customer
        )

    def get_authenticated_client(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        return client

    def test_get_amount_money_spent(self):
        client = self.get_authenticated_client()
        response = client.get(f"{CUSTOMERS_API_ENDPOINT}/money-spent/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            len(response.data["spent_money"]),
            1,
        )
        max_spent_sum = self.history1.amount * self.history1.price

        self.assertEqual(response.data["spent_money"][0]["spent_sum"], max_spent_sum)
