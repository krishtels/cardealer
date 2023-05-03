from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from tools.functions import find_cars_by_specification
from tools.permissions import (
    IsCustomerAdminOrReadOnly,
    IsProviderAdmin,
    IsProviderAdminOrReadOnly,
    IsShowroomAdmin,
    IsShowroomAdminOrReadOnly,
)
from tools.validators import is_valid_id

from core.filters import (
    CarFilter,
    CarShowroomDiscountFilter,
    CarShowroomFilter,
    CarShowroomSalesHistoryFilter,
    CustomerFilter,
    ProviderDiscountFilter,
    ProviderFilter,
    UserFilter,
)
from core.models import (
    Car,
    CarShowroom,
    CarShowroomDiscount,
    CarShowroomSalesHistory,
    Customer,
    Provider,
    ProviderCars,
    ProviderDiscount,
    ProviderSalesHistory,
    ShowroomCars,
    User,
)
from core.serializers import (
    CarSerializer,
    CarShowroomDiscountSerializer,
    CarShowroomNumberOfSellsSerializer,
    CarShowroomProfitSerializer,
    CarShowroomSalesHistorySerializer,
    CarShowroomSerializer,
    CarShowroomUniqueCustomersSerializer,
    CarShowroomUniqueProvidersSerializer,
    CustomerSerializer,
    CustomerSpentMoneySerializer,
    ProviderDiscountSerializer,
    ProviderSalesHistorySerializer,
    ProviderSerializer,
    UserSerializer,
)


class BaseViewSet(ModelViewSet):
    def perform_destroy(self, instance, pk=None):
        instance.is_active = False
        instance.save()


