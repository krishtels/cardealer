from core.models import User
from core.tests.factories.customers_factory import CustomerFactory
from core.tests.factories.users_factory import UserFactory
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

CUSTOMER_API_ENDPOINT = "/api/customers"


class CustomerViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory(user_type=User.Profile.CUSTOMER)
        self.customer = CustomerFactory(user=self.user)

    def get_authenticated_client(self):
        client = APIClient()
        client.force_authenticate(user=self.user)
        return client

    def test_get_customer(self):
        client = self.get_authenticated_client()
        response = client.get(f"{CUSTOMER_API_ENDPOINT}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["age"], self.customer.age)
