import datetime

from celery import Celery
from core.models import (
    CarShowroomSalesHistory,
    ProviderSalesHistory,
    ShowroomCars,
    User,
)
from core.tasks import (
    buy_cars_from_provider_to_showroom,
    buy_cars_from_showroom_to_customer,
    check_passed_discounts,
)
from core.tests.factories.cars_factory import CarFactory
from core.tests.factories.customers_factory import CustomerFactory
from core.tests.factories.discount_factories import CarShowroomDiscountFactory
from core.tests.factories.providers_factory import ProviderFactory
from core.tests.factories.showrooms_factory import CarShowroomFactory
from core.tests.factories.users_factory import UserFactory
from django.shortcuts import get_object_or_404
from django.test import TestCase


class CeleryTaskTestCase(TestCase):
    def setUp(self):
        self.car = CarFactory()
        self.user = UserFactory(user_type=User.Profile.SHOWROOM)
        self.percent = 20
        self.showroom = CarShowroomFactory(
            user=self.user,
            cars=[self.car],
            balance=10,
            specification=[{"brand": self.car.brand}],
        )

        self.user_provider = UserFactory(user_type=User.Profile.PROVIDER)
        self.provider = ProviderFactory(
            user=self.user_provider,
            cars=[self.car],
        )

        self.showroom_discount = CarShowroomDiscountFactory(
            showroom=self.showroom,
            date_start=datetime.date.today() - datetime.timedelta(days=2),
            date_end=datetime.date.today() - datetime.timedelta(days=1),
            percent=self.percent,
            params={"brand": self.car.brand, "color": self.car.color},
        )

        self.user_customer = UserFactory(user_type=User.Profile.CUSTOMER)

        self.customer = CustomerFactory(
            user=self.user_customer,
            balance=10,
            specification=[{"brand": self.car.brand, "max_price": 10}],
        )
        self.showroom_car = ShowroomCars.objects.filter(
            car=self.car, showroom=self.showroom
        )[0]

    def test_update_passed_discount_task(self):
        check_passed_discounts()

        self.showroom_car.refresh_from_db()
        price_after_celery = self.showroom_car.price_with_discount
        self.assertEqual(price_after_celery, self.showroom_car.price)

    def test_buy_cars_from_provider_to_showroom_task(self):
        self.showroom_car.refresh_from_db()

        amount_before_celery = self.showroom_car.amount
        amount_sales_before = ProviderSalesHistory.objects.filter(
            provider=self.provider, showroom=self.showroom
        ).count()

        buy_cars_from_provider_to_showroom()
        self.showroom_car.refresh_from_db()
        amount_after_celery = self.showroom_car.amount
        amount_sales_after = ProviderSalesHistory.objects.filter(
            provider=self.provider, showroom=self.showroom
        ).count()

        self.assertEqual(amount_before_celery + 1, amount_after_celery)
        self.assertEqual(amount_sales_before + 1, amount_sales_after)

    def test_buy_cars_from_showroom_to_customer_task(self):
        amount_sales_before = CarShowroomSalesHistory.objects.filter(
            customer=self.customer, showroom=self.showroom
        ).count()

        buy_cars_from_showroom_to_customer()

        amount_sales_after = CarShowroomSalesHistory.objects.filter(
            customer=self.customer, showroom=self.showroom
        ).count()

        self.assertEqual(amount_sales_before + 1, amount_sales_after)