class CarViewSet(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = (IsProviderAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarFilter


class CarShowroomViewSet(BaseViewSet):
    queryset = CarShowroom.objects.filter(is_active=True)
    serializer_class = CarShowroomSerializer
    permission_classes = (IsShowroomAdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = CarShowroomFilter

    @action(
        detail=True,
        methods=["post"],
        url_path="add-car",
    )
    def add_showroom_cars(self, request, pk=None):
        showroom = self.get_object()
        car_id = request.data.get("car_id")
        if not is_valid_id(car_id):
            return Response(
                {"error": "Id must be numeric"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        car = get_object_or_404(Car, pk=car_id)

        amount = request.data.get("amount")
        price = request.data.get("price")
        try:
            ShowroomCars.objects.create(
                car=car, showroom=showroom, amount=amount, price=price
            )
        except IntegrityError:
            return Response(
                {"error": "This car already exists in this showroom"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_200_OK)

    @action(
        methods=["get"],
        detail=True,
        serializer_class=CarShowroomNumberOfSellsSerializer,
        url_path="number-of-sell",
    )
    def get_number_of_sells(self, request, pk=None):
        serializer = self.get_serializer(data=request.data, context={"showroom_id": pk})
        if serializer.is_valid():
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)

    @action(
        methods=["get"],
        detail=True,
        serializer_class=CarShowroomProfitSerializer,
        url_path="profit",
    )
    def get_showroom_profit(self, request, pk=None):
        serializer = self.get_serializer(data=request.data, context={"showroom_id": pk})
        if serializer.is_valid():
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)

    @action(
        methods=["get"],
        detail=True,
        serializer_class=CarShowroomUniqueCustomersSerializer,
        url_path="unique-customers",
    )
    def get_unique_customers(self, request, pk=None):
        serializer = self.get_serializer(data=request.data, context={"showroom_id": pk})
        if serializer.is_valid():
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)

    @action(
        methods=["get"],
        detail=True,
        serializer_class=CarShowroomUniqueProvidersSerializer,
        url_path="unique-providers",
    )
    def get_unique_providers(self, request, pk=None):
        serializer = self.get_serializer(data=request.data, context={"showroom_id": pk})
        if serializer.is_valid():
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)


class CustomerViewSet(BaseViewSet):
    queryset = Customer.objects.filter(is_active=True)
    serializer_class = CustomerSerializer
    permission_classes = (IsCustomerAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomerFilter

    @action(
        methods=["get"],
        detail=False,
        serializer_class=CustomerSpentMoneySerializer,
        url_path="money-spent",
    )
    def get_amount_money_spent(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)


class ProviderViewSet(BaseViewSet):
    queryset = Provider.objects.filter(is_active=True)
    serializer_class = ProviderSerializer
    permission_classes = (IsProviderAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProviderFilter

    @action(
        detail=True,
        methods=["post"],
        url_path="add-car",
    )
    def add_provider_cars(self, request, pk=None):
        provider = self.get_object()
        car_id = request.data.get("car_id")
        if not is_valid_id(car_id):
            return Response(
                {"error": "Id must be numeric"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        car = get_object_or_404(Car, pk=car_id)

        price = request.data.get("price")
        try:
            ProviderCars.objects.create(car=car, provider=provider, price=price)
        except IntegrityError:
            return Response(
                {"error": "This car already exists in this provider"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_200_OK)


class CarShowroomDiscountViewSet(BaseViewSet):
    queryset = CarShowroomDiscount.objects.filter(is_active=True)
    serializer_class = CarShowroomDiscountSerializer
    permission_classes = (IsShowroomAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CarShowroomDiscountFilter

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        showroom = request.data["showroom"]
        cars = find_cars_by_specification(request.data["params"])
        percent = request.data["percent"]
        for car in cars:
            showroom_car_price = (
                ShowroomCars.objects.filter(showroom__id=showroom)
                .select_related("car")
                .get(car__id=car.id)
            )
            showroom_car_price.save(percent=percent)

        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        instance = self.get_object()
        showroom = instance.showroom
        cars = find_cars_by_specification(instance.params)
        percent = instance.percent
        for car in cars:
            showroom_car_price = (
                ShowroomCars.objects.filter(showroom__id=showroom.id)
                .select_related("car")
                .get(car__id=car.id)
            )
            showroom_car_price.save(percent=percent)
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        showroom = instance.showroom
        cars = find_cars_by_specification(instance.params)
        for car in cars:
            showroom_car_price = (
                ShowroomCars.objects.filter(showroom__id=showroom.id)
                .select_related("car")
                .get(car__id=car.id)
            )
            showroom_car_price.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProviderDiscountListView(APIView):
    permission_classes = (IsProviderAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProviderDiscountFilter

    def get(self, request):
        discount = ProviderDiscount.objects.filter(is_active=True)
        serializer = ProviderDiscountSerializer(instance=discount, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProviderDiscountSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            provider = request.data["provider"]
            cars = find_cars_by_specification(request.data["params"])
            percent = request.data["percent"]
            for car in cars:
                provider_car_price = (
                    ProviderCars.objects.filter(provider__id=provider)
                    .select_related("car")
                    .get(car__id=car.id)
                )
                provider_car_price.save(percent=percent)

            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProviderDiscountDetailView(APIView):
    permission_classes = (IsProviderAdminOrReadOnly,)

    def get(self, request, pk):
        discount = get_object_or_404(ProviderDiscount, pk=pk, is_active=True)
        serializer = ProviderDiscountSerializer(instance=discount)
        return Response(serializer.data)

    def put(self, request, pk):
        discount = get_object_or_404(ProviderDiscount, pk=pk, is_active=True)
        serializer = ProviderDiscountSerializer(
            instance=discount, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            provider = discount.provider
            cars = find_cars_by_specification(discount.params)
            percent = discount.percent

            for car in cars:
                provider_car_price = (
                    ProviderCars.objects.filter(provider__id=provider.id)
                    .select_related("car")
                    .get(car__id=car.id)
                )
                provider_car_price.save(percent=percent)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        discount = get_object_or_404(ProviderDiscount, pk=pk, is_active=True)
        discount.is_active = False
        discount.save()

        provider = discount.provider
        cars = find_cars_by_specification(discount.params)
        for car in cars:
            try:
                provider_car_price = (
                    ProviderCars.objects.filter(provider__id=provider.id)
                    .select_related("car")
                    .get(car__id=car.id)
                )
            except ProviderCars.DoesNotExist:
                provider_car_price = None
            if provider_car_price:
                provider_car_price.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CarShowroomSalesHistoryViewSet(BaseViewSet):
    queryset = CarShowroomSalesHistory.objects.filter(is_active=True)
    serializer_class = CarShowroomSalesHistorySerializer
    permission_classes = (IsShowroomAdmin,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CarShowroomSalesHistoryFilter


class ProviderSalesHistoryViewSet(BaseViewSet):
    queryset = ProviderSalesHistory.objects.filter(is_active=True)
    serializer_class = ProviderSalesHistorySerializer
    permission_classes = (IsProviderAdmin,)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = UserFilter
