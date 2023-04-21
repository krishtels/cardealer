from core.tests.factories.users_factory import UserFactory
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

USERS_API_ENDPOINT = "/api/users"


class UserViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_get_without_permission(self):
        client = APIClient()
        response = client.get(f"{USERS_API_ENDPOINT}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
