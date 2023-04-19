import pytest
from core.models import ProviderDiscount, User
from rest_framework import status

SHOWROOMS_DISCOUNTS_API_ENDPOINT = "/api/showroomdiscounts"
PROVIDER_DISCOUNTS_API_ENDPOINT = "/api/providerdiscounts"


@pytest.mark.django_db
@pytest.mark.parametrize(
    "get_authenticated_client", [User.Profile.SHOWROOM], indirect=True
)
def test_list_car_showroom_discounts(
    get_carshowroom_discount, get_authenticated_client
):
    discount = get_carshowroom_discount
    client = get_authenticated_client
    response = client.get(f"{SHOWROOMS_DISCOUNTS_API_ENDPOINT}/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "get_authenticated_client", [User.Profile.SHOWROOM], indirect=True
)
def test_retrieve_car_showroom_discount(
    get_carshowroom_discount, get_authenticated_client
):
    discount = get_carshowroom_discount
    client = get_authenticated_client
    response = client.get(f"{SHOWROOMS_DISCOUNTS_API_ENDPOINT}/{discount.pk}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == discount.id


@pytest.mark.django_db
@pytest.mark.parametrize(
    "get_authenticated_client", [User.Profile.PROVIDER], indirect=True
)
def test_delete_provider_discount(get_provider_discount, get_authenticated_client):
    discount = get_provider_discount
    client = get_authenticated_client
    response = client.delete(f"{PROVIDER_DISCOUNTS_API_ENDPOINT}/{discount.pk}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert ProviderDiscount.objects.filter(pk=discount.id).exists() is True
    assert ProviderDiscount.objects.filter(is_active=True).count() == 0
